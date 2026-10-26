# leck-games.github.io — Sine Rally launcher

https://leck-games.github.io/ — one page linking every Sine Rally build. iPhone: Safari → Share → Add to Home Screen.

- `index.html` – launcher (cards rendered from the baked JSON in `<script id="builds">`; commit info refreshed at runtime from the GitHub API, falls back to baked values)
- `sw.js` – launcher-only service worker (network-first, versioned cache `launcher-vN`; ignores every path outside the launcher, so game builds are never cached)
- `tools/builds.py` – card list · `tools/bake.py` – thumbnails + commit hash/date · `tools/make_icons.py` – comic icons (Pillow) · `tools/patch_builds.py` – one-off iOS head patch used on the build repos · `tools/test.cjs` – headless iPhone 12 check
- Fonts: Bangers (SIL OFL 1.1), subset to woff2.

Update: `python3 tools/bake.py && git commit -am bake && git push` (bump `VERSION` in sw.js when changing cached files).
