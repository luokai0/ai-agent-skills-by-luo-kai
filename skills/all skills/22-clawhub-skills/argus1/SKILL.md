---
name: argus
description: "Argus — The Hundred-Eyed. Scan your Python or JavaScript codebase for bugs, security vulnerabilities, code smells, and common anti-patterns — get a prioritised fix list with line numbers, severity ratings, and suggested corrections for every issue found. Nothing escapes Argus."
version: "1.0.0"
metadata:
  openclaw:
    requires:
      env: []
      bins: [python3, pip3]
    primaryEnv: "SOURCE_PATH"
    homepage: https://clawhub.ai/skills/argus
    emoji: "👁️"
    tags: [code, bugs, security, scanner, python, javascript, argus, debugging, linting]
    envVars:
      - name: SOURCE_PATH
        description: "File or directory to scan"
        required: true
      - name: LANGUAGE
        description: "Language to scan: python / javascript / auto"
        required: false
        default: "auto"
      - name: SEVERITY_FILTER
        description: "Minimum severity to show: critical / high / medium / all"
        required: false
        default: "all"
---

# 🐛 👁️ Argus — Code Intelligence Scanner

Static analysis for your codebase — finds real bugs, security holes, and code smells before
they hit production. No external API needed. Works on Python and JavaScript files.

**What you get:**
- Hardcoded passwords, API keys, and tokens flagged as Critical
- SQL injection and prototype pollution detection
- Bare excepts, mutable defaults, wildcard imports, and 13 other patterns
- Severity-filtered output: focus on Critical first, drill down from there
- `bug_report_[DATE].md` + `bug_report_[DATE].json` with full fix suggestions

## Quick Start
```bash
SOURCE_PATH="./src" LANGUAGE="python" SEVERITY_FILTER="high" python skill.py
```

## Security
Reads local files only. Nothing transmitted.

---

## Step 1 — Install dependencies
```python
import subprocess, sys
subprocess.run([sys.executable,"-m","pip","install","rich","--break-system-packages","--quiet"], check=True)
```

## Step 2 — Scan for Bugs
```python
import os, re, json
from pathlib import Path
from datetime import date
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()
SRC_PATH   = os.environ.get("SOURCE_PATH", ".")
LANGUAGE   = os.environ.get("LANGUAGE", "auto").lower()
SEV_FILTER = os.environ.get("SEVERITY_FILTER", "all").lower()
TODAY      = date.today()

src = Path(SRC_PATH)
if not src.exists():
    console.print(Panel(f"[red]Path not found: {SRC_PATH}[/red]", border_style="red")); raise SystemExit(1)

console.print(Panel.fit(f"[bold red]🐛 👁️ Argus — Code Intelligence Scanner[/bold red]\nScanning: [cyan]{SRC_PATH}[/cyan]  |  Language: [yellow]{LANGUAGE}[/yellow]  |  Filter: [green]{SEV_FILTER}[/green]", border_style="red"))

# Detect language
def detect_lang(path: Path) -> str:
    py = len(list(path.rglob("*.py") if path.is_dir() else [path] if str(path).endswith(".py") else []))
    js = len(list(path.rglob("*.js") if path.is_dir() else [path] if str(path).endswith(".js") else []))
    if py == 0 and js == 0:
        return "python"  # default; user can override with LANGUAGE env var
    return "python" if py >= js else "javascript"

lang = LANGUAGE if LANGUAGE != "auto" else detect_lang(src)

# Bug patterns
PYTHON_RULES = [
    ("PY001", "critical", "security",  r"eval\s*\(",              "eval() is dangerous — executes arbitrary code", "Use ast.literal_eval() for safe parsing"),
    ("PY002", "critical", "security",  r"exec\s*\(",              "exec() executes arbitrary strings", "Refactor to avoid dynamic code execution"),
    ("PY003", "critical", "security",  r'password\s*=\s*["\'][^"\']{3,}', "Hardcoded password", "Use environment variables: os.environ.get('PASSWORD')"),
    ("PY004", "high",     "security",  r"pickle\.loads?\(",       "pickle.load is unsafe with untrusted data", "Use json.loads() for safe deserialization"),
    ("PY005", "high",     "bug",       r"except\s*:",              "Bare except catches ALL exceptions including KeyboardInterrupt", "Use except Exception: or catch specific exception types"),
    ("PY006", "high",     "bug",       r"==\s*None|None\s*==",    "Use 'is None' not '== None' — can produce unexpected results", "Replace == None with is None"),
    ("PY007", "medium",   "bug",       r"def\s+\w+\(.*=\[\]", "Mutable default argument — shared across calls", "Use None as default: def f(x=None): x = x or []"),
    ("PY008", "medium",   "security",  r"shell\s*=\s*True",       "subprocess with shell=True is a command injection risk", "Use shell=False and pass args as a list"),
    ("PY009", "medium",   "smell",     r"import \*",               "Wildcard import pollutes namespace and hides dependencies", "Import only what you need: from module import func"),
    ("PY010", "low",      "smell",     r"print\s*\(",             "print() left in code — likely debug statement", "Use logging module instead of print for production code"),
    ("PY011", "critical", "security",  r"(?i)(api_key|api_secret|secret_key|access_token|auth_token)\s*=\s*[\x27\x22][^\x27\x22]{8,}", "Hardcoded API key or token", "Store in environment variable: os.environ.get('API_KEY')"),
    ("PY012", "high",     "security",  r"execute\s*\(.*%.*\)|execute\s*\(.*\.format\(|execute\s*\(.*f[\x22\x27]", "Possible SQL injection via string formatting", "Use parameterised queries: cursor.execute(sql, (value,))"),
    ("PY013", "medium",   "security",  r"open\s*\((?![^)\n]*\bencoding)[^)\n]*[\x27\x22]w[\x27\x22]", "File opened for write without encoding", "Add encoding='utf-8': open(path, 'w', encoding='utf-8')"),
]
JS_RULES = [
    ("JS001", "critical", "security",  r"eval\s*\(",              "eval() executes arbitrary code", "Remove eval — refactor logic"),
    ("JS002", "critical", "security",  r"innerHTML\s*=",           "innerHTML is an XSS vector if it contains user input", "Use textContent or sanitize input first"),
    ("JS003", "high",     "bug",       r"==\s*null|null\s*==",    "Use === null for strict equality check", "Replace == null with === null"),
    ("JS004", "high",     "bug",       r"catch\s*\(\s*\)",      "Empty catch silently swallows errors", "Log the error: catch(e) { console.error(e); }"),
    ("JS005", "medium",   "bug",       r"var\s+",                  "var has function scope and hoisting issues", "Use const or let instead of var"),
    ("JS006", "medium",   "security",  r"localStorage\.setItem.*password", "Storing passwords in localStorage is insecure", "Never store credentials in localStorage"),
    ("JS007", "critical", "security",  r"(?i)(api_key|apikey|api_secret|access_token|auth_token)\s*[:=]\s*[\x27\x22][^\x27\x22]{8,}", "Hardcoded API key or token", "Use environment variable: process.env.API_KEY"),
    ("JS008", "high",     "security",  r"__proto__|constructor\.prototype", "Prototype pollution vulnerability", "Validate input keys; use Object.create(null) for safe maps"),
    ("JS009", "high",     "security",  r"\$\{.*\}.*query|query.*\$\{|db\.query\s*\(", "Possible SQL/NoSQL injection via template literal", "Use parameterised queries or an ORM"),
]
RULES = PYTHON_RULES if lang == "python" else JS_RULES
SEV_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
SEV_SHOW  = {"all": 4, "medium": 2, "high": 1, "critical": 0}.get(SEV_FILTER, 4)

# Get files
ext = "*.py" if lang == "python" else "*.js"
files = list(src.rglob(ext) if src.is_dir() else [src])
files = [f for f in files if ".git" not in str(f) and "node_modules" not in str(f) and "venv" not in str(f)][:50]
console.print(f"[dim]Scanning {len(files)} {lang} files…[/dim]")

# Scan
findings = []
for fpath in files:
    try:
        lines = fpath.read_text(encoding="utf-8", errors="ignore").splitlines()
        for i, line in enumerate(lines, 1):
            for rule_id, sev, category, pattern, message, fix in RULES:
                if SEV_ORDER.get(sev, 3) <= SEV_SHOW and re.search(pattern, line):
                    findings.append({"id": rule_id, "severity": sev, "category": category,
                                     "file": str(fpath.relative_to(src) if src.is_dir() else fpath),
                                     "line": i, "code": line.strip()[:80], "message": message, "fix": fix})
    except Exception: pass

# Dedupe and sort
seen = set(); unique = []
for f in findings:
    key = (f["id"], f["file"], f["line"])
    if key not in seen: seen.add(key); unique.append(f)
unique.sort(key=lambda x: (SEV_ORDER.get(x["severity"],3), x["file"], x["line"]))

# Stats
from collections import Counter
sev_counts = Counter(f["severity"] for f in unique)
cat_counts = Counter(f["category"] for f in unique)

console.print()
console.print(Panel(
    f"Files scanned: [cyan]{len(files)}[/cyan]  |  Issues found: [bold]{len(unique)}[/bold]\n"
    f"[red]Critical: {sev_counts['critical']}[/red]  [yellow]High: {sev_counts['high']}[/yellow]  [blue]Medium: {sev_counts['medium']}[/blue]  [dim]Low: {sev_counts['low']}[/dim]\n"
    f"Security: {cat_counts['security']}  |  Bugs: {cat_counts['bug']}  |  Smells: {cat_counts['smell']}",
    title="[bold]📊 Scan Summary[/bold]", border_style="red" if sev_counts["critical"] > 0 else "yellow"
))

if unique:
    console.print()
    display_count = min(len(unique), 25)
    title_suffix = f" — showing {display_count} of {len(unique)}" if len(unique) > 25 else ""
    t = Table(title=f"🐛 Issues Found ({len(unique)}){title_suffix}", box=box.ROUNDED, show_lines=True, border_style="red")
    t.add_column("ID", width=7, style="dim"); t.add_column("Sev", width=10); t.add_column("File:Line", style="cyan", width=28)
    t.add_column("Issue", style="white", width=35); t.add_column("Fix", style="green", width=40)
    SEV_COLOR = {"critical":"bold red","high":"yellow","medium":"blue","low":"dim"}
    for f in unique[:25]:
        col = SEV_COLOR.get(f["severity"],"white")
        t.add_row(f["id"], f"[{col}]{f['severity']}[/{col}]", f"{f['file'][:22]}:{f['line']}", f["message"][:35], f["fix"][:40])
    console.print(t)
else:
    console.print(Panel("[green]✅ No issues found matching your filter criteria![/green]", border_style="green"))

# Save
out_path = f"bug_report_{TODAY}.json"
with open(out_path,"w", encoding="utf-8") as f:
    json.dump({"scanned_files": len(files), "language": lang, "findings": unique, "generated": str(TODAY)}, f, indent=2)
md_path = f"bug_report_{TODAY}.md"
with open(md_path,"w", encoding="utf-8") as f:
    f.write(f"# Bug Hunt Report — {TODAY}\n\n**Files:** {len(files)}  |  **Issues:** {len(unique)}\n\n")
    f.write("| ID | Severity | File:Line | Issue | Fix |\n|-----|---------|-----------|-------|-----|\n")
    for fi in unique: f.write(f"| {fi['id']} | {fi['severity']} | {fi['file'][:25]}:{fi['line']} | {fi['message'][:40]} | {fi['fix'][:40]} |\n")

console.print()
console.print(Panel(f"[bold green]✅ Scan complete![/bold green]\n\n📄 [cyan]{md_path}[/cyan]\n📄 [cyan]{out_path}[/cyan]\n\n[bold]What to do next:[/bold]\n1. [yellow]Fix Critical issues first[/yellow] — security and crash bugs\n2. [yellow]Fix High severity next[/yellow] — these will cause real problems\n3. [yellow]Run again after fixes[/yellow] to confirm clean\n4. [yellow]Add to CI/CD pipeline[/yellow] so every commit is scanned",title="[bold red]🐛 👁️ Argus — Code Intelligence Scanner — Done[/bold red]",border_style="red"))
```