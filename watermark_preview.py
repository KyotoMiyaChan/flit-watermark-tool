#!/usr/bin/env python3
"""
图片水印预览生成器（纯本地处理）
为图片添加半透明水印，生成一半分辨率的 JPG 预告图。
"""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

DEFAULT_WATERMARK_TEXT = "PREVIEW"
DEFAULT_FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"
WATERMARK_OPACITY = 128
WATERMARK_COLOR = (255, 255, 255, WATERMARK_OPACITY)
OUTPUT_FORMAT = "JPEG"
JPEG_QUALITY = 85

def get_font(size, font_path=DEFAULT_FONT_PATH):
    try:
        return ImageFont.truetype(font_path, size)
    except IOError:
        print(f"⚠️ 字体 {font_path} 未找到，使用默认字体")
        return ImageFont.load_default()

def add_watermark(image, text, font_path=DEFAULT_FONT_PATH):
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    layer = Image.new("RGBA", image.size, (0,0,0,0))
    draw = ImageDraw.Draw(layer)
    font_size = int(min(image.size) * 0.1)
    font = get_font(font_size, font_path)
    bbox = draw.textbbox((0,0), text, font=font)
    w = bbox[2]-bbox[0]
    h = bbox[3]-bbox[1]
    x = (image.width - w) / 2
    y = (image.height - h) / 2
    draw.text((x, y), text, font=font, fill=WATERMARK_COLOR)
    return Image.alpha_composite(image, layer).convert("RGB")

def resize_half(image):
    return image.resize((image.width//2, image.height//2), Image.Resampling.LANCZOS)

def main():
    parser = argparse.ArgumentParser(description="加水印并缩放")
    parser.add_argument("image")
    parser.add_argument("-o", "--output", default="preview.jpg")
    parser.add_argument("--text", default=DEFAULT_WATERMARK_TEXT)
    parser.add_argument("--quality", type=int, default=JPEG_QUALITY)
    parser.add_argument("--font", default=DEFAULT_FONT_PATH)
    args = parser.parse_args()
    try:
        img = Image.open(args.image)
        print(f"📷 原图尺寸: {img.size}")
    except Exception as e:
        print(f"❌ 无法打开图片: {e}")
        return
    img = resize_half(img)
    print(f"📐 缩放至一半: {img.size}")
    watermarked = add_watermark(img, args.text, args.font)
    watermarked.save(args.output, format=OUTPUT_FORMAT, quality=args.quality)
    print(f"✅ 已保存: {args.output}")

if __name__ == "__main__":
    main()
