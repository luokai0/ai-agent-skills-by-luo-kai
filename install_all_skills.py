#!/usr/bin/env python3
"""
Master AI Agent Skills Installer — by Luo Kai (Lous Creations)
v2.0 — Fixed categorization + more repos + cleanup pass
Usage: python3 install_all_skills.py
"""

import os, re, shutil, subprocess, sys

# ============================================================
# CONFIG
# ============================================================
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_USER  = "luokai0"
REPO_NAME    = "ai-agent-skills-by-luo-kai"
REPO_DIR     = os.path.expanduser("~/skills-repo")
WORK_DIR     = os.path.expanduser("~/skill-sources")
AUTHOR       = "luo-kai"

# ============================================================
# SOURCE REPOS
# ============================================================
SOURCE_REPOS = [
    ("https://github.com/anthropics/skills.git",                        "anthropic-official"),
    ("https://github.com/VoltAgent/skills.git",                         "voltagent-skills"),
    ("https://github.com/VoltAgent/awesome-agent-skills.git",           "volt-awesome"),
    ("https://github.com/VoltAgent/awesome-claude-code-subagents.git",  "volt-subagents"),
    ("https://github.com/callstackincubator/agent-skills.git",          "callstack-skills"),
    ("https://github.com/better-auth/skills.git",                       "betterauth-skills"),
    ("https://github.com/fal-ai-community/skills.git",                  "fal-skills"),
    ("https://github.com/obra/superpowers.git",                         "obra-superpowers"),
    ("https://github.com/getsentry/skills.git",                         "sentry-skills"),
    ("https://github.com/google-labs-code/stitch-skills.git",           "stitch-skills"),
    ("https://github.com/ComposioHQ/skills.git",                        "composio-skills"),
    ("https://github.com/WordPress/agent-skills.git",                   "wordpress-skills"),
    ("https://github.com/ClickHouse/agent-skills.git",                  "clickhouse-skills"),
    ("https://github.com/NeoLabHQ/context-engineering-kit.git",         "neolab-cek"),
    ("https://github.com/NoizAI/skills.git",                            "noizai-skills"),
    ("https://github.com/BrianRWagner/ai-marketing-skills.git",         "marketing-skills"),
    ("https://github.com/heilcheng/awesome-agent-skills.git",           "heilcheng-skills"),
    ("https://github.com/supabase/agent-skills.git",                    "supabase-skills"),
    ("https://github.com/vercel-labs/agent-skills.git",                 "vercel-skills"),
    ("https://github.com/netlify/agent-skills.git",                     "netlify-skills"),
    ("https://github.com/cloudflare/agent-skills.git",                  "cloudflare-skills"),
    ("https://github.com/stripe/agent-skills.git",                      "stripe-skills"),
    # NEW BATCH
    ("https://github.com/expo/agent-skills.git",                        "expo-skills"),
    ("https://github.com/tinybird-co/agent-skills.git",                 "tinybird-skills"),
    ("https://github.com/hashicorp/agent-skills.git",                   "hashicorp-skills"),
    ("https://github.com/sanity-io/agent-skills.git",                   "sanity-skills"),
    ("https://github.com/firecrawl-dev/agent-skills.git",               "firecrawl-skills"),
    ("https://github.com/neondatabase/agent-skills.git",                "neon-skills"),
    ("https://github.com/replicate/agent-skills.git",                   "replicate-skills"),
    ("https://github.com/trailofbits/agent-skills.git",                 "trailofbits-skills"),
    ("https://github.com/transloadit/agent-skills.git",                 "transloadit-skills"),
    ("https://github.com/openai/codex-skills.git",                      "openai-skills"),
    ("https://github.com/skillmatic-ai/awesome-agent-skills.git",       "skillmatic-skills"),
    ("https://github.com/numman-ali/n-skills.git",                      "n-skills"),
    ("https://github.com/Digidai/product-manager-skills.git",           "pm-skills"),
    ("https://github.com/Orchestra-Research/AI-research-SKILLs.git",   "research-skills"),
    ("https://github.com/K-Dense-AI/claude-scientific-skills.git",      "scientific-skills"),
    ("https://github.com/ReScienceLab/opc-skills.git",                  "rescience-skills"),
    ("https://github.com/HeshamFS/materials-simulation-skills.git",     "materials-skills"),
    ("https://github.com/Paramchoudhary/ResumeSkills.git",              "resume-skills"),
    ("https://github.com/AgriciDaniel/claude-seo.git",                  "seo-skills"),
    ("https://github.com/BehiSecc/VibeSec-Skill.git",                   "vibesec-skills"),
    ("https://github.com/SHADOWPR0/security-bluebook-builder.git",      "security-bluebook"),
    ("https://github.com/RoundTable02/tutor-skills.git",                "tutor-skills"),
    ("https://github.com/ZhangHanDong/makepad-skills.git",              "makepad-skills"),
    ("https://github.com/CloudAI-X/threejs-skills.git",                 "threejs-extra-skills"),
    ("https://github.com/CosmoBlk/email-marketing-bible.git",          "email-marketing-skills"),
    ("https://github.com/Xquik-dev/tweetclaw.git",                      "tweetclaw-skills"),
    ("https://github.com/PSPDFKit-labs/nutrient-agent-skill.git",       "nutrient-skills"),
    ("https://github.com/SeanZoR/claude-speed-reader.git",              "speed-reader-skill"),
    ("https://github.com/Joannis/claude-skills.git",                    "joannis-skills"),
    ("https://github.com/AvdLee/SwiftUI-Agent-Skill.git",               "swiftui-skill"),
    ("https://github.com/Leonxlnx/taste-skill.git",                     "taste-skill"),
    ("https://github.com/alinaqi/claude-bootstrap.git",                 "bootstrap-skill"),
    ("https://github.com/Kevin7Qi/codex-collab.git",                    "codex-collab"),
    ("https://github.com/Charlie85270/Dorothy.git",                     "dorothy-skills"),
    ("https://github.com/Shpigford/skills.git",                         "shpigford-skills"),
    ("https://github.com/SHADOWPR0/beautiful_prose.git",                "prose-skills"),
    ("https://github.com/EveryInc/charlie-cfo-skill.git",               "cfo-skill"),
    ("https://github.com/PleasePrompto/notebooklm-skill.git",           "notebooklm-skill"),
    ("https://github.com/NotMyself/claude-win11-speckit-update-skill.git", "win11-skill"),
]

# ============================================================
# SMART CATEGORY DETECTION
# Uses FOLDER NAME as primary signal (most reliable)
# Falls back to content keywords only if name is generic
# ============================================================

# Explicit folder-name → category mappings (exact or partial match)
NAME_MAP = {
    # Auth
    "better-auth": "06-security-and-auth (by Luo Kai)/01-authentication-authorization",
    "auth": "06-security-and-auth (by Luo Kai)/01-authentication-authorization",
    "oauth": "06-security-and-auth (by Luo Kai)/01-authentication-authorization",
    "two-factor": "06-security-and-auth (by Luo Kai)/01-authentication-authorization",
    "twofactor": "06-security-and-auth (by Luo Kai)/01-authentication-authorization",
    "emailandpassword": "06-security-and-auth (by Luo Kai)/01-authentication-authorization",
    # Security
    "security": "06-security-and-auth (by Luo Kai)/02-application-security",
    "appsec": "06-security-and-auth (by Luo Kai)/02-application-security",
    "pentest": "06-security-and-auth (by Luo Kai)/03-penetration-testing",
    "devsecops": "06-security-and-auth (by Luo Kai)/05-devsecops",
    "gha-security": "06-security-and-auth (by Luo Kai)/05-devsecops",
    "django-access": "06-security-and-auth (by Luo Kai)/02-application-security",
    "django-perf": "06-security-and-auth (by Luo Kai)/02-application-security",
    "vibesec": "06-security-and-auth (by Luo Kai)/02-application-security",
    # React / Frontend
    "react-best-practices": "02-frontend-development (by Luo Kai)/01-react-ecosystem",
    "react-native": "10-mobile-development (by Luo Kai)/03-react-native",
    "react-native-skills": "10-mobile-development (by Luo Kai)/03-react-native",
    "composition-patterns": "02-frontend-development (by Luo Kai)/01-react-ecosystem",
    "nextjs": "02-frontend-development (by Luo Kai)/01-react-ecosystem",
    "next.js": "02-frontend-development (by Luo Kai)/01-react-ecosystem",
    "shadcn": "02-frontend-development (by Luo Kai)/06-css-styling",
    "shadcn-ui": "02-frontend-development (by Luo Kai)/06-css-styling",
    "css": "02-frontend-development (by Luo Kai)/06-css-styling",
    "tailwind": "02-frontend-development (by Luo Kai)/06-css-styling",
    "remotion": "02-frontend-development (by Luo Kai)/13-general-frontend",
    "stitch-design": "02-frontend-development (by Luo Kai)/13-general-frontend",
    "stitch-loop": "18-ai-agents-and-automation (by Luo Kai)/03-context-engineering",
    "design-md": "18-ai-agents-and-automation (by Luo Kai)/03-context-engineering",
    "enhance-prompt": "18-ai-agents-and-automation (by Luo Kai)/03-context-engineering",
    "vercel-cli": "05-devops-and-cloud (by Luo Kai)/10-serverless-platforms",
    "deploy-to-vercel": "05-devops-and-cloud (by Luo Kai)/10-serverless-platforms",
    "wp-": "02-frontend-development (by Luo Kai)/13-general-frontend",
    "wordpress": "02-frontend-development (by Luo Kai)/13-general-frontend",
    "wpds": "02-frontend-development (by Luo Kai)/13-general-frontend",
    "web-design-guidelines": "02-frontend-development (by Luo Kai)/13-general-frontend",
    "web-artifacts-builder": "02-frontend-development (by Luo Kai)/13-general-frontend",
    "frontend-design": "02-frontend-development (by Luo Kai)/13-general-frontend",
    "threejs": "02-frontend-development (by Luo Kai)/07-data-visualization",
    "three.js": "02-frontend-development (by Luo Kai)/07-data-visualization",
    "accessibility": "02-frontend-development (by Luo Kai)/10-accessibility",
    "wasm": "02-frontend-development (by Luo Kai)/12-webassembly",
    "webassembly": "02-frontend-development (by Luo Kai)/12-webassembly",
    # iOS / Mobile
    "swiftui": "10-mobile-development (by Luo Kai)/01-ios-swift",
    "swift": "10-mobile-development (by Luo Kai)/01-ios-swift",
    "ios": "10-mobile-development (by Luo Kai)/01-ios-swift",
    "android": "10-mobile-development (by Luo Kai)/02-android-kotlin",
    "flutter": "10-mobile-development (by Luo Kai)/04-flutter",
    # Databases
    "supabase": "04-databases-and-storage (by Luo Kai)/09-database-platforms",
    "postgres": "04-databases-and-storage (by Luo Kai)/01-relational-sql",
    "postgresql": "04-databases-and-storage (by Luo Kai)/01-relational-sql",
    "mysql": "04-databases-and-storage (by Luo Kai)/01-relational-sql",
    "sqlite": "04-databases-and-storage (by Luo Kai)/01-relational-sql",
    "mongodb": "04-databases-and-storage (by Luo Kai)/02-nosql-document",
    "redis": "04-databases-and-storage (by Luo Kai)/03-key-value-cache",
    "elasticsearch": "04-databases-and-storage (by Luo Kai)/04-search-engines",
    "clickhouse": "04-databases-and-storage (by Luo Kai)/04-search-engines",
    "vector": "04-databases-and-storage (by Luo Kai)/05-vector-databases",
    "neon": "04-databases-and-storage (by Luo Kai)/09-database-platforms",
    "stripe": "04-databases-and-storage (by Luo Kai)/10-payments-billing",
    "prisma": "04-databases-and-storage (by Luo Kai)/08-orm-query-builders",
    # DevOps / Cloud
    "aws": "05-devops-and-cloud (by Luo Kai)/01-aws",
    "azure": "05-devops-and-cloud (by Luo Kai)/02-azure",
    "gcp": "05-devops-and-cloud (by Luo Kai)/03-gcp",
    "kubernetes": "05-devops-and-cloud (by Luo Kai)/04-kubernetes",
    "k8s": "05-devops-and-cloud (by Luo Kai)/04-kubernetes",
    "docker": "05-devops-and-cloud (by Luo Kai)/05-docker-containers",
    "terraform": "05-devops-and-cloud (by Luo Kai)/06-terraform-iac",
    "github-actions": "05-devops-and-cloud (by Luo Kai)/07-cicd",
    "cicd": "05-devops-and-cloud (by Luo Kai)/07-cicd",
    "netlify": "05-devops-and-cloud (by Luo Kai)/10-serverless-platforms",
    "cloudflare": "05-devops-and-cloud (by Luo Kai)/10-serverless-platforms",
    "linux": "05-devops-and-cloud (by Luo Kai)/11-linux-sysadmin",
    "wpcli": "05-devops-and-cloud (by Luo Kai)/11-linux-sysadmin",
    "monitoring": "05-devops-and-cloud (by Luo Kai)/08-monitoring-observability",
    "nginx": "05-devops-and-cloud (by Luo Kai)/09-networking",
    "composio": "18-ai-agents-and-automation (by Luo Kai)/04-workspace-integrations",
    # Testing / QA
    "tdd": "07-testing-and-quality (by Luo Kai)/08-other-testing",
    "test-driven": "07-testing-and-quality (by Luo Kai)/08-other-testing",
    "playwright": "07-testing-and-quality (by Luo Kai)/02-e2e-testing",
    "cypress": "07-testing-and-quality (by Luo Kai)/02-e2e-testing",
    "jest": "07-testing-and-quality (by Luo Kai)/01-unit-testing",
    "pytest": "07-testing-and-quality (by Luo Kai)/01-unit-testing",
    "code-review": "07-testing-and-quality (by Luo Kai)/08-other-testing",
    "debugging": "07-testing-and-quality (by Luo Kai)/08-other-testing",
    "systematic-debugging": "07-testing-and-quality (by Luo Kai)/08-other-testing",
    "find-bugs": "07-testing-and-quality (by Luo Kai)/08-other-testing",
    "fix-tests": "07-testing-and-quality (by Luo Kai)/08-other-testing",
    "write-tests": "07-testing-and-quality (by Luo Kai)/08-other-testing",
    "phpstan": "07-testing-and-quality (by Luo Kai)/08-other-testing",
    "review-pr": "07-testing-and-quality (by Luo Kai)/08-other-testing",
    "review-local": "07-testing-and-quality (by Luo Kai)/08-other-testing",
    "code-simplifier": "07-testing-and-quality (by Luo Kai)/08-other-testing",
    "receiving-code-review": "07-testing-and-quality (by Luo Kai)/08-other-testing",
    "requesting-code-review": "07-testing-and-quality (by Luo Kai)/08-other-testing",
    # AI / ML / Data
    "fal-": "09-data-and-ai (by Luo Kai)/14-other-ai",
    "fal.ai": "09-data-and-ai (by Luo Kai)/14-other-ai",
    "hugging": "09-data-and-ai (by Luo Kai)/09-huggingface",
    "huggingface": "09-data-and-ai (by Luo Kai)/09-huggingface",
    "rag": "09-data-and-ai (by Luo Kai)/04-rag-retrieval",
    "mlops": "09-data-and-ai (by Luo Kai)/05-mlops",
    "prompt-engineering": "18-ai-agents-and-automation (by Luo Kai)/03-context-engineering",
    "llm": "09-data-and-ai (by Luo Kai)/03-llm-engineering",
    "research": "09-data-and-ai (by Luo Kai)/10-research-analysis",
    "scientific": "09-data-and-ai (by Luo Kai)/10-research-analysis",
    "materials": "14-chemistry-and-biology (by Luo Kai)",
    # Agent / Automation
    "voltagent": "18-ai-agents-and-automation (by Luo Kai)/01-agent-frameworks",
    "mcp": "18-ai-agents-and-automation (by Luo Kai)/02-mcp-tools",
    "build-mcp": "18-ai-agents-and-automation (by Luo Kai)/02-mcp-tools",
    "setup-arxiv-mcp": "18-ai-agents-and-automation (by Luo Kai)/02-mcp-tools",
    "setup-context7": "18-ai-agents-and-automation (by Luo Kai)/02-mcp-tools",
    "setup-serena": "18-ai-agents-and-automation (by Luo Kai)/02-mcp-tools",
    "setup-codemap": "18-ai-agents-and-automation (by Luo Kai)/02-mcp-tools",
    "claude-api": "18-ai-agents-and-automation (by Luo Kai)/02-mcp-tools",
    "brainstorm": "18-ai-agents-and-automation (by Luo Kai)/03-context-engineering",
    "parallel-agent": "18-ai-agents-and-automation (by Luo Kai)/03-context-engineering",
    "dispatching": "18-ai-agents-and-automation (by Luo Kai)/03-context-engineering",
    "subagent": "18-ai-agents-and-automation (by Luo Kai)/03-context-engineering",
    "tree-of-thoughts": "18-ai-agents-and-automation (by Luo Kai)/03-context-engineering",
    "reflexion": "18-ai-agents-and-automation (by Luo Kai)/03-context-engineering",
    "context-engineering": "18-ai-agents-and-automation (by Luo Kai)/03-context-engineering",
    "agents-md": "18-ai-agents-and-automation (by Luo Kai)/03-context-engineering",
    "verification-before": "18-ai-agents-and-automation (by Luo Kai)/03-context-engineering",
    "writing-plans": "18-ai-agents-and-automation (by Luo Kai)/03-context-engineering",
    "executing-plans": "18-ai-agents-and-automation (by Luo Kai)/03-context-engineering",
    "gmail": "18-ai-agents-and-automation (by Luo Kai)/04-workspace-integrations",
    "google-calendar": "18-ai-agents-and-automation (by Luo Kai)/04-workspace-integrations",
    "slack": "18-ai-agents-and-automation (by Luo Kai)/04-workspace-integrations",
    "notion": "18-ai-agents-and-automation (by Luo Kai)/04-workspace-integrations",
    "elevenlabs": "18-ai-agents-and-automation (by Luo Kai)/04-workspace-integrations",
    "tts": "18-ai-agents-and-automation (by Luo Kai)/04-workspace-integrations",
    "noizai": "18-ai-agents-and-automation (by Luo Kai)/04-workspace-integrations",
    "gumloop": "18-ai-agents-and-automation (by Luo Kai)/06-automation-workflows",
    "meeting": "18-ai-agents-and-automation (by Luo Kai)/10-task-management",
    "daily-brief": "18-ai-agents-and-automation (by Luo Kai)/10-task-management",
    "plan-my-day": "18-ai-agents-and-automation (by Luo Kai)/10-task-management",
    "go-mode": "18-ai-agents-and-automation (by Luo Kai)/10-task-management",
    "twitter": "18-ai-agents-and-automation (by Luo Kai)/12-social-media-agents",
    "tweet": "18-ai-agents-and-automation (by Luo Kai)/12-social-media-agents",
    "linkedin": "18-ai-agents-and-automation (by Luo Kai)/12-social-media-agents",
    "reddit": "18-ai-agents-and-automation (by Luo Kai)/12-social-media-agents",
    "youtube": "18-ai-agents-and-automation (by Luo Kai)/12-social-media-agents",
    "tweetclaw": "18-ai-agents-and-automation (by Luo Kai)/12-social-media-agents",
    "email-autoreply": "18-ai-agents-and-automation (by Luo Kai)/13-email-agents",
    # Git
    "git-": "11-specialized-coding (by Luo Kai)/02-git-version-control",
    "github": "11-specialized-coding (by Luo Kai)/02-git-version-control",
    "worktree": "11-specialized-coding (by Luo Kai)/02-git-version-control",
    "create-pr": "11-specialized-coding (by Luo Kai)/02-git-version-control",
    "pr-writer": "11-specialized-coding (by Luo Kai)/02-git-version-control",
    "commit": "11-specialized-coding (by Luo Kai)/02-git-version-control",
    "create-branch": "11-specialized-coding (by Luo Kai)/02-git-version-control",
    "finish-branch": "11-specialized-coding (by Luo Kai)/02-git-version-control",
    "analyze-issue": "11-specialized-coding (by Luo Kai)/02-git-version-control",
    "load-issues": "11-specialized-coding (by Luo Kai)/02-git-version-control",
    # Blockchain
    "blockchain": "11-specialized-coding (by Luo Kai)/04-blockchain-web3",
    "web3": "11-specialized-coding (by Luo Kai)/04-blockchain-web3",
    "solidity": "11-specialized-coding (by Luo Kai)/04-blockchain-web3",
    # Game dev
    "game-dev": "11-specialized-coding (by Luo Kai)/05-game-development",
    "unity": "11-specialized-coding (by Luo Kai)/05-game-development",
    "godot": "11-specialized-coding (by Luo Kai)/05-game-development",
    # Business / Marketing
    "marketing": "19-business-and-entrepreneurship (by Luo Kai)/04-marketing-content",
    "newsletter": "19-business-and-entrepreneurship (by Luo Kai)/04-marketing-content",
    "content-idea": "19-business-and-entrepreneurship (by Luo Kai)/04-marketing-content",
    "blog": "19-business-and-entrepreneurship (by Luo Kai)/04-marketing-content",
    "voice-extractor": "19-business-and-entrepreneurship (by Luo Kai)/04-marketing-content",
    "characteristic-voice": "19-business-and-entrepreneurship (by Luo Kai)/04-marketing-content",
    "social-card": "19-business-and-entrepreneurship (by Luo Kai)/04-marketing-content",
    "de-ai-ify": "19-business-and-entrepreneurship (by Luo Kai)/04-marketing-content",
    "internal-comms": "19-business-and-entrepreneurship (by Luo Kai)/04-marketing-content",
    "cold-outreach": "19-business-and-entrepreneurship (by Luo Kai)/05-sales-outreach",
    "cold-email": "19-business-and-entrepreneurship (by Luo Kai)/05-sales-outreach",
    "sales": "19-business-and-entrepreneurship (by Luo Kai)/05-sales-outreach",
    "kaizen": "19-business-and-entrepreneurship (by Luo Kai)/12-project-management",
    "root-cause": "19-business-and-entrepreneurship (by Luo Kai)/12-project-management",
    "retrospective": "19-business-and-entrepreneurship (by Luo Kai)/12-project-management",
    "homepage-audit": "19-business-and-entrepreneurship (by Luo Kai)/14-other-business",
    "ai-discoverability": "19-business-and-entrepreneurship (by Luo Kai)/14-other-business",
    "testimonial": "19-business-and-entrepreneurship (by Luo Kai)/14-other-business",
    "positioning": "19-business-and-entrepreneurship (by Luo Kai)/14-other-business",
    "resume": "19-business-and-entrepreneurship (by Luo Kai)/14-other-business",
    "seo": "19-business-and-entrepreneurship (by Luo Kai)/14-other-business",
    "cfo": "12-finance-and-trading (by Luo Kai)/10-other-finance",
    "product-manager": "19-business-and-entrepreneurship (by Luo Kai)/02-product-management",
    # Misc
    "speed-reader": "11-specialized-coding (by Luo Kai)/14-other-specialized",
    "skill-creator": "18-ai-agents-and-automation (by Luo Kai)/02-mcp-tools",
    "skill-writer": "18-ai-agents-and-automation (by Luo Kai)/02-mcp-tools",
    "skill-scanner": "18-ai-agents-and-automation (by Luo Kai)/02-mcp-tools",
    "skill-creator": "18-ai-agents-and-automation (by Luo Kai)/02-mcp-tools",
    "validate-skills": "18-ai-agents-and-automation (by Luo Kai)/02-mcp-tools",
    "presentation-creator": "11-specialized-coding (by Luo Kai)/14-other-specialized",
    "pptx": "11-specialized-coding (by Luo Kai)/03-document-processing",
    "docx": "11-specialized-coding (by Luo Kai)/03-document-processing",
    "pdf": "11-specialized-coding (by Luo Kai)/03-document-processing",
    "nutrient": "11-specialized-coding (by Luo Kai)/03-document-processing",
    "write-concisely": "11-specialized-coding (by Luo Kai)/14-other-specialized",
    "writing-skills": "11-specialized-coding (by Luo Kai)/14-other-specialized",
    "beautiful-prose": "11-specialized-coding (by Luo Kai)/14-other-specialized",
    "tutor": "09-data-and-ai (by Luo Kai)/10-research-analysis",
    "notebooklm": "18-ai-agents-and-automation (by Luo Kai)/04-workspace-integrations",
    "theme-factory": "02-frontend-development (by Luo Kai)/13-general-frontend",
    "brand-guidelines": "19-business-and-entrepreneurship (by Luo Kai)/04-marketing-content",
    "canvas-design": "02-frontend-development (by Luo Kai)/13-general-frontend",
    "algorithmic-art": "02-frontend-development (by Luo Kai)/13-general-frontend",
    "claude-settings": "18-ai-agents-and-automation (by Luo Kai)/02-mcp-tools",
    "sred": "19-business-and-entrepreneurship (by Luo Kai)/12-project-management",
    "bootstrap": "02-frontend-development (by Luo Kai)/06-css-styling",
    "makepad": "02-frontend-development (by Luo Kai)/13-general-frontend",
    "dorothy": "18-ai-agents-and-automation (by Luo Kai)/16-other-agents",
    "chat-with-anyone": "18-ai-agents-and-automation (by Luo Kai)/16-other-agents",
    "video-translation": "09-data-and-ai (by Luo Kai)/14-other-ai",
    "daily-news": "18-ai-agents-and-automation (by Luo Kai)/10-task-management",
    "win11": "05-devops-and-cloud (by Luo Kai)/11-linux-sysadmin",
    "taste": "20-health-and-wellness (by Luo Kai)/04-recipes-cooking",
    "email-marketing": "19-business-and-entrepreneurship (by Luo Kai)/04-marketing-content",
    "codex-collab": "18-ai-agents-and-automation (by Luo Kai)/16-other-agents",
    "last30days": "19-business-and-entrepreneurship (by Luo Kai)/14-other-business",
    "homepage": "19-business-and-entrepreneurship (by Luo Kai)/14-other-business",
    "vault-cleanup": "11-specialized-coding (by Luo Kai)/14-other-specialized",
    "webapp-testing": "18-ai-agents-and-automation (by Luo Kai)/15-claude-code-helpers",
    "claude-api": "18-ai-agents-and-automation (by Luo Kai)/02-mcp-tools",
    "update-docs": "11-specialized-coding (by Luo Kai)/14-other-specialized",
}

DEFAULT_CATEGORY = "18-ai-agents-and-automation (by Luo Kai)/16-other-agents"


def detect_category(skill_name):
    """Use folder name as primary signal — much more reliable than content."""
    name_lower = skill_name.lower()
    # Check longest match first (most specific)
    matches = [(k, v) for k, v in NAME_MAP.items() if k in name_lower]
    if matches:
        # Pick the longest matching key (most specific)
        return max(matches, key=lambda x: len(x[0]))[1]
    return DEFAULT_CATEGORY


def run(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr


def fix_author(content):
    if re.search(r'^author:', content, re.MULTILINE):
        content = re.sub(r'^author:.*$', f'author: {AUTHOR}', content, flags=re.MULTILINE)
    elif content.startswith('---'):
        content = content.replace('---\n', f'---\nauthor: {AUTHOR}\n', 1)
    return content


def slug(name):
    return re.sub(r'[^a-z0-9-]', '-', name.lower()).strip('-')


def get_existing_skills(repo_dir):
    existing = set()
    for root, dirs, files in os.walk(os.path.join(repo_dir, "ai-agent-skills")):
        if "SKILL.md" in files:
            existing.add(os.path.basename(root).lower())
    return existing


def main():
    if not GITHUB_TOKEN:
        print("[ERROR] Set GITHUB_TOKEN env var first: export GITHUB_TOKEN=your_token")
        sys.exit(1)

    stats = {"cloned": 0, "failed": 0, "installed": 0, "skipped": 0, "errors": 0}
    os.makedirs(WORK_DIR, exist_ok=True)

    # --- Setup repo ---
    if not os.path.exists(os.path.join(REPO_DIR, ".git")):
        remote = f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"
        ok, _, err = run(f"git clone {remote} {REPO_DIR}")
        if not ok:
            print(f"[FATAL] Cannot clone: {err[:200]}")
            sys.exit(1)
    else:
        run("git pull", cwd=REPO_DIR)

    run(f'git config user.email "{GITHUB_USER}@lous-creations.dev"', cwd=REPO_DIR)
    run(f'git config user.name "Luo Kai"', cwd=REPO_DIR)

    existing = get_existing_skills(REPO_DIR)
    print(f"[SETUP] {len(existing)} existing skills found")

    # --- Clone sources ---
    print(f"[CLONE] Cloning {len(SOURCE_REPOS)} source repos...")
    for url, dirname in SOURCE_REPOS:
        dest = os.path.join(WORK_DIR, dirname)
        if os.path.exists(dest):
            stats["cloned"] += 1
            continue
        ok, _, _ = run(f"git clone --depth=1 {url} {dest}")
        if ok:
            stats["cloned"] += 1
        else:
            stats["failed"] += 1

    # --- Find all SKILL.md files ---
    skill_files = []
    for root, dirs, files in os.walk(WORK_DIR):
        dirs[:] = [d for d in dirs if d != ".git"]
        if "SKILL.md" in files:
            skill_files.append(os.path.join(root, "SKILL.md"))

    print(f"[SCAN] Found {len(skill_files)} SKILL.md files")

    # --- Install each ---
    for skill_path in skill_files:
        skill_dir  = os.path.dirname(skill_path)
        skill_name = os.path.basename(skill_dir)
        skill_slug = slug(skill_name)

        if skill_slug in existing:
            stats["skipped"] += 1
            continue

        try:
            with open(skill_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            category = detect_category(skill_name)
            content  = fix_author(content)

            dest_dir = os.path.join(REPO_DIR, "ai-agent-skills", category, skill_slug)
            os.makedirs(dest_dir, exist_ok=True)

            with open(os.path.join(dest_dir, "SKILL.md"), 'w', encoding='utf-8') as f:
                f.write(content)

            # Copy supporting files
            for item in os.listdir(skill_dir):
                if item == "SKILL.md" or item.startswith('.'):
                    continue
                src = os.path.join(skill_dir, item)
                dst = os.path.join(dest_dir, item)
                try:
                    if os.path.isfile(src):
                        shutil.copy2(src, dst)
                    elif os.path.isdir(src) and not os.path.exists(dst):
                        shutil.copytree(src, dst)
                except Exception:
                    pass

            existing.add(skill_slug)
            stats["installed"] += 1

        except Exception as e:
            stats["errors"] += 1

    # --- Commit & push ---
    total = sum(1 for r, d, f in os.walk(os.path.join(REPO_DIR, "ai-agent-skills"))
                for fn in f if fn == "SKILL.md")

    run("git add .", cwd=REPO_DIR)
    msg = f"Auto-install: +{stats['installed']} skills (total: {total})"
    ok, _, _ = run(f'git commit -m "{msg}"', cwd=REPO_DIR)

    if ok:
        remote = f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"
        run(f"git remote set-url origin {remote}", cwd=REPO_DIR)
        push_ok, _, _ = run("git push", cwd=REPO_DIR)
        pushed = "✅ Pushed" if push_ok else "⚠️ Push failed"
    else:
        pushed = "ℹ️ Nothing new"

    print("\n" + "="*50)
    print("  DONE — Lous Creations / Luo Kai")
    print("="*50)
    print(f"  Repos cloned:    {stats['cloned']}")
    print(f"  Clone failures:  {stats['failed']}")
    print(f"  New skills:      {stats['installed']}")
    print(f"  Skipped:         {stats['skipped']}")
    print(f"  Errors:          {stats['errors']}")
    print(f"  Total now:       {total} skills")
    print(f"  Push:            {pushed}")
    print("="*50)


if __name__ == "__main__":
    main()
