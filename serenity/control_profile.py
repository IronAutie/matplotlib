#!/usr/bin/env python3
"""Control experiment: call-count profiling of stock mplot3d.

Unit of measurement: CALLS, not time. Counts are deterministic and
machine-independent, which is the point of the control.

Workload: the parked example cube (235,944 segments) drawn through
mpl_toolkits.mplot3d Line3DCollection on the Agg backend. One warmup
draw (unprofiled), then N profiled draws; counts are reported per draw
so draw-to-draw determinism can be checked directly.

Python function calls are counted from sys.setprofile 'call' events;
C function calls from 'c_call' events. Only events whose code lives
under the matplotlib package directory are itemized; global totals
are also kept.
"""
import json
import sys
from collections import Counter

import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Line3DCollection  # noqa: E402

MPL_DIR = matplotlib.__file__.rsplit("/", 2)[0] + "/"  # dist-packages root
SEGMENTS = "/home/hatch/workspace/iscandar/example-cube/segments.npz"
DRAWS = 2

py_calls = Counter()   # (file, line, name) -> count, matplotlib files only
c_calls = Counter()    # C function name -> count
totals = Counter()     # all 'call' and 'c_call' events, everywhere


def profiler(frame, event, arg):
    if event == "call":
        totals["py_call_all"] += 1
        code = frame.f_code
        filename = code.co_filename
        if filename.startswith(MPL_DIR + "matplotlib/") or filename.startswith(MPL_DIR + "mpl_toolkits/"):
            key = (filename[len(MPL_DIR):], code.co_firstlineno, code.co_name)
            py_calls[key] += 1
    elif event == "c_call":
        totals["c_call_all"] += 1
        name = getattr(arg, "__qualname__", None) or getattr(arg, "__name__", None) or repr(arg)
        mod = getattr(arg, "__self__", None)
        modname = type(mod).__name__ if mod is not None else ""
        c_calls[(modname + "." + name) if modname else name] += 1


def main():
    data = np.load(SEGMENTS)
    endpoints = data["endpoints"].astype(np.float64)
    rgb = data["rgb"].astype(np.float64) / 255.0
    rgba = np.concatenate([rgb, np.ones((rgb.shape[0], 1))], axis=1)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")
    coll = Line3DCollection(endpoints, colors=rgba)
    ax.add_collection3d(coll)
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 32)
    ax.set_zlim(0, 32)

    fig.canvas.draw()  # warmup, unprofiled

    per_draw = []
    for i in range(DRAWS):
        py_calls.clear()
        c_calls.clear()
        totals.clear()
        sys.setprofile(profiler)
        try:
            fig.canvas.draw()
        finally:
            sys.setprofile(None)
        per_draw.append({
            "draw": i + 1,
            "totals": dict(totals),
            "py_calls": {"{}:{}:{}".format(f, ln, nm): c
                         for (f, ln, nm), c in py_calls.items()},
            "c_calls": dict(c_calls),
        })
        print("draw {} done: py_call_all={} c_call_all={} mpl_py_entries={}".format(
            i + 1, totals["py_call_all"], totals["c_call_all"], len(py_calls)),
            flush=True)

    out = {
        "matplotlib_version": matplotlib.__version__,
        "matplotlib_dir": MPL_DIR,
        "python_version": sys.version.split()[0],
        "segments": int(endpoints.shape[0]),
        "draws": per_draw,
    }
    with open("/home/hatch/workspace/serenity-profiling/control_run.json", "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("wrote control_run.json")


if __name__ == "__main__":
    main()
