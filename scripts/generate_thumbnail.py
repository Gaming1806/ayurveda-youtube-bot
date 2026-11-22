#!/usr/bin/env python3
"""Generate a YouTube thumbnail (1280×720) with the video title over a solid colour.
Uses Pillow – no external API key required.
If you have a Stability AI key, replace the logic with a diffusion call."""
import os, argparse
from PIL import Image, ImageDraw, ImageFont

def make_thumbnail(title: str, output_path: str = "thumbnail.jpg", bg_color="#FF6B6B", text_color="#FFFFFF"):
    # Create a 1280x720 image with the background colour
    img = Image.new("RGB", (1280, 720), color=int(bg_color.lstrip("#"), 16))
    draw = ImageDraw.Draw(img)

    # Try to use a truetype font; fall back to default if not found.
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except Exception:
        font = ImageFont.load_default()

    # Center the text
    text_w, text_h = draw.textsize(title, font=font)
    x = (1280 - text_w) / 2
    y = (720 - text_h) / 2
    draw.text((x, y), title, fill=text_color, font=font)

    img.save(output_path, "JPEG")
    print(f"✅ Thumbnail saved → {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True, help="Video title to place on thumbnail")
    parser.add_argument("--output", default="thumbnail.jpg", help="Output file path")
    parser.add_argument("--bg-color", default="#FF6B6B", help="Background hex colour")
    parser.add_argument("--text-color", default="#FFFFFF", help="Text hex colour")
    args = parser.parse_args()
    make_thumbnail(args.title, args.output, args.bg_color, args.text_color)