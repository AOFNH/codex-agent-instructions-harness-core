---
iteration: 2026-09-ruleharness-name
status: current
---

# 决策

## D1：采用 RuleHarness

将 `Codex Agent Instructions Harness — Core` / `codex-agent-instructions-harness-core`
调整为 `RuleHarness` / `rule-harness`。中文定位为“跨 agent 的指令管理、上下文路由与验证框架”。

借鉴 Ruler、Rulesync 和 OpenSpec 以核心概念命名、在说明中表达客户端支持范围的方式。
保留 Rule 与 Harness，突出规则体系及其验证；客户端名称移到适配说明，
core/overlay 通过 README 和仓库角色声明表达。

## D2：区分扩展方向与已实现支持

当前 bootstrap 和客户端专属说明仍首先面向 Codex。其他客户端需要明确的 adapter
和验证后才可声明支持；更名不代表这些适配已经完成。

继续沿用单一 canonical instruction source 和客户端 adapter 的既有边界。
保留 `CODEX_HOME`、`AGENTS.override.md`、profile 等 Codex 专属说明，
不通过文本替换将客户端特有机制泛化为通用机制。

## D3：更名不改变运行契约

本轮不改变规则适用范围、证据优先级、角色权限或数据结构。
catalog、fixture expected values、`contract_version`、`schema_version` 和既有 release tag
命名保持不变；历史迭代记录保留原有语境。

托管仓库名称与本 checkout 的 origin 同步更新。其他 checkout 或 personal overlay
在后续维护中核对 remote 地址并完成正常的上游影响评估，本轮不修改这些仓库。
