# CLAUDE.md

本仓库是 Yonyou AI 场景案例库。开始任何工作前先完整阅读 `BRIEFING.md`，并严格按其中第 3、4、5 节执行。

最重要的几条：
- 只编辑 `cases/<领域id>/<场景id>.yaml`；样式由 `template/index.html` 统一生成，不要为单个场景改模板。
- 任何格式的原始资料都转成 `template/case-template.yaml` 的结构；不编造资料里没有的数字、客户、上线状态。
- 每个场景必须中英双语：中文写顶层字段，英文写 `en:` 块，两者结构一一对应。
- 公开仓库：不写未确认可公开的客户名或内部敏感信息；原始资料放 `raw/`（已忽略）。
- 提交前 `python build.py --strict` 必须 0 错误 0 警告；提交前 `git pull --rebase`。
- `site.yaml` 和 `template/` 是共享配置，改动前先让用户和协作者确认。
