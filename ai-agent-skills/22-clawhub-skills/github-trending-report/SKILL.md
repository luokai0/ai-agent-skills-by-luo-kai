---
name: "skill"
description: "- Data is sourced from the GitHub Search API; freshness depends on GitHub's indexing lag"
---


<!-- Original nonstandard metadata retained for reference:
## 📈 GitHub <Period> Trending Report

### 1. Fastest-Growing Projects
> Source: `trending` — reflects real growth velocity, age bias removed

List Top 5–10 entries, each with:
- Repository name (with link)
- Short description
- Star count / daily average growth
- Primary language

### 2. Newly Popular Repositories
> Source: `popular` — recently created projects gaining rapid traction

List Top 5–10 entries, same format as above.

### 3. Hot Topics
> Source: `topic` — scored by repository count × star magnitude

List Top 10 topic tags with a brief description of each technology area.

### 4. AI Insights
Based on the data above, provide:
- A 2–3 sentence summary of the key technical trends this period
- Projects or movements worth watching closely
- If a language filter was applied, a brief analysis of that ecosystem's current state
-->


## Limitations

- Data is sourced from the GitHub Search API; freshness depends on GitHub's indexing lag
- The `trending` growth score is estimated from creation time and star count, and it is **not** GitHub's official Trending page data
- The `-l` language filter matches only the repository's primary language; multi-language projects may be excluded
