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

当前 328 条公开来源具有 2026-06-26、389 条私有快照的历史谱系。该谱系不形成实时
依赖或同步契约。后续私有记录必须逐条审查并在本仓准入后才会出现。

## 私有输入边界

`research-bookmarks` 独立管理私有书签真值，可以提交明确审查过的公开安全候选。
本仓自行完成准入与验证；禁止镜像原始私有数据，也不会仅凭路径关系继承私仓权威。

## 本仓提供什么

- `data/public-sources.json`：经过审查的公开官方或规范来源。
- `data/taxonomy.json`：宽域公开资源 taxonomy。
- `exports/research-engineering-bookmarks-public.html`：确定性 Netscape 书签产物。
- `data/projection-report.json`：派生聚合与边界证据。
- 本地验证和用户流程模拟。

## 验证方式

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

公开产物只能包含经过审查的公开安全官方或规范来源。禁止原始浏览器导出、私有目录
结构、本地 URL、账号或 session 数据、个人偏好、低信任兜底和疑似凭据内容。
