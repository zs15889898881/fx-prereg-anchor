# SEED_A v3.6 B-free preregistration packet

这是待独立审计、未发布的离线准备包。v3.6承接已发布v3.5，只把B置为`NOT_REQUIRED`：不设B gate、不计算B、不产生B invalid阻塞，也不把B显示为PASS。活跃结论仅由Gate E与固定12 cell的A主pDelta Holm(.05)决定。未来若恢复B，必须证明增量价值并新版本/新验证。

## 文件白名单

仅以下三项可作为未来公开发布候选：本anchor、此README、`reproduce_v3_6_canonical.py`。本地状态文书、回执和合成细节不在包内，不默认外传。

## 绑定

- record: `FX_LOCAL/controller/25_SEED_A预注册记录_v3_6_20260920.json`
- record bytes: 23551
- record SHA-256: `45957d96fa074b5fc7364ae8e17def9a5b5435d6ef35951f251e70adf7fa3d69`
- canonical payload SHA-256 (whole payload, including the inactive historical v3.5 B reference): `470bd5507046e19c885af6a3111771ba8a2dbcc3712c5e03dc17535fce790cd6`
- parent v3.5 record SHA-256: `8773aa46e86992da6d19a68877844d2601bb81b21712da07ca371b10385b8394`
- parent v3.5 canonical SHA-256: `19fbb3f43a842584547d6ff5495461a16e17b202ce6e8b2460c5b5a7fc846542`
- status: `PREPARED_NOT_PUBLISHED`; engineering paused; real read/trial not authorized

## 继承与唯一变更

close-to-close/PIT/same-week matching/ATR/support、四周calendar MBB/R9999/V9500/seed、Holm 12-cell主p、Gate E成本/频率/压力、Seen/固定12/terminal/family/缺p按p=1等均继承。B的历史完整定义保留在record的`canonical_payload.inactive_references.v3_5_rule_set`，不能进入v3.6 active计算或证明。

主张严格限于固定开发窗、PIT/matching、成本、MBB依赖假设和Holm下的matched predictive increment evidence；不代表机制、因果、实盘盈利或交易许可。
