# XR 人机工程学空间布局推导方案 (XR-ErgoSpatial Model)

## 一、概述

### 1.1 本文档的目标

在 XR 环境中，界面不再被限制在一块固定尺寸的屏幕上——设计师拥有了用户周围完整的三维空间。然而，空间自由度的增加并不意味着交互对象可以被随意放置。用户的身体是有物理边界和生理负荷极限的，忽视这些约束的布局会直接导致疲劳、不适甚至使用意愿的下降。

本文档提供一套**基于上肢生物力学的空间布局推导模型**，帮助设计师和开发者回答以下四个核心布局问题：

- **放在哪里** — 交互对象应当占据用户周围哪片空间区域？
- **用什么方式交互** — 该位置适合直接触摸，还是应当使用眼动+手势等远程模态？
- **放什么** — 哪类组件的交互特征与该区域的负荷水平相匹配？
- **怎么操作** — 该区域适合哪些动作类型（精细拖拽、单次点按、注视确认等）？

### 1.2 为什么需要关注上肢负荷

在传统 GUI 设计中，用户的手臂搁在桌面或膝盖上，操作输入设备时上肢几乎不承受额外负荷。但在 XR 空间交互中，情况发生了根本性的变化：

**手臂本身成为了输入设备。** 用户需要抬起手臂、伸向空间中的目标并维持姿态来完成操作。这意味着肩关节和上肢肌群必须持续对抗手臂自身的重力——这就是被广泛讨论的**"猩猩臂效应"（Gorilla Arm Effect）**。

肌肉疲劳研究（Rohmert, 1960; Sjogaard et al., 1986）表明，即使是较低水平的持续肌肉收缩，也会在数分钟内引发明显的疲劳和不适。具体而言：

- 当肌肉持续负荷低于最大自主收缩力（MVC）的 **15%** 时，用户可以维持 30 分钟以上而不感到明显疲劳；
- 当负荷处于 **15%–30% MVC** 时，数分钟内即出现疲劳感；
- 当负荷超过 **30% MVC** 时，仅能维持数十秒到数分钟。

因此，空间中不同位置对应着截然不同的生理代价。将**高频交互组件放在低负荷区域、将低频或纯展示内容放在高负荷区域**，是 XR 空间布局设计的基本原则。本文档的核心价值，就是提供一种量化方法来精确评估这种代价。

### 1.3 核心概念

理解本文档的推导逻辑，需要把握以下几个核心概念：

**物理可达性（Reachability）**

用户的手臂长度决定了一个以肩关节为球心的可达球面。球面内部是手可以物理触碰的空间，球面外部则必须依赖远程交互模态（如注视+捏合）。这是人体骨骼结构决定的硬性边界，无法通过训练或适应来突破。

**肩关节力矩（Shoulder Torque）**

手臂是一根有重量的杠杆，肩关节是支点。当手臂偏离自然下垂状态时，重力会在肩关节产生力矩，这个力矩就是肩部肌群需要持续对抗的负荷。手臂抬得越高、伸得越直，力矩越大，疲劳越快。

**归一化疲劳指数（Normalized Fatigue Index）**

将任意手臂姿态下的肩关节力矩，与最大力矩（手臂完全水平伸直时）做比值，得到一个 0.0 到 1.0 之间的无量纲指标。0.0 表示手臂自然下垂、零负荷；1.0 表示手臂水平前伸、最大负荷。这个指数是后续所有布局决策的量化基础。

**疲劳分区（Fatigue Zones）**

基于 MVC 阈值，将归一化疲劳指数映射到三个具有明确设计含义的区域：

| 分区 | 疲劳指数范围 | 设计含义 |
| :--- | :--- | :--- |
| **舒适区 (Comfort Zone)** | 0 – 0.15 | 适合放置高频、长时间、高精度的核心交互内容 |
| **过渡区 (Transition Zone)** | 0.15 – 0.30 | 适合放置低频、快速触发、即点即走的辅助控件 |
| **高负荷区 (High-Load Zone)** | 0.30 – 1.0 | 仅适合放置极低频触发或纯展示内容 |

需要强调的是，这些分区的边界不是简单的矩形平面，而是以肩关节为中心的**弯曲三维曲面**。本文档提供的模型可以对空间中任意一点进行逐点查询，而非仅给出粗略的区间划分。

---

## 二、身体数据采集

### 2.1 设计原则

本模型依赖少量用户个体化身体数据来驱动后续的可达性判断和力矩评估。数据采集遵循以下原则：

- **无感优先：** 采集过程嵌入 onboarding 流程，用户的主观感受是"在完成一次自然的交互引导"，而非"在被测量身体"。
- **只测必要量：** 仅采集无法通过人体测量学常数替代的个体化数据（全臂长、肩关节偏移量），其余参数（上臂/前臂比例、质量比例、重心比例）使用文献常数。
- **功能性优于解剖学：** 采集的是用户愿意且习惯伸出的手臂距离（功能性臂长），而非解剖学上的最大臂展。这使得后续推导的空间布局更贴合用户的真实使用习惯。

### 2.2 采集流程

采集发生在应用的 onboarding 阶段，分为两个连续的阶段。用户感知到的是一次连贯的交互引导。

**阶段一：惯用手检测**

一个交互目标（如按钮、光点、浮动物件）出现在用户正前方的身体中轴线上，距离较近（轻松可达）。系统不做测量，仅观察**哪只手先离开静息位置并向目标移动**，将其标记为惯用手（即用户在 XR 环境中偏好使用的手）。

**阶段二：功能性臂长采集**

检测到惯用手后，目标平滑移动到**该侧肩膀的正前方**，随后开始缓慢向远处移动。用户自然地伸手跟随目标。

系统持续监测手腕坐标。当手腕位置在空间中**稳定不再前移达 1 秒**时，判定为用户的自然伸展极限，完成采集。此时记录：

- 惯用手手腕坐标（稳定瞬间）
- 头部坐标（同一瞬间）

目标给出"已触达"的反馈（视觉或听觉），onboarding 流程继续。

### 2.3 采集的变量清单

通过上述流程，直接测量或推算以下变量：

```
# ===== 直接测量 =====

# 惯用手标记
dominant_hand              # "left" 或 "right"

# 功能性全臂长（肩关节到手腕的距离，在用户自然伸展极限处测得）
# 来源：稳定瞬间的 (手腕坐标 - 估算肩关节坐标) 的长度
L_arm_dominant             # 惯用手侧全臂长

# ===== 镜像估算 =====

# 非惯用手全臂长（镜像取惯用手数值）
L_arm_non_dominant         # 非惯用手侧全臂长 = L_arm_dominant

# ===== 人体测量学常数推算 =====

# 上臂长 / 前臂长（基于全臂长和通用比例拆分）
# 来源：Winter, 2009
UPPER_FOREARM_RATIO = 0.55 : 0.45
L_upper = L_arm_dominant * 0.55
L_forearm = L_arm_dominant * 0.45

# 肩关节相对于头部的偏移量（基于人体测量学常数）
# 来源：人体比例文献
S_offset_down              # 肩关节在头部下方的垂直距离（约 0.20–0.25m）
S_offset_lateral           # 肩关节相对于头部中轴线的水平偏移（约 0.18–0.20m）
```

### 2.4 肩关节坐标估算

由于 visionOS 的手部追踪止于手腕，无法直接获取肩关节位置。通过头部坐标加偏移常数来实时推算：

```
# P_head = 头显实时坐标 (x, y, z)

P_shoulder_left = (
    P_head.x - S_offset_lateral,
    P_head.y - S_offset_down,
    P_head.z
)

P_shoulder_right = (
    P_head.x + S_offset_lateral,
    P_head.y - S_offset_down,
    P_head.z
)
```

由于肩关节坐标始终相对于头部实时计算，当用户改变体位（如从站姿变为坐姿）时，肩关节位置会自动跟随更新，模型无需额外区分坐/站姿态。

### 2.5 传感器依赖

本方案仅依赖 visionOS ARKit Hand Tracking 提供的以下数据：

| 数据 | 来源 | 说明 |
| :--- | :--- | :--- |
| 手腕三维坐标 | ARKit Hand Tracking（每手 25 个关节点中的 wrist） | 用于测量功能性臂长、检测惯用手 |
| 头部三维坐标与朝向 | 设备自身定位 | 用于实时推算肩关节位置 |

不依赖肘关节、肩关节追踪，不依赖外部传感器或额外硬件。

---

## 三、交互模态决策 — 物理可达性判断

### 3.1 理论依据

此步骤回答的核心问题是：**用户的手能不能物理触碰到这个点？**

- **能触碰** → 允许使用直接触摸 (Direct Touch)
- **不能触碰** → 必须使用眼动+手势 (Gaze & Pinch) 或射线 (Ray-casting)

可达性的判定需要同时满足三个层次的约束：

| 约束层 | 判定内容 | 物理依据 |
| :--- | :--- | :--- |
| 视野范围 | 该点是否在用户可及的视觉范围内 | 颈椎舒适转动范围 |
| 关节活动度 | 肩关节能否将手臂导向该方向 | 肩关节 ROM |
| 距离 | 手臂能否够到该点的距离 | 功能性臂长 |

三个约束全部通过，才判定为可达。任一约束未通过，即判定为不可达。

### 3.2 约束一：视野范围

在 XR 交互中，用户不会与视野之外的空间发生有意义的交互。位于身后或极端侧方的空间，即使手臂物理上可达，也不具备实际交互价值。

视野约束基于颈椎的**舒适转动范围**（非极限范围）定义，以用户身体朝向为基准：

```
# 视野范围参数（基于颈椎舒适转动范围，非设备即时 FOV）
FOV_HORIZONTAL = 70    # 水平方向：左右各 ±70°
FOV_UP = 50            # 垂直向上：+50°（相对于重力水平面）
FOV_DOWN = 60          # 垂直向下：-60°（相对于重力水平面）

def check_visual_field(P_target, P_head, body_forward):
    """
    判断目标点是否在用户的有效视野范围内。
    垂直偏角以重力水平面（经过用户眼睛的水平面）为基准，
    不随用户抬头/低头而改变。
    """
    direction = normalize(P_target - P_head)

    # 水平偏角（相对于身体朝前方向）
    horizontal_angle = angle_in_horizontal_plane(direction, body_forward)

    # 垂直偏角（相对于重力水平面，向上为正）
    vertical_angle = elevation_angle(direction)

    if abs(horizontal_angle) > FOV_HORIZONTAL:
        return False
    if vertical_angle > FOV_UP:
        return False
    if vertical_angle < -FOV_DOWN:
        return False

    return True
```

超出此范围的点直接归类为"不可达"，不进入后续评估。

### 3.3 约束二：关节活动度

肩关节通过以下运动自由度控制手臂的空间指向：

| 自由度 | 运动描述 | 实用活动范围 |
| :--- | :--- | :--- |
| 屈曲 (Flexion) | 手臂向前上方抬起 | 0° – 150° |
| 伸展 (Extension) | 手臂向后方摆动 | 0° – 40° |
| 外展 (Abduction) | 手臂向外侧抬起 | 0° – 150° |
| 内收 (Adduction) | 手臂越过身体中线 | 0° – 30° |
| 外旋 (External Rotation) | 上臂沿自身轴向外旋转 | 0° – 80° |
| 内旋 (Internal Rotation) | 上臂沿自身轴向内旋转 | 0° – 70° |

所有角度以手臂自然下垂为 0° 起点。内旋/外旋在肘关节弯曲时会显著改变手在空间中的位置（前臂绕上臂轴线扫动），因此纳入可达性模型。

**关于身体后方空间：** 肩关节伸展仅约 40°，意味着手臂最多向后偏离身体约 40°（此时手仍远低于水平面）。身体正后方在肩关节的运动范围之外，属于不可达区域。实际上，该区域已被 3.2 的视野约束（±70°）排除。

**自由度耦合：** 当手臂斜向伸展时需要同时使用多个自由度，各自的可用范围会因关节结构的相互约束而缩减：

| 组合情况 | 耦合效果 |
| :--- | :--- |
| 屈曲 + 外展同时较大 | 各自上限约减少 15%（如屈曲从 150° 降至约 130°） |
| 伸展 + 外展 | 外展上限大幅降至约 25° |
| 屈曲 + 内收 | 内收范围略增（前方跨中线较容易，可达约 40°） |
| 伸展 + 内收 | 几乎不可达 |
| 高屈曲/外展 + 内旋 | 内旋范围随抬升角度增大而缩减（肩峰撞击限制） |
| 低屈曲 + 外旋 | 外旋范围充裕，前臂可大幅向外侧扫动 |

```
def check_joint_rom(P_target, P_shoulder, body_forward, body_right,
                    L_upper, L_forearm):
    """
    将目标方向分解为肩关节各自由度分量，
    检查是否在关节活动范围内。
    """
    direction = normalize(P_target - P_shoulder)

    # === 第一步：分解屈曲/伸展 和 外展/内收 ===
    # 这两个自由度决定上臂的指向方向（即肘关节在空间中的位置）。
    # 将目标方向分别投影到矢状面和冠状面即可获得。

    # 矢状面投影 → 屈曲/伸展分量
    flex_ext = compute_flexion_extension(direction, body_forward)

    # 冠状面投影 → 外展/内收分量
    abd_add = compute_abduction_adduction(direction, body_right)

    # === 第二步：由上臂指向确定肘关节位置 ===
    # 屈曲/伸展 + 外展/内收 → 上臂方向向量 → 肘关节坐标
    upper_arm_dir = resolve_upper_arm_direction(flex_ext, abd_add,
                                                body_forward, body_right)
    P_elbow = P_shoulder + upper_arm_dir * L_upper

    # === 第三步：反算所需的内旋/外旋角 ===
    # 已知肘关节位置和目标手腕位置，前臂方向随之确定。
    # 前臂相对于上臂轴线的偏转角度即为所需的旋转角：
    #   - 偏向外侧 → 需要外旋
    #   - 偏向内侧 → 需要内旋
    forearm_dir = normalize(P_target - P_elbow)
    rotation = angle_around_axis(forearm_dir, upper_arm_dir)

    # === 第四步：检查所有分量是否在耦合后的 ROM 内 ===
    rom_limits = apply_coupling(flex_ext, abd_add, rotation)

    if not within_limits(flex_ext, abd_add, rotation, rom_limits):
        return False

    return True
```

### 3.4 约束三：距离

手臂的物理长度决定了可达空间的最远边界。

```
def check_distance(P_target, P_shoulder, L_arm):
    """
    判断目标点是否在臂长范围内。
    """
    D = distance(P_target, P_shoulder)
    return D <= L_arm
```

### 3.5 综合可达性判定

三层约束按顺序执行。视野范围最先检查（计算代价最低），通过后再检查关节活动度和距离。

```
def check_reachability(P_target, user_model):
    """
    综合三层约束，判定目标点的可达性。
    """
    P_head = user_model.head_position
    body_forward = user_model.body_forward_direction
    body_right = user_model.body_right_direction

    # === 约束一：视野范围 ===
    if not check_visual_field(P_target, P_head, body_forward):
        return False

    # === 约束二 & 三：关节活动度 + 距离 ===
    P_shoulder = get_nearest_shoulder(P_target, user_model)
    L_arm = get_corresponding_arm_length(P_shoulder, user_model)

    if not check_joint_rom(P_target, P_shoulder, body_forward, body_right):
        return False

    if not check_distance(P_target, P_shoulder, L_arm):
        return False

    return True
```

### 3.6 模态映射规则

| 可达性结果 | 交互模态 | 说明 |
| :--- | :--- | :--- |
| 可达 (reachable = True) | **直接触摸 (Direct Touch)** | 用户可以伸手直接操作 |
| 不可达 (reachable = False) | **眼动+捏合 (Gaze & Pinch)** 或 **射线 (Ray-casting)** | 用户通过注视目标并捏合手指来操作 |

**关于不可达区域内 UI 的放置深度：** 位于 VAC（视觉辐辏调节）舒适区内，本方案不做具体数值规定。

---

## 四、Step 3：空间布局推导 — 肩关节力矩评估

此步骤在 Step 2 判定为"可达"的空间内展开，回答的问题是：**虽然手能摸到，但摸到这个位置有多累？**

### 4.1 生物力学原理

手臂是一根有重量的杠杆，肩关节是支点。当手臂不是自然下垂时，重力会在肩关节产生一个向下拉的扭矩（力矩）。这个力矩就是肩部肌肉需要持续对抗的负荷，也是"猩猩臂效应 (Gorilla Arm)"的直接原因。

关键规律：

- 手臂越往前伸（肘关节越直），力矩越大
- 手臂越往上抬（肩关节屈曲越大），力矩越大
- 手臂自然下垂时，力矩为零（最轻松）
- 手臂完全水平前伸时，力矩最大（最累）

### 4.2 两段式手臂模型

将手臂简化为两个刚性段：**上臂**和**前臂（含手）**。

每段的重心位置基于人体测量学常数（来源：Winter, 2009 - Biomechanics and Motor Control of Human Movement）：

```
# 人体测量学常数（不需要校准，所有人通用的比例）

# 上臂重心位于上臂近端（肩侧）43.6% 处
UPPER_ARM_COM_RATIO = 0.436

# 前臂重心位于前臂近端（肘侧）43.0% 处
FOREARM_COM_RATIO = 0.430

# 上臂质量占全臂质量的比例（约 54%）
UPPER_ARM_MASS_RATIO = 0.54

# 前臂+手质量占全臂质量的比例（约 46%）
FOREARM_MASS_RATIO = 0.46
```

### 4.3 逆运动学：从目标点反推手臂姿态

当用户要把手伸到空间中的某个点 P_target 时，需要反推出此时手臂的姿态（肩关节角度和肘关节角度），才能计算力矩。

```
def compute_arm_angles(P_target, P_shoulder, L_upper, L_forearm):
    """
    输入：
        P_target:    目标点坐标 (x, y, z)
        P_shoulder:  肩关节坐标 (x, y, z)
        L_upper:     上臂长
        L_forearm:   前臂长
    输出：
        alpha:  肩关节抬升角（0=自然下垂, 90=水平前伸, >90=举过肩）
        beta:   肘关节弯曲角（0=完全伸直, 90=弯成直角）
    """

    # 目标点相对于肩关节的向量
    dx = P_target.x - P_shoulder.x
    dy = P_target.y - P_shoulder.y  # 正值=在肩膀上方, 负值=在肩膀下方
    dz = P_target.z - P_shoulder.z

    # 肩关节到目标点的直线距离
    D = sqrt(dx*dx + dy*dy + dz*dz)

    # 如果目标点超出臂长，无法触达（应在 Step 2 已排除）
    if D > L_upper + L_forearm:
        return None

    # 用余弦定理求肘关节弯曲角
    cos_beta = (L_upper*L_upper + L_forearm*L_forearm - D*D)
               / (2 * L_upper * L_forearm)
    beta = acos(cos_beta)

    # 肩关节抬升角（目标向量相对于竖直向下方向的夹角）
    # alpha = 0 表示目标在正下方（手臂自然下垂）
    # alpha = 90 表示目标在水平方向
    # alpha > 90 表示目标在肩膀上方
    vertical_down = (0, -1, 0)
    alpha = angle_between((dx, dy, dz), vertical_down)

    return alpha, beta
```

### 4.4 归一化力矩计算

```
def compute_normalized_torque(alpha, beta, L_upper, L_forearm):
    """
    输入：
        alpha:      肩关节抬升角
        beta:       肘关节弯曲角
        L_upper:    上臂长
        L_forearm:  前臂长
    输出：
        normalized_torque: 归一化疲劳指数 (0.0 ~ 1.0)
            0.0 = 手臂自然下垂，零负荷
            1.0 = 手臂完全水平伸直，最大负荷
    """

    # --- 当前姿态的力矩 ---

    # 上臂重心的水平力臂（距肩关节的水平距离）
    upper_com_horizontal = UPPER_ARM_COM_RATIO * L_upper * sin(alpha)

    # 肘关节的水平位置（距肩关节）
    elbow_horizontal = L_upper * sin(alpha)

    # 前臂重心的水平力臂
    # 前臂方向取决于 alpha 和 beta 的组合
    forearm_angle = alpha - (pi - beta)
    forearm_com_horizontal = elbow_horizontal
                           + FOREARM_COM_RATIO * L_forearm * sin(forearm_angle)

    # 当前总力矩（归一化后质量会消除）
    current_torque = (UPPER_ARM_MASS_RATIO * upper_com_horizontal
                    + FOREARM_MASS_RATIO * forearm_com_horizontal)

    # --- 最大力矩（手臂完全水平伸直: alpha=90度, beta=0度） ---

    max_upper_horizontal = UPPER_ARM_COM_RATIO * L_upper
    max_elbow_horizontal = L_upper
    max_forearm_horizontal = max_elbow_horizontal
                           + FOREARM_COM_RATIO * L_forearm

    max_torque = (UPPER_ARM_MASS_RATIO * max_upper_horizontal
                + FOREARM_MASS_RATIO * max_forearm_horizontal)

    # --- 归一化 ---
    normalized_torque = max(0.0, current_torque / max_torque)
    normalized_torque = min(1.0, normalized_torque)

    return normalized_torque
```

### 4.5 MVC 阈值分区

**最大自主收缩力（MVC, Maximum Voluntary Contraction）** 是指一块肌肉或一组肌群在意志控制下能够产生的最大等长收缩力。它是肌肉疲劳研究中最常用的基准尺度——后续所有疲劳阈值均以 MVC 的百分比来表达（例如"15% MVC"意味着当前肌肉负荷为其最大能力的 15%）。

**影响 MVC 的主要因素：**

| 因素 | 影响方向 | 说明 |
| :--- | :--- | :--- |
| 肌群部位 | 不同肌群差异显著 | 肩关节屈肌的 MVC 远小于股四头肌；本模型关注的是肩部肌群 |
| 性别 | 男性通常高于女性 | 肩部肌群的绝对 MVC 差异约 30%–50% |
| 年龄 | 随年龄增长而下降 | 峰值通常在 20–35 岁，此后逐步衰减 |
| 训练水平 | 训练者显著高于未训练者 | 力量训练可提高 MVC，但对疲劳耐受百分比影响较小 |
| 关节角度 | 不同角度下 MVC 不同 | 肌肉存在最优长度-张力关系，角度偏离最优位置时 MVC 下降 |
| 肌肉横截面积 | 截面积越大，MVC 越高 | 是个体间差异的主要解剖学来源 |
| 疲劳状态 | 已疲劳的肌肉 MVC 下降 | 先前的持续负荷会暂时降低可用 MVC |

**为什么个体间 MVC 的差异不影响本模型？** 虽然不同用户的绝对 MVC 值可能相差数倍，但肌肉疲劳研究一致表明：**疲劳发生的百分比阈值在个体间是高度一致的**。无论一个人的肩部 MVC 是 40N 还是 80N，当持续负荷超过其自身 MVC 的约 15% 时，都会在相近的时间尺度内出现疲劳。这正是本模型采用归一化疲劳指数（比值）而非绝对力矩值的原因——它天然地适配了不同体质的用户。

基于肌肉疲劳研究（Sjogaard et al., 1986; Rohmert, 1960），持续肌肉负荷与可维持时长的关系：

- **低于 15% MVC：** 可持续长时间工作（30 分钟以上）无明显疲劳
- **15% ~ 30% MVC：** 数分钟内出现疲劳感
- **超过 30% MVC：** 仅能维持数十秒到数分钟

将归一化力矩值映射到三个分区：

```
# 阈值定义（可配置参数）
THRESHOLD_COMFORT  = 0.15   # 舒适区上限
THRESHOLD_MODERATE = 0.30   # 过渡区上限

def classify_zone(normalized_torque):
    if normalized_torque <= THRESHOLD_COMFORT:
        return "舒适区 (Comfort Zone)"
    elif normalized_torque <= THRESHOLD_MODERATE:
        return "过渡区 (Transition Zone)"
    else:
        return "高负荷区 (High-Load Zone)"
```

**重要说明：** 0.15 和 0.30 是基于文献的默认值，可根据目标用户群进行调整。底层连续值始终可用，分区标签只是表层翻译。

### 4.6 垂直高度与水平角度的影响

力矩模型已自然包含了高度和角度的影响，以下描述其物理直觉供参考：

**垂直方向的规律：**

| 手部位置 | 力矩趋势 | 原因 |
| :--- | :--- | :--- |
| 肩膀正下方（自然下垂） | 最低 (接近 0) | 重力方向与骨骼方向一致，肌肉几乎不需要发力 |
| 肘部高度（前臂前伸 90 度） | 低 | 上臂仍然下垂，仅前臂产生力矩 |
| 肩膀高度（手臂水平伸出） | **最高（力矩峰值）** | 整条手臂的重心水平力臂达到最大值，sin(α) = 1 |
| 高于肩膀（手臂上举） | 力矩回落，但主观疲劳感可能更强 | 手臂超过水平后，重心水平力臂随 sin(α) 减小，力矩开始下降；但血液回流受阻、肩峰撞击等额外生理因素会加速主观疲劳，使该区域的实际体验比力矩数值所暗示的更差 |

**水平方向的规律：**

| 手部位置 | 力矩趋势 | 原因 |
| :--- | :--- | :--- |
| 身体正前方 | 基准值 | 标准前伸姿态 |
| 侧方（同侧） | 略高 | 肩关节外展，三角肌中束额外受力 |
| 对侧（跨身体中线） | 明显更高 | 需要额外的肩关节内收和躯干旋转 |

### 4.7 A 层：通用功能级推荐

基于疲劳分区，给出通用的功能建议：

| 分区 | 通用功能建议 | 交互频率 | 操作时长限制 |
| :--- | :--- | :--- | :--- |
| **舒适区** | 核心交互区：放置需要频繁操作、精密控制的内容 | 高频 | 无限制 |
| **过渡区** | 快捷控制区：放置偶尔触发、即点即走的内容 | 低频 | 单次操作建议 < 10 秒 |
| **高负荷区** | 信息展示区：放置仅供查看或极少操作的内容 | 极低频 | 单次操作建议 < 3 秒 |
| **不可达区** | 纯视觉区：放置仅供观看的内容，模态必须切换 | 仅限远程 | 不适用 |

**关于操作时长限制与 MVC 耐受时长的关系：** 4.5 节引用的 MVC 文献给出的是一次性静态维持某负荷水平直到疲劳出现的**生理耐受时长**（过渡区约数分钟，高负荷区约数十秒至数分钟）。而此处的操作时长限制是面向整个使用会话的**设计指导值**，两者度量的尺度不同。XR 应用的典型会话时长可达 30 分钟甚至更久，在此期间用户可能反复进入较高负荷区域执行操作。如果每次停留都逼近生理耐受极限，累积疲劳会远超单次测量所暗示的水平，且肌肉在两次操作之间可能无法充分恢复。因此，操作时长限制在生理耐受时长的基础上施加了大幅余量，确保单次操作足够短暂，使手臂在操作间隙能回到低负荷或静息状态，从而将整个会话的累积疲劳控制在可接受范围内。

### 4.8 B 层：具体组件级推荐

在 A 层的基础上，根据每种组件的交互特征（精度需求、操作时长、运动方向）进一步匹配：

**舒适区适合的组件：**

| 组件 | 匹配理由 |
| :--- | :--- |
| 虚拟键盘 (Virtual Keyboard) | 需要高频、高精度的连续点按，操作时间长 |
| 滑块 (Slider) | 需要精细的水平/垂直拖拽控制 |
| 绘图板 (Drawing Canvas) | 需要手部稳定性和长时间悬停 |
| 3D 变换手柄 (Gizmo) | 需要多方向精密拖拽 |
| 复杂菜单 (Nested Menu) | 需要多次精确点选 |

**过渡区适合的组件：**

| 组件 | 匹配理由 |
| :--- | :--- |
| 功能开关 (Toggle) | 仅需一次点按，接触面积大，容错率高 |
| 工具栏 (Tool Palette) | 选完工具后手立刻回到舒适区操作 |
| 标签页 (Tab Bar) | 低频切换，点按即可 |
| 确认按钮 (Action Button) | 单次触发，目标尺寸可以放大 |

**高负荷区（仍在可达范围内）适合的组件：**

| 组件 | 匹配理由 |
| :--- | :--- |
| 通知气泡 (Notification) | 仅需偶尔点一下消除 |
| 最小化窗口 (Minimized Window) | 极低频触发 |

> 注意：此区域虽然物理上可达，但建议优先使用远场交互模态（眼动+捏合）来操作。

**不可达区（远场）适合的组件：**

| 组件 | 匹配理由 |
| :--- | :--- |
| 视频播放器 (Video Player) | 纯观看为主，偶尔用眼动控制播放 |
| 数据看板 (Dashboard) | 信息展示，不需要手动操作 |
| 环境装饰 (Ambient UI) | 氛围营造，无需交互 |

### 4.9 交互动作类型推荐

**舒适区推荐动作（直接触摸模态）：**

| 动作类型 | 适用理由 |
| :--- | :--- |
| 精细拖拽 (Drag) | 手臂稳定，可以做小幅精密移动 |
| 旋转 (Rotate) | 手腕在此位置灵活性最高 |
| 双手操作 (Two-handed) | 双手均在舒适范围内，可以协同缩放、旋转 |
| 连续书写 (Draw/Write) | 手部稳定性足以支持书写精度 |
| 高频点按 (Rapid Tap) | 手指灵活，不会因手臂晃动导致误触 |

**过渡区推荐动作（直接触摸模态）：**

| 动作类型 | 适用理由 |
| :--- | :--- |
| 单次点按 (Tap) | 简单直接，不需要手臂在此位置停留 |
| 推/拉 (Push/Pull) | 利用大臂的整体运动，减少手腕精细负担 |
| 大幅挥动 (Swipe) | 借助手臂回收的自然运动（翻页、切歌） |

**远场推荐动作（眼动+手势模态）：**

| 动作类型 | 适用理由 |
| :--- | :--- |
| 注视+捏合确认 (Gaze & Pinch) | 眼睛瞄准，手指捏合触发，手臂无需抬起 |
| 注视+捏合滚动 (Gaze & Scroll) | 注视目标后捏合并上下微移手指 |
| 射线指向 (Ray-cast) | 手臂微抬指向远处，仅需短暂维持 |

---

## 五、使用方法

### 5.1 用法一：逐点查询（最常用）

开发者已有一个候选位置，直接问模型"这个点怎么样"。

```
result = evaluate_spatial_point(
    P_target = (0.0, 1.4, -0.4),  # 世界坐标中的候选位置
    user_model = calibrated_user_data
)

# 返回结果示例
# {
#     "zone": "过渡区",
#     "fatigue_index": 0.23,
#     "modality": "直接触摸",
#     "functional_recommendation": "快捷控制区，适合低频、简单、即点即走操作",
#     "recommended_components": ["功能开关", "工具栏", "标签页", "大按钮"],
#     "recommended_actions": ["单次点按", "推/拉", "大幅挥动"],
#     "time_limit": "单次操作建议 < 10秒"
# }
```

### 5.2 用法二：最优位置推荐（反向查询）

开发者知道自己要放什么组件，让模型帮忙找最佳位置。

```
best_position = find_optimal_position(
    component_type = "keyboard",
    user_model = calibrated_user_data
)

# 返回结果示例
# {
#     "recommended_center": (0.0, 1.05, -0.32),
#     "fatigue_index": 0.08,
#     "zone": "舒适区"
# }
```

实现原理：在可达空间内采样大量点，计算每个点的疲劳指数，根据组件类型的需求（如键盘需要低疲劳+高精度），返回疲劳指数最低的区域中心。

### 5.3 用法三：可视化热力图（设计工具用）

在空间中均匀采样大量点，为每个点计算疲劳指数，生成一个 3D 热力图。设计师可以直观看到哪里是绿色（舒适）、哪里是红色（高负荷）。

```
def generate_heatmap(user_model, resolution=0.05):
    """
    在用户周围的空间中，每隔 resolution 米采样一个点，
    为每个点计算疲劳指数。
    """
    points = []

    for x in range(-1.0, 1.0, resolution):
        for y in range(0.5, 2.0, resolution):
            for z in range(-1.0, 0.0, resolution):
                P = (x, y, z)
                result = evaluate_spatial_point(P, user_model)
                points.append({
                    "position": P,
                    "fatigue_index": result["fatigue_index"],
                    "zone": result["zone"]
                })

    return points

# 输出可以渲染为 3D 热力图
# 绿色点 = 舒适区, 黄色点 = 过渡区, 红色点 = 高负荷区, 无点 = 不可达
```

### 5.4 使用方法对照表

| 用法 | 输入 | 输出 | 适合谁 |
| :--- | :--- | :--- | :--- |
| 逐点查询 | 一个空间坐标 | 该点的分区、疲劳指数、组件建议 | 开发者（运行时判断） |
| 最优位置推荐 | 一个组件类型 | 推荐放置的坐标 | 开发者（自动布局） |
| 可视化热力图 | 用户身体数据 | 大量空间点的疲劳指数集合 | 设计师（设计阶段参考） |

---

## 六、端到端推导流程（伪代码总结）

```
def evaluate_spatial_point(P_target, user_model):
    """
    输入一个空间中的点，输出该点的完整布局建议。
    """

    # === Step 2: 可达性判定 ===
    P_shoulder = get_nearest_shoulder(P_target, user_model)
    L_arm = get_corresponding_arm_length(P_shoulder, user_model)
    D = distance(P_target, P_shoulder)

    if D > L_arm:
        return {
            "zone": "不可达区（远场）",
            "modality": "眼动+捏合 / 射线",
            "recommended_components": [
                "视频播放器", "数据看板", "通知气泡"
            ],
            "recommended_actions": [
                "注视+捏合确认", "注视+捏合滚动"
            ],
            "fatigue_index": None
        }

    # === Step 3: 力矩评估 ===
    L_upper = get_corresponding_upper_length(P_shoulder, user_model)
    L_forearm = get_corresponding_forearm_length(P_shoulder, user_model)

    alpha, beta = compute_arm_angles(
        P_target, P_shoulder, L_upper, L_forearm
    )
    fatigue_index = compute_normalized_torque(
        alpha, beta, L_upper, L_forearm
    )
    zone = classify_zone(fatigue_index)

    if zone == "舒适区":
        return {
            "zone": "舒适区",
            "modality": "直接触摸",
            "fatigue_index": fatigue_index,
            "functional_recommendation":
                "核心交互区，适合高频、精密、长时间操作",
            "recommended_components": [
                "键盘", "滑块", "绘图板", "3D手柄", "复杂菜单"
            ],
            "recommended_actions": [
                "精细拖拽", "旋转", "双手操作", "书写", "高频点按"
            ]
        }

    elif zone == "过渡区":
        return {
            "zone": "过渡区",
            "modality": "直接触摸",
            "fatigue_index": fatigue_index,
            "functional_recommendation":
                "快捷控制区，适合低频、简单、即点即走操作",
            "recommended_components": [
                "功能开关", "工具栏", "标签页", "大按钮"
            ],
            "recommended_actions": [
                "单次点按", "推/拉", "大幅挥动"
            ],
            "time_limit": "单次操作建议 < 10秒"
        }

    else:  # 高负荷区
        return {
            "zone": "高负荷区",
            "modality": "直接触摸（建议切换为眼动+捏合）",
            "fatigue_index": fatigue_index,
            "functional_recommendation":
                "信息展示区，极少操作",
            "recommended_components": [
                "通知气泡", "最小化窗口"
            ],
            "recommended_actions": ["单次点按"],
            "time_limit": "单次操作建议 < 3秒"
        }
```

---

## 七、完整变量表

| 变量名 | 含义 | 来源 | 是否因人而异 |
| :--- | :--- | :--- | :--- |
| P_head | 头部中心实时坐标 | 设备传感器 | 是（实时） |
| L_arm_left / right | 全臂长 | 校准动作 A | 是 |
| L_upper_left / right | 上臂长 | 校准推算 | 是 |
| L_forearm_left / right | 前臂长 | 校准动作 B | 是 |
| S_offset_down | 肩关节垂直偏移 | 校准推算 | 是 |
| S_offset_left / right | 肩关节水平偏移 | 校准推算 | 是 |
| H_shoulder | 肩关节离地高度 | 校准推算 | 是 |
| H_elbow | 肘部离地高度 | 校准动作 B | 是 |
| UPPER_ARM_COM_RATIO | 上臂重心比例 (0.436) | 人体测量学文献 | 否（常数） |
| FOREARM_COM_RATIO | 前臂重心比例 (0.430) | 人体测量学文献 | 否（常数） |
| UPPER_ARM_MASS_RATIO | 上臂质量比例 (0.54) | 人体测量学文献 | 否（常数） |
| FOREARM_MASS_RATIO | 前臂质量比例 (0.46) | 人体测量学文献 | 否（常数） |
| THRESHOLD_COMFORT | 舒适区阈值 (0.15) | MVC 文献 | 否（可配置） |
| THRESHOLD_MODERATE | 过渡区阈值 (0.30) | MVC 文献 | 否（可配置） |

---

## 八、参考文献

- Winter, D.A. (2009). *Biomechanics and Motor Control of Human Movement*. 4th Edition.
- Sjogaard, G. et al. (1986). Intramuscular pressure, EMG and blood flow during low-level prolonged static contraction in man. *Acta Physiologica Scandinavica*.
- Rohmert, W. (1960). Ermittlung von Erholungspausen fur statische Arbeit des Menschen. *Internationale Zeitschrift fur Angewandte Physiologie*.
- ISO 9241-920: Ergonomics of human-system interaction - Guidance on tactile and haptic interactions.
