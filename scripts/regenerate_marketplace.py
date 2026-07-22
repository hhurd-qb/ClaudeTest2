#!/usr/bin/env python3
"""
Rebuilds .claude-plugin/marketplace.json by scanning the plugins/ folder
directly — no Confluence involved. Every subfolder of plugins/ that has
a valid .claude-plugin/plugin.json becomes one entry in the catalog.

This means: however a new skill folder ends up under plugins/ (manually
added in GitHub, dragged in, synced from Confluence, whatever) — the next
run of this script picks it up automatically, because it looks at what's
actually sitting in the repo, not at any external source of truth.

Usage:
  python scripts/regenerate_marketplace.py

Writes:
  .claude-plugin/marketplace.json
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(".")
MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"
PLUGINS_DIR = REPO_ROOT / "plugins"

MARKETPLACE_DEFAULTS = {
    "$schema": "https://json.schemastore.org/claude-code-marketplace.json",
    "name": "quickbase-ias",
    "owner": {"name": "Henry Hurd", "email": "hhurd@quickbase.com"},
    "version": "1.0.0",
    "description": "Quickbase Internal AI Skills (IAS) marketplace",
}


def load_existing_marketplace() -> dict:
    if MARKETPLACE_JSON.exists():
        data = json.loads(MARKETPLACE_JSON.read_text())
        # Keep existing top-level metadata (name/owner/description/etc.),
        # only the "plugins" list gets fully rebuilt below.
        return data
    return dict(MARKETPLACE_DEFAULTS, plugins=[])


def discover_plugins() -> list[dict]:
    entries = []
    if not PLUGINS_DIR.exists():
        print(f"WARNING: {PLUGINS_DIR} does not exist — no plugins found.")
        return entries

    for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
        if not plugin_dir.is_dir():
            continue

        plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"
        if not plugin_json_path.exists():
            print(f"  SKIP {plugin_dir.name}: no .claude-plugin/plugin.json found")
            continue

        try:
            plugin_manifest = json.loads(plugin_json_path.read_text())
        except json.JSONDecodeError as e:
            print(f"  SKIP {plugin_dir.name}: invalid JSON in plugin.json ({e})")
            continue

        name = plugin_manifest.get("name", plugin_dir.name)
        description = plugin_manifest.get("description", "")

        print(f"  FOUND {name} -> ./plugins/{plugin_dir.name}")
        entries.append({
            "name": name,
            "description": description,
            "source": f"./plugins/{plugin_dir.name}",
            "category": "productivity",
        })

    return entries


def main() -> None:
    print(f"Scanning {PLUGINS_DIR}/ ...")
    marketplace = load_existing_marketplace()
    plugin_entries = discover_plugins()

    before = marketplace.get("plugins", [])
    marketplace["plugins"] = plugin_entries

    MARKETPLACE_JSON.parent.mkdir(parents=True, exist_ok=True)
    new_text = json.dumps(marketplace, indent=2) + "\n"
    old_text = MARKETPLACE_JSON.read_text() if MARKETPLACE_JSON.exists() else None

    MARKETPLACE_JSON.write_text(new_text)

    if old_text == new_text:
        print(f"No change: {len(plugin_entries)} plugin(s), same as before.")
    else:
        print(f"Updated marketplace.json: {len(before)} -> {len(plugin_entries)} plugin(s).")


if __name__ == "__main__":
    sys.exit(main())
