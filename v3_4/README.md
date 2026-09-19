# SEED_A v3.4 待发布锚包

状态：`PREPARED_NOT_PUBLISHED`。本目录只准备可发布内容；本轮没有联网、上传或创建外部资源。

## 内容与复算

(1) `FX_SEED_A_PREREGISTRATION_RECORD_V3_4_20260919_01.anchor.json` 绑定本地预注册记录的完整文件 bytes/SHA-256、完整 canonical 规则 payload 的 SHA-256、已采纳设计和最终设计复核。

(2) canonical payload 位于 `FX_LOCAL/controller/23_SEED_A预注册记录_v3_4_20260919.json` 的 `canonical_payload`。复算规则严格为：UTF-8；对象键按 ordinal 名称递归排序；数组保持原顺序；字符串按 PowerShell `ConvertTo-Json -Compress` 转义；对象/数组以 `,` 和 `:` 无空白连接；对所得字节 SHA-256。预期值：`a37e9432fa24a88648ab22dbca150a7dcc4b61b12f121f47809c7627deb2509f`。

(3) 预注册记录现行引用：10,017 B / `ebea5d23d609caf51ac89810de818ba56e06be651221ed803ce7f0e6230c27db`。锚外层文件采用 UTF-8/LF 且恰一尾随 LF；其自身 SHA-256 不内嵌，避免自引用。

## 发布和工程边界

发布必须在任何真实读取、结果揭示或 trial 前另行执行；本包不授权发布。后续具体工程仍需单独授权，随后出新 pin、合成验收和独立审计。新实现的 hash/plan hash 只可在那时按锚内的 `code_binding_plan` 绑定；不得将 v3.3/pin37 当作 v3.4 实现已审证明。

本包不含市场数据、凭据、朋友材料或其正文，也不改变 12 格预算。
