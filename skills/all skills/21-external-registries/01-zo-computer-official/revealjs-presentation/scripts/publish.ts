#!/usr/bin/env bun

import { parseArgs } from "util";
import { readFileSync } from "fs";

const { values } = parseArgs({
  args: Bun.argv.slice(2),
  options: {
    file: { type: "string", short: "f" },
    route: { type: "string", short: "r" },
    public: { type: "boolean", default: false },
    help: { type: "boolean", short: "h" },
  },
  strict: true,
});

if (values.help || !values.file || !values.route) {
  console.log(`Usage: bun publish.ts --file <html-path> --route <zo-space-path> [--public]

Converts a self-contained Reveal.js HTML presentation into a zo.space page route.

Options:
  --file, -f    Path to the HTML presentation file (required)
  --route, -r   zo.space route path, e.g. /presentations/my-deck (required)
  --public      Make the route publicly accessible (default: private)
  --help, -h    Show this help

Examples:
  bun publish.ts --file /home/workspace/Inbox/pitch.html --route /pitch --public
  bun publish.ts -f deck.html -r /presentations/q1-review`);
  process.exit(values.help ? 0 : 1);
}

const html = readFileSync(values.file!, "utf-8");

// Extract content between tags
function extractBetween(content: string, startTag: string, endTag: string): string {
  const startIdx = content.indexOf(startTag);
  if (startIdx === -1) return "";
  const afterStart = startIdx + startTag.length;
  const endIdx = content.indexOf(endTag, afterStart);
  if (endIdx === -1) return "";
  return content.slice(afterStart, endIdx).trim();
}

// Extract all content between matching tags (multiple occurrences)
function extractAllBetween(content: string, startTag: string, endTag: string): string[] {
  const results: string[] = [];
  let searchFrom = 0;
  while (true) {
    const startIdx = content.indexOf(startTag, searchFrom);
    if (startIdx === -1) break;
    const afterStart = startIdx + startTag.length;
    const endIdx = content.indexOf(endTag, afterStart);
    if (endIdx === -1) break;
    results.push(content.slice(afterStart, endIdx).trim());
    searchFrom = endIdx + endTag.length;
  }
  return results;
}

// 1. Extract custom CSS from <style> block
const styleMatch = html.match(/<style>([\s\S]*?)<\/style>/);
const customCss = styleMatch ? styleMatch[1].trim() : "";

// 2. Extract SVG symbols block
const svgSymbolsMatch = html.match(/<svg\s+style="display:none[^"]*">([\s\S]*?)<\/svg>/);
const svgSymbols = svgSymbolsMatch ? svgSymbolsMatch[0] : "";

// 3. Extract slides HTML
const slidesHtml = extractBetween(html, '<div class="slides">', '</div>\n</div>');

// 4. Extract chart builder functions and chartMap
const scriptBlocks = extractAllBetween(html, "<script>", "</script>");
let chartFunctions = "";
let chartMapStr = "{}";

for (const block of scriptBlocks) {
  // Skip the reveal.js CDN script tag content (which would be empty anyway)
  if (block.includes("Reveal.initialize") || block.includes("chartMap")) {
    // Extract chartMap definition
    const mapMatch = block.match(/const\s+chartMap\s*=\s*(\{[^}]*\})/);
    if (mapMatch) chartMapStr = mapMatch[1];

    // Extract all function definitions (chart builders)
    const funcRegex = /function\s+\w+\s*\([^)]*\)\s*\{[\s\S]*?\n\}/g;
    const funcs = block.match(funcRegex);
    if (funcs) {
      chartFunctions = funcs.join("\n\n");
    }
  }
}

const hasCharts = chartFunctions.length > 0 && chartMapStr !== "{}";

// 5. Extract Google Fonts link
const fontsMatch = html.match(/href="(https:\/\/fonts\.googleapis\.com\/css2[^"]*)"/);
const fontsUrl = fontsMatch ? fontsMatch[1] : "";

// 6. Extract title
const titleMatch = html.match(/<title>(.*?)<\/title>/);
const title = titleMatch ? titleMatch[1] : "Presentation";

// Escape backticks and ${} in extracted HTML/CSS for template literal safety
function escapeForTemplateLiteral(str: string): string {
  return str.replace(/\\/g, "\\\\").replace(/`/g, "\\`").replace(/\$\{/g, "\\${");
}

// Build the React component
const component = `import { useEffect, useRef } from "react";
import Reveal from "reveal.js";

export default function Presentation() {
  const deckRef = useRef<HTMLDivElement>(null);
  const revealRef = useRef<any>(null);

  useEffect(() => {
    const revealCss = document.createElement("link");
    revealCss.rel = "stylesheet";
    revealCss.href = "https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css";
    document.head.appendChild(revealCss);

    const themeCss = document.createElement("link");
    themeCss.rel = "stylesheet";
    themeCss.href = "https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css";
    document.head.appendChild(themeCss);
${fontsUrl ? `
    const fontLink = document.createElement("link");
    fontLink.rel = "stylesheet";
    fontLink.href = "${fontsUrl}";
    document.head.appendChild(fontLink);
` : ""}
    document.title = ${JSON.stringify(title)};
${hasCharts ? `
    const chartScript = document.createElement("script");
    chartScript.src = "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js";
    chartScript.onload = () => initDeck();
    document.head.appendChild(chartScript);
` : ""}
    function initDeck() {
      if (!deckRef.current || revealRef.current) return;

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

${hasCharts ? `
      ${chartFunctions.replace(/\n/g, "\n      ")}

      const chartMap: Record<number, () => void> = ${chartMapStr};
      const built = new Set<number>();
` : ""}

      function animateSlide(slide: Element) {
        slide.querySelectorAll(".pre").forEach(el => el.classList.remove("pre"));
      }

      deck.on("slidechanged", (event: any) => {
        const slide = deck.getSlide(event.indexh);
        if (slide) animateSlide(slide);
${hasCharts ? `        if (chartMap[event.indexh] && !built.has(event.indexh)) {
          built.add(event.indexh);
          chartMap[event.indexh]();
        }` : ""}
      });

      deck.on("ready", () => {
        const slide = deck.getSlide(0);
        if (slide) animateSlide(slide);
${hasCharts ? `        if (chartMap[0] && !built.has(0)) {
          built.add(0);
          chartMap[0]();
        }` : ""}
      });

      deck.initialize();
      revealRef.current = deck;
    }

${!hasCharts ? `
    themeCss.onload = () => initDeck();
` : ""}

    return () => {
      revealRef.current?.destroy();
      revealRef.current = null;
      revealCss.remove();
      themeCss.remove();
${fontsUrl ? `      fontLink.remove();` : ""}
    };
  }, []);

  return (
    <>
      <style dangerouslySetInnerHTML={{ __html: \`${escapeForTemplateLiteral(customCss)}\` }} />
      <div style={{ width: "100vw", height: "100vh", overflow: "hidden" }}>
${svgSymbols ? `        <div dangerouslySetInnerHTML={{ __html: \`${escapeForTemplateLiteral(svgSymbols)}\` }} />` : ""}
        <div ref={deckRef} className="reveal">
          <div className="slides" dangerouslySetInnerHTML={{ __html: \`${escapeForTemplateLiteral(slidesHtml)}\` }} />
        </div>
      </div>
    </>
  );
}
`;

// Output the generated component to stdout for inspection
console.log("Generated zo.space route component:");
console.log("Route:", values.route);
console.log("Public:", values.public);
console.log("Has charts:", hasCharts);
console.log("Has fonts:", !!fontsUrl);
console.log("Has SVG symbols:", !!svgSymbols);
console.log("Slides HTML length:", slidesHtml.length);
console.log("Custom CSS length:", customCss.length);
console.log("---");

// Write the component to a temp file for the Zo tool to pick up
const outPath = `/home/.z/workspaces/temp-route-${Date.now()}.tsx`;
Bun.write(outPath, component);
console.log("Component written to:", outPath);
console.log("\nTo deploy, use update_space_route with:");
console.log(`  path: ${values.route}`);
console.log(`  route_type: page`);
console.log(`  public: ${values.public}`);
console.log(`  code: <contents of ${outPath}>`);
