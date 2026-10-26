import re, json, pathlib
L = "https://leck-games.github.io/"
B = {
 "sinerally": dict(title="SineRally", name="SineRally", desc="Sine Rally main game", theme="#ff6a1a", bg="#f7e6b5", orient="landscape", display="fullscreen"),
 "sinerally-engine": dict(title="SR Engine", name="SineRally Engine (test)", desc="Older physics/terrain test build", theme="#4fb3ff", bg="#7cc6f0", orient="landscape", display="fullscreen"),
 "engine-sim": dict(title="SR EngineSim", name="Sine Rally Engine Sim", desc="Engine sound simulator", theme="#38c45a", bg="#f7e6b5", orient="any", display="standalone"),
 "sinerally-physics": dict(title="SR Physics", name="Sine Rally Physics Lab", desc="Tree HP, engine heat, car selector, attachments", theme="#e8453c", bg="#8fd0ff", orient="landscape", display="fullscreen"),
 "sinerally-terrain": dict(title="SR Terrain", name="Sine Rally Terrain", desc="Trees, grassland fire, forest weather", theme="#2f8f4e", bg="#111111", orient="landscape", display="fullscreen"),
}
LINKCSS = "#allBuilds{display:inline-block;text-decoration:none;font:900 12px \"Arial Black\",system-ui,sans-serif;color:#111;background:#fff;border:3px solid #111;border-radius:6px;padding:5px 9px;box-shadow:3px 3px 0 #111;-webkit-tap-highlight-color:transparent}"
CANVCSS = "canvas{touch-action:none;-webkit-touch-callout:none;-webkit-user-select:none;user-select:none}"
for repo, c in B.items():
  p = pathlib.Path("/workspace")/repo/"index.html"; h = p.read_text()
  if "manifest.webmanifest" in h: print("skip", repo); continue
  # drop tags we re-add
  h = re.sub(r'<meta name="(apple-mobile-web-app-capable|mobile-web-app-capable|theme-color)" content="[^"]*">\n?', "", h)
  h = h.replace('<link rel="icon" href="data:,">', "")
  head = (f'<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">\n'
          f'<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"><meta name="apple-mobile-web-app-title" content="{c["title"]}">\n'
          f'<meta name="theme-color" content="{c["theme"]}"><meta name="format-detection" content="telephone=no">\n'
          f'<link rel="manifest" href="manifest.webmanifest"><link rel="apple-touch-icon" href="icons/apple-touch-icon.png">\n'
          + ('' if repo == "sinerally" else '<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">\n')
          + f'<style>/* iOS home-screen */{CANVCSS}{LINKCSS}</style>\n')
  h = h.replace("</head>", head + "</head>", 1)
  h = re.sub(r"\n\n+", "\n", h)
  p.write_text(h)
  m = {"name": c["name"], "short_name": c["title"], "description": c["desc"], "id": "./", "start_url": "./", "scope": "./",
       "display": c["display"], "display_override": [c["display"], "standalone"], "orientation": c["orient"],
       "background_color": c["bg"], "theme_color": c["theme"],
       "icons": [{"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
                 {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
                 {"src": "icons/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}]}
  (p.parent/"manifest.webmanifest").write_text(json.dumps(m, indent=1) + "\n")
  print("patched", repo)
