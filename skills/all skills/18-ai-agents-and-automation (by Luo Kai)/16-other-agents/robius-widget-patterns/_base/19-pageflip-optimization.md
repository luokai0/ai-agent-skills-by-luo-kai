---
name: makepad-pageflip-optimization
author: robius
source: moly, robrix
date: 2025-01-20
tags: [pageflip, performance, cache, lifecycle, optimization]
level: advanced
---

# Pattern 19: PageFlip 切换优化

解决 PageFlip 页面切换慢的问题 —— 当页面组件多或组件树深时，所有组件在 visible 时都会走创建生命周期。

## Problem

PageFlip（或类似的页面切换组件）切换慢，原因：
- 页面中组件数量多
- 组件树层级深
- 所有组件在 `visible` 时都要完成创建生命周期
- 用户快速切换时，前一个页面还没加载完

## Solution

两种模式：

| 模式 | 行为 | 适用场景 |
|-----|------|---------|
| **即刻销毁** | 切换时强制销毁未加载完的组件 | 内存敏感，页面不常回切 |
| **即刻缓存** | 暂停加载但不销毁，切回继续 | 频繁切换的页面 |

---

## Pattern 1: 即刻销毁模式 (Immediate Destroy)

通过事件通知父 View 强制销毁未完成加载的子组件。

### 定义 Action

```rust
#[derive(Clone, Debug, DefaultNone)]
pub enum PageSwitchAction {
    None,
    /// 请求销毁当前页面未完成的加载
    RequestDestroy { page_id: LiveId },
    /// 页面切换开始
    SwitchStarted { from: LiveId, to: LiveId },
}
```

### PageFlip 包装器

```rust
#[derive(Live, LiveHook, Widget)]
pub struct ManagedPageFlip {
    #[deref] view: View,
    #[live] page_flip: PageFlip,

    #[rust] current_page: Option<LiveId>,
    #[rust] loading_pages: HashSet<LiveId>,
    #[rust] page_load_state: HashMap<LiveId, PageLoadState>,
}

#[derive(Clone, Default)]
pub struct PageLoadState {
    pub is_loading: bool,
    pub loaded_count: usize,
    pub total_count: usize,
}

impl ManagedPageFlip {
    pub fn switch_to(&mut self, cx: &mut Cx, page_id: LiveId) {
        let old_page = self.current_page;

        // 1. 通知旧页面停止加载
        if let Some(old_id) = old_page {
            if self.loading_pages.contains(&old_id) {
                // 发送销毁请求
                cx.widget_action(
                    self.widget_uid(),
                    &HeapLiveIdPath::default(),
                    PageSwitchAction::RequestDestroy { page_id: old_id }
                );
            }
        }

        // 2. 切换到新页面
        self.current_page = Some(page_id);
        self.page_flip.set_active(cx, page_id);

        // 3. 发送切换事件
        if let Some(from) = old_page {
            cx.widget_action(
                self.widget_uid(),
                &HeapLiveIdPath::default(),
                PageSwitchAction::SwitchStarted { from, to: page_id }
            );
        }

        self.redraw(cx);
    }

    pub fn mark_page_loading(&mut self, page_id: LiveId) {
        self.loading_pages.insert(page_id);
    }

    pub fn mark_page_loaded(&mut self, page_id: LiveId) {
        self.loading_pages.remove(&page_id);
    }
}
```

### 页面组件响应销毁请求

```rust
#[derive(Live, LiveHook, Widget)]
pub struct HeavyPage {
    #[deref] view: View,

    #[rust] is_loading: bool,
    #[rust] loaded_items: Vec<WidgetRef>,
    #[rust] pending_items: VecDeque<ItemData>,
    #[rust] load_batch_size: usize,
}

impl Widget for HeavyPage {
    fn handle_event(&mut self, cx: &mut Cx, event: &Event, scope: &mut Scope) {
        // 处理销毁请求
        if let Event::Actions(actions) = event {
            for action in actions {
                if let Some(PageSwitchAction::RequestDestroy { page_id }) = action.downcast_ref() {
                    if self.is_this_page(*page_id) {
                        self.force_destroy_pending(cx);
                        return;
                    }
                }
            }
        }

        // 正常事件处理...
        self.view.handle_event(cx, event, scope);
    }

    fn draw_walk(&mut self, cx: &mut Cx2d, scope: &mut Scope, walk: Walk) -> DrawStep {
        // 增量加载：每帧只加载一批
        if self.is_loading && !self.pending_items.is_empty() {
            self.load_next_batch(cx);
        }

        self.view.draw_walk(cx, scope, walk)
    }
}

impl HeavyPage {
    fn force_destroy_pending(&mut self, cx: &mut Cx) {
        // 清空待加载队列
        self.pending_items.clear();
        self.is_loading = false;

        // 可选：销毁部分已加载的组件以释放内存
        // self.loaded_items.truncate(MIN_KEEP_COUNT);

        log!("Page loading interrupted, pending items destroyed");
    }

    fn load_next_batch(&mut self, cx: &mut Cx) {
        let batch: Vec<_> = self.pending_items
            .drain(..self.load_batch_size.min(self.pending_items.len()))
            .collect();

        for item_data in batch {
            let widget = self.create_item_widget(cx, &item_data);
            self.loaded_items.push(widget);
        }

        if self.pending_items.is_empty() {
            self.is_loading = false;
            // 通知加载完成
            Cx::post_action(PageSwitchAction::None);  // 或自定义完成事件
        }

        self.redraw(cx);
    }
}
```

---

## Pattern 2: 即刻缓存模式 (Immediate Cache)

暂停加载但保留已加载的组件，切回时继续加载。

### CacheView 定义

```rust
#[derive(Live, LiveHook, Widget)]
pub struct CacheView {
    #[deref] view: View,

    #[rust] is_active: bool,
    #[rust] load_paused: bool,
    #[rust] load_progress: LoadProgress,
}

#[derive(Clone, Default)]
pub struct LoadProgress {
    pub loaded_count: usize,
    pub total_count: usize,
    pub pending_items: VecDeque<ItemData>,
}

impl CacheView {
    /// 暂停加载（切换离开时调用）
    pub fn pause_loading(&mut self) {
        if !self.load_paused {
            self.load_paused = true;
            log!("CacheView: Loading paused at {}/{}",
                self.load_progress.loaded_count,
                self.load_progress.total_count);
        }
    }

    /// 恢复加载（切换回来时调用）
    pub fn resume_loading(&mut self, cx: &mut Cx) {
        if self.load_paused {
            self.load_paused = false;
            log!("CacheView: Resuming loading from {}/{}",
                self.load_progress.loaded_count,
                self.load_progress.total_count);
            self.redraw(cx);  // 触发继续加载
        }
    }

    /// 检查是否还有待加载内容
    pub fn has_pending_load(&self) -> bool {
        !self.load_progress.pending_items.is_empty()
    }
}

impl Widget for CacheView {
    fn draw_walk(&mut self, cx: &mut Cx2d, scope: &mut Scope, walk: Walk) -> DrawStep {
        // 只在激活且未暂停时继续加载
        if self.is_active && !self.load_paused && self.has_pending_load() {
            self.load_next_chunk(cx);
        }

        self.view.draw_walk(cx, scope, walk)
    }
}
```

### 使用 CacheView 的 PageFlip

```rust
#[derive(Live, LiveHook, Widget)]
pub struct CachedPageFlip {
    #[deref] view: View,

    #[rust] pages: HashMap<LiveId, CacheViewRef>,
    #[rust] current_page: Option<LiveId>,
}

impl CachedPageFlip {
    pub fn switch_to(&mut self, cx: &mut Cx, page_id: LiveId) {
        // 1. 暂停当前页面的加载
        if let Some(current) = self.current_page {
            if let Some(page) = self.pages.get_mut(&current) {
                page.pause_loading();
            }
        }

        // 2. 切换页面
        self.current_page = Some(page_id);

        // 3. 恢复新页面的加载（如果之前暂停过）
        if let Some(page) = self.pages.get_mut(&page_id) {
            page.resume_loading(cx);
        }

        self.redraw(cx);
    }
}
```

---

## Pattern 3: 混合模式 (Hybrid)

根据内存压力动态选择销毁或缓存。

```rust
#[derive(Clone, Copy, PartialEq)]
pub enum PageCachePolicy {
    /// 总是缓存（内存充足）
    AlwaysCache,
    /// 总是销毁（内存紧张）
    AlwaysDestroy,
    /// LRU 策略（保留最近 N 个）
    LruCache { max_cached: usize },
}

#[derive(Live, Widget)]
pub struct SmartPageFlip {
    #[deref] view: View,

    #[rust] cache_policy: PageCachePolicy,
    #[rust] page_cache: HashMap<LiveId, CachedPage>,
    #[rust] access_order: VecDeque<LiveId>,
    #[rust] current_page: Option<LiveId>,
}

impl SmartPageFlip {
    pub fn switch_to(&mut self, cx: &mut Cx, page_id: LiveId) {
        let old_page = self.current_page;

        match self.cache_policy {
            PageCachePolicy::AlwaysDestroy => {
                // 销毁旧页面
                if let Some(old_id) = old_page {
                    self.destroy_page(cx, old_id);
                }
            }
            PageCachePolicy::AlwaysCache => {
                // 暂停旧页面
                if let Some(old_id) = old_page {
                    self.pause_page(old_id);
                }
            }
            PageCachePolicy::LruCache { max_cached } => {
                // 暂停旧页面
                if let Some(old_id) = old_page {
                    self.pause_page(old_id);
                }
                // 更新访问顺序
                self.update_access_order(page_id);
                // 淘汰超出限制的页面
                self.evict_if_needed(cx, max_cached);
            }
        }

        self.current_page = Some(page_id);
        self.activate_page(cx, page_id);
        self.redraw(cx);
    }

    fn evict_if_needed(&mut self, cx: &mut Cx, max_cached: usize) {
        while self.page_cache.len() > max_cached {
            if let Some(oldest) = self.access_order.pop_front() {
                self.destroy_page(cx, oldest);
            }
        }
    }
}
```

---

## 增量加载模式

避免一次性创建所有组件，分帧加载。

```rust
const ITEMS_PER_FRAME: usize = 5;

impl HeavyPage {
    fn start_incremental_load(&mut self, items: Vec<ItemData>) {
        self.pending_items = VecDeque::from(items);
        self.is_loading = true;
        self.loaded_items.clear();
    }

    fn load_next_chunk(&mut self, cx: &mut Cx) {
        if self.load_paused || self.pending_items.is_empty() {
            return;
        }

        // 每帧只加载固定数量
        for _ in 0..ITEMS_PER_FRAME {
            if let Some(item_data) = self.pending_items.pop_front() {
                let widget = self.create_item_widget(cx, &item_data);
                self.loaded_items.push(widget);
            } else {
                break;
            }
        }

        // 如果还有待加载，请求下一帧继续
        if !self.pending_items.is_empty() {
            self.redraw(cx);  // 触发下一帧的 draw_walk
        } else {
            self.is_loading = false;
        }
    }
}
```

---

## Makepad 官方 CachedWidget

Makepad 提供了内置的 `CachedWidget`，是一个**全局单例包装器**，用于跨布局共享 widget 实例。

### 源码位置

`makepad-widgets/src/cached_widget.rs`

### 核心实现

```rust
/// A Singleton wrapper widget that caches and reuses its child widget across multiple instances.
#[derive(Live, LiveRegisterWidget, WidgetRef)]
pub struct CachedWidget {
    #[walk] walk: Walk,
    #[rust] template_id: LiveId,
    #[rust] template: Option<LivePtr>,
    #[rust] widget: Option<WidgetRef>,
}

/// 全局缓存存储
#[derive(Default)]
pub struct WidgetWrapperCache {
    map: HashMap<LiveId, WidgetRef>,
}

impl LiveHook for CachedWidget {
    fn after_apply(&mut self, cx: &mut Cx, ...) {
        // 确保全局缓存存在
        if !cx.has_global::<WidgetWrapperCache>() {
            cx.set_global(WidgetWrapperCache::default())
        }

        if self.widget.is_none() {
            // 尝试从全局缓存获取
            if let Some(widget) = cx.get_global::<WidgetWrapperCache>()
                .map.get_mut(&self.template_id)
            {
                self.widget = Some(widget.clone());
            } else {
                // 不存在则创建并缓存
                let widget = WidgetRef::new_from_ptr(cx, self.template);
                cx.get_global::<WidgetWrapperCache>()
                    .map.insert(self.template_id, widget.clone());
                self.widget = Some(widget);
            }
        }
    }
}
```

### DSL 用法

```rust
live_design! {
    <CachedWidget> {
        my_widget = <MyWidget> {}
    }
}
```

### 特点

- **全局单例**：相同 `template_id` 的 widget 只创建一次
- **状态保持**：切换布局时保持 widget 状态
- **透明代理**：自动代理 `handle_event` 和 `draw_walk`

---

## Moly 的 ChatsDeck 实现

Moly 使用**自定义 LRU 缓存** + `CachedWidget` 组合方案。

### 架构

```
ChatScreen
  └── <CachedWidget>           // 跨布局共享
        └── ChatsDeck          // 自定义 LRU 缓存
              └── HashMap<ChatID, ChatViewRef>  // 聊天视图缓存
```

### 核心代码 (moly/src/chat/chats_deck.rs)

```rust
const MAX_CHAT_VIEWS: usize = 10;

#[derive(Live, LiveHook, Widget)]
pub struct ChatsDeck {
    #[deref] view: View,

    /// 所有聊天视图缓存
    #[rust] chat_view_refs: HashMap<ChatID, ChatViewRef>,

    /// LRU 访问顺序
    #[rust] chat_view_accesed_order: VecDeque<ChatID>,

    /// 当前可见的聊天 ID
    #[rust] currently_visible_chat_id: Option<ChatID>,

    /// 聊天视图模板
    #[live] chat_view_template: Option<LivePtr>,
}

impl ChatsDeck {
    pub fn create_or_update_chat_view(&mut self, cx: &mut Cx, chat: &ChatData, ...) {
        // 1. 检查是否已存在
        if let Some(chat_view) = self.chat_view_refs.get_mut(&chat.id) {
            // 更新现有视图
            self.currently_visible_chat_id = Some(chat.id);
        } else {
            // 2. 创建新视图
            let chat_view = WidgetRef::new_from_ptr(cx, self.chat_view_template);
            self.chat_view_refs.insert(chat.id, chat_view.as_chat_view());
            self.currently_visible_chat_id = Some(chat.id);
        }

        // 3. 更新 LRU 访问顺序
        self.chat_view_accesed_order.retain(|id| *id != chat.id);
        self.chat_view_accesed_order.push_back(chat.id);

        // 4. 超出限制时淘汰（但保护正在流式传输的聊天）
        if self.chat_view_accesed_order.len() > MAX_CHAT_VIEWS {
            let oldest_id = self.chat_view_accesed_order.pop_front().unwrap();
            if let Some(chat_view) = self.chat_view_refs.get_mut(&oldest_id) {
                // 🔑 关键：不淘汰正在流式传输的聊天
                if !chat_view.chat(id!(chat)).read().is_streaming() {
                    self.chat_view_refs.remove(&oldest_id);
                }
            }
        }
    }
}
```

### 亮点

- **流式保护**：不淘汰正在接收 AI 响应的聊天
- **懒加载**：只在需要时创建 ChatView
- **状态同步**：通过 `chats_views_pending_sync` 延迟更新上下文

---

## Robrix 的 CachedWidget 使用

Robrix 大量使用 `CachedWidget` 实现 **Desktop/Mobile 布局状态共享**。

### 使用场景

```rust
live_design! {
    pub HomeScreen = {{HomeScreen}} {
        <AdaptiveView> {
            // NOTE: 使用 CachedWidget 包装确保只有一个全局实例
            // 这样在 Desktop 和 Mobile 布局切换时保持状态

            Desktop = <View> {
                <CachedWidget> {
                    navigation_tab_bar = <NavigationTabBar> {}
                }
                <CachedWidget> {
                    rooms_list = <RoomsList> {}
                }
                <CachedWidget> {
                    settings_screen = <SettingsScreen> {}
                }
            }

            Mobile = <View> {
                // 同样的 widget ID，复用同一实例
                <CachedWidget> {
                    navigation_tab_bar = <NavigationTabBar> {}
                }
                <CachedWidget> {
                    rooms_list = <RoomsList> {}
                }
            }
        }
    }
}
```

### 典型包装对象

| Widget | 为什么缓存 |
|--------|----------|
| `NavigationTabBar` | 保持选中状态 |
| `RoomsList` | 保持滚动位置和加载状态 |
| `RoomFilterInputBar` | 保持搜索文本 |
| `SettingsScreen` | 保持设置状态 |
| `SpacesBar` | 保持展开/折叠状态 |

### 注意事项

```rust
// ⚠️ CachedWidget + AdaptiveView 的 DSL 样式覆盖问题
// DSL 级别的样式覆盖可能不生效，需要在代码中手动 apply_over

fn draw_walk(&mut self, cx: &mut Cx2d, ...) {
    // 因为 chats_deck 被缓存，DSL 属性覆盖不会生效
    // 需要通过 apply_over 手动覆盖
    if cx.display_context.is_desktop() {
        self.view.apply_over(cx, live! {
            padding: {top: 18, bottom: 10, right: 28, left: 28}
        });
    } else {
        self.view.apply_over(cx, live! {
            padding: {top: 55, left: 0, right: 0, bottom: 0}
        });
    }
}
```

---

## 对比总结

| 特性 | Makepad CachedWidget | Moly ChatsDeck | 本文档 Pattern |
|------|---------------------|----------------|---------------|
| **目标** | 跨布局状态共享 | 聊天视图 LRU 缓存 | PageFlip 切换优化 |
| **粒度** | Widget 级单例 | 视图级 LRU | 页面级生命周期 |
| **缓存策略** | 永久缓存 | LRU (max=10) | 可配置 |
| **淘汰条件** | 不淘汰 | 非流式传输时淘汰 | 暂停/销毁可选 |
| **适用场景** | Desktop/Mobile 切换 | 多聊天切换 | 深组件树页面切换 |

---

## When to Use

| 场景 | 推荐模式 |
|------|---------|
| 页面组件 100+ | 增量加载 + 即刻销毁 |
| 频繁切换的标签页 | 即刻缓存 |
| 内存敏感的移动端 | LRU 混合模式 |
| 简单页面 (<20 组件) | 无需优化 |

## 性能对比

| 模式 | 首次切换 | 回切 | 内存占用 |
|------|---------|------|---------|
| 无优化 | 慢 | 慢 | 高 |
| 即刻销毁 | 快 | 慢（重建） | 低 |
| 即刻缓存 | 快 | 快（恢复） | 中 |
| LRU 混合 | 快 | 取决于缓存命中 | 可控 |

## References

### Makepad 源码
- `makepad-widgets/src/cached_widget.rs` - CachedWidget 官方实现

### Moly 源码
- `moly/src/chat/chats_deck.rs` - ChatsDeck LRU 缓存实现
- `moly/src/chat/chat_screen.rs` - CachedWidget 使用示例
- `moly/src/chat/chat_screen_mobile.rs` - Mobile 布局 CachedWidget

### Robrix 源码
- `robrix/src/home/home_screen.rs:62-226` - 大量 CachedWidget 使用
- `robrix/src/home/rooms_sidebar.rs` - RoomsList 缓存
- `robrix/src/home/navigation_tab_bar.rs` - 导航栏缓存
- `robrix/src/shared/room_filter_input_bar.rs` - 搜索栏缓存说明

### GitHub
- [Moly](https://github.com/moxin-org/moly) - AI 聊天应用
- [Robrix](https://github.com/project-robius/robrix) - Matrix 客户端
