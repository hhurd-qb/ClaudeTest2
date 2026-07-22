#!/usr/bin/env python3
"""
Sync accepted IAS skills from Confluence into the ClaudeSkillsTest plugin
marketplace structure.

Pulls only DEPTH-1 descendants of the two "Accepted" root pages:
  - Accepted (Team)       -> plugins/<slug>/  (tier: team)
  - Accepted (Enterprise) -> plugins/<slug>/  (tier: enterprise)

Depth-2+ pages (audit-summary companion pages) are deliberately skipped —
they are children of the skill page, not of the Accepted root, so filtering
on depth == 1 excludes them automatically.

For each skill page, this also pulls any Confluence ATTACHMENTS on that
specific page and writes them into skills/<slug>/references/<filename>,
so supporting files survive the sync alongside the main SKILL.md — not
just the page body text.

Requires env vars:
  CONFLUENCE_EMAIL       - Atlassian account email (e.g. hhurd@quickbase.com)
  CONFLUENCE_API_TOKEN   - Atlassian API token
  CONFLUENCE_SITE        - e.g. quickbase.atlassian.net
  CLOUD_ID               - 20d966ed-3d3f-4c0c-b14b-c1dbb9bb6aa7

Writes into REPO_ROOT (default: current directory):
  .claude-plugin/marketplace.json
  plugins/<slug>/.claude-plugin/plugin.json
  plugins/<slug>/skills/<slug>/SKILL.md
  plugins/<slug>/skills/<slug>/references/<attachment filename>   (if any)
"""

import json
import os
import re
import sys
from pathlib import Path

import requests
from markdownify import markdownify as md

# --- Config -----------------------------------------------------------------

ACCEPTED_ROOTS = {
    "team": "6429769806",        # Accepted (Team)
    "enterprise": "6429147235",  # Accepted (Enterprise)
}

REPO_ROOT = Path(os.environ.get("REPO_ROOT", "."))
MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"
PLUGINS_DIR = REPO_ROOT / "plugins"

CONFLUENCE_EMAIL = os.environ["CONFLUENCE_EMAIL"]
CONFLUENCE_API_TOKEN = os.environ["CONFLUENCE_API_TOKEN"]
CONFLUENCE_SITE = os.environ["CONFLUENCE_SITE"]
CLOUD_ID = os.environ["CLOUD_ID"]

WIKI_BASE = f"https://{CONFLUENCE_SITE}/wiki"
BASE_URL = f"{WIKI_BASE}/api/v2"
AUTH = (CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN)
HEADERS = {"Accept": "application/json"}


# --- Helpers ------------------------------------------------------------------

def slugify(title: str) -> str:
    """
    'quickbase-context — Team 2026-07-16'  -> 'quickbase-context'
    'confluence-submit — Enterprise 2026-07-10' -> 'confluence-submit'
    'Quickbase Info' -> 'quickbase-info'
    'Skill Example Test' -> 'skill-example-test'
    """
    base = re.split(r"\s+—\s+(Team|Enterprise)\s+\d{4}-\d{2}-\d{2}$", title)[0]
    base = base.strip().lower()
    base = re.sub(r"[^a-z0-9]+", "-", base)
    return base.strip("-")


def get_descendants(page_id: str) -> list[dict]:
    results, cursor = [], None
    while True:
        params = {"limit": 50}
        if cursor:
            params["cursor"] = cursor
        resp = requests.get(
            f"{BASE_URL}/pages/{page_id}/descendants",
            params=params, auth=AUTH, headers=HEADERS, timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        results.extend(data.get("results", []))
        next_link = data.get("_links", {}).get("next")
        if not next_link:
            break
        cursor = next_link.split("cursor=")[-1]
    return results


def get_page_body_markdown(page_id: str) -> str:
    resp = requests.get(
        f"{BASE_URL}/pages/{page_id}",
        params={"body-format": "storage"},
        auth=AUTH, headers=HEADERS, timeout=30,
    )
    resp.raise_for_status()
    storage_html = resp.json()["body"]["storage"]["value"]
    return md(storage_html, heading_style="ATX").strip()


def get_page_attachments(page_id: str) -> list[dict]:
    """Returns [{'title': filename, 'download_url': full url, 'media_type': str}, ...]"""
    attachments = []
    cursor = None
    while True:
        params = {"limit": 50}
        if cursor:
            params["cursor"] = cursor
        resp = requests.get(
            f"{BASE_URL}/pages/{page_id}/attachments",
            params=params, auth=AUTH, headers=HEADERS, timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        for item in data.get("results", []):
            download_path = item.get("_links", {}).get("download")
            if not download_path:
                continue
            attachments.append({
                "title": item["title"],
                "download_url": f"{WIKI_BASE}{download_path}",
                "media_type": item.get("mediaType", ""),
            })
        next_link = data.get("_links", {}).get("next")
        if not next_link:
            break
        cursor = next_link.split("cursor=")[-1]
    return attachments


def download_attachment(download_url: str) -> bytes:
    resp = requests.get(download_url, auth=AUTH, timeout=60)
    resp.raise_for_status()
    return resp.content


def load_marketplace() -> dict:
    if MARKETPLACE_JSON.exists():
        return json.loads(MARKETPLACE_JSON.read_text())
    return {
        "$schema": "https://json.schemastore.org/claude-code-marketplace.json",
        "name": "quickbase-ias",
        "owner": {"name": "Henry Hurd", "email": "hhurd@quickbase.com"},
        "version": "1.0.0",
        "description": "Quickbase Internal AI Skills (IAS), synced from the IAS Confluence space",
        "plugins": [],
    }


def bump_version(version: str) -> str:
    parts = version.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    return ".".join(parts)


def write_if_changed(path: Path, content: bytes) -> bool:
    """Writes content to path; returns True if the file was new or different."""
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_bytes() if path.exists() else None
    changed = existing != content
    if changed:
        path.write_bytes(content)
    return changed


# --- Main sync ----------------------------------------------------------------

def main() -> None:
    marketplace = load_marketplace()
    plugins_by_name = {p["name"]: p for p in marketplace["plugins"]}
    changed = False

    for tier, root_id in ACCEPTED_ROOTS.items():
        for page in get_descendants(root_id):
            if page.get("depth") != 1:
                continue  # skip audit-summary children (depth 2+)
            if page.get("type") != "page":
                continue

            title = page["title"]
            slug = slugify(title)
            page_id = page["id"]

            print(f"[{tier}] {title} -> plugins/{slug}")

            body_md = get_page_body_markdown(page_id)
            skill_dir = PLUGINS_DIR / slug / "skills" / slug
            plugin_manifest_dir = PLUGINS_DIR / slug / ".claude-plugin"

            # --- SKILL.md ---
            skill_changed = write_if_changed(
                skill_dir / "SKILL.md", (body_md + "\n").encode("utf-8")
            )

            # --- reference files (any attachments on this specific page) ---
            refs_changed = False
            attachments = get_page_attachments(page_id)
            for att in attachments:
                print(f"    + reference file: {att['title']}")
                content = download_attachment(att["download_url"])
                ref_path = skill_dir / "references" / att["title"]
                if write_if_changed(ref_path, content):
                    refs_changed = True

            content_changed = skill_changed or refs_changed

            # --- plugin.json ---
            plugin_json_path = plugin_manifest_dir / "plugin.json"
            plugin_manifest_dir.mkdir(parents=True, exist_ok=True)
            if plugin_json_path.exists():
                plugin_manifest = json.loads(plugin_json_path.read_text())
            else:
                plugin_manifest = {
                    "name": slug,
                    "version": "1.0.0",
                    "description": f"IAS skill: {slug} ({tier})",
                    "author": {"name": "Henry Hurd", "email": "hhurd@quickbase.com"},
                }

            if content_changed:
                plugin_manifest["version"] = bump_version(
                    plugin_manifest.get("version", "1.0.0")
                )
                changed = True

            plugin_json_path.write_text(json.dumps(plugin_manifest, indent=2) + "\n")

            plugins_by_name[slug] = {
                "name": slug,
                "description": plugin_manifest["description"],
                "source": f"./plugins/{slug}",
                "category": "productivity",
            }

    marketplace["plugins"] = list(plugins_by_name.values())
    MARKETPLACE_JSON.parent.mkdir(parents=True, exist_ok=True)
    MARKETPLACE_JSON.write_text(json.dumps(marketplace, indent=2) + "\n")

    gh_output = os.environ.get("GITHUB_OUTPUT")
    if gh_output:
        with open(gh_output, "a") as f:
            f.write(f"changed={'true' if changed else 'false'}\n")

    print("Sync complete." + (" Changes detected." if changed else " No changes."))


if __name__ == "__main__":
    sys.exit(main())
