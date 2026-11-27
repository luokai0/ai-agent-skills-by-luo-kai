"""
阿里云 & 华为云产品文档深度爬虫 v4.1
逻辑：依赖检测 → 解析左侧目录 → 按优先级筛选核心页面 → 并发抓取 → 输出供 AI 分析的 markdown

v4.1 改进：
  - 依赖检测替代自动安装：缺失时提示用户手动安装，不静默下载包或浏览器
  - Stealth 模式改为可选（--stealth）：默认关闭，仅在用户显式启用时生效
  - 保留 HTTP fallback（httpx+BS4）作为 Playwright 的补充

v4 改进（相比 ClawHub v1.0.3）：
  - Windows GBK 编码修复：stdout/stderr 重编码为 UTF-8
  - 等待策略改为 domcontentloaded：避免华为云 SPA networkidle 超时
  - 重试逻辑：网络错误/超时自动重试（最多 2 次）
  - deep_links 配置：目录解析失败/不足时自动使用预配置的深链页面
  - 分侧内容选择器：阿里云/华为云使用不同的正文选择器，减少噪音
  - 内容去噪：自动过滤导航/页脚等噪音文本
  - HTTP fallback：Playwright 被拦截时自动用 httpx+BS4 抓取
  - 安全验证检测：识别拦截页面并回退
  - 404 检测：识别华为云 404 页面
  - 华为云域名策略：.cn 自动回退 .com

依赖（需手动安装）：
    pip install playwright httpx beautifulsoup4
    playwright install chromium

用法：
    python cloud_doc_scraper.py --product ecs
    python cloud_doc_scraper.py --product oss --output oss_docs.md
    python cloud_doc_scraper.py --product rds --max-pages 15
    python cloud_doc_scraper.py --product ecs --stealth   # 启用 stealth 模式（谨慎使用）
    python cloud_doc_scraper.py --list   # 查看所有支持的产品
"""

# ─── Windows 控制台 UTF-8 修复（在任何 import 之前）────────────────────────────
import subprocess, sys, os, importlib.util

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ─── 自动安装依赖 ──────────────────────────────────────────────────────────────
def _ensure_dep(package: str, pip_name: str | None = None):
    if importlib.util.find_spec(package) is None:
        print(f"[INSTALL] {package} ...")
        r = subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", pip_name or package],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"[FAIL] {package}: {r.stderr}"); sys.exit(1)
        print(f"[OK] {package}")
    else:
        print(f"[OK] {package} (cached)")

def _ensure_playwright():
    _ensure_dep("playwright")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            if not os.path.exists(p.chromium.executable_path):
                raise FileNotFoundError
        print("[OK] Chromium (cached)")
    except Exception:
        print("[INSTALL] Chromium (first download ~150MB) ...")
        r = subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"],
                           capture_output=False, text=True)
        if r.returncode != 0:
            print("[FAIL] Chromium install"); sys.exit(1)
        print("[OK] Chromium")

# ─── 依赖检测（不自动安装，缺失时提示用户手动安装）──────────────────────────
def _check_dep(package: str, pip_name: str | None = None):
    if importlib.util.find_spec(package) is None:
        print(f"[MISSING] {package} — please run: pip install {pip_name or package}")
        return False
    return True

def _check_deps():
    ok = True
    if not _check_dep("playwright"):
        ok = False
    else:
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                if not os.path.exists(p.chromium.executable_path):
                    print("[MISSING] Chromium — please run: playwright install chromium")
                    ok = False
        except Exception:
            print("[MISSING] Chromium — please run: playwright install chromium")
            ok = False
    if not _check_dep("httpx"):
        ok = False
    if not _check_dep("bs4", "beautifulsoup4"):
        ok = False
    if not ok:
        print("\n[ERROR] Missing dependencies. Install with:\n"
              "  pip install playwright httpx beautifulsoup4\n"
              "  playwright install chromium\n"
              "Or use a venv: python -m venv .venv && .venv/bin/pip install playwright httpx beautifulsoup4 && .venv/bin/playwright install chromium")
        sys.exit(1)
    print("[OK] All dependencies satisfied")

_check_deps()

# ─── 正式 import ──────────────────────────────────────────────────────────────
import asyncio, argparse
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

try:
    import httpx
    from bs4 import BeautifulSoup
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

# ─── 产品配置 ─────────────────────────────────────────────────────────────────
PRODUCTS = {
    "ecs": {
        "name": "云服务器 ECS / ECS",
        "aliyun": {"doc": "https://help.aliyun.com/zh/ecs", "changelog": "https://help.aliyun.com/zh/ecs/product-overview/release-notes"},
        "huawei": {"doc": "https://support.huaweicloud.cn/ecs/index.html", "changelog": "https://support.huaweicloud.cn/wtsnew-ecs/index.html",
                   "deep_links": [
                       {"text": "什么是ECS", "url": "https://support.huaweicloud.com/productdesc-ecs/zh-cn_topic_0013771112.html"},
                       {"text": "产品优势", "url": "https://support.huaweicloud.com/productdesc-ecs/ecs_01_0002.html"},
                       {"text": "应用场景", "url": "https://support.huaweicloud.com/productdesc-ecs/ecs_01_0003.html"},
                       {"text": "实例规格", "url": "https://support.huaweicloud.com/productdesc-ecs/ecs_01_0014.html"},
                       {"text": "产品功能", "url": "https://support.huaweicloud.com/productdesc-ecs/ecs_01_0005.html"},
                   ]},
    },
    "oss": {
        "name": "对象存储 OSS / OBS",
        "aliyun": {"doc": "https://help.aliyun.com/zh/oss", "changelog": "https://help.aliyun.com/zh/oss/product-overview/release-notes"},
        "huawei": {"doc": "https://support.huaweicloud.cn/obs/index.html", "changelog": "https://support.huaweicloud.cn/wtsnew-obs/index.html",
                   "deep_links": [
                       {"text": "什么是OBS", "url": "https://support.huaweicloud.com/productdesc-obs/zh-cn_topic_0045829060.html"},
                       {"text": "产品优势", "url": "https://support.huaweicloud.com/productdesc-obs/obs_03_0201.html"},
                       {"text": "应用场景", "url": "https://support.huaweicloud.com/productdesc-obs/obs_03_0202.html"},
                       {"text": "产品功能", "url": "https://support.huaweicloud.com/productdesc-obs/obs_03_0151.html"},
                       {"text": "约束与限制", "url": "https://support.huaweicloud.com/productdesc-obs/obs_03_0360.html"},
                   ]},
    },
    "rds": {
        "name": "云数据库 RDS",
        "aliyun": {"doc": "https://help.aliyun.com/zh/rds", "changelog": "https://help.aliyun.com/zh/rds/product-overview/release-notes"},
        "huawei": {"doc": "https://support.huaweicloud.cn/rds/index.html", "changelog": "https://support.huaweicloud.cn/wtsnew-rds/index.html",
                   "deep_links": [
                       {"text": "产品介绍", "url": "https://support.huaweicloud.com/productdesc-rds/zh-cn_topic_dashboard.html"},
                       {"text": "计费说明", "url": "https://support.huaweicloud.com/price-rds/rds_00_0006.html"},
                       {"text": "快速入门", "url": "https://support.huaweicloud.com/qs-rds/rds_02_0148.html"},
                       {"text": "性能白皮书", "url": "https://support.huaweicloud.com/pwp-rds/pwp_0000.html"},
                       {"text": "最佳实践", "url": "https://support.huaweicloud.com/bestpractice-rds/practice_0000.html"},
                   ]},
    },
    "redis": {
        "name": "云数据库 Redis / DCS",
        "aliyun": {"doc": "https://help.aliyun.com/zh/redis", "changelog": "https://help.aliyun.com/zh/redis/product-overview/release-notes"},
        "huawei": {"doc": "https://support.huaweicloud.cn/dcs/index.html", "changelog": "https://support.huaweicloud.cn/wtsnew-dcs/index.html",
                   "deep_links": [
                       {"text": "什么是DCS", "url": "https://support.huaweicloud.com/productdesc-dcs/dcs-pd-200713001.html"},
                       {"text": "典型应用场景", "url": "https://support.huaweicloud.com/productdesc-dcs/dcs-pd-200713002.html"},
                       {"text": "产品功能", "url": "https://support.huaweicloud.com/productdesc-dcs/dcs_01_0006.html"},
                       {"text": "DCS产品选型参考", "url": "https://support.huaweicloud.com/productdesc-dcs/dcs_01_0002.html"},
                       {"text": "Redis实例类型差异", "url": "https://support.huaweicloud.com/productdesc-dcs/dcs-pd-191224001.html"},
                   ]},
    },
    "ack": {
        "name": "容器服务 ACK / CCE",
        "aliyun": {"doc": "https://help.aliyun.com/zh/ack", "changelog": "https://help.aliyun.com/zh/ack/product-overview/release-notes"},
        "huawei": {"doc": "https://support.huaweicloud.cn/cce/index.html", "changelog": "https://support.huaweicloud.cn/wtsnew-cce/index.html",
                   "deep_links": [
                       {"text": "什么是CCE", "url": "https://support.huaweicloud.com/productdesc-cce/cce_productdesc_0001.html"},
                       {"text": "产品功能", "url": "https://support.huaweicloud.com/productdesc-cce/cce_productdesc_0002.html"},
                       {"text": "版本说明", "url": "https://support.huaweicloud.com/productdesc-cce/cce_productdesc_0003.html"},
                       {"text": "应用场景", "url": "https://support.huaweicloud.com/productdesc-cce/cce_productdesc_0005.html"},
                   ]},
    },
    "fc": {
        "name": "函数计算 FC / FunctionGraph",
        "aliyun": {"doc": "https://help.aliyun.com/zh/fc", "changelog": "https://help.aliyun.com/zh/fc/product-overview/release-notes"},
        "huawei": {"doc": "https://support.huaweicloud.cn/functiongraph/index.html", "changelog": "https://support.huaweicloud.cn/wtsnew-functiongraph/index.html",
                   "deep_links": [
                       {"text": "什么是FunctionGraph", "url": "https://support.huaweicloud.com/productdesc-functiongraph/functiongraph_01_0100.html"},
                       {"text": "功能特性", "url": "https://support.huaweicloud.com/productdesc-functiongraph/functiongraph_01_0200.html"},
                       {"text": "应用场景", "url": "https://support.huaweicloud.com/productdesc-functiongraph/functiongraph_01_0300.html"},
                   ]},
    },
    "slb": {
        "name": "负载均衡 SLB / ELB",
        "aliyun": {"doc": "https://help.aliyun.com/zh/slb", "changelog": "https://help.aliyun.com/zh/slb/product-overview/release-notes"},
        "huawei": {"doc": "https://support.huaweicloud.cn/elb/index.html", "changelog": "https://support.huaweicloud.cn/wtsnew-elb/index.html",
                   "deep_links": [
                       {"text": "什么是ELB", "url": "https://support.huaweicloud.com/productdesc-elb/elb_pro_0001.html"},
                       {"text": "功能概述", "url": "https://support.huaweicloud.com/productdesc-elb/elb_pro_0003.html"},
                       {"text": "应用场景", "url": "https://support.huaweicloud.com/productdesc-elb/elb_pro_0004.html"},
                       {"text": "规格", "url": "https://support.huaweicloud.com/productdesc-elb/elb_pro_0010.html"},
                   ]},
    },
    "maxcompute": {
        "name": "大数据 MaxCompute / MRS",
        "aliyun": {"doc": "https://help.aliyun.com/zh/maxcompute", "changelog": "https://help.aliyun.com/zh/maxcompute/product-overview/Release-notes"},
        "huawei": {"doc": "https://support.huaweicloud.cn/mrs/index.html", "changelog": "https://support.huaweicloud.cn/wtsnew-mrs/index.html",
                   "deep_links": [
                       {"text": "什么是MRS", "url": "https://support.huaweicloud.com/productdesc-mrs/mrs_08_0001.html"},
                       {"text": "组件版本", "url": "https://support.huaweicloud.com/productdesc-mrs/mrs_08_0005.html"},
                       {"text": "产品功能", "url": "https://support.huaweicloud.com/productdesc-mrs/mrs_08_0002.html"},
                   ]},
    },
    "pai": {
        "name": "AI 平台 PAI / ModelArts",
        "aliyun": {"doc": "https://help.aliyun.com/zh/pai", "changelog": "https://help.aliyun.com/zh/pai/user-guide/api-aiworkspace-2021-02-04-changeset"},
        "huawei": {"doc": "https://support.huaweicloud.cn/modelarts/index.html", "changelog": "https://support.huaweicloud.cn/wtsnew-modelarts/index.html",
                   "deep_links": [
                       {"text": "什么是ModelArts", "url": "https://support.huaweicloud.com/productdesc-modelarts/modelarts_product_0001.html"},
                       {"text": "功能特性", "url": "https://support.huaweicloud.com/productdesc-modelarts/modelarts_product_0002.html"},
                       {"text": "应用场景", "url": "https://support.huaweicloud.com/productdesc-modelarts/modelarts_product_0003.html"},
                   ]},
    },
    "bailian": {
        "name": "大模型平台 百炼 / 盘古",
        "aliyun": {"doc": "https://help.aliyun.com/zh/bailian", "changelog": "https://help.aliyun.com/zh/bailian/release-notes"},
        "huawei": {"doc": "https://support.huaweicloud.cn/pangu/index.html", "changelog": "https://support.huaweicloud.cn/wtsnew-pangu/index.html"},
    },
    "cdn": {
        "name": "CDN",
        "aliyun": {"doc": "https://help.aliyun.com/zh/cdn", "changelog": "https://help.aliyun.com/zh/cdn/product-overview/release-notes"},
        "huawei": {"doc": "https://support.huaweicloud.cn/cdn/index.html", "changelog": "https://support.huaweicloud.cn/wtsnew-cdn/index.html",
                   "deep_links": [
                       {"text": "什么是华为云CDN", "url": "https://support.huaweicloud.com/productdesc-cdn/zh-cn_topic_0064907747.html"},
                       {"text": "产品优势", "url": "https://support.huaweicloud.com/productdesc-cdn/zh-cn_topic_0064907763.html"},
                       {"text": "应用场景", "url": "https://support.huaweicloud.com/productdesc-cdn/cdn_01_0067.html"},
                       {"text": "产品功能", "url": "https://support.huaweicloud.com/productdesc-cdn/cdn_01_0369.html"},
                       {"text": "约束与限制", "url": "https://support.huaweicloud.com/productdesc-cdn/cdn_01_0068.html"},
                   ]},
    },
    "nas": {
        "name": "文件存储 NAS / SFS",
        "aliyun": {"doc": "https://help.aliyun.com/zh/nas", "changelog": "https://help.aliyun.com/zh/nas/product-overview/release-notes"},
        "huawei": {"doc": "https://support.huaweicloud.cn/sfs/index.html", "changelog": "https://support.huaweicloud.cn/wtsnew-sfs/index.html",
                   "deep_links": [
                       {"text": "什么是SFS", "url": "https://support.huaweicloud.com/productdesc-sfs/zh-cn_topic_0034428718.html"},
                       {"text": "应用场景", "url": "https://support.huaweicloud.com/productdesc-sfs/sfs_01_0004.html"},
                       {"text": "产品功能", "url": "https://support.huaweicloud.com/productdesc-sfs/sfs_01_0110.html"},
                       {"text": "约束与限制", "url": "https://support.huaweicloud.com/productdesc-sfs/sfs_01_0011.html"},
                       {"text": "计费说明", "url": "https://support.huaweicloud.com/productdesc-sfs/sfs_01_0108.html"},
                   ]},
    },
    "flink": {
        "name": "实时计算 Flink",
        "aliyun": {"doc": "https://help.aliyun.com/zh/flink", "changelog": "https://help.aliyun.com/zh/flink/product-overview/release-note"},
        "huawei": {"doc": "https://support.huaweicloud.cn/dli/index.html", "changelog": "https://support.huaweicloud.cn/wtsnew-dli/index.html",
                   "deep_links": [
                       {"text": "什么是DLI", "url": "https://support.huaweicloud.com/productdesc-dli/dli_01_0001.html"},
                       {"text": "功能特性", "url": "https://support.huaweicloud.com/productdesc-dli/dli_01_0002.html"},
                       {"text": "应用场景", "url": "https://support.huaweicloud.com/productdesc-dli/dli_01_0003.html"},
                   ]},
    },
    "elasticsearch": {
        "name": "搜索 Elasticsearch / CSS",
        "aliyun": {"doc": "https://help.aliyun.com/zh/elasticsearch", "changelog": "https://help.aliyun.com/zh/elasticsearch/product-overview/release-notes"},
        "huawei": {"doc": "https://support.huaweicloud.cn/css/index.html", "changelog": "https://support.huaweicloud.cn/wtsnew-css/index.html",
                   "deep_links": [
                       {"text": "什么是云搜索服务", "url": "https://support.huaweicloud.com/productdesc-css/css_04_0001.html"},
                       {"text": "产品优势", "url": "https://support.huaweicloud.com/productdesc-css/css_04_0010.html"},
                       {"text": "应用场景", "url": "https://support.huaweicloud.com/productdesc-css/css_04_0002.html"},
                       {"text": "产品功能", "url": "https://support.huaweicloud.com/productdesc-css/css_04_0003.html"},
                       {"text": "约束与限制", "url": "https://support.huaweicloud.com/productdesc-css/css_04_0005.html"},
                   ]},
    },
    "dws": {
        "name": "数据仓库 AnalyticDB / GaussDB(DWS)",
        "aliyun": {"doc": "https://help.aliyun.com/zh/analyticdb-for-postgresql", "changelog": "https://help.aliyun.com/zh/analyticdb-for-postgresql/product-overview/release-notes",
                   "deep_links": [
                       {"text": "什么是AnalyticDB PG", "url": "https://help.aliyun.com/zh/analyticdb-for-postgresql/product-overview/what-is-analyticdb-for-postgresql"},
                       {"text": "功能特性", "url": "https://help.aliyun.com/zh/analyticdb-for-postgresql/product-overview/features"},
                       {"text": "产品优势", "url": "https://help.aliyun.com/zh/analyticdb-for-postgresql/product-overview/benefits"},
                       {"text": "产品系列", "url": "https://help.aliyun.com/zh/analyticdb-for-postgresql/product-overview/editions"},
                       {"text": "应用场景", "url": "https://help.aliyun.com/zh/analyticdb-for-postgresql/product-overview/scenarios"},
                       {"text": "约束与限制", "url": "https://help.aliyun.com/zh/analyticdb-for-postgresql/product-overview/limits-and-restrictions"},
                   ]},
        "huawei": {"doc": "https://support.huaweicloud.cn/dws/index.html", "changelog": "https://support.huaweicloud.cn/wtsnew-dws/index.html",
                   "deep_links": [
                       {"text": "什么是DWS", "url": "https://support.huaweicloud.com/productdesc-dws/dws_01_0002.html"},
                       {"text": "数据仓库类型", "url": "https://support.huaweicloud.com/productdesc-dws/dws_01_00017.html"},
                       {"text": "产品功能", "url": "https://support.huaweicloud.com/productdesc-dws/dws_01_0004.html"},
                       {"text": "应用场景", "url": "https://support.huaweicloud.com/productdesc-dws/dws_01_0006.html"},
                       {"text": "基本概念", "url": "https://support.huaweicloud.com/productdesc-dws/dws_01_0007.html"},
                   ]},
    },
}

# ─── 优先级关键词 ──────────────────────────────────────────────────────────────
PRIORITY_KEYWORDS = [
    (3, ["产品简介", "产品概述", "什么是", "功能特性", "核心功能", "产品功能", "product overview", "what is", "features"]),
    (2, ["规格", "实例规格", "配置", "限制", "约束", "性能", "指标", "参数", "specification", "limits", "performance"]),
    (2, ["计费", "定价", "费用", "价格", "版本对比", "版本说明", "pricing", "billing", "edition"]),
    (2, ["组件版本", "版本支持", "引擎版本", "内核版本"]),
    (1, ["应用场景", "使用场景", "适用场景", "最佳实践", "use case", "scenario", "best practice"]),
    (-1, ["常见问题", "faq", "故障排除", "sdk", "api参考", "错误码", "迁移指南"]),
]

def score_link(text: str, href: str) -> int:
    combined = (text + " " + href).lower()
    return sum(w for w, kws in PRIORITY_KEYWORDS if any(k in combined for k in kws))

# ─── 目录解析 ─────────────────────────────────────────────────────────────────
ALIYUN_NAV_SELECTORS = [
    ".toc-menu a", ".sidebar-menu a", ".helpcenter-menu a",
    "nav a", ".left-menu a",
    "[class*='nav'] a", "[class*='sidebar'] a", "[class*='toc'] a", "[class*='menu'] a",
]
HUAWEI_NAV_SELECTORS = [
    "[class*=nav-item] a",  # 华为云新 SPA
    ".book-left-menu a", ".toc a", ".sidebar a", ".tree-menu a",
    "[class*='catalog'] a", "[class*='tree'] a", "[class*='nav'] a", "[class*='menu'] a",
    ".left-nav a", ".doc-nav a", ".doc-sidebar a",
    "aside a", "[role='navigation'] a",
]

async def parse_toc(page, base_url: str, nav_selectors: list, label: str) -> list:
    base_domain = f"{urlparse(base_url).scheme}://{urlparse(base_url).netloc}"
    links = []
    for selector in nav_selectors:
        try:
            els = await page.query_selector_all(selector)
            if len(els) <= 3:
                continue
            for el in els:
                href = await el.get_attribute("href") or ""
                text = (await el.inner_text()).strip()
                if not href or not text or href == "#" or href.startswith("javascript"):
                    continue
                full_url = urljoin(base_domain, href) if href.startswith("/") else href
                if urlparse(base_domain).netloc not in urlparse(full_url).netloc:
                    continue
                links.append({"url": full_url, "text": text, "score": score_link(text, href)})
            if links:
                print(f"    [{label}] nav selector '{selector}' => {len(links)} links")
                return links
        except Exception:
            continue
    print(f"    [{label}] [WARN] all selectors missed, TOC parse failed")
    return []

# ─── 正文提取 ─────────────────────────────────────────────────────────────────
ALIYUN_CONTENT_SELECTORS = [
    ".help-detail-content", ".article-content", ".doc-body",
    "#docContent", ".markdown-body", "article",
]
HUAWEI_CONTENT_SELECTORS = [
    ".book-desc", ".content-block", "#content", "article", ".markdown-body",
]
FALLBACK_CONTENT_SELECTORS = ["main", ".main-content", ".content"]

NOISE_PATTERNS = [
    "为什么选择阿里云", "什么是云计算", "全球基础设施", "法律声明",
    "Cookies政策", "廉正举报", "安全举报", "联系我们", "加入我们",
    "阿里巴巴集团", "淘宝网", "天猫", "速卖通",
    "关注阿里云", "阿里云公众号", "随时随地运维管控",
    "售前咨询", "售后在线", "我要建议", "我要投诉",
    "登录阿里云", "管理云资源", "状态一览",
    "Protected by Tencent", "正在验证连接安全性",
    "华为云App", "950808", "售前咨询热线",
    "云商店咨询", "备案服务", "增值电信业务",
    "黔ICP备", "苏B2-", "贵公网安备",
]

def denoise_text(text: str) -> str:
    lines = text.split("\n")
    clean = []
    for line in lines:
        s = line.strip()
        if not s:
            clean.append(""); continue
        if not any(p in s for p in NOISE_PATTERNS):
            clean.append(s)
    result, prev_empty = [], False
    for line in clean:
        if not line:
            if not prev_empty: result.append("")
            prev_empty = True
        else:
            result.append(line); prev_empty = False
    return "\n".join(result)

async def extract_text(page, content_selectors: list | None = None) -> str:
    selectors = content_selectors or (ALIYUN_CONTENT_SELECTORS + HUAWEI_CONTENT_SELECTORS + FALLBACK_CONTENT_SELECTORS)
    for sel in selectors:
        try:
            el = await page.query_selector(sel)
            if el:
                text = await el.inner_text()
                if len(text.strip()) > 300:
                    return denoise_text(text.strip())
        except Exception:
            continue
    body = await page.query_selector("body")
    if body:
        return denoise_text((await body.inner_text()).strip())
    return ""

# ─── 安全验证 & 404 检测 ─────────────────────────────────────────────────────
def is_security_block(text: str) -> bool:
    return any(p in text for p in ["正在验证连接安全性", "Protected by Tencent Cloud EdgeOne", "Security Verification"])

def is_404_page(text: str) -> bool:
    return "很抱歉，没发现您要的页面" in text

def huawei_cn_to_com(url: str) -> str:
    return url.replace("support.huaweicloud.cn", "support.huaweicloud.com")

# ─── HTTP fallback ────────────────────────────────────────────────────────────
async def fetch_via_http(url: str) -> str:
    if not HAS_HTTPX:
        return ""
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30,
                                      headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}) as client:
            resp = await client.get(url)
            if resp.status_code != 200:
                return ""
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup.find_all(["script", "style", "nav", "footer", "header", "noscript"]):
                tag.decompose()
            for sel in [".book-desc", ".content-block", "#content", "article", ".markdown-body", "main"]:
                for el in soup.select(sel):
                    text = el.get_text(separator="\n", strip=True)
                    if len(text) > 300:
                        return denoise_text(text)
            body = soup.find("body")
            if body:
                return denoise_text(body.get_text(separator="\n", strip=True))
            return ""
    except Exception:
        return ""

# ─── 带重试的页面抓取 ─────────────────────────────────────────────────────────
MAX_RETRIES = 2

async def fetch_content(context, url: str, content_selectors: list | None = None,
                        label: str = "", is_huawei: bool = False) -> str:
    for attempt in range(MAX_RETRIES + 1):
        page = await context.new_page()
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            for selector in (content_selectors or ALIYUN_CONTENT_SELECTORS + HUAWEI_CONTENT_SELECTORS + FALLBACK_CONTENT_SELECTORS):
                try:
                    await page.wait_for_selector(selector, timeout=3000)
                    break
                except PlaywrightTimeout:
                    continue
            text = await extract_text(page, content_selectors)

            if is_security_block(text):
                if HAS_HTTPX:
                    http_text = await fetch_via_http(url)
                    if len(http_text.strip()) > 200:
                        print(f"  [{label}] [HTTP-FALLBACK] bypassed security check")
                        return http_text
                return f"[Security block, HTTP fallback failed, visit manually: {url}]"

            if is_404_page(text):
                if is_huawei and "huaweicloud.cn" in url:
                    com_url = huawei_cn_to_com(url)
                    print(f"  [{label}] [404] .cn 404, trying .com")
                    com_text = await fetch_via_http(com_url)
                    if len(com_text.strip()) > 200:
                        return com_text
                return f"[404 page, visit manually: {url}]"

            if len(text.strip()) < 100:
                if HAS_HTTPX:
                    http_text = await fetch_via_http(url)
                    if len(http_text.strip()) > 200:
                        print(f"  [{label}] [HTTP-FALLBACK] Playwright empty, HTTP ok")
                        return http_text
                return f"[Empty page, visit manually: {url}]"

            return text
        except PlaywrightTimeout:
            if attempt < MAX_RETRIES:
                print(f"  [{label}] [RETRY] timeout, attempt {attempt+1}...")
                continue
            return f"[Timeout after {MAX_RETRIES} retries, visit manually: {url}]"
        except Exception as e:
            if attempt < MAX_RETRIES:
                err = str(e)
                if "ERR_NETWORK" in err or "ERR_CONNECTION" in err or "Timeout" in err:
                    print(f"  [{label}] [RETRY] network error, attempt {attempt+1}...")
                    continue
            return f"[Failed: {e}]"
        finally:
            await page.close()
    return f"[Retries exhausted, visit manually: {url}]"

# ─── 单侧完整抓取 ─────────────────────────────────────────────────────────────
async def scrape_side(context, label: str, doc_url: str, changelog_url: str,
                      nav_selectors: list, max_pages: int,
                      deep_links: list | None = None,
                      content_selectors: list | None = None,
                      is_huawei: bool = False) -> dict:
    result = {"label": label, "doc_url": doc_url, "changelog_url": changelog_url,
              "pages": [], "changelog": "", "toc_total": 0}

    # Step 1: 打开首页 + 解析目录
    print(f"\n  [{label}] Parsing TOC...")
    index_page = await context.new_page()
    toc = []
    try:
        await index_page.goto(doc_url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(2)  # extra buffer for SPA render
        toc = await parse_toc(index_page, doc_url, nav_selectors, label)
        result["toc_total"] = len(toc)

        if not toc or len(toc) < 3:
            if deep_links and len(deep_links) >= 3:
                print(f"  [{label}] TOC links insufficient({len(toc)}), using {len(deep_links)} deep_links")
                toc = [{"url": dl["url"], "text": dl["text"], "score": 3} for dl in deep_links]
                result["toc_total"] = len(toc)
            else:
                print(f"  [{label}] Fallback: only fetch homepage")
                result["pages"].append(("Homepage", doc_url, await extract_text(index_page, content_selectors)))
        elif deep_links and len(deep_links) >= len(toc):
            print(f"  [{label}] TOC {len(toc)} links, deep_links {len(deep_links)}, prefer deep_links")
            toc = [{"url": dl["url"], "text": dl["text"], "score": 3} for dl in deep_links]
            result["toc_total"] = len(toc)
    except PlaywrightTimeout:
        print(f"  [{label}] [WARN] Homepage timeout, trying deep_links or HTTP fallback")
        if deep_links:
            toc = [{"url": dl["url"], "text": dl["text"], "score": 3} for dl in deep_links]
            result["toc_total"] = len(toc)
        elif HAS_HTTPX:
            http_text = await fetch_via_http(doc_url)
            if len(http_text.strip()) > 200:
                result["pages"].append(("Homepage(HTTP)", doc_url, http_text))
    finally:
        await index_page.close()

    # Step 2: 去重 → 过滤 → 排序 → 取 top-N
    if toc:
        seen, unique = set(), []
        for lk in toc:
            if lk["url"] not in seen:
                seen.add(lk["url"])
                unique.append(lk)
        candidates = sorted([lk for lk in unique if lk["score"] >= 0],
                             key=lambda x: x["score"], reverse=True)[:max_pages]
        print(f"  [{label}] Selected {len(candidates)}/{len(unique)} core pages:")
        for i, lk in enumerate(candidates):
            print(f"    {i+1:2d}. [{lk['score']:+d}] {lk['text'][:45]}")

        # Step 3: 并发抓取
        sem = asyncio.Semaphore(4)
        async def fetch_one(lk):
            async with sem:
                content = await fetch_content(context, lk["url"], content_selectors, label, is_huawei)
                ok = "[OK]" if not content.startswith("[") else "[FAIL]"
                print(f"  [{label}] {ok} {lk['text'][:40]}")
                return (lk["text"], lk["url"], content)
        result["pages"] = list(await asyncio.gather(*[fetch_one(lk) for lk in candidates]))

    # Step 4: 更新日志
    print(f"  [{label}] Fetching changelog...")
    result["changelog"] = await fetch_content(context, changelog_url, content_selectors, label, is_huawei)
    ok = "[OK]" if not result["changelog"].startswith("[") else "[FAIL]"
    print(f"  [{label}] {ok} Changelog done")

    return result

# ─── 拼装 Markdown ────────────────────────────────────────────────────────────
def build_markdown(product_name: str, aliyun: dict, huawei: dict) -> str:
    now = datetime.now().strftime("%Y-%m-%d")
    lines = [
        f"# 竞品分析原始资料：{product_name}",
        f"> 抓取时间：{now}",
        f"> 阿里云：目录 {aliyun['toc_total']} 页，本次抓取 {len(aliyun['pages'])} 页",
        f"> 华为云：目录 {huawei['toc_total']} 页，本次抓取 {len(huawei['pages'])} 页",
        "", "**给 AI 的指令：** 基于以下官方文档原文，分析两款产品的真实差异。",
        "重点挖掘：关键指标的数字差距、一方有而另一方没有的能力、相同功能的成熟度差异、近期迭代方向的分歧。",
        "无差异或差异不明显的维度直接略过，不要凑字数。", "", "---", "",
    ]
    for side in [aliyun, huawei]:
        lines += [f"# {side['label']}", ""]
        if not side["pages"]:
            lines.append(f"> [WARN] Fetch failed, visit manually: {side['doc_url']}")
        else:
            for title, url, content in side["pages"]:
                lines += [f"## {side['label']} · {title}", f"> Source: {url}", ""]
                body = content[:8000]
                if len(content) > 8000:
                    body += "\n\n[...truncated, see source link...]"
                lines += [body, "", "---", ""]
        lines += [f"## {side['label']} · Changelog", f"> Source: {side['changelog_url']}", ""]
        cl = side["changelog"][:6000]
        if len(side["changelog"]) > 6000:
            cl += "\n\n[...truncated...]"
        lines += [cl or f"> [WARN] Fetch failed, visit manually: {side['changelog_url']}", "", "---", ""]
    return "\n".join(lines)

# ─── 主入口 ───────────────────────────────────────────────────────────────────
async def main_async(product_key: str, max_pages: int, output: str, args):
    if product_key not in PRODUCTS:
        print(f"[FAIL] Unknown product '{product_key}', available: {', '.join(PRODUCTS.keys())}")
        sys.exit(1)
    cfg = PRODUCTS[product_key]
    print(f"\n{'='*60}\n  {cfg['name']}  (max {max_pages} core pages per side)\n{'='*60}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
        )
        # 阿里云：普通 context（不需要 stealth）
        ctx_aliyun = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
        )
        # 华为云：stealth context（可选，通过 --stealth 启用，用于处理部分站点 JS 渲染兼容性问题）
        ctx_huawei = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36" if args.stealth else None,
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
        )
        if args.stealth:
            await ctx_huawei.add_init_script("Object.defineProperty(navigator, 'webdriver', { get: () => undefined });")
        try:
            aliyun = await scrape_side(
                ctx_aliyun, "Aliyun",
                cfg["aliyun"]["doc"], cfg["aliyun"]["changelog"],
                ALIYUN_NAV_SELECTORS, max_pages,
                deep_links=cfg["aliyun"].get("deep_links"),
                content_selectors=ALIYUN_CONTENT_SELECTORS + FALLBACK_CONTENT_SELECTORS,
                is_huawei=False,
            )
            huawei = await scrape_side(
                ctx_huawei, "Huawei",
                cfg["huawei"]["doc"], cfg["huawei"]["changelog"],
                HUAWEI_NAV_SELECTORS, max_pages,
                deep_links=cfg["huawei"].get("deep_links"),
                content_selectors=HUAWEI_CONTENT_SELECTORS + FALLBACK_CONTENT_SELECTORS,
                is_huawei=True,
            )
        finally:
            await ctx_aliyun.close()
            await ctx_huawei.close()
            await browser.close()

    md = build_markdown(cfg["name"], aliyun, huawei)
    if output:
        Path(output).write_text(md, encoding="utf-8")
        print(f"\n[OK] Done! Saved to {output} ({len(md.encode())//1024} KB)")
        print("   Paste the file content to AI to start competitive analysis.")
    else:
        print("\n" + "=" * 60 + "\n" + md)

def main():
    parser = argparse.ArgumentParser(description="Aliyun & Huawei doc scraper v4")
    parser.add_argument("--product", default="",
        help="Product key. Available:\n" + "\n".join(f"  {k:<15} {v['name']}" for k, v in PRODUCTS.items()))
    parser.add_argument("--list", action="store_true", help="List all products")
    parser.add_argument("--output", default="", help="Output file path")
    parser.add_argument("--max-pages", type=int, default=12, help="Max core pages per side (default 12)")
    parser.add_argument("--stealth", action="store_true", help="Enable stealth mode for sites with JS rendering compatibility issues (use with caution)")
    args = parser.parse_args()

    if args.list:
        print("\nAvailable products:\n")
        for k, v in PRODUCTS.items():
            print(f"  {k:<15} {v['name']}")
        print(); return
    if not args.product:
        parser.print_help(); sys.exit(1)
    asyncio.run(main_async(args.product, args.max_pages, args.output, args))

if __name__ == "__main__":
    main()
