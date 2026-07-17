# research-bookmarks-public

[English](README.md) | 简体中文

独立的公开安全资源目录与浏览器书签产物仓库。

## 仓库职责

本仓库自行管理结构化公开来源、公开 taxonomy、脱敏策略、确定性导出器、聚合证据和
可导入浏览器的产物。构建、验证和维护当前目录不依赖中央总仓、私有 checkout 或外部发现
服务。

## 真源模型

```text
data/public-sources.json                  公开目录真值
data/taxonomy.json                        公开 taxonomy 真值
          |
          v
scripts/build_public_bookmarks.py
scripts/build_projection_report.py
          |
          v
exports/research-engineering-bookmarks-public.html
data/projection-report.json               派生证据
```

当前 334 条公开来源具有 2026-06-26、389 条私有快照的历史谱系。该谱系不形成实时
依赖或同步契约。后续私有记录必须逐条审查并在本仓准入后才会出现。

## 私有输入边界

`research-bookmarks` 独立管理私有书签真值，可以提交明确审查过的公开安全候选。
本仓自行完成准入与验证；禁止镜像原始私有数据，也不会仅凭路径关系继承私仓权威。

## 本仓提供什么

- `data/public-sources.json`：具有规范主机、产品、入口角色、市场范围、归属状态、
  证据和 URL 健康状态的公开安全来源；未知法律主体明确保持 `needs_review`。
- `data/taxonomy.json`：宽域公开资源 taxonomy。
- `exports/research-engineering-bookmarks-public.html`：确定性 Netscape 书签产物。
- `data/projection-report.json`：派生聚合与边界证据。
- 本地验证和用户流程模拟。

## 验证方式

本轮全量目录修正及仍待补证的主体归属边界记录在
`docs/catalog-audit-2026-07-17.md`。

重新生成：

```bash
python -B scripts/build_public_bookmarks.py
python -B scripts/build_projection_report.py
```

验证：

```bash
python -B scripts/verify.py
python -B scripts/simulate_user_flow.py
```

所有正确性检查均可在本地完成。GitHub Actions 可以作为便利性重复执行，但不是仓库
真值，也不是必需运行时依赖。

## 安全边界

公开产物只能包含具有明确准入依据的公开安全来源；官方/规范来源与经过审查的二手
参考保持不同来源类型。禁止原始浏览器导出、私有目录
结构、本地 URL、账号或 session 数据、个人偏好、低信任兜底和疑似凭据内容。

## 社区与可持续维护

- 提交来源、taxonomy 或工具变更前，请先阅读[贡献说明](CONTRIBUTING.md)。
- 按[支持说明](SUPPORT.zh-CN.md)选择合适的公开渠道，禁止披露私有书签或账号数据。
- 参与社区须遵守[行为准则](CODE_OF_CONDUCT.md)。
- 自愿赞助渠道及边界见[赞助说明](SPONSORING.zh-CN.md)；赞助不购买审查优先级、
  来源准入、发布权限或对目录决策的影响力。
