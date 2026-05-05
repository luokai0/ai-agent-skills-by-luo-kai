#!/usr/bin/env node
'use strict';

// Ocean Agent — 实时监听 + 自动首响
//
// 持续监听 OceanBus 收件箱。
// 收到已知联系人的消息 → 直接展示
// 收到未知联系人的消息 → 展示 + 自动回复（自我介绍 + 需求问卷）
//
// 用法:
//   node scripts/listen.js          持续监听
//   node scripts/listen.js --once   检查一次后退出

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

function shortId(openid) {
  return openid.slice(0, 16) + '...';
}

function formatTime(iso) {
  try { return new Date(iso).toLocaleTimeString('zh-CN', { hour12: false }); } catch (_) { return iso; }
}

function loadProfile() {
  const profileFile = path.join(DATA_DIR, 'profile.json');
  if (!fs.existsSync(profileFile)) return null;
  try { return JSON.parse(fs.readFileSync(profileFile, 'utf-8')); } catch (_) { return null; }
}

// ── Auto-reply ────────────────────────────────────────────────────────────

function buildAutoReply(profile) {
  const name = profile ? profile.name : '保险顾问';
  const company = profile && profile.company ? profile.company + ' ' : '';
  const years = profile ? profile.experience_years : 0;

  return '【自动回复】您好！我是' + name + '，' + company + '保险顾问' +
    (years ? '，从业' + years + '年' : '') + '。\n' +
    '\n' +
    '很高兴为您服务！为了给您更精准的建议，想先了解几个信息：\n' +
    '① 您主要关注哪方面的保障？（如重疾、医疗、意外、养老等）\n' +
    '② 是为自己还是家人咨询？\n' +
    '③ 之前是否有过商业保险？\n' +
    '\n' +
    '期待您的回复！';
}

// ── Message processing ────────────────────────────────────────────────────

async function processMessage(msg, ob, creds, profile) {
  const contacts = loadContacts();
  const name = resolveName(msg.from_openid, contacts);
  const senderDisplay = name
    ? name + ' (' + shortId(msg.from_openid) + ')'
    : msg.from_openid;

  // Display message
  console.log('');
  console.log('═══ ' + '═'.repeat(50));
  if (name) {
    console.log('📩 ' + senderDisplay + ' · ' + formatTime(msg.created_at));
  } else {
    console.log('🆕 新客户 · ' + senderDisplay + ' · ' + formatTime(msg.created_at));
  }
  console.log('───' + '─'.repeat(50));
  console.log(msg.content);
  console.log('═══' + '═'.repeat(50));
  console.log('');

  // For unknown senders, auto-send introduction + intake questions
  if (!name) {
    const autoReply = buildAutoReply(profile);
    console.log('🤖 自动发送首响...');
    console.log(autoReply);
    console.log('');

    try {
      await ob.send(msg.from_openid, autoReply);
      console.log('✅ 首响已发送');
    } catch (e) {
      console.log('⚠️  首响发送失败: ' + e.message);
    }

    // Add to contacts as unknown with intake stage
    contacts['客户_' + shortId(msg.from_openid)] = {
      openid: msg.from_openid,
      stage: '新线索',
      source: '黄页',
      first_contact: new Date().toISOString(),
      last_contact: msg.created_at,
      history: [{ direction: 'in', content: msg.content, time: msg.created_at }]
    };
    saveContacts(contacts);
  } else {
    // Update last contact time for known contacts
    const info = contacts[name];
    if (info && typeof info === 'object') {
      info.last_contact = msg.created_at;
      info.history = info.history || [];
      info.history.push({ direction: 'in', content: msg.content, time: msg.created_at });
      saveContacts(contacts);
    }
  }
}

// ── Main ──────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  const once = args.includes('--once');

  const creds = loadCredentials();
  if (!creds) {
    console.log('尚未注册。运行: node scripts/profile.js setup');
    process.exit(1);
  }

  const profile = loadProfile();
  const contacts = loadContacts();
  const lastSeq = loadCursor();

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key },
  });

  console.log('[Ocean Agent] ' + (once ? '检查消息...' : '实时监听中...'));
  if (!once) {
    console.log('  姓名: ' + (profile ? profile.name : '未设置档案'));
    console.log('  OpenID: ' + shortId(creds.openid));
    console.log('  当前客户数: ' + Object.keys(contacts).length);
    console.log('  按 Ctrl+C 停止\n');
  }

  let maxSeq = lastSeq;
  let firstCheck = true;

  const checkMessages = async () => {
    try {
      const messages = await ob.sync(firstCheck && lastSeq > 0 ? lastSeq : undefined);
      firstCheck = false;

      for (const msg of messages) {
        const seq = typeof msg.seq_id === 'number' ? msg.seq_id : parseInt(msg.seq_id, 10);
        if (!isNaN(seq) && seq > maxSeq) maxSeq = seq;
        await processMessage(msg, ob, creds, profile);
      }

      if (maxSeq > lastSeq) saveCursor(maxSeq);
    } catch (e) {
      // Silently handle polling errors — retry on next cycle
    }
  };

  if (once) {
    await checkMessages();
    if (maxSeq === lastSeq) console.log('没有新消息。');
  } else {
    // Use startListening for real-time delivery
    ob.startListening((msg) => {
      const seq = typeof msg.seq_id === 'number' ? msg.seq_id : parseInt(msg.seq_id, 10);
      if (!isNaN(seq) && seq > maxSeq) maxSeq = seq;
      processMessage(msg, ob, creds, profile).then(() => {
        if (maxSeq > lastSeq) saveCursor(maxSeq);
      }).catch(() => {
        // Silently handle per-message processing errors
      });
    });

    // Also do an initial sync to catch any messages while we were offline
    await checkMessages();

    // Keep running
    await new Promise(() => {});
  }
}

main().catch(err => {
  if (err.message && (err.message.includes('ECONNREFUSED') || err.message.includes('ENOTFOUND'))) {
    console.error('无法连接 OceanBus 网络。请检查互联网连接。');
  } else {
    console.error('错误: ' + err.message);
  }
  process.exit(1);
});
