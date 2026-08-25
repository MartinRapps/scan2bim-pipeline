"""Baut pa_panel_sugar_iteration.png neu: Kacheln aus dem alten Panel,
aber mit sauberen Labels (ohne Dateinamen-Hinweis). Kein Pipeline-Code."""
from PIL import Image, ImageDraw, ImageFont
import os

SRC = r"PA/figures/pa_panel_sugar_iteration.png"
OUT = r"PA/Fertigstellung/figures/pa_panel_sugar_iteration.png"

im = Image.open(SRC).convert("RGB")

# Kachel-Crops (x0,y0,x1,y1) - Unterkante vor der alten Beschriftung
tiles = {
    "brille":   im.crop((29, 68, 652, 376)),
    "flasche":  im.crop((700, 68, 1125, 463)),
    "vergl9k":  im.crop((29, 505, 652, 706)),
    "vergl15k": im.crop((673, 505, 1300, 729)),
    "alurohr":  im.crop((29, 802, 652, 1148)),
}

labels = {
    "brille":   "Historischer Stand: SuGaR-Coarse, Zielzaehler 9001",
    "flasche":  "Historischer Stand: SuGaR-Coarse, Zielzaehler 9001",
    "vergl9k":  "Vergleich 9k- vs. 10k-Iterationen (historisch)",
    "vergl15k": "Coarse-Mesh-Vergleich 10k vs. 15k (historisch)",
    "alurohr":  "Mesh-Stufe nach Coarse-Optimierung mit Zielzaehler 9001",
}

HEADER = "Historische SuGaR-Coarse-Iterationsentwicklung"
CAP_H = 30          # Platz fuer Bildunterschrift
GAP_X = 22
GAP_Y = 34
MARGIN = 29

try:
    font_b = ImageFont.truetype("arialbd.ttf", 26)
except Exception:
    font_b = ImageFont.load_default()
try:
    font_c = ImageFont.truetype("arial.ttf", 17)
except Exception:
    font_c = ImageFont.load_default()

header_h = 52
col_w = max(tiles[k].width for k in ("brille", "vergl9k", "alurohr"))
row1_h = max(tiles["brille"].height, tiles["flasche"].height) + CAP_H
row2_h = max(tiles["vergl9k"].height, tiles["vergl15k"].height) + CAP_H
row3_h = tiles["alurohr"].height + CAP_H

W = MARGIN * 2 + col_w * 2 + GAP_X
H = header_h + row1_h + GAP_Y + row2_h + GAP_Y + row3_h + MARGIN

canvas = Image.new("RGB", (W, H), "white")
draw = ImageDraw.Draw(canvas)
draw.rectangle([0, 0, W, header_h], fill=(28, 42, 66))
draw.text((MARGIN, 12), HEADER, fill="white", font=font_b)

def paste_tile(key, x, y):
    t = tiles[key]
    canvas.paste(t, (x, y))
    draw.text((x, y + t.height + 8), labels[key], fill=(30, 30, 30), font=font_c)

y = header_h
paste_tile("brille", MARGIN, y)
paste_tile("flasche", MARGIN + col_w + GAP_X, y)
y += row1_h + GAP_Y
paste_tile("vergl9k", MARGIN, y)
paste_tile("vergl15k", MARGIN + col_w + GAP_X, y)
y += row2_h + GAP_Y
paste_tile("alurohr", MARGIN, y)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
canvas.save(OUT)
print("geschrieben:", OUT, canvas.size)
