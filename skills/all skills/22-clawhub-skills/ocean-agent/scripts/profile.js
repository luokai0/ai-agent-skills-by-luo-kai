#!/usr/bin/env node
'use strict';

// Ocean Agent — 黄页档案管家
//
// 命令:
//   node scripts/profile.js setup        初始化注册 + 填写档案（交互式）
//   node scripts/profile.js publish      发布/更新黄页
//   node scripts/profile.js show         查看当前黄页档案
//   node scripts/profile.js heartbeat    手动发送心跳
//   node scripts/profile.js unpublish    从黄页移除

const { createOceanBus } = require('oceanbus');
const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');

// ── Config ────────────────────────────────────────────────────────────────
const DATA_DIR = path.join(os.homedir(), '.oceanbus-agent');
const CRED_FILE = path.join(DATA_DIR, 'credentials.json');
const PROFILE_FILE = path.join(DATA_DIR, 'profile.json');

const SKILL_SOURCE = 'ocean-agent';

// ── Helpers ───────────────────────────────────────────────────────────────

function ensureDir() {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

function loadCredentials() {
  if (!fs.existsSync(CRED_FILE)) return null;
  try {
    const data = JSON.parse(fs.readFileSync(CRED_FILE, 'utf-8'));
    if (data.source && data.source !== SKILL_SOURCE) return null;
    return data;
  } catch (_) { return null; }
}

function saveCredentials(agentId, apiKey, openid) {
  ensureDir();
  fs.writeFileSync(CRED_FILE, JSON.stringify({
    agent_id: agentId, api_key: apiKey, openid: openid,
    source: SKILL_SOURCE, created_at: new Date().toISOString()
  }, null, 2));
}

function loadProfile() {
  if (!fs.existsSync(PROFILE_FILE)) return null;
  try { return JSON.parse(fs.readFileSync(PROFILE_FILE, 'utf-8')); } catch (_) { return null; }
}

function saveProfile(profile) {
  ensureDir();
  fs.writeFileSync(PROFILE_FILE, JSON.stringify(profile, null, 2));
}

function shortId(openid) {
  return openid.slice(0, 16) + '...';
}

// ── Interactive setup ─────────────────────────────────────────────────────

function ask(rl, question) {
  return new Promise(resolve => {
    rl.question(question, answer => resolve(answer.trim()));
  });
}

async function interactiveSetup() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  console.log('\n═══ Ocean Agent 初始化设置 ═══\n');
  console.log('我将引导你完成 OceanBus 注册和代理人档案填写。\n');

  // ── Step 1: Register on OceanBus ──
  console.log('── 第1步：注册 OceanBus 身份 ──');
  console.log('正在连接 OceanBus 网络...\n');

  let ob;
  try {
    ob = await createOceanBus({ keyStore: { type: 'memory' } });
    const reg = await ob.register();
    const openid = await ob.getOpenId();
    saveCredentials(reg.agent_id, reg.api_key, openid);

    console.log('✅ 注册成功！');
    console.log('  你的 OpenID: ' + openid);
    console.log('  (简写: ' + shortId(openid) + ')\n');

    // ── Step 2: Profile info ──
    console.log('── 第2步：填写代理人档案 ──');
    console.log('这些信息会显示在 OceanBus 黄页上，帮助客户找到你。\n');

    const profile = {};

    profile.name = await ask(rl, '姓名/称呼（如：张三）: ');
    profile.city = await ask(rl, '主要服务城市（如：北京）: ');
    profile.district = await ask(rl, '主要服务区域（如：朝阳）: ');
    profile.experience_years = await ask(rl, '从业年限（如：8）: ');
    profile.specialties = await ask(rl, '擅长险种，逗号分隔（如：重疾险,医疗险,寿险）: ');
    profile.company = await ask(rl, '所属保险公司（可选，如：平安人寿）: ');
    profile.certifications = await ask(rl, '资质证书，逗号分隔（可选，如：RFC,ChFP）: ');
    profile.service_feature = await ask(rl, '服务特色，一句话（如：专注家庭保障规划，已服务500+家庭）: ');

    // Parse comma-separated fields
    profile.specialties = profile.specialties.split(',').map(s => s.trim()).filter(Boolean);
    profile.certifications = profile.certifications.split(',').map(s => s.trim()).filter(Boolean);
    profile.experience_years = parseInt(profile.experience_years, 10) || 0;

    saveProfile(profile);

    console.log('\n✅ 档案已保存！\n');
    console.log('档案预览:');
    console.log('  姓名: ' + profile.name);
    console.log('  城市: ' + profile.city + ' ' + profile.district);
    console.log('  从业: ' + profile.experience_years + '年');
    console.log('  擅长: ' + profile.specialties.join('、'));
    console.log('  公司: ' + (profile.company || '未填写'));
    console.log('  特色: ' + profile.service_feature);
    console.log('\n下一步: node scripts/profile.js publish  发布到黄页');
  } finally {
    rl.close();
    if (ob) await ob.destroy().catch(() => {});
  }
}

// ── Build tags and description from profile ──

function buildTags(profile) {
  const tags = ['insurance'];

  // Add specialty tags
  for (const s of (profile.specialties || [])) {
    tags.push(s);
  }

  // Add location tags
  if (profile.city) tags.push(profile.city);
  if (profile.district) tags.push(profile.district);

  return tags;
}

function buildDescription(profile) {
  const parts = [];
  if (profile.name) parts.push(profile.name);
  if (profile.company) parts.push(profile.company);
  if (profile.specialties && profile.specialties.length > 0) {
    parts.push('擅长' + profile.specialties.join('/'));
  }
  if (profile.experience_years) {
    parts.push('从业' + profile.experience_years + '年');
  }
  if (profile.service_feature) parts.push(profile.service_feature);
  if (profile.city) {
    const loc = profile.district ? profile.city + profile.district : profile.city;
    parts.push('服务区域:' + loc);
  }
  return parts.join(' | ');
}

// ── Commands ──────────────────────────────────────────────────────────────

async function cmdSetup() {
  const existing = loadCredentials();
  const existingProfile = loadProfile();

  if (existing && existingProfile) {
    console.log('已注册。当前档案:');
    console.log('  姓名: ' + existingProfile.name);
    console.log('  OpenID: ' + shortId(existing.openid));
    console.log('');
    console.log('如需重新设置，删除 ' + DATA_DIR + ' 后重试。');
    return;
  }

  await interactiveSetup();
}

async function cmdPublish() {
  const creds = loadCredentials();
  if (!creds) { console.log('尚未注册。运行: node scripts/profile.js setup'); return; }

  const profile = loadProfile();
  if (!profile) { console.log('尚未填写档案。运行: node scripts/profile.js setup'); return; }

  const tags = buildTags(profile);
  const description = buildDescription(profile);

  console.log('正在发布到 OceanBus 黄页...');
  console.log('  标签: ' + tags.join(', '));
  console.log('  描述: ' + description);

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key },
  });

  const key = await ob.createServiceKey();
  ob.l1.yellowPages.setIdentity(creds.openid, key.signer, key.publicKey);

  try {
    const result = await ob.l1.yellowPages.registerService(tags, description);
    console.log('✅ 已发布到黄页！');
    console.log('  客户可通过以下标签搜索到你: ' + tags.join(', '));
    console.log('');
    console.log('保持在线: 建议将 "node scripts/listen.js" 设置为常驻运行。');
    console.log('定期心跳: 建议设置定时任务运行 "node scripts/profile.js heartbeat"。');
  } catch (e) {
    if (e.message && e.message.includes('11000')) {
      console.log('已发布过。更新描述...');
      await ob.l1.yellowPages.updateService(tags, description);
      console.log('✅ 黄页档案已更新。');
    } else {
      console.log('❌ 发布失败: ' + e.message);
    }
  }

  await ob.destroy();
}

async function cmdShow() {
  const profile = loadProfile();
  const creds = loadCredentials();

  if (!profile) { console.log('尚未填写档案。运行: node scripts/profile.js setup'); return; }

  console.log('\n═══ 你的黄页档案 ═══\n');
  console.log('OpenID: ' + (creds ? creds.openid : '(未注册)'));
  console.log('');
  console.log('标签: ' + buildTags(profile).join(', '));
  console.log('描述: ' + buildDescription(profile));
  console.log('');
  console.log('── 原始档案 ──');
  console.log(JSON.stringify(profile, null, 2));
}

async function cmdHeartbeat() {
  const creds = loadCredentials();
  if (!creds) { console.log('尚未注册。运行: node scripts/profile.js setup'); return; }

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key },
  });

  const key = await ob.createServiceKey();
  ob.l1.yellowPages.setIdentity(creds.openid, key.signer, key.publicKey);

  try {
    await ob.l1.yellowPages.heartbeat();
    console.log('✅ 心跳已发送 ' + new Date().toLocaleString('zh-CN'));
  } catch (e) {
    console.log('❌ 心跳失败: ' + e.message);
  }

  await ob.destroy();
}

async function cmdUnpublish() {
  const creds = loadCredentials();
  if (!creds) { console.log('尚未注册。运行: node scripts/profile.js setup'); return; }

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key },
  });

  const key = await ob.createServiceKey();
  ob.l1.yellowPages.setIdentity(creds.openid, key.signer, key.publicKey);

  try {
    await ob.l1.yellowPages.deregisterService();
    console.log('✅ 已从黄页移除。');
  } catch (e) {
    console.log('❌ 移除失败: ' + e.message);
  }

  await ob.destroy();
}

// ── Main ──────────────────────────────────────────────────────────────────

async function main() {
  const cmd = process.argv[2];

  if (!cmd || cmd === 'help' || cmd === '--help') {
    console.log('Ocean Agent — 黄页档案管家');
    console.log('');
    console.log('命令:');
    console.log('  node scripts/profile.js setup        初始化注册 + 填写档案');
    console.log('  node scripts/profile.js publish      发布/更新黄页');
    console.log('  node scripts/profile.js show         查看当前黄页档案');
    console.log('  node scripts/profile.js heartbeat    发送心跳');
    console.log('  node scripts/profile.js unpublish    从黄页移除');
    return;
  }

  try {
    switch (cmd) {
      case 'setup':    await cmdSetup();    break;
      case 'publish':  await cmdPublish();  break;
      case 'show':     await cmdShow();     break;
      case 'heartbeat': await cmdHeartbeat(); break;
      case 'unpublish': await cmdUnpublish(); break;
      default:
        console.log('未知命令: ' + cmd);
        console.log('运行 "node scripts/profile.js help" 查看帮助。');
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
