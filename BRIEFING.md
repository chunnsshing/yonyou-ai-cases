# Briefing：Yonyou AI 场景案例库（给协作者的 Claude）

> 把这份文档整段发给你的 Claude。它说明了这个项目是什么、文件怎么组织、原始资料怎么转成统一格式、怎么接入同一个 GitHub 仓库并同步进度。第 7 节是接手后的第一步清单。

## 1. 项目是什么

ChunShing 和同事共同维护的 **AI 场景案例库**：按业务领域整理"AI 可以用在企业标准流程的哪里"，最终输出一个 **横版（16:9）、简约、带 Yonyou logo 的 HTML 页面**，可在线浏览、演示、导出 PDF。

- 仓库：`https://github.com/chunnsshing/yonyou-ai-cases`（公开仓库）
- 在线预览：`https://chunnsshing.github.io/yonyou-ai-cases/`（push 到 main 后约 1 分钟自动更新）
- 页面结构：首页按 **领域页签**（财务 / 供应链 / 制造 / 人力 / 销售 / 经营分析）→ 点击场景卡片 → **每个场景一页**，内容固定为：场景描述、业务痛点、标准流程图（标出 AI 介入的步骤）
- **中英双语**：页面按 `L` 键（或右上角按钮）切换中文 / English，选择会被记住；也可用链接参数 `?lang=en` 直接打开英文版
- 每个场景有一个 **状态标签**：已交付 `delivered` / 可复制 `replicable` / 可Demo `demo` / 待验证 `to-verify` / 未来可能 `future`

**核心原则：内容和样式分离。** 人只写数据文件（YAML），样式全部由模板统一生成。所以无论原始资料是什么格式，最后都长一个样子。

## 2. 仓库结构

```
site.yaml                  全站配置：领域页签、状态标签、主色、logo 路径（改这里全局生效）
cases/<领域id>/<场景id>.yaml  ★ 每个场景一个文件，这是唯一需要日常编辑的地方
template/case-template.yaml  场景模板（带逐字段说明和字数上限）
template/index.html        页面模板（样式/交互，一般不改）
build.py                   校验 + 生成 dist/index.html（单文件、无外部依赖、可离线）
assets/logo.png            官方 Yonyou Singapore logo（透明底）
.github/workflows/pages.yml  push 后自动构建并发布到 GitHub Pages
raw/                       本地放原始资料用，已被 .gitignore 忽略，不会上传
```

## 3. 场景文件格式（必须严格遵守）

```yaml
id: fin-ap-invoice-matching     # 全库唯一，小写英文+连字符，且与文件名一致
title: 应付发票识别与三单匹配      # ≤18字
domain: finance                 # finance / supply-chain / manufacturing / hr / sales / analytics，且文件放在同名文件夹
status: to-verify               # delivered / replicable / demo / to-verify / future
owner: 负责人名字                 # 谁在跟进
updated: 2026-09-24             # 最后修改日期
industry: 通用                   # 选填
client: ""                      # 选填；公开仓库，客户名一律不写，只在 industry 写行业（门店名、API 路径等细节也不写）
products: [YonSuite]            # 选填
summary: 一句话价值说明            # ≤40字
description: >                  # ≤140字：谁、在哪个业务环节、现在怎么做
  ……
pain_points:                    # 2–4 条
  - title: 痛点标题               # ≤12字
    detail: 痛点说明               # ≤40字
system: YonSuite                # 选填；泳道图第三行的系统名（YonSuite / YonBIP / NCC），默认 ERP
flow:                           # 标准业务流程 3–8 步，按顺序；页面画成三行泳道图（使用者 / YonWork / 系统）
  - step: 步骤名                  # ≤10字（7–8 步时 ≤9）
    lane: ai                    # 必填：user 使用者 / ai YonWork / erp 系统；至少一步是 ai
    note: 这一步做什么            # 选填，≤26字（7–8 步时 ≤18）
    edge: 回复                    # 选填，传入这一步的内容，≤6字
    type: decision              # 选填：decision 判断 / exception 例外（虚线）/ future 后续阶段
sources: [raw/原始文件名.pdf]      # 选填，记录出处，不展示

en:                             # 英文版，结构与中文一一对应（痛点条数、流程步数、每步 lane/type 都要相同）
  title: …                      # ≤34 字符
  industry: …                   # 选填
  summary: …                    # ≤95
  description: >                # ≤380
    …
  pain_points:                  # title ≤26，detail ≤80
    - title: …
      detail: …
  flow:                         # ≤6 步：step ≤24、note ≤80；7–8 步：step ≤18、note ≤40；edge ≤14
    - step: …
      lane: ai                  # lane / type 必须与中文逐步一致
      note: …
```

字数上限是为了保证横版一页放得下；超出 `build.py` 会警告。完整带注释的模板见 `template/case-template.yaml`，参考已有场景，如 `cases/sales/sales-po-email-to-do.yaml`。旧格式（step/role/ai）构建时会自动转换并警告，请改成 lane/note 写法。

## 4. 把任意格式的资料转成场景文件（给 Claude 的工作规则）

用户可能丢给你：Word/PDF/PPT、截图、会议纪要、微信聊天记录、Notion 页面、口述要点、Excel 流程表……处理方式都一样：

1. **读懂资料**，先判断里面有几个独立场景。一个场景 = 一个具体业务流程里的一类 AI 应用。资料里有多个就拆成多个文件。
2. **归到领域**：只能用 `site.yaml` 里的领域 id。确实不属于任何领域时，先问用户，不要自己新增领域。
3. **映射字段**：
   - 场景描述 = 现状（谁、在哪个环节、现在怎么做），不写方案
   - 痛点 = 现状的问题，每条一个点，标题短、说明具体
   - 流程 = **标准业务流程**（不是 AI 方案的步骤），每一步按“谁在做”放进泳道：人做的放 `user`，AI 做的放 `ai`，系统里生成/读取数据的放 `erp`
   - 状态：按资料中的事实判断；判断不了默认 `to-verify` 并告诉用户
4. **压缩到字数上限内**，用业务语言，删掉形容词和营销话术。
5. **中英双语都要写**：资料是中文就译出 `en:`，资料是英文就写出中文顶层字段。用企业/ERP 常用术语（如 AP、PO、3-way match），不要逐字直译；两种语言表达同一件事，不增不减。
6. **不编造**：资料里没有的数字、客户名、效果指标、"已上线"等事实一律不写；缺必填内容时列出来问用户，而不是自己补。
7. **保密**：这是公开仓库。客户名、内部报价、合同、联系人等敏感信息不写进 YAML；原始资料放 `raw/`（不会上传）。
8. 写完运行校验，修到 0 错误 0 警告：
   ```bash
   pip install pyyaml   # 首次
   python build.py --strict
   ```
   然后打开 `dist/index.html`，中英文（按 L）各看一眼，确认版面没有溢出。
9. 给用户一个简短汇总：新增/修改了哪些场景、各自状态、哪些信息需要他确认。

## 5. 接入 GitHub（按你所在的环境选一种）

仓库 owner 是 ChunShing（GitHub: `chunnsshing`）。**先让你的用户确认已接受仓库的 Collaborator 邀请**（GitHub 通知或邮件里点 Accept），否则没有写权限。

**A. 本地终端 / Claude Code（首选）**
```bash
git clone https://github.com/chunnsshing/yonyou-ai-cases.git
cd yonyou-ai-cases && pip install pyyaml && python build.py --strict
```
推送用你用户本人的 GitHub 登录（`gh auth login` 或已有的 git 凭据）。不要索要、保存或在对话里输出任何 token / 密码。

**B. 云端会话（Claude 网页 / Cowork 云端 / Claude Code on the web）**
云端会话只能访问**开启会话时绑定的仓库**。请让用户在新建会话时选中 `chunnsshing/yonyou-ai-cases`。如果 `git push` 返回 403 或 "not in this session's authorized repository set"，说明没绑定，不要反复重试，直接告诉用户换一个绑定了该仓库的会话。

**C. 以上都不可用时的兜底：GitHub 网页上传**
在用户浏览器里打开 `https://github.com/chunnsshing/yonyou-ai-cases/upload/main/cases/<领域id>`，上传写好的 yaml 文件并直接提交到 main（同名文件会被覆盖）。每次提交前让用户确认。

**验证已接入：** `git log --oneline -5` 能看到历史；修改后 push，约 1 分钟后在线预览更新（Actions 页面显示绿色 ✓）。

## 6. 日常协作规则

- **开工前**：`git pull --rebase`，再看一眼 `cases/` 里有没有同主题场景，避免两人重复写。
- **一个场景 = 一个文件**，两人改的是不同文件，基本不会冲突。开始写一个较大的场景时，可以先提交一个 `status: to-verify` 的初版占位，让对方知道你在做。
- **提交**：
  ```bash
  python build.py --strict          # 必须 0 错误 0 警告
  git add cases/ && git commit -m "新增：<领域> <场景名>"
  git pull --rebase && git push
  ```
- **commit 信息**：`新增：…` / `更新：…（状态 to-verify→demo）` / `删除：…`
- **归属**：`owner` 写你用户的名字；不改别人 `owner` 的场景，除非对方同意，并在 commit 信息里写明。
- **共享配置**：`site.yaml`（领域、状态、中英文名）、`template/`、`build.py`、`.github/` 改之前先让用户和 ChunShing 确认，并单独提交。
- **不要提交** `dist/`、`raw/`（已忽略）。
- **看进度**：在线预览首页的状态图例有各状态数量，卡片上有负责人和更新日期；或看 `git log`。

## 7. 接手后第一次要做的事

1. 按第 5 节接入仓库，跑通 `python build.py --strict`。
2. 读 `template/case-template.yaml` 和示例 `cases/finance/fin-ap-invoice-matching.yaml`。
3. 打开在线预览，按 `L` 看中英文，感受版面（页面会铺满浏览器窗口；导出 PDF 固定为 1280×720 横版每场景一页）。
4. 向你的用户确认：他负责哪些领域 / 场景，`owner` 用什么名字。
5. 之后用户给你资料时，按第 4 节转换，按第 6 节提交。

## 8. 常见问题

- **构建报错 "文件应放在 cases/xxx/ 下"**：domain 和文件夹不一致，挪文件或改 domain。
- **"flow 至少要有一步在 YonWork 泳道"**：这个库的重点就是标出 AI 介入点，每个场景至少一步 `lane: ai`。
- **想加新领域**：在 `site.yaml` 的 domains 里加一项，并新建同名文件夹（先和对方确认）。
- **换 logo**：覆盖 `assets/logo.png`，或放新文件并改 `site.yaml` 的 `logo`。
- **英文版缺失**：构建会警告（`--strict` 下算失败）；页面切到英文时该场景显示中文并带 "中文 only" 标记。
- **领域/状态的英文名**：在 `site.yaml` 的 `name_en` / `desc_en` 改。
- **导出 PDF**：在页面上点"导出本领域 PDF"（首页）或"导出 PDF"（场景页），浏览器打印选"另存为 PDF"，每个场景一页横版。
- **快捷键**：`L` 切换中/英；场景页 ← → 切换同领域场景，Esc 返回领域列表。
