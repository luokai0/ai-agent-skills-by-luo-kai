import { defineChannelPluginEntry } from "openclaw/plugin-sdk/core";
import { DEFAULT_ACCOUNT_ID } from "openclaw/plugin-sdk/account-id";
import WS from "ws";

// ─── Runtime state ─────────────────────────────────────────────
let _pluginApi = null;
let _runtime = null;

function setPluginApi(api) { _pluginApi = api; }
function getPluginApi() {
  if (!_pluginApi) throw new Error("botland plugin API is not initialized");
  return _pluginApi;
}
function setPluginRuntime(runtime) { _runtime = runtime; }
function getRuntime() {
  if (!_runtime) throw new Error("botland plugin runtime is not initialized");
  return _runtime;
}

// ─── Constants ─────────────────────────────────────────────────
const CHANNEL_ID = "botland";
const DEFAULT_API_URL = "https://api.botland.im";
const DEFAULT_WS_URL = "wss://api.botland.im/ws";
const DEFAULT_RECONNECT_MS = 5000;
const DEFAULT_PING_INTERVAL_MS = 20000;
const DEFAULT_TIMEOUT_MS = 120000;

// ─── Auth ──────────────────────────────────────────────────────
let cachedToken = null;
let cachedCitizenId = null;

async function login(apiUrl, handle, password, log) {
  log?.info?.(`[${CHANNEL_ID}] logging in as ${handle}...`);
  const res = await fetch(`${apiUrl}/api/v1/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ handle, password }),
  });
  const data = await res.json();
  if (data.access_token) {
    cachedToken = data.access_token;
    cachedCitizenId = data.citizen_id;
    log?.info?.(`[${CHANNEL_ID}] logged in as ${handle} (${data.citizen_id})`);
    return true;
  }
  log?.error?.(`[${CHANNEL_ID}] login failed: ${JSON.stringify(data)}`);
  return false;
}

// ─── Agent reply dispatch ──────────────────────────────────────
function extractReplyText(payload) {
  const visited = new Set();
  const fragments = [];
  const visit = (value) => {
    const direct = typeof value === "string" ? value.trim() : "";
    if (direct) { fragments.push(direct); return; }
    if (!value || typeof value !== "object") return;
    if (visited.has(value)) return;
    visited.add(value);
    if (Array.isArray(value)) { for (const item of value) visit(item); return; }
    if (value.type === "text" && typeof value.text === "string") { visit(value.text); return; }
    for (const key of ["text", "body", "content", "message", "markdown", "channelData"]) {
      if (key in value) visit(value[key]);
    }
  };
  visit(payload);
  return fragments.filter((f, i) => fragments.indexOf(f) === i).join("\n\n").trim();
}

async function runAgentReply(params) {
  const { account, cfg, from, text, senderName, requestId } = params;
  const runtime = getRuntime();
  const logger = getPluginApi().logger;

  const route = runtime.channel.routing.resolveAgentRoute({
    cfg,
    channel: CHANNEL_ID,
    accountId: account.accountId,
    peer: { kind: "direct", id: from },
  });

  const sessionKey = route.sessionKey || `${CHANNEL_ID}:direct:${from}`;
  const replyParts = [];

  const ctxPayload = runtime.channel.reply.finalizeInboundContext({
    Body: text,
    BodyForAgent: text,
    RawBody: text,
    CommandBody: text,
    From: from,
    To: account.botName,
    SessionKey: sessionKey,
    AccountId: route.accountId,
    ChatType: "direct",
    ConversationLabel: senderName || from,
    SenderName: senderName || from,
    SenderId: from,
    CommandAuthorized: true,
    Provider: CHANNEL_ID,
    Surface: CHANNEL_ID,
    OriginatingChannel: CHANNEL_ID,
    OriginatingTo: from,
  });

  const storePath = runtime.channel.session.resolveStorePath(cfg.session?.store, {
    agentId: route.agentId,
  });

  await runtime.channel.session.recordInboundSession({
    storePath,
    sessionKey: ctxPayload.SessionKey ?? sessionKey,
    ctx: ctxPayload,
    onRecordError: (err) => {
      logger.warn(`[${CHANNEL_ID}] failed to record inbound session: ${err instanceof Error ? err.message : String(err)}`);
    },
  });

  logger.info(`[${CHANNEL_ID}] dispatching reply from=${from} sessionKey=${sessionKey} routeAgent=${route.agentId}`);

  const abortController = new AbortController();
  const timeoutHandle = setTimeout(() => {
    abortController.abort(new Error(`Timed out after ${account.timeoutMs}ms`));
  }, account.timeoutMs);

  try {
    await runtime.channel.reply.dispatchReplyWithBufferedBlockDispatcher({
      ctx: ctxPayload,
      cfg,
      dispatcherOptions: {
        deliver: async (outbound, info) => {
          const chunk = extractReplyText(outbound);
          if (chunk) {
            replyParts.push(chunk);
            logger.info(`[${CHANNEL_ID}] deliver kind=${info?.kind ?? "unknown"} chunkLen=${chunk.length}`);
          }
        },
        onError: (error, info) => {
          logger.error(`[${CHANNEL_ID}] dispatcher error kind=${info.kind} message=${error instanceof Error ? error.message : String(error)}`);
        },
      },
      replyOptions: {
        abortSignal: abortController.signal,
        disableBlockStreaming: true,
        timeoutOverrideSeconds: Math.max(1, Math.ceil(account.timeoutMs / 1000)),
        onModelSelected: (ctx) => {
          logger.info(`[${CHANNEL_ID}] model selected provider=${ctx.provider} model=${ctx.model}`);
        },
      },
    });
  } catch (err) {
    logger.error(`[${CHANNEL_ID}] dispatch error: ${err instanceof Error ? err.message : String(err)}`);
  } finally {
    clearTimeout(timeoutHandle);
  }

  return replyParts.join("\n\n").trim();
}

// ─── WebSocket connection ──────────────────────────────────────
async function connectBotland(params) {
  const { account, cfg, log, abortSignal, setStatus } = params;
  const reconnectMs = account.reconnectMs;
  const pingIntervalMs = account.pingIntervalMs;
  let retryCount = 0;
  const MAX_RETRIES = 20;

  // Login first
  const loggedIn = await login(account.apiUrl, account.handle, account.password, log);
  if (!loggedIn) {
    log?.error?.(`[${CHANNEL_ID}] cannot start: login failed`);
    setStatus({ running: false, lastError: "login failed" });
    return;
  }

  while (!abortSignal.aborted) {
    const wsUrl = `${account.wsUrl}?token=${cachedToken}`;
    log?.info?.(`[${CHANNEL_ID}] connecting WebSocket (attempt ${retryCount + 1})...`);

    const shouldRetry = await new Promise((resolve) => {
      let resolved = false;
      let pingTimer = null;
      const ws = new WS(wsUrl);

      const safeResolve = (val) => { if (!resolved) { resolved = true; resolve(val); } };
      const cleanup = () => { if (pingTimer) { clearInterval(pingTimer); pingTimer = null; } };

      const onAbort = () => { cleanup(); try { ws.close(1000, "abort"); } catch {} safeResolve(false); };
      abortSignal.addEventListener("abort", onAbort, { once: true });

      ws.addEventListener("open", () => {
        log?.info?.(`[${CHANNEL_ID}] WebSocket connected`);
        retryCount = 0;
        setStatus({ running: true, lastStartAt: Date.now(), lastError: null });

        // Send presence
        ws.send(JSON.stringify({ type: "presence.update", payload: { state: "online" } }));

        // Ping keepalive
        pingTimer = setInterval(() => {
          if (ws.readyState === WS.OPEN) {
            try { ws.send(JSON.stringify({ type: "ping" })); } catch {}
          }
        }, pingIntervalMs);
      });

      ws.addEventListener("message", (event) => {
        void (async () => {
          try {
            const raw = typeof event.data === "string" ? event.data : Buffer.from(event.data).toString("utf8");
            const msg = JSON.parse(raw);

            // Only handle incoming messages
            if (msg.type !== "message.received" || !msg.from) return;

            const text = msg.payload?.text ?? "";
            if (!text.trim()) return;

            const senderId = msg.from;
            const senderName = msg.sender_name || msg.from;
            const requestId = msg.id || `botland_${Date.now()}`;

            log?.info?.(`[${CHANNEL_ID}] message from=${senderId}: ${text.substring(0, 50)}...`);

            // Run agent reply
            const reply = await runAgentReply({
              account, cfg, from: senderId, text, senderName, requestId,
            });

            if (reply && ws.readyState === WS.OPEN) {
              ws.send(JSON.stringify({
                type: "message.send",
                id: `reply_${Date.now()}`,
                to: senderId,
                payload: { content_type: "text", text: reply },
              }));
              log?.info?.(`[${CHANNEL_ID}] replied to ${senderId}: ${reply.substring(0, 50)}...`);
            }
          } catch (err) {
            log?.error?.(`[${CHANNEL_ID}] message handler error: ${err instanceof Error ? err.message : String(err)}`);
          }
        })();
      });

      ws.addEventListener("error", (err) => {
        log?.error?.(`[${CHANNEL_ID}] WebSocket error`);
      });

      ws.addEventListener("close", (event) => {
        abortSignal.removeEventListener("abort", onAbort);
        cleanup();
        log?.warn?.(`[${CHANNEL_ID}] WebSocket closed code=${event.code} reason=${event.reason || ""}`);
        setStatus({ running: false, lastStopAt: Date.now() });

        // If auth error, try re-login
        if (event.code === 4001 || event.code === 4003) {
          log?.info?.(`[${CHANNEL_ID}] auth error, will re-login on reconnect`);
          cachedToken = null;
        }
        safeResolve(true); // should retry
      });

      // Connection timeout
      setTimeout(() => {
        if (ws.readyState === WS.CONNECTING) {
          log?.warn?.(`[${CHANNEL_ID}] connection timeout (10s)`);
          cleanup();
          try { ws.close(4001, "connection timeout"); } catch {} safeResolve(true);
        }
      }, 10000);
    });

    if (!shouldRetry || abortSignal.aborted) break;

    retryCount++;
    if (retryCount >= MAX_RETRIES) {
      log?.error?.(`[${CHANNEL_ID}] max reconnection attempts (${MAX_RETRIES}) reached`);
      setStatus({ running: false, lastError: `max retries (${MAX_RETRIES}) reached` });
      break;
    }

    // Re-login if token expired
    if (!cachedToken) {
      const ok = await login(account.apiUrl, account.handle, account.password, log);
      if (!ok) {
        log?.error?.(`[${CHANNEL_ID}] re-login failed, will retry in ${reconnectMs}ms`);
      }
    }

    log?.info?.(`[${CHANNEL_ID}] reconnecting in ${reconnectMs}ms (${retryCount}/${MAX_RETRIES})...`);
    await new Promise((r) => setTimeout(r, reconnectMs));
  }
}

// ─── Channel config ────────────────────────────────────────────
function resolveAccount(cfg) {
  const c = cfg.channels?.botland ?? {};
  return {
    accountId: DEFAULT_ACCOUNT_ID,
    enabled: c.enabled !== false,
    configured: Boolean(c.handle && c.password),
    apiUrl: String(c.apiUrl ?? DEFAULT_API_URL).replace(/\/$/, ""),
    wsUrl: String(c.wsUrl ?? DEFAULT_WS_URL).replace(/\/$/, ""),
    handle: String(c.handle ?? ""),
    password: String(c.password ?? ""),
    botName: String(c.botName ?? "BotLand Agent"),
    timeoutMs: Math.min(Math.max(c.timeoutMs ?? DEFAULT_TIMEOUT_MS, 1000), 300000),
    reconnectMs: Math.min(Math.max(c.reconnectMs ?? DEFAULT_RECONNECT_MS, 1000), 60000),
    pingIntervalMs: Math.min(Math.max(c.pingIntervalMs ?? DEFAULT_PING_INTERVAL_MS, 5000), 60000),
  };
}

// ─── Plugin definition ─────────────────────────────────────────
const botlandPlugin = {
  id: CHANNEL_ID,
  meta: {
    id: CHANNEL_ID,
    label: "BotLand",
    selectionLabel: "BotLand (AI Social Network)",
    detailLabel: "BotLand - Where AI agents and humans coexist",
    docsPath: "/channels/botland",
    docsLabel: "BotLand",
    blurb: "Connect to BotLand, the social network where AI agents are first-class citizens.",
    order: 201,
  },
  capabilities: {
    chatTypes: ["direct"],
    media: false,
    threads: false,
    reactions: false,
    nativeCommands: false,
    blockStreaming: false,
  },
  reload: { configPrefixes: [`channels.${CHANNEL_ID}`] },
  configSchema: {
    schema: {
      type: "object",
      additionalProperties: true,
      properties: {
        enabled: { type: "boolean" },
        apiUrl: { type: "string" },
        wsUrl: { type: "string" },
        handle: { type: "string" },
        password: { type: "string" },
        botName: { type: "string" },
        timeoutMs: { type: "integer", minimum: 1000, maximum: 300000 },
        reconnectMs: { type: "integer", minimum: 1000, maximum: 60000 },
        pingIntervalMs: { type: "integer", minimum: 5000, maximum: 60000 },
      },
    },
  },
  config: {
    listAccountIds: () => [DEFAULT_ACCOUNT_ID],
    resolveAccount: (cfg) => resolveAccount(cfg),
    defaultAccountId: () => DEFAULT_ACCOUNT_ID,
    isEnabled: (account) => account.enabled,
    isConfigured: (account) => account.configured,
    describeAccount: (account) => ({
      accountId: account.accountId,
      enabled: account.enabled,
      configured: account.configured,
      apiUrl: account.apiUrl,
      handle: account.handle || "[未配置]",
      botName: account.botName,
      timeoutMs: account.timeoutMs,
    }),
  },
  security: {
    resolveDmPolicy: () => ({
      policy: "open",
      allowFrom: [],
      policyPath: `channels.${CHANNEL_ID}.handle`,
      allowFromPath: `channels.${CHANNEL_ID}.handle`,
      approveHint: "BotLand 账号登录授权",
      normalizeEntry: (raw) => raw.trim(),
    }),
  },
  directory: {
    self: async () => cachedCitizenId ? { id: cachedCitizenId, name: cachedToken ? "online" : "offline" } : null,
    listPeers: async () => [],
    listGroups: async () => [],
  },
  status: {
    defaultRuntime: {
      accountId: DEFAULT_ACCOUNT_ID,
      running: false,
      lastStartAt: null,
      lastStopAt: null,
      lastError: null,
    },
    buildAccountSnapshot: ({ account, runtime }) => ({
      accountId: account.accountId,
      enabled: account.enabled,
      configured: account.configured,
      handle: account.handle || "[missing]",
      apiUrl: account.apiUrl,
      running: runtime?.running ?? false,
      lastStartAt: runtime?.lastStartAt ?? null,
      lastStopAt: runtime?.lastStopAt ?? null,
      lastError: runtime?.lastError ?? null,
    }),
  },
  gateway: {
    startAccount: async (ctx) => {
      const log = ctx.log;
      const account = resolveAccount(ctx.cfg);
      if (!account.enabled) {
        log?.info?.(`[${CHANNEL_ID}] channel disabled, skipping`);
        return;
      }
      if (!account.configured) {
        log?.warn?.(`[${CHANNEL_ID}] handle/password not configured, skipping`);
        return;
      }
      await connectBotland({
        account,
        cfg: ctx.cfg,
        log,
        abortSignal: ctx.abortSignal,
        setStatus: (patch) => ctx.setStatus({ accountId: ctx.accountId, ...patch }),
      });
    },
  },
  messaging: {
    normalizeTarget: (target) => target.trim() || undefined,
    targetResolver: {
      looksLikeId: (value) => Boolean(value.trim()),
      hint: "<citizen_id>",
    },
  },
};

// ─── Entry point ───────────────────────────────────────────────
const plugin = defineChannelPluginEntry({
  id: botlandPlugin.id,
  name: "BotLand",
  description: "Connect to BotLand social network",
  plugin: botlandPlugin,
  setRuntime(runtime) { setPluginRuntime(runtime); },
  registerFull(api) { setPluginApi(api); },
});

export default plugin;
