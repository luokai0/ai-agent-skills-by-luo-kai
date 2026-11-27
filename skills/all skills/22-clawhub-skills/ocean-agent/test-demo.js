#!/usr/bin/env node
'use strict';

// Ocean Agent — 保险代理人完整演示
//
// 场景:
//   代理人张三(8年健康险专家,北京朝阳)在黄页上线
//   客户王先生搜索"重疾险 北京"发现张三
//   王先生发起咨询 → 张三自动首响 → 需求采集 → 方案跟进 → 会面协商 → 成交打标签
//
// 运行: node test-demo.js

const { createOceanBus } = require('oceanbus');

// ── Helpers ────────────────────────────────────────────────────────────────

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
function shortId(s) { return s.slice(0, 18) + '...'; }
function now() { return new Date().toLocaleTimeString('zh-CN', { hour12: false }); }

let step = 0;
function phase(title) {
  step++;
  const bar = '─'.repeat(60);
  console.log('\n' + bar);
  console.log('  第 ' + step + ' 步: ' + title);
  console.log(bar + '\n');
}

function agentThink(name, thoughts) {
  console.log('  🤖 ' + name + ' Agent 分析:');
  for (const t of thoughts) {
    console.log('     ' + t);
  }
  console.log('');
}

function oceanbusMsg(from, to, content) {
  console.log('  ── OceanBus 消息 ─────────────────────────────');
  console.log('  ' + from + ' ──→ ' + to);
  const lines = content.split('\n');
  for (const line of lines) {
    console.log('  ' + line);
  }
  console.log('  ─────────────────────────────────────────────\n');
}

// ── Main Demo ──────────────────────────────────────────────────────────────

async function main() {
  console.log('╔══════════════════════════════════════════════════════════╗');
  console.log('║     Ocean Agent — 保险代理人获客→成交 完整演示           ║');
  console.log('║     基于 OceanBus 网络 · 零服务器部署                    ║');
  console.log('╚══════════════════════════════════════════════════════════╝\n');

  console.log('场景:');
  console.log('  张三 — 健康险专家，从业8年，北京朝阳');
  console.log('  王先生 — 32岁IT工程师，已婚有小孩，想买重疾险');
  console.log('  王先生通过 OceanBus 黄页搜索 "重疾险 北京" 找到张三\n');

  // ═══════════════════════════════════════════════════════════
  // Phase 1: 张三注册 + 发布黄页
  // ═══════════════════════════════════════════════════════════

  phase('代理人张三注册 OceanBus + 发布黄页档案');

  const zhang = await createOceanBus({ keyStore: { type: 'memory' } });
  await zhang.register();
  const zhangOpenid = await zhang.getOpenId();

  console.log('  ✅ 张三注册成功');
  console.log('     OpenID: ' + zhangOpenid);
  console.log('     (简写: ' + shortId(zhangOpenid) + ')\n');

  // 张三填写档案
  console.log('  📋 张三的档案:');
  console.log('     姓名: 张三');
  console.log('     城市: 北京 · 朝阳');
  console.log('     从业: 8年');
  console.log('     擅长: 重疾险、医疗险、寿险');
  console.log('     公司: 平安人寿');
  console.log('     特色: 专注家庭保障规划，已服务500+家庭\n');

  // 发布黄页
  const zhangKey = await zhang.createServiceKey();
  zhang.l1.yellowPages.setIdentity(zhangOpenid, zhangKey.signer, zhangKey.publicKey);

  const tags = ['insurance', '重疾险', '医疗险', '寿险', '北京', '朝阳'];
  const description = '张三 | 平安人寿 | 擅长重疾险/医疗险/寿险 | 从业8年 | 专注家庭保障规划，已服务500+家庭 | 服务区域:北京朝阳';

  try {
    await zhang.l1.yellowPages.registerService(tags, description);
    console.log('  ✅ 黄页发布成功');
    console.log('     标签: ' + tags.join(', '));
    console.log('     描述: ' + description + '\n');
  } catch (e) {
    console.log('  ⚠️  黄页发布: ' + e.message + ' (可能已发布过)\n');
  }

  // 张三开启监听
  const zhangInbox = [];
  zhang.startListening(m => zhangInbox.push(m));
  console.log('  👂 张三开启实时监听...\n');

  await sleep(2000);

  // ═══════════════════════════════════════════════════════════
  // Phase 2: 王先生通过黄页发现张三
  // ═══════════════════════════════════════════════════════════

  phase('客户王先生搜索黄页，发现张三');

  const wang = await createOceanBus({ keyStore: { type: 'memory' } });
  await wang.register();
  const wangOpenid = await wang.getOpenId();

  console.log('  🧑 王先生: "想买重疾险，搜一下北京的代理人"\n');

  // 王先生搜索黄页
  try {
    const result = await wang.l1.yellowPages.discover(['重疾险', '北京'], 5);
    if (result && result.data && result.data.entries && result.data.entries.length > 0) {
      console.log('  🔍 黄页搜索结果: ' + result.data.entries.length + ' 位代理人');
      for (const entry of result.data.entries) {
        console.log('     - ' + entry.description);
        console.log('       OpenID: ' + shortId(entry.openid));
      }
      console.log('');
      console.log('  🧑 王先生: "张三，从业8年，500+家庭，看起来靠谱"\n');
    } else {
      console.log('  🔍 黄页搜索: 未找到结果（可能是 L1 服务暂未开放）\n');
      console.log('  💡 跳过黄页发现，改为直接联系（模拟已知 OpenID 场景）\n');
    }
  } catch (e) {
    console.log('  ⚠️  黄页搜索暂不可用: ' + e.message);
    console.log('  💡 跳过黄页发现，改为直接联系（模拟已知 OpenID 场景）\n');
  }

  await sleep(1000);

  // ═══════════════════════════════════════════════════════════
  // Phase 3: 王先生发起咨询
  // ═══════════════════════════════════════════════════════════

  phase('王先生发起保险咨询');

  const wangInbox = [];
  wang.startListening(m => wangInbox.push(m));

  console.log('  🧑 王先生: "先问问看"\n');

  const inquiryMsg = '你好，想了解一下重疾险。我今年32岁，有社保，已婚，有一个3岁小孩。';

  oceanbusMsg('王先生', '张三', inquiryMsg);
  await wang.send(zhangOpenid, inquiryMsg);
  await sleep(3000);

  // 张三 Agent 收到消息
  const zhangMsg1 = zhangInbox[zhangInbox.length - 1];
  if (zhangMsg1) {
    agentThink('张三', [
      '收到新客户消息: ' + zhangMsg1.content.slice(0, 50),
      '识别: 陌生OpenID，新线索',
      '评估: 🔵 热线索 — 明确提到险种、年龄、家庭结构',
      '决策: 发送自动首响（自我介绍 + 需求问卷）'
    ]);

    // 自动首响
    const autoReply = '【自动回复】您好！我是张三，平安人寿保险顾问，从业8年。\n\n' +
      '很高兴为您服务！为了给您更精准的建议，想先了解几个信息：\n' +
      '① 您主要关注哪方面的保障？（重疾、医疗、意外等）\n' +
      '② 您的预算范围大概是多少？\n' +
      '③ 之前是否有过商业保险？\n\n' +
      '期待您的回复！';

    oceanbusMsg('张三', '王先生(自动)', autoReply);
    await zhang.send(zhangMsg1.from_openid, autoReply);
  }

  await sleep(3000);

  // 王先生收到首响
  const wangMsg1 = wangInbox[wangInbox.length - 1];
  if (wangMsg1) {
    console.log('  🧑 王先生: "回复挺快，问得也挺专业的"\n');

    // 王先生回复需求
    const replyMsg = '主要关注重疾险和医疗险。预算每年8000左右。之前没有买过商业保险，只有社保。';
    oceanbusMsg('王先生', '张三', replyMsg);
    await wang.send(zhangOpenid, replyMsg);
  }

  await sleep(3000);

  // 张三 Agent 分析需求
  agentThink('张三', [
    '客户需求明确: 重疾险+医疗险，预算8000/年，无商业保险',
    '家庭情况: 32岁已婚，小孩3岁 → 建议考虑家庭保障组合',
    '更新线索阶段: 新线索 → 需求采集中',
    '生成方案建议，待代理人确认后发送'
  ]);

  // ═══════════════════════════════════════════════════════════
  // Phase 4: 张三跟进 — 发送方案
  // ═══════════════════════════════════════════════════════════

  phase('张三跟进 — 发送方案草稿，代理人确认后发送');

  console.log('  🤖 张三 Agent 生成方案草稿:\n');

  const draftMsg = '王先生您好！根据您的需求，我为您设计了一个方案：\n\n' +
    '📋 推荐方案:\n' +
    '  重疾险: 平安福2026 · 保额50万 · 保至70岁\n' +
    '  医疗险: 平安e生保 · 保额200万 · 年缴\n' +
    '  组合年保费: 约7600元（在您预算内）\n\n' +
    '💡 方案亮点:\n' +
    '  ① 重疾确诊即赔50万，覆盖治疗和收入损失\n' +
    '  ② 医疗险报销住院和特殊门诊，社保外也能报\n' +
    '  ③ 孩子3岁，建议加一份少儿重疾，年费仅600+元\n\n' +
    '方便的话，可以约个时间当面聊一下，15分钟就能把方案讲清楚。您这周什么时间方便？';

  console.log('  ┌──────────────────────────────────────────────┐');
  console.log('  │ 💬 消息草稿:                                   │');
  const draftLines = draftMsg.split('\n');
  for (const line of draftLines) {
    console.log('  │ ' + line.padEnd(46) + '│');
  }
  console.log('  └──────────────────────────────────────────────┘');
  console.log('');
  console.log('  🧑 张三: "方案不错，发吧"\n');

  oceanbusMsg('张三', '王先生(稳定OpenID)', draftMsg);
  await zhang.send(wangOpenid, draftMsg);  // 使用王先生的稳定 OpenID，而非临时 from_openid

  await sleep(3000);

  // 王先生收到方案
  console.log('  🧑 王先生: "方案挺详细的，可以考虑见面聊"\n');

  // ═══════════════════════════════════════════════════════════
  // Phase 5: 会面协商
  // ═══════════════════════════════════════════════════════════

  phase('会面协商 — 张三的 Agent 与王先生的 Agent 自动协商');

  agentThink('张三', [
    '代理人位置: 朝阳大望路',
    '代理人偏好: 周末下午，靠近地铁',
    '发起会面协商请求...'
  ]);

  const meetingReq = '【会面请求】你好！我们约个方便的地方当面聊吧。我在朝阳区大望路，最好靠近1号线地铁站。你在哪个区域？';
  oceanbusMsg('张三 Agent', '王先生 Agent', meetingReq);
  await zhang.send(wangOpenid, meetingReq);
  await sleep(3000);

  // 王先生 Agent 回复
  console.log('  🧑 王先生: "我在通州，1号线沿线都方便"\n');

  agentThink('王先生', [
    '用户位置: 通州，1号线沿线',
    '张三位置: 朝阳大望路（1号线）',
    '分析: 国贸在两者之间，1号线直达，有星巴克',
    '提出建议...'
  ]);

  const meetingSuggest = '【会面建议】地点: 国贸商城B1层星巴克 | 理由: 1号线大望路→国贸仅1站，通州过来也方便。国贸在两人之间，星巴克有座位可以坐下来慢慢聊。时间: 周六下午2点？';
  oceanbusMsg('王先生 Agent', '张三 Agent', meetingSuggest);
  await wang.send(zhangOpenid, meetingSuggest);
  await sleep(3000);

  // 张三 Agent 评估
  agentThink('张三', [
    '收到建议: 国贸星巴克，周六下午2点',
    '评估: 1号线国贸站，距大望路1站 ✅ 交通便利',
    '评估: 国贸在两人之间，位置公平 ✅',
    '评估: 星巴克有座位，适合谈话 ✅',
    '决策: 接受建议'
  ]);

  const meetingConfirm = '【会面确认】地点: 国贸商城B1层星巴克 · 时间: 周六下午2点 · 1号线国贸站C口步行5分钟';
  oceanbusMsg('张三 Agent', '王先生 Agent', meetingConfirm);
  await zhang.send(wangOpenid, meetingConfirm);
  await sleep(2000);

  // 会面协商报告
  console.log('  ╔══════════════════════════════════════════════╗');
  console.log('  ║           ✅ 会面协商完成                      ║');
  console.log('  ╚══════════════════════════════════════════════╝');
  console.log('');
  console.log('  📍 地点: 国贸商城B1层星巴克');
  console.log('  🕐 时间: 周六下午 2:00');
  console.log('  🚇 交通: 1号线国贸站C口，步行5分钟');
  console.log('  📋 协商轮次: 2轮');
  console.log('');
  console.log('  📝 面谈准备清单:');
  console.log('     · 带好王先生的方案对比表（平安福+e生保）');
  console.log('     · 准备少儿重疾附加方案（小孩3岁）');
  console.log('     · 带名片和公司宣传册');
  console.log('     · 提前15分钟到，占安静位置\n');

  // ═══════════════════════════════════════════════════════════
  // Phase 6: 成交 + 声誉累积
  // ═══════════════════════════════════════════════════════════

  phase('成交后 — 引导声誉积累');

  console.log('  [会面结束，王先生决定购买]\n');

  agentThink('张三', [
    '王先生已确认购买平安福+e生保组合',
    '建议代理人引导客户打 OceanBus 声誉标签',
    '生成引导话术...'
  ]);

  console.log('  💡 张三 Agent 提醒:');
  console.log('  ┌──────────────────────────────────────────────┐');
  console.log('  │ "感谢您的信任！如果您觉得我的服务还不错，        │');
  console.log('  │  能否在 OceanBus 上给我一个好评？              │');
  console.log('  │  这对其他客户选择我很有帮助。"                  │');
  console.log('  └──────────────────────────────────────────────┘');
  console.log('');
  console.log('  🧑 王先生: "没问题，服务很好！"\n');

  // 王先生给张三打标签
  try {
    await wang.l1.reputation.tag(zhangOpenid, '专业耐心，方案讲解清晰，值得信赖');
    console.log('  ✅ 王先生为张三打了声誉标签: "专业耐心，方案讲解清晰，值得信赖"\n');
  } catch (e) {
    console.log('  💡 声誉标签: ' + e.message + ' (声誉服务可能暂未开放，这是预期行为)\n');
  }

  // ═══════════════════════════════════════════════════════════
  // Phase 7: 每日回顾
  // ═══════════════════════════════════════════════════════════

  phase('每日回顾 — 张三的一天');

  console.log('  ╔══════════════════════════════════════════════╗');
  console.log('  ║           📊 今日回顾                         ║');
  console.log('  ╚══════════════════════════════════════════════╝');
  console.log('');
  console.log('  今日成果:');
  console.log('    ● 新线索: 1人（王先生 — 从黄页来）');
  console.log('    ● 跟进完成: 方案已发送，已确认');
  console.log('    ● 会面协商: 1场（国贸星巴克，2轮达成）');
  console.log('    ● 成交: 1单（平安福+平安e生保组合）');
  console.log('');
  console.log('  管道变化:');
  console.log('    新线索: 0 → 1 → 0（王先生已成交）');
  console.log('    需求采集中: 0 → 1 → 0');
  console.log('    方案已发: 0 → 1 → 0');
  console.log('    已成交: 0 → 1 ✅');
  console.log('');
  console.log('  声誉变化:');
  console.log('    新增好评: "专业耐心，方案讲解清晰，值得信赖"');

  // ═══════════════════════════════════════════════════════════
  // Summary
  // ═══════════════════════════════════════════════════════════

  console.log('\n╔══════════════════════════════════════════════════════════╗');
  console.log('║                  演示完成                                ║');
  console.log('╚══════════════════════════════════════════════════════════╝\n');

  console.log('  演示覆盖的 Ocean Agent 核心流程:');
  console.log('    ① 黄页档案发布        ✅ 张三以保险标签+专业描述发布');
  console.log('    ② 客户黄页发现        ' + (wangInbox.length > 0 ? '✅' : '⚠️  跳过(L1暂未开放)'));
  console.log('    ③ 新线索自动首响      ✅ 自动发送自我介绍+需求问卷');
  console.log('    ④ 线索分级            ✅ 热线索识别(明确险种/年龄/家庭)');
  console.log('    ⑤ 方案跟进            ✅ 草稿→确认→发送');
  console.log('    ⑥ 会面协商            ✅ 2轮协商达成(国贸星巴克)');
  console.log('    ⑦ 声誉积累            ✅ 成交后引导打标签');
  console.log('    ⑧ 每日回顾            ✅ 结构化当日总结');
  console.log('');
  console.log('  使用的 OceanBus SDK 能力:');
  console.log('    · 身份注册 (ob.register)');
  console.log('    · P2P 加密消息 (ob.send / ob.startListening)');
  console.log('    · 黄页服务 (ob.l1.yellowPages.registerService / discover)');
  console.log('    · 声誉服务 (ob.l1.reputation.tag)');
  console.log('    · 稳定 OpenID vs 临时 from_openid 的区别使用');
  console.log('');
  console.log('  一句话: 从黄页获客到成交，全链路在 OceanBus 上完成。');
  console.log('  零服务器。零域名。零数据库。\n');

  // Cleanup
  await zhang.destroy();
  await wang.destroy();
}

main().catch(err => {
  console.error('演示出错:', err.message);
  process.exit(1);
});
