# Control experiment: stock mplot3d, call-count profile

Date: 2026-11-02. Harness: control_profile.py (sys.setprofile).
Unit of measurement: CALLS, not time.

- Library under test: matplotlib 3.6.3 (system install, the autopsied copy)
- Python: 3.12.3
- Workload: example cube, 235,944 segments, Line3DCollection, Agg, one full draw
- Per single steady-state draw: **6,391,206 Python calls total**, of which **4,264,451 inside matplotlib + mpl_toolkits files**; **4,964,486 C calls**.
- Determinism: draw 1 = draw 2 within a run, and independent process runs reproduce identical counts.

## Calls by file, mpl_toolkits/mplot3d (total 944,265)

- mpl_toolkits/mplot3d/proj3d.py: 944,121
- mpl_toolkits/mplot3d/axis3d.py: 78
- mpl_toolkits/mplot3d/axes3d.py: 53
- mpl_toolkits/mplot3d/art3d.py: 13

## Top 25 Python functions by calls (matplotlib + mpl_toolkits)

- 707,976  matplotlib/_api/__init__.py:154:<genexpr>
- 472,620  matplotlib/__init__.py:662:__getitem__
- 236,651  matplotlib/artist.py:265:axes
- 236,095  matplotlib/path.py:211:vertices
- 236,064  matplotlib/cbook/__init__.py:1361:_to_unmasked_float_array
- 236,046  mpl_toolkits/mplot3d/proj3d.py:120:_proj_transform_vec
- 236,046  mpl_toolkits/mplot3d/proj3d.py:150:_vec_pad_ones
- 236,046  mpl_toolkits/mplot3d/proj3d.py:154:proj_transform
- 235,994  matplotlib/path.py:225:codes
- 235,994  matplotlib/path.py:244:simplify_threshold
- 235,994  matplotlib/path.py:256:should_simplify
- 235,992  matplotlib/_api/__init__.py:134:check_shape
- 235,992  matplotlib/path.py:202:_update_values
- 235,992  matplotlib/path.py:99:__init__
- 235,974  mpl_toolkits/mplot3d/proj3d.py:179:proj_trans_points
- 1,042  matplotlib/artist.py:816:get_animated
- 1,037  matplotlib/artist.py:289:stale
- 342  matplotlib/transforms.py:110:__init__
- 306  matplotlib/artist.py:904:get_rasterized
- 306  matplotlib/artist.py:929:get_agg_filter
- 274  matplotlib/_api/__init__.py:101:check_in_list
- 252  matplotlib/transforms.py:1769:__init__
- 218  matplotlib/transforms.py:1926:get_matrix
- 216  matplotlib/font_manager.py:782:get_size
- 210  matplotlib/font_manager.py:737:get_family

## Top 25 C calls by calls

- 708,299  module.len
- 708,194  module.array
- 472,620  RcParams.RcParams.__getitem__
- 472,208  module.asarray
- 472,185  module.hasattr
- 472,167  list.list.append
- 472,135  module.asanyarray
- 471,930  module.min
- 237,196  module.isinstance
- 236,806  dict.dict.items
- 236,012  module.any
- 672  module.getattr
- 614  dict.dict.get
- 338  ndarray.ndarray.copy
- 315  module.hash
- 213  ufunc.ufunc.reduce
- 174  module.next
- 147  module.issubclass
- 126  str.str.count
- 124  module.id
- 102  Pattern.Pattern.match
- 97  ndarray.ndarray.reshape
- 87  type.object.__new__
- 86  module.max
- 84  module.affine_transform

## Reading

Control numbers for the unmodified library. Future Serenity builds
are compared against them in the same units.
