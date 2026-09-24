#!/usr/bin/env python3
"""把 cases/**/*.yaml 校验后渲染成单文件 dist/index.html（无外部依赖，可离线打开/发给客户）。

用法:
  python build.py            # 校验 + 构建；有错误则失败，超长只警告
  python build.py --strict   # 警告也算失败（提交前建议跑一次）
  python build.py --check    # 只校验不输出
依赖: pip install pyyaml
"""
import base64, datetime, json, mimetypes, pathlib, re, sys

try:
    import yaml
except ImportError:
    sys.exit("缺少 PyYAML：pip install pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent
LIMITS = {  # 字段: 最大长度（中文按字数，英文按字符数；超出=警告）
    "zh": {"title": 18, "summary": 40, "description": 140, "pain.title": 12, "pain.detail": 40,
           "flow.step": 10, "flow.role": 8, "flow.ai": 36},
    "en": {"title": 34, "summary": 95, "description": 380, "pain.title": 26, "pain.detail": 80,
           "flow.step": 18, "flow.role": 16, "flow.ai": 60},  # 7–8 步时的上限
}
REQUIRED = ["id", "title", "domain", "status", "owner", "updated", "summary", "description", "pain_points", "flow"]
EN_REQUIRED = ["title", "summary", "description", "pain_points", "flow"]


def load_yaml(p):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


CJK_GAP = re.compile(r"(?<=[\u3000-\u9fff\uff00-\uffef])\s+(?=[\u3000-\u9fff\uff00-\uffef])")


def s(v):
    """去首尾空白，并去掉中文之间因YAML折行产生的空格"""
    return "" if v is None else CJK_GAP.sub("", str(v).strip())


def check_content(c, lang, E, W, ref_flow=None):
    """校验一套语言内容（中文=顶层字段，英文=en: 块）"""
    tag = "" if lang == "zh" else "en."
    L = dict(LIMITS[lang])
    if lang == "en" and len(c.get("flow") or []) <= 6:   # 步骤少时每个节点更宽，英文可放宽
        L.update({"flow.step": 22, "flow.role": 20, "flow.ai": 80})

    def ln(key, val, label):
        if len(s(val)) > L[key]:
            W(f"{tag}{label} 超长 {len(s(val))}/{L[key]}：{s(val)[:24]}…")

    for k in ("title", "summary", "description"):
        ln(k, c.get(k), k)
    pains = c.get("pain_points") or []
    if pains and not (2 <= len(pains) <= 4):
        W(f"{tag}pain_points 建议 2–4 条（当前 {len(pains)}）")
    for i, p in enumerate(pains, 1):
        if not isinstance(p, dict) or not p.get("title"):
            E(f"{tag}pain_points 第{i}条需要 title（和 detail）")
            continue
        ln("pain.title", p.get("title"), f"痛点{i}.title")
        ln("pain.detail", p.get("detail"), f"痛点{i}.detail")
    flow = c.get("flow") or []
    if ref_flow is None and flow and not (3 <= len(flow) <= 8):
        (E if len(flow) > 10 else W)(f"flow 建议 3–8 步（当前 {len(flow)}）")
    for i, f in enumerate(flow, 1):
        if not isinstance(f, dict) or not f.get("step"):
            E(f"{tag}flow 第{i}步需要 step")
            continue
        ln("flow.step", f.get("step"), f"流程{i}.step")
        ln("flow.role", f.get("role"), f"流程{i}.role")
        ln("flow.ai", f.get("ai"), f"流程{i}.ai")
    if ref_flow is None:
        if flow and not any(isinstance(f, dict) and f.get("ai") for f in flow):
            E("flow 至少要有一步标注 ai（AI在哪里介入）")
    else:
        if len(flow) != len(ref_flow):
            E(f"en.flow 步数（{len(flow)}）必须与中文 flow（{len(ref_flow)}）一致")
        elif any(bool(a.get("ai")) != bool(b.get("ai")) for a, b in zip(flow, ref_flow)
                 if isinstance(a, dict) and isinstance(b, dict)):
            E("en.flow 标注 ai 的步骤必须与中文 flow 一一对应")


def validate(case, path, site, errors, warnings):
    rel = path.relative_to(ROOT)
    E = lambda m: errors.append(f"{rel}: {m}")
    W = lambda m: warnings.append(f"{rel}: {m}")
    for k in REQUIRED:
        if not case.get(k):
            E(f"缺少必填字段 `{k}`")
    domains = {d["id"] for d in site["domains"]}
    statuses = {x["id"] for x in site["statuses"]}
    if case.get("domain") and case["domain"] not in domains:
        E(f"domain `{case['domain']}` 不在 site.yaml 领域列表 {sorted(domains)}")
    if case.get("domain") and path.parent.name != case.get("domain"):
        E(f"文件应放在 cases/{case.get('domain')}/ 下（当前在 {path.parent.name}/）")
    if case.get("status") and case["status"] not in statuses:
        E(f"status `{case['status']}` 无效，可选 {sorted(statuses)}")
    if case.get("id") and path.stem != case["id"]:
        E(f"文件名应与 id 一致：{case['id']}.yaml")
    check_content(case, "zh", E, W)

    en = case.get("en")
    if not en:
        W("缺少英文版 `en:`（按 L 切换英文时会显示中文）")
        return
    for k in EN_REQUIRED:
        if not en.get(k):
            E(f"en 缺少字段 `{k}`")
    if len(en.get("pain_points") or []) != len(case.get("pain_points") or []):
        E("en.pain_points 条数必须与中文一致")
    check_content(en, "en", E, W, ref_flow=case.get("flow") or [])


def content(c):
    return {
        "title": s(c.get("title")), "summary": s(c.get("summary")), "description": s(c.get("description")),
        "industry": s(c.get("industry")),
        "pain_points": [{"title": s(p.get("title")), "detail": s(p.get("detail"))} for p in c.get("pain_points") or []],
        "flow": [{"step": s(f.get("step")), "role": s(f.get("role")), "ai": s(f.get("ai"))} for f in c.get("flow") or []],
    }


def normalize(case):
    return {
        "id": s(case["id"]), "domain": s(case["domain"]), "status": s(case["status"]),
        "owner": s(case.get("owner")), "updated": s(case.get("updated")), "client": s(case.get("client")),
        "products": [s(x) for x in (case.get("products") or [])], "example": bool(case.get("example")),
        "zh": content(case), "en": content(case["en"]) if case.get("en") else None,
    }


def logo_data_uri(site):
    p = ROOT / site.get("logo", "assets/logo.png")
    if not p.exists():
        return ""
    mime = mimetypes.guess_type(p.name)[0] or "image/svg+xml"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


def main():
    strict, check = "--strict" in sys.argv, "--check" in sys.argv
    site = load_yaml(ROOT / "site.yaml")
    errors, warnings, cases, seen = [], [], [], {}
    for path in sorted((ROOT / "cases").glob("*/*.y*ml")):
        try:
            case = load_yaml(path)
        except yaml.YAMLError as e:
            errors.append(f"{path.relative_to(ROOT)}: YAML 格式错误 {e}")
            continue
        n = len(errors)
        validate(case, path, site, errors, warnings)
        if case.get("id") in seen:
            errors.append(f"{path.relative_to(ROOT)}: id 与 {seen[case['id']]} 重复")
        seen[case.get("id")] = path.relative_to(ROOT)
        if len(errors) == n:
            cases.append(normalize(case))

    for w in warnings:
        print("⚠️ ", w)
    for e in errors:
        print("❌", e)
    print(f"—— {len(cases)} 个场景通过，{len(errors)} 个错误，{len(warnings)} 个警告")
    if errors or (strict and warnings):
        sys.exit(1)
    if check:
        return

    data = {"site": {k: site[k] for k in ("title", "title_en", "subtitle", "subtitle_en", "brand_color", "default_lang", "domains", "statuses") if k in site},
            "logo": logo_data_uri(site), "cases": cases,
            "built": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
    html = (ROOT / "template" / "index.html").read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("/*__DATA__*/null", payload)
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(html, encoding="utf-8")
    print(f"✅ 已输出 {out / 'index.html'}")


if __name__ == "__main__":
    main()
