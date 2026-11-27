#!/usr/bin/env node
// Validates all SKILL.md and rule files in the skills/ directory.
// Checks: required frontmatter fields, field constraints, name matches directory.

import { readFileSync, readdirSync, statSync } from 'fs';
import { join, dirname, basename } from 'path';

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;
  const fm = {};
  let currentKey = null;
  for (const line of match[1].split('\n')) {
    if (/^\S/.test(line)) {
      const colon = line.indexOf(':');
      if (colon === -1) continue;
      currentKey = line.slice(0, colon).trim();
      fm[currentKey] = line.slice(colon + 1).trim().replace(/^["']|["']$/g, '');
    }
  }
  return fm;
}

function findFiles(dir, filename) {
  const results = [];
  for (const entry of readdirSync(dir)) {
    const path = join(dir, entry);
    if (statSync(path).isDirectory()) {
      results.push(...findFiles(path, filename));
    } else if (filename === '*.md' ? entry.endsWith('.md') : entry === filename) {
      results.push(path);
    }
  }
  return results;
}

let errors = 0;

// Validate SKILL.md files
for (const skillPath of findFiles('skills', 'SKILL.md')) {
  const content = readFileSync(skillPath, 'utf8');
  const fm = parseFrontmatter(content);
  const dir = basename(dirname(skillPath));

  if (!fm) {
    console.error(`❌ ${skillPath}: missing frontmatter`);
    errors++;
    continue;
  }

  if (!fm.name) {
    console.error(`❌ ${skillPath}: missing required field 'name'`);
    errors++;
  } else {
    if (fm.name !== dir) {
      console.error(`❌ ${skillPath}: 'name' (${fm.name}) does not match directory (${dir})`);
      errors++;
    }
    if (!/^[a-z0-9-]+$/.test(fm.name)) {
      console.error(`❌ ${skillPath}: 'name' must be lowercase alphanumeric and hyphens only`);
      errors++;
    }
    if (fm.name.length > 64) {
      console.error(`❌ ${skillPath}: 'name' exceeds 64 characters`);
      errors++;
    }
  }

  if (!fm.description) {
    console.error(`❌ ${skillPath}: missing required field 'description'`);
    errors++;
  } else if (fm.description.length > 1024) {
    console.error(`❌ ${skillPath}: 'description' exceeds 1024 characters`);
    errors++;
  }

  if (!errors) console.log(`✓ ${skillPath}`);
}

// Validate rule files (rules/*.md, excluding _ prefixed)
const RULE_IMPACTS = ['CRITICAL', 'HIGH', 'MEDIUM-HIGH', 'MEDIUM', 'LOW-MEDIUM', 'LOW'];

for (const rulePath of findFiles('skills', '*.md')) {
  if (!rulePath.includes('/rules/')) continue;
  if (basename(rulePath).startsWith('_')) continue;

  const content = readFileSync(rulePath, 'utf8');
  const fm = parseFrontmatter(content);

  if (!fm) {
    console.error(`❌ ${rulePath}: missing frontmatter`);
    errors++;
    continue;
  }

  if (!fm.title) {
    console.error(`❌ ${rulePath}: missing required field 'title'`);
    errors++;
  }

  if (!fm.impact) {
    console.error(`❌ ${rulePath}: missing required field 'impact'`);
    errors++;
  } else if (!RULE_IMPACTS.includes(fm.impact)) {
    console.error(`❌ ${rulePath}: 'impact' must be one of: ${RULE_IMPACTS.join(', ')}`);
    errors++;
  }

  if (!errors) console.log(`✓ ${rulePath}`);
}

if (errors > 0) {
  console.error(`\n${errors} error(s) found.`);
  process.exit(1);
} else {
  console.log('\nAll files valid.');
}
