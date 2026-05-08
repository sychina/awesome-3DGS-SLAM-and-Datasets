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

> This section is generated from `data/papers.yml` and `data/datasets.yml`. Do not edit the tables manually. Use `readme_group` in `data/papers.yml` to override automatic classification.

### Surveys and collections

| Year | Venue | Paper / Resource | Category | Summary |
|---:|---|---|---|---|
| 2024 | arXiv | [How NeRFs and 3D Gaussian Splatting are Reshaping SLAM: a Survey](https://arxiv.org/abs/2402.13255) | Survey | Reviews neural/radiance-field SLAM progress and positions 3DGS as a key explicit radiance-field representation for SLAM. |
| active | GitHub | [Awesome-3DGS-SLAM](https://github.com/KwanWaiPang/Awesome-3DGS-SLAM) | Collection | Useful cross-check list covering image-, LiDAR-, and event-based 3DGS-SLAM works. |

### RGB-D / dense SLAM

| Year | Venue | Paper | Code | Modality | Representation | Datasets | Metrics | Summary | Local Eval |
|---:|---|---|---|---|---|---|---|---|---|
| 2026 | CVPR | [SGAD-SLAM: Splatting Gaussians at Adjusted Depth for Better Radiance Fields in RGBD SLAM](https://arxiv.org/pdf/2603.21055) | [code](https://github.com/MachinePerceptionLab/SGAD-SLAM) | RGB-D | Depth-adjusted 3DGS | TBD | ATE, rendering, depth | RGB-D Gaussian SLAM that adjusts Gaussian placement/depth for improved radiance fields. | not tested |
| 2025 | arXiv | [Globally Consistent RGB-D SLAM with 2D Gaussian Splatting](https://arxiv.org/pdf/2506.00970) | [code](https://github.com/PRBonn/2DGS-SLAM) | RGB-D | 2D Gaussian primitives | Replica, TUM RGB-D, ScanNet | ATE, geometry, rendering | Globally consistent RGB-D SLAM with surface-aligned 2D Gaussian primitives. | not tested |
| 2024 | CVPR | [SplaTAM: Splat, Track & Map 3D Gaussians for Dense RGB-D SLAM](https://spla-tam.github.io/) | [code](https://github.com/spla-tam/SplaTAM) | RGB-D | 3D Gaussian Splatting | Replica, TUM RGB-D, ScanNet | ATE, PSNR, SSIM, LPIPS, Depth L1 | Online dense RGB-D SLAM using explicit 3D Gaussians and silhouette-aware map expansion. | reproduce pending |
| 2024 | CVPR | [SplaTAM: Splat, Track & Map 3D Gaussians for Dense RGB-D SLAM](https://arxiv.org/pdf/2312.02126.pdf) | [code](https://github.com/spla-tam/SplaTAM) | RGB-D | 3DGS | Replica, TUM RGB-D, ScanNet | ATE, PSNR, SSIM, LPIPS, Depth L1 | Online dense RGB-D SLAM with explicit 3D Gaussians and silhouette-aware map expansion. | reproduce pending |
| 2024 | CVPR Highlight | [GS-SLAM: Dense Visual SLAM with 3D Gaussian Splatting](https://gs-slam.github.io/) | [code](https://github.com/yanchi-3dv/diff-gaussian-rasterization-for-gsslam) | RGB-D | 3D Gaussian Splatting | Replica, TUM RGB-D | ATE, PSNR, SSIM, LPIPS, FPS | Differentiable splatting pipeline with adaptive Gaussian expansion/pruning and coarse-to-fine camera tracking for real-time dense RGB-D SLAM. | reproduce pending |
| 2024 | ECCV | [CG-SLAM: Efficient Dense RGB-D SLAM in a Consistent Uncertainty-aware 3D Gaussian Field](https://arxiv.org/pdf/2403.16095.pdf) | [code](https://github.com/hjr37/CG-SLAM) | RGB-D | Uncertainty-aware 3DGS | TBD | ATE, uncertainty, rendering | RGB-D Gaussian SLAM method emphasizing uncertainty-aware and consistent dense mapping. | not tested |
| 2024 | ECCV | [RGBD GS-ICP SLAM](https://arxiv.org/pdf/2403.12550.pdf) | [code](https://github.com/Lab-of-AI-and-Robotics/GS_ICP_SLAM) | RGB-D | 3DGS + ICP | TBD | ATE, ICP residual, rendering | RGB-D SLAM variant coupling Gaussian maps with ICP-style geometric alignment. | not tested |
| 2024 | RAL | [GSFusion: Online RGB-D Mapping Where Gaussian Splatting Meets TSDF Fusion](https://arxiv.org/pdf/2408.12677) | [code](https://github.com/goldoak/GSFusion) | RGB-D | 3DGS + TSDF fusion | TBD | reconstruction, rendering, FPS | Combines online RGB-D Gaussian mapping with TSDF-style fusion ideas. | not tested |
| 2024 | arXiv | [FlashSLAM: Accelerated RGB-D SLAM for Real-Time 3D Scene Reconstruction with Gaussian Splatting](https://arxiv.org/pdf/2412.00682) | TBD | RGB-D | Accelerated 3DGS | TBD | ATE, FPS, memory | Accelerated RGB-D Gaussian SLAM targeting real-time 3D reconstruction. | not tested |
| 2024 | arXiv | [High-Fidelity SLAM Using Gaussian Splatting with Rendering-Guided Densification and Regularized Optimization](https://arxiv.org/pdf/2403.12535.pdf) | TBD | RGB-D | Rendering-guided 3DGS densification | Replica, TUM RGB-D | ATE, PSNR, SSIM, LPIPS | Dense RGB-D Gaussian SLAM focusing on rendering-guided densification and regularized optimization for high-fidelity mapping. | not tested |
| 2023 | arXiv | [Gaussian-SLAM: Photo-realistic Dense SLAM with Gaussian Splatting](https://arxiv.org/pdf/2312.10070.pdf) | [code](https://github.com/VladimirYugay/Gaussian-SLAM) | RGB-D | 3DGS | TBD | ATE, rendering | Early photo-realistic dense SLAM work using Gaussian Splatting for map representation. | not tested |

### Monocular / RGB-only / multi-sensor

| Year | Venue | Paper | Code | Modality | Representation | Datasets | Metrics | Summary | Local Eval |
|---:|---|---|---|---|---|---|---|---|---|
| 2025 | ICCV | [SEGS-SLAM: Structure-enhanced 3D Gaussian Splatting SLAM with Appearance Embedding](https://arxiv.org/pdf/2501.05242) | [code](https://github.com/leaner-forever/SEGS-SLAM) | Monocular, RGB-D | Structure-enhanced 3DGS | TBD | ATE, rendering, geometry | Structure-enhanced Gaussian SLAM with appearance embedding. | not tested |
| 2025 | IROS | [MemGS: Memory-Efficient Gaussian Splatting for Real-Time SLAM](https://arxiv.org/pdf/2509.13536) | [code](https://github.com/NAIL-HNU/MemGS_SLAM) | RGB-D, Monocular | Memory-efficient 3DGS | TBD | memory, FPS, ATE | Memory-efficient Gaussian Splatting design for real-time SLAM. | not tested |
| 2025 | RAL | [GSORB-SLAM: Gaussian Splatting SLAM benefits from ORB features and Transmittance information](https://arxiv.org/pdf/2410.11356) | [code](https://github.com/Aczheng-cai/GSORB-SLAM) | Monocular, RGB-D | 3DGS + ORB features | TBD | ATE, feature tracking, rendering | Combines ORB features and transmittance cues with Gaussian Splatting SLAM. | not tested |
| 2025 | TRO | [HI-SLAM2: Geometry-Aware Gaussian SLAM for Fast Monocular Scene Reconstruction](https://arxiv.org/pdf/2411.17982) | [code](https://github.com/Willyzw/HI-SLAM2) | Monocular | Geometry-aware 3DGS | TBD | ATE, reconstruction, FPS | Fast monocular Gaussian SLAM with geometry-aware scene reconstruction. | not tested |
| 2024 | CVPR | [Gaussian Splatting SLAM / MonoGS](https://arxiv.org/pdf/2312.06741.pdf) | [code](https://github.com/muskie82/MonoGS) | Monocular, Stereo, RGB-D | 3DGS | Replica, TUM RGB-D | ATE, PSNR, SSIM, FPS | Monocular-first Gaussian SLAM system, with repository support for stereo and RGB-D inputs. | reproduce pending |
| 2024 | CVPR | [Gaussian-SLAM: Photo-realistic Dense SLAM with Gaussian Splatting](https://arxiv.org/abs/2312.10070) | [code](https://github.com/vladimiryugay/Gaussian-SLAM) | RGB-D, Monocular | 3D Gaussian Splatting | Replica, TUM RGB-D, ScanNet | ATE, PSNR, SSIM, LPIPS | 采用子地图策略的 3DGS SLAM 系统，将全局地图划分为多个局部高斯子图，控制了随场景扩大的显存消耗。 | not tested |
| 2024 | CVPR Highlight | [Gaussian Splatting SLAM / MonoGS](https://rmurai.co.uk/projects/GaussianSplattingSLAM/) | [code](https://github.com/muskie82/MonoGS) | Monocular, Stereo, RGB-D | 3D Gaussian Splatting | TUM RGB-D, Replica | ATE, rendering, FPS | Monocular-first 3DGS SLAM system, with repository support for stereo and RGB-D inputs. | reproduce pending |
| 2024 | ICCV Workshop | [DROID-Splat: Combining end-to-end SLAM with 3D Gaussian Splatting](https://arxiv.org/pdf/2411.17660) | [code](https://github.com/ChenHoy/DROID-Splat) | Monocular, RGB-D | End-to-end SLAM + 3DGS | TBD | ATE, rendering, runtime | Combines an end-to-end SLAM backbone with Gaussian Splatting map rendering. | not tested |
| 2024 | RAL | [MGS-SLAM: Monocular Sparse Tracking and Gaussian Mapping with Depth Smooth Regularization](https://arxiv.org/pdf/2405.06241) | [code](https://github.com/Z-Pengcheng/MGS-SLAM) | Monocular | 3DGS + sparse tracking | TBD | ATE, rendering, FPS | Monocular Gaussian SLAM with sparse tracking and depth-smooth regularization. | not tested |
| 2024 | arXiv | [TAMBRIDGE: Bridging Frame-Centered Tracking and 3D Gaussian Splatting for Enhanced SLAM](https://arxiv.org/pdf/2405.19614) | [code](https://github.com/ZeldaFromHeaven/TAMBRIDGE-DAVID) | Monocular, RGB-D | 3DGS | TBD | ATE, rendering | Studies the interaction between frame-centered tracking and Gaussian map optimization. | not tested |
| 2024 | arXiv / CVPRW | [Splat-SLAM: Globally Optimized RGB-only SLAM with 3D Gaussians](https://arxiv.org/pdf/2405.16544) | [code](https://github.com/eriksandstroem/Splat-SLAM) | RGB-only, Monocular | 3DGS + global optimization | Replica, TUM RGB-D, ScanNet | ATE, PSNR, SSIM, FPS | RGB-only dense SLAM with globally optimized tracking and updates to a Gaussian map. | not tested |

### Dynamic, semantic, large-scale, and specialized settings

| Year | Venue | Paper | Code | Modality | Focus | Datasets | Summary | Local Eval |
|---:|---|---|---|---|---|---|---|---|
| 2026 | AAAI | [CoMA-SLAM: Collaborative Multi-Agent Gaussian SLAM with Geometric Consistency](https://ojs.aaai.org/index.php/AAAI/article/view/37283) | [code](https://github.com/npu-chenlin/CoMA-SLAM) | Multi-agent, RGB-D | Collaborative 3DGS-SLAM | TBD | Collaborative multi-agent Gaussian SLAM emphasizing geometric consistency. | not tested |
| 2026 | CVPR | [Unblur-SLAM: Dense Neural SLAM for Blurry Inputs](https://arxiv.org/pdf/2603.26810) | [code](https://github.com/SlamMate/Unblur-SLAM) | Monocular, RGB-D | Robust 3DGS-SLAM | Blurry datasets, TBD | Dense SLAM method targeting blurry inputs. | not tested |
| 2026 | CVPR | [VarSplat: Uncertainty-aware 3D Gaussian Splatting for Robust RGB-D SLAM](https://arxiv.org/pdf/2603.09673) | [code](https://github.com/anhthuan1999/varsplat) | RGB-D | Visual 3DGS-SLAM | TBD | Uncertainty-aware Gaussian Splatting for robust RGB-D SLAM. | not tested |
| 2026 | Pattern Recognition | [RGD-SLAM: Robust Gaussian Splatting SLAM for Dynamic Environments](https://www.sciencedirect.com/science/article/abs/pii/S0031320326000348) | [code](https://github.com/00Haocheng/RGD-SLAM) | RGB-D, Dynamic | Dynamic 3DGS-SLAM | TBD | Robust Gaussian Splatting SLAM method for dynamic environments. | not tested |
| 2026 | RAL | [DiskChunGS: Large-Scale 3D Gaussian SLAM Through Chunk-Based Memory Management](https://arxiv.org/pdf/2511.23030) | [code](https://github.com/leggedrobotics/DiskChunGS) | Monocular, RGB-D, Outdoor | Large-scale 3DGS-SLAM | TBD | Large-scale Gaussian SLAM with chunk-based memory management. | not tested |
| 2026 | RAL | [GauS-SLAM: Dense RGB-D SLAM with Gaussian Surfels](https://arxiv.org/pdf/2505.01934) | [code](https://github.com/gaus-slam/gaus-slam) | RGB-D | Surface / Surfel 3DGS-SLAM | Replica, TUM RGB-D, ScanNet, ScanNet++ | Dense RGB-D SLAM using surface-aligned Gaussian surfels for localization and reconstruction. | not tested |
| 2026 | WACV | [DynaGSLAM: Real-Time Gaussian-Splatting SLAM for Online Rendering, Tracking, Motion Predictions of Moving Objects in Dynamic Scenes](https://arxiv.org/pdf/2503.11979) | [code](https://github.com/BlarkLee/DynaGSLAM_official) | RGB-D, Dynamic | Dynamic 3DGS-SLAM | TBD | Dynamic Gaussian SLAM for online rendering, tracking, and motion prediction of moving objects. | not tested |
| 2026 | arXiv | [LangGS-SLAM: Real-Time Language-Feature Gaussian Splatting SLAM](https://arxiv.org/pdf/2602.06991) | TBD | RGB-D, Language, Open-vocabulary | Language / Open-vocabulary 3DGS-SLAM | TBD | Real-time Gaussian SLAM with language-feature map representation. | not tested |
| 2026 | arXiv | [M3: Dense Matching Meets Multi-View Foundation Models for Monocular Gaussian Splatting SLAM](https://arxiv.org/pdf/2603.16844) | [code](https://github.com/InternRobotics/M3) | Monocular, Features | Feature-enhanced 3DGS-SLAM | TBD | Monocular Gaussian SLAM combining dense matching with multi-view foundation models. | not tested |
| 2025 | 3DV | [LoopSplat: Loop Closure by Registering 3D Gaussian Splats](https://arxiv.org/pdf/2408.10154) | [code](https://github.com/GradientSpaces/LoopSplat) | Monocular, RGB-D | Loop closure / Global consistency | TBD | Uses registration of Gaussian splats for loop closure and global consistency. | not tested |
| 2025 | CVPR | [MAGiC-SLAM: Multi-Agent Gaussian Globally Consistent SLAM](https://arxiv.org/pdf/2411.16785) | [code](https://github.com/VladimirYugay/MAGiC-SLAM) | Multi-agent, RGB-D | Collaborative 3DGS-SLAM | TBD | Multi-agent Gaussian SLAM focused on globally consistent collaborative mapping. | not tested |
| 2025 | CVPR | [STDLoc: From Sparse to Dense: Camera Relocalization with Scene-Specific Detector from Feature Gaussian Splatting](https://zju3dv.github.io/stdloc/) | [code](https://github.com/zju3dv/STDLoc) | Visual Localization, 3DGS-map | Localization / Re-localization | 7-Scenes, Cambridge Landmarks, TBD | Camera relocalization using a scene-specific detector derived from feature Gaussian Splatting. | not tested |
| 2025 | CVPR | [WildGS-SLAM: Monocular Gaussian Splatting SLAM in Dynamic Environments](https://arxiv.org/pdf/2504.03886) | [code](https://github.com/GradientSpaces/WildGS-SLAM) | Monocular, Dynamic | Dynamic 3DGS-SLAM | TBD | Monocular Gaussian SLAM designed for dynamic, in-the-wild environments. | not tested |
| 2025 | ICCV | [4D Gaussian Splatting SLAM](https://arxiv.org/pdf/2503.16710) | [code](https://github.com/yanyan-li/4DGS-SLAM) | Monocular, Dynamic | Dynamic 3DGS-SLAM | TBD | Extends Gaussian SLAM toward dynamic/4D scene representation. | not tested |
| 2025 | ICCV | [DyGS-SLAM: Real-Time Accurate Localization and Gaussian Reconstruction for Dynamic Scenes](https://openaccess.thecvf.com/content/ICCV2025/papers/Hu_DyGS-SLAM_Real-Time_Accurate_Localization_and_Gaussian_Reconstruction_for_Dynamic_Scenes_ICCV_2025_paper.pdf) | TBD | Monocular, Dynamic | Dynamic 3DGS-SLAM | TBD | Real-time localization and Gaussian reconstruction for dynamic scenes. | not tested |
| 2025 | ICCV | Splat-LOAM: Gaussian Splatting LiDAR Odometry and Mapping | TBD | LiDAR | LiDAR-based 3DGS-SLAM | KITTI, MulRan, TBD | LiDAR odometry and mapping method using Gaussian Splatting. | not tested |
| 2025 | ICRA | [DGS-SLAM: Gaussian Splatting SLAM in Dynamic Environment](https://arxiv.org/pdf/2411.10722) | [code](https://github.com/kmk97/DGS-SLAM) | RGB-D, Dynamic | Dynamic 3DGS-SLAM | TBD | Gaussian Splatting SLAM method explicitly targeting dynamic environments. | not tested |
| 2025 | ICRA | [GARAD-SLAM: 3D GAussian splatting for Real-time Anti Dynamic SLAM](https://arxiv.org/pdf/2502.03228) | [code](https://github.com/DrLi-Ming/GARAD-SLAM) | RGB-D, Dynamic | Dynamic 3DGS-SLAM | TBD | Real-time anti-dynamic Gaussian SLAM intended to improve robustness under moving objects. | not tested |
| 2025 | ICRA | [Gaussian-LIC: Photo-realistic LiDAR-Inertial-Camera SLAM with 3D Gaussian Splatting](https://arxiv.org/pdf/2404.06926.pdf) | [code](https://github.com/APRIL-ZJU/Gaussian-LIC) | LiDAR, Camera, IMU, Multi-modal | Multimodal 3DGS-SLAM | KITTI, TBD | Photo-realistic LiDAR-inertial-camera SLAM with Gaussian Splatting. | not tested |
| 2025 | ICRA | [OpenGS-SLAM: Open-Set Dense Semantic SLAM with 3D Gaussian Splatting for Object-Level Scene Understanding](https://arxiv.org/pdf/2503.01646) | TBD | RGB-D, Semantic, Open-vocabulary | Semantic 3DGS-SLAM | ScanNet, Replica, TBD | Open-set object-level semantic Gaussian SLAM for dense scene understanding. | not tested |
| 2025 | ICRA | [OpenGS-SLAM: RGB-Only Gaussian Splatting SLAM for Unbounded Outdoor Scenes](https://arxiv.org/pdf/2502.15633) | TBD | RGB-only, Monocular, Outdoor | Outdoor 3DGS-SLAM | KITTI, KITTI-360, TBD | RGB-only Gaussian SLAM for unbounded outdoor scenes. | not tested |
| 2025 | IJCV | [CurvLoc: Surface Curvature Prompted Gaussian Splatting for Visual Localization](https://dl.acm.org/doi/10.1007/s11263-025-02440-1) | TBD | Visual Localization, 3DGS-map | Localization / Re-localization | TBD | Visual localization using surface curvature prompts in Gaussian Splatting maps. | not tested |
| 2025 | IROS | [FGS-SLAM: Fourier-based Gaussian Splatting for Real-time SLAM with Sparse and Dense Map Fusion](https://arxiv.org/pdf/2503.01109) | [code](https://github.com/3DV-Coder/FGS-SLAM) | RGB-D, Monocular | Visual 3DGS-SLAM | TBD | Real-time SLAM method using Fourier-based Gaussian Splatting and sparse/dense map fusion. | not tested |
| 2025 | IROS | [OpenGS-Fusion: Open-Vocabulary Dense Mapping with Hybrid 3D Gaussian Splatting for Refined Object-Level Understanding](https://arxiv.org/pdf/2508.01150) | [code](https://github.com/YOUNG-bit/OpenGS-Fusion) | RGB-D, Open-vocabulary, Semantic | Language / Open-vocabulary 3DGS-SLAM | TBD | Hybrid Gaussian dense mapping for open-vocabulary object-level understanding. | not tested |
| 2025 | IROS | SGLoc: Semantic Localization System for Camera Pose Estimation from 3D Gaussian Splatting Representation | TBD | Visual Localization, Semantic, 3DGS-map | Localization / Re-localization | TBD | Semantic localization system for estimating camera pose from 3DGS map representations. | not tested |
| 2025 | IROS | [SemGauss-SLAM: Dense Semantic Gaussian Splatting SLAM](https://arxiv.org/pdf/2403.07494.pdf) | [code](https://github.com/IRMVLab/SemGauss-SLAM) | RGB-D, Semantic | Semantic 3DGS-SLAM | TBD | Dense semantic 3DGS-SLAM system for jointly maintaining geometry, appearance, and semantic information. | not tested |
| 2025 | Journal of Autonomous Vehicles and Systems | [3DGS-Loc: 3D Gaussian Splatting for Map Representation and Visual Localization](https://asmedigitalcollection.asme.org/autonomousvehicles/article/doi/10.1115/1.4068379/1213167/3DGS-Loc-3D-Gaussian-Splatting-for-Map) | TBD | Visual Localization, 3DGS-map | Localization / Re-localization | TBD | Uses 3D Gaussian Splatting as a map representation for visual localization. | not tested |
| 2025 | RAL | [EGS-SLAM: RGB-D Gaussian Splatting SLAM with Events](https://arxiv.org/pdf/2508.07003) | [code](https://github.com/Chensiyu00/EGS-SLAM) | RGB-D, Event | Event 3DGS-SLAM | Event camera datasets, TBD | Combines RGB-D Gaussian Splatting SLAM with event-camera information. | not tested |
| 2025 | RAL | GS-Loc: A Vision Foundation Model-Driven 3D Gaussian Splatting Framework for Robust Visual Relocalization | TBD | Visual Localization, 3DGS-map, Features | Localization / Re-localization | TBD | Visual relocalization framework combining 3DGS with vision foundation model features. | not tested |
| 2025 | RAL | [RGBDS-SLAM: A RGB-D Semantic Dense SLAM Based on 3D Multi Level Pyramid Gaussian Splatting](https://arxiv.org/pdf/2412.01217) | [code](https://github.com/zhenzhongcao/RGBDS-SLAM) | RGB-D, Semantic | Semantic 3DGS-SLAM | TBD | RGB-D semantic dense SLAM using multi-level pyramid Gaussian Splatting. | not tested |
| 2025 | TIM | [LVI-GS: Tightly-coupled LiDAR-Visual-Inertial SLAM using 3D Gaussian Splatting](https://arxiv.org/pdf/2411.02703) | [code](https://github.com/arclab-hku/LVI-3DGS) | LiDAR, Camera, IMU, Multi-modal | Multimodal 3DGS-SLAM | TBD | Tightly coupled LiDAR-visual-inertial Gaussian SLAM. | not tested |
| 2025 | TRO | [GS-LIVO: Real-Time LiDAR, Inertial, and Visual Multi-sensor Fused Odometry with Gaussian Mapping](https://arxiv.org/pdf/2501.08672) | [code](https://github.com/HKUST-Aerial-Robotics/GS-LIVO) | LiDAR, Camera, IMU, Multi-modal | Multimodal 3DGS-SLAM | TBD | Real-time LiDAR-inertial-visual odometry with Gaussian mapping. | not tested |
| 2025 | TRO | [OmniMap: A General Mapping Framework Integrating Optics, Geometry, and Semantics](https://arxiv.org/pdf/2509.07500) | [code](https://github.com/BIT-DYN/omnimapde) | RGB-D, Semantic, Multi-modal | Semantic 3DGS-SLAM | TBD | General mapping framework integrating appearance, geometry, and semantic information. | not tested |
| 2025 | TRO | [VINGS-Mono: Visual-Inertial Gaussian Splatting Monocular SLAM in Large Scenes](https://arxiv.org/pdf/2501.08286) | [code](https://github.com/Fudan-MAGIC-Lab/VINGS-Mono) | Monocular, VIO | Visual-inertial 3DGS-SLAM | TBD | Visual-inertial monocular Gaussian SLAM for large-scale scenes. | not tested |
| 2025 | arXiv | [CityLoc: 6 DoF Localization of Text Descriptions in Large-Scale Scenes with Gaussian Representation](https://arxiv.org/pdf/2501.08982.pdf) | TBD | Text, Visual Localization, Large-scale, 3DGS-map | Localization / Re-localization | Large-scale localization datasets, TBD | Uses Gaussian scene representations and visual reasoning to refine 6-DoF localization from text descriptions. | not tested |
| 2025 | arXiv | [DINO-SLAM: DINO-informed RGB-D SLAM for Neural Implicit and Explicit Representations](https://arxiv.org/pdf/2507.19474) | TBD | RGB-D, Features | Feature-enhanced 3DGS-SLAM | TBD | Uses DINO-informed visual features for RGB-D SLAM across implicit and explicit scene representations. | not tested |
| 2025 | arXiv | [GauS-SLAM: Dense RGB-D SLAM with Gaussian Surfels](https://github.com/gaus-slam/gaus-slam) | [code](https://github.com/gaus-slam/gaus-slam) | RGB-D | surfel, dense-slam, scannet++ | Replica, TUM RGB-D, ScanNet, ScanNet++ | Dense RGB-D SLAM using surface-oriented Gaussian surfels for localization and high-fidelity reconstruction. | not tested |
| 2025 | arXiv | [GigaSLAM: Large-Scale Monocular SLAM with Hierachical Gaussian Splats](https://arxiv.org/pdf/2503.08071) | [code](https://github.com/DengKaiCQ/GigaSLAM) | Monocular, Outdoor | Large-scale 3DGS-SLAM | TBD | Large-scale monocular Gaussian SLAM using hierarchical Gaussian splats. | not tested |
| 2025 | arXiv | [LEG-SLAM: Language-Enhanced Gaussian Splatting for Real-Time SLAM](https://arxiv.org/pdf/2506.03073) | [code](https://github.com/Titrom025/LEG-SLAM/) | RGB-D, Language, Open-vocabulary | Language / Open-vocabulary 3DGS-SLAM | TBD | Adds language features to Gaussian SLAM for map querying and semantic understanding. | not tested |
| 2025 | arXiv | [LEGO-SLAM: Language-Embedded Gaussian Optimization SLAM](https://arxiv.org/pdf/2511.16144.pdf) | [code](https://github.com/Lab-of-AI-and-Robotics/LEGO-SLAM) | RGB-D, Language, Open-vocabulary | Language / Open-vocabulary 3DGS-SLAM | TBD | Real-time open-vocabulary 3DGS-SLAM with compact language embeddings and language-guided pruning. | not tested |
| 2025 | arXiv | [PINGS: Gaussian Splatting Meets Distance Fields within a Point-Based Implicit Neural Map](https://arxiv.org/pdf/2502.05752) | [code](https://github.com/PRBonn/PINGS) | LiDAR, RGB-D, Multi-modal | Hybrid representation SLAM | TBD | Hybrid map combining Gaussian Splatting with distance fields and a point-based implicit neural representation. | not tested |
| 2025 | arXiv | [VPGS-SLAM: Voxel-based Progressive 3D Gaussian SLAM in Large-Scale Scenes](https://arxiv.org/pdf/2505.18992) | [code](https://github.com/dtc111111/vpgs-slam) | RGB-D, LiDAR, Outdoor | Large-scale 3DGS-SLAM | TBD | Voxel-based progressive Gaussian SLAM for large-scale scenes. | not tested |
| 2024 | ACM MM | [GS3LAM: Gaussian Semantic Splatting SLAM](https://openreview.net/pdf?id=juMYrkJlV3) | [code](https://github.com/lif314/GS3LAM) | RGB-D, Semantic | Semantic 3DGS-SLAM | TBD | Semantic Gaussian Splatting SLAM method for integrating semantic cues into Gaussian maps. | not tested |
| 2024 | CVPR | [CG-SLAM: Efficient Dense RGB-D SLAM in a Consistent Uncertainty-aware 3D Gaussian Field](https://arxiv.org/abs/2403.16095) | [code](https://github.com/zju3dv/CG-SLAM) | RGB-D | dense-slam, uncertainty, efficiency | Replica, TUM RGB-D, ScanNet | 引入不确定性感知的 3DGS 场，通过信息矩阵指导高斯椭球的生成与修剪，提高了建图效率与内存利用率。 | not tested |
| 2024 | CVPR | [GS-SLAM: Dense Visual SLAM with 3D Gaussian Splatting](https://arxiv.org/pdf/2311.11700.pdf) | [code](https://github.com/yanchi-3dv/diff-gaussian-rasterization-for-gsslam) | RGB-D | Visual 3DGS-SLAM | Replica, TUM RGB-D | Dense RGB-D SLAM baseline using differentiable Gaussian splatting for tracking and online map optimization. | reproduce pending |
| 2024 | CVPR | [HUGS: Holistic Urban 3D Scene Understanding via Gaussian Splatting](https://arxiv.org/pdf/2403.12722.pdf) | [code](https://github.com/hyzhou404/HUGS) | RGB, Autonomous Driving, Dynamic, Semantic | Autonomous driving / scene understanding | KITTI, KITTI-360, Virtual KITTI 2 | 3DGS-based urban scene understanding with geometry, appearance, semantics, and moving-object modeling. | not tested |
| 2024 | CVPR | [Photo-SLAM: Real-time Simultaneous Localization and Photorealistic Mapping](https://arxiv.org/abs/2311.16728) | [code](https://github.com/huajianup/Photo-SLAM) | Monocular, Stereo, RGB-D | hybrid, real-time, orb-features | TUM RGB-D, Replica, EuRoC | 前端使用特征点法（ORB）进行高频位姿跟踪，后端利用 3DGS 进行光度级建图，实现跟踪与渲染的计算解耦。 | not tested |
| 2024 | CVPR | [Photo-SLAM: Real-time Simultaneous Localization and Photorealistic Mapping for Monocular, Stereo, and RGB-D Cameras](https://arxiv.org/pdf/2311.16728.pdf) | [code](https://github.com/HuajianUP/Photo-SLAM) | Monocular, Stereo, RGB-D | Visual 3DGS-SLAM | TBD | Real-time photorealistic mapping across monocular, stereo, and RGB-D settings using a Gaussian map. | not tested |
| 2024 | Computer Graphics Forum | [GauLoc: 3D Gaussian Splatting-based Camera Relocalization](https://onlinelibrary.wiley.com/doi/10.1111/cgf.15104) | TBD | Visual Localization, 3DGS-map | Localization / Re-localization | TBD | Camera relocalization based on 3D Gaussian Splatting maps. | not tested |
| 2024 | ECCV | [SGS-SLAM: Semantic Gaussian Splatting For Neural Dense SLAM](https://arxiv.org/pdf/2402.03246.pdf) | [code](https://github.com/ShuhongLL/SGS-SLAM) | RGB-D, Semantic | Semantic 3DGS-SLAM | TBD | Adds semantic-aware Gaussian map modeling to dense neural SLAM. | not tested |
| 2024 | IROS | [MM3DGS SLAM: Multi-modal 3D Gaussian Splatting for SLAM Using Vision, Depth, and Inertial Measurements](https://arxiv.org/pdf/2404.00923.pdf) | [code](https://github.com/VITA-Group/MM3DGS-SLAM) | RGB-D, VIO, Multi-modal | Multimodal 3DGS-SLAM | TBD | Multi-modal Gaussian SLAM using vision, depth, and inertial measurements. | not tested |
| 2024 | NeurIPS | [DG-SLAM: Robust Dynamic Gaussian Splatting SLAM with Hybrid Pose Optimization](https://openreview.net/pdf?id=tGozvLTDY3) | [code](https://github.com/fudan-zvg/DG-SLAM) | RGB-D, Dynamic | Dynamic 3DGS-SLAM | TBD | Addresses dynamic scenes with hybrid pose optimization in Gaussian Splatting SLAM. | not tested |
| 2024 | RAL | [HGS-Mapping: Online Dense Mapping Using Hybrid Gaussian Representation in Urban Scenes](https://arxiv.org/pdf/2403.20159.pdf) | TBD | LiDAR, Outdoor | Multimodal 3DGS-SLAM | KITTI, KITTI-360, TBD | Online dense mapping in urban scenes with a hybrid Gaussian representation. | not tested |
| 2024 | RAL | [LI-GS: Gaussian Splatting with LiDAR Incorporated for Accurate Large-Scale Reconstruction](https://arxiv.org/pdf/2409.12899) | TBD | LiDAR, Camera, Outdoor | Multimodal 3DGS-SLAM | KITTI, KITTI-360, TBD | Uses LiDAR information to improve large-scale Gaussian reconstruction. | not tested |
| 2024 | RAL | [LIV-GaussMap: LiDAR-Inertial-Visual Fusion for Real-time 3D Radiance Field Map Rendering](https://arxiv.org/pdf/2401.14857.pdf) | [code](https://github.com/sheng00125/LIV-GaussMap) | LiDAR, VIO, Multi-modal | Multimodal 3DGS-SLAM | KITTI, TBD | LiDAR-inertial-visual fusion for real-time radiance-field map rendering with Gaussians. | not tested |
| 2024 | RAL | [NEDS-SLAM: A Novel Neural Explicit Dense Semantic SLAM Framework using 3D Gaussian Splatting](https://arxiv.org/pdf/2403.11679.pdf) | TBD | RGB-D, Semantic | Semantic 3DGS-SLAM | TBD | Neural explicit dense semantic SLAM framework built around 3D Gaussian Splatting. | not tested |
| 2024 | SIGGRAPH | [RTG-SLAM: Real-time 3D Reconstruction at Scale using Gaussian Splatting](https://arxiv.org/pdf/2404.19706) | [code](https://github.com/MisEty/RTG-SLAM) | RGB-D, Monocular | Large-scale 3DGS-SLAM | TBD | Targets real-time scalable 3D reconstruction using Gaussian Splatting in a SLAM-like setting. | not tested |
| 2024 | arXiv | [Compact 3D Gaussian Splatting For Dense Visual SLAM](https://arxiv.org/pdf/2403.11247.pdf) | [code](https://github.com/dtc111111/Compact_GSSLAM) | RGB-D | Efficient 3DGS-SLAM | TBD | Focuses on reducing map size and computation for dense visual Gaussian SLAM. | not tested |
| 2024 | arXiv | [EndoGSLAM: Real-Time Dense Reconstruction and Tracking in Endoscopic Surgeries using Gaussian Splatting](https://arxiv.org/pdf/2403.15124.pdf) | [code](https://github.com/Loping151/EndoGSLAM) | Endoscopy, Monocular | Medical / Endoscopic 3DGS-SLAM | Endoscopy datasets, TBD | Specialized Gaussian SLAM for real-time tracking and dense reconstruction in endoscopic scenes. | not tested |
| 2024 | arXiv | [GLC-SLAM: Gaussian Splatting SLAM with Efficient Loop Closure](https://arxiv.org/pdf/2409.10982) | TBD | Monocular, RGB-D | Loop closure / Global consistency | TBD | Targets efficient loop closure for Gaussian Splatting SLAM. | not tested |
| 2024 | arXiv | [GS-LIVM: Real-Time Photo-Realistic LiDAR-Inertial-Visual Mapping with Gaussian Splatting](https://arxiv.org/pdf/2410.17084) | [code](https://github.com/xieyuser/GS-LIVM) | LiDAR, Camera, IMU, Multi-modal | Multimodal 3DGS-SLAM | TBD | Real-time LiDAR-inertial-visual mapping with photorealistic Gaussian maps. | not tested |
| 2024 | arXiv | [GSLoc: Efficient Camera Pose Refinement via 3D Gaussian Splatting](https://arxiv.org/pdf/2408.11085) | TBD | Visual Localization, 3DGS-map | Localization / Re-localization | TBD | Efficient camera pose refinement using a 3D Gaussian Splatting scene representation. | not tested |
| 2024 | arXiv | [GSplatLoc: Grounding Keypoint Descriptors into 3D Gaussian Splatting for Improved Visual Localization](https://arxiv.org/pdf/2409.16502) | [code](https://github.com/gsplatloc/GSplatLoc) | Visual Localization, 3DGS-map | Localization / Re-localization | 7-Scenes, Cambridge Landmarks, TBD | Grounds keypoint descriptors in 3DGS scenes to improve visual localization. | not tested |
| 2024 | arXiv | [GSplatLoc: Ultra-Precise Camera Localization via 3D Gaussian Splatting](https://arxiv.org/pdf/2412.20056.pdf) | [code](https://github.com/AtticusZeller/GsplatLoc) | RGB-D, Visual Localization, 3DGS-map | Localization / Re-localization | Replica, TUM RGB-D | Pose optimization method that localizes RGB-D observations against a pre-built 3D Gaussian scene. | not tested |
| 2024 | arXiv | [LIV-GaussMap: LiDAR-Inertial-Visual Fusion for Real-time 3D Radiance Field Mapping](https://arxiv.org/abs/2404.10755) | [code](https://github.com/hku-mars/LIV-GaussMap) | LiDAR, IMU, Camera | multi-sensor-fusion, lidar, imu, real-time | Custom Multi-modal, NCLT | 基于激光-惯性-视觉多传感器融合系统提供先验位姿与深度结构，利用 3DGS 进行大尺度户外环境的实时高保真建图。 | not tested |
| 2024 | arXiv | LoGS: Visual Localization via Gaussian Splatting with Fewer Training Images | TBD | Visual Localization, 3DGS-map | Localization / Re-localization | TBD | Visual localization using Gaussian Splatting with fewer training images. | not tested |
| 2024 | arXiv | [MotionGS: Compact Gaussian Splatting SLAM by Motion Filter](https://arxiv.org/pdf/2405.11129) | [code](https://github.com/Antonio521/MotionGS) | Monocular, RGB-D | Efficient 3DGS-SLAM | TBD | Uses motion filtering to make Gaussian SLAM more compact and efficient. | not tested |
| 2024 | arXiv | [NEDS-SLAM: A Novel Event-Driven Point-Cloud Spatial Representation for 3DGS SLAM](https://arxiv.org/abs/2402.16486) | [code](paper-only) | Event Camera | event-camera, high-speed, hdr | Event camera benchmarks | 针对高动态范围与高速运动场景，利用事件相机提供的异步像素级亮度变化流直接驱动 3DGS 地图的构建与更新。 | not tested |
| 2024 | arXiv | [SemGauss-SLAM: Dense Semantic Gaussian Splatting SLAM](https://arxiv.org/abs/2403.07494) | [code](paper-only) | RGB-D | semantic, dense-slam, scene-understanding | Replica, ScanNet | 在高斯属性中嵌入语义特征维度，通过 2D 语义分割先验监督，实现密集几何与语义属性的联合优化与提取。 | not tested |
| 2024 | arXiv | [SplatAD: Real-Time Lidar and Camera Rendering with 3D Gaussian Splatting for Autonomous Driving](https://arxiv.org/pdf/2411.16816) | TBD | Camera, LiDAR, Autonomous Driving, Dynamic | Autonomous driving / sensor simulation | Autonomous driving datasets, TBD | 3DGS method for realistic, real-time rendering of camera and LiDAR logs in autonomous-driving scenarios. | not tested |
| 2024 | arXiv | [SplatLoc: 3D Gaussian Splatting-based Visual Localization for Augmented Reality](https://arxiv.org/pdf/2409.16502) | [code](https://github.com/zju3dv/SplatLoc) | Visual Localization, 3DGS-map, AR | Localization / Re-localization | TBD | 3DGS-based visual localization method oriented toward augmented reality applications. | not tested |
| 2024 | arXiv | [Visual Localization with 3D Gaussian Splatting](https://arxiv.org/abs/2406.00000) | [code](paper-only) | RGB-only | localization, 3dgs, camera-pose, pnp | 7-Scenes, Cambridge Landmarks | 直接利用 3DGS 场景表示渲染关键点与深度特征，通过 2D-3D 匹配与 PnP 求解实现相机的 6-DoF 位姿估计。 | not tested |
| 2024 | arXiv / CVPRW 2025 | [Splat-SLAM: Globally Optimized RGB-only SLAM with 3D Gaussians](https://arxiv.org/abs/2405.16544) | [code](https://github.com/eriksandstroem/Splat-SLAM) | RGB-only | rgb-only, global-optimization, loop-closure | Replica, TUM RGB-D, ScanNet | RGB-only dense SLAM using globally optimized tracking and dynamic updates to a dense Gaussian map. | not tested |
| 2023 | ICCV | [3DGS-ReLoc: 3D Gaussian Splatting for Map Representation and Visual ReLocalization](https://openaccess.thecvf.com/content/ICCV2023/papers/Chen_3DGS-ReLoc_3D_Gaussian_Splatting_for_Map_Representation_and_Visual_ReLocalization_ICCV_2023_paper.pdf) | TBD | Visual Localization, 3DGS-map | Localization / Re-localization | TBD | Early 3DGS-based map representation for visual relocalization. | not tested |

## Datasets

| Dataset | Type | Sensors / data | Ground truth | Common use in 3DGS-SLAM | Notes |
|---|---|---|---|---|---|
| [Bonn RGB-D Dynamic](http://www.ipb.uni-bonn.de/data/bonn-rgbd-dynamic/) | Real indoor dynamic RGB-D | ['RGB', 'depth'] | motion-capture trajectories for camera and dynamic objects |  | 常用于评估 3DGS-SLAM 系统在包含高动态物体（如走动的人）场景下的前端跟踪鲁棒性与动态遮罩剥离准确度。 |
| [Cambridge Landmarks](https://www.repository.cam.ac.uk/handle/1810/251342) | Outdoor large-scale RGB | ['RGB images'] | Structure from Motion (SfM) reconstructed poses |  | 评估大尺度室外场景 6-DoF 绝对位姿回归与视觉定位的标准数据集。 |
| [Deep Blending](http://visual.cs.ucl.ac.uk/pubs/deepblending/) | Real-world NVS benchmark | RGB images with calibrated cameras | Evaluation image splits | Rendering quality and general 3DGS baseline comparison | Useful for non-SLAM rendering baselines and acceleration/compression comparisons. |
| [DTU MVS](https://roboimagedata.compute.dtu.dk/?page_id=36) | Multi-view stereo / reconstruction | Calibrated RGB image scans | Camera calibration and reference geometry depending split | Geometry/reconstruction quality for Gaussian and 2DGS variants | More useful for reconstruction/geometric fidelity than online SLAM tracking. |
| [ETH3D](https://www.eth3d.net/) | Multi-view reconstruction / SLAM-style scenes | High-resolution images and laser-scan references depending benchmark | Camera calibration and 3D reference scans depending benchmark | Geometry-focused reconstruction and view-synthesis validation | Useful for checking geometric fidelity beyond indoor RGB-D SLAM datasets. |
| [EuRoC MAV](https://projects.asl.ethz.ch/datasets/euroc-mav/) | Visual-inertial MAV | ['stereo cameras', 'IMU'] | accurate motion and structure ground truth |  | Useful for stereo/VIO variants of Gaussian-map SLAM. |
| [ICL-NUIM](https://www.doc.ic.ac.uk/~ahanda/VaFRIC/iclnuim.html) | Synthetic indoor RGB-D | Rendered RGB-D sequences | Ground-truth camera trajectory and geometry | Legacy dense RGB-D SLAM benchmark | Useful for controlled reconstruction tests and historical comparison. |
| [KITTI Odometry](https://www.cvlibs.net/datasets/kitti/eval_odometry.php) | Outdoor driving | ['stereo', 'LiDAR-compatible benchmark'] | GT trajectories for training sequences 00-10 |  | Useful for large-scale outdoor and LiDAR/vision SLAM. |
| [KITTI-360](https://www.cvlibs.net/datasets/kitti-360/) | Outdoor large-scale multi-sensor | ['LiDAR', 'stereo cameras', 'fisheye cameras', 'RTK GPS'] | high-precision dense point clouds, 6-DoF poses, semantic annotations |  | 提供大尺度室外多传感器融合的原始数据。其时间戳对齐与多视角约束结构，适合通过脚本离线打包为 ROS2 db3 格式，用于验证高保真数字孪生和 Sim-to-Real 的建图渲染效果。 |
| [Microsoft 7-Scenes](https://www.microsoft.com/en-us/research/project/rgb-d-dataset-7-scenes/) | Real indoor RGB-D | ['RGB', 'depth'] | KinectFusion generated 6-DoF camera poses |  | 室内视觉定位的基础基准测试，常用于评估基于隐式场或 3DGS 的重定位精度。 |
| [Mip-NeRF 360](https://jonbarron.info/mipnerf360/) | Real-world 360-degree NVS benchmark | RGB image collections with camera poses | Camera poses / benchmark images | Novel-view synthesis and rendering-quality baseline for 3DGS variants | Dataset name retained for compatibility; this is a dataset entry, not a NeRF paper entry. |
| [MulRan](https://sites.google.com/view/mulran-pr/home) | Outdoor LiDAR / radar / urban driving | 3D LiDAR, radar, cameras, GPS/INS depending sequence | Trajectory references depending sequence | Large-scale LiDAR and multi-modal SLAM | Candidate for LiDAR-based Gaussian SLAM and localization. |
| [NCLT Dataset](https://irvlab.engin.umich.edu/resources/nclt-dataset/) | Outdoor long-term multi-sensor | ['LiDAR', 'omnidirectional camera', 'RTK GPS', 'IMU'] | RTK GPS and optimized full 6-DoF trajectories |  | 包含丰富的长周期户外多模态数据。其原始数据集的 ROS1 bag 结构可通过脚本高效迁移至 ROS2 的 mcap 或 db3 格式进行回放与测试。 |
| [Newer College Dataset](https://ori-drs.github.io/newer-college-dataset/) | Outdoor long-term multi-sensor | ['LiDAR', 'stereo cameras', 'IMU'] | ICP registered sub-centimeter point clouds, 6-DoF poses |  | 记录了长周期、存在结构退化与高动态特征的校园场景。便于通过 ROS 节点流式读取，验证跨层统计退化感知以及联合优化过程中的鲁棒性。 |
| [nuScenes](https://www.nuscenes.org/) | Autonomous driving / multi-modal | Cameras, LiDAR, radar, GPS/IMU | 3D annotations and sensor calibration | Multi-modal outdoor perception, localization, and dynamic scene mapping | Good candidate for camera-LiDAR-radar Gaussian mapping studies. |
| [Replica](https://github.com/facebookresearch/Replica-Dataset) | Synthetic / reconstructed indoor | ['mesh', 'rendered RGB-D', 'semantic labels'] | dense geometry and semantic annotations |  | Controlled indoor benchmark often used for rendering and reconstruction quality. |
| [ScanNet](https://www.scan-net.org/) | Real indoor RGB-D video | ['RGB-D video', 'poses', 'surface reconstruction', 'semantic labels'] | poses, 3D reconstructions, semantic and instance labels |  | Access approval may be required; use official splits when possible. |
| [ScanNet++](https://scannetpp.mlsg.cit.tum.de/scannetpp/) | High-fidelity real indoor | ['laser scans', 'DSLR images', 'iPhone RGB-D'] | high-quality geometry and semantic annotations |  | Useful for high-fidelity reconstruction and NVS-oriented SLAM evaluation. |
| [Tanks and Temples](https://www.tanksandtemples.org/) | Real-world reconstruction / NVS | RGB video/images, reconstructions | Evaluation geometry for selected scenes | Reconstruction and novel-view-synthesis style evaluation | Not a standard SLAM trajectory benchmark, but useful for mapping quality. |
| [TartanAir](https://theairlab.org/tartanair-dataset/) | Synthetic multi-sensor | ['stereo RGB', 'depth', 'optical flow', 'IMU'] | exact camera poses, dense depth, optical flow, semantic segmentation |  | 提供极端环境与复杂运动模式的合成数据，传感器模态丰富。适合用于验证多模态融合 3DGS 建图与 Sim-to-Real 的算法迁移能力。 |
| [TUM RGB-D](https://cvg.cit.tum.de/data/datasets/rgbd-dataset) | Real indoor RGB-D | ['RGB', 'depth', 'accelerometer'] | motion-capture camera trajectory |  | Classic RGB-D SLAM benchmark; always report sequence name and alignment protocol. |
| [Virtual KITTI 2](https://europe.naverlabs.com/research/computer-vision/proxy-virtual-worlds-vkitti-2/) | Synthetic autonomous driving | Synthetic RGB, depth, optical flow, semantics, poses | Dense synthetic annotations and camera poses | Dynamic/outdoor/autonomous-driving 3DGS scene understanding | Useful with KITTI/KITTI-360 for controlled dynamic-scene evaluation. |
| [Waymo Open Dataset](https://waymo.com/open/) | Autonomous driving / multi-sensor | Cameras, LiDAR, labels depending task | 3D boxes / segmentation / motion labels depending task | Outdoor autonomous-driving mapping, sensor rendering, and dynamic-scene evaluation | Use official splits and document whether LiDAR labels, camera images, or motion labels are used. |

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

### Paper cover thumbnails

The website supports paper-cover thumbnails in each paper card. Put low-resolution paper first-page screenshots, teaser figures, or official thumbnails under:

```text
docs/assets/thumbnails/
```

Recommended naming convention:

```text
docs/assets/thumbnails/<paper_id>.jpg
docs/assets/thumbnails/<paper_id>.png
docs/assets/thumbnails/<paper_id>.svg
```

Then add a public-safe field in the paper metadata or generated HTML data:

```yaml
thumbnail: docs/assets/thumbnails/splatam_2024.jpg
```

Use small images, ideally under 400 KB each, so GitHub Pages loads quickly. Do not put private experiment plots or unreleased results into thumbnails.

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
