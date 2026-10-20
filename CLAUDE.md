# CLAUDE.md

本仓库是 Yonyou AI 场景案例库。开始任何工作前先完整阅读 `HANDOFF.md`（当前的发布标准：网站已对客户公开、标签、Demo 视频/HTML、隐私检查），再读 `BRIEFING.md` 第 3–4 节（如何把资料转成场景文件）。两者冲突时以 `HANDOFF.md` 为准。

最重要的几条：
- 网站对客户公开，由 yonyou.com.sg 链接：push 到 main 约 1 分钟后即上线。只推送用户已在本地预览并确认的内容。
- 场景、视频、HTML 看板里都不能有客户数据（公司名、人名、电话、车牌、发票、银行账号、客户的销售数据等）；每次提交前按 `HANDOFF.md` 第 5 节检查。
- `status: delivered`（网站显示「客户已上线」）只在用户确认已在客户处上线时使用；`ready` 由构建自动添加，不要手写。
- Demo 视频/HTML 放在 `videos/<场景id>/`，视频先压缩（单个文件 < 100MB）。
- 只编辑 `cases/<领域id>/<场景id>.yaml`；样式由 `template/index.html` 统一生成，不要为单个场景改模板。
- 任何格式的原始资料都转成 `template/case-template.yaml` 的结构；不编造资料里没有的数字、客户、上线状态。
- 每个场景必须中英双语：中文写顶层字段，英文写 `en:` 块，两者结构一一对应。
- 公开仓库：不写未确认可公开的客户名或内部敏感信息；原始资料放 `raw/`（已忽略）。
- 提交前 `python build.py --strict` 必须 0 错误 0 警告；提交前 `git pull --rebase`。
- `site.yaml` 和 `template/` 是共享配置，改动前先让用户和协作者确认。
