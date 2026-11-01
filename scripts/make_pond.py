"""Place Git Koi's animated fish on a wider, transparent swimming path."""
from math import cos, pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps, ImageSequence

source = Image.open("koi/koi.gif")
frames = [frame.convert("RGBA") for frame in ImageSequence.Iterator(source)]
duration = source.info.get("duration", 70)
bounds = [frame.getbbox() for frame in frames if frame.getbbox()]
box = (min(b[0] for b in bounds), min(b[1] for b in bounds),
       max(b[2] for b in bounds), max(b[3] for b in bounds))
fish = [frame.crop(box) for frame in frames]
target_width = 132
target_height = round(fish[0].height * target_width / fish[0].width)
fish = [frame.resize((target_width, target_height), Image.Resampling.NEAREST) for frame in fish]

width, height = 760, max(94, target_height + 38)
output = []
count = len(fish) * 2
for i in range(count):
    phase = i / count
    x = round((width - target_width) * (1 - cos(2 * pi * phase)) / 2)
    y = round(7 + 4 * sin(4 * pi * phase))
    sprite = fish[i % len(fish)]
    if i >= len(fish):
        sprite = ImageOps.mirror(sprite)
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    # Broken wave strokes form a quiet divider that works on light and dark pages.
    for row, starts in ((25, (30, 172, 320, 490, 650)),
                        (55, (5, 120, 255, 440, 590, 725)),
                        (height - 12, (60, 220, 390, 545, 680))):
        for start in starts:
            points = [(px, round(row + 2 * sin((px - start) * pi / 24)))
                      for px in range(max(0, start), min(width, start + 54), 2)]
            if len(points) > 1:
                draw.line(points, fill=(78, 127, 151, 255), width=1)
    # A few bubbles follow the fish and move with it.
    direction = 1 if i < len(fish) else -1
    tail = x + (4 if direction == 1 else target_width - 4)
    for j in range(3):
        bx = round(tail - direction * (12 + j * 11))
        by = y + target_height // 2 + round(5 * sin(2 * pi * phase + j))
        if 1 <= bx < width - 1:
            draw.point((bx, by), fill=(105, 163, 184, 255))
    canvas.alpha_composite(sprite, (x, y))
    output.append(canvas)

Path("koi").mkdir(exist_ok=True)
output[0].save("koi/pond.gif", save_all=True, append_images=output[1:],
               duration=duration, loop=0, disposal=2, optimize=False)
