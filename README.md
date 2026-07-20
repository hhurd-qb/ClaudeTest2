# ClaudeSkillsTest — Quickbase IAS Marketplace (2 plugins)

## Structure

```
.claude-plugin/marketplace.json         <- catalog: lists both plugins below
plugins/
  quickbase-context/
    .claude-plugin/plugin.json          <- manifest
    skills/quickbase-context/SKILL.md   <- real, current skill content
  quickbase-lore/
    .claude-plugin/plugin.json          <- manifest
    skills/quickbase-lore/
      SKILL.md                          <- real, current skill content
      references/lore.md                <- supporting reference file the skill reads
```

Both SKILL.md files (and the lore reference file) are copied verbatim from
the live IAS skill library — nothing here is a placeholder.

## IMPORTANT: how to actually get this into GitHub without losing files

This repo relies on **hidden dotfolders** (`.claude-plugin`). GitHub's web
"Add file > Upload files" button, and dragging a folder out of macOS Finder,
can silently drop dotfolders — this has caused the exact "no plugins showing"
problem already. To avoid that:

**Do NOT use the GitHub web upload button for this zip.** Instead:

1. Unzip this file locally (double-click, or `unzip ClaudeSkillsTest.zip`).
2. Open Terminal:
   ```bash
   cd path/to/ClaudeSkillsTest        # the unzipped folder
   git init                            # if this is a fresh repo, or:
   git remote add origin https://github.com/hhurd-qb/ClaudeSkillsTest.git
   git add -A
   git status                          # confirm .claude-plugin/marketplace.json
                                        # and both plugin.json files show up here
   git commit -m "Add quickbase-context and quickbase-lore plugins"
   git push -u origin main
   ```
   If you already have this repo cloned, just delete its old contents first
   (except `.git`), copy this unzipped folder's contents in, then run the
   `git add -A` / `commit` / `push` steps above.
3. `git status` before committing is the safety check — if you don't see
   `.claude-plugin/marketplace.json` and both `plugins/*/.claude-plugin/plugin.json`
   listed, they didn't make it in and won't sync.

## After pushing

- **Personal test**: Directory > Plugins > Personal > "+" > Add marketplace from GitHub > paste repo URL
- **Org-wide**: Directory > Plugins > Your organization > "+" (Owner/admin only),
  repo must be private, Claude GitHub App installed with Webhooks (Read & Write)

## Updating later

Edit a SKILL.md, bump that plugin's `version` in its `plugin.json`, open a
PR, merge to main — that merge (with the version bump) is what triggers
auto-sync if you've enabled it. A direct push without a version bump won't.
