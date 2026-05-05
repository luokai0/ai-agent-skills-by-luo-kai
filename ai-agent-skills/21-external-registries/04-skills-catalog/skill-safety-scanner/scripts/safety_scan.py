#!/usr/bin/env python3
"""
Agent Skills Safety Scanner

Local safety scanner for Agent Skills. Detects:
- Hardcoded secrets (API keys, tokens, credentials)
- Dangerous code patterns (eval, exec, command injection)
- Required permissions (filesystem, network, subprocess)

Produces grades matching the skillscatalog.ai web scanner.
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ============================================================================
# Types and Data Classes
# ============================================================================

@dataclass
class Finding:
    dimension: str  # "secret", "dangerous_code", "permission"
    severity: str   # "critical", "high", "medium", "low", "info"
    title: str
    description: str
    file_path: str
    line_number: int
    code_snippet: str = ""
    rule_id: str = ""


@dataclass
class ScanResult:
    skill_name: str
    grade: str
    score: int
    secret_score: int
    dangerous_code_score: int
    permissions: list = field(default_factory=list)
    findings: list = field(default_factory=list)


# ============================================================================
# Secret Detection Patterns (from gitleaks.ts)
# ============================================================================

SECRET_PATTERNS = [
    # API Keys
    {
        "id": "aws-access-key",
        "name": "AWS Access Key",
        "pattern": r"\bAKIA[0-9A-Z]{16}\b",
        "severity": "critical",
    },
    {
        "id": "aws-secret-key",
        "name": "AWS Secret Key",
        "pattern": r"\b[A-Za-z0-9/+=]{40}\b(?=.*(?:aws|secret|key))",
        "severity": "critical",
        "flags": re.IGNORECASE,
    },
    {
        "id": "github-token",
        "name": "GitHub Token",
        "pattern": r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b",
        "severity": "critical",
    },
    {
        "id": "openai-api-key",
        "name": "OpenAI API Key",
        "pattern": r"\bsk-[A-Za-z0-9]{20,}T3BlbkFJ[A-Za-z0-9]{20,}\b",
        "severity": "critical",
    },
    {
        "id": "anthropic-api-key",
        "name": "Anthropic API Key",
        "pattern": r"\bsk-ant-[A-Za-z0-9-]{80,}\b",
        "severity": "critical",
    },
    {
        "id": "stripe-api-key",
        "name": "Stripe API Key",
        "pattern": r"\b(sk|pk)_(test|live)_[A-Za-z0-9]{24,}\b",
        "severity": "critical",
    },
    {
        "id": "slack-token",
        "name": "Slack Token",
        "pattern": r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b",
        "severity": "critical",
    },
    {
        "id": "slack-webhook",
        "name": "Slack Webhook",
        "pattern": r"https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+",
        "severity": "high",
    },
    {
        "id": "google-api-key",
        "name": "Google API Key",
        "pattern": r"\bAIza[A-Za-z0-9_-]{35}\b",
        "severity": "high",
    },
    {
        "id": "firebase-key",
        "name": "Firebase Key",
        "pattern": r"\bAAAA[A-Za-z0-9_-]{140,}\b",
        "severity": "high",
    },
    {
        "id": "npm-token",
        "name": "npm Token",
        "pattern": r"\bnpm_[A-Za-z0-9]{36}\b",
        "severity": "critical",
    },
    {
        "id": "pypi-token",
        "name": "PyPI Token",
        "pattern": r"\bpypi-[A-Za-z0-9]{100,}\b",
        "severity": "critical",
    },
    {
        "id": "jwt-token",
        "name": "JWT Token",
        "pattern": r"\beyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]+\b",
        "severity": "medium",
    },
    # Private Keys
    {
        "id": "private-key",
        "name": "Private Key",
        "pattern": r"-----BEGIN (RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY( BLOCK)?-----",
        "severity": "critical",
    },
    # Generic secrets
    {
        "id": "generic-password",
        "name": "Hardcoded Password",
        "pattern": r"(?:password|passwd|pwd)\s*[:=]\s*[\"'][^\"']{8,}[\"']",
        "severity": "high",
        "flags": re.IGNORECASE,
    },
    {
        "id": "generic-secret",
        "name": "Hardcoded Secret",
        "pattern": r"(?:secret|api_key|apikey|auth_token|authtoken|access_token)\s*[:=]\s*[\"'][^\"']{10,}[\"']",
        "severity": "high",
        "flags": re.IGNORECASE,
    },
    {
        "id": "connection-string",
        "name": "Database Connection String",
        "pattern": r"(?:mongodb|postgres|mysql|redis)://[^\s\"']+:[^\s\"']+@[^\s\"']+",
        "severity": "critical",
        "flags": re.IGNORECASE,
    },
    {
        "id": "bearer-token",
        "name": "Bearer Token",
        "pattern": r"\bBearer\s+[A-Za-z0-9_-]{20,}\b",
        "severity": "medium",
    },
]

# Files to skip (too many false positives)
SKIP_FILES = [
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    ".min.js",
    ".min.css",
]

# Sensitive file names (increase severity)
SENSITIVE_FILES = [
    ".env",
    ".env.local",
    ".env.production",
    "credentials",
    "secrets",
    "config.json",
    "settings.json",
]

# ============================================================================
# Dangerous Code Patterns (from semgrep.ts)
# ============================================================================

CODE_PATTERNS = [
    # JavaScript/TypeScript patterns
    {
        "id": "js-eval",
        "name": "Use of eval()",
        "description": "eval() can execute arbitrary code and is a major security risk",
        "pattern": r"\beval\s*\(",
        "severity": "critical",
        "languages": ["javascript", "typescript"],
        "recommendation": "Use JSON.parse() for JSON data or find an alternative approach",
    },
    {
        "id": "js-function-constructor",
        "name": "Use of Function constructor",
        "description": "new Function() is equivalent to eval() and can execute arbitrary code",
        "pattern": r"\bnew\s+Function\s*\(",
        "severity": "critical",
        "languages": ["javascript", "typescript"],
        "recommendation": "Avoid dynamic code generation; use static functions instead",
    },
    {
        "id": "js-exec-sync",
        "name": "Synchronous command execution",
        "description": "execSync can execute shell commands; ensure input is properly sanitized",
        "pattern": r"\bexecSync\s*\(",
        "severity": "high",
        "languages": ["javascript", "typescript"],
        "recommendation": "Use execFile() with explicit arguments instead of exec()",
    },
    {
        "id": "js-child-process",
        "name": "Child process spawn with shell",
        "description": "Spawning child processes with shell=true is dangerous",
        "pattern": r"spawn\s*\([^)]*,\s*\{[^}]*shell\s*:\s*true",
        "severity": "high",
        "languages": ["javascript", "typescript"],
        "recommendation": "Use spawn() without shell:true and pass arguments as array",
    },
    {
        "id": "js-innerhtml",
        "name": "Use of innerHTML",
        "description": "innerHTML can lead to XSS if used with untrusted input",
        "pattern": r"\.innerHTML\s*=",
        "severity": "medium",
        "languages": ["javascript", "typescript"],
        "recommendation": "Use textContent for text, or sanitize HTML with DOMPurify",
    },
    {
        "id": "js-dangerously-set-innerhtml",
        "name": "Use of dangerouslySetInnerHTML",
        "description": "React's dangerouslySetInnerHTML can lead to XSS attacks",
        "pattern": r"dangerouslySetInnerHTML\s*=\s*\{\s*\{\s*__html\s*:",
        "severity": "high",
        "languages": ["javascript", "typescript"],
        "recommendation": "Avoid dangerouslySetInnerHTML; use sanitization if necessary",
    },
    {
        "id": "js-document-write",
        "name": "Use of document.write",
        "description": "document.write can be exploited for XSS attacks",
        "pattern": r"document\.write\s*\(",
        "severity": "medium",
        "languages": ["javascript", "typescript"],
        "recommendation": "Use DOM manipulation methods instead",
    },
    {
        "id": "js-sql-concat",
        "name": "SQL string concatenation",
        "description": "String concatenation in SQL queries can lead to SQL injection",
        "pattern": r"(?:SELECT|INSERT|UPDATE|DELETE|FROM|WHERE).*[\"'`]\s*\+",
        "severity": "critical",
        "languages": ["javascript", "typescript"],
        "flags": re.IGNORECASE,
        "recommendation": "Use parameterized queries or an ORM",
    },
    # Python patterns
    {
        "id": "py-eval",
        "name": "Use of eval()",
        "description": "eval() can execute arbitrary Python code",
        "pattern": r"\beval\s*\(",
        "severity": "critical",
        "languages": ["python"],
        "recommendation": "Use ast.literal_eval() for literals or find an alternative",
    },
    {
        "id": "py-exec",
        "name": "Use of exec()",
        "description": "exec() can execute arbitrary Python code",
        "pattern": r"\bexec\s*\(",
        "severity": "critical",
        "languages": ["python"],
        "recommendation": "Avoid exec(); use explicit function calls instead",
    },
    {
        "id": "py-subprocess-shell",
        "name": "Subprocess with shell=True",
        "description": "subprocess with shell=True is vulnerable to command injection",
        "pattern": r"subprocess\.\w+\s*\([^)]*shell\s*=\s*True",
        "severity": "critical",
        "languages": ["python"],
        "recommendation": "Use subprocess.run() with a list of arguments, shell=False",
    },
    {
        "id": "py-os-system",
        "name": "Use of os.system()",
        "description": "os.system() is vulnerable to command injection",
        "pattern": r"os\.system\s*\(",
        "severity": "high",
        "languages": ["python"],
        "recommendation": "Use subprocess.run() with explicit arguments",
    },
    {
        "id": "py-pickle",
        "name": "Use of pickle",
        "description": "pickle can execute arbitrary code when loading untrusted data",
        "pattern": r"pickle\.load|pickle\.loads|cPickle\.load",
        "severity": "high",
        "languages": ["python"],
        "recommendation": "Use JSON or another safe serialization format for untrusted data",
    },
    {
        "id": "py-yaml-load",
        "name": "Unsafe YAML loading",
        "description": "yaml.load() without Loader can execute arbitrary code",
        "pattern": r"yaml\.load\s*\([^)]*(?!Loader)",
        "severity": "high",
        "languages": ["python"],
        "recommendation": "Use yaml.safe_load() or specify Loader=yaml.SafeLoader",
    },
    {
        "id": "py-sql-format",
        "name": "SQL string formatting",
        "description": "String formatting in SQL queries can lead to SQL injection",
        "pattern": r"(?:execute|cursor\.execute)\s*\([^)]*%|(?:execute|cursor\.execute)\s*\([^)]*\.format\(",
        "severity": "critical",
        "languages": ["python"],
        "recommendation": "Use parameterized queries with placeholders",
    },
    # Shell patterns
    {
        "id": "sh-eval",
        "name": "Use of eval in shell",
        "description": "eval in shell scripts can execute arbitrary commands",
        "pattern": r"\beval\s+",
        "severity": "critical",
        "languages": ["shell"],
        "recommendation": "Avoid eval; use explicit commands",
    },
    {
        "id": "sh-unquoted-var",
        "name": "Unquoted variable expansion",
        "description": "Unquoted variables can lead to word splitting and globbing issues",
        "pattern": r"\$\w+(?!\w)(?![\"'])",
        "severity": "medium",
        "languages": ["shell"],
        "recommendation": "Always quote variable expansions: \"$var\"",
    },
]

# ============================================================================
# Permission Detection Patterns (from permissions.ts)
# ============================================================================

PERMISSION_PATTERNS = [
    {
        "permission": "filesystem",
        "description": "Reads or writes files on the filesystem",
        "patterns": [
            # Node.js filesystem
            r"\bfs\.(read|write|append|mkdir|rmdir|unlink|rename|copyFile|access|stat|readdir)",
            r"\bfs/promises",
            r"\brequire\s*\(\s*[\"']fs[\"']\s*\)",
            r"\bimport\s+.*\s+from\s+[\"']fs[\"']",
            r"\bimport\s+.*\s+from\s+[\"']node:fs[\"']",
            r"\breadFileSync|writeFileSync|appendFileSync",
            # Python filesystem
            r"\bopen\s*\([^)]*,\s*[\"'](?:r|w|a|rb|wb|ab)",
            r"\bos\.path\.",
            r"\bpathlib\.",
            r"\bshutil\.",
            r"\bglob\.",
            # General
            r"\bprocess\.cwd\(\)",
            r"\b__dirname\b",
            r"\b__filename\b",
        ],
    },
    {
        "permission": "network",
        "description": "Makes HTTP requests or network connections",
        "patterns": [
            # JavaScript/Node.js
            r"\bfetch\s*\(",
            r"\baxios\.",
            r"\brequire\s*\(\s*[\"']https?[\"']\s*\)",
            r"\bimport\s+.*\s+from\s+[\"']node-fetch[\"']",
            r"\bnew\s+WebSocket\s*\(",
            r"\bhttp\.(get|post|request)",
            r"\bhttps\.(get|post|request)",
            r"\bXMLHttpRequest\b",
            # Python
            r"\brequests\.(get|post|put|delete|patch|head)",
            r"\bimport\s+requests\b",
            r"\bfrom\s+requests\s+import\b",
            r"\burllib\.(request|parse)",
            r"\baiohttp\.",
            r"\bhttpx\.",
        ],
    },
    {
        "permission": "environment",
        "description": "Reads environment variables",
        "patterns": [
            # Node.js
            r"\bprocess\.env\b",
            # Python
            r"\bos\.environ\b",
            r"\bos\.getenv\s*\(",
            # dotenv
            r"\bdotenv\.config\(",
            r"\bload_dotenv\(",
            r"\bfrom\s+dotenv\s+import\b",
        ],
    },
    {
        "permission": "subprocess",
        "description": "Spawns child processes or executes commands",
        "patterns": [
            # Node.js
            r"\bchild_process\b",
            r"\bexec\s*\(",
            r"\bexecSync\s*\(",
            r"\bexecFile\s*\(",
            r"\bspawn\s*\(",
            r"\bspawnSync\s*\(",
            r"\bfork\s*\(",
            # Python
            r"\bsubprocess\.(run|call|Popen|check_output|check_call)",
            r"\bos\.system\s*\(",
            r"\bos\.popen\s*\(",
            r"\bos\.exec\w*\s*\(",
        ],
    },
    {
        "permission": "system",
        "description": "Accesses system information or resources",
        "patterns": [
            # Node.js
            r"\bos\.(platform|arch|cpus|freemem|totalmem|homedir|hostname|userInfo)",
            r"\bprocess\.(pid|ppid|platform|arch|version|memoryUsage)",
            # Python
            r"\bplatform\.(system|node|release|version|machine|processor)",
            r"\bsocket\.gethostname\(",
            r"\bgetpass\.getuser\(",
            r"\bos\.uname\(",
            r"\bpsutil\.",
        ],
    },
]

# ============================================================================
# File Language Detection
# ============================================================================

EXTENSION_LANGUAGE = {
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".py": "python",
    ".sh": "shell",
    ".bash": "shell",
}


def get_language(path: str) -> Optional[str]:
    """Get the language for a file based on extension."""
    for ext, lang in EXTENSION_LANGUAGE.items():
        if path.endswith(ext):
            return lang
    return None


# ============================================================================
# Scanner Implementation
# ============================================================================

def should_skip_file(path: str) -> bool:
    """Check if a file should be skipped."""
    return any(skip in path for skip in SKIP_FILES)


def is_sensitive_file(path: str) -> bool:
    """Check if a file is in a sensitive location."""
    return any(sf in path.lower() for sf in SENSITIVE_FILES)


def get_line_number(content: str, match_index: int) -> int:
    """Get the line number for a match index."""
    return content[:match_index].count("\n") + 1


def get_code_snippet(content: str, match_index: int, redact: bool = False) -> str:
    """Get a code snippet around a match."""
    lines = content.split("\n")
    line_number = get_line_number(content, match_index)
    line_index = line_number - 1

    start_line = max(0, line_index - 1)
    end_line = min(len(lines) - 1, line_index + 1)

    snippet_lines = []
    for i in range(start_line, end_line + 1):
        num = i + 1
        prefix = ">" if num == line_number else " "
        line = lines[i]

        if redact and num == line_number:
            # Mask secrets in the snippet
            line = line[:30] + "***REDACTED***" if len(line) > 30 else line

        snippet_lines.append(f"{prefix} {num}: {line}")

    return "\n".join(snippet_lines)


def scan_for_secrets(files: list[tuple[str, str]]) -> tuple[list[Finding], int]:
    """Scan files for hardcoded secrets."""
    findings = []
    seen_secrets = set()

    for file_path, content in files:
        if should_skip_file(file_path):
            continue

        sensitive = is_sensitive_file(file_path)

        for pattern_info in SECRET_PATTERNS:
            flags = pattern_info.get("flags", 0)
            pattern = re.compile(pattern_info["pattern"], flags)

            for match in pattern.finditer(content):
                # Create fingerprint to avoid duplicates
                fingerprint = f"{pattern_info['id']}:{file_path}:{match.group()[:10]}"
                if fingerprint in seen_secrets:
                    continue
                seen_secrets.add(fingerprint)

                line_number = get_line_number(content, match.start())
                severity = "critical" if sensitive else pattern_info["severity"]

                findings.append(Finding(
                    dimension="secret",
                    severity=severity,
                    title=f"{pattern_info['name']} detected",
                    description=f"Potential {pattern_info['name'].lower()} found. Hardcoded secrets should be stored in environment variables or a secrets manager.",
                    file_path=file_path,
                    line_number=line_number,
                    code_snippet=get_code_snippet(content, match.start(), redact=True),
                    rule_id=pattern_info["id"],
                ))

    # Score: any secret = 0
    score = 0 if findings else 100
    return findings, score


def scan_for_dangerous_code(files: list[tuple[str, str]]) -> tuple[list[Finding], int]:
    """Scan files for dangerous code patterns."""
    findings = []
    seen_findings = set()

    for file_path, content in files:
        language = get_language(file_path)
        if not language:
            continue

        applicable_patterns = [p for p in CODE_PATTERNS if language in p["languages"]]

        for pattern_info in applicable_patterns:
            flags = pattern_info.get("flags", 0)
            pattern = re.compile(pattern_info["pattern"], flags)

            for match in pattern.finditer(content):
                fingerprint = f"{pattern_info['id']}:{file_path}:{match.start()}"
                if fingerprint in seen_findings:
                    continue
                seen_findings.add(fingerprint)

                line_number = get_line_number(content, match.start())
                recommendation = pattern_info.get("recommendation", "")

                findings.append(Finding(
                    dimension="dangerous_code",
                    severity=pattern_info["severity"],
                    title=pattern_info["name"],
                    description=f"{pattern_info['description']}. {recommendation}",
                    file_path=file_path,
                    line_number=line_number,
                    code_snippet=get_code_snippet(content, match.start()),
                    rule_id=pattern_info["id"],
                ))

    # Calculate score based on findings
    score = 100
    for finding in findings:
        if finding.severity == "critical":
            score = 0
            break
        elif finding.severity == "high":
            score = min(score, 50)
        elif finding.severity == "medium":
            score = min(score, 70)
        elif finding.severity == "low":
            score = min(score, 90)

    return findings, score


def detect_permissions(files: list[tuple[str, str]]) -> tuple[list[str], list[Finding]]:
    """Detect required permissions from code."""
    detected_permissions = set()
    findings = []
    seen_findings = set()

    for file_path, content in files:
        # Skip non-code files
        if not re.search(r"\.(js|jsx|ts|tsx|mjs|cjs|py|sh|bash)$", file_path):
            continue

        for perm_info in PERMISSION_PATTERNS:
            for pattern_str in perm_info["patterns"]:
                pattern = re.compile(pattern_str)

                for match in pattern.finditer(content):
                    detected_permissions.add(perm_info["permission"])

                    fingerprint = f"{perm_info['permission']}:{file_path}:{match.group()}"
                    if fingerprint not in seen_findings:
                        seen_findings.add(fingerprint)
                        line_number = get_line_number(content, match.start())

                        findings.append(Finding(
                            dimension="permission",
                            severity="info",
                            title=f"Requires {perm_info['permission']} access",
                            description=perm_info["description"],
                            file_path=file_path,
                            line_number=line_number,
                            rule_id=f"permission-{perm_info['permission']}",
                        ))

    return list(detected_permissions), findings


def calculate_overall_score(secret_score: int, dangerous_code_score: int) -> int:
    """
    Calculate overall score from dimension scores.

    For local scans (no vulnerability dimension):
    - 50% secrets, 50% dangerous code
    - Capped at min dimension + 20
    """
    weighted_score = secret_score * 0.5 + dangerous_code_score * 0.5
    min_score = min(secret_score, dangerous_code_score)
    capped_score = min(weighted_score, min_score + 20)
    return round(capped_score)


def score_to_grade(score: int) -> str:
    """Convert numeric score to letter grade."""
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


# ============================================================================
# File Collection
# ============================================================================

def collect_files(skill_path: Path) -> list[tuple[str, str]]:
    """Collect all scannable files from a skill directory."""
    files = []

    # Scannable extensions
    extensions = {
        ".js", ".jsx", ".mjs", ".cjs",
        ".ts", ".tsx",
        ".py",
        ".sh", ".bash",
        ".json", ".yaml", ".yml",
        ".env", ".env.local", ".env.production",
        ".md", ".txt",
    }

    for root, dirs, filenames in os.walk(skill_path):
        # Skip hidden directories and common non-code directories
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in {"node_modules", "__pycache__", "venv", ".venv", "dist", "build"}]

        for filename in filenames:
            file_path = Path(root) / filename

            # Check extension or known config files
            if any(filename.endswith(ext) for ext in extensions) or filename in {".env", "Dockerfile"}:
                try:
                    relative_path = str(file_path.relative_to(skill_path))
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    files.append((relative_path, content))
                except Exception:
                    pass

    return files


def get_skill_name(skill_path: Path) -> str:
    """Get the skill name from SKILL.md or directory name."""
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        try:
            content = skill_md.read_text()
            # Parse YAML frontmatter
            if content.startswith("---"):
                end = content.find("---", 3)
                if end > 0:
                    frontmatter = content[3:end]
                    for line in frontmatter.split("\n"):
                        if line.startswith("name:"):
                            return line.split(":", 1)[1].strip().strip("\"'")
        except Exception:
            pass

    return skill_path.name


# ============================================================================
# Output Formatting
# ============================================================================

def format_text_report(result: ScanResult, verbose: bool = False) -> str:
    """Format the scan result as human-readable text."""
    lines = []

    # Header
    lines.append("")
    lines.append("Safety Scan Report")
    lines.append(f"  Skill: {result.skill_name}")
    lines.append(f"  Grade: {result.grade} ({result.score}/100)")
    lines.append("")

    # Scores
    lines.append("  Scores:")
    lines.append(f"    Secrets: {result.secret_score}/100")
    lines.append(f"    Dangerous Code: {result.dangerous_code_score}/100")
    lines.append("")

    # Permissions
    if result.permissions:
        lines.append("  Permissions Detected:")
        for perm in result.permissions:
            lines.append(f"    - {perm}")
        lines.append("")

    # Findings (exclude permission findings in non-verbose mode)
    security_findings = [f for f in result.findings if f.dimension != "permission"]

    if security_findings:
        lines.append(f"  Findings ({len(security_findings)}):")
        for finding in security_findings:
            severity_icon = {
                "critical": "[critical]",
                "high": "[high]",
                "medium": "[medium]",
                "low": "[low]",
            }.get(finding.severity, "[info]")

            lines.append(f"    {severity_icon} {finding.title}")
            lines.append(f"      File: {finding.file_path}:{finding.line_number}")

            if verbose and finding.code_snippet:
                for snippet_line in finding.code_snippet.split("\n"):
                    lines.append(f"      {snippet_line}")

            if verbose and finding.description:
                lines.append(f"      {finding.description}")

            lines.append("")
    else:
        lines.append("  No security issues found.")
        lines.append("")

    # Recommendation
    if result.grade in ("A", "B"):
        lines.append("  Ready for publishing.")
    elif result.grade == "C":
        lines.append("  Review findings before publishing.")
    else:
        lines.append("  Fix critical issues before publishing.")

    lines.append("")
    return "\n".join(lines)


def format_json_report(result: ScanResult) -> str:
    """Format the scan result as JSON."""
    return json.dumps({
        "skill_name": result.skill_name,
        "grade": result.grade,
        "score": result.score,
        "scores": {
            "secrets": result.secret_score,
            "dangerous_code": result.dangerous_code_score,
        },
        "permissions": result.permissions,
        "findings": [
            {
                "dimension": f.dimension,
                "severity": f.severity,
                "title": f.title,
                "description": f.description,
                "file_path": f.file_path,
                "line_number": f.line_number,
                "rule_id": f.rule_id,
            }
            for f in result.findings
            if f.dimension != "permission"  # Exclude permission findings from JSON
        ],
        "finding_count": len([f for f in result.findings if f.dimension != "permission"]),
    }, indent=2)


# ============================================================================
# Main Entry Point
# ============================================================================

def scan_skill(skill_path: Path) -> ScanResult:
    """Scan a skill directory and return results."""
    skill_name = get_skill_name(skill_path)
    files = collect_files(skill_path)

    # Run scanners
    secret_findings, secret_score = scan_for_secrets(files)
    code_findings, code_score = scan_for_dangerous_code(files)
    permissions, perm_findings = detect_permissions(files)

    # Calculate overall
    overall_score = calculate_overall_score(secret_score, code_score)
    grade = score_to_grade(overall_score)

    # Combine findings
    all_findings = secret_findings + code_findings + perm_findings

    return ScanResult(
        skill_name=skill_name,
        grade=grade,
        score=overall_score,
        secret_score=secret_score,
        dangerous_code_score=code_score,
        permissions=permissions,
        findings=all_findings,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Scan an Agent Skill for safety issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python safety_scan.py /path/to/my-skill
  python safety_scan.py ./my-skill --verbose
  python safety_scan.py ./my-skill --json
        """,
    )
    parser.add_argument("path", help="Path to the skill directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed findings")
    args = parser.parse_args()

    skill_path = Path(args.path).resolve()

    if not skill_path.exists():
        print(f"Error: Path does not exist: {skill_path}", file=sys.stderr)
        sys.exit(1)

    if not skill_path.is_dir():
        print(f"Error: Path is not a directory: {skill_path}", file=sys.stderr)
        sys.exit(1)

    # Run scan
    result = scan_skill(skill_path)

    # Output
    if args.json:
        print(format_json_report(result))
    else:
        print(format_text_report(result, verbose=args.verbose))

    # Exit code: 0 for A/B, 1 for C/D/F
    sys.exit(0 if result.grade in ("A", "B") else 1)


if __name__ == "__main__":
    main()
