# research-bookmarks-public

[English](README.md) | 简体中文

公开安全的书签目录、来源分类和可导入浏览器的 HTML 投影，用于研究、工程、知识工作与资源发现。

说明：`public` 描述的是内容边界。仓库在 staging 阶段可以暂时保持 private，但内容按 public-safe 标准维护，以便未来公开时不暴露私有书签数据。

## 仓库职责

本仓库负责公开安全的书签投影，提供：

- 可复用分类；
- 结构化公开来源目录；
- 可导入浏览器的书签 HTML 确定性生成；
- 面向公开产物的验证和用户流程模拟。

它不是用户私有浏览器书签的完整导出。

## 本仓库提供什么

- `data/taxonomy.json`：与 resource-radar domain model 对齐的宽域资源分类。
- `data/public-sources.json`：经过审查的 public-safe 官方或权威来源。
- `exports/research-engineering-bookmarks-public.html`：可直接导入浏览器的生成书签 HTML。
- `scripts/build_public_bookmarks.py`：结构化来源到 HTML 的确定性导出器。
- `scripts/simulate_user_flow.py`：面向用户导入与安全边界的模拟验证。
- 公开/私有边界、来源策略、设计依据和同步模型文档。

## 本仓库不负责什么

- 完整个人浏览器书签。
- 浏览历史、私有文件夹、私人笔记、账号状态或主观偏好。
- 原始私有书签导入；这些属于 `research-bookmarks`。
- 发现、评分、生命周期分析、摘要或宽域自动化；这些属于 `resource-radar`。
- Agent Skill 准入审批；这属于 curated Skills 仓。

## 与配对仓库的关系

```text
research-bookmarks
  -> 完整导入、私有 overlay、审计与脱敏输入的私有真源

research-bookmarks-public
  -> public-safe 分类、结构化官方/权威来源、确定性 HTML 导出

resource-radar
  -> 发现、归一、评分、生命周期、摘要和更宽的投影

open-resource-governance
  -> 公开治理中枢与发布/宣传/ready 证据
```

不要盲目双向同步。私有到公开必须经过过滤、审查，并通过本仓导出器重新生成。

## 设计依据

这套设计遵循四个约束：

1. 用户需要真实可导入的书签产物，而不只是抽象规则。
2. HTML 是有用输出，但结构化数据必须是源头。
3. 公开投影不得泄漏本地服务、账号/session URL、私有偏好或低信任兜底资源。
4. `resource-radar` 可以承担发现和生命周期自动化，但本仓仍是公开书签投影 lane。

详见 [docs/design-basis.md](docs/design-basis.md)。

## 目录结构

```text
data/taxonomy.json                         公开资源分类
data/public-sources.json                   public-safe 官方/权威来源目录
docs/design-basis.md                       仓库存在原因与拆分依据
docs/automation-validation.md              验证与用户流程模拟契约
docs/public-private-boundary.md            公开/私有书签边界
docs/private-public-sync-model.md          安全提升与同步模型
docs/source-policy.md                      来源准入策略
exports/research-engineering-bookmarks-public.html
                                            生成的可导入浏览器书签 HTML
scripts/build_public_bookmarks.py          确定性导出器
scripts/simulate_user_flow.py              用户流程模拟
scripts/verify.py                          结构、安全与确定性检查
```

## 验证方式

重新生成：

```bash
python -B scripts/build_public_bookmarks.py
```

验证：

```bash
python -B scripts/verify.py
python -B scripts/simulate_user_flow.py
```

GitHub Actions 会在 pull request 和推送到 `main` 时运行验证。

## 更新规则

1. 修改 `data/public-sources.json`，不要手写生成 HTML。
2. 重新生成 `exports/research-engineering-bookmarks-public.html`。
3. 运行验证和用户流程模拟。
4. 完整私有书签保留在 `research-bookmarks`。
5. 更广义的发现、评分、生命周期和未来自动补充交给 `resource-radar`。

## 安全边界

本仓按 public-safe 公开投影设计。任何会暴露个人偏好、私有上下文、非官方背书、本地服务状态、账号/session 数据或低信任兜底行为的书签，都应保留在 `research-bookmarks` 或私有审查队列。
