# web-monitor

Monitor web pages for content changes with keyword alerts.

Track URLs, detect updates, view diffs, get notified when specific keywords appear in new content.

**Pure Python, zero required dependencies** (beautifulsoup4 optional for CSS selectors).

## Usage

```bash
# Add a URL to watch
python3 scripts/monitor.py add https://anthropic.com/news --name "Anthropic News"

# Add with keyword alerts (triggers only on NEW content)
python3 scripts/monitor.py add https://openai.com/blog -n "OpenAI Blog" \
    --keywords "gpt,o3,codex,sora"

# Add with regex keywords
python3 scripts/monitor.py add https://example.com -k "re:v\d+\.\d+,release"

# Check all watched URLs for changes
python3 scripts/monitor.py check

# Quiet mode (only show changes/alerts)
python3 scripts/monitor.py check -q

# View the last diff
python3 scripts/monitor.py diff "Anthropic News"

# Manage keywords
python3 scripts/monitor.py keywords "OpenAI Blog" --add "reasoning,agents"
python3 scripts/monitor.py keywords "OpenAI Blog" --remove "sora"

# View current snapshot
python3 scripts/monitor.py snapshot "Anthropic News" --lines 20

# Search within a snapshot
python3 scripts/monitor.py snapshot "OpenAI Blog" --search "codex"

# Show keyword alert history
python3 scripts/monitor.py alerts

# Statistics
python3 scripts/monitor.py stats
```

## Features

- **Content change detection** with unified diffs
- **Keyword alerts** — plain text or regex (`re:pattern`)
- **Diff-only keyword matching** — alerts only fire on *new* content, not existing page elements
- **Content fingerprinting** (SHA-256) for fast unchanged detection
- **CSS selector targeting** (with beautifulsoup4)
- **Alert history** saved as JSON
- **JSON output** for scripting (`--format json`)
- **Multiple diff history** (`diff --last N`)
- **Snapshot search** within saved content

## Data

All data stored in `~/.web-monitor/`:
- `watches.json` — tracked URLs and their state
- `snapshots/` — latest page content + diff history
- `alerts/` — keyword alert records

## License

MIT
