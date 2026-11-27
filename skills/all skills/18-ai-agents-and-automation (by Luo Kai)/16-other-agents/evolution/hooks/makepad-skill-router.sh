#!/bin/bash
# Makepad Skills Router - UserPromptSubmit Hook
#
# Analyzes user input and routes to appropriate skill
# Output goes to stderr so Claude can see it
#
# Usage: Called by Claude Code UserPromptSubmit hook
# Input: User's prompt via stdin (JSON format)

set -e

# Read user input from stdin
read -r USER_INPUT 2>/dev/null || USER_INPUT=""

# Extract the actual prompt text from JSON if present
# UserPromptSubmit provides: {"prompt": "user text here"}
if echo "$USER_INPUT" | grep -q '"prompt"'; then
    PROMPT=$(echo "$USER_INPUT" | sed 's/.*"prompt"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
else
    PROMPT="$USER_INPUT"
fi

# Convert to lowercase for matching
PROMPT_LOWER=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]')

# Track matched skills
MATCHED_SKILLS=""

# ============================================================================
# Makepad Core Skills
# ============================================================================

# makepad-basics: Getting started, app structure
if echo "$PROMPT_LOWER" | grep -qE 'live_design!|app_main!|getting started|how to create|makepad app|入门|教程|hello world|appmaintf|appmaini|基础|创建.*应用'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-basics"
fi

# makepad-dsl: DSL syntax, inheritance
if echo "$PROMPT_LOWER" | grep -qE 'dsl|inheritance|prototype|<widget>|<view>|<button>|foo = \{|bar = \{|live.*syntax|继承|原型|dsl.*语法|如何定义.*组件'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-dsl"
fi

# makepad-layout: Layout system
if echo "$PROMPT_LOWER" | grep -qE 'layout|flow|walk|size|padding|margin|width|height|center|align|fit|fill|spacing|布局|居中|宽度|高度|对齐|间距'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-layout"
fi

# makepad-widgets: Widget components
if echo "$PROMPT_LOWER" | grep -qE '\bview\b|\bbutton\b|\blabel\b|\bimage\b|textinput|scrollview|roundedview|solidview|widget|\bmarkdown\b|\bhtml\b|textflow|rich.*text|富文本|markdown.*渲染|link.*click|链接.*点击|code.*block|代码块|组件|按钮|标签|视图|输入框|图片|列表'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-widgets"
fi

# makepad-event-action: Event handling
if echo "$PROMPT_LOWER" | grep -qE '\bevent\b|\baction\b|\bhit\b|fingerdown|fingerup|keydown|keyup|mousedown|handle_event|touchupdate|click|tap|事件|点击|触摸|键盘'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-event-action"
fi

# makepad-animation: Animation system
if echo "$PROMPT_LOWER" | grep -qE 'animat|state.*transition|hover.*effect|pressed.*state|animator|from:.*\{|play:.*\{|ease|动画|状态|过渡|悬停|按下'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-animation"
fi

# makepad-shaders: Shader and visual effects
if echo "$PROMPT_LOWER" | grep -qE 'shader|draw_bg|sdf2d|sdf\.|pixel|glsl|gradient|glow|shadow|visual.*effect|着色器|渐变|阴影|光效|绘制'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-shaders"
fi

# makepad-platform: Cross-platform support
if echo "$PROMPT_LOWER" | grep -qE 'platform|macos|windows|linux|android|ios|wasm|web|mobile|desktop|cross.*platform|跨平台|移动端|桌面端'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-platform"
fi

# makepad-font: Font and typography
if echo "$PROMPT_LOWER" | grep -qE 'font|text.*style|glyph|typography|font.*size|font.*family|text.*layout|字体|文字|排版|字号'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-font"
fi

# makepad-splash: Splash scripting language
if echo "$PROMPT_LOWER" | grep -qE 'splash|script!|cx\.eval|makepad.*script|dynamic.*ui|脚本|动态'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-splash"
fi

# ============================================================================
# Robius Pattern Skills
# ============================================================================

# robius-app-architecture: Async/Tokio integration
if echo "$PROMPT_LOWER" | grep -qE 'tokio|async.*runtime|submit_async|spawn_blocking|异步|运行时|架构'; then
    MATCHED_SKILLS="$MATCHED_SKILLS robius-app-architecture"
fi

# robius-widget-patterns: Reusable widget patterns
if echo "$PROMPT_LOWER" | grep -qE 'apply_over|textorimage|reusable.*widget|widget.*pattern|modal|overlay|collapsible|drag.*drop|可复用|模态|折叠|pageflip|page.*flip|切换.*慢|switch.*slow|cache.*view|即刻.*销毁|即刻.*缓存|incremental.*load|增量.*加载|组件.*多|deep.*tree|组件树'; then
    MATCHED_SKILLS="$MATCHED_SKILLS robius-widget-patterns"
fi

# robius-event-action: Custom actions
if echo "$PROMPT_LOWER" | grep -qE 'custom.*action|matchevent|cx\.widget_action|post_action|自定义.*action'; then
    MATCHED_SKILLS="$MATCHED_SKILLS robius-event-action"
fi

# robius-state-management: State and persistence
if echo "$PROMPT_LOWER" | grep -qE 'appstate|persistence|scope::with_data|save.*state|load.*state|theme.*switch|状态管理|持久化|主题切换'; then
    MATCHED_SKILLS="$MATCHED_SKILLS robius-state-management"
fi

# robius-matrix-integration: Matrix SDK
if echo "$PROMPT_LOWER" | grep -qE 'matrix.*sdk|sliding.*sync|timeline|matrixrequest|matrix.*client|robrix'; then
    MATCHED_SKILLS="$MATCHED_SKILLS robius-matrix-integration"
fi

# ============================================================================
# MolyKit Skill
# ============================================================================

if echo "$PROMPT_LOWER" | grep -qE 'botclient|openai|llm|sse.*stream|ai.*chat|moly|chat.*widget|ai.*integration|platformsend|threadtoken'; then
    MATCHED_SKILLS="$MATCHED_SKILLS molykit"
fi

# ============================================================================
# Extended Skills
# ============================================================================

# makepad-deployment: Build and packaging
if echo "$PROMPT_LOWER" | grep -qE 'deploy|package|apk|ipa|cargo.*makepad|build.*android|build.*ios|build.*wasm|发布|打包|部署'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-deployment"
fi

# makepad-reference: Troubleshooting and API
if echo "$PROMPT_LOWER" | grep -qE 'troubleshoot|error.*fix|debug|api.*doc|reference|problem|issue|故障|错误|调试|文档'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-reference"
fi

# evolution: Self-improvement and contribution
if echo "$PROMPT_LOWER" | grep -qE 'evolut|contribut|hooks|template|self.*improv|贡献|演进'; then
    MATCHED_SKILLS="$MATCHED_SKILLS evolution"
fi

# ============================================================================
# App Development Context Detection (loads skill bundles)
# ============================================================================

# Full app development - load essential skills bundle
if echo "$PROMPT_LOWER" | grep -qE 'build.*app|create.*app|develop.*app|new.*project|从零|从头|完整.*应用|开发.*应用|构建.*应用|app.*architecture|应用架构|full.*stack|全栈'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-basics makepad-dsl makepad-layout makepad-widgets makepad-event-action robius-app-architecture"
fi

# UI development context - load UI skill bundle
if echo "$PROMPT_LOWER" | grep -qE 'ui.*design|界面设计|ui.*开发|design.*ui|build.*ui|create.*interface|设计界面|用户界面'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-dsl makepad-layout makepad-widgets makepad-animation makepad-shaders"
fi

# Widget/Component creation context - load component development bundle
if echo "$PROMPT_LOWER" | grep -qE 'create.*widget|create.*component|build.*widget|build.*component|custom.*widget|custom.*component|创建.*组件|开发.*组件|组件.*开发|自定义.*组件|写.*组件|实现.*组件|new.*widget|design.*widget|设计.*组件|做.*组件|component.*dev|widget.*dev'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-widgets makepad-dsl makepad-layout makepad-animation makepad-shaders makepad-font makepad-event-action robius-widget-patterns"
fi

# Production app context - load production patterns
if echo "$PROMPT_LOWER" | grep -qE 'production|生产|robrix.*pattern|moly.*pattern|real.*world|实际项目|最佳实践|best.*practice'; then
    MATCHED_SKILLS="$MATCHED_SKILLS robius-app-architecture robius-widget-patterns robius-state-management robius-event-action"
fi

# ============================================================================
# Skill Dependencies (auto-load related skills)
# ============================================================================

# robius-app-architecture implies basic app structure
if echo "$MATCHED_SKILLS" | grep -q 'robius-app-architecture'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-basics makepad-event-action"
fi

# robius-widget-patterns implies widget knowledge
if echo "$MATCHED_SKILLS" | grep -q 'robius-widget-patterns'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-widgets makepad-layout"
fi

# Animation often needs shaders for effects
if echo "$MATCHED_SKILLS" | grep -q 'makepad-animation'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-shaders"
fi

# Custom actions need event handling knowledge
if echo "$MATCHED_SKILLS" | grep -q 'robius-event-action'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-event-action"
fi

# Widgets often need layout and DSL
if echo "$MATCHED_SKILLS" | grep -q 'makepad-widgets'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-layout makepad-dsl"
fi

# Font styling often relates to widgets
if echo "$MATCHED_SKILLS" | grep -q 'makepad-font'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-widgets"
fi

# Shaders need to know about draw_bg in widgets
if echo "$MATCHED_SKILLS" | grep -q 'makepad-shaders'; then
    MATCHED_SKILLS="$MATCHED_SKILLS makepad-widgets"
fi

# ============================================================================
# Output routing instructions (limited to max 4 skills)
# ============================================================================

# Remove leading space and deduplicate
MATCHED_SKILLS=$(echo "$MATCHED_SKILLS" | xargs | tr ' ' '\n' | sort -u | tr '\n' ' ' | xargs)

# Context-aware priority order
# Detect which context was triggered and adjust priority accordingly
if echo "$MATCHED_SKILLS" | grep -qE 'robius-app-architecture|robius-state-management'; then
    # Production/Architecture context: prioritize robius patterns
    PRIORITY_ORDER="robius-app-architecture robius-widget-patterns robius-state-management makepad-widgets makepad-event-action makepad-layout makepad-dsl robius-event-action makepad-basics makepad-animation makepad-shaders makepad-font makepad-platform makepad-deployment molykit robius-matrix-integration makepad-reference makepad-splash evolution"
elif echo "$MATCHED_SKILLS" | grep -qE 'makepad-animation|makepad-shaders'; then
    # Visual/Animation context: prioritize graphics skills
    PRIORITY_ORDER="makepad-animation makepad-shaders makepad-widgets makepad-layout makepad-dsl makepad-event-action robius-widget-patterns makepad-font makepad-basics robius-app-architecture makepad-platform makepad-deployment molykit robius-state-management robius-event-action robius-matrix-integration makepad-reference makepad-splash evolution"
else
    # Default: widget development context
    PRIORITY_ORDER="makepad-widgets makepad-layout makepad-dsl makepad-event-action robius-widget-patterns makepad-animation makepad-shaders makepad-font robius-app-architecture makepad-basics robius-state-management robius-event-action makepad-platform makepad-deployment molykit robius-matrix-integration makepad-reference makepad-splash evolution"
fi

MAX_SKILLS=4

# Filter and prioritize skills
PRIORITIZED_SKILLS=""
SKILL_COUNT=0
for skill in $PRIORITY_ORDER; do
    if echo "$MATCHED_SKILLS" | grep -qw "$skill"; then
        if [ $SKILL_COUNT -lt $MAX_SKILLS ]; then
            PRIORITIZED_SKILLS="$PRIORITIZED_SKILLS $skill"
            SKILL_COUNT=$((SKILL_COUNT + 1))
        fi
    fi
done
PRIORITIZED_SKILLS=$(echo "$PRIORITIZED_SKILLS" | xargs)

# Count original matches for info
ORIGINAL_COUNT=$(echo "$MATCHED_SKILLS" | wc -w | xargs)

if [ -n "$PRIORITIZED_SKILLS" ]; then
    # Build skill loading instructions
    SKILL_LIST=""
    for skill in $PRIORITIZED_SKILLS; do
        SKILL_LIST="${SKILL_LIST}Skill(${skill}), "
    done
    SKILL_LIST=$(echo "$SKILL_LIST" | sed 's/, $//')

    # Output JSON with systemMessage for Claude
    # This message will be injected into Claude's context
    cat << EOF
{
  "continue": true,
  "systemMessage": "[makepad-skills] IMPORTANT: Before responding, you MUST call these skills: ${SKILL_LIST}. These skills contain essential Makepad patterns and APIs. Load them using the Skill tool, then answer the user's question."
}
EOF
fi
