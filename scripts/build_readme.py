"""Rebuilds README.md's generated parts (counts, overview, top 20, category tables) and
data/directories.csv from data/directories.json, and keeps the JSON sorted by DR.

Usage, from the repo root:  python scripts/build_readme.py

Edit data/directories.json only; this script writes everything that's derived from it.
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "directories.json"

LABELS = {
    "🚀 Startup Directory": "Startup Directories",
    "⭐️ Review Directory": "Review Sites",
    "👥 Community": "Communities",
    "🤖 AI Directory": "AI Directories",
    "🗞 Press Coverage": "Press & Media",
    "📂 General Directory": "General Directories",
    "🧩 SaaS Marketplace": "SaaS Marketplaces",
    "💫 Other": "Other",
    "💻 Software Directory": "Software",
    "🎨 Design Directory": "Design",
    "🌍 International": "International",
    "🤝 API Marketplace": "API Marketplaces",
    "💻 Social Media": "Social Media",
    "💵 Acquire & Sell": "Acquire & Sell",
}
HEAD = "| Directory | DR | Link Type | Pricing | Description |\n|-----------|:--:|-----------|:-------:|-------------|"


def by_dr(d):
    # Highest DR first, unrated last; ties keep the file's order.
    return (d["domain_rating"] is None, -(d["domain_rating"] or 0))


def anchor(heading):
    # GitHub's heading ids: lowercase, keep letters, digits, spaces and hyphens, spaces to hyphens.
    return "#" + re.sub(r"[^\w\- ]", "", heading.lower()).replace("_", "").replace(" ", "-")


def dr(d):
    v = d["domain_rating"]
    return "—" if v is None else (f"**{v}**" if v >= 70 else str(v))


def link(d):
    return {"Dofollow": "✅ Dofollow", "Nofollow": "❌ Nofollow"}.get(d["link_type"], "—")


def cell(s):
    return (s or "—").replace("|", "/").replace("\n", " ")


def row(d, with_cat=False, n=None, cut=None):
    desc = d["description"] or ""
    if cut and len(desc) > cut:
        desc = desc[: cut - 3] + "..."
    name = d["name"].replace("|", "/").replace("[", "(").replace("]", ")")
    parts = ([str(n)] if n else []) + [f"[{name}]({d['url']})", dr(d), link(d), cell(d["pricing"])]
    if with_cat:
        parts.append(d["category"])
    parts.append(cell(desc))
    return "| " + " | ".join(parts) + " |"


def main():
    dirs = json.loads(DATA.read_text(encoding="utf-8"))
    dirs.sort(key=by_dr)
    DATA.write_text(json.dumps(dirs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\r\n")

    total = len(dirs)
    with_dr = sum(d["domain_rating"] is not None for d in dirs)
    dofollow = sum(d["link_type"] == "Dofollow" for d in dirs)
    nofollow = sum(d["link_type"] == "Nofollow" for d in dirs)
    free = sum(d["pricing"] in ("Free", "Freemium") for d in dirs)
    count = {}
    for d in dirs:
        count[d["category"]] = count.get(d["category"], 0) + 1
    cats = sorted(count, key=lambda c: -count[c])

    out = ["## 📊 Overview", "", '<div align="center">', "", "| | Count |", "|---|------:|"]
    out += [
        f"| 📁 Total directories | **{total}** |",
        f"| 📈 With Domain Rating data | **{with_dr}** |",
        f"| ✅ Dofollow backlinks | **{dofollow}** |",
        f"| ❌ Nofollow backlinks | **{nofollow}** |",
        f"| 🆓 Free or Freemium | **{free}** |",
        "", "</div>", "", "### Distribution", "", "| Category | Count | |", "|----------|------:|---|",
    ]
    top = max(count.values())
    out += [f"| {c} | {count[c]} | {'█' * max(1, round(count[c] / top * 42))} |" for c in cats]
    out += ["", "&nbsp;", "", "## 🏆 Top 20 Highest Authority Directories", "", "Start here. These give the most SEO value.", ""]
    out += ["| # | Directory | DR | Link Type | Pricing | Category | Description |", "|:-:|-----------|:--:|-----------|:-------:|----------|-------------|"]
    out += [row(d, with_cat=True, n=i + 1, cut=120) for i, d in enumerate(dirs[:20])]
    out += ["", "&nbsp;", "", "## 📂 Browse by Category", "", "Jump to a category:", ""]
    out += ["> " + " · ".join(f"{c.split(' ')[0]} [{LABELS.get(c, c.split(' ', 1)[1])}]({anchor(f'{c} ({count[c]})')})" for c in cats)]
    out += ["", "---", "", ""]
    for c in cats:
        items = [d for d in dirs if d["category"] == c]
        rated = [d["domain_rating"] for d in items if d["domain_rating"] is not None]
        df = sum(d["link_type"] == "Dofollow" for d in items)
        stats = " · ".join(([f"Top DR: **{max(rated)}**"] if rated else []) + ([f"Dofollow: **{df}**"] if df else []))
        out += [f"### {c} ({len(items)})", ""] + ([stats, ""] if stats else []) + [HEAD] + [row(d) for d in items[:10]]
        if len(items) > 10:
            out += ["", "<details>", f"<summary>View all {len(items)} directories</summary>", "", HEAD] + [row(d) for d in items] + ["", "</details>"]
        out += ["", ""]
    out += ["&nbsp;", ""]

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    start = readme.index("## 📊 Overview")
    end = readme.index("## 💡 Submission Strategy")
    readme = readme[:start] + "\n".join(out) + "\n" + readme[end:]
    readme = re.sub(r"### \d+\+ directories to submit", f"### {total // 10 * 10}+ directories to submit", readme)
    readme = re.sub(r"badge/Directories-\d+-", f"badge/Directories-{total}-", readme)
    readme = re.sub(r"badge/With_DR_Data-\d+-", f"badge/With_DR_Data-{with_dr}-", readme)
    readme = re.sub(r"badge/Dofollow-\d+-", f"badge/Dofollow-{dofollow}-", readme)
    readme_path.write_text(readme, encoding="utf-8", newline="\n")

    with open(ROOT / "data" / "directories.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["name", "url", "domain_rating", "link_type", "pricing", "category", "description"])
        for d in dirs:
            w.writerow([d["name"], d["url"], "" if d["domain_rating"] is None else d["domain_rating"], d["link_type"] or "", d["pricing"] or "", d["category"], d["description"] or ""])
    print(f"{total} directories, {len(cats)} categories")


if __name__ == "__main__":
    main()
