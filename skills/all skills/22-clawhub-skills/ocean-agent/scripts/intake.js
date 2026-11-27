#!/usr/bin/env node
'use strict';

// Ocean Agent — 线索管理
//
// 命令:
//   node scripts/intake.js check              查看新消息
//   node scripts/intake.js reply <oid> <msg>   回复客户
//   node scripts/intake.js classify <oid> <stage>  修改线索阶段
//   node scripts/intake.js note <oid> <text>   添加客户备注
//   node scripts/intake.js summary             线索管道总览

const { createOceanBus } = require('oceanbus');
const fs = require('fs');
const path = require('path');
const os = require('os');

// ── Config ────────────────────────────────────────────────────────────────
const DATA_DIR = path.join(os.homedir(), '.oceanbus-agent');
const CRED_FILE = path.join(DATA_DIR, 'credentials.json');
const CONTACTS_FILE = path.join(DATA_DIR, 'contacts.json');
const CURSOR_FILE = path.join(DATA_DIR, 'cursor.json');

const SKILL_SOURCE = 'ocean-agent';

// Pipeline stages
const STAGES = ['新线索', '需求采集中', '方案已发', '待成交', '已成交', '已流失'];

// ── Helpers ───────────────────────────────────────────────────────────────

function ensureDir() { fs.mkdirSync(DATA_DIR, { recursive: true }); }

function loadCredentials() {
  if (!fs.existsSync(CRED_FILE)) return null;
  try {
    const data = JSON.parse(fs.readFileSync(CRED_FILE, 'utf-8'));
    if (data.source && data.source !== SKILL_SOURCE) return null;
    return data;
  } catch (_) { return null; }
}

function loadContacts() {
  ensureDir();
  if (!fs.existsSync(CONTACTS_FILE)) return {};
  try { return JSON.parse(fs.readFileSync(CONTACTS_FILE, 'utf-8')); } catch (_) { return {}; }
}

function saveContacts(contacts) {
  ensureDir();
  fs.writeFileSync(CONTACTS_FILE, JSON.stringify(contacts, null, 2));
}

function loadCursor() {
  if (!fs.existsSync(CURSOR_FILE)) return 0;
  try { return JSON.parse(fs.readFileSync(CURSOR_FILE, 'utf-8')).last_seq || 0; } catch (_) { return 0; }
}

function saveCursor(seq) {
  ensureDir();
  fs.writeFileSync(CURSOR_FILE, JSON.stringify({ last_seq: seq }));
}

function resolveName(openid, contacts) {
  for (const [name, info] of Object.entries(contacts)) {
    const id = typeof info === 'string' ? info : info.openid;
    if (id === openid) return name;
  }
  return null;
}

function findContact(query, contacts) {
  // Search by name or OpenID (partial match)
  for (const [name, info] of Object.entries(contacts)) {
    const id = typeof info === 'string' ? info : info.openid;
    if (name === query || id === query || id.startsWith(query) || name.includes(query)) {
      return { name, info: typeof info === 'string' ? { openid: info } : info };
    }
  }
  return null;
}

function shortId(openid) {
  return openid.slice(0, 16) + '...';
}

function formatTime(iso) {
  try { return new Date(iso).toLocaleString('zh-CN', { hour12: false }); } catch (_) { return iso; }
}

function daysAgo(iso) {
  try {
    const diff = Date.now() - new Date(iso).getTime();
    return Math.floor(diff / (1000 * 60 * 60 * 24));
  } catch (_) { return '?'; }
}

// ── Commands ──────────────────────────────────────────────────────────────

async function cmdCheck() {
  const creds = loadCredentials();
  if (!creds) { console.log('尚未注册。运行: node scripts/profile.js setup'); return; }

  const contacts = loadContacts();
  const lastSeq = loadCursor();

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key },
  });

  const messages = await ob.sync(lastSeq > 0 ? lastSeq : undefined);

  if (messages.length === 0) {
    console.log('没有新消息。');
  } else {
    let maxSeq = lastSeq;
    for (const msg of messages) {
      const name = resolveName(msg.from_openid, contacts);
      const from = name || shortId(msg.from_openid);
      const isNew = !name;

      console.log('');
      console.log((isNew ? '🆕 ' : '📩 ') + from + ' · ' + formatTime(msg.created_at));
      console.log('─'.repeat(50));
      console.log(msg.content);
      console.log('');

      const seq = typeof msg.seq_id === 'number' ? msg.seq_id : parseInt(msg.seq_id, 10);
      if (!isNaN(seq) && seq > maxSeq) maxSeq = seq;
    }

    if (maxSeq > lastSeq) saveCursor(maxSeq);
  }

  await ob.destroy();
}

async function cmdReply(target, message) {
  if (!target || !message) {
    console.log('用法: node scripts/intake.js reply <名字|OpenID> <消息>');
    return;
  }

  const creds = loadCredentials();
  if (!creds) { console.log('尚未注册。运行: node scripts/profile.js setup'); return; }

  const contacts = loadContacts();
  const contact = findContact(target, contacts);
  const openid = contact ? contact.info.openid : target;
  const displayName = contact ? contact.name : shortId(target);

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key },
  });

  await ob.send(openid, message);
  console.log('✅ 已发送 → ' + displayName);

  // Update contact last_contact
  if (contact && typeof contact.info === 'object') {
    contact.info.last_contact = new Date().toISOString();
    saveContacts(contacts);
  }

  await ob.destroy();
}

async function cmdClassify(target, stage) {
  if (!target || !stage) {
    console.log('用法: node scripts/intake.js classify <名字|OpenID> <阶段>');
    console.log('阶段: ' + STAGES.join(' | '));
    return;
  }

  if (!STAGES.includes(stage)) {
    console.log('无效阶段: ' + stage);
    console.log('可选: ' + STAGES.join(' | '));
    return;
  }

  const contacts = loadContacts();
  const contact = findContact(target, contacts);

  if (!contact) {
    console.log('未找到客户: ' + target);
    return;
  }

  const oldStage = (typeof contact.info === 'object' ? contact.info.stage : null) || '未知';

  if (typeof contact.info === 'string') {
    contacts[contact.name] = { openid: contact.info, stage: stage };
  } else {
    contact.info.stage = stage;
  }

  saveContacts(contacts);
  console.log('✅ ' + contact.name + ': ' + oldStage + ' → ' + stage);
}

async function cmdNote(target, text) {
  if (!target || !text) {
    console.log('用法: node scripts/intake.js note <名字|OpenID> <备注内容>');
    return;
  }

  const contacts = loadContacts();
  const contact = findContact(target, contacts);

  if (!contact) {
    console.log('未找到客户: ' + target);
    return;
  }

  if (typeof contact.info === 'string') {
    contacts[contact.name] = { openid: contact.info, notes: [text] };
  } else {
    contact.info.notes = contact.info.notes || [];
    contact.info.notes.push({ text, time: new Date().toISOString() });
  }

  saveContacts(contacts);
  console.log('✅ 已为 ' + contact.name + ' 添加备注');
}

async function cmdSummary() {
  const contacts = loadContacts();

  if (Object.keys(contacts).length === 0) {
    console.log('暂无客户。');
    console.log('开启监听后，新客户会自动出现在这里。');
    return;
  }

  console.log('\n═══ 线索管道总览 ═══');
  console.log('总客户数: ' + Object.keys(contacts).length);
  console.log('');

  // Group by stage
  const byStage = {};
  for (const stage of STAGES) byStage[stage] = [];
  byStage['未知'] = [];

  for (const [name, info] of Object.entries(contacts)) {
    const data = typeof info === 'string' ? { openid: info, stage: '未知' } : info;
    const stage = data.stage || '未知';
    if (!byStage[stage]) byStage[stage] = [];
    byStage[stage].push({ name, ...data });
  }

  // Print pipeline
  const stageColors = {
    '新线索': '🔵', '需求采集中': '🟡', '方案已发': '🟠',
    '待成交': '🟢', '已成交': '✅', '已流失': '❌', '未知': '⚪'
  };

  for (const stage of STAGES.concat(['未知'])) {
    const items = byStage[stage];
    if (items.length === 0) continue;

    const icon = stageColors[stage] || '⚪';
    console.log(icon + ' ' + stage + ' (' + items.length + '人)');
    for (const c of items) {
      const last = c.last_contact ? ' | 最后联系: ' + daysAgo(c.last_contact) + '天前' : '';
      console.log('  - ' + c.name + ' | ' + shortId(c.openid) + last);
    }
    console.log('');
  }

  // Alerts
  console.log('── 需要关注的线索 ──');
  let alerts = 0;
  const thresholds = { '新线索': 1, '需求采集中': 2, '方案已发': 3, '待成交': 2 };

  for (const [stage, days] of Object.entries(thresholds)) {
    const items = byStage[stage] || [];
    for (const c of items) {
      const ago = c.last_contact ? daysAgo(c.last_contact) : 999;
      if (typeof ago === 'number' && ago >= days) {
        console.log('⚠️  ' + c.name + ' — ' + stage + '阶段，最后联系' + ago + '天前，建议跟进');
        alerts++;
      }
    }
  }

  if (alerts === 0) console.log('✅ 所有线索都在正常跟进周期内');
  console.log('');
}

// ── Main ──────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (!cmd || cmd === 'help' || cmd === '--help') {
    console.log('Ocean Agent — 线索管理');
    console.log('');
    console.log('命令:');
    console.log('  node scripts/intake.js check              查看新消息');
    console.log('  node scripts/intake.js reply <oid> <msg>   回复客户');
    console.log('  node scripts/intake.js classify <oid> <stage>  修改线索阶段');
    console.log('  node scripts/intake.js note <oid> <text>   添加客户备注');
    console.log('  node scripts/intake.js summary             线索管道总览');
    console.log('');
    console.log('线索阶段: ' + STAGES.join(' → '));
    return;
  }

  try {
    switch (cmd) {
      case 'check':    await cmdCheck();   break;
      case 'reply':    await cmdReply(args[1], args.slice(2).join(' ')); break;
      case 'classify': await cmdClassify(args[1], args[2]); break;
      case 'note':     await cmdNote(args[1], args.slice(2).join(' ')); break;
      case 'summary':  await cmdSummary(); break;
      default:
        console.log('未知命令: ' + cmd);
        console.log('运行 "node scripts/intake.js help" 查看帮助。');
    }
  } catch (err) {
    if (err.message && (err.message.includes('ECONNREFUSED') || err.message.includes('ENOTFOUND'))) {
      console.error('无法连接 OceanBus 网络。请检查互联网连接。');
    } else {
      console.error('错误: ' + err.message);
    }
    process.exit(1);
  }
}

main();
