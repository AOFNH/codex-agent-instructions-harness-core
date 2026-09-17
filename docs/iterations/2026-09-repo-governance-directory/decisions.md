---
iteration: 2026-09-repo-governance-directory
status: current
---

# 决策

## D1：以仓库治理职责命名

采用 `.repo-governance/`。现有文件声明仓库类型、agent 工作模式和 core 修改权限，
属于仓库治理元数据。`.instructions/` 容易被理解为指令正文目录；
`.repo-meta/` 缺少内容边界；`.harness/` 容易与现有 `harness/` 工具目录混淆。

后续可以按实际需求扩展文件归属、上游同步和兼容性声明，但每个新增文件都需要
独立定义 schema、读取方、归属和 allowlist，不预建空文件或放宽整个目录的跟踪规则。
指令正文、测试工具、fixture 和本地运行状态继续遵循既有存放边界。

## D2：保持角色语义，统一迁移路径

`repository-role.yaml` 内容保持不变；入口规则和校验脚本只使用新路径，
不引入旧路径 fallback 或两份角色声明。已有 overlay 升级时须保留自己的
`personal-overlay`、`overlay-maintainer` 和 `none`，审查引用与自动化中的旧路径。

目录重命名不改变路由决策、角色权限或数据结构，因此不调整 catalog、路由
fixture 的 expected values、`schema_version` 或路由 `contract_version`。
这是路径迁移，仍要求下游完成上游影响评估和语义兼容性审查；本次只修改 core。
