"""Generate the PNG used as the repository social preview."""

from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1280, 640


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = (
        ["DejaVuSans-Bold.ttf", "arialbd.ttf"]
        if bold
        else ["DejaVuSans.ttf", "arial.ttf"]
    )
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def render_social_preview(config: dict, output_path: str | Path) -> None:
    """Render a deterministic 1280x640 social preview with a solid background."""
    profile = config["profile"]
    name = profile["name"]
    tagline = profile.get("tagline", "")
    arms = config.get("galaxy_arms", [])

    image = Image.new("RGB", (WIDTH, HEIGHT), "#0d1117")
    draw = ImageDraw.Draw(image)

    # Deterministic star field keeps previews stable between runs.
    for index in range(110):
        digest = hashlib.sha256(f"{config['username']}:{index}".encode()).digest()
        x = int.from_bytes(digest[:2], "big") % WIDTH
        y = int.from_bytes(digest[2:4], "big") % HEIGHT
        radius = 1 + digest[4] % 3
        shade = 95 + digest[5] % 120
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(shade,) * 3)

    accent = "#58a6ff"
    violet = "#bc8cff"
    draw.rounded_rectangle((58, 58, WIDTH - 58, HEIGHT - 58), radius=30, fill="#161b22", outline="#30363d", width=3)
    draw.ellipse((820, 110, 1160, 450), fill="#111d2e", outline=accent, width=3)
    draw.ellipse((875, 165, 1105, 395), outline=violet, width=2)
    draw.ellipse((948, 238, 1032, 322), fill="#0d1117", outline=accent, width=4)
    draw.ellipse((978, 268, 1002, 292), fill="#f0f6fc")

    draw.text((110, 145), name, font=_font(58, bold=True), fill="#f0f6fc")
    draw.text((112, 225), tagline, font=_font(28), fill="#8b949e")
    draw.line((112, 286, 705, 286), fill="#30363d", width=3)

    labels = [arm.get("name", "") for arm in arms[:3]]
    colors = [accent, violet, "#d29922"]
    y = 330
    for label, color in zip(labels, colors, strict=False):
        draw.rounded_rectangle((112, y, 132, y + 20), radius=5, fill=color)
        draw.text((152, y - 8), label, font=_font(24), fill="#c9d1d9")
        y += 58

    draw.text((112, 520), f"github.com/{config['username']}", font=_font(23), fill=accent)
    image.save(output_path, format="PNG", optimize=True)
