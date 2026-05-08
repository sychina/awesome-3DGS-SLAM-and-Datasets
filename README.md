# Awesome 3DGS-SLAM & Datasets

> A curated and maintainable literature list for **3D Gaussian Splatting SLAM (3DGS-SLAM)**, related radiance-field SLAM methods, and benchmark datasets.
>
> 本仓库重点关注：在线 SLAM、跟踪/建图、3DGS/2DGS/Surfels 表示、RGB-D / monocular / stereo / LiDAR 输入、语义/动态/大规模场景，以及可复现实验配置。

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing)
[![Maintained](https://img.shields.io/badge/maintained-yes-blue.svg)](#maintenance-policy)
[![Topic](https://img.shields.io/badge/topic-3DGS--SLAM-orange.svg)](#scope)

[![Open Website](https://img.shields.io/badge/Open-Website-7c3aed?style=for-the-badge&logo=githubpages&logoColor=white)](https://sychina.github.io/awesome-3DGS-SLAM-and-Datasets/) 

## Scope

This repository tracks papers and datasets related to 3DGS-SLAM, including:

- **Core 3DGS-SLAM**: tracking, mapping, pose optimization, differentiable rendering, online Gaussian map update.
- **Input modalities**: RGB-D, monocular/RGB-only, stereo, LiDAR, event camera, visual-inertial, multi-modal.
- **Scene assumptions**: static, dynamic, semantic/open-vocabulary, large-scale, multi-robot/collaborative.
- **Evaluation resources**: public datasets, metrics, official code, reproducibility notes.

Non-goals: pure offline novel-view synthesis papers are included only when they strongly affect SLAM initialization, tracking, or map optimization.


## Taxonomy

### By input modality

| Category | Typical goal | Typical datasets | Notes |
|---|---|---|---|
| RGB-D 3DGS-SLAM | Dense tracking + mapping with depth supervision | Replica, TUM RGB-D, ScanNet, ScanNet++ | Usually strongest geometry supervision and easiest reproduction. |
| Monocular / RGB-only | Dense SLAM without sensor depth | Replica, TUM RGB-D RGB-only protocol, ScanNet | Often needs learned depth, global optimization, or robust initialization. |
| Stereo / VIO | Scale-aware visual SLAM | EuRoC, KITTI, TartanAir | Useful for robotics deployment; may combine existing SLAM frontend with GS map. |
| LiDAR / RGB-LiDAR | Large-scale geometry and outdoor mapping | KITTI, KITTI-360, NCLT, MulRan | Track map size, streaming, and memory carefully. |
| Event camera | High-speed / high-dynamic-range SLAM | Event camera datasets | Often specialized tracking and asynchronous update. |
| Semantic / language | Map perception and querying | ScanNet, ScanNet++, Replica semantic variants | Include open-vocabulary, object-level, feature-field methods. |
| Dynamic scenes | Robust tracking and map update under moving objects | TUM dynamic, Bonn RGB-D Dynamic, ScanNet videos | Separate static map quality from dynamic filtering accuracy. |

### By method component

- **Tracking**: frame-to-model, frame-to-frame, photometric loss, depth loss, feature loss, ICP/GICP, learned correspondence, bundle adjustment.
- **Mapping**: Gaussian initialization, densification, pruning, keyframe selection, local/global map update, submap fusion.
- **Representation**: 3D Gaussian ellipsoids, 2D Gaussian surfels, compact GS, semantic/feature Gaussians, mesh+GS hybrids.
- **Optimization**: differentiable rasterization, coarse-to-fine tracking, global BA, loop closure, pose graph optimization.
- **Efficiency**: FPS, VRAM, number of Gaussians, map size, streaming latency, embedded GPU support.

## Representative papers

> This is a starter list. Prefer editing `data/papers.yml` and regenerating this table.

### Surveys and collections

| Year | Venue | Paper / Resource | Category | Summary |
|---:|---|---|---|---|
| 2024 | arXiv | [How NeRFs and 3D Gaussian Splatting are Reshaping SLAM: a Survey](https://arxiv.org/abs/2402.13255) | Survey | Reviews neural/radiance-field SLAM progress and positions 3DGS as a key explicit radiance-field representation for SLAM. |
| active | GitHub | [Awesome-3DGS-SLAM](https://github.com/KwanWaiPang/Awesome-3DGS-SLAM) | Collection | Useful cross-check list covering image-, LiDAR-, and event-based 3DGS-SLAM works. |

### RGB-D / dense SLAM

| Year | Venue | Paper | Code | Modality | Representation | Datasets | Metrics | Summary | Local Eval |
|---:|---|---|---|---|---|---|---|---|---|
| 2024 | CVPR Highlight | [GS-SLAM: Dense Visual SLAM with 3D Gaussian Splatting](https://gs-slam.github.io/) | [code](https://github.com/yanchi-3dv/diff-gaussian-rasterization-for-gsslam) | RGB-D | 3DGS | Replica, TUM RGB-D | ATE, PSNR, SSIM, LPIPS, FPS | Uses a differentiable splatting pipeline, adaptive Gaussian expansion/pruning, and coarse-to-fine camera tracking for real-time dense RGB-D SLAM. | reproduce pending |
| 2024 | CVPR | [SplaTAM: Splat, Track & Map 3D Gaussians for Dense RGB-D SLAM](https://spla-tam.github.io/) | [code](https://github.com/spla-tam/SplaTAM) | RGB-D | 3DGS | Replica, TUM RGB-D, ScanNet | ATE, PSNR, SSIM, LPIPS, depth L1 | Online tracking and mapping with explicit 3D Gaussians; uses silhouette-aware map expansion to decide observed/unobserved regions. | reproduce pending |
| 2025 | arXiv | [GauS-SLAM: Dense RGB-D SLAM with Gaussian Surfels](https://github.com/gaus-slam/gaus-slam) | [code](https://github.com/gaus-slam/gaus-slam) | RGB-D | Gaussian surfels / 2DGS-style surface map | Replica, TUM RGB-D, ScanNet, ScanNet++ | ATE, rendering metrics, reconstruction | Surface-oriented Gaussian map for dense localization and reconstruction; include if tracking surfel-style 3DGS variants. | not tested |
| 2025 | arXiv | [2DGS-SLAM: Globally Consistent RGB-D SLAM with 2D Gaussian Splatting](https://arxiv.org/html/2506.00970v1) | [code](https://github.com/PRBonn/2DGS-SLAM) | RGB-D | 2D Gaussian primitives | Replica, ScanNet, TUM configs | ATE, rendering, geometry | Focuses on globally consistent RGB-D SLAM with surface-aligned 2D Gaussian primitives. | not tested |

### Monocular / RGB-only / multi-sensor

| Year | Venue | Paper | Code | Modality | Representation | Datasets | Metrics | Summary | Local Eval |
|---:|---|---|---|---|---|---|---|---|---|
| 2024 | CVPR Highlight | [Gaussian Splatting SLAM / MonoGS](https://github.com/muskie82/MonoGS) | [code](https://github.com/muskie82/MonoGS) | monocular, stereo, RGB-D | 3DGS | TUM RGB-D, Replica, others | ATE, rendering, FPS | First monocular SLAM system solely based on 3DGS; repository also supports stereo/RGB-D modes. | reproduce pending |
| 2024 | arXiv / CVPRW 2025 | [Splat-SLAM: Globally Optimized RGB-only SLAM with 3D Gaussians](https://arxiv.org/abs/2405.16544) | [code](https://github.com/eriksandstroem/Splat-SLAM) | RGB-only | 3DGS + global optimization | Replica, TUM RGB-D, ScanNet | ATE, mapping, rendering, runtime | RGB-only dense SLAM with globally optimized tracking and dynamic updates to the Gaussian map. | not tested |

### Dynamic, semantic, large-scale, and specialized settings

| Year | Venue | Paper | Code | Modality | Focus | Datasets | Summary | Local Eval |
|---:|---|---|---|---|---|---|---|---|
| 2026 | Pattern Recognition | RGD-SLAM: Robust Gaussian Splatting SLAM for Dynamic Environments | TBD | RGB-D / visual | Dynamic scenes | TBD | Robust 3DGS-based dense SLAM for dynamic scenes; track separately because dynamic filtering metrics differ from static reconstruction metrics. | not tested |
| 2026 | arXiv | LangGS-SLAM: Real-Time Language-Feature Gaussian Splatting SLAM | TBD | RGB-D / visual-language | Language features | TBD | Adds language/open-vocabulary feature fields to Gaussian SLAM; useful for semantic map querying. | not tested |

## Datasets

| Dataset | Type | Sensors / data | Ground truth | Common use in 3DGS-SLAM | Notes |
|---|---|---|---|---|---|
| [Replica](https://github.com/facebookresearch/Replica-Dataset) | Synthetic / reconstructed indoor | Dense mesh, HDR textures, semantic labels | Mesh / rendered trajectories depending protocol | Rendering quality, reconstruction, controlled indoor scenes | Good for PSNR/SSIM/LPIPS and depth/reconstruction evaluation. |
| [TUM RGB-D](https://cvg.cit.tum.de/data/datasets/rgbd-dataset) | Real indoor RGB-D | RGB, depth, Kinect accelerometer | Motion-capture trajectory | ATE tracking benchmark, RGB-D SLAM baseline | Include exact sequence and association script. |
| [ScanNet](https://www.scan-net.org/) | Real indoor RGB-D video | RGB-D videos, poses, reconstructions, semantics | Camera poses, reconstructions, semantic/instance labels | Real-world dense reconstruction and semantic evaluation | Access approval may be required. |
| [ScanNet++](https://scannetpp.mlsg.cit.tum.de/scannetpp/) | High-fidelity real indoor | Laser scans, DSLR images, iPhone RGB-D streams | High-quality geometry and annotations | High-fidelity reconstruction / NVS / semantic benchmarks | Useful for testing high-quality map rendering and geometry. |
| [EuRoC MAV](https://projects.asl.ethz.ch/datasets/euroc-mav/) | Visual-inertial MAV | Stereo images, synchronized IMU | Accurate motion and structure ground truth | VIO / stereo / loop-closure variants | Track scale, IMU usage, and sequence difficulty. |
| [KITTI Odometry](https://www.cvlibs.net/datasets/kitti/eval_odometry.php) | Outdoor driving | Stereo, LiDAR-compatible benchmark protocols | GT for training sequences 00-10 | Large-scale visual/LiDAR SLAM | Use for outdoor scalability, trajectory drift, map memory. |

## Maintenance policy

### Sorting rules

1. Sort by **year descending**.
2. Within the same year, sort by **venue rank / publication status**: journal / main conference / workshop / arXiv.
3. Within the same venue, sort by **paper title A-Z**.
4. Keep survey and benchmark papers in separate sections even if they are highly cited.

### Required fields for every paper

| Field | Required | Description |
|---|---:|---|
| `id` | yes | Stable slug, e.g. `gs_slam_2024` |
| `year` | yes | Publication year |
| `venue` | yes | CVPR, ICCV, IROS, arXiv, etc. |
| `title` | yes | Paper title |
| `paper` | yes | arXiv / DOI / project / CVF link |
| `code` | optional | Official repository if available |
| `modality` | yes | RGB-D, monocular, stereo, LiDAR, event, VIO |
| `representation` | yes | 3DGS, 2DGS, Gaussian surfels, hybrid mesh+GS, etc. |
| `datasets` | yes | Evaluation datasets |
| `metrics` | recommended | ATE, PSNR, SSIM, LPIPS, depth L1, FPS, memory |
| `summary` | yes | 1-2 sentence contribution summary |
| `tags` | recommended | `loop-closure`, `dynamic`, `semantic`, `large-scale`, etc. |
| `local_eval` | public-safe | `not tested`, `tested locally`, `reproduce pending` |

### Status labels

- `paper-only`: no public code found.
- `code-released`: official implementation released.
- `reproduce-pending`: code exists but local reproduction not done.
- `tested-locally`: tested privately; raw numbers are not public.
- `archived`: outdated or superseded, kept for history.

## Contributing

Please open a PR with changes to `data/papers.yml` or `data/datasets.yml`. A good paper entry includes:

1. paper link and official code link;
2. one-sentence contribution summary;
3. input modality and map representation;
4. evaluated datasets and metrics;
5. tags for filtering.

Do not submit private/local benchmark numbers unless they are intentionally public and reproducible.

## License

Suggested: CC-BY-4.0 for the list content and MIT for scripts. Check the license compatibility of any copied text, figures, or tables before adding them.
