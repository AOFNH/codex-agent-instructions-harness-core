---
iteration: 2026-09-repo-governance-directory
status: complete
---

# 验收记录

## 基线

- `python3 harness/scripts/validate.py --root .`：通过，角色为 core / core-maintainer。
- `python3 harness/scripts/route_regression.py --root .`：10 个抽象路由用例通过。
- 开始前工作区干净。

## 变更后

- [x] 角色声明原样迁移，bootstrap、allowlist、校验入口和脱敏扫描使用新路径。
- [x] 文档说明目录职责、扩展边界及 overlay 角色保留要求。
- [x] 结构校验通过，能够识别新路径下的 core / core-maintainer。
- [x] 10 个路由回归用例通过，expected values 未修改。
- [x] 角色文件迁移前后的 Git blob hash 一致，内容未改变。
- [x] allowlist 仅放行新角色文件，新目录中的其他文件仍默认忽略。
- [x] 旧路径仅出现在迁移说明和本次历史记录中。
- [x] 完整 diff、暂存清单和 `git diff --check` 审查通过；本迭代以一个原子提交保存。
