# Eye-Head Coordination: Gaze Angle vs. Eye/Head Contribution Ratio

## 1. Overview

When人类将视线转向一个新目标时，整个注视偏转（gaze shift）由 **眼球在眼眶内的旋转（eye-in-orbit rotation）** 和 **头部旋转（head rotation）** 共同完成：

```
Gaze Shift = Eye Rotation + Head Rotation
```

两者的分配比例随注视角度增大而系统性地变化，并且在水平方向（yaw）和垂直方向（pitch）表现出不同的特征。

---

## 2. Eye & Head 基本运动范围

| 参数 | 水平方向 (Yaw) | 垂直方向 (Pitch) |
|---|---|---|
| **眼球舒适旋转范围** | ±15° | ±10° ~ ±12° |
| **眼球生理极限范围** | ±44° ~ ±50° | 上视 25°–28°；下视 30°–47° |
| **头部舒适旋转范围** | ±30° ~ ±35° | 前屈 25°–30°；后仰 30°–35° |
| **头部生理极限范围** | ±55° ~ ±80° | 前屈 45°–60°；后仰 35°–50° |

> **来源**: Guitton & Volle 1987; ISO 11226; Differences in eye movement range based on age and gaze direction (Nature, 2019).

---

## 3. 水平方向 (Horizontal / Yaw) 的眼-头分配

### 3.1 三阶段模型

水平方向的眼-头协调可以用**三阶段模型**概括：

#### Phase 1 — Eye-Only Zone（纯眼动区）: 注视角 < 15°–20°

- 注视偏转几乎完全由**眼球 saccade** 完成
- 头部可能有微弱、延迟的跟随运动，但对注视贡献极小（< 5%）
- 这一阈值在文献中通常称为 **gaze shift threshold** 或 **oculomotor range**

| 注视角 | 眼球贡献 | 头部贡献 |
|---|---|---|
| 5° | ~100% (~5°) | ~0% |
| 10° | ~100% (~10°) | ~0% |
| 15° | ~95%–100% (~14°–15°) | ~0%–5% (~0°–1°) |

#### Phase 2 — Eye-Head Coordination Zone（眼-头协调区）: 注视角 20°–50°

- 头部开始显著参与注视偏转
- 眼球 saccade 振幅不再线性增长，逐渐趋于饱和
- Head gain（头部贡献/总注视偏转）近似线性增长，斜率约 **0.5–0.7**
- 个体差异显著：存在 **"eye-mover"**（偏好用眼）与 **"head-mover"**（偏好转头）的谱系

| 注视角 | 眼球贡献 | 头部贡献 | Head Gain |
|---|---|---|---|
| 20° | ~15°–18° | ~2°–5° | 0.10–0.25 |
| 30° | ~18°–22° | ~8°–12° | 0.27–0.40 |
| 40° | ~20°–25° | ~15°–20° | 0.38–0.50 |
| 50° | ~22°–28° | ~22°–28° | 0.44–0.56 |

#### Phase 3 — Head-Dominant Zone（头部主导区）: 注视角 > 50°–60°

- 眼球 saccade 振幅接近或达到生理极限（~35°–50°），基本饱和
- 超过眼球极限的注视偏转**完全依赖头部（和躯干）旋转**
- 当注视角 > 80°–90° 时，躯干（trunk/torso）旋转也开始参与

| 注视角 | 眼球贡献 | 头部贡献 | Head Gain |
|---|---|---|---|
| 60° | ~25°–30° | ~30°–35° | 0.50–0.58 |
| 80° | ~28°–35° (saturated) | ~45°–52° | 0.56–0.65 |
| 90° | ~30°–35° (saturated) | ~55°–60° | 0.61–0.67 |
| 120°+ | ~30°–35° (saturated) | ~60°+ (trunk also contributes) | 0.65+ |

### 3.2 水平方向总结曲线

```
Eye amplitude
 (degrees)
    50 |
    40 |                          ___________   <- Eye saturates (~35°–50°)
    30 |                   ------/
    20 |             -----/
    10 |       -----/
     0 |______/
       +------+------+------+------+------+-------> Gaze shift (°)
       0     15     30     45     60     75    90

Head amplitude
 (degrees)
    60 |                                    /
    50 |                                  /
    40 |                              /
    30 |                          /
    20 |                     /
    10 |               /
     0 |__________/                        <- Head starts ~15°–20°
       +------+------+------+------+------+-------> Gaze shift (°)
       0     15     30     45     60     75    90
```

---

## 4. 垂直方向 (Vertical / Pitch) 的眼-头分配

垂直方向的眼-头协调与水平方向有三个关键差异：

### 4.1 差异一：头部参与的阈值更低

- 垂直方向上，头部在更小的注视角就开始参与（约 **10°–15°**，vs 水平方向的 15°–20°）
- 原因：垂直方向眼球舒适范围更窄（±10°–12° vs 水平方向的 ±15°）

### 4.2 差异二：上视 vs 下视的不对称性

| 方向 | 眼球最大贡献 | 头部贡献特征 |
|---|---|---|
| **上视 (Upward)** | 较大（~25°–28°） | 头部后仰贡献相对**较少**；眼球承担更大比例 |
| **下视 (Downward)** | 较小（~20°–25°常用范围） | 头部前屈贡献相对**较多**；head gain 更高 |

这种不对称性的原因包括：
1. 眼球上视生理范围（~25°–28°）小于下视范围（~30°–47°），但头部后仰范围也受限
2. 下视时头部前屈在力学上更自然（重力辅助），因此 head gain 更高
3. 日常行为中下视（看地面、桌面）远多于上视，头部前屈已形成习惯性运动模式

### 4.3 垂直方向的典型分配

#### 上视 (Upward Gaze)

| 注视角 | 眼球贡献 | 头部贡献 | Head Gain |
|---|---|---|---|
| 10° | ~8°–10° | ~0°–2° | 0.00–0.20 |
| 20° | ~14°–17° | ~3°–6° | 0.15–0.30 |
| 30° | ~18°–22° | ~8°–12° | 0.27–0.40 |
| 40° | ~22°–25° (approaching limit) | ~15°–18° | 0.38–0.45 |
| 50°+ | ~25°–28° (saturated) | ~22°+ | 0.44+ |

#### 下视 (Downward Gaze)

| 注视角 | 眼球贡献 | 头部贡献 | Head Gain |
|---|---|---|---|
| 10° | ~7°–9° | ~1°–3° | 0.10–0.30 |
| 20° | ~12°–15° | ~5°–8° | 0.25–0.40 |
| 30° | ~15°–20° | ~10°–15° | 0.33–0.50 |
| 40° | ~18°–22° | ~18°–22° | 0.45–0.55 |
| 50°+ | ~20°–25° | ~25°+ | 0.50+ |

> 注意：下视时 head gain 普遍高于上视和水平方向同等角度。

---

## 5. 水平 vs 垂直 对比总结

| 特征 | 水平方向 (Yaw) | 垂直方向 (Pitch) |
|---|---|---|
| **Eye-only 阈值** | ~15°–20° | ~10°–15° |
| **Eye 饱和角度** | ~35°–50° | 上视 ~25°–28°; 下视 ~25°–30°(常用) |
| **Head gain 增长斜率** | ~0.5–0.7 | 上视 ~0.4–0.6; 下视 ~0.5–0.8 |
| **Head 参与的渐进性** | 较线性、平滑 | 上/下不对称，下视 head gain 更高 |
| **个体差异** | 显著（eye-mover vs head-mover spectrum） | 同样显著，且受年龄影响更大 |
| **躯干参与阈值** | > 80°–90° | 通常无需躯干（垂直总范围较小） |

---

## 6. 个体差异：Eye-Mover vs Head-Mover Spectrum

Hu et al. (2026, arXiv:2602.06164) 在 VR 环境中的研究发现，人群的眼-头分配策略形成一个**连续谱系**：

- **Eye-Mover（眼动偏好型）**: 更多依赖眼球旋转，头部运动较少，head gain 较低
- **Head-Mover（头动偏好型）**: 更多依赖头部转动，head gain 较高

这意味着上述所有数值都存在显著的个体差异带（上表中用范围表示），在 XR/VR 设计中不能假设所有用户具有相同的眼-头分配策略。

---

## 7. XR/VR 设计启示

| 设计考量 | 建议 |
|---|---|
| **UI 元素放置** | 核心交互元素放在 ±15° 以内（eye-only zone），避免频繁头部运动导致疲劳 |
| **注视引导 (Gaze Cue)** | 需要引导注视到 >20° 区域时，提供渐进式视觉引导让头部有时间跟随 |
| **Foveated Rendering** | 需考虑 eye-mover/head-mover 个体差异来预测注视点 |
| **垂直布局** | 避免需要持续上视（>20°）的设计；下视方向可以稍宽松但也应克制 |
| **Eye Tracking 精度** | 超过 ±15° 眼球偏心角后，眼动追踪精度显著下降，需结合头部朝向补偿 |
| **运动舒适区** | 频繁交互区域建议控制在水平 ±30°、垂直 ±20° 以内 |

---

## 8. 主要参考文献

1. Guitton, D. & Volle, M. (1987). Gaze control in humans: eye-head coordination during orienting movements to targets within and beyond the oculomotor range. *Journal of Neurophysiology*, 58(3), 427–459.
2. Freedman, E. G. (2008). Coordination of the eyes and head during visual orienting. *Experimental Brain Research*, 190(4), 369–387.
3. Hu, Y., Sidenmark, L., Lee, B., & Gellersen, H. (2026). The Eye–Head Mover Spectrum: Modelling Individual and Population Head Movement Tendencies in Virtual Reality. *arXiv:2602.06164*.
4. Land, M. F. (2004). The coordination of rotations of the eyes, head and trunk in saccadic turns produced in natural situations. *Experimental Brain Research*, 159(2), 151–160.
5. Stahl, J. S. (1999). Amplitude of human head movements associated with horizontal saccades. *Experimental Brain Research*, 126(1), 41–54.
6. Fuller, J. H. (1992). Head movement propensity. *Experimental Brain Research*, 92(1), 152–164.
7. Pelz, J. B., Hayhoe, M. M., & Loeber, R. (2001). The coordination of eye, head, and hand movements in a natural task. *Experimental Brain Research*, 139(3), 266–277.
8. ISO 11226:2000 — Ergonomics — Evaluation of static working postures.
