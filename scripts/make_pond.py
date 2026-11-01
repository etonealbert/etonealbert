"""Place Git Koi's animated fish on a wider, transparent swimming path."""
from math import cos, pi, sin
from pathlib import Path

from PIL import Image, ImageOps, ImageSequence

source = Image.open("koi/koi.gif")
frames = [frame.convert("RGBA") for frame in ImageSequence.Iterator(source)]
duration = source.info.get("duration", 70)
bounds = [frame.getbbox() for frame in frames if frame.getbbox()]
box = (min(b[0] for b in bounds), min(b[1] for b in bounds),
       max(b[2] for b in bounds), max(b[3] for b in bounds))
fish = [frame.crop(box) for frame in frames]
target_width = 150
target_height = round(fish[0].height * target_width / fish[0].width)
fish = [frame.resize((target_width, target_height), Image.Resampling.NEAREST) for frame in fish]

width, height = 760, max(120, target_height + 30)
output = []
count = len(fish) * 2
for i in range(count):
    phase = i / count
    x = round((width - target_width) * (1 - cos(2 * pi * phase)) / 2)
    y = round((height - target_height) / 2 + 8 * sin(4 * pi * phase))
    sprite = fish[i % len(fish)]
    if i >= len(fish):
        sprite = ImageOps.mirror(sprite)
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    canvas.alpha_composite(sprite, (x, y))
    output.append(canvas)

Path("koi").mkdir(exist_ok=True)
output[0].save("koi/pond.gif", save_all=True, append_images=output[1:],
               duration=duration, loop=0, disposal=2, optimize=False)
