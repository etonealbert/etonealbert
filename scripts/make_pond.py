"""Frame Git Koi's unmodified circular swim with a quiet water pattern."""
from math import pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageSequence

source = Image.open("koi/cruise.gif")
duration = source.info.get("duration", 70)
width, height, koi_size = 760, 200, 200
frames = []
for frame in ImageSequence.Iterator(source):
    koi = frame.convert("RGBA").resize((koi_size, koi_size), Image.Resampling.NEAREST)
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    for row, starts in ((55, (30, 145, 565, 690)),
                        (100, (5, 195, 535, 715)),
                        (145, (65, 175, 570, 670))):
        for start in starts:
            points = [(x, round(row + 2 * sin((x - start) * pi / 24)))
                      for x in range(start, min(width, start + 54), 2)]
            draw.line(points, fill=(78, 127, 151, 255), width=1)
    canvas.alpha_composite(koi, ((width - koi_size) // 2, 0))
    frames.append(canvas)

Path("koi").mkdir(exist_ok=True)
frames[0].save("koi/pond.gif", save_all=True, append_images=frames[1:],
               duration=duration, loop=0, disposal=2, optimize=False)
