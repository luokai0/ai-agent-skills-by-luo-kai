#!/usr/bin/env bun
import { Database } from "bun:sqlite";
import { resolve, basename } from "path";
import { existsSync } from "fs";

const DB_PATH = resolve(import.meta.dir, "../assets/file-share.db");
const WORKSPACE = "/home/workspace";

// Initialize database (same schema as server)
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

function generateToken(): string {
  return crypto.randomUUID();
}

const commands: Record<string, { desc: string; usage: string; fn: (args: string[]) => void }> = {
  "list-files": {
    desc: "List all registered files",
    usage: "list-files",
    fn: () => {
      const files = db.query(`
        SELECT f.id, f.name, f.path, f.created_at,
               COUNT(uf.user_id) as user_count
        FROM files f
        LEFT JOIN user_files uf ON f.id = uf.file_id
        GROUP BY f.id
      `).all() as any[];
      
      if (files.length === 0) {
        console.log("No files registered. Use 'add-file <path>' to add one.");
        return;
      }
      
      console.log("\n📁 Registered Files:\n");
      console.log("ID  | Name                           | Users | Path");
      console.log("----|--------------------------------|-------|-----------------------------");
      for (const f of files) {
        const name = f.name.substring(0, 30).padEnd(30);
        const users = String(f.user_count).padStart(5);
        console.log(`${String(f.id).padStart(3)} | ${name} | ${users} | ${f.path}`);
      }
      console.log();
    }
  },
  
  "list-users": {
    desc: "List all users and their access",
    usage: "list-users",
    fn: () => {
      const users = db.query(`
        SELECT u.id, u.email, u.confirmed, u.created_at,
               GROUP_CONCAT(f.name, ', ') as files
        FROM users u
        LEFT JOIN user_files uf ON u.id = uf.user_id
        LEFT JOIN files f ON uf.file_id = f.id
        GROUP BY u.id
      `).all() as any[];
      
      if (users.length === 0) {
        console.log("No users registered.");
        return;
      }
      
      console.log("\n👤 Users:\n");
      console.log("ID  | Email                          | Confirmed | Files");
      console.log("----|--------------------------------|-----------|-----------------------------");
      for (const u of users) {
        const email = u.email.substring(0, 30).padEnd(30);
        const confirmed = u.confirmed ? "    ✅    " : "    ❌    ";
        const files = (u.files || "none").substring(0, 30);
        console.log(`${String(u.id).padStart(3)} | ${email} | ${confirmed} | ${files}`);
      }
      console.log();
    }
  },
  
  "add-file": {
    desc: "Register a file for sharing",
    usage: "add-file <path> [name]",
    fn: (args) => {
      if (args.length < 1) {
        console.error("Usage: add-file <path> [name]");
        process.exit(1);
      }
      
      let filePath = args[0];
      // Resolve relative paths against workspace
      if (!filePath.startsWith("/")) {
        filePath = resolve(WORKSPACE, filePath);
      }
      
      if (!existsSync(filePath)) {
        console.error(`File not found: ${filePath}`);
        process.exit(1);
      }
      
      const name = args[1] || basename(filePath);
      
      try {
        db.run("INSERT INTO files (name, path) VALUES (?, ?)", [name, filePath]);
        const file = db.query("SELECT * FROM files WHERE path = ?").get(filePath) as any;
        console.log(`✅ File registered with ID ${file.id}: ${name}`);
        console.log(`   Path: ${filePath}`);
      } catch (e: any) {
        if (e.message.includes("UNIQUE")) {
          console.error("File already registered.");
        } else {
          console.error("Error:", e.message);
        }
        process.exit(1);
      }
    }
  },
  
  "remove-file": {
    desc: "Remove a file from sharing",
    usage: "remove-file <file_id>",
    fn: (args) => {
      if (args.length < 1) {
        console.error("Usage: remove-file <file_id>");
        process.exit(1);
      }
      
      const fileId = parseInt(args[0]);
      const file = db.query("SELECT * FROM files WHERE id = ?").get(fileId) as any;
      
      if (!file) {
        console.error("File not found.");
        process.exit(1);
      }
      
      db.run("DELETE FROM user_files WHERE file_id = ?", [fileId]);
      db.run("DELETE FROM files WHERE id = ?", [fileId]);
      console.log(`✅ Removed file: ${file.name}`);
    }
  },
  
  "add-user": {
    desc: "Add a user with access to a file",
    usage: "add-user <email> <file_id>",
    fn: (args) => {
      if (args.length < 2) {
        console.error("Usage: add-user <email> <file_id>");
        process.exit(1);
      }
      
      const email = args[0];
      const fileId = parseInt(args[1]);
      
      const file = db.query("SELECT * FROM files WHERE id = ?").get(fileId) as any;
      if (!file) {
        console.error("File not found.");
        process.exit(1);
      }
      
      let user = db.query("SELECT * FROM users WHERE email = ?").get(email) as any;
      
      if (!user) {
        const token = generateToken();
        db.run("INSERT INTO users (email, confirmation_token) VALUES (?, ?)", [email, token]);
        user = db.query("SELECT * FROM users WHERE email = ?").get(email) as any;
        console.log(`✅ Created user: ${email} (unconfirmed)`);
      }
      
      const existing = db.query(
        "SELECT * FROM user_files WHERE user_id = ? AND file_id = ?"
      ).get(user.id, fileId);
      
      if (existing) {
        console.log(`User already has access to ${file.name}`);
        return;
      }
      
      const accessToken = generateToken();
      db.run(
        "INSERT INTO user_files (user_id, file_id, access_token) VALUES (?, ?, ?)",
        [user.id, fileId, accessToken]
      );
      console.log(`✅ Granted ${email} access to: ${file.name}`);
      console.log(`   User confirmed: ${user.confirmed ? 'Yes' : 'No'}`);
      if (!user.confirmed) {
        console.log(`   User needs to confirm email via the web UI or /request-access endpoint`);
      }
    }
  },
  
  "remove-user": {
    desc: "Remove a user completely",
    usage: "remove-user <user_id>",
    fn: (args) => {
      if (args.length < 1) {
        console.error("Usage: remove-user <user_id>");
        process.exit(1);
      }
      
      const userId = parseInt(args[0]);
      const user = db.query("SELECT * FROM users WHERE id = ?").get(userId) as any;
      
      if (!user) {
        console.error("User not found.");
        process.exit(1);
      }
      
      db.run("DELETE FROM user_files WHERE user_id = ?", [userId]);
      db.run("DELETE FROM users WHERE id = ?", [userId]);
      console.log(`✅ Removed user: ${user.email}`);
    }
  },
  
  "revoke-access": {
    desc: "Revoke a user's access to a file",
    usage: "revoke-access <user_id> <file_id>",
    fn: (args) => {
      if (args.length < 2) {
        console.error("Usage: revoke-access <user_id> <file_id>");
        process.exit(1);
      }
      
      const userId = parseInt(args[0]);
      const fileId = parseInt(args[1]);
      
      db.run("DELETE FROM user_files WHERE user_id = ? AND file_id = ?", [userId, fileId]);
      console.log(`✅ Access revoked`);
    }
  },
  
  "confirm-user": {
    desc: "Manually confirm a user's email",
    usage: "confirm-user <user_id>",
    fn: (args) => {
      if (args.length < 1) {
        console.error("Usage: confirm-user <user_id>");
        process.exit(1);
      }
      
      const userId = parseInt(args[0]);
      db.run("UPDATE users SET confirmed = 1 WHERE id = ?", [userId]);
      console.log(`✅ User confirmed`);
    }
  },
  
  "file-users": {
    desc: "List users with access to a specific file",
    usage: "file-users <file_id>",
    fn: (args) => {
      if (args.length < 1) {
        console.error("Usage: file-users <file_id>");
        process.exit(1);
      }
      
      const fileId = parseInt(args[0]);
      const file = db.query("SELECT * FROM files WHERE id = ?").get(fileId) as any;
      
      if (!file) {
        console.error("File not found.");
        process.exit(1);
      }
      
      const users = db.query(`
        SELECT u.id, u.email, u.confirmed
        FROM users u
        JOIN user_files uf ON u.id = uf.user_id
        WHERE uf.file_id = ?
      `).all(fileId) as any[];
      
      console.log(`\n📁 ${file.name}\n`);
      if (users.length === 0) {
        console.log("No users have access to this file.");
        return;
      }
      
      console.log("ID  | Email                          | Confirmed");
      console.log("----|--------------------------------|----------");
      for (const u of users) {
        const email = u.email.substring(0, 30).padEnd(30);
        const confirmed = u.confirmed ? "   ✅" : "   ❌";
        console.log(`${String(u.id).padStart(3)} | ${email} | ${confirmed}`);
      }
      console.log();
    }
  }
};

function printHelp() {
  console.log("\n📁 File Share CLI\n");
  console.log("Usage: bun cli.ts <command> [args]\n");
  console.log("Commands:");
  for (const [name, cmd] of Object.entries(commands)) {
    console.log(`  ${cmd.usage.padEnd(35)} ${cmd.desc}`);
  }
  console.log("\nExamples:");
  console.log("  bun cli.ts add-file Documents/report.pdf");
  console.log("  bun cli.ts add-user alice@example.com 1");
  console.log("  bun cli.ts list-files");
  console.log("  bun cli.ts list-users");
  console.log();
}

const [command, ...args] = process.argv.slice(2);

if (!command || command === "help" || command === "--help" || command === "-h") {
  printHelp();
  process.exit(0);
}

if (commands[command]) {
  commands[command].fn(args);
} else {
  console.error(`Unknown command: ${command}`);
  printHelp();
  process.exit(1);
}
