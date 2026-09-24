# Yonyou AI 场景案例库 · AI Use Case Library

按业务领域整理 AI 在企业标准流程中的应用场景。横版单页 HTML，统一模板，中英双语（按 `L` 切换），可在线浏览、演示、导出 PDF。

**在线预览：** https://chunnsshing.github.io/yonyou-ai-cases/

## 快速开始

```bash
pip install pyyaml
cp template/case-template.yaml cases/finance/fin-xxx.yaml   # 新建场景并填写
python build.py --strict                                    # 校验 + 生成 dist/index.html
```

| 状态 | id | 含义 |
|---|---|---|
| 已交付 | `delivered` | 已在客户现场上线交付 |
| 可复制 | `replicable` | 方案成熟，可直接复制到其他客户 |
| 可Demo | `demo` | 有可演示的 Demo 环境 |
| 待验证 | `to-verify` | 方案已设计，需技术/业务验证 |
| 未来可能 | `future` | 方向性构想，依赖产品或技术演进 |

协作规则和字段说明见 [BRIEFING.md](BRIEFING.md)。
