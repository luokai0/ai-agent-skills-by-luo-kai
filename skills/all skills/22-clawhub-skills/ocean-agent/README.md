# 🌊 Ocean Agent — 保险代理人的 AI 工作台

**每天早上打开，三件事一目了然：今天聊谁、聊什么、怎么约见面。**

[![npm](https://img.shields.io/npm/v/oceanbus)](https://www.npmjs.com/package/oceanbus)
[![ClawHub](https://img.shields.io/badge/ClawHub-ocean--agent-blue)](https://clawhub.ai/skills/ocean-agent)
[![downloads](https://img.shields.io/npm/dm/oceanbus)](https://www.npmjs.com/package/oceanbus)
[![license](https://img.shields.io/badge/license-MIT--0-green)](LICENSE)

---

## 它解决什么

一个保险代理人每天最焦虑的三个问题：

| 焦虑 | 没有 Ocean Agent 时 | 有了之后 |
|------|-------------------|---------|
| **今天找谁聊？** | 翻微信、翻通讯录、凭感觉挑人 | 每天早上自动生成**今日行动清单**，按紧迫度排序 |
| **聊什么？** | 翻聊天记录回忆上下文，想措辞 | 每个客户附**上下文回顾 + 消息草稿**，说"发"就行 |
| **怎么约见面？** | 不敢提、不知道约哪、约了怕被拒 | **一键发起会面协商**，Agent 自动谈地点，成了给你准备面谈清单 |

底下还有两件事：

| | 没有时 | 有了之后 |
|------|--------|---------|
| **客户从哪来？** | 靠朋友圈、靠转介绍，不稳定 | 黄页 24h 在线，新客户搜索保险时能找到你 |
| **客户信我吗？** | 截屏发证书，看起来很 desperate | OceanBus 密码学声誉，客户自己能查到你的信任数据 |

---

## 怎么用

**安装** — 跟你的 AI Agent 说：

> "帮我安装 ocean-agent"

Agent 会处理安装、注册 OceanBus、发布黄页。你只需要回答几个问题（名字、擅长险种、服务区域），两分钟搞定。

**之后每天** — 随时跟 Agent 说：

> "看看今天概览"
> "帮我跟进一下"
> "帮我和XXX约个见面"
> "回顾一下今天"

Agent 根据 SKILL.md 知道每一步该做什么，你不用记命令。

---

## 每天都做什么

| 时间 | 做什么 | 对代理人说 |
|------|--------|----------|
| **早上 8:30** | 打开 Ocean Agent | "帮我看看今天概览" |
| **新客户来的时候** | 实时通知 + 自动首响 | 系统主动推送 |
| **上午/下午** | 按清单跟进 | "帮我看看该跟谁跟进" |
| **聊到可以见面了** | 发起会面协商 | "帮我和XXX约个见面" |
| **晚上** | 回顾一天 | "帮我回顾今天" |

---

## 跟 ocean-chat 的关系

| | ocean-chat | ocean-agent |
|---|---|---|
| 定位 | SDK 能力演示 | 保险代理人日常工作台 |
| 适合谁 | 开发者 | 保险代理人 |
| 界面思路 | CLI 命令逐条执行 | AI Agent 按每日流程主动服务 |

两个 skill 共用 `oceanbus` SDK，数据互相隔离。

---

## 目录结构

```
ocean-agent/
├── SKILL.md              ← AI Agent 行为总纲（产品说明书）
├── README.md             ← 本文件
├── package.json
├── config.example.yaml
├── scripts/
│   ├── profile.js        ← 黄页档案（初始化/publish/心跳）
│   ├── listen.js         ← 实时监听 + 自动首响
│   ├── intake.js         ← 线索管理（查消息/回复/分级/备注）
│   └── reputation.js     ← 声誉查询 & 打标签
├── profiles/SKILL.md     ← 黄页档案 · LLM 行为指南
├── intake/SKILL.md       ← 线索承接 · LLM 行为指南
├── reputation/SKILL.md   ← 声誉积累 · LLM 行为指南
└── followup/SKILL.md     ← 跟进管理 · LLM 行为指南
```

---

## 安全 & 隐私

- 所有消息端到端加密（OceanBus 服务器看不到内容）
- 数据存在本地 `~/.oceanbus-agent/`，不上传第三方
- 对外消息必须经代理人确认才发送（除了首次自动自我介绍）
- 消息 72h 后自动从 OceanBus 网络删除

---

## 依赖

- [OceanBus SDK](https://www.npmjs.com/package/oceanbus) `^0.2.1`
- Node.js

---

## 相关项目

- 核心 SDK：[oceanbus](https://www.npmjs.com/package/oceanbus) — `npm install oceanbus`
- 灯塔 Skill：[Ocean Chat](https://clawhub.ai/skills/ocean-chat) — OceanBus SDK P2P 消息入门示范
- 更多 Skills：[ClawHub OceanBus 集合](https://clawhub.ai/skills?search=oceanbus)

## License

MIT-0
