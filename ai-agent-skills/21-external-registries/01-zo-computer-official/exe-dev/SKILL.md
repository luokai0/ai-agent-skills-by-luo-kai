---
name: exe-dev
description: Manage exe.dev VMs - create, list, delete, restart, rename, copy VMs and manage sharing/access. Use when the user wants to spin up new VMs, manage existing ones, or configure HTTP proxy sharing on exe.dev.
compatibility: Created for Zo Computer
metadata:
  author: davidj.zo.computer
  category: Community
---
# exe.dev VM Management

This skill provides a CLI for managing exe.dev VMs directly from Zo.

## Prerequisites

You must have an exe.dev account with your Zo's SSH key registered.

### Setup Steps

1. **Get Zo's public key** - Run this in Zo's terminal:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
   Copy the output.

2. **Register with exe.dev** - From your **local machine** (not Zo), run:
   ```bash
   ssh exe.dev
   ```
   Follow the prompts to create an account or sign in.

3. **Add Zo's SSH key** - Once logged into exe.dev, add Zo's public key:
   ```bash
   ssh exe.dev ssh-key add "zo-computer" "ssh-ed25519 AAAA... (paste Zo's key)"
   ```
   
   Or visit https://exe.dev and add the key in your account settings.

4. **Verify connection** - Back in Zo, test:
   ```bash
   bun Skills/exe-dev/scripts/exe.ts whoami
   ```

## Usage

Run the CLI script with `--help` to see all commands:

```bash
bun Skills/exe-dev/scripts/exe.ts --help
```

## Commands

### List VMs
```bash
bun Skills/exe-dev/scripts/exe.ts ls
bun Skills/exe-dev/scripts/exe.ts ls --detailed
```

### Create a new VM
```bash
bun Skills/exe-dev/scripts/exe.ts new
bun Skills/exe-dev/scripts/exe.ts new --name myvm
bun Skills/exe-dev/scripts/exe.ts new --name myvm --image ubuntu:22.04
bun Skills/exe-dev/scripts/exe.ts new --name myvm --prompt "Install Node.js and create a hello world app"
```

### Delete a VM
```bash
bun Skills/exe-dev/scripts/exe.ts rm <vmname>
```

### Restart a VM
```bash
bun Skills/exe-dev/scripts/exe.ts restart <vmname>
```

### Rename a VM
```bash
bun Skills/exe-dev/scripts/exe.ts rename <oldname> <newname>
```

### Copy a VM
```bash
bun Skills/exe-dev/scripts/exe.ts cp <source-vm>
bun Skills/exe-dev/scripts/exe.ts cp <source-vm> <new-name>
```

### Run command on a VM
```bash
bun Skills/exe-dev/scripts/exe.ts ssh <vmname> <command>
bun Skills/exe-dev/scripts/exe.ts ssh myvm "ls -la"
```

### Sharing & Access

Show sharing status:
```bash
bun Skills/exe-dev/scripts/exe.ts share show <vmname>
```

Set HTTP proxy port:
```bash
bun Skills/exe-dev/scripts/exe.ts share port <vmname> <port>
```

Make public/private:
```bash
bun Skills/exe-dev/scripts/exe.ts share set-public <vmname>
bun Skills/exe-dev/scripts/exe.ts share set-private <vmname>
```

Share with email:
```bash
bun Skills/exe-dev/scripts/exe.ts share add <vmname> <email>
```

Create shareable link:
```bash
bun Skills/exe-dev/scripts/exe.ts share add-link <vmname>
```

### Account Info
```bash
bun Skills/exe-dev/scripts/exe.ts whoami
```

## VM Access

Once created, VMs are accessible via:
- **SSH**: `ssh <vmname>.exe.xyz`
- **HTTP**: `https://<vmname>.exe.xyz` (if HTTP proxy is configured on port 8000)

## Notes

- All exe.dev commands support `--json` for machine-readable output
- The default image is `boldsoftware/exeuntu` which includes Shelley agent support
- VMs share CPU/RAM from your account allocation
- HTTP proxy defaults to port 8000
