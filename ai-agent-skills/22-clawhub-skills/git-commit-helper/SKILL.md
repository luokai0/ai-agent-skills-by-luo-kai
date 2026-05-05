# Git Commit Helper Skill

🎯 智能生成 Git commit message，遵循 Conventional Commits 规范，提升代码质量和团队协作效率。

## 功能特性

### 核心功能
- **自动生成 commit message** - 根据代码变更智能生成
- **Conventional Commits 规范** - 遵循业界最佳实践
- **多语言支持** - 中文/英文 commit message
- **代码变更分析** - 理解修改意图
- **PR 描述生成** - 一键生成 Pull Request 描述

### 高级功能
- **Breaking Change 检测** - 自动识别破坏性变更
- **关联 Issue** - 自动关联 GitHub Issues
- **Commit 分类** - 按类型/模块分组
- **历史学习** - 学习团队 commit 风格

## 使用方式

### 基础使用
```
帮我生成这次提交的 commit message
```

### 分析变更
```
分析这个代码变更，生成 commit message
```

### 指定类型
```
这是一个新功能，生成 commit message
```

### 多语言
```
用中文生成 commit message
```

### PR 描述
```
为这次变更生成 PR 描述
```

## 输出格式

### 简短版本
```
📝 Commit Message

feat: add user login feature
```

### 详细版本
```
📝 Commit Message

feat(auth): add user login feature

- Add login page with email/password form
- Implement JWT authentication
- Add login API endpoint
- Add form validation
- Add loading state and error handling

Closes #123
```

### PR 描述
```
## 📝 Pull Request

### 变更概述
添加用户登录功能

### 变更内容
- ✅ 登录页面（邮箱/密码表单）
- ✅ JWT 认证实现
- ✅ 登录 API 端点
- ✅ 表单验证
- ✅ 加载状态和错误处理

### 测试计划
- [ ] 测试正常登录流程
- [ ] 测试错误处理
- [ ] 测试表单验证

### 相关 Issue
Closes #123
```

## Commit 类型说明

| 类型 | 说明 | 示例 |
|------|------|------|
| feat | 新功能 | feat: add user login |
| fix | 修复 bug | fix: correct login validation |
| docs | 文档更新 | docs: update README |
| style | 代码格式（不影响逻辑） | style: format code |
| refactor | 重构（不是新功能也不是修复） | refactor: simplify login logic |
| perf | 性能优化 | perf: improve query speed |
| test | 测试相关 | test: add login tests |
| build | 构建系统 | build: update webpack config |
| ci | CI 配置 | ci: add github actions |
| chore | 其他修改 | chore: update dependencies |
| revert | 回滚 | revert: revert login feature |

## 最佳实践

### Commit Message 规范
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 示例
```
feat(auth): add user login feature

- Add login page with email/password form
- Implement JWT authentication
- Add login API endpoint

Closes #123
Breaking change: Session API changed
```

### 建议
- 保持 subject 在 50 字符以内
- 使用动词开头（add, fix, update, remove）
- body 说明"做了什么"和"为什么"
- 关联相关 Issue

## 使用场景

1. **日常提交** - 快速生成规范 commit
2. **团队协作** - 统一 commit 风格
3. **Code Review** - 清晰描述变更内容
4. **版本发布** - 自动生成 CHANGELOG
5. **项目文档** - 保持提交历史可读

---

创建时间：2026-03-11
作者：ClawMart
版本：1.0.0