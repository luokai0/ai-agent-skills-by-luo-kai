---
name: revealjs-presentation
description: |
  Build interactive HTML slide presentations using Reveal.js + Chart.js. Use when asked to create a slide deck, pitch deck, presentation, or slideshow. Creates a single self-contained .html file with animations, charts, and polished UI. Can also publish presentations directly to zo.space as live page routes.
compatibility: Created for Zo Computer
metadata:
  author: skeletorjs.zo.computer
  version: 1.0
---
# Reveal.js Presentation Skill

Build self-contained HTML slide decks using Reveal.js 5 + Chart.js 4. Every output is a single `.html` file that opens in any browser. Optionally publish to zo.space as a live page route.

## Two Output Modes

### 1. Local HTML File (default)
Creates a single `.html` file saved to the user's workspace. No build step, no dependencies. Open in any browser.

### 2. zo.space Page Route (on request)
Publishes the presentation as a live page on the user's `<handle>.zo.space`. Uses the pre-installed `reveal.js` package + inline styles. Use when the user says "publish", "put it on zo.space", "make it live", or "share it online".

The publish script at `scripts/publish.ts` handles the conversion from local HTML to a zo.space-compatible React page route. Run it via:
```bash
bun /home/workspace/Skills/revealjs-presentation/scripts/publish.ts --file <path-to-html> --route <path> [--public]
```

When publishing to zo.space:
- Reveal.js is imported from the pre-installed package (`import Reveal from "reveal.js"`)
- Chart.js is loaded from CDN via dynamic script injection in useEffect
- All CSS is inlined in the component
- The route defaults to private unless `--public` is passed
- After publishing, check `get_space_errors()` for build issues

---

## Core Stack (Local HTML)

| Library | CDN | Purpose |
|---------|-----|---------|
| Reveal.js 5.1 | `cdn.jsdelivr.net/npm/reveal.js@5.1.0` | Slide engine |
| Chart.js 4.4 | `cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js` | Charts |
| Google Fonts | `fonts.googleapis.com` | Typography |

---

## Approved Extension Libraries

Reach for these when the core stack can't cover the requirement. All are CDN-loadable and UMD-compatible.

### Data Visualization

| Need | Library | CDN |
|------|---------|-----|
| Custom charts | D3.js v7 | `cdn.jsdelivr.net/npm/d3@7` |
| Animated counters | CountUp.js | `cdn.jsdelivr.net/npm/countup.js@2` |
| Geographic maps | Leaflet.js | `cdn.jsdelivr.net/npm/leaflet@1.9` |
| Flow diagrams | Mermaid.js | `cdn.jsdelivr.net/npm/mermaid@10` |

### Animation & Motion

| Need | Library | CDN |
|------|---------|-----|
| Complex sequences | GSAP | `cdn.jsdelivr.net/npm/gsap@3` |
| Particle backgrounds | tsParticles | `cdn.jsdelivr.net/npm/tsparticles@2` |
| Typewriter effect | Typed.js | `cdn.jsdelivr.net/npm/typed.js@2` |
| Lottie animations | lottie-web | `cdn.jsdelivr.net/npm/lottie-web@5` |

### Content & Code

| Need | Library | CDN |
|------|---------|-----|
| Code highlighting | Prism.js | `cdn.jsdelivr.net/npm/prismjs@1` |
| Math / LaTeX | MathJax 3 | `cdn.jsdelivr.net/npm/mathjax@3` |
| Icons | Lucide | `unpkg.com/lucide@latest/dist/umd/lucide.js` |

---

## Compatibility Checks for New Libraries

Before adding any library not listed above:

1. **Can CSS or existing stack handle it?** Many effects don't need a library.
2. **UMD build on CDN?** Must work via `<script src="...">` tag. ES module-only packages won't work.
3. **No conflict with Reveal.js?** Watch for global keyboard/scroll listeners, body transform manipulation.
4. **Init after slide visible?** Use `slidechanged` event handler, not DOMContentLoaded.
5. **< 200KB gzipped?** Check bundlephobia.com before adding.

---

## File Structure (Local HTML)

Always output a **single `.html` file**:

```
<head>
  fonts → reveal.css → theme → chart.js → <style>
</head>
<body>
  SVG symbol defs (logos, icons)
  <div class="reveal">
    <div class="slides">
      <section> x N slides
    </div>
  </div>
  reveal.js script → init script → chart build functions
</body>
```

---

## Boilerplate Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>PRESENTATION TITLE</title>
<link href="https://fonts.googleapis.com/css2?family=YOUR+FONTS&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css"/>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root {
  --bg:    #FAFAF8;
  --dk:    #111111;
  --dk2:   #333333;
  --gray:  #888888;
  --accent:#YOUR_COLOR;
  --border:#E5E5E5;
  --f-sans:'YOUR_FONT', system-ui, sans-serif;
  --f-mono:'YOUR_MONO', 'SF Mono', monospace;
}

.reveal { font-family: var(--f-sans); }
.reveal .slides section {
  text-align: left;
  height: 100%;
  padding: 0;
}

.S {
  position: relative;
  width: 100%; height: 100%;
  display: flex; flex-direction: column;
  padding: 32px 52px 24px;
  overflow: hidden;
  background: var(--bg);
  color: var(--dk);
  box-sizing: border-box;
}
.S > * { position: relative; z-index: 1; }

.pre { opacity: 0; }
.al  { animation: fromLeft  .5s ease forwards; }
.ar  { animation: fromRight .5s ease forwards; }
.ab  { animation: fromBelow .5s ease forwards; }
.af  { animation: fadeUp    .55s ease forwards; }
.ap  { animation: pop       .4s ease forwards; }

.d1 { animation-delay:.08s }
.d2 { animation-delay:.18s }
.d3 { animation-delay:.28s }
.d4 { animation-delay:.38s }
.d5 { animation-delay:.48s }
.d6 { animation-delay:.58s }

@keyframes fromLeft  { from{opacity:0;transform:translateX(-22px)} to{opacity:1;transform:none} }
@keyframes fromRight { from{opacity:0;transform:translateX(22px)}  to{opacity:1;transform:none} }
@keyframes fromBelow { from{opacity:0;transform:translateY(18px)}  to{opacity:1;transform:none} }
@keyframes fadeUp    { from{opacity:0}                             to{opacity:1} }
@keyframes pop       { from{opacity:0;transform:scale(.93)}        to{opacity:1;transform:scale(1)} }

.cw {
  position: relative;
  width: 100%;
  min-height: 200px;
  flex-shrink: 0;
}
.cw canvas {
  position: absolute;
  inset: 0;
  width: 100% !important;
  height: 100% !important;
}

.h1 { font-size:52px; font-weight:800; line-height:1.05; }
.h2 { font-size:38px; font-weight:700; line-height:1.1;  }
.h3 { font-size:28px; font-weight:700; line-height:1.15; }
.stag {
  font-family: var(--f-mono);
  font-size: 11px;
  letter-spacing: .25em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 10px;
}
.mono { font-family: var(--f-mono); }

.row { display:flex; flex-direction:row; gap:24px; }
.col { display:flex; flex-direction:column; gap:12px; }
.g2  { display:grid; grid-template-columns:1fr 1fr;         gap:12px; }
.g3  { display:grid; grid-template-columns:1fr 1fr 1fr;     gap:12px; }
.g4  { display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:12px; }

.card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 18px 20px;
}
.card.accent {
  background: var(--accent);
  color: #fff;
  border: none;
}

.pill {
  display:inline-flex; align-items:center;
  padding:3px 10px; border-radius:99px;
  font-size:11px; font-weight:600; letter-spacing:.03em;
  background: rgba(0,0,0,.07);
}
</style>
</head>
<body>

<div class="reveal">
<div class="slides">

  <!-- SLIDES GO HERE -->

</div>
</div>

<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
<script>
const chartMap = {};
const built = new Set();

Reveal.initialize({
  hash: true,
  transition: 'fade',
  transitionSpeed: 'fast',
  controls: true,
  progress: true,
  width: 1280,
  height: 720,
  margin: 0,
});

function animateSlide(slide) {
  slide.querySelectorAll('.pre').forEach(el => el.classList.remove('pre'));
}

Reveal.on('slidechanged', ({ indexh }) => {
  const slide = Reveal.getSlide(indexh);
  if (slide) animateSlide(slide);
  if (chartMap[indexh] && !built.has(indexh)) {
    built.add(indexh);
    chartMap[indexh]();
  }
});

Reveal.on('ready', () => {
  const slide = Reveal.getSlide(0);
  if (slide) animateSlide(slide);
  if (chartMap[0] && !built.has(0)) {
    built.add(0);
    chartMap[0]();
  }
});
</script>
</body>
</html>
```

---

## Slide Anatomy

Every slide follows this pattern:

```html
<section>
<div class="S">
  <div class="stag pre af d1">Category</div>
  <div class="h2 pre al d2">Headline with <span style="color:var(--accent)">accent</span></div>
  <div class="pre af d3" style="color:var(--gray);font-size:16px;margin-bottom:20px;">
    Supporting text.
  </div>
  <div class="g2 pre af d4" style="flex:1;min-height:0;">
    <!-- content -->
  </div>
</div>
</section>
```

---

## Layout Patterns

### 2-Column Split
```html
<div class="row" style="flex:1;gap:32px;">
  <div class="col" style="flex:1;"><!-- left --></div>
  <div class="col" style="flex:1.2;"><!-- right --></div>
</div>
```

### Card Grid (3-up)
```html
<div class="g3" style="flex:1;min-height:0;">
  <div class="card pre ap d3">...</div>
  <div class="card pre ap d4">...</div>
  <div class="card pre ap d5">...</div>
</div>
```

### Hero Stat
```html
<div style="display:flex;align-items:baseline;gap:8px;margin-bottom:4px;">
  <div style="font-size:64px;font-weight:900;color:var(--accent);">$5.2B</div>
  <div style="font-size:18px;color:var(--gray);">market</div>
</div>
```

### CSS Treemap
```html
<div style="display:flex;flex-direction:column;gap:4px;flex:1;">
  <div style="display:flex;gap:4px;flex:34;">
    <div style="flex:1;background:#COLOR;border-radius:6px;padding:10px;color:#fff;">
      <div style="font-size:11px;opacity:.7;">Category</div>
      <div style="font-weight:700;">34%</div>
    </div>
  </div>
</div>
```

### Numbered Steps / Timeline
```html
<div style="display:flex;gap:0;flex:1;position:relative;">
  <div style="position:absolute;top:28px;left:28px;right:28px;height:2px;background:var(--border);z-index:0;"></div>
  <div style="flex:1;display:flex;flex-direction:column;align-items:center;text-align:center;position:relative;z-index:1;">
    <div style="width:56px;height:56px;border-radius:50%;background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:18px;flex-shrink:0;">1</div>
    <div style="font-weight:600;margin-top:10px;font-size:14px;">Step Title</div>
    <div style="font-size:12px;color:var(--gray);margin-top:4px;">Description</div>
  </div>
</div>
```

### Comparison Table (CSS grid)
```html
<div style="display:grid;grid-template-columns:2fr 1fr 1fr;gap:1px;background:var(--border);border-radius:10px;overflow:hidden;">
  <div style="background:var(--dk);color:#fff;padding:10px 14px;font-size:12px;font-weight:700;">Feature</div>
  <div style="background:var(--dk);color:#fff;padding:10px 14px;font-size:12px;font-weight:700;text-align:center;">Option A</div>
  <div style="background:var(--dk);color:var(--accent);padding:10px 14px;font-size:12px;font-weight:700;text-align:center;">Option B</div>
  <div style="background:#fff;padding:9px 14px;font-size:13px;">Feature name</div>
  <div style="background:#fff;padding:9px 14px;font-size:13px;text-align:center;color:var(--gray);">No</div>
  <div style="background:#fff;padding:9px 14px;font-size:13px;text-align:center;color:var(--accent);font-weight:600;">Yes</div>
</div>
```

---

## Chart.js Recipes

### Bar Chart
```js
function buildBarChart() {
  const ctx = document.getElementById('barChart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [{
        label: 'Revenue',
        data: [42, 68, 55, 89, 104, 127],
        backgroundColor: 'YOUR_COLOR',
        borderRadius: 6,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, border: { display: false } },
        y: { grid: { color: '#f0f0f0' }, border: { display: false } }
      }
    }
  });
}
```

### Line Chart
```js
function buildLineChart() {
  const ctx = document.getElementById('lineChart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Q1', 'Q2', 'Q3', 'Q4'],
      datasets: [{
        label: 'Series A',
        data: [30, 55, 80, 120],
        borderColor: 'YOUR_COLOR_1',
        backgroundColor: 'YOUR_COLOR_1_20',
        borderWidth: 2.5,
        pointRadius: 4,
        tension: 0.35,
        fill: true,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { grid: { display: false } },
        y: { grid: { color: '#f0f0f0' } }
      }
    }
  });
}
```

### Doughnut
```js
function buildDoughnut() {
  const ctx = document.getElementById('doughnutChart').getContext('2d');
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['A', 'B', 'C'],
      datasets: [{
        data: [40, 30, 30],
        backgroundColor: ['#C1','#C2','#C3'],
        borderWidth: 0,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '65%',
    }
  });
}
```

**Canvas HTML:**
```html
<div class="cw" style="min-height:220px;">
  <canvas id="UNIQUE_CHART_ID"></canvas>
</div>
```

Register in chartMap:
```js
const chartMap = { 3: buildFunnelChart, 7: buildLineChart };
```

---

## Animation Rules

1. Add `.pre` to any element to start invisible
2. Add direction: `.al` (left), `.ar` (right), `.ab` (below), `.af` (fade), `.ap` (pop)
3. Add delay: `.d1` through `.d6`
4. Init script removes `.pre` when slide becomes active

---

## Critical Gotchas

- **Chart height must be explicit.** `.cw` wrappers need `min-height`. Chart.js reads container height; 0px = invisible.
- **Dead functions = errors.** Every `chartMap` entry needs a matching `<canvas id>`.
- **Don't reuse canvas IDs.** Each chart needs a unique ID.
- **SVG logos: define once, use everywhere** with `<symbol>` and `<use href="#id">`.
- **Reveal.js default is 960x700.** For widescreen: `width: 1280, height: 720`.

---

## Slide Type Catalog

| Type | Best For |
|------|----------|
| Hero / Title | Opening, closing |
| Stat Showcase | Key metrics |
| Problem / Opportunity | Setting context |
| Feature Grid | Capability overview |
| Comparison | Competitive positioning |
| Chart | Data storytelling |
| Process / Steps | How it works |
| Timeline | Roadmap |
| Quote / Testimonial | Social proof |
| Closing / CTA | Next steps |

---

## Publishing to zo.space

When the user wants to publish a presentation to zo.space:

1. First create the local HTML file as normal
2. Run the publish script:
   ```bash
   bun /home/workspace/Skills/revealjs-presentation/scripts/publish.ts \
     --file /home/workspace/Inbox/my-deck.html \
     --route /presentations/my-deck \
     --public
   ```
3. The script extracts slides HTML, CSS variables, custom styles, chart functions, and SVG symbols from the HTML file
4. It generates a React page route component that:
   - Imports Reveal.js from the pre-installed package
   - Loads Chart.js from CDN dynamically if charts are present
   - Inlines all custom CSS
   - Initializes Reveal.js in a useEffect
   - Handles animations and chart building
5. The route is deployed via `update_space_route`
6. Check `get_space_errors()` after publishing

The published presentation will be live at `https://<handle>.zo.space<route>`.

### Manual zo.space Publishing (without the script)

If you need more control, you can manually create a page route. The pattern:

```tsx
import { useEffect, useRef } from "react";
import Reveal from "reveal.js";

export default function Presentation() {
  const deckRef = useRef<HTMLDivElement>(null);
  const revealRef = useRef<any>(null);

  useEffect(() => {
    // Load reveal.js CSS from CDN
    const revealCss = document.createElement("link");
    revealCss.rel = "stylesheet";
    revealCss.href = "https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css";
    document.head.appendChild(revealCss);

    const themeCss = document.createElement("link");
    themeCss.rel = "stylesheet";
    themeCss.href = "https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css";
    document.head.appendChild(themeCss);

    // Init Reveal after CSS loads
    themeCss.onload = () => {
      if (deckRef.current && !revealRef.current) {
        const deck = new Reveal(deckRef.current, {
          hash: true,
          transition: "fade",
          transitionSpeed: "fast",
          controls: true,
          progress: true,
          width: 1280,
          height: 720,
          margin: 0,
          embedded: false,
        });
        deck.initialize();
        revealRef.current = deck;
      }
    };

    return () => {
      revealRef.current?.destroy();
      revealCss.remove();
      themeCss.remove();
    };
  }, []);

  return (
    <>
      <style>{`
        /* your custom CSS here */
      `}</style>
      <div ref={deckRef} className="reveal" style={{ width: "100vw", height: "100vh" }}>
        <div className="slides">
          {/* <section> slides here </section> */}
        </div>
      </div>
    </>
  );
}
```

---

## Quick-Start Checklist

Before writing slides:
- [ ] Define CSS variables: `--bg`, `--dk`, `--accent`, `--f-sans`, `--f-mono`
- [ ] Choose font pair and add Google Fonts import
- [ ] Plan slide count and sequence
- [ ] Identify charts and assign unique canvas IDs
- [ ] Identify logos/icons to SVG-symbolize

When writing each slide:
- [ ] Wrap in `<div class="S">`
- [ ] Add `.pre` + animation class + delay to animated elements
- [ ] Use explicit `min-height` on `.cw` chart wrappers

After all slides:
- [ ] Build `chartMap` with 0-based slide indices
- [ ] One `buildXxx()` per chart
- [ ] Every `chartMap` key has a matching `<canvas id>`
- [ ] If publishing to zo.space, run publish script
