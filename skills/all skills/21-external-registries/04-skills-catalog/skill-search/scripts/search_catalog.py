#!/usr/bin/env python3
"""
Agent Skills Catalog Search

Search the skillscatalog.ai catalog for skills.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path for shared imports
SCRIPT_DIR = Path(__file__).parent
SKILLS_DIR = SCRIPT_DIR.parent.parent
SHARED_DIR = SKILLS_DIR / "_shared"
sys.path.insert(0, str(SHARED_DIR))

try:
    from agentskills_config import get_skill_key, get_api_url, get_auth_header
except ImportError:
    print("Error: Could not import agentskills_config.")
    print("Make sure the _shared/agentskills_config.py module exists.")
    sys.exit(1)

# Optional: import requests
try:
    import requests
except ImportError:
    requests = None  # type: ignore


# ============================================================================
# API Functions
# ============================================================================

def search_catalog(query: str, limit: int = 20) -> dict:
    """Search the catalog for skills."""
    if requests is None:
        return {
            "error": "requests library not installed. Run: pip install requests",
            "results": [],
        }

    api_url = get_api_url()
    headers = get_auth_header()

    try:
        response = requests.get(
            f"{api_url}/api/catalog/search",
            headers=headers,
            params={"q": query},
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])[:limit]
            return {"results": results, "query": query, "count": len(results)}
        else:
            try:
                error_data = response.json()
                return {"error": error_data.get("error", f"HTTP {response.status_code}"), "results": []}
            except json.JSONDecodeError:
                return {"error": f"HTTP {response.status_code}", "results": []}

    except requests.exceptions.Timeout:
        return {"error": "Request timed out", "results": []}
    except requests.exceptions.ConnectionError:
        return {"error": f"Could not connect to {api_url}", "results": []}
    except Exception as e:
        return {"error": str(e), "results": []}


def get_skill(vendor_key: str, skill_key: str) -> dict:
    """Get details for a specific skill."""
    if requests is None:
        return {"error": "requests library not installed. Run: pip install requests"}

    api_url = get_api_url()
    headers = get_auth_header()

    try:
        response = requests.get(
            f"{api_url}/api/catalog/{vendor_key}/{skill_key}",
            headers=headers,
            timeout=30,
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": f"Skill not found: {vendor_key}/{skill_key}"}
        else:
            try:
                error_data = response.json()
                return {"error": error_data.get("error", f"HTTP {response.status_code}")}
            except json.JSONDecodeError:
                return {"error": f"HTTP {response.status_code}"}

    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.ConnectionError:
        return {"error": f"Could not connect to {api_url}"}
    except Exception as e:
        return {"error": str(e)}


def list_vendor_skills(vendor_key: str) -> dict:
    """List all skills from a vendor."""
    # For now, use search with vendor name
    return search_catalog(vendor_key, limit=50)


# ============================================================================
# Output Formatting
# ============================================================================

def format_search_results(data: dict, json_output: bool = False) -> str:
    """Format search results for display."""
    if json_output:
        return json.dumps(data, indent=2)

    if "error" in data:
        return f"Error: {data['error']}"

    results = data.get("results", [])
    query = data.get("query", "")

    if not results:
        return f"No skills found matching \"{query}\""

    lines = [f"Found {len(results)} skills matching \"{query}\":", ""]

    for i, result in enumerate(results, 1):
        vendor_key = result.get("vendorKey", "unknown")
        skill_key = result.get("skillKey", "unknown")
        skill_name = result.get("skillName", skill_key)
        description = result.get("description", "No description")
        vendor_name = result.get("vendorName", vendor_key)

        # Truncate description
        if len(description) > 60:
            description = description[:57] + "..."

        lines.append(f"{i}. {vendor_key}/{skill_key}")
        lines.append(f"   {description}")
        lines.append(f"   Vendor: {vendor_name}")
        lines.append("")

    return "\n".join(lines)


def format_skill_details(data: dict, json_output: bool = False) -> str:
    """Format skill details for display."""
    if json_output:
        return json.dumps(data, indent=2)

    if "error" in data:
        return f"Error: {data['error']}"

    vendor_key = data.get("vendorKey", "unknown")
    skill_key = data.get("skillKey", "unknown")
    certified = data.get("certified", False)
    skill = data.get("skill", {})
    cert = data.get("certification", {})

    lines = [
        f"{vendor_key}/{skill_key}",
        f"  Title: {skill.get('title', skill_key)}",
        f"  Description: {skill.get('desc', 'No description')}",
        f"  Vendor: {skill.get('vendor', vendor_key)}",
    ]

    if certified and cert:
        lines.append(f"  Version: {cert.get('version', 'unknown')}")
        lines.append(f"  Safety Score: {cert.get('safetyScore', 'N/A')}")
        lines.append(f"  Certified: Yes")
    else:
        lines.append(f"  Certified: No")

    if skill.get("repo"):
        lines.append(f"  Repository: {skill.get('repo')}")

    if skill.get("license"):
        lines.append(f"  License: {skill.get('license')}")

    return "\n".join(lines)


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Search the Agent Skills Catalog",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python search_catalog.py "pdf tools"
  python search_catalog.py "pdf tools" --limit 5
  python search_catalog.py --get anthropic/document-skills
  python search_catalog.py --vendor anthropic
  python search_catalog.py "excel" --json
        """,
    )
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--limit", type=int, default=10, help="Maximum results (default: 10)")
    parser.add_argument("--get", metavar="VENDOR/SKILL", help="Get skill details")
    parser.add_argument("--vendor", help="List skills by vendor")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    # Handle different modes
    if args.get:
        # Get skill details
        parts = args.get.split("/", 1)
        if len(parts) != 2:
            print("Error: Use format vendor/skill (e.g., anthropic/document-skills)", file=sys.stderr)
            sys.exit(1)

        vendor_key, skill_key = parts
        result = get_skill(vendor_key, skill_key)
        print(format_skill_details(result, json_output=args.json))
        sys.exit(0 if "error" not in result else 1)

    elif args.vendor:
        # List vendor skills
        result = list_vendor_skills(args.vendor)
        print(format_search_results(result, json_output=args.json))
        sys.exit(0 if "error" not in result else 1)

    elif args.query:
        # Search
        result = search_catalog(args.query, limit=args.limit)
        print(format_search_results(result, json_output=args.json))
        sys.exit(0 if "error" not in result else 1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
