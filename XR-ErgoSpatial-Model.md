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

### 1.4 文档结构

本文档的后续章节按照模型的构建逻辑依次展开：

| 章节 | 内容 | 核心依据 |
| :--- | :--- | :--- |
| 二、身体数据采集 | 通过校准动作获取用户的臂长、肩关节位置等个体化参数 | 引导动作 + 设备传感器 |
| 三、交互模态决策 | 基于臂长判断目标点是否可达，决定使用直接触摸还是远程模态 | 物理可达性（骨骼硬约束） |
| 四、空间布局推导 | 对可达空间内的目标点评估肩关节力矩，划分疲劳分区，匹配组件与动作 | 肩关节力矩模型 + MVC 阈值 |
| 五、使用方法 | 逐点查询、最优位置推荐、可视化热力图三种使用方式 | — |
| 六、端到端伪代码 | 完整推导流程的伪代码实现 | — |
| 七、完整变量表 | 模型涉及的所有变量及其来源 | — |
| 八、参考文献 | 生物力学与肌肉疲劳领域的学术依据 | — |

---

## 二、Step 1：显式校准 — 身体数据采集

### 2.1 校准动作

**动作 A：T-Pose（双臂侧平举）**

用户站直（或坐正），双臂向两侧水平伸展。系统记录：

- 左手腕坐标、右手腕坐标
- 头部坐标

**动作 B：Ready-Pose（交互预备姿态）**

用户大臂自然下垂贴近身体，小臂向前伸出约 90 度。系统记录：

- 左手腕坐标、右手腕坐标
- 头部坐标

### 2.2 采集的变量清单

通过上述两个动作，计算并存储以下变量：

```
# ===== 核心身体变量 =====

# 全臂长（肩关节到手腕的直线距离）
# 来源：T-Pose 时，(手腕坐标 - 估算肩关节坐标) 的长度
L_arm_left          # 左臂全长
L_arm_right         # 右臂全长

# 上臂长（肩关节到肘关节）
# 来源：T-Pose 与 Ready-Pose 的几何推算
L_upper_left        # 左上臂长
L_upper_right       # 右上臂长

# 前臂长（肘关节到手腕）
# 来源：Ready-Pose 时，肘关节到手腕的距离
L_forearm_left      # 左前臂长
L_forearm_right     # 右前臂长

# 肩关节相对于头部的偏移量
S_offset_down       # 肩关节在头部下方的垂直距离
S_offset_left       # 左肩相对于头部中轴线的水平偏移
S_offset_right      # 右肩相对于头部中轴线的水平偏移

# 肩关节高度（离地）
H_shoulder_left     # 左肩高度
H_shoulder_right    # 右肩高度

# 肘部高度（Ready-Pose 时）
H_elbow             # 肘部离地高度（自然垂臂时）
```

### 2.3 肩关节坐标估算

由于 visionOS 无法直接获取肩关节位置，通过头部坐标加偏移量来推算：

```
# P_head = 头显实时坐标 (x, y, z)

P_shoulder_left = (
    P_head.x - S_offset_left,
    P_head.y - S_offset_down,
    P_head.z
)

P_shoulder_right = (
    P_head.x + S_offset_right,
    P_head.y - S_offset_down,
    P_head.z
)
```

### 2.4 姿态检测（可选扩展功能）

坐姿/站姿检测不作为核心流程的一部分。原因如下：

- 力矩模型的输入是"目标点相对于肩关节的相对位置"，肩关节坐标会随头部坐标自动更新，因此模型本身无需区分坐/站。
- 臂长等身体尺寸变量不随姿态改变。

如果未来需要姿态检测（例如：坐姿时大腿会遮挡正下方空间），可作为独立模块扩展，不影响核心推导逻辑。

---

## 三、Step 2：交互模态决策 — 物理可达性判断

### 3.1 理论依据

此步骤只回答一个问题：**用户的手能不能物理触碰到这个点？**

- **能触碰** → 允许使用直接触摸 (Direct Touch)
- **不能触碰** → 必须使用眼动+手势 (Gaze & Pinch) 或射线 (Ray-casting)

判定标准是**臂长**。这是人体骨骼结构决定的硬性物理约束。

### 3.2 判定公式

```
# 对于空间中的任意一个目标点 P_target：

# 计算该点到左、右肩关节的距离，取较小值
D_left  = distance(P_target, P_shoulder_left)
D_right = distance(P_target, P_shoulder_right)
D = min(D_left, D_right)

# 使用距离较近的那侧手臂的臂长作为判定依据
if D == D_left:
    L_arm = L_arm_left
else:
    L_arm = L_arm_right

# 可达性判定
if D <= L_arm:
    reachable = True
else:
    reachable = False
```

### 3.3 模态映射规则

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
| 肩膀高度（手臂水平伸出） | 高 | 整条手臂都在对抗重力 |
| 高于肩膀（手臂上举） | 最高 | 力矩最大，且血液回流受阻，疲劳加速 |

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
