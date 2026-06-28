"""
LeetCode Solution Archive Generator
====================================
Scans Solutions/ (LeetSync format: {id}-{slug}/{slug}.ext + README.md)
→ Extracts difficulty from per-problem README.md badge
→ Generates Web/solutions.json
→ Rewrites root README.md with updated stats + table
"""

import os
import json
import re

SOLUTIONS_DIR = "Solutions"
WEB_DIR = "Web"
EXTENSIONS = {".cpp", ".c", ".py", ".java", ".js", ".ts", ".kt", ".cs", ".go", ".rs"}

REPO_OWNER = "mhdnazrul"
REPO_NAME = "LeetCode-Solutions"
REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
LEETCODE_BASE = "https://leetcode.com/problems"

DIFFICULTY_COLORS = {
    "Easy": "brightgreen",
    "Medium": "orange",
    "Hard": "red",
}


def extract_difficulty(problem_dir: str) -> str:
    """
    LeetSync creates a README.md in each problem folder with a shields.io badge:
      <img src='https://img.shields.io/badge/Difficulty-Easy-brightgreen' ...>
    We parse this to extract the difficulty level.
    """
    readme_path = os.path.join(problem_dir, "README.md")
    if not os.path.isfile(readme_path):
        return "Unknown"
    try:
        with open(readme_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        match = re.search(
            r"Difficulty-(\w+)-(?:brightgreen|orange|red|yellow|blue)",
            content,
            re.IGNORECASE,
        )
        if match:
            diff = match.group(1).capitalize()
            if diff in ("Easy", "Medium", "Hard"):
                return diff
        # Fallback: look for text like "Difficulty: Easy"
        match2 = re.search(r"Difficulty[:\s]+([EMH]\w+)", content, re.IGNORECASE)
        if match2:
            diff = match2.group(1).capitalize()
            if diff in ("Easy", "Medium", "Hard"):
                return diff
    except Exception:
        pass
    return "Unknown"


def detect_language(files: list) -> str:
    """Return the display language name for the first recognized solution file."""
    ext_map = {
        ".cpp": "C++",
        ".c": "C",
        ".py": "Python",
        ".java": "Java",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".kt": "Kotlin",
        ".cs": "C#",
        ".go": "Go",
        ".rs": "Rust",
    }
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in ext_map:
            return ext_map[ext]
    return "Unknown"


def find_solution_file(files: list) -> str | None:
    """Return the first recognized solution source file."""
    for f in sorted(files):
        ext = os.path.splitext(f)[1].lower()
        if ext in EXTENSIONS:
            return f
    return None


def process_solutions() -> list:
    """Walk Solutions/ and collect metadata for each problem."""
    problems = []

    if not os.path.isdir(SOLUTIONS_DIR):
        print(f"⚠️  '{SOLUTIONS_DIR}' directory not found.")
        return problems

    for folder in sorted(os.listdir(SOLUTIONS_DIR)):
        folder_path = os.path.join(SOLUTIONS_DIR, folder)
        if not os.path.isdir(folder_path):
            continue

        # LeetSync naming: {id}-{slug}  e.g. "1-two-sum" or "4179-largest-even-number"
        parts = folder.split("-", 1)
        if len(parts) < 2:
            continue
        problem_id_str = parts[0]
        slug = parts[1]  # e.g. "two-sum"

        if not problem_id_str.isdigit():
            continue
        problem_id = int(problem_id_str)

        # Derive title from slug
        title = slug.replace("-", " ").title()

        # Enumerate files in problem folder
        try:
            files = os.listdir(folder_path)
        except Exception:
            continue

        sol_file = find_solution_file(files)
        if not sol_file:
            continue

        language = detect_language(files)
        difficulty = extract_difficulty(folder_path)

        rel_path = f"{SOLUTIONS_DIR}/{folder}/{sol_file}".replace("\\", "/")

        problems.append(
            {
                "id": problem_id,
                "id_str": problem_id_str.zfill(4),  # zero-padded for sorting
                "name": title,
                "slug": slug,
                "difficulty": difficulty,
                "language": language,
                "path": rel_path,
                "folder": folder,
                "lc_link": f"{LEETCODE_BASE}/{slug}/",
                "sol_link": f"{REPO_URL}/blob/main/{rel_path}",
            }
        )

    # Sort numerically by problem ID
    problems.sort(key=lambda p: p["id"])
    return problems


def write_solutions_json(problems: list):
    """Write Web/solutions.json for the website."""
    os.makedirs(WEB_DIR, exist_ok=True)
    out_path = os.path.join(WEB_DIR, "solutions.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(problems, f, indent=2, ensure_ascii=False)
    print(f"✅ solutions.json → {len(problems)} problems written to {out_path}")


def build_readme(problems: list) -> str:
    """Generate the full README.md content."""
    total = len(problems)
    easy = sum(1 for p in problems if p["difficulty"] == "Easy")
    medium = sum(1 for p in problems if p["difficulty"] == "Medium")
    hard = sum(1 for p in problems if p["difficulty"] == "Hard")

    langs: dict = {}
    for p in problems:
        langs[p["language"]] = langs.get(p["language"], 0) + 1
    lang_badge = "%20%7C%20".join(sorted(langs.keys()))

    pages_url = f"https://{REPO_OWNER}.github.io/{REPO_NAME}/"

    header = f"""\
<h1 align="center">🚀 LeetCode Solutions</h1>

<p align="center">
  <a href="{pages_url}">
    <img src="https://img.shields.io/badge/🌐 View_Website-Click_Here-2ecc71?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Language-{lang_badge}-blue?style=for-the-badge&logo=cplusplus" alt="Languages">
  <img src="https://img.shields.io/badge/Total%20Solved-{total}-00b894?style=for-the-badge&logo=leetcode" alt="Total">
  <img src="https://img.shields.io/github/stars/{REPO_OWNER}/{REPO_NAME}?style=for-the-badge&logo=github" alt="Stars">
  <a href="https://leetcode.com/{REPO_OWNER}/">
    <img src="https://img.shields.io/badge/LeetCode-{REPO_OWNER}-FFA116?style=for-the-badge&logo=leetcode&logoColor=white" alt="LeetCode">
  </a>
</p>

<p align="center">
  <b>🔗 Find me on:</b>
  <a href="https://github.com/{REPO_OWNER}">GitHub</a> |
  <a href="https://leetcode.com/{REPO_OWNER}/">LeetCode</a> |
  <a href="https://www.linkedin.com/in/nazrulislam7/">LinkedIn</a>
</p>

---
"""

    stats = f"""\
## 📊 Progress Statistics

<!-- STATS_START -->
**Total Problems Solved:** {total}

| Difficulty | Count | Progress |
|:-----------|:-----:|:--------:|
| 🟢 Easy   | {easy} | {"█" * easy}{"░" * max(0, 10 - easy)} |
| 🟡 Medium | {medium} | {"█" * medium}{"░" * max(0, 10 - medium)} |
| 🔴 Hard   | {hard} | {"█" * hard}{"░" * max(0, 10 - hard)} |

<details><summary><b>📈 Language Breakdown</b></summary>

| Language | Count |
|:---------|:-----:|
"""
    for lang, cnt in sorted(langs.items(), key=lambda x: -x[1]):
        stats += f"| {lang} | {cnt} |\n"

    stats += """
</details>
<!-- STATS_END -->

---
"""

    table_rows = ""
    for p in problems:
        diff_emoji = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}.get(
            p["difficulty"], "⚪"
        )
        table_rows += (
            f"| {p['id']} | {p['name']} | {diff_emoji} {p['difficulty']} "
            f"| {p['language']} "
            f"| [🔗 Problem]({p['lc_link']}) "
            f"| [💻 Solution]({p['sol_link']}) |\n"
        )

    solution_index = f"""\
## 📋 Solution Index

<!-- SOLUTIONS_TABLE_START -->
| # | Problem Name | Difficulty | Language | Problem | Solution |
|:--|:-------------|:----------:|:--------:|:-------:|:--------:|
{table_rows}
<!-- SOLUTIONS_TABLE_END -->

---
"""

    how_it_works = f"""\
## 🔄 How It Works

1. **Solve & Submit** on LeetCode → Accepted ✅
2. **LeetSync** Chrome extension automatically pushes the solution to this repo
3. **GitHub Actions** runs `Web/generate.py` on every push to `main`
4. The script:
   - Scans `Solutions/` directory (LeetSync format: `{{id}}-{{slug}}/`)
   - Extracts **difficulty** from each problem's `README.md` shield badge
   - Writes `Web/solutions.json` for the website
   - Rewrites this `README.md` with updated stats + table
5. The `Web/` folder is **deployed to GitHub Pages** automatically

---

## 📂 Repository Structure

```
{REPO_NAME}/
├── .github/workflows/
│   └── automation.yml          ← GitHub Actions workflow
├── Solutions/                  ← Auto-created by LeetSync
│   ├── 1-two-sum/
│   │   ├── two-sum.cpp
│   │   └── README.md           ← Contains difficulty badge
│   └── ...
├── Web/
│   ├── generate.py             ← 🤖 Automation script
│   ├── index.html              ← Website SPA
│   ├── style.css
│   ├── script.js
│   └── solutions.json          ← Auto-generated data
├── README.md                   ← Auto-updated by automation
└── .gitignore
```

---

## 📄 License

This project is licensed under the **MIT License**.

---

<p align="center">
  <b>⭐ Star this repo</b> if it helps your journey! Happy Coding! 💻<br>
  <i>Auto-generated by <a href="Web/generate.py">Web/generate.py</a></i>
</p>
"""

    return header + stats + solution_index + how_it_works


def update_readme(problems: list):
    """Rewrite README.md with updated content."""
    content = build_readme(problems)
    with open("README.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"✅ README.md updated with {len(problems)} problems")


def main():
    print("🔍 Scanning Solutions directory...")
    problems = process_solutions()
    print(f"📦 Found {len(problems)} solved problems")

    write_solutions_json(problems)
    update_readme(problems)

    total = len(problems)
    easy = sum(1 for p in problems if p["difficulty"] == "Easy")
    medium = sum(1 for p in problems if p["difficulty"] == "Medium")
    hard = sum(1 for p in problems if p["difficulty"] == "Hard")

    print(f"""
📊 Stats Summary:
   Total  : {total}
   Easy   : {easy}
   Medium : {medium}
   Hard   : {hard}
""")


if __name__ == "__main__":
    main()
