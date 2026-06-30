"""Crop the NEW 3x3 illustration grid (text-free, 3D style) into individual cards."""
from PIL import Image
import os

src = "/home/z/my-project/upload/ChatGPT Image Jun 30, 2026, 08_31_34 PM.png"
out_dir = "/home/z/my-project/public/images"
os.makedirs(out_dir, exist_ok=True)

# First, remove old card-*.png, illust-*.png and features-grid.png
for f in os.listdir(out_dir):
    if f.startswith("card-") or f.startswith("illust-") or f == "features-grid.png":
        os.remove(os.path.join(out_dir, f))
        print(f"Removed: {f}")

img = Image.open(src)
W, H = img.size
print(f"Source: {W}x{H}")

# Copy full grid as-is
img.save(os.path.join(out_dir, "features-grid.png"))
print("Saved: features-grid.png (full grid)")

# 3x3 grid — each cell is roughly W/3 x H/3
cell_w = W // 3
cell_h = H // 3

# Names matching the new grid content (row by row)
# Row 0: person+ laptop, cloud/servers+shield, rocket
# Row 1: website mockup, computer+charts, headset+chat
# Row 2: bar graph+arrow, gauge meter, shield+lock
names = [
    "build-presence",    # row 0, col 0 — person with laptop (remote work)
    "succeed-online",    # row 0, col 1 — cloud servers + shield (security)
    "fast-secure",       # row 0, col 2 — rocket (launch/innovation)
    "hosting-easy",      # row 1, col 0 — website mockup (web design)
    "site-priority",     # row 1, col 1 — computer with charts (analytics)
    "expert-support",    # row 1, col 2 — headset + chat (support)
    "scalable",          # row 2, col 0 — bar graph (growth)
    "speed-perf",        # row 2, col 1 — gauge meter (performance)
    "trusted",           # row 2, col 2 — shield + lock (cybersecurity)
]

for row in range(3):
    for col in range(3):
        idx = row * 3 + col
        left = col * cell_w
        top = row * cell_h
        right = left + cell_w
        bottom = top + cell_h
        card = img.crop((left, top, right, bottom))
        name = names[idx]
        card_path = os.path.join(out_dir, f"card-{name}.png")
        card.save(card_path)
        print(f"Saved: card-{name}.png ({card.width}x{card.height})")

print("\nDone! Old images removed, new images cropped and saved.")
