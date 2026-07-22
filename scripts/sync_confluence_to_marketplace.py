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

AUDIT_SUMMARY_PATTERN = re.compile(r"—\s*Audit Summary", re.IGNORECASE)


def get_direct_children(page_id: str, all_descendants: list[dict]) -> list[dict]:
    """Direct children of a given page, pulled from an already-fetched
    descendants list (avoids a second API round trip per skill)."""
    return [d for d in all_descendants if d.get("parentId") == page_id]


def slugify_reference_title(title: str) -> str:
    slug = title.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-") + ".md"


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


def _yaml_quote(value: str) -> str:
    """Produce a safe double-quoted YAML scalar from arbitrary text —
    escapes backslashes and double quotes, and collapses any embedded
    newlines/extra whitespace into single spaces. A quoted single-line
    scalar can't be broken by Confluence collapsing line breaks, because
    there are no line breaks left in it to collapse."""
    collapsed = re.sub(r"\s+", " ", value).strip()
    escaped = collapsed.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def sanitize_frontmatter(body_md: str) -> str:
    """
    Confluence's markdown import/export round-trip has been observed to
    mangle SKILL.md frontmatter in more than one way — turning 'name:'
    into a heading, dropping the closing '---' delimiter entirely, and
    (the newest failure mode) collapsing the <br/> line breaks between
    'name:' and 'description:' into a single space, merging both onto
    one physical line. That last case produces YAML errors like:

        mapping values are not allowed in this context at line 1 column 39

    Rather than pattern-matching each new corruption shape as it turns
    up, this extracts the actual 'name' and 'description' VALUES
    directly via regex — wherever they are, however they're joined to
    surrounding text — and rebuilds a clean, guaranteed-valid frontmatter
    block from scratch. The description is written as a quoted
    single-line scalar (not a multi-line ">" folded block), since a
    quoted single-line string has no internal line breaks for Confluence
    to collapse in the first place — this sidesteps the whole class of
    bug rather than repairing it after the fact.
    """
    # Work over the whole text as one string (not line-by-line) so this
    # catches name/description regardless of whether they're on separate
    # lines, merged onto one line, or prefixed with stray heading markers.
    name_match = re.search(
        r"name\s*:\s*(.+?)(?=\s+description\s*:|\n|$)", body_md, re.IGNORECASE
    )
    if name_match is None:
        return body_md  # no frontmatter-like content found; leave untouched

    name_value = name_match.group(1).strip().strip("\"'")

    # Description: capture everything after 'description:' up to the
    # first heading line (the real start of the document body). Handles
    # a YAML '>' marker right after the colon if present.
    desc_search_start = name_match.end()
    desc_match = re.search(
        r"description\s*:\s*>?\s*(.+?)(?=\n\s*#{1,6}\s|\Z)",
        body_md[desc_search_start:],
        re.IGNORECASE | re.DOTALL,
    )
    if desc_match is None:
        return body_md  # couldn't confidently find a description; leave untouched

    description_value = desc_match.group(1)
    # Strip any stray heading markers or dash-delimiters that got mixed
    # into the captured span (e.g. a leftover '---' from a partially
    # intact closing delimiter).
    description_value = re.sub(r"^\s*#+\s*", "", description_value, flags=re.MULTILINE)
    description_value = re.sub(r"^\s*-{3,}\s*$", "", description_value, flags=re.MULTILINE)

    # Everything from the end of the matched description span onward is
    # the real document body.
    body_start = desc_search_start + desc_match.end()
    rest_block = body_md[body_start:].lstrip("\n")
    # Drop a leftover bare '---' line if the original closing delimiter
    # partially survived and got left dangling at the top of the body.
    rest_block = re.sub(r"^\s*-{3,}\s*\n+", "", rest_block)

    frontmatter_block = (
        f"name: {name_value}\n"
        f"description: {_yaml_quote(description_value)}"
    )
    return f"---\n{frontmatter_block}\n---\n\n{rest_block}\n"


def get_page_body_markdown(page_id: str) -> str:
    resp = requests.get(
        f"{BASE_URL}/pages/{page_id}",
        params={"body-format": "storage"},
        auth=AUTH, headers=HEADERS, timeout=30,
    )
    resp.raise_for_status()
    storage_html = resp.json()["body"]["storage"]["value"]
    raw_md = md(storage_html, heading_style="ATX").strip()
    return sanitize_frontmatter(raw_md)


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
        all_descendants = get_descendants(root_id)  # full tree, all depths

        for page in all_descendants:
            if page.get("depth") != 1:
                continue  # only depth-1 pages are skill pages
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

            content_changed = skill_changed
            found_reference_source = False

            # --- reference files: this skill page's own CHILD PAGES ---
            # (the audit-summary companion page is a child too, at the same
            #  depth — exclude it by title pattern, not by depth, since both
            #  live one level below the skill page)
            child_pages = get_direct_children(page_id, all_descendants)
            for child in child_pages:
                if child.get("type") != "page":
                    continue
                if AUDIT_SUMMARY_PATTERN.search(child["title"]):
                    continue  # this is the audit-summary companion, not a reference
                found_reference_source = True
                print(f"    + reference page: {child['title']}")
                ref_body_md = get_page_body_markdown(child["id"])
                ref_filename = slugify_reference_title(child["title"])
                ref_path = skill_dir / "references" / ref_filename
                if write_if_changed(ref_path, (ref_body_md + "\n").encode("utf-8")):
                    content_changed = True

            # --- reference files: any Confluence ATTACHMENTS on the skill page ---
            # (kept as a second, independent source — some skills may attach
            #  files directly instead of using child pages)
            attachments = get_page_attachments(page_id)
            for att in attachments:
                found_reference_source = True
                print(f"    + reference attachment: {att['title']}")
                content = download_attachment(att["download_url"])
                ref_path = skill_dir / "references" / att["title"]
                if write_if_changed(ref_path, content):
                    content_changed = True

            if not found_reference_source:
                print("    (no reference pages or attachments found)")

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
