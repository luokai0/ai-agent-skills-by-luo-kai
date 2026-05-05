#!/usr/bin/env python3
import argparse
import json
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://www.htmlcode.fun"


def request_json(url: str, method: str = "GET", payload: dict | None = None):
    data = None
    headers = {"User-Agent": "OpenClaw easy-html-deploy", "Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {"success": False, "error": body}
        return e.code, parsed


def deploy(args):
    path = pathlib.Path(args.file)
    html = path.read_text(encoding="utf-8")
    payload = {
        "filename": args.filename or path.name,
        "content": html,
    }
    if args.title:
        payload["title"] = args.title
    if args.code:
        payload["enableCustomCode"] = True
        payload["customCode"] = args.code
    status, data = request_json(f"{BASE}/api/deploy", method="POST", payload=payload)
    print(json.dumps({"httpStatus": status, **data}, ensure_ascii=False, indent=2))
    return 0 if 200 <= status < 300 and data.get("success") else 1


def update(args):
    path = pathlib.Path(args.file)
    html = path.read_text(encoding="utf-8")
    payload = {
        "code": args.code,
        "content": html,
        "filename": args.filename or path.name,
    }
    if args.title:
        payload["title"] = args.title
    status, data = request_json(f"{BASE}/api/deploy/content", method="PATCH", payload=payload)
    print(json.dumps({"httpStatus": status, **data}, ensure_ascii=False, indent=2))
    return 0 if 200 <= status < 300 and data.get("success", True) else 1


def get_content(args):
    query = urllib.parse.urlencode({"code": args.code, **({"download": 1} if args.download else {})})
    url = f"{BASE}/api/deploy/content?{query}"
    req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw easy-html-deploy"})
    with urllib.request.urlopen(req) as resp:
        body = resp.read()
    if args.output:
        pathlib.Path(args.output).write_bytes(body)
    else:
        try:
            sys.stdout.write(body.decode("utf-8"))
        except UnicodeDecodeError:
            sys.stdout.buffer.write(body)
    return 0


def main():
    parser = argparse.ArgumentParser(description="Deploy or update single-file HTML pages on htmlcode.fun")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_deploy = sub.add_parser("deploy", help="Deploy a new HTML page")
    p_deploy.add_argument("file", help="Path to an HTML file")
    p_deploy.add_argument("--title", help="Optional title metadata")
    p_deploy.add_argument("--filename", help="Filename sent to the API")
    p_deploy.add_argument("--code", help="Stable custom short code")
    p_deploy.set_defaults(func=deploy)

    p_update = sub.add_parser("update", help="Update an existing deployed code")
    p_update.add_argument("code", help="Existing deployed short code")
    p_update.add_argument("file", help="Path to an HTML file")
    p_update.add_argument("--title", help="Optional title metadata")
    p_update.add_argument("--filename", help="Filename sent to the API")
    p_update.set_defaults(func=update)

    p_get = sub.add_parser("get", help="Fetch deployed content by code")
    p_get.add_argument("code", help="Existing deployed short code")
    p_get.add_argument("--download", action="store_true", help="Request download mode")
    p_get.add_argument("--output", help="Write response to a file")
    p_get.set_defaults(func=get_content)

    args = parser.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
