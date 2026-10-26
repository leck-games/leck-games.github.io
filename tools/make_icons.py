#!/usr/bin/env python3
"""Comic-style home-screen icons for the Sine Rally builds.
usage: make_icons.py <key> <outdir>   -> apple-touch-icon.png (180), icon-192.png, icon-512.png, favicon-32.png
"""
import sys, math, os
from PIL import Image, ImageDraw, ImageFont
FONT = "/usr/share/fonts/truetype/sand-box/google/Bangers/Bangers-Regular.ttf"
STYLES = {  # key: (bg, ray, label, sub, sub_bg)
  "launcher":  ("#ffd23f", "#ffb627", "SR", "ALL BUILDS", "#111111"),
  "sinerally": ("#ff6a1a", "#ff8a3d", "SR", "RALLY", "#111111"),
  "engine":    ("#4fb3ff", "#7cc6f0", "ENG", "TEST", "#111111"),
  "enginesim": ("#38c45a", "#62d67e", "VRM", "SOUND", "#111111"),
  "physics":   ("#e8453c", "#f06a5f", "PHY", "LAB", "#111111"),
  "terrain":   ("#2f8f4e", "#45a862", "TER", "FIRE", "#111111"),
}
def make(key, out):
  bg, ray, label, sub, sub_bg = STYLES[key]
  S = 1024; im = Image.new("RGB", (S, S), bg); d = ImageDraw.Draw(im)
  cx, cy = S/2, S*0.42
  for i in range(0, 24, 2):  # sunburst
    a0, a1 = 2*math.pi*i/24, 2*math.pi*(i+1)/24
    d.polygon([(cx, cy), (cx+2*S*math.cos(a0), cy+2*S*math.sin(a0)), (cx+2*S*math.cos(a1), cy+2*S*math.sin(a1))], fill=ray)
  # halftone dots bottom-right
  for y in range(0, S, 40):
    for x in range(0, S, 40):
      r = max(0, (x+y-S)/S*12)
      if r > 1: d.ellipse([x-r, y-r, x+r, y+r], fill="#00000030" if False else _darken(bg))
  # sine wave stripe
  pts = [(x, S*0.70 + S*0.07*math.sin(x/S*2*math.pi*1.5)) for x in range(-20, S+21, 8)]
  d.line(pts, fill="#111111", width=70, joint="curve"); d.line(pts, fill="#ffffff", width=38, joint="curve")
  # label
  f = ImageFont.truetype(FONT, 470 if len(label) <= 2 else 360)
  tw = d.textlength(label, font=f); tx = (S-tw)/2; ty = S*0.40
  d.text((tx+22, ty+26), label, font=f, fill="#111111", anchor="lm", stroke_width=26, stroke_fill="#111111")
  d.text((tx, ty), label, font=f, fill="#ffffff", anchor="lm", stroke_width=26, stroke_fill="#111111")
  # sub banner
  fs = ImageFont.truetype(FONT, 150 if len(sub) <= 6 else 120)
  sw = d.textlength(sub, font=fs) + 90; bx0 = (S-sw)/2; by0 = S*0.80
  d.rectangle([bx0, by0, bx0+sw, by0+170], fill=sub_bg)
  d.text((S/2, by0+88), sub, font=fs, fill="#ffffff", anchor="mm")
  # ink frame
  d.rectangle([0, 0, S-1, S-1], outline="#111111", width=36)
  os.makedirs(out, exist_ok=True)
  for n, sz in (("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512), ("favicon-32.png", 32)):
    im.resize((sz, sz), Image.LANCZOS).save(os.path.join(out, n), optimize=True)
def _darken(h):
  h = h.lstrip("#"); r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4)); return (int(r*.8), int(g*.8), int(b*.8))
if __name__ == "__main__":
  make(sys.argv[1], sys.argv[2])
