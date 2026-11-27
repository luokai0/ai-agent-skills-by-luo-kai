#!/usr/bin/env python3
"""
web-monitor v2.0: Track web pages for changes with keyword alerts, regex matching,
content fingerprinting, and structured diff output.
Pure Python, zero required dependencies (beautifulsoup4 optional).
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from difflib import unified_diff

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

DATA_DIR = Path(os.environ.get("WEB_MONITOR_DIR", Path.home() / ".web-monitor"))
WATCHES_FILE = DATA_DIR / "watches.json"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"
ALERTS_DIR = DATA_DIR / "alerts"

def ensure_dirs():
    for d in (DATA_DIR, SNAPSHOTS_DIR, ALERTS_DIR):
        d.mkdir(parents=True, exist_ok=True)

def load_watches() -> dict:
    if WATCHES_FILE.exists():
        return json.loads(WATCHES_FILE.read_text())
    return {"watches": []}

def save_watches(data: dict):
    WATCHES_FILE.write_text(json.dumps(data, indent=2))

def slug(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()[:12]

def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]

def fetch_content(url: str, selector: str = None, headers: dict = None) -> str:
    req_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) web-monitor/2.0"
    }
    if headers:
        req_headers.update(headers)
    
    req = Request(url, headers=req_headers)
    try:
        with urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.reason}")
    except URLError as e:
        raise RuntimeError(f"Connection error: {e.reason}")
    
    if selector and HAS_BS4:
        soup = BeautifulSoup(raw, "html.parser")
        elements = soup.select(selector)
        if not elements:
            return f"[No elements matched selector: {selector}]"
        return "\n".join(el.get_text(strip=True, separator="\n") for el in elements)
    
    if HAS_BS4:
        soup = BeautifulSoup(raw, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        return soup.get_text(strip=True, separator="\n")
    
    text = re.sub(r'<[^>]+>', ' ', raw)
    return re.sub(r'\s+', ' ', text).strip()

def normalize_text(text: str) -> str:
    lines = text.split("\n")
    lines = [re.sub(r'\s+', ' ', line.strip()) for line in lines if line.strip()]
    return "\n".join(lines)

def check_keywords(text: str, keywords: list) -> list:
    """Check if any keywords appear in the text. Returns matched keywords."""
    matches = []
    text_lower = text.lower()
    for kw in keywords:
        if kw.startswith("re:"):
            pattern = kw[3:]
            if re.search(pattern, text, re.IGNORECASE):
                matches.append(kw)
        elif kw.lower() in text_lower:
            matches.append(kw)
    return matches

def extract_keyword_context(text: str, keyword: str, context_chars: int = 100) -> list:
    """Extract text snippets around keyword matches."""
    snippets = []
    kw = keyword[3:] if keyword.startswith("re:") else re.escape(keyword)
    for m in re.finditer(kw, text, re.IGNORECASE):
        start = max(0, m.start() - context_chars)
        end = min(len(text), m.end() + context_chars)
        snippet = text[start:end].replace("\n", " ")
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."
        snippets.append(snippet)
    return snippets[:5]  # Max 5 snippets per keyword

def cmd_add(args):
    ensure_dirs()
    data = load_watches()
    
    for w in data["watches"]:
        if w["url"] == args.url:
            print(f"Already watching: {args.url}")
            return
    
    keywords = []
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(",")]
    
    watch = {
        "url": args.url,
        "name": args.name or args.url[:60],
        "selector": args.selector,
        "keywords": keywords,
        "added": datetime.now(timezone.utc).isoformat(),
        "last_check": None,
        "last_change": None,
        "check_count": 0,
        "change_count": 0,
        "content_hash": None,
        "alert_on_keywords_only": bool(args.keywords_only) if hasattr(args, 'keywords_only') else False,
    }
    data["watches"].append(watch)
    save_watches(data)
    
    try:
        content = fetch_content(args.url, args.selector)
        content = normalize_text(content)
        snap_path = SNAPSHOTS_DIR / f"{slug(args.url)}.txt"
        snap_path.write_text(content)
        watch["content_hash"] = content_hash(content)
        save_watches(data)
        
        if keywords:
            matches = check_keywords(content, keywords)
            if matches:
                print(f"✅ Added: {watch['name']} (⚠️ keywords already present: {', '.join(matches)})")
            else:
                print(f"✅ Added: {watch['name']} (watching for: {', '.join(keywords)})")
        else:
            print(f"✅ Added and snapshotted: {watch['name']}")
    except Exception as e:
        print(f"⚠️  Added but initial fetch failed: {e}")

def cmd_remove(args):
    ensure_dirs()
    data = load_watches()
    original = len(data["watches"])
    data["watches"] = [w for w in data["watches"] if w["url"] != args.url and w["name"] != args.url]
    if len(data["watches"]) < original:
        save_watches(data)
        # Clean up snapshots
        s = slug(args.url)
        for f in SNAPSHOTS_DIR.glob(f"{s}*"):
            f.unlink()
        print(f"✅ Removed: {args.url}")
    else:
        print(f"Not found: {args.url}")

def cmd_list(args):
    ensure_dirs()
    data = load_watches()
    if not data["watches"]:
        print("No URLs being watched. Use 'add' to start.")
        return
    
    fmt = getattr(args, 'format', 'text')
    if fmt == 'json':
        print(json.dumps(data["watches"], indent=2))
        return
    
    for i, w in enumerate(data["watches"], 1):
        status = "never checked" if not w["last_check"] else f"checked {w['check_count']}x, {w['change_count']} changes"
        sel = f" [selector: {w['selector']}]" if w.get("selector") else ""
        kw = f" [keywords: {', '.join(w['keywords'])}]" if w.get("keywords") else ""
        print(f"{i}. {w['name']}")
        print(f"   URL: {w['url']}{sel}{kw}")
        print(f"   Status: {status}")
        if w.get("last_change"):
            print(f"   Last change: {w['last_change']}")
        print()

def cmd_keywords(args):
    """Add or remove keywords for a watch."""
    ensure_dirs()
    data = load_watches()
    
    watch = None
    for w in data["watches"]:
        if w["url"] == args.url or w["name"] == args.url:
            watch = w
            break
    
    if not watch:
        print(f"Not found: {args.url}")
        return
    
    if not watch.get("keywords"):
        watch["keywords"] = []
    
    if args.add:
        new_kw = [k.strip() for k in args.add.split(",")]
        watch["keywords"].extend(new_kw)
        watch["keywords"] = list(set(watch["keywords"]))
        save_watches(data)
        print(f"✅ Keywords for {watch['name']}: {', '.join(watch['keywords'])}")
    elif args.remove:
        rm_kw = [k.strip() for k in args.remove.split(",")]
        watch["keywords"] = [k for k in watch["keywords"] if k not in rm_kw]
        save_watches(data)
        print(f"✅ Keywords for {watch['name']}: {', '.join(watch['keywords']) or '(none)'}")
    elif args.clear:
        watch["keywords"] = []
        save_watches(data)
        print(f"✅ Cleared all keywords for {watch['name']}")
    else:
        if watch["keywords"]:
            print(f"Keywords for {watch['name']}: {', '.join(watch['keywords'])}")
        else:
            print(f"No keywords set for {watch['name']}")

def cmd_check(args):
    ensure_dirs()
    data = load_watches()
    
    if not data["watches"]:
        print("No URLs being watched.")
        return
    
    watches_to_check = data["watches"]
    if args.url:
        watches_to_check = [w for w in data["watches"] if w["url"] == args.url or w["name"] == args.url]
        if not watches_to_check:
            print(f"Not found: {args.url}")
            return
    
    results = []
    for watch in watches_to_check:
        url = watch["url"]
        s = slug(url)
        snap_path = SNAPSHOTS_DIR / f"{s}.txt"
        
        try:
            new_content = fetch_content(url, watch.get("selector"))
            new_content = normalize_text(new_content)
        except Exception as e:
            results.append({"name": watch["name"], "url": url, "error": str(e)})
            continue
        
        now = datetime.now(timezone.utc).isoformat()
        watch["last_check"] = now
        watch["check_count"] = watch.get("check_count", 0) + 1
        new_hash = content_hash(new_content)
        
        # Quick hash check — skip diff if unchanged
        if watch.get("content_hash") == new_hash and snap_path.exists():
            results.append({"name": watch["name"], "url": url, "changed": False})
            continue
        
        result = {"name": watch["name"], "url": url, "changed": False}
        keywords = watch.get("keywords", [])
        added_text = ""  # will be set from diff
        
        if snap_path.exists():
            old_content = snap_path.read_text()
            if old_content != new_content:
                old_lines = old_content.split("\n")
                new_lines = new_content.split("\n")
                diff = list(unified_diff(old_lines, new_lines, n=2, lineterm=""))
                
                added = [l for l in diff if l.startswith("+") and not l.startswith("+++")]
                removed = [l for l in diff if l.startswith("-") and not l.startswith("---")]
                
                watch["last_change"] = now
                watch["change_count"] = watch.get("change_count", 0) + 1
                watch["content_hash"] = new_hash
                
                snap_path.write_text(new_content)
                
                diff_path = SNAPSHOTS_DIR / f"{s}_diff_{int(time.time())}.txt"
                diff_path.write_text("\n".join(diff))
                
                result["changed"] = True
                result["added_lines"] = len(added)
                result["removed_lines"] = len(removed)
                result["diff_preview"] = "\n".join(diff[:30])
                added_text = "\n".join(l[1:] for l in added)
                
                # Extract only the added content for summary
                result["new_content"] = "\n".join(l[1:] for l in added[:20])
        else:
            snap_path.write_text(new_content)
            watch["content_hash"] = new_hash
            result["note"] = "initial snapshot"
            added_text = new_content  # for first snapshot, check all content
        
        # Keyword check — only on ADDED text (new content from diff)
        if keywords and added_text:
            kw_matches = check_keywords(added_text, keywords)
            if kw_matches:
                result["keyword_matches"] = kw_matches
                result["keyword_contexts"] = {}
                for kw in kw_matches:
                    result["keyword_contexts"][kw] = extract_keyword_context(added_text, kw)
                
                alert = {
                    "url": url,
                    "name": watch["name"],
                    "time": now,
                    "keywords": kw_matches,
                    "contexts": result["keyword_contexts"],
                }
                alert_path = ALERTS_DIR / f"{s}_{int(time.time())}.json"
                alert_path.write_text(json.dumps(alert, indent=2))
        
        results.append(result)
    
    save_watches(data)
    
    fmt = getattr(args, 'format', 'text')
    if fmt == 'json':
        print(json.dumps(results, indent=2))
        return
    
    for r in results:
        if r.get("error"):
            print(f"❌ {r['name']}: {r['error']}")
        elif r.get("changed"):
            print(f"🔔 CHANGED: {r['name']}")
            print(f"   URL: {r['url']}")
            print(f"   +{r['added_lines']} lines / -{r['removed_lines']} lines")
            if r.get("keyword_matches"):
                print(f"   🔑 KEYWORD ALERT: {', '.join(r['keyword_matches'])}")
                for kw, contexts in r.get("keyword_contexts", {}).items():
                    for ctx in contexts[:2]:
                        print(f"      → {ctx}")
            if r.get("diff_preview") and not args.quiet:
                print(f"   Preview:")
                for line in r["diff_preview"].split("\n")[:10]:
                    print(f"     {line}")
            print()
        elif r.get("keyword_matches"):
            print(f"🔑 KEYWORD FOUND: {r['name']}")
            print(f"   Keywords: {', '.join(r['keyword_matches'])}")
            for kw, contexts in r.get("keyword_contexts", {}).items():
                for ctx in contexts[:2]:
                    print(f"   → {ctx}")
            print()
        elif r.get("note"):
            print(f"📸 {r['name']}: {r['note']}")
        else:
            if not args.quiet:
                print(f"✅ {r['name']}: no changes")
    
    # Summary
    changes = sum(1 for r in results if r.get("changed"))
    kw_alerts = sum(1 for r in results if r.get("keyword_matches"))
    errors = sum(1 for r in results if r.get("error"))
    
    if len(results) > 1:
        parts = []
        if changes:
            parts.append(f"{changes} changed")
        if kw_alerts:
            parts.append(f"{kw_alerts} keyword alerts")
        if errors:
            parts.append(f"{errors} errors")
        if not parts:
            parts.append("no changes")
        print(f"\nSummary: {', '.join(parts)} ({len(results)} checked)")

def cmd_diff(args):
    ensure_dirs()
    data = load_watches()
    
    watch = None
    for w in data["watches"]:
        if w["url"] == args.url or w["name"] == args.url:
            watch = w
            break
    
    if not watch:
        print(f"Not found: {args.url}")
        return
    
    s = slug(watch["url"])
    diffs = sorted(SNAPSHOTS_DIR.glob(f"{s}_diff_*.txt"), reverse=True)
    if not diffs:
        print(f"No diffs recorded for: {watch['name']}")
        return
    
    n = args.last if hasattr(args, 'last') and args.last else 1
    for i, diff_file in enumerate(diffs[:n]):
        ts = int(diff_file.stem.split("_diff_")[1])
        dt = datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        print(f"{'─' * 60}")
        print(f"Diff #{i+1} for: {watch['name']} ({dt})")
        print(f"{'─' * 60}")
        print(diff_file.read_text())
        print()

def cmd_snapshot(args):
    ensure_dirs()
    data = load_watches()
    
    watch = None
    for w in data["watches"]:
        if w["url"] == args.url or w["name"] == args.url:
            watch = w
            break
    
    if not watch:
        print(f"Not found: {args.url}")
        return
    
    snap_path = SNAPSHOTS_DIR / f"{slug(watch['url'])}.txt"
    if not snap_path.exists():
        print(f"No snapshot for: {watch['name']}")
        return
    
    content = snap_path.read_text()
    if args.lines:
        lines = content.split("\n")[:args.lines]
        print("\n".join(lines))
    elif args.search:
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if args.search.lower() in line.lower():
                print(f"  {i+1}: {line}")
    else:
        print(content[:5000])

def cmd_alerts(args):
    """Show recent keyword alerts."""
    ensure_dirs()
    alert_files = sorted(ALERTS_DIR.glob("*.json"), reverse=True)
    
    if not alert_files:
        print("No keyword alerts recorded.")
        return
    
    n = args.last if hasattr(args, 'last') and args.last else 10
    fmt = getattr(args, 'format', 'text')
    
    if fmt == 'json':
        alerts = [json.loads(f.read_text()) for f in alert_files[:n]]
        print(json.dumps(alerts, indent=2))
        return
    
    for f in alert_files[:n]:
        alert = json.loads(f.read_text())
        dt = alert.get("time", "unknown")[:19].replace("T", " ")
        print(f"🔑 {alert['name']} ({dt})")
        print(f"   Keywords: {', '.join(alert.get('keywords', []))}")
        for kw, contexts in alert.get("contexts", {}).items():
            for ctx in contexts[:1]:
                print(f"   → {ctx[:120]}")
        print()

def cmd_stats(args):
    """Show monitoring statistics."""
    ensure_dirs()
    data = load_watches()
    
    total = len(data["watches"])
    total_checks = sum(w.get("check_count", 0) for w in data["watches"])
    total_changes = sum(w.get("change_count", 0) for w in data["watches"])
    with_keywords = sum(1 for w in data["watches"] if w.get("keywords"))
    alert_count = len(list(ALERTS_DIR.glob("*.json")))
    snap_size = sum(f.stat().st_size for f in SNAPSHOTS_DIR.glob("*"))
    
    print(f"📊 Web Monitor Stats")
    print(f"   Watches: {total} ({with_keywords} with keywords)")
    print(f"   Total checks: {total_checks}")
    print(f"   Total changes: {total_changes}")
    print(f"   Keyword alerts: {alert_count}")
    print(f"   Snapshot storage: {snap_size / 1024:.1f} KB")

def main():
    parser = argparse.ArgumentParser(prog="web-monitor", description="Monitor web pages for changes v2.0")
    sub = parser.add_subparsers(dest="command", required=True)
    
    # add
    p = sub.add_parser("add", help="Add a URL to watch")
    p.add_argument("url")
    p.add_argument("--name", "-n")
    p.add_argument("--selector", "-s", help="CSS selector (requires beautifulsoup4)")
    p.add_argument("--keywords", "-k", help="Comma-separated keywords to alert on (prefix re: for regex)")
    p.add_argument("--keywords-only", action="store_true", help="Only alert on keyword matches, not all changes")
    p.set_defaults(func=cmd_add)
    
    # remove
    p = sub.add_parser("remove", help="Remove a URL")
    p.add_argument("url")
    p.set_defaults(func=cmd_remove)
    
    # list
    p = sub.add_parser("list", help="List watched URLs")
    p.add_argument("--format", "-f", choices=["text", "json"], default="text")
    p.set_defaults(func=cmd_list)
    
    # keywords
    p = sub.add_parser("keywords", help="Manage keywords for a watch")
    p.add_argument("url", help="URL or name")
    p.add_argument("--add", "-a", help="Add keywords (comma-separated)")
    p.add_argument("--remove", "-r", help="Remove keywords (comma-separated)")
    p.add_argument("--clear", action="store_true")
    p.set_defaults(func=cmd_keywords)
    
    # check
    p = sub.add_parser("check", help="Check for changes")
    p.add_argument("url", nargs="?")
    p.add_argument("--format", "-f", choices=["text", "json"], default="text")
    p.add_argument("--quiet", "-q", action="store_true", help="Only show changes/alerts")
    p.set_defaults(func=cmd_check)
    
    # diff
    p = sub.add_parser("diff", help="Show diffs for a URL")
    p.add_argument("url")
    p.add_argument("--last", "-l", type=int, default=1, help="Number of recent diffs")
    p.set_defaults(func=cmd_diff)
    
    # snapshot
    p = sub.add_parser("snapshot", help="Show current snapshot")
    p.add_argument("url")
    p.add_argument("--lines", "-l", type=int)
    p.add_argument("--search", "-s", help="Search within snapshot")
    p.set_defaults(func=cmd_snapshot)
    
    # alerts
    p = sub.add_parser("alerts", help="Show keyword alerts")
    p.add_argument("--last", "-l", type=int, default=10)
    p.add_argument("--format", "-f", choices=["text", "json"], default="text")
    p.set_defaults(func=cmd_alerts)
    
    # stats
    p = sub.add_parser("stats", help="Show monitoring statistics")
    p.set_defaults(func=cmd_stats)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
