#!/usr/bin/env python3
"""Bake launcher data: thumbnails (JPEG <80 KB) + last-commit info into index.html.
run from repo root: python3 tools/bake.py   (needs gh CLI; falls back to local git)"""
import json, subprocess, re, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__)); from builds import BUILDS
WS = "/workspace"
def commit(b):
  try:
    j = json.loads(subprocess.check_output(["gh", "api", f"repos/leck-games/{b['repo']}/commits/main"], text=True))
    return j["sha"][:7], j["commit"]["committer"]["date"]
  except Exception:
    out = subprocess.check_output(["git", "-C", f"{WS}/{b['dir']}", "log", "-1", "--format=%h %cI"], text=True).split()
    return out[0], out[1]
data = []
for b in BUILDS:
  im = Image.open(f"{WS}/{b['dir']}/{b['shot']}").convert("RGB")
  w, h = im.size; tw = min(w, int(h*16/9)); th = int(tw*9/16); l = (w-tw)//2; t = (h-th)//2
  im = im.crop((l, t, l+tw, t+th)).resize((640, 360), Image.LANCZOS)
  q = 80; path = f"thumbs/{b['id']}.jpg"
  while True:
    im.save(path, "JPEG", quality=q, optimize=True, progressive=True)
    if os.path.getsize(path) < 80_000 or q <= 40: break
    q -= 5
  sha, date = commit(b)
  data.append(dict(id=b["id"], repo=b["repo"], url=b["url"], title=b["title"], tag=b["tag"], desc=b["desc"], color=b["color"],
                   thumb=path, sha=sha, date=date))
  print(b["id"], sha, date, os.path.getsize(path), "bytes q", q)
html = open("index.html").read()
html = re.sub(r'(<script id="builds" type="application/json">).*?(</script>)', lambda m: m.group(1) + json.dumps(data, separators=(",", ":")) + m.group(2), html, flags=re.S)
open("index.html", "w").write(html)
