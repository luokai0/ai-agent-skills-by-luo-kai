import { Database } from "bun:sqlite";
import { readFileSync, existsSync } from "fs";
import { basename, resolve } from "path";

const PORT = parseInt(process.env.PORT || "8765");
const DB_PATH = resolve(import.meta.dir, "../assets/file-share.db");
const WORKSPACE = "/home/workspace";
const ZO_TOKEN = process.env.ZO_CLIENT_IDENTITY_TOKEN;
const BASE_URL = process.env.FILE_SHARE_BASE_URL || `http://localhost:${PORT}`;

// Initialize database
const db = new Database(DB_PATH, { create: true });
db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    confirmed INTEGER DEFAULT 0,
    confirmation_token TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);
db.run(`
  CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT UNIQUE NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);
db.run(`
  CREATE TABLE IF NOT EXISTS user_files (
    user_id INTEGER NOT NULL,
    file_id INTEGER NOT NULL,
    access_token TEXT,
    PRIMARY KEY (user_id, file_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (file_id) REFERENCES files(id)
  )
`);

const BRAILLE_FOOTER = "⢕⣿⣏⣿⢳⡕⣆⢺⣋⢟";

const PAGE_STYLE = `
  * { box-sizing: border-box; }
  body { 
    font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', monospace;
    max-width: 480px; 
    margin: 80px auto; 
    padding: 24px;
    background: #0a0a0a;
    color: #e0e0e0;
    line-height: 1.6;
  }
  h1 { 
    font-size: 1.25rem; 
    font-weight: 500;
    margin-bottom: 24px;
    letter-spacing: -0.02em;
  }
  p { 
    font-size: 0.875rem; 
    color: #888;
    margin: 12px 0;
  }
  form { margin: 24px 0; }
  label { 
    display: block; 
    font-size: 0.75rem; 
    color: #666;
    margin: 16px 0 6px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  input, select { 
    width: 100%;
    padding: 12px;
    background: #141414;
    border: 1px solid #2a2a2a;
    color: #e0e0e0;
    font-family: inherit;
    font-size: 0.875rem;
    border-radius: 4px;
  }
  input:focus, select:focus {
    outline: none;
    border-color: #444;
  }
  select option { background: #141414; }
  button { 
    width: 100%;
    padding: 12px 24px;
    margin-top: 20px;
    background: #fff;
    color: #000;
    border: none;
    font-family: inherit;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    border-radius: 4px;
    transition: opacity 0.15s;
  }
  button:hover { opacity: 0.85; }
  button:disabled { opacity: 0.5; cursor: not-allowed; }
  .message { 
    padding: 12px;
    margin: 16px 0;
    font-size: 0.875rem;
    border-radius: 4px;
  }
  .success { background: #0d2818; color: #4ade80; border: 1px solid #166534; }
  .error { background: #2d1215; color: #f87171; border: 1px solid #991b1b; }
  .footer {
    margin-top: 48px;
    padding-top: 24px;
    border-top: 1px solid #1a1a1a;
    text-align: center;
    font-size: 1rem;
    color: #333;
    letter-spacing: 0.1em;
  }
`;

function htmlPage(title: string, content: string): string {
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${title}</title>
  <style>${PAGE_STYLE}</style>
</head>
<body>
  ${content}
  <div class="footer">${BRAILLE_FOOTER}</div>
</body>
</html>`;
}

function generateToken(): string {
  return crypto.randomUUID();
}

async function sendEmail(to: string, subject: string, body: string) {
  if (!ZO_TOKEN) {
    console.error("ZO_CLIENT_IDENTITY_TOKEN not set, cannot send email");
    return false;
  }
  
  const response = await fetch("https://api.zo.computer/zo/ask", {
    method: "POST",
    headers: {
      "authorization": ZO_TOKEN,
      "content-type": "application/json"
    },
    body: JSON.stringify({
      input: `Use the Gmail integration to send an email. First call list_app_tools("gmail") to get the tool name, then use use_app_gmail to send an email to "${to}" with subject "${subject}" and the following markdown body:

${body}

Send the email and confirm it was sent. Do not ask for confirmation, just send it.`
    })
  });
  
  const result = await response.json();
  console.log(`Email send result for ${to}:`, result.output?.substring(0, 200));
  return response.ok;
}

// Update sendConfirmationEmail to include braille footer
async function sendConfirmationEmail(to: string, token: string, fileName: string) {
  const confirmUrl = `${BASE_URL}/confirm/${token}`;
  const body = `You requested access to "${fileName}".

Click below to confirm your email:
${confirmUrl}

—
${BRAILLE_FOOTER}`;
  
  return sendEmail(to, `Confirm your email to access "${fileName}"`, body);
}

// Update sendAccessEmail to include braille footer
async function sendAccessEmail(to: string, fileId: number, accessToken: string, fileName: string) {
  const downloadUrl = `${BASE_URL}/file/${fileId}/${accessToken}`;
  const body = `Your access to "${fileName}" is ready.

Download:
${downloadUrl}

—
${BRAILLE_FOOTER}`;

  return sendEmail(to, `Access granted: ${fileName}`, body);
}

const server = Bun.serve({
  port: PORT,
  idleTimeout: 120,
  async fetch(req) {
    const url = new URL(req.url);
    const path = url.pathname;

    // CORS headers
    const headers = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (req.method === "OPTIONS") {
      return new Response(null, { headers });
    }

    // Health check
    if (path === "/health") {
      return new Response(JSON.stringify({ status: "ok" }), {
        headers: { ...headers, "Content-Type": "application/json" }
      });
    }

    // List available files (public endpoint)
    if (path === "/files" && req.method === "GET") {
      const files = db.query("SELECT id, name FROM files").all();
      return new Response(JSON.stringify(files), {
        headers: { ...headers, "Content-Type": "application/json" }
      });
    }

    // Request access to a file
    if (path === "/request-access" && req.method === "POST") {
      try {
        const { email, file_id } = await req.json();
        
        if (!email || !file_id) {
          return new Response(JSON.stringify({ error: "email and file_id required" }), {
            status: 400,
            headers: { ...headers, "Content-Type": "application/json" }
          });
        }

        const file = db.query("SELECT * FROM files WHERE id = ?").get(file_id) as any;
        if (!file) {
          return new Response(JSON.stringify({ error: "file not found" }), {
            status: 404,
            headers: { ...headers, "Content-Type": "application/json" }
          });
        }

        // Check if user exists
        let user = db.query("SELECT * FROM users WHERE email = ?").get(email) as any;
        const confirmationToken = generateToken();
        
        if (!user) {
          db.run(
            "INSERT INTO users (email, confirmation_token) VALUES (?, ?)",
            [email, confirmationToken]
          );
          user = db.query("SELECT * FROM users WHERE email = ?").get(email) as any;
        } else if (!user.confirmed) {
          // Update confirmation token
          db.run("UPDATE users SET confirmation_token = ? WHERE id = ?", [confirmationToken, user.id]);
        }

        // Check if access already exists
        const existingAccess = db.query(
          "SELECT * FROM user_files WHERE user_id = ? AND file_id = ?"
        ).get(user.id, file_id);

        if (!existingAccess) {
          const accessToken = generateToken();
          db.run(
            "INSERT INTO user_files (user_id, file_id, access_token) VALUES (?, ?, ?)",
            [user.id, file_id, accessToken]
          );
        }

        if (user.confirmed) {
          // Already confirmed, send access email directly (fire and forget)
          const uf = db.query(
            "SELECT access_token FROM user_files WHERE user_id = ? AND file_id = ?"
          ).get(user.id, file_id) as any;
          sendAccessEmail(email, file_id, uf.access_token, file.name);
          return new Response(JSON.stringify({ 
            message: "Access email sent",
            already_confirmed: true 
          }), {
            headers: { ...headers, "Content-Type": "application/json" }
          });
        } else {
          // Send confirmation email (fire and forget)
          sendConfirmationEmail(email, confirmationToken, file.name);
          return new Response(JSON.stringify({ 
            message: "Confirmation email sent",
            already_confirmed: false
          }), {
            headers: { ...headers, "Content-Type": "application/json" }
          });
        }
      } catch (e: any) {
        return new Response(JSON.stringify({ error: e.message }), {
          status: 500,
          headers: { ...headers, "Content-Type": "application/json" }
        });
      }
    }

    // Confirm email
    if (path.startsWith("/confirm/") && req.method === "GET") {
      const token = path.split("/confirm/")[1];
      
      const user = db.query(
        "SELECT * FROM users WHERE confirmation_token = ?"
      ).get(token) as any;

      if (!user) {
        return new Response(htmlPage("Invalid Link", `
          <h1>Invalid Link</h1>
          <p>This confirmation link is invalid or has expired.</p>
        `), {
          status: 404,
          headers: { ...headers, "Content-Type": "text/html; charset=utf-8" }
        });
      }

      // Confirm the user
      db.run("UPDATE users SET confirmed = 1 WHERE id = ?", [user.id]);

      // Get all files this user has access to and send access emails in background
      const userFiles = db.query(`
        SELECT f.id, f.name, uf.access_token 
        FROM user_files uf 
        JOIN files f ON uf.file_id = f.id 
        WHERE uf.user_id = ?
      `).all(user.id) as any[];

      // Fire and forget - send emails in background
      for (const uf of userFiles) {
        sendAccessEmail(user.email, uf.id, uf.access_token, uf.name);
      }
      
      return new Response(htmlPage("Email Confirmed", `
        <h1>Email Confirmed</h1>
        <p>Your email has been confirmed.</p>
        <p>Download links are being sent to your inbox.</p>
      `), {
        headers: { ...headers, "Content-Type": "text/html; charset=utf-8" }
      });
    }

    // Serve file
    if (path.startsWith("/file/") && req.method === "GET") {
      const parts = path.split("/file/")[1].split("/");
      const fileId = parseInt(parts[0]);
      const accessToken = parts[1];

      if (!fileId || !accessToken) {
        return new Response("Invalid request", { status: 400, headers });
      }

      // Verify access
      const access = db.query(`
        SELECT u.*, uf.access_token, f.path, f.name
        FROM user_files uf
        JOIN users u ON uf.user_id = u.id
        JOIN files f ON uf.file_id = f.id
        WHERE uf.file_id = ? AND uf.access_token = ?
      `).get(fileId, accessToken) as any;

      if (!access) {
        return new Response("Access denied or invalid token", { status: 403, headers });
      }

      if (!access.confirmed) {
        return new Response("Please confirm your email first", { status: 403, headers });
      }

      const filePath = access.path.startsWith("/") ? access.path : resolve(WORKSPACE, access.path);
      
      if (!existsSync(filePath)) {
        return new Response("File not found on server", { status: 404, headers });
      }

      const fileContent = readFileSync(filePath);
      const fileName = basename(filePath);
      
      return new Response(fileContent, {
        headers: {
          ...headers,
          "Content-Type": "application/octet-stream",
          "Content-Disposition": `attachment; filename="${fileName}"`
        }
      });
    }

    // Update the main form page
    if (path === "/" && req.method === "GET") {
      const files = db.query("SELECT id, name FROM files").all() as any[];
      const fileOptions = files.map(f => `<option value="${f.id}">${f.name}</option>`).join("");
      
      return new Response(htmlPage("File Share", `
        <h1>File Share</h1>
        <p>Request access to files by entering your email.</p>
        
        <form id="accessForm">
          <label>File</label>
          <select name="file_id" required>
            <option value="">Select a file</option>
            ${fileOptions}
          </select>
          
          <label>Email</label>
          <input type="email" name="email" placeholder="you@example.com" required />
          
          <button type="submit">Request Access</button>
        </form>
        
        <div id="message"></div>
        
        <script>
          document.getElementById('accessForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = e.target;
            const btn = form.querySelector('button');
            const msgDiv = document.getElementById('message');
            const data = {
              email: form.email.value,
              file_id: parseInt(form.file_id.value)
            };
            
            btn.disabled = true;
            btn.textContent = 'Sending...';
            msgDiv.className = 'message';
            msgDiv.textContent = '';
            
            try {
              const res = await fetch('/request-access', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
              });
              const result = await res.json();
              if (res.ok) {
                msgDiv.className = 'message success';
                msgDiv.textContent = result.already_confirmed 
                  ? 'Access email sent. Check your inbox.'
                  : 'Confirmation email sent. Check your inbox.';
                form.reset();
              } else {
                msgDiv.className = 'message error';
                msgDiv.textContent = result.error || 'Request failed';
              }
            } catch (err) {
              msgDiv.className = 'message error';
              msgDiv.textContent = 'Error: ' + err.message;
            } finally {
              btn.disabled = false;
              btn.textContent = 'Request Access';
            }
          });
        </script>
      `), {
        headers: { ...headers, "Content-Type": "text/html; charset=utf-8" }
      });
    }

    return new Response("Not found", { status: 404, headers });
  }
});

console.log(`File share server running on port ${PORT}`);
console.log(`Database: ${DB_PATH}`);
console.log(`Base URL: ${BASE_URL}`);
