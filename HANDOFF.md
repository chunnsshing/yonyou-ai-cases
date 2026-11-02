# HANDOFF — publishing standard for the YonWork Use Case Library

> For a collaborator's Claude. Read this first, then `BRIEFING.md` sections 3–4 (how to turn raw
> material into a case file). **Where `BRIEFING.md` and this file disagree, this file wins** — it
> reflects the site as it is now: a client-facing page that yonyou.com.sg links to.

## 1. What you are publishing to

- Live site: https://chunnsshing.github.io/yonyou-ai-cases/ — **public and client-facing.** Yonyou
  Singapore's website links to it, so every visitor is a prospect, not a colleague.
- Repo: `https://github.com/chunnsshing/yonyou-ai-cases` (public). Owner: Elmond (`chunnsshing`).
- **A push to `main` goes live in about a minute** (GitHub Actions builds `dist/` and deploys it).
  There is no staging. Treat every push as publishing.

So the two rules that matter most:
1. **No client data, ever** — not in case text, not in videos, not in HTML dashboards, not in commit
   messages. See section 5.
2. **Only push what your user has seen and approved.** Build, preview locally, show them, then push.

## 2. Setup (once)

```bash
git clone https://github.com/chunnsshing/yonyou-ai-cases.git
cd yonyou-ai-cases
python3 -m venv .venv && .venv/bin/pip install pyyaml      # or: pip install pyyaml
.venv/bin/python build.py --strict                          # must end with 0 errors, 0 warnings
```

Your user must have accepted the repo's Collaborator invite to push. Push with their own GitHub login
(`gh auth login` or existing git credentials). Never ask for, store or print a token or password.
`.venv/`, `dist/` and `raw/` are git-ignored and never committed.

**Preview locally** (videos and dashboards need a server, not a double-clicked file):

```bash
python3 -m http.server 8000 --directory dist      # then open http://localhost:8000
```

Check both languages (press `L`), the home page, the case page, and Play Demo if you added a demo.

## 3. Repo layout

```
cases/<area>/<case-id>.yaml   ← the only files you edit day to day (one case = one file)
videos/<case-id>/             ← demo videos and HTML dashboards for that case (section 4)
template/case-template.yaml   ← annotated field reference with length limits
site.yaml                     ← SHARED: areas, tag names, which tags are public
template/index.html           ← SHARED: page design (matches yonyou.com.sg)
build.py, .github/            ← SHARED: build and deploy
raw/                          ← your source material, git-ignored, never uploaded
```

**Shared files** (`site.yaml`, `template/`, `build.py`, `.github/`): don't change them without Elmond
agreeing first, and commit them separately from case changes.

Good example to copy: `cases/sales/sales-po-email-to-do.yaml` (8 steps, decision/exception types,
edge labels). (The example named in `BRIEFING.md`, `fin-ap-invoice-matching.yaml`, no longer exists.)

## 4. Adding or updating a case

Follow `BRIEFING.md` section 4 for content. In short:

- File: `cases/<area>/<id>.yaml`, file name = `id`, folder = `domain`. Areas: `finance`,
  `supply-chain`, `manufacturing`, `hr`, `sales`, `analytics` (new areas need Elmond).
- Required: `id, title, domain, status, owner, updated, visual, summary, description, pain_points, flow`,
  plus a full English `en:` block with the same number of pain points and flow steps, and the same
  `lane`/`type` on every step.
- Flow = the **standard business process**, 3–8 steps, in three lanes: `user` (a person), `ai`
  (YonWork), `erp` (the system). At least one step must be `lane: ai`.
- `owner`: your user's name. Don't edit cases another owner holds unless they agree.
- `updated`: today's date, YYYY-MM-DD. **It is not shown on the site** (clients don't need it); it is
  kept in the yaml and in the page data for the team.
- Length limits are enforced: `build.py --strict` must report 0 errors and 0 warnings.
- Never invent numbers, client names, results or go-live status. Ask your user instead.

### Tags (`status:`)

Write the internal status honestly; the site decides what clients see. Only three tags are public.

| `status` id | Internal meaning | Shown on the site as |
|---|---|---|
| `delivered` | Running in production at a real client | **Live at Clients** (green tag + filter) |
| `best-practice` | Flagship use case proven with Yonyou clients in China. Goes in its normal area | **Best Practice** (amber tag + filter) |
| `replicable` | Proven, can be rolled out to other clients | not shown (internal) |
| `demo` | A demo environment exists | not shown (internal) |
| `to-verify` | Being developed, can't demo yet | not shown (internal) |
| `future` | Idea, needs validation | not shown (internal) |
| `ready` | **Automatic** — never write it. Added by the build when `videos/<id>/` has a file | **Watch Demo** filter + red ▶ button on the card + Play Demo button on the case page |

- `status` can be a list: `status: [delivered, demo]`.
- **`delivered` only when your user confirms the case is live at a client.** It is the strongest claim
  on the site. Don't infer it from "replicable" or a successful demo.
- Which tags are public is controlled by `public: false` in `site.yaml` (shared file).
- Cases are listed with the `bold_owner` set in `site.yaml` (currently Elmond) first; everyone else's
  cases follow. That is expected, not a bug.

### Card picture (`visual:`)

Every card on the home page is a **picture plus a title**, so a client can scan the page without
reading. Each case picks one ready-made drawing with a single line in its yaml, right after `system:`:

```yaml
system: YonBIP
visual: doc
```

**Choose by what the result looks like, not by the topic or the area.** Ask "what does the client get
at the end?" and take the closest row below. Sharing a picture with another case is fine.

| `visual` | The picture | Use it when the result is… | Example case |
|---|---|---|---|
| `bars` | Bar chart, one bar in red | A comparison that highlights what changed | `ana-marketing-intelligence` |
| `hbars` | Ranked horizontal bars | A ranking by product, branch, etc. | `ana-product-sales-by-branch` |
| `forecast` | Bars, then dashed future bars | Actuals followed by a forecast or budget | `ana-month-end-analysis` |
| `dash` | KPI tiles above a small chart | A one-page overview or dashboard | `fin-company-financial-overview` |
| `trend` | Line crossing a target, red alert dot | Monitoring a value with an alert | `sc-material-price-monitor` |
| `stock` | Line falling to a limit | Something running out; a latest-action date | `sc-replenishment-forecast` |
| `heat` | Heatmap grid with a red peak | Patterns by time, place or category | `ana-store-peak-heatmap` |
| `gauge` | Half-circle gauge | One overall score or rating | `fin-customer-credit-score` |
| `radar` | Five-point radar | A score across several dimensions | `sc-procurement-analysis` |
| `compare` | Stacked columns, best one in red | Choosing between options | `sales-cost-estimate-quotation` |
| `doc` | Tilted paper → system document | One photo or PDF becomes a system record | `sc-po-from-photo` |
| `batch` | Stack of paper → several documents | Many inputs become records in one go | `sc-batch-doc-capture` |
| `order` | Email → document → truck | An order runs from request to delivery | `sales-po-email-to-do` |
| `pay` | Invoice → approved → bank | An invoice runs through to payment | `fin-p2p-vendor-invoice` |
| `send` | Document → emails | Documents are checked and sent to people | `fin-soa-project-email` |
| `folder` | Document → folder | Files are generated and filed or uploaded | `fin-invoice-pdf-export` |
| `ask` | Speech bubble → document | One sentence creates a document | `sales-rate-card-quotation` |
| `split` | Document branching into rows | One source is split or allocated | `fin-contract-gross-profit` |
| `match` | Two columns linked, one dashed red | Reconciliation; exceptions stand out | `fin-ecommerce-settlement-recon` |
| `chat` | Question and answer bubbles | The AI answers questions | `fin-finance-qa-assistant` |
| `graph` | Files linked to a red hub | Linked search across documents or records | `ana-document-query` |
| `rank` | Prioritised list, top row red | A ranked work queue or brief | `sc-daily-fulfilment-queue` |
| `team` | Red lead linked to three agents | Several agents working together | `sc-agent-team-collaboration` |
| `profile` | Person with a timeline | A full history of one customer or item | `sales-plate-lookup` |

Keep the card style, so the page stays calm as it grows:

- **Don't add text to the card.** It shows the picture, the title, the public tags and, on the All
  tab, the area. `summary` belongs on the case page, not the card.
- **No screenshots, photos or per-case artwork on cards.** Demo screens are unreadable at card size
  and need a privacy check. Show the demo through the red ▶ button, which the build adds for you.
- **Pictures have no words or numbers.** They work in both languages and can't be mistaken for a real
  result. `visual` goes at the top level only, not in `en:`.
- **Use a row from the table.** A new picture is a shared-file change, so it needs Elmond's OK. Add it
  to `VIS` in `template/index.html` and `VISUALS` in `build.py`, then add a row here. Draw it in the
  same 240×135 frame and grey palette, with one red focus point and no text.

## 5. Privacy — the checklist (do this every time)

The site is public and linked from the company website. Before you commit a case, video or dashboard:

- **Case text and file names:** no client or partner company names, store/outlet names, people,
  prices, contract terms, or internal URLs. Put the industry in `industry:` instead. The `sources:`
  field is not shown on the page but **is public in the repo**: keep client names out of it too.
- **Commit messages:** no client names.
- **Videos:** must not show real client records: customer/supplier names, phone numbers, emails,
  vehicle plates, addresses, invoices, bank account details, client sales figures, a client's
  mailbox or inbox list. Record on a demo/test tenant, or blur those regions before adding.
- **HTML dashboards:** must not contain real client data, **including hidden data** (embedded JSON,
  search indexes, tooltips, `<title>`). Build them from a demo tenant or synthetic data. Renaming
  what you can see is not enough; the data underneath has to be fake or aggregated and rescaled.
- If you're unsure, don't commit it. Ask your user, and Elmond if needed.

**Check a video:** make a contact sheet of 8 frames and look at every one:

```bash
f=videos/<id>/demo.mp4
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
ffmpeg -loglevel error -y -i "$f" -vf "fps=8/$d,scale=640:-2,tile=4x2" -frames:v 1 /tmp/sheet.jpg
```

Scrub through the full video too: frames between samples can still show a name or number.

**Check an HTML dashboard:** search the whole file, not just what's visible:

```bash
f=videos/<id>/dashboard.html
grep -o "<title>[^<]*" "$f" | head
grep -Eoc "(^|[^0-9])[689][0-9]{3} ?[0-9]{4}([^0-9]|$)" "$f"   # SG-style phone numbers → expect 0
grep -Eoc "\bS[A-Z]{1,2} ?[0-9]{1,4} ?[A-Z]\b" "$f"               # SG-style plates → expect 0 unless synthetic
grep -Eio "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}" "$f" | sort -u    # emails → expect none
grep -Eic "pte\.? ?ltd|sdn\.? ?bhd|co\., ?ltd" "$f"               # company names → look at every hit
```

Also grep for the client's own name and its store/outlet names. Report what you checked to your user.

## 6. Demo videos and HTML dashboards

Put files in **`videos/<case-id>/`** (folder name = the case `id`). That is all. The build:

- copies them to `dist/videos/<case-id>/`,
- adds the automatic `ready` status (the **Watch Demo** filter),
- shows a red **▶** button on the card and a **Play Demo** button on the case page. Both always open
  in a **new tab**.

| You add | Play Demo opens |
|---|---|
| one `.html` file | that dashboard directly, in a new tab |
| one or more videos (`.mp4` `.mov` `.m4v` `.webm`) | the built-in player in a new tab (‹ › between clips, Space pause, hold Q for 4×, tap Q for +5 s) |

Rules:

- **Name files plainly**: `demo.mp4`, `dashboard.html`. Several files play in file-name order, so
  use `01-overview.mp4`, `02-detail.mp4`, …; the file name (without extension) is the clip label.
- **Compress every video before committing.** GitHub rejects files over 100 MB, and the site loads
  faster. Screen recordings drop from ~100 MB to a few MB with no visible loss:

  ```bash
  ffmpeg -i original.mov -vf "scale='min(1920,iw)':-2,fps=30" -c:v libx264 -preset slow -crf 26 \
    -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart videos/<case-id>/demo.mp4
  ```

  Keep the original outside the repo. Grab one frame and confirm on-screen text is still readable.
- **HTML dashboards must be one self-contained file** (inline CSS/JS/data). No API keys, tokens,
  tenant URLs, or calls to a live system. Open it from the local preview to check it works.
- Privacy checklist (section 5) applies to every file, every time.

## 7. Daily workflow

```bash
git pull --rebase                       # always first: someone else may have pushed
# … edit cases/… and/or add videos/<id>/ …
.venv/bin/python build.py --strict      # 0 errors, 0 warnings
python3 -m http.server 8000 --directory dist   # preview; show your user
git add cases/ videos/
git commit -m "New: <area> <case title in English>"    # or "Update: …", "Demo: …", "Remove: …"
git pull --rebase && git push
```

Then check the deploy: `gh run list --limit 1` should show `success`, and the live site updates in
about a minute (hard-refresh to bypass the cache).

- One case per commit where possible. Never commit `dist/`, `raw/` or `.venv/`.
- Don't push work in progress to `main`; it goes straight to clients.
- Commit message footer: whatever attribution your user's setup requires.

## 8. Before you push — checklist

- [ ] `git pull --rebase` done; no one else already wrote this case (`ls cases/*/`)
- [ ] `build.py --strict` → 0 errors, 0 warnings
- [ ] Both languages checked in the local preview; nothing overflows on the case page
- [ ] `visual` chosen from the table in section 4 and the card checked on the home page
- [ ] `delivered` only if your user confirmed it is live at a client
- [ ] Privacy checklist (section 5) done for text, videos and dashboards
- [ ] Videos compressed; every file under 100 MB
- [ ] Shared files untouched (or changed with Elmond's OK, in a separate commit)
- [ ] Your user has seen the preview and said to publish

## 9. Troubleshooting

The build prints its messages in Chinese:

- **`文件应放在 cases/xxx/ 下`**: `domain` and folder don't match.
- **`文件名应与 id 一致`**: the file name must equal `id`.
- **`flow 至少要有一步在 YonWork 泳道（lane: ai）`**: add a `lane: ai` step.
- **`en.flow 步数…必须与中文 flow…一致` / `en.flow 每一步的 lane / type 必须与中文 flow 一一对应` /
  `en.pain_points 条数必须与中文一致`**: the English block must mirror the Chinese one exactly.
- **`… 超长 n/limit`** (too long): shorten. The limits keep each case on one 16:9 page and in the PDF export.
- **`status … 无效`**: use one of the ids in section 4; never write `ready`.
- **`缺少 visual` / `visual … 无效`**: add `visual:` with a name from the table in section 4.
- **Push rejected (non-fast-forward)**: `git pull --rebase`, rebuild, push again.
- **Push rejected, file too large**: compress the video (section 6); if it is already in a commit,
  `git reset --soft HEAD~1`, replace the file, recommit.
- **Play Demo missing after adding a file**: the folder name must equal the case `id` exactly, and
  the extension must be one of those listed in section 6. Rebuild.
- **Something looks wrong on the live site after a push**: tell your user right away. Revert with
  `git revert <commit> && git push` rather than rewriting history.
