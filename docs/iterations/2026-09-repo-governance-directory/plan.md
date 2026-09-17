---
iteration: 2026-09-repo-governance-directory
status: complete
---

# 仓库治理目录命名

## 目标

将 `.instructions/` 改为 `.repo-governance/`，使目录名称直接表达仓库身份、
维护角色和权限边界，并为后续治理元数据保留明确的扩展范围。

## 范围

- 迁移 `repository-role.yaml`，同步 bootstrap、Git allowlist 和校验脚本。
- 更新 README、live design 和 personal overlay 升级说明。
- 明确新增治理文件需要单独定义 schema、读取方、归属和 allowlist。

本次不新增治理文件，不改变角色字段、维护权限或引用路由策略。

## 验收

- 结构校验能够从新路径读取 core 角色，脱敏扫描覆盖新目录。
- 现有 10 个路由回归用例保持通过，expected values 不变。
- 旧路径仅出现在迁移说明和本次历史记录中。
- 完成 diff 与 allowlist 审查，并以一个原子提交保存。
