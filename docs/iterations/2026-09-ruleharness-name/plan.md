---
iteration: 2026-09-ruleharness-name
status: complete
---

# RuleHarness 项目命名

## 目标

采用展示名 `RuleHarness`、仓库名 `rule-harness`，以简短且不绑定客户端的名称
表达指令管理、上下文路由与验证能力，为后续其他 agent 的适配保留空间。

## 范围

- 更新 README、bootstrap 标题、live design 和维护文档标题。
- 明确当前首先面向 Codex，其他客户端须完成适配和验证后才能声明支持。
- 将 core/overlay 作为仓库角色表达，保持既有路由协议和权限边界。
- 同步托管仓库名称与本 checkout 的 origin 地址。

本轮不实现新客户端适配，不修改路由 expected values、角色 schema 或历史迭代记录。

## 验收

- 当前文档使用新名称，旧名称仅在命名变更记录中出现。
- 结构校验和现有 10 个路由回归用例通过。
- 完成 diff 与 allowlist 审查，以一个原子提交保存文档变更。
- 验证托管仓库新名称及 origin 地址；无法完成时明确记录外部阻塞。
