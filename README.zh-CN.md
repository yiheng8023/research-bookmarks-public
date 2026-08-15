# research-bookmarks-public

[English](README.md) | 简体中文

公开安全书签目录与可导入浏览器的 HTML 产物。

## 职责

本仓库独立维护结构化公开来源、公开 taxonomy、确定性浏览器导出器、聚合报告和
可导入浏览器的产物。

## 当前快照

- 335 条公开安全链接、97 个书签目录。
- 最近一次命名、分类、归属和冗余审计见
  [目录审计](docs/catalog-audit-2026-07-17.md)。

## 核心文件

- `data/public-sources.json`：持续维护的公开目录。
- `data/taxonomy.json`：公开 taxonomy。
- `exports/research-engineering-bookmarks-public.html`：可导入浏览器的产物。
- `data/projection-report.json`：生成的计数与边界检查。

## 低频更新

仅在公开目录变化时运行：

```bash
python -B scripts/build_public_bookmarks.py
python -B scripts/build_projection_report.py
python -B scripts/verify.py
python -B scripts/simulate_user_flow.py
```

## 隐私与贡献

`research-bookmarks` 可以提出经过审查的公开安全候选，但由本仓决定是否收录。禁止
提交原始私有书签、目录路径、浏览历史、账号或 session 数据、凭据、私有备注和本地
URL。小范围来源或分类修正可直接使用普通 GitHub Issue 或 Pull Request；本项目不设
正式支持或发布周期。安全与隐私问题按 [SECURITY.md](SECURITY.md) 处理。

## 自愿赞助

赞助完全自愿，用于支持偶尔维护；不购买支持优先级、来源准入、功能、发布或技术影响力。

- 人民币：扫描下方微信支付或支付宝收款码。
- 其他受支持币种：使用
  [PayPal 付款链接](https://www.paypal.com/ncp/payment/LNTF8KXGJXMZY)。

付款前请核对结算页面显示的收款方。

<table>
  <tr>
    <td align="center"><strong>微信支付（人民币）</strong><br><img src="docs/assets/sponsoring/wechat-pay.png" alt="微信支付自愿赞助收款码" width="280"></td>
    <td align="center"><strong>支付宝（人民币）</strong><br><img src="docs/assets/sponsoring/alipay.png" alt="支付宝自愿赞助收款码" width="280"></td>
  </tr>
</table>
