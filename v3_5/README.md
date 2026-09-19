# SEED_A v3.5 anchor preparation

本目录是待独立核验、未发布的 v3.5 anchor 包。它绑定完整预注册记录的原始字节 hash 与 canonical payload hash；不回填 v3.4 或任何旧原件，也不把准备状态写成已发布。

## 绑定对象

- record：`FX_LOCAL/controller/24_SEED_A预注册记录_v3_5_20260920.json`
- record bytes：17941
- record SHA-256：`8773AA46E86992DA6D19A68877844D2601BB81B21712DA07CA371B10385B8394`
- canonical payload SHA-256：`19fbb3f43a842584547d6ff5495461a16e17b202ce6e8b2460c5b5a7fc846542`
- 正确定义附件：`CORRECT_RECOMMENDED_RULES_DRAFT.md`，9499 bytes，SHA-256 `F5A72DEF06A7B95E63E02EECCF8DD8F5AB22E274F1C02E73BF91887267B0A1CB`

## v3.4 → v3.5

v3.5 完整继承 v3.4 的 12 cell、Gate E/D/B、MBB、Holm、cost、seed、ledger 与状态门；仅合入 close-to-close/UTC 四周尾余/字段映射/B population 与 dependence 的机械定义，以及 Owner 转述确认的两项口径：`event_emitted`/suppression 随 descriptor 整体移动且不重算；原始 PIT/ATR/label/support 不完整 slot 在 B population 前排除并记 reason，变换失配为 attempt invalid。A 仍按原 fixed range 自然 PIT，B 不裁 A。

纸面覆盖例固定为 X(10,3), P(S,C) 原3；Y(2,9), Q(C,S) 原3；交换并重跑 A matcher 后局部值为 -11。该例不是正式门验收。

## 离线复算

1. 读取 record 原始 UTF-8 字节，核对 bytes 与 record SHA-256。
2. 读取 `canonical_payload`，按声明的递归 ordinal key 排序；数组保持顺序；使用声明的 PowerShell `ConvertTo-Json -Compress` 字符串规则和 UTF-8 无 BOM，计算 canonical payload SHA-256。
3. 比较 anchor JSON 中两项 hash。anchor JSON 不引用自身 hash，避免自引用。

状态：`PREPARED_NOT_PUBLISHED`。Owner选择由 Lead 转述登记，message_id/精确时间为 null；工程仍暂停，未授权真实读取、trial、上传、实现、pin 或运行。
