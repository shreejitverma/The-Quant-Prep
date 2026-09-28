# Obsidian setup

The repo is an Obsidian vault. Settings are committed; plugin code is not.

```sh
python3 tools/obsidian/bootstrap.py          # install the 23 pinned plugins into .obsidian/plugins/
python3 tools/obsidian/bootstrap.py --check  # show plugins that are missing or out of date
```

- `plugins.lock.json` pins each community plugin to a release tag and the sha256 of each release asset; the bootstrap refuses any file whose hash differs.
- To upgrade a plugin, change its `version`, `tag` and hashes in the lock together (hash the GitHub release assets, not an installed copy, because Obsidian rewrites installed `main.js`).
- Committed settings: `app.json` (relative Markdown links, matching the repo's link convention; `_archive/` excluded from search), `community-plugins.json`, and `plugins/obsidian-git/data.json`.
- obsidian-git never commits or pushes automatically here (`autoSaveInterval: 0`, `autoPushInterval: 0`, `disablePush: true`): changes reach GitHub only through the `no-mistakes` gate.
- Per-machine state (`workspace*.json`, caches, plugin bundles) is gitignored.
