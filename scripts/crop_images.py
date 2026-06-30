"""Crop the 3x3 illustration grid into individual cards and illustration-only sections."""
from PIL import Image
import os

src = "/home/z/my-project/upload/88E3E17C-6578-4CF5-8C78-CA02B067F854.png"
out_dir = "/home/z/my-project/public/images"
os.makedirs(out_dir, exist_ok=True)

img = Image.open(src)
W, H = img.size  # 1536 x 1024
print(f"Source: {W}x{H}")

# Copy full grid as-is
img.save(os.path.join(out_dir, "features-grid.png"))
print("Saved: features-grid.png (full grid)")

# 3x3 grid — each cell is roughly W/3 x H/3
cell_w = W // 3
cell_h = H // 3

# Names for each cell
names = [
    "build-presence",    # row 0, col 0 — person with laptop
    "succeed-online",    # row 0, col 1 — servers + shield
    "fast-secure",       # row 0, col 2 — rocket
    "hosting-easy",      # row 1, col 0 — website dashboard
    "site-priority",     # row 1, col 1 — person at desk
    "expert-support",    # row 1, col 2 — support agent
    "scalable",          # row 2, col 0 — bar graph
    "speed-perf",        # row 2, col 1 — speedometer
    "trusted",           # row 2, col 2 — customer avatars
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

# Also crop just the bottom portion of each card for illustration-only
for row in range(3):
    for col in range(3):
        idx = row * 3 + col
        left = col * cell_w
        top = row * cell_h
        right = left + cell_w
        bottom = top + cell_h
        card = img.crop((left, top, right, bottom))

        # Crop bottom 55% for illustration
        crop_top = int(card.height * 0.45)
        illustration = card.crop((0, crop_top, card.width, card.height))
        name = names[idx]
        ill_path = os.path.join(out_dir, f"illust-{name}.png")
        illustration.save(ill_path)
        print(f"Saved: illust-{name}.png ({illustration.width}x{illustration.height})")

print("\nDone! All images cropped and saved.")
