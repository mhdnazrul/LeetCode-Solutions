import os
import re

def get_problems():
    problems = []
    base = "Solutions"
    for folder in sorted(os.listdir(base)):
        path = os.path.join(base, folder)
        if os.path.isdir(path):
            parts = folder.split('-', 1)
            pid = parts[0]
            slug = parts[1] if len(parts) > 1 else ""
            title = slug.replace('-', ' ').title()
            
            files = os.listdir(path)
            sol_file = next((f for f in files if f.endswith(('.cpp', '.py', '.java'))), None)
            if not sol_file:
                continue
                
            ext = sol_file.split('.')[-1]
            lang = {'cpp': 'C++', 'py': 'Python', 'java': 'Java'}.get(ext, ext.upper())
            
            sol_link = f"./Solutions/{folder}/{sol_file}"
            lc_link = f"https://leetcode.com/problems/{slug}/"
            
            problems.append((pid, title, lc_link, lang, sol_link))
    return problems

def main():
    problems = get_problems()
    total = len(problems)
    
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Update total
    content = re.sub(r'Total Problems Solved: \d+', f'Total Problems Solved: {total}', content)
    
    # Generate table
    table = "| #    | Problem Name             | LeetCode Link                          | Language | Solution |\n"
    table += "|------|--------------------------|----------------------------------------|----------|----------|\n"
    for p in problems:
        table += f"| {p[0]} | {p[1]} | [Link]({p[2]}) | {p[3]} | [View]({p[4]}) |\n"
    
    # Replace table between markers
    content = re.sub(
        r'(<!-- SOLUTIONS_TABLE_START -->)(.*?)(<!-- SOLUTIONS_TABLE_END -->)',
        r'\1\n' + table + r'\n\3',
        content,
        flags=re.DOTALL
    )
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ Updated README with {total} problems")

if __name__ == "__main__":
    main()