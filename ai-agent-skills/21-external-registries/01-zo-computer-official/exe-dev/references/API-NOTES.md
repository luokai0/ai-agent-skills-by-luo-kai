# exe.dev API Reference

The exe.dev API is SSH-based. All commands are run via `ssh exe.dev <command>`.

## CLI Commands

### ls - List VMs
```
ssh exe.dev ls [--json] [-l] [name|pattern]
```
- `--json`: Output in JSON format
- `-l`: Show detailed information

JSON output structure:
```json
{
  "vms": [
    {
      "image": "boldsoftware/exeuntu",
      "ssh_dest": "myvm.exe.xyz",
      "status": "running",
      "vm_name": "myvm"
    }
  ]
}
```

### new - Create VM
```
ssh exe.dev new [options]
```
Options:
- `--name=<name>`: VM name (auto-generated if not specified)
- `--image=<image>`: Container image (default: boldsoftware/exeuntu)
- `--command=<cmd>`: Container command (auto, none, or custom)
- `--env KEY=VALUE`: Environment variable (can repeat)
- `--prompt=<text>`: Initial Shelley prompt (requires exeuntu image)
- `--no-email`: Don't send email notification
- `--json`: JSON output

### rm - Delete VM
```
ssh exe.dev rm <vmname>... [--json]
```

### restart - Restart VM
```
ssh exe.dev restart <vmname> [--json]
```

### rename - Rename VM
```
ssh exe.dev rename <oldname> <newname> [--json]
```

### cp - Copy VM
```
ssh exe.dev cp <source-vm> [new-name] [--json]
```

### ssh - Run command on VM
```
ssh exe.dev ssh <vmname> [command...]
```

### whoami - Account info
```
ssh exe.dev whoami [--json]
```

## Share Commands

### share show - Show sharing status
```
ssh exe.dev share show <vm> [--json] [--qr]
```

### share port - Set HTTP proxy port
```
ssh exe.dev share port <vm> [port] [--json]
```
Default port is 8000.

### share set-public - Make public
```
ssh exe.dev share set-public <vm> [--json]
```

### share set-private - Require auth
```
ssh exe.dev share set-private <vm> [--json]
```

### share add - Share with email
```
ssh exe.dev share add <vm> <email|team> [--message='...'] [--json] [--qr]
```

### share remove - Revoke access
```
ssh exe.dev share remove <vm> <email|team> [--json]
```

### share add-link - Create shareable link
```
ssh exe.dev share add-link <vm> [--json] [--qr]
```

### share remove-link - Revoke link
```
ssh exe.dev share remove-link <vm> <token> [--json]
```

### share receive-email - Email forwarding
```
ssh exe.dev share receive-email <vm> [on|off] [--json]
```

## VM Access

- **SSH**: `ssh <vmname>.exe.xyz`
- **HTTP proxy**: `https://<vmname>.exe.xyz` (requires service on port 8000 by default)
- **Internal SSH** (from exe.dev jumphost): `ssh exe.dev ssh <vmname>`

## Pricing (as of 2025)

| Plan | Price | VMs | CPU | RAM | Disk |
|------|-------|-----|-----|-----|------|
| Individual | $20/mo | 25 | 2 | 8GB | 25GB |
| Team | $25/mo/user | 25 | 2 | 8GB | 25GB |
| Enterprise | $30/mo/user | 30 | 2 | 16GB | 25GB |

Additional: Disk $0.08/GB/mo, Bandwidth $0.07/GB/mo

## Resources

- Docs: https://exe.dev/docs
- API docs: https://exe.dev/docs/api
- CLI reference: https://exe.dev/docs/list (section 8)
