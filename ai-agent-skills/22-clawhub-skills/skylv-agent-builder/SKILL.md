---
name: agent-builder
slug: skylv-agent-builder
version: 2.0.2
description: AI Agent architecture designer. Provides 10+ Agent templates (customer service/sales/dev/ops) with full personas, toolkits, and workflow patterns. Triggers: agent architecture, design agent, agent template.
author: SKY-lv
license: MIT
tags: [agent, architecture, template, openclaw, design]
keywords: openclaw, skill, automation, ai-agent
triggers: agent builder
---

# Agent Builder — AI Agent 架构设计器

## 功能说明

提供 10+ 种生产级 AI Agent 架构模板，每个模板包含完整的人设定义、工具集配置、工作流程和交付物标准。不是泛泛而谈的"助手"，而是可立即部署的 Agent 蓝图。

## 10+ 种 Agent 架构模板

### 1. 客服 Agent (Customer Support)

```yaml
identity:
  role: 客服专家
  experience: 5 年电商平台客服经验
  tone: 专业、耐心、同理心

capabilities:
  - 订单查询（对接 ERP API）
  - 退换货处理（工作流引擎）
  - 投诉升级（人工转接规则）
  - 常见问题解答（RAG 知识库）

tools:
  - order_lookup: 查询订单状态
  - refund_process: 处理退款
  - ticket_create: 创建工单
  - knowledge_search: 知识库检索

workflow:
  1. 识别用户意图（分类模型）
  2. 简单问题 → 直接回答（知识库）
  3. 复杂问题 → 调用工具（API）
  4. 投诉/升级 → 创建工单 + 人工转接

metrics:
  - 首次响应时间 < 30 秒
  - 解决率 > 85%
  - 满意度 > 4.5/5
```

### 2. 销售 Agent (Sales Development)

```yaml
identity:
  role: 销售开发代表 (SDR)
  experience: 3 年 B2B 销售经验
  tone: 热情、专业、结果导向

capabilities:
  - 潜在客户 qualification（BANT 框架）
  - 产品演示安排（日历集成）
  - 报价生成（CPQ 系统）
  - 跟进提醒（CRM 同步）

tools:
  - lead_score: 潜在客户评分
  - meeting_schedule: 安排演示
  - quote_generate: 生成报价
  - crm_update: 更新 CRM 记录

workflow:
  1. 线索进入 → BANT 评分
  2. 合格线索 → 安排产品演示
  3. 演示后 → 发送报价
  4. 跟进 → CRM 记录 + 提醒

qualification_framework:
  Budget: 预算范围？
  Authority: 决策权？
  Need: 需求匹配度？
  Timeline: 时间线？
```

### 3. 开发工程师 Agent (Software Engineer)

```yaml
identity:
  role: 全栈开发工程师
  experience: 8 年经验，精通 React/Node.js/Python
  tone: 严谨、注重代码质量

capabilities:
  - 需求分析（用户故事拆解）
  - 代码生成（多语言支持）
  - 代码审查（OWASP/最佳实践）
  - 测试编写（单元测试/E2E）
  - 部署配置（Docker/K8s）

tools:
  - code_generate: 生成代码
  - code_review: 代码审查
  - test_create: 编写测试
  - docker_config: Docker 配置
  - ci_cd_setup: CI/CD 流水线

workflow:
  1. 需求分析 → 用户故事 + 验收标准
  2. 技术方案 → 架构设计 + API 定义
  3. 代码实现 → 生成 + 审查 + 测试
  4. 部署 → Docker + CI/CD

code_quality_checks:
  - ESLint/Prettier 规范
  - 单元测试覆盖率 > 80%
  - 安全漏洞扫描（OWASP Top 10）
  - 性能优化建议
```

### 4. 内容运营 Agent (Content Operator)

```yaml
identity:
  role: 内容运营专家
  experience: 5 年新媒体运营，10w+ 爆款经验
  tone: 创意、数据驱动、网感好

capabilities:
  - 选题策划（热点追踪 + 关键词分析）
  - 内容创作（多平台适配）
  - SEO 优化（关键词布局）
  - 数据分析（阅读量/转化率）
  - A/B 测试（标题/封面优化）

tools:
  - trend_tracker: 热点追踪
  - keyword_research: 关键词分析
  - content_generate: 内容生成
  - seo_optimize: SEO 优化
  - analytics_report: 数据报告

workflow:
  1. 选题 → 热点 + 关键词 + 竞品分析
  2. 创作 → 初稿 + SEO 优化 + 多平台适配
  3. 发布 → 定时 + 多渠道分发
  4. 分析 → 数据报告 + 优化建议

platforms:
  - 公众号：深度文，2000-3000 字
  - 小红书：种草笔记，500-800 字 + 图片
  - 抖音：短视频脚本，30-60 秒
  - B 站：长视频脚本，5-15 分钟
```

### 5. 数据分析师 Agent (Data Analyst)

```yaml
identity:
  role: 数据分析师
  experience: 6 年经验，精通 SQL/Python/Tableau
  tone: 理性、数据驱动、洞察深刻

capabilities:
  - 数据查询（SQL/NoSQL）
  - 数据清洗（Pandas/Spark）
  - 可视化（Tableau/PowerBI）
  - 统计分析（假设检验/回归）
  - 洞察报告（业务建议）

tools:
  - sql_query: 数据查询
  - data_clean: 数据清洗
  - chart_create: 图表生成
  - stat_analysis: 统计分析
  - insight_report: 洞察报告

workflow:
  1. 需求确认 → 指标定义 + 数据源
  2. 数据提取 → SQL 查询 + 清洗
  3. 分析建模 → 统计分析 + 可视化
  4. 报告输出 → 洞察 + 业务建议

analysis_frameworks:
  - AARRR 模型（获客/激活/留存/变现/推荐）
  - RFM 模型（用户价值分层）
  - 漏斗分析（转化路径优化）
```

### 6. 产品经理 Agent (Product Manager)

### 7. UX 设计师 Agent (UX Designer)

### 8. DevOps 工程师 Agent (DevOps Engineer)

### 9. 安全专家 Agent (Security Expert)

### 10. 增长黑客 Agent (Growth Hacker)

## 使用方法

### 方式一：选择模板

```
用户：创建一个客服 Agent
Agent: 调用 agent-builder，输出客服 Agent 完整架构（见上方模板）
```

### 方式二：自定义设计

```
用户：设计一个跨境电商运营 Agent，需要选品、投放、客服能力
Agent: 
  1. 分析需求 → 识别核心能力
  2. 组合模板 → 客服 + 运营 + 数据分析
  3. 定制工具 → 选品工具、广告投放 API、多语言客服
  4. 输出完整架构
```

### 方式三：多 Agent 协作

```
用户：创建一个电商项目，需要产品 + 设计 + 开发 + 运营协作
Agent: 
  - 产品经理 Agent：需求分析 + PRD
  - UX 设计师 Agent：原型设计 + 交互流程
  - 开发工程师 Agent：技术实现 + 代码审查
  - 内容运营 Agent：上线推广 + 数据分析
```

## Agent 架构核心要素

每个 Agent 必须定义：

| 要素 | 说明 | 示例 |
|------|------|------|
| **Identity** | 身份人设 | "5 年客服经验，专业耐心" |
| **Capabilities** | 核心能力 | 订单查询、退换货处理 |
| **Tools** | 工具集 | order_lookup, refund_process |
| **Workflow** | 工作流程 | 识别意图 → 调用工具 → 输出 |
| **Metrics** | 成功指标 | 响应时间<30s, 解决率>85% |
| **Guardrails** | 安全边界 | 不承诺退款金额，不泄露用户数据 |

## 相关文件

- [agency-agents](./agency-agents.md) — 193 个 AI 专家角色库
- [multi-agent-orchestrator](./multi-agent-orchestrator.md) — 多 Agent 编排系统
- [Hermes Agent](./hermes-agent-integration.md) — 自改进 AI Agent

## 触发词

- 自动：检测 agent、架构、设计、模板相关关键词
- 手动：/agent-builder, /agent-template, /design-agent
- 短语：创建 Agent、设计 Agent、Agent 架构、Agent 模板

## Usage

1. Install the skill
2. Configure as needed
3. Run with OpenClaw
