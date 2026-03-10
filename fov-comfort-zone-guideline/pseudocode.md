# 验证/建议工具伪代码

## 概述

本文档描述两类工具的伪代码设计：

1. **输入验证型**：设计师输入 UI 元素的角度参数，工具返回区域判定、舒适度评级和设计建议
2. **可视化编排型**：提供二维视野地图，支持拖放 UI 元素，实时显示区域反馈

---

## Part 1: 数据模型

### 1.1 区域定义

```
ENUM ComfortLevel:
    OPTIMAL     = 5    // ★★★★★ 最佳
    COMFORTABLE = 4    // ★★★★☆ 舒适
    MODERATE    = 3    // ★★★☆☆ 适度
    EFFORTFUL   = 2    // ★★☆☆☆ 费力
    EXTREME     = 1    // ★☆☆☆☆ 极限
    AVOID       = 0    // ☆☆☆☆☆ 避免

ENUM ContentType:
    PRIMARY_INTERACTION    // 主交互面板
    INFORMATION_DISPLAY    // 信息展示
    NOTIFICATION           // 通知/提示
    NAVIGATION             // 导航元素
    MEDIA                  // 媒体内容
    AMBIENT                // 环境氛围

ENUM Posture:
    STANDING    // 站姿，自然视线偏移 = -10°
    SITTING     // 坐姿，自然视线偏移 = -15°

ENUM AnchorType:
    BODY_LOCKED
    WORLD_LOCKED
    HEAD_LOCKED
```

### 1.2 区域阈值表

```
STRUCT HorizontalZone:
    id          : STRING       // "H0", "H1", ...
    name        : STRING       // "静默焦点区", ...
    min_angle   : FLOAT        // 水平绝对值下界（度）
    max_angle   : FLOAT        // 水平绝对值上界（度）
    comfort     : ComfortLevel
    feel        : STRING       // 身体感受描述
    max_dwell   : STRING       // 最大建议停留时间

STRUCT VerticalZone:
    id          : STRING
    name        : STRING
    min_angle   : FLOAT        // 从自然视线起算的绝对值下界
    max_angle   : FLOAT
    direction   : "up" | "down" | "center"
    comfort     : ComfortLevel
    feel        : STRING

CONST H_ZONES : LIST<HorizontalZone> = [
    { "H0", "静默焦点区",   0,  10, OPTIMAL,     "完全无感...",        "无限" },
    { "H1", "核心舒适区",  10,  25, COMFORTABLE, "轻松自在...",        "数分钟" },
    { "H2", "自然转视区",  25,  45, MODERATE,    "轻微转头...",        "数十秒" },
    { "H3", "刻意转头区",  45,  70, EFFORTFUL,   "刻意转头...",        "数秒" },
    { "H4", "极限边缘区",  70, 100, EXTREME,     "大幅回头...",        "瞬间" },
    { "H5", "身体转向区", 100, 180, AVOID,       "需要躯干转动...",    "避免" },
]

CONST V_ZONES_UP : LIST<VerticalZone> = [
    { "V0",  "自然视线区",   0,  5, "center", OPTIMAL,     "完全无感..." },
    { "V+1", "舒适上视区",   5, 15, "up",     COMFORTABLE, "轻微上瞥..." },
    { "V+2", "适度上视区",  15, 25, "up",     MODERATE,    "轻微仰头..." },
    { "V+3", "极限上视区",  25, 90, "up",     EXTREME,     "明显仰头..." },
]

CONST V_ZONES_DOWN : LIST<VerticalZone> = [
    { "V0",  "自然视线区",   0,  5, "center", OPTIMAL,     "完全无感..." },
    { "V-1", "舒适下视区",   5, 20, "down",   COMFORTABLE, "轻微下瞥..." },
    { "V-2", "适度下视区",  20, 35, "down",   MODERATE,    "中度低头..." },
    { "V-3", "极限下视区",  35, 90, "down",   EXTREME,     "过度低头..." },
]
```

### 1.3 内容类型推荐规则

```
STRUCT ContentPlacementRule:
    content_type       : ContentType
    recommended_h      : RANGE      // 推荐水平角度范围
    recommended_v      : RANGE      // 推荐垂直角度范围
    max_tolerable_h    : RANGE      // 最大容许水平范围
    max_tolerable_v    : RANGE      // 最大容许垂直范围
    rationale          : STRING

CONST PLACEMENT_RULES : LIST<ContentPlacementRule> = [
    {
        PRIMARY_INTERACTION,
        recommended_h: { ±0° ~ ±25° },
        recommended_v: { +5° ~ -20° },
        max_tolerable_h: { ±0° ~ ±45° },
        max_tolerable_v: { +15° ~ -35° },
        rationale: "频繁操作需最低运动代价，下方偏移符合手部操作位置"
    },
    {
        INFORMATION_DISPLAY,
        recommended_h: { ±0° ~ ±25° },
        recommended_v: { -5° ~ +15° },
        max_tolerable_h: { ±0° ~ ±45° },
        max_tolerable_v: { -20° ~ +15° },
        rationale: "阅读需要中央凹视觉，略偏上符合信息展示直觉"
    },
    {
        NOTIFICATION,
        recommended_h: { ±15° ~ ±35° },
        recommended_v: { +5° ~ +15° },
        max_tolerable_h: { ±10° ~ ±45° },
        max_tolerable_v: { +5° ~ +25° },
        rationale: "周边可感知但不遮挡主任务，上方有跳出感"
    },
    {
        NAVIGATION,
        recommended_h: { ±25° ~ ±70° },
        recommended_v: { -5° ~ +5° },
        max_tolerable_h: { ±0° ~ ±100° },
        max_tolerable_v: { -20° ~ +15° },
        rationale: "服务于空间定位，本身需要分布在较广范围"
    },
    {
        MEDIA,
        recommended_h: { ±0° ~ ±10° },
        recommended_v: { -5° ~ +5° },
        max_tolerable_h: { ±0° ~ ±25° },
        max_tolerable_v: { -20° ~ +15° },
        rationale: "持续观看需最大舒适度"
    },
    {
        AMBIENT,
        recommended_h: { ±45° ~ ±100° },
        recommended_v: { 任意 },
        max_tolerable_h: { ±0° ~ ±180° },
        max_tolerable_v: { 任意 },
        rationale: "不需要直接注视，营造空间感"
    }
]
```

### 1.4 UI 元素数据结构

```
STRUCT UIElement:
    id              : STRING
    name            : STRING
    content_type    : ContentType
    h_angle         : FLOAT        // 水平角度（正 = 右，负 = 左）
    v_angle         : FLOAT        // 垂直角度（正 = 上，负 = 下）（相对自然视线）
    angular_width   : FLOAT        // 元素的水平角宽度
    angular_height  : FLOAT        // 元素的垂直角高度
    anchor_type     : AnchorType
    interaction_freq: "high" | "medium" | "low" | "none"  // 交互频率
    dwell_time      : "sustained" | "brief" | "glance"    // 预期注视时长
```

---

## Part 2: 输入验证型工具

### 2.1 核心判定函数

```
FUNCTION classify_horizontal(h_angle_abs : FLOAT) -> HorizontalZone:
    FOR zone IN H_ZONES:
        IF h_angle_abs >= zone.min_angle AND h_angle_abs < zone.max_angle:
            RETURN zone
    RETURN H_ZONES.last    // 默认归入最外区域

FUNCTION classify_vertical(v_angle : FLOAT) -> VerticalZone:
    IF v_angle >= 0:
        abs_val = v_angle
        FOR zone IN V_ZONES_UP:
            IF abs_val >= zone.min_angle AND abs_val < zone.max_angle:
                RETURN zone
        RETURN V_ZONES_UP.last
    ELSE:
        abs_val = ABS(v_angle)
        FOR zone IN V_ZONES_DOWN:
            IF abs_val >= zone.min_angle AND abs_val < zone.max_angle:
                RETURN zone
        RETURN V_ZONES_DOWN.last

FUNCTION composite_comfort(h_zone : HorizontalZone, v_zone : VerticalZone) -> ComfortLevel:
    RETURN MIN(h_zone.comfort, v_zone.comfort)
```

### 2.2 单元素验证

```
FUNCTION validate_element(element : UIElement, posture : Posture) -> ValidationResult:

    // Step 1: 区域判定
    h_zone = classify_horizontal(ABS(element.h_angle))
    v_zone = classify_vertical(element.v_angle)
    comfort = composite_comfort(h_zone, v_zone)

    // Step 2: 覆盖范围检查（元素可能跨区域）
    h_left_edge  = ABS(element.h_angle) - element.angular_width / 2
    h_right_edge = ABS(element.h_angle) + element.angular_width / 2
    v_top_edge   = element.v_angle + element.angular_height / 2
    v_bottom_edge = element.v_angle - element.angular_height / 2

    h_zone_left  = classify_horizontal(MAX(0, h_left_edge))
    h_zone_right = classify_horizontal(h_right_edge)
    v_zone_top   = classify_vertical(v_top_edge)
    v_zone_bottom = classify_vertical(v_bottom_edge)

    spans_multiple_h = (h_zone_left.id != h_zone_right.id)
    spans_multiple_v = (v_zone_top.id != v_zone_bottom.id)

    // Step 3: 内容类型匹配检查
    rule = FIND rule IN PLACEMENT_RULES WHERE rule.content_type == element.content_type
    in_recommended = is_within_range(element.h_angle, element.v_angle, rule.recommended_h, rule.recommended_v)
    in_tolerable   = is_within_range(element.h_angle, element.v_angle, rule.max_tolerable_h, rule.max_tolerable_v)

    // Step 4: 交互频率 vs 区域舒适度检查
    freq_comfort_ok = check_frequency_comfort(element.interaction_freq, comfort)

    // Step 5: 注视时长 vs 区域舒适度检查
    dwell_comfort_ok = check_dwell_comfort(element.dwell_time, comfort)

    // Step 6: 生成结果
    result = new ValidationResult()
    result.element       = element
    result.h_zone        = h_zone
    result.v_zone        = v_zone
    result.comfort       = comfort
    result.warnings      = []
    result.suggestions   = []

    IF NOT in_tolerable:
        result.warnings.ADD("严重：元素超出内容类型的最大容许范围")
        result.suggestions.ADD(suggest_position(element))

    ELSE IF NOT in_recommended:
        result.warnings.ADD("注意：元素不在推荐区域内，但在容许范围内")
        result.suggestions.ADD(suggest_position(element))

    IF NOT freq_comfort_ok:
        result.warnings.ADD("警告：高频交互内容放置在低舒适度区域，可能导致颈部疲劳")

    IF NOT dwell_comfort_ok:
        result.warnings.ADD("警告：需要持续注视的内容放置在非最佳区域")

    IF spans_multiple_h:
        result.warnings.ADD("提示：元素水平跨越多个舒适区域（{h_zone_left.id} ~ {h_zone_right.id}）")

    IF spans_multiple_v:
        result.warnings.ADD("提示：元素垂直跨越多个舒适区域（{v_zone_top.id} ~ {v_zone_bottom.id}）")

    RETURN result
```

### 2.3 辅助检查函数

```
FUNCTION check_frequency_comfort(freq : STRING, comfort : ComfortLevel) -> BOOL:
    IF freq == "high":
        RETURN comfort >= COMFORTABLE    // 高频交互至少需要 ★★★★☆
    IF freq == "medium":
        RETURN comfort >= MODERATE       // 中频交互至少需要 ★★★☆☆
    IF freq == "low":
        RETURN comfort >= EFFORTFUL      // 低频交互至少需要 ★★☆☆☆
    RETURN TRUE                          // 无交互（none）无限制

FUNCTION check_dwell_comfort(dwell : STRING, comfort : ComfortLevel) -> BOOL:
    IF dwell == "sustained":
        RETURN comfort >= COMFORTABLE    // 持续注视至少需要 ★★★★☆
    IF dwell == "brief":
        RETURN comfort >= MODERATE       // 短暂注视至少需要 ★★★☆☆
    RETURN TRUE                          // 瞥视无特殊要求
```

### 2.4 位置建议生成

```
FUNCTION suggest_position(element : UIElement) -> PositionSuggestion:

    rule = FIND rule IN PLACEMENT_RULES WHERE rule.content_type == element.content_type

    // 计算推荐区域的中心点
    rec_h_center = (rule.recommended_h.min + rule.recommended_h.max) / 2
    rec_v_center = (rule.recommended_v.min + rule.recommended_v.max) / 2

    // 保持元素原始方向（左/右），只调整绝对角度
    IF element.h_angle >= 0:
        suggested_h = rec_h_center
    ELSE:
        suggested_h = -rec_h_center

    suggested_v = rec_v_center

    // 如果元素原始位置只是略微偏离，建议最小移动量
    h_distance = ABS(element.h_angle) - ABS(suggested_h)
    v_distance = element.v_angle - suggested_v

    IF ABS(h_distance) < 5 AND ABS(v_distance) < 5:
        // 微调即可
        suggested_h = CLAMP(element.h_angle, rule.recommended_h)
        suggested_v = CLAMP(element.v_angle, rule.recommended_v)

    RETURN PositionSuggestion {
        original_h:  element.h_angle,
        original_v:  element.v_angle,
        suggested_h: suggested_h,
        suggested_v: suggested_v,
        reason:      rule.rationale
    }
```

### 2.5 批量布局验证

```
FUNCTION validate_layout(elements : LIST<UIElement>, posture : Posture) -> LayoutReport:

    report = new LayoutReport()
    report.element_results = []
    report.layout_warnings = []
    report.score = 0

    // 逐个验证
    FOR element IN elements:
        result = validate_element(element, posture)
        report.element_results.ADD(result)

    // 布局级别检查

    // 检查 1: 是否有内容在 Golden Zone（H0-H1 × V0-V-1）
    golden_zone_elements = FILTER elements WHERE
        ABS(h_angle) <= 25 AND v_angle >= -20 AND v_angle <= 5
    IF golden_zone_elements.is_empty():
        report.layout_warnings.ADD("布局中没有内容位于黄金区域，主要内容缺乏焦点")

    // 检查 2: Golden Zone 是否被非核心内容占据
    golden_non_primary = FILTER golden_zone_elements WHERE
        content_type IN [AMBIENT, NAVIGATION]
    IF golden_non_primary.is_not_empty():
        report.layout_warnings.ADD("黄金区域被非核心内容占据，可能浪费最佳视觉资源")

    // 检查 3: 元素重叠检测
    FOR i IN 0..elements.length:
        FOR j IN (i+1)..elements.length:
            IF elements_overlap(elements[i], elements[j]):
                report.layout_warnings.ADD(
                    "元素 '{elements[i].name}' 与 '{elements[j].name}' 存在角度重叠"
                )

    // 检查 4: 信息密度递减规则
    // 验证从 H0 到外围，信息密度是否逐渐降低
    density_by_zone = calculate_density_per_zone(elements)
    FOR i IN 1..density_by_zone.length:
        IF density_by_zone[i] > density_by_zone[i-1]:
            report.layout_warnings.ADD(
                "外围区域 {H_ZONES[i].id} 的信息密度高于内侧区域 {H_ZONES[i-1].id}，" +
                "违反了渐进式信息密度原则"
            )

    // 检查 5: 坐姿/站姿兼容性
    IF posture == "both":
        standing_results = validate_layout(elements, STANDING)
        sitting_results  = validate_layout(elements, SITTING)
        incompatible = FIND elements WHERE
            standing_result.comfort != sitting_result.comfort
        IF incompatible.is_not_empty():
            report.layout_warnings.ADD(
                "以下元素在坐/站姿下处于不同舒适等级：{incompatible.names}"
            )

    // 综合评分（0-100）
    report.score = calculate_layout_score(report)

    RETURN report

FUNCTION calculate_layout_score(report : LayoutReport) -> INT:
    score = 100

    FOR result IN report.element_results:
        // 每个元素根据舒适度和是否在推荐区域扣分
        IF result.comfort < COMFORTABLE:
            score -= (COMFORTABLE - result.comfort) * 5
        IF result.warnings.length > 0:
            score -= result.warnings.length * 3

    FOR warning IN report.layout_warnings:
        score -= 5

    RETURN CLAMP(score, 0, 100)
```

### 2.6 元素重叠检测

```
FUNCTION elements_overlap(a : UIElement, b : UIElement) -> BOOL:
    a_left   = a.h_angle - a.angular_width / 2
    a_right  = a.h_angle + a.angular_width / 2
    a_top    = a.v_angle + a.angular_height / 2
    a_bottom = a.v_angle - a.angular_height / 2

    b_left   = b.h_angle - b.angular_width / 2
    b_right  = b.h_angle + b.angular_width / 2
    b_top    = b.v_angle + b.angular_height / 2
    b_bottom = b.v_angle - b.angular_height / 2

    h_overlap = (a_left < b_right) AND (a_right > b_left)
    v_overlap = (a_bottom < b_top) AND (a_top > b_bottom)

    RETURN h_overlap AND v_overlap
```

---

## Part 3: 可视化编排型工具

### 3.1 架构概述

```
可视化编排工具 (Visual Layout Editor)
├── 视野地图层 (Field Map Layer)
│   ├── 背景热力图 — 舒适度色彩渲染
│   ├── 区域网格线 — H0-H5 / V0-V±3 边界
│   └── 黄金区域标注 — Golden Zone 高亮
├── 元素层 (Element Layer)
│   ├── 可拖放的 UI 元素矩形
│   ├── 元素标签与类型图标
│   └── 实时舒适度指示器
├── 反馈层 (Feedback Layer)
│   ├── 元素移动时的吸附引导线
│   ├── 警告/建议气泡
│   └── 区域边界穿越提示
├── 控制面板 (Control Panel)
│   ├── 姿态切换（坐/站）
│   ├── 元素属性编辑器
│   ├── 布局评分仪表盘
│   └── 一键优化建议
└── 导出模块 (Export Module)
    ├── 参数表导出（JSON/CSV）
    └── 布局截图导出
```

### 3.2 视野地图渲染

```
FUNCTION render_field_map(canvas, posture : Posture):

    width  = canvas.width
    height = canvas.height
    center_x = width / 2
    center_y = height / 2

    // 可视范围：水平 ±120°，垂直 ±70°
    H_VISUAL_RANGE = 120
    V_VISUAL_RANGE = 70
    scale_x = (width - MARGIN * 2) / (H_VISUAL_RANGE * 2)
    scale_y = (height - MARGIN * 2) / (V_VISUAL_RANGE * 2)

    // 逐像素渲染舒适度热力图
    FOR px IN MARGIN..(width - MARGIN):
        FOR py IN MARGIN..(height - MARGIN):
            h_angle = (px - center_x) / scale_x
            v_angle = -(py - center_y) / scale_y    // Y轴翻转：屏幕上方 = 正角度

            h_zone = classify_horizontal(ABS(h_angle))
            v_zone = classify_vertical(v_angle)
            comfort = composite_comfort(h_zone, v_zone)

            color = COMFORT_COLOR_MAP[comfort]
            canvas.set_pixel(px, py, color, alpha=0.5)

    // 绘制区域边界线
    draw_zone_grid(canvas, scale_x, scale_y, center_x, center_y)

    // 标注 Golden Zone
    golden_rect = {
        left:   center_x - 25 * scale_x,
        right:  center_x + 25 * scale_x,
        top:    center_y - 5 * scale_y,
        bottom: center_y + 20 * scale_y
    }
    canvas.draw_rect(golden_rect, stroke_color=GREEN, stroke_width=2)
    canvas.draw_label("Golden Zone", golden_rect.center_top, color=GREEN)

    // 绘制轴标签
    draw_axis_labels(canvas, scale_x, scale_y, center_x, center_y)
```

### 3.3 可拖放元素

```
CLASS DraggableElement:

    PROPERTIES:
        ui_element   : UIElement
        rect         : Rectangle       // 在画布上的当前位置和尺寸
        is_dragging  : BOOL = FALSE
        drag_offset  : Point
        current_validation : ValidationResult = NULL

    METHOD render(canvas):
        // 根据当前验证状态选择边框颜色
        IF current_validation == NULL:
            border_color = WHITE
        ELSE IF current_validation.warnings.is_empty():
            border_color = GREEN
        ELSE IF has_severe_warnings(current_validation):
            border_color = RED
        ELSE:
            border_color = YELLOW

        // 绘制元素矩形
        canvas.draw_filled_rect(rect, fill=SEMI_TRANSPARENT_WHITE, stroke=border_color)

        // 绘制元素名称和类型图标
        canvas.draw_text(ui_element.name, rect.center, color=WHITE, size=12)
        canvas.draw_icon(CONTENT_TYPE_ICONS[ui_element.content_type], rect.top_left)

        // 绘制舒适度小徽章
        IF current_validation != NULL:
            comfort = current_validation.comfort
            badge_text = COMFORT_LABELS[comfort]
            badge_color = COMFORT_COLOR_MAP[comfort]
            canvas.draw_badge(badge_text, rect.bottom_right, color=badge_color)

    METHOD on_drag_start(mouse_pos : Point):
        is_dragging = TRUE
        drag_offset = mouse_pos - rect.top_left

    METHOD on_drag_move(mouse_pos : Point, canvas, posture):
        IF NOT is_dragging: RETURN

        // 更新元素位置
        new_pos = mouse_pos - drag_offset
        rect.move_to(new_pos)

        // 将画布坐标转换为角度坐标
        h_angle = pixel_to_h_angle(rect.center.x, canvas)
        v_angle = pixel_to_v_angle(rect.center.y, canvas)
        ui_element.h_angle = h_angle
        ui_element.v_angle = v_angle

        // 实时验证
        current_validation = validate_element(ui_element, posture)

        // 检查是否接近区域边界 → 显示吸附引导线
        snap_lines = check_snap_to_zone_boundaries(h_angle, v_angle)
        IF snap_lines.is_not_empty():
            canvas.draw_snap_guides(snap_lines)

        // 显示实时信息
        show_realtime_tooltip(h_angle, v_angle, current_validation)

    METHOD on_drag_end():
        is_dragging = FALSE
        // 触发完整布局重新验证
        EMIT "layout_changed"
```

### 3.4 吸附与引导

```
FUNCTION check_snap_to_zone_boundaries(h_angle, v_angle) -> LIST<SnapLine>:

    snap_lines = []
    SNAP_THRESHOLD = 3.0    // 距离边界 3° 以内时触发吸附提示

    // 水平区域边界
    h_boundaries = [10, 25, 45, 70, 100]
    FOR boundary IN h_boundaries:
        IF ABS(ABS(h_angle) - boundary) < SNAP_THRESHOLD:
            snap_lines.ADD(SnapLine {
                type: "vertical",
                angle: boundary * SIGN(h_angle),
                label: "H区域边界 ±{boundary}°"
            })

    // 垂直区域边界
    v_up_boundaries = [5, 15, 25]
    v_down_boundaries = [5, 20, 35]
    boundaries = v_angle >= 0 ? v_up_boundaries : v_down_boundaries
    FOR boundary IN boundaries:
        IF ABS(ABS(v_angle) - boundary) < SNAP_THRESHOLD:
            snap_lines.ADD(SnapLine {
                type: "horizontal",
                angle: boundary * SIGN(v_angle),
                label: "V区域边界"
            })

    RETURN snap_lines
```

### 3.5 布局评分仪表盘

```
CLASS LayoutScoreDashboard:

    PROPERTIES:
        elements     : LIST<DraggableElement>
        posture      : Posture
        last_report  : LayoutReport = NULL

    METHOD update():
        ui_elements = elements.MAP(e -> e.ui_element)
        last_report = validate_layout(ui_elements, posture)
        render()

    METHOD render():
        // 总分环形图
        draw_score_ring(last_report.score)

        // 分项得分
        draw_category_bars({
            "区域合理性":   calculate_zone_sub_score(last_report),
            "内容匹配度":   calculate_content_sub_score(last_report),
            "密度分布":     calculate_density_sub_score(last_report),
            "姿态兼容性":   calculate_posture_sub_score(last_report),
        })

        // 警告列表
        FOR warning IN last_report.layout_warnings:
            draw_warning_item(warning)

        // 元素逐项状态
        FOR result IN last_report.element_results:
            draw_element_status(result.element.name, result.comfort, result.warnings)
```

### 3.6 一键优化建议

```
FUNCTION auto_optimize_layout(elements : LIST<UIElement>, posture : Posture) -> LIST<PositionSuggestion>:

    suggestions = []

    // Phase 1: 将每个元素移至其内容类型的推荐区域中心
    initial_positions = []
    FOR element IN elements:
        rule = FIND rule IN PLACEMENT_RULES WHERE rule.content_type == element.content_type
        initial_positions.ADD({
            element: element,
            h: recommended_center_h(rule),
            v: recommended_center_v(rule)
        })

    // Phase 2: 解决重叠——使用简单的排斥算法
    resolved = resolve_overlaps(initial_positions)

    // Phase 3: 保持相对空间关系
    // 如果原始布局中 A 在 B 的左边，优化后也应保持
    final_positions = preserve_spatial_relations(elements, resolved)

    // Phase 4: 生成建议
    FOR i IN 0..elements.length:
        IF position_changed(elements[i], final_positions[i]):
            suggestions.ADD(PositionSuggestion {
                element:     elements[i],
                original_h:  elements[i].h_angle,
                original_v:  elements[i].v_angle,
                suggested_h: final_positions[i].h,
                suggested_v: final_positions[i].v,
                reason:      generate_reason(elements[i], final_positions[i])
            })

    RETURN suggestions

FUNCTION resolve_overlaps(positions : LIST<Position>) -> LIST<Position>:

    MAX_ITERATIONS = 50
    REPULSION_STEP = 2.0    // 每次迭代的排斥移动量（度）

    FOR iteration IN 0..MAX_ITERATIONS:
        has_overlap = FALSE

        FOR i IN 0..positions.length:
            FOR j IN (i+1)..positions.length:
                IF rects_overlap(positions[i], positions[j]):
                    has_overlap = TRUE

                    // 计算排斥方向
                    dh = positions[j].h - positions[i].h
                    dv = positions[j].v - positions[i].v
                    dist = SQRT(dh*dh + dv*dv)
                    IF dist < 0.01: dist = 1

                    // 双方各移开一半
                    positions[i].h -= (dh / dist) * REPULSION_STEP / 2
                    positions[i].v -= (dv / dist) * REPULSION_STEP / 2
                    positions[j].h += (dh / dist) * REPULSION_STEP / 2
                    positions[j].v += (dv / dist) * REPULSION_STEP / 2

                    // 将位置限制在推荐区域内（软约束）
                    positions[i] = soft_clamp_to_recommended(positions[i])
                    positions[j] = soft_clamp_to_recommended(positions[j])

        IF NOT has_overlap: BREAK

    RETURN positions
```

### 3.7 导出

```
FUNCTION export_layout_as_json(elements : LIST<UIElement>, report : LayoutReport) -> JSON:
    RETURN {
        "metadata": {
            "guideline_version": "1.0",
            "export_time": NOW(),
            "posture": current_posture
        },
        "layout_score": report.score,
        "elements": elements.MAP(e -> {
            "id": e.id,
            "name": e.name,
            "content_type": e.content_type,
            "position": {
                "h_angle": e.h_angle,
                "v_angle": e.v_angle,
                "angular_width": e.angular_width,
                "angular_height": e.angular_height
            },
            "anchor_type": e.anchor_type,
            "validation": {
                "h_zone": classify_horizontal(ABS(e.h_angle)).id,
                "v_zone": classify_vertical(e.v_angle).id,
                "comfort": composite_comfort(...),
                "warnings": validate_element(e, posture).warnings
            }
        }),
        "layout_warnings": report.layout_warnings
    }
```

---

## Part 4: 应用流程示例

### 4.1 输入验证型 — 典型使用流程

```
// 设计师定义一个 UI 元素
my_menu = UIElement {
    id:              "main_menu",
    name:            "主菜单",
    content_type:    PRIMARY_INTERACTION,
    h_angle:         -15,           // 左侧 15°
    v_angle:         -10,           // 自然视线下方 10°
    angular_width:   20,
    angular_height:  30,
    anchor_type:     BODY_LOCKED,
    interaction_freq: "high",
    dwell_time:      "brief"
}

// 验证
result = validate_element(my_menu, STANDING)

// 输出示例：
// ┌──────────────────────────────────────────┐
// │  元素: 主菜单                              │
// │  水平: H1 核心舒适区 (-15°)               │
// │  垂直: V-1 舒适下视区 (-10°)              │
// │  综合舒适度: ★★★★☆ 舒适                   │
// │  状态: ✅ 在推荐区域内                     │
// │  无警告                                    │
// └──────────────────────────────────────────┘
```

```
// 另一个有问题的元素
side_panel = UIElement {
    id:              "side_tools",
    name:            "工具面板",
    content_type:    PRIMARY_INTERACTION,
    h_angle:         60,            // 右侧 60° — 太远了！
    v_angle:         0,
    angular_width:   15,
    angular_height:  40,
    anchor_type:     BODY_LOCKED,
    interaction_freq: "high",
    dwell_time:      "brief"
}

result = validate_element(side_panel, STANDING)

// 输出示例：
// ┌──────────────────────────────────────────────┐
// │  元素: 工具面板                                │
// │  水平: H3 刻意转头区 (60°)                    │
// │  垂直: V0 自然视线区 (0°)                     │
// │  综合舒适度: ★★☆☆☆ 费力                       │
// │  ⚠️ 警告: 高频交互内容放置在低舒适度区域       │
// │  ⚠️ 警告: 元素超出内容类型的推荐范围           │
// │  💡 建议: 移至水平 ±12.5°, 垂直 -7.5°        │
// │     (推荐区域中心，保持右侧方向)               │
// └──────────────────────────────────────────────┘
```

### 4.2 可视化编排型 — 交互流程

```
SEQUENCE: 设计师使用可视化编排工具

1. 打开编排器
   → 渲染视野地图（舒适度热力图 + 区域网格）
   → 显示空白画布，Golden Zone 高亮标注

2. 添加元素
   → 从左侧面板拖入"主菜单"（类型：主交互面板）
   → 元素默认出现在 Golden Zone 中心
   → 仪表盘显示初始评分

3. 调整位置
   → 设计师拖拽"主菜单"向右移动
   → 跨越 H1→H2 边界时：
      - 边界线高亮闪烁
      - 元素边框从绿色变为黄色
      - 浮动提示："进入自然转视区，舒适度降低为 ★★★☆☆"
   → 松开鼠标，仪表盘评分实时更新

4. 继续添加多个元素
   → 添加"通知面板"、"导航锚点"、"视频播放器"等
   → 每次添加/移动后，重叠检测和密度分析自动运行
   → 仪表盘持续更新

5. 查看优化建议
   → 点击"一键优化"按钮
   → 系统计算每个元素的最佳位置
   → 以虚线箭头标注原位置 → 建议位置
   → 设计师可逐个接受/忽略建议

6. 导出
   → 导出为 JSON 参数表 + 布局截图
   → 参数表包含每个元素的角度坐标、区域判定和验证结果
```

---

## Part 5: 扩展接口预留

### 5.1 与 VAC 深度规范的集成点

```
// 本规范定义了角度维度，VAC 规范定义了深度维度
// 未来可通过以下接口将两者集成

INTERFACE SpatialPlacementValidator:
    METHOD validate_angle(element) -> AngleValidationResult     // 本规范
    METHOD validate_depth(element) -> DepthValidationResult     // VAC 规范
    METHOD validate_combined(element) -> CombinedResult         // 集成验证

    // 集成后的完整位置描述
    STRUCT SpatialPosition:
        h_angle  : FLOAT    // 水平角度（本规范）
        v_angle  : FLOAT    // 垂直角度（本规范）
        depth    : FLOAT    // 深度/距离（VAC 规范）
```

### 5.2 动态姿态适配接口

```
// 如果 XR 系统能检测用户姿态，可动态调整区域参数

INTERFACE PostureAdapter:
    METHOD detect_posture() -> Posture
    METHOD get_gaze_offset() -> FLOAT              // 实时自然视线偏移
    METHOD adjust_zones(posture) -> ZoneConfig      // 动态调整区域阈值
```

### 5.3 多用户差异适配

```
// 不同用户的颈部活动度、视力等存在差异
// 可以通过校准流程获取个性化参数

INTERFACE UserCalibration:
    METHOD calibrate_neck_range() -> NeckRangeProfile
    METHOD calibrate_visual_acuity() -> VisualProfile
    METHOD generate_personalized_zones(profile) -> ZoneConfig
```
