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

## Demo 视频 / 看板

把视频（.mp4 / .mov / .webm）或结果看板（.html）放进 `videos/<场景id>/`，构建时会复制到 `dist/videos/`，
场景自动加上「已就绪」标签，卡片和场景页出现「播放 Demo」。这是公开网站：只放演示/测试租户的内容，
不放真实客户数据；视频先压缩（GitHub 单个文件上限 100MB），例如：

```bash
ffmpeg -i 原视频.mov -vf "scale='min(1920,iw)':-2,fps=30" -c:v libx264 -crf 26 -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart videos/<场景id>/demo.mp4
```

场景的 `updated` 日期保留在 yaml 和页面数据里（`DATA.cases[].updated`、`DATA.built`），但不在页面上显示。
