#!/usr/bin/env bun
/**
 * exe.dev CLI - Manage exe.dev VMs from Zo
 * 
 * Usage: bun exe.ts <command> [options]
 * 
 * Supports multiple accounts via --account flag
 */

import { parseArgs } from "util";
import { $ } from "bun";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import { homedir } from "os";
import { join } from "path";

const CONFIG_DIR = join(homedir(), ".config", "exe-dev");
const ACCOUNTS_FILE = join(CONFIG_DIR, "accounts.json");

interface Account {
  name: string;
  keyPath: string;
}

interface AccountsConfig {
  default?: string;
  accounts: Account[];
}

function loadAccounts(): AccountsConfig {
  if (!existsSync(ACCOUNTS_FILE)) {
    return { accounts: [] };
  }
  try {
    return JSON.parse(readFileSync(ACCOUNTS_FILE, "utf-8"));
  } catch {
    return { accounts: [] };
  }
}

function saveAccounts(config: AccountsConfig) {
  if (!existsSync(CONFIG_DIR)) {
    mkdirSync(CONFIG_DIR, { recursive: true });
  }
  writeFileSync(ACCOUNTS_FILE, JSON.stringify(config, null, 2));
}

function getKeyPath(accountName?: string): string | undefined {
  if (!accountName) {
    const config = loadAccounts();
    if (config.default) {
      const account = config.accounts.find(a => a.name === config.default);
      if (account) return account.keyPath;
    }
    return undefined; // Use default SSH key
  }
  
  const config = loadAccounts();
  const account = config.accounts.find(a => a.name === accountName);
  if (!account) {
    console.error(`Account '${accountName}' not found. Run 'exe.ts accounts list' to see available accounts.`);
    process.exit(1);
  }
  return account.keyPath;
}

const HELP = `
exe.dev CLI - Manage exe.dev VMs

Usage: bun exe.ts <command> [args] [options]

Commands:
  ls                          List all VMs
  new                         Create a new VM
  rm <vmname>                 Delete a VM
  restart <vmname>            Restart a VM
  rename <old> <new>          Rename a VM
  cp <source> [newname]       Copy a VM
  ssh <vmname> [command]      Run command on VM (or get SSH info)
  whoami                      Show account info
  share <subcommand> <vm>     Manage sharing (see below)
  accounts <subcommand>       Manage multiple exe.dev accounts (see below)

Share subcommands:
  share show <vm>             Show sharing status
  share port <vm> <port>      Set HTTP proxy port
  share set-public <vm>       Make HTTP proxy public
  share set-private <vm>      Make HTTP proxy private (auth required)
  share add <vm> <email>      Share with user via email
  share remove <vm> <email>   Revoke user's access
  share add-link <vm>         Create shareable link
  share remove-link <vm> <token>  Revoke shareable link

Accounts subcommands:
  accounts list               List configured accounts
  accounts add <name> <keypath>  Add an account (keypath is SSH private key)
  accounts remove <name>      Remove an account
  accounts default [name]     Show or set the default account

Options:
  --help, -h        Show this help
  --json            Output in JSON format
  --detailed, -l    Show detailed info (for ls)
  --account <name>  Use a specific account (by name)
  --name <name>     VM name (for new)
  --image <image>   Container image (for new)
  --prompt <text>   Initial Shelley prompt (for new)
  --env <K=V>       Environment variable (for new, can repeat)
  --no-email        Don't send email notification (for new)

Examples:
  bun exe.ts ls
  bun exe.ts ls --account work
  bun exe.ts new --name myvm
  bun exe.ts new --name myvm --image ubuntu:22.04 --account personal
  bun exe.ts accounts add work ~/.ssh/id_ed25519_work
  bun exe.ts accounts add personal ~/.ssh/id_ed25519_personal
  bun exe.ts accounts default work
`;

async function runSSH(args: string[], json = false, keyPath?: string): Promise<{ stdout: string; stderr: string; exitCode: number }> {
  const sshArgs = json ? [...args, "--json"] : args;
  const sshOpts = keyPath ? ["-i", keyPath] : [];
  const cmd = ["ssh", ...sshOpts, "exe.dev", ...sshArgs];
  
  try {
    const result = await $`${cmd}`.quiet();
    return {
      stdout: result.stdout.toString(),
      stderr: result.stderr.toString(),
      exitCode: result.exitCode,
    };
  } catch (err: any) {
    return {
      stdout: err.stdout?.toString() || "",
      stderr: err.stderr?.toString() || err.message,
      exitCode: err.exitCode || 1,
    };
  }
}

function parseJSON(stdout: string): any {
  try {
    return JSON.parse(stdout);
  } catch {
    return null;
  }
}

async function listVMs(detailed: boolean, json: boolean, keyPath?: string) {
  const args = detailed ? ["ls", "-l"] : ["ls"];
  const result = await runSSH(args, json, keyPath);
  
  if (result.exitCode !== 0) {
    console.error("Error listing VMs:", result.stderr);
    process.exit(1);
  }
  
  if (json) {
    const data = parseJSON(result.stdout);
    console.log(JSON.stringify(data, null, 2));
  } else {
    console.log(result.stdout);
  }
}

async function newVM(options: {
  name?: string;
  image?: string;
  prompt?: string;
  env?: string[];
  noEmail?: boolean;
  json?: boolean;
}, keyPath?: string) {
  const args = ["new"];
  
  if (options.name) args.push(`--name=${options.name}`);
  if (options.image) args.push(`--image=${options.image}`);
  if (options.prompt) args.push(`--prompt=${options.prompt}`);
  if (options.noEmail) args.push("--no-email");
  if (options.env) {
    for (const e of options.env) {
      args.push("--env", e);
    }
  }
  
  const result = await runSSH(args, options.json, keyPath);
  
  if (result.exitCode !== 0) {
    console.error("Error creating VM:", result.stderr);
    process.exit(1);
  }
  
  if (options.json) {
    const data = parseJSON(result.stdout);
    console.log(JSON.stringify(data, null, 2));
  } else {
    console.log(result.stdout);
  }
}

async function removeVM(vmname: string, json: boolean, keyPath?: string) {
  const result = await runSSH(["rm", vmname], json, keyPath);
  
  if (result.exitCode !== 0) {
    console.error("Error removing VM:", result.stderr);
    process.exit(1);
  }
  
  if (json) {
    const data = parseJSON(result.stdout);
    console.log(JSON.stringify(data, null, 2));
  } else {
    console.log(result.stdout || `VM '${vmname}' deleted.`);
  }
}

async function restartVM(vmname: string, json: boolean, keyPath?: string) {
  const result = await runSSH(["restart", vmname], json, keyPath);
  
  if (result.exitCode !== 0) {
    console.error("Error restarting VM:", result.stderr);
    process.exit(1);
  }
  
  if (json) {
    const data = parseJSON(result.stdout);
    console.log(JSON.stringify(data, null, 2));
  } else {
    console.log(result.stdout || `VM '${vmname}' restarted.`);
  }
}

async function renameVM(oldname: string, newname: string, json: boolean, keyPath?: string) {
  const result = await runSSH(["rename", oldname, newname], json, keyPath);
  
  if (result.exitCode !== 0) {
    console.error("Error renaming VM:", result.stderr);
    process.exit(1);
  }
  
  if (json) {
    const data = parseJSON(result.stdout);
    console.log(JSON.stringify(data, null, 2));
  } else {
    console.log(result.stdout || `VM renamed from '${oldname}' to '${newname}'.`);
  }
}

async function copyVM(source: string, newname: string | undefined, json: boolean, keyPath?: string) {
  const args = newname ? ["cp", source, newname] : ["cp", source];
  const result = await runSSH(args, json, keyPath);
  
  if (result.exitCode !== 0) {
    console.error("Error copying VM:", result.stderr);
    process.exit(1);
  }
  
  if (json) {
    const data = parseJSON(result.stdout);
    console.log(JSON.stringify(data, null, 2));
  } else {
    console.log(result.stdout);
  }
}

async function sshVM(vmname: string, command: string[], json: boolean, keyPath?: string) {
  if (command.length === 0) {
    // Just show SSH info
    console.log(`SSH destination: ${vmname}.exe.xyz`);
    console.log(`To connect: ssh ${vmname}.exe.xyz`);
    return;
  }
  
  // Run command via exe.dev ssh
  const args = ["ssh", vmname, ...command];
  const result = await runSSH(args, false, keyPath); // ssh command doesn't support --json
  
  if (result.exitCode !== 0) {
    console.error(result.stderr);
    process.exit(result.exitCode);
  }
  
  console.log(result.stdout);
}

async function whoami(json: boolean, keyPath?: string) {
  const result = await runSSH(["whoami"], json, keyPath);
  
  if (result.exitCode !== 0) {
    console.error("Error:", result.stderr);
    process.exit(1);
  }
  
  if (json) {
    const data = parseJSON(result.stdout);
    console.log(JSON.stringify(data, null, 2));
  } else {
    console.log(result.stdout);
  }
}

async function shareCommand(subcommand: string, args: string[], json: boolean, keyPath?: string) {
  const shareArgs = ["share", subcommand, ...args];
  const result = await runSSH(shareArgs, json, keyPath);
  
  if (result.exitCode !== 0) {
    console.error("Error:", result.stderr);
    process.exit(1);
  }
  
  if (json) {
    const data = parseJSON(result.stdout);
    console.log(JSON.stringify(data, null, 2));
  } else {
    console.log(result.stdout);
  }
}

function accountsCommand(subcommand: string, args: string[]) {
  const config = loadAccounts();
  
  switch (subcommand) {
    case "list": {
      if (config.accounts.length === 0) {
        console.log("No accounts configured.");
        console.log("\nUsing default SSH key (~/.ssh/id_ed25519)");
        console.log("\nTo add an account:");
        console.log("  bun exe.ts accounts add <name> <path-to-ssh-key>");
        return;
      }
      console.log("Configured accounts:\n");
      for (const account of config.accounts) {
        const isDefault = config.default === account.name ? " (default)" : "";
        console.log(`  ${account.name}${isDefault}`);
        console.log(`    Key: ${account.keyPath}`);
      }
      if (!config.default) {
        console.log("\nNo default set - using system default SSH key");
      }
      break;
    }
    
    case "add": {
      if (args.length < 2) {
        console.error("Usage: accounts add <name> <keypath>");
        console.error("Example: accounts add work ~/.ssh/id_ed25519_work");
        process.exit(1);
      }
      const [name, keyPath] = args;
      const expandedPath = keyPath.replace(/^~/, homedir());
      
      if (!existsSync(expandedPath)) {
        console.error(`SSH key not found: ${expandedPath}`);
        process.exit(1);
      }
      
      const existing = config.accounts.findIndex(a => a.name === name);
      if (existing >= 0) {
        config.accounts[existing].keyPath = expandedPath;
        console.log(`Updated account '${name}'`);
      } else {
        config.accounts.push({ name, keyPath: expandedPath });
        console.log(`Added account '${name}'`);
      }
      
      // Set as default if it's the first account
      if (config.accounts.length === 1) {
        config.default = name;
        console.log(`Set '${name}' as default account`);
      }
      
      saveAccounts(config);
      break;
    }
    
    case "remove": {
      if (args.length < 1) {
        console.error("Usage: accounts remove <name>");
        process.exit(1);
      }
      const [name] = args;
      const idx = config.accounts.findIndex(a => a.name === name);
      if (idx < 0) {
        console.error(`Account '${name}' not found`);
        process.exit(1);
      }
      config.accounts.splice(idx, 1);
      if (config.default === name) {
        config.default = config.accounts[0]?.name;
      }
      saveAccounts(config);
      console.log(`Removed account '${name}'`);
      break;
    }
    
    case "default": {
      if (args.length === 0) {
        if (config.default) {
          console.log(`Default account: ${config.default}`);
        } else {
          console.log("No default account set - using system default SSH key");
        }
        return;
      }
      const [name] = args;
      if (name === "none" || name === "clear") {
        config.default = undefined;
        saveAccounts(config);
        console.log("Cleared default account - will use system default SSH key");
        return;
      }
      const account = config.accounts.find(a => a.name === name);
      if (!account) {
        console.error(`Account '${name}' not found`);
        process.exit(1);
      }
      config.default = name;
      saveAccounts(config);
      console.log(`Default account set to '${name}'`);
      break;
    }
    
    default: {
      console.error(`Unknown accounts subcommand: ${subcommand}`);
      console.log("Subcommands: list, add, remove, default");
      process.exit(1);
    }
  }
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
    console.log(HELP);
    process.exit(0);
  }
  
  const command = args[0];
  const restArgs = args.slice(1);
  
  // Parse common flags
  const hasJson = restArgs.includes("--json");
  const hasDetailed = restArgs.includes("--detailed") || restArgs.includes("-l");
  
  // Parse --account flag
  const accountIdx = restArgs.indexOf("--account");
  let accountName: string | undefined;
  if (accountIdx >= 0 && restArgs[accountIdx + 1]) {
    accountName = restArgs[accountIdx + 1];
  }
  
  // Get the key path for the account
  const keyPath = getKeyPath(accountName);
  
  // Filter out flags for positional args
  const positional = restArgs.filter((a, i) => {
    if (a.startsWith("--") || a.startsWith("-")) return false;
    // Also filter out the value after --account
    if (i > 0 && restArgs[i - 1] === "--account") return false;
    return true;
  });
  
  switch (command) {
    case "ls": {
      await listVMs(hasDetailed, hasJson, keyPath);
      break;
    }
    
    case "new": {
      // Parse new-specific options
      const { values } = parseArgs({
        args: restArgs,
        options: {
          name: { type: "string" },
          image: { type: "string" },
          prompt: { type: "string" },
          env: { type: "string", multiple: true },
          "no-email": { type: "boolean" },
          json: { type: "boolean" },
          account: { type: "string" },
        },
        allowPositionals: true,
      });
      
      await newVM({
        name: values.name,
        image: values.image,
        prompt: values.prompt,
        env: values.env,
        noEmail: values["no-email"],
        json: values.json,
      }, keyPath);
      break;
    }
    
    case "rm": {
      if (positional.length === 0) {
        console.error("Error: VM name required. Usage: exe.ts rm <vmname>");
        process.exit(1);
      }
      await removeVM(positional[0], hasJson, keyPath);
      break;
    }
    
    case "restart": {
      if (positional.length === 0) {
        console.error("Error: VM name required. Usage: exe.ts restart <vmname>");
        process.exit(1);
      }
      await restartVM(positional[0], hasJson, keyPath);
      break;
    }
    
    case "rename": {
      if (positional.length < 2) {
        console.error("Error: Old and new names required. Usage: exe.ts rename <old> <new>");
        process.exit(1);
      }
      await renameVM(positional[0], positional[1], hasJson, keyPath);
      break;
    }
    
    case "cp": {
      if (positional.length === 0) {
        console.error("Error: Source VM required. Usage: exe.ts cp <source> [newname]");
        process.exit(1);
      }
      await copyVM(positional[0], positional[1], hasJson, keyPath);
      break;
    }
    
    case "ssh": {
      if (positional.length === 0) {
        console.error("Error: VM name required. Usage: exe.ts ssh <vmname> [command]");
        process.exit(1);
      }
      const vmname = positional[0];
      const cmdArgs = positional.slice(1);
      await sshVM(vmname, cmdArgs, hasJson, keyPath);
      break;
    }
    
    case "whoami": {
      await whoami(hasJson, keyPath);
      break;
    }
    
    case "share": {
      if (positional.length === 0) {
        console.error("Error: Share subcommand required.");
        console.error("Subcommands: show, port, set-public, set-private, add, remove, add-link, remove-link");
        process.exit(1);
      }
      const subcommand = positional[0];
      const shareArgs = positional.slice(1);
      await shareCommand(subcommand, shareArgs, hasJson, keyPath);
      break;
    }
    
    case "accounts": {
      if (positional.length === 0) {
        accountsCommand("list", []);
      } else {
        const subcommand = positional[0];
        const accountArgs = positional.slice(1);
        accountsCommand(subcommand, accountArgs);
      }
      break;
    }
    
    default: {
      console.error(`Unknown command: ${command}`);
      console.log("Run 'bun exe.ts --help' for usage.");
      process.exit(1);
    }
  }
}

main().catch(err => {
  console.error("Error:", err.message);
  process.exit(1);
});
