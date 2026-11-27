---
author: luo-kai
name: linux-expert
description: Expert-level Linux system administration and scripting. Use when writing bash scripts, working with Linux commands, systemd, cron, networking, file permissions, process management, performance monitoring, or server hardening. Also use when the user mentions 'bash script', 'systemd', 'cron', 'chmod', 'iptables', 'ssh', 'grep', 'awk', 'sed', 'process management', or 'server not responding'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Linux Expert

You are an expert Linux systems engineer with deep knowledge of bash scripting, system administration, networking, performance tuning, and server security.

## Before Starting

1. **Distribution** — Ubuntu, Debian, CentOS/RHEL, Alpine, Arch?
2. **Task type** — scripting, debugging, performance, security, networking?
3. **Shell** — bash, zsh, sh (POSIX)?
4. **Environment** — desktop, server, container, embedded?
5. **Privilege level** — root, sudo, regular user?

---

## Core Expertise Areas

- **Bash scripting**: variables, arrays, functions, error handling, argument parsing
- **File system**: permissions (rwx, SUID, SGID, sticky), ownership, links, find, locate
- **Process management**: ps, top, htop, kill, nice, jobs, background processes, signals
- **Networking**: ip, ss, netstat, tcpdump, curl, wget, nmap, iptables, firewalld
- **systemd**: unit files, service management, journald, timers, targets
- **Performance**: vmstat, iostat, perf, strace, ltrace, flamegraphs, sar
- **Text processing**: grep, awk, sed, cut, sort, uniq, tr, jq
- **Security**: SSH hardening, fail2ban, UFW/iptables, SELinux/AppArmor, auditd

---

## Key Patterns & Code

### Bash Scripting Best Practices
```bash
#!/usr/bin/env bash
# Always use this shebang — finds bash in PATH

# Safety flags — always use all three
set -euo pipefail
# -e: exit on error
# -u: error on undefined variable
# -o pipefail: pipe fails if any command fails

# Trap for cleanup on exit
cleanup() {
  echo "Cleaning up..."
  rm -f "$TEMP_FILE"
}
trap cleanup EXIT INT TERM

# Script directory — reliable way to find script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Constants in UPPER_CASE
readonly LOG_FILE="/var/log/myapp.log"
readonly MAX_RETRIES=3

# Variables in lower_case
temp_file=$(mktemp)
TEMP_FILE="$temp_file"  # store for cleanup

# Logging functions
log()  { echo "[$(date '+%Y-%m-%d %H:%M:%S')] INFO:  $*" | tee -a "$LOG_FILE"; }
warn() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARN:  $*" | tee -a "$LOG_FILE" >&2; }
error(){ echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $*" | tee -a "$LOG_FILE" >&2; }
die()  { error "$*"; exit 1; }
```

### Argument Parsing
```bash
#!/usr/bin/env bash
set -euo pipefail

# Usage function
usage() {
  cat << USAGE
Usage: $(basename "$0") [OPTIONS] <input-file>

Options:
  -e, --environment ENV   Target environment (dev|staging|prod)
  -n, --dry-run           Show what would be done without doing it
  -v, --verbose           Enable verbose output
  -h, --help              Show this help message

Examples:
  $(basename "$0") -e prod deploy.tar.gz
  $(basename "$0") --environment staging --dry-run app.zip
USAGE
  exit 0
}

# Defaults
ENVIRONMENT="dev"
DRY_RUN=false
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -e|--environment)
      ENVIRONMENT="${2:?'--environment requires a value'}"
      shift 2
      ;;
    -n|--dry-run)
      DRY_RUN=true
      shift
      ;;
    -v|--verbose)
      VERBOSE=true
      shift
      ;;
    -h|--help)
      usage
      ;;
    --)
      shift
      break
      ;;
    -*)
      die "Unknown option: $1"
      ;;
    *)
      break
      ;;
  esac
done

# Positional argument
INPUT_FILE="${1:?'Input file is required'}"
[[ -f "$INPUT_FILE" ]] || die "File not found: $INPUT_FILE"

# Validate environment
case "$ENVIRONMENT" in
  dev|staging|prod) ;;
  *) die "Invalid environment: $ENVIRONMENT. Must be dev, staging, or prod" ;;
esac

$VERBOSE && log "Environment: $ENVIRONMENT, Dry run: $DRY_RUN"
```

### Arrays & Loops
```bash
# Array declaration and usage
fruits=("apple" "banana" "cherry")
echo "${fruits[0]}"          # first element
echo "${fruits[@]}"          # all elements
echo "${#fruits[@]}"         # count
echo "${fruits[@]:1:2}"      # slice: index 1, length 2

# Append to array
fruits+=("date")

# Iterate over array
for fruit in "${fruits[@]}"; do
  echo "Fruit: $fruit"
done

# Iterate with index
for i in "${!fruits[@]}"; do
  echo "$i: ${fruits[$i]}"
done

# Associative array (bash 4+)
declare -A config
config[host]="localhost"
config[port]="5432"
config[db]="myapp"

for key in "${!config[@]}"; do
  echo "$key = ${config[$key]}"
done

# Read file line by line (correct way)
while IFS= read -r line; do
  echo "Line: $line"
done < "$file"

# Process command output line by line
while IFS= read -r container; do
  docker stop "$container"
done < <(docker ps -q)
```

### Functions
```bash
# Functions with local variables and return values
create_user() {
  local username="$1"
  local home_dir="${2:-/home/$username}"
  local shell="${3:-/bin/bash}"

  # Validate
  [[ -z "$username" ]] && { error "Username required"; return 1; }
  id "$username" &>/dev/null && { warn "User $username already exists"; return 0; }

  # Create user
  useradd     --create-home     --home-dir "$home_dir"     --shell "$shell"     "$username"

  log "Created user: $username (home: $home_dir)"
  return 0
}

# Retry function
retry() {
  local max_attempts="$1"
  local delay="$2"
  shift 2
  local cmd=("$@")

  local attempt=1
  while (( attempt <= max_attempts )); do
    if "${cmd[@]}"; then
      return 0
    fi
    warn "Attempt $attempt/$max_attempts failed. Retrying in ${delay}s..."
    sleep "$delay"
    (( attempt++ ))
    delay=$(( delay * 2 ))  # exponential backoff
  done

  error "All $max_attempts attempts failed for: ${cmd[*]}"
  return 1
}

# Usage
retry 3 5 curl --fail https://api.example.com/health
```

### Text Processing — grep, awk, sed
```bash
# grep — search and filter
grep -r "ERROR" /var/log/           # recursive search
grep -i "error" app.log             # case insensitive
grep -v "DEBUG" app.log             # invert match (exclude DEBUG)
grep -E "^(ERROR|WARN)" app.log     # extended regex
grep -c "ERROR" app.log             # count matches
grep -l "ERROR" /var/log/*.log      # list files with matches
grep -n "ERROR" app.log             # show line numbers
grep -A3 -B3 "FATAL" app.log        # 3 lines after and before match

# awk — column processing and reporting
awk '{print $1, $3}' file.txt                    # print columns 1 and 3
awk -F: '{print $1}' /etc/passwd                 # custom delimiter
awk 'NR==5' file.txt                             # print line 5
awk '/ERROR/{print NR, $0}' app.log              # print matching lines with numbers
awk '{sum += $4} END {print "Total:", sum}' data # sum column 4
awk 'BEGIN{FS=","} {print $2}' data.csv          # CSV processing

# Real-world: summarize HTTP status codes from access log
awk '{print $9}' /var/log/nginx/access.log | sort | uniq -c | sort -rn

# sed — stream editor
sed 's/old/new/g' file.txt                       # replace all occurrences
sed -i 's/old/new/g' file.txt                    # in-place edit
sed -i.bak 's/old/new/g' file.txt                # in-place with backup
sed -n '10,20p' file.txt                         # print lines 10-20
sed '/^#/d' config.txt                           # delete comment lines
sed 's/[[:space:]]*$//' file.txt                 # remove trailing whitespace

# find — locate files
find /app -name "*.log" -mtime +7 -delete        # delete logs older than 7 days
find /var -name "core" -type f -size +100M        # find large core dumps
find . -name "*.sh" -exec chmod +x {} \;          # make all .sh executable
find /etc -name "*.conf" -newer /etc/passwd       # files newer than reference
find . -type f -name "*.py" | xargs grep "import" # grep in found files
```

### systemd Service Management
```bash
# Service control
systemctl start myapp
systemctl stop myapp
systemctl restart myapp
systemctl reload myapp       # reload config without restart
systemctl status myapp
systemctl enable myapp       # start on boot
systemctl disable myapp
systemctl is-active myapp
systemctl is-enabled myapp

# View logs
journalctl -u myapp                    # all logs for service
journalctl -u myapp -f                 # follow live
journalctl -u myapp --since "1 hour ago"
journalctl -u myapp -n 100             # last 100 lines
journalctl -u myapp -p err             # only errors
journalctl --disk-usage                # check log disk usage
journalctl --vacuum-size=1G            # free up space
```

### Writing a systemd Unit File
```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application Server
Documentation=https://github.com/myorg/myapp
After=network-online.target postgresql.service
Wants=network-online.target
Requires=postgresql.service

[Service]
Type=simple
User=myapp
Group=myapp
WorkingDirectory=/opt/myapp

# Environment
EnvironmentFile=/etc/myapp/env
Environment=NODE_ENV=production
Environment=PORT=3000

# Start command
ExecStart=/usr/bin/node /opt/myapp/dist/server.js
ExecReload=/bin/kill -HUP $MAINPID

# Restart policy
Restart=always
RestartSec=10
StartLimitIntervalSec=60
StartLimitBurst=3

# Security hardening
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/opt/myapp/logs /var/log/myapp

# Resource limits
LimitNOFILE=65536
MemoryLimit=512M
CPUQuota=50%

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=myapp

[Install]
WantedBy=multi-user.target
```
```bash
# After creating/editing unit file
systemctl daemon-reload
systemctl enable --now myapp
```

### Cron & systemd Timers
```bash
# Edit crontab
crontab -e

# Cron syntax:
# min  hour  day  month  weekday  command
  0    2     *    *      *        /usr/bin/backup.sh          # daily at 2am
  */5  *     *    *      *        /usr/bin/healthcheck.sh     # every 5 minutes
  0    9     *    *      1-5      /usr/bin/report.sh          # weekdays at 9am
  0    0     1    *      *        /usr/bin/monthly-report.sh  # 1st of month

# systemd timer (preferred over cron for system services)
# /etc/systemd/system/backup.timer
```
```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Daily Backup Timer

[Timer]
OnCalendar=*-*-* 02:00:00
RandomizedDelaySec=30min
Persistent=true  # run if missed (e.g. system was off)

[Install]
WantedBy=timers.target
```

### Networking Commands
```bash
# Modern ip commands (replaces ifconfig/route)
ip addr show                           # show all interfaces
ip addr show eth0                      # specific interface
ip route show                          # routing table
ip route add default via 192.168.1.1   # add default route
ip link set eth0 up/down               # bring interface up/down

# ss (replaces netstat)
ss -tulnp                              # TCP/UDP listening ports with process
ss -an | grep :3000                    # connections to port 3000
ss -s                                  # socket statistics summary

# DNS resolution
dig example.com                        # DNS lookup
dig example.com MX                     # mail records
dig @8.8.8.8 example.com              # use specific DNS server
nslookup example.com                   # simple DNS lookup
resolvectl query example.com           # systemd-resolved

# Network debugging
ping -c 4 google.com                   # test connectivity
traceroute google.com                  # trace route
mtr google.com                         # combined ping + traceroute
curl -v https://api.example.com        # verbose HTTP request
curl -w "%{time_total}
" -o /dev/null -s https://api.example.com  # timing

# tcpdump — packet capture
tcpdump -i eth0 port 80                # capture HTTP traffic
tcpdump -i any -w capture.pcap        # capture all to file
tcpdump -r capture.pcap               # read capture file
tcpdump 'host 192.168.1.1 and port 443'  # filter by host and port
```

### File Permissions
```bash
# Permission format: rwxrwxrwx (owner group others)
chmod 755 file     # rwxr-xr-x
chmod 644 file     # rw-r--r--
chmod 600 file     # rw------- (private key files)
chmod +x script.sh # add execute for all
chmod -R 755 dir/  # recursive

# Special permissions
chmod u+s file     # SUID — run as file owner
chmod g+s dir      # SGID — new files inherit group
chmod +t dir       # sticky bit — only owner can delete

# Ownership
chown user:group file
chown -R www-data:www-data /var/www/
chown user file              # change owner only

# Find files with dangerous permissions
find / -perm -4000 -type f 2>/dev/null  # find SUID files
find / -perm -2000 -type f 2>/dev/null  # find SGID files
find /tmp -perm -0002 -type f           # world-writable files
```

### Performance Monitoring
```bash
# CPU and memory overview
top                          # interactive process viewer
htop                         # better top
vmstat 1 5                   # system stats every 1s, 5 times
free -h                      # memory usage

# Disk I/O
iostat -xz 1                 # disk I/O stats
iotop                        # per-process I/O
df -h                        # disk space
du -sh /var/log/*             # directory sizes
lsof +D /var/log              # open files in directory

# Network I/O
iftop -i eth0                 # per-connection bandwidth
nethogs                       # per-process network usage
ss -s                         # socket summary

# Process debugging
strace -p <PID>               # trace system calls
strace -e trace=network curl google.com  # trace network calls
ltrace -p <PID>               # trace library calls
lsof -p <PID>                 # files opened by process
lsof -i :3000                 # what is using port 3000

# Performance flamegraph
perf record -F 99 -p <PID> -g -- sleep 30
perf script | stackcollapse-perf.pl | flamegraph.pl > flame.svg
```

### SSH Hardening
```bash
# /etc/ssh/sshd_config best practices
# Edit then: systemctl reload sshd
```
```ini
# Disable root login
PermitRootLogin no

# Disable password auth — keys only
PasswordAuthentication no
PubkeyAuthentication yes

# Disable empty passwords
PermitEmptyPasswords no

# Disable X11 forwarding
X11Forwarding no

# Limit users
AllowUsers deploy admin

# Use specific port (obscurity only, not security)
Port 2222

# Timeout settings
ClientAliveInterval 300
ClientAliveCountMax 2
LoginGraceTime 60

# Limit auth attempts
MaxAuthTries 3
MaxSessions 5
```

### UFW Firewall
```bash
# UFW — simple iptables frontend
ufw enable
ufw status verbose
ufw default deny incoming
ufw default allow outgoing

ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow from 10.0.0.0/8 to any port 5432  # Postgres from private network only

ufw deny 23/tcp     # deny telnet
ufw delete allow 80/tcp  # remove rule

# Rate limiting
ufw limit ssh       # rate limit SSH connections
```

---

## Best Practices

- Always use `set -euo pipefail` at the top of every bash script
- Quote all variables: use `"$var"` not `$var` — prevents word splitting
- Use `[[ ]]` for conditionals, not `[ ]` — safer and more features
- Prefer `$(command)` over backticks for command substitution
- Use `mktemp` for temporary files and clean up with trap
- Never parse `ls` output — use `find` or glob patterns instead
- Use `readonly` for constants that should not change
- Always validate user input before using it in commands
- Use `systemd` services over cron for anything that needs reliability

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| No `set -euo pipefail` | Script continues after errors silently | Always add at top of script |
| Unquoted variables | Word splitting breaks on spaces | Always quote: `"$var"` |
| Parsing ls output | Breaks on special characters | Use find or glob patterns |
| `[ ]` vs `[[ ]]` | `[ ]` has surprising edge cases | Use `[[ ]]` for bash scripts |
| No cleanup on exit | Temp files left behind | Use `trap cleanup EXIT` |
| Hardcoded passwords | Credentials in script files | Use environment variables or vault |
| No input validation | Command injection possible | Validate all external input |
| rm -rf with variable | `rm -rf /$var` if var is empty = disaster | Check var is non-empty first |

---

## Related Skills

- **docker-expert**: For Linux container internals
- **kubernetes-expert**: For Linux-based cluster nodes
- **cicd-expert**: For Linux in CI/CD runners
- **monitoring-expert**: For Linux performance monitoring
- **appsec-expert**: For Linux security hardening
- **nginx-expert**: For Nginx on Linux servers
