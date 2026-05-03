import os, glob
from PIL import ImageFont

FONT_DIRS = [
    "/System/Library/Fonts",
    "/System/Library/Fonts/Supplemental",
    "/Library/Fonts",
    os.path.expanduser("~/Library/Fonts"),
]

def scan_fonts():
    fonts = {}
    for d in FONT_DIRS:
        if not os.path.isdir(d):
            continue
        for ext in ("*.ttf", "*.ttc", "*.otf"):
            for path in glob.glob(os.path.join(d, ext)):
                name = os.path.splitext(os.path.basename(path))[0]
                fonts[name] = path
    return fonts

def load_font(font_path, size):
    if not os.path.exists(font_path):
        return ImageFont.load_default()
    try:
        if font_path.lower().endswith(".ttc"):
            for idx in range(6):
                try:
                    return ImageFont.truetype(font_path, size, index=idx)
                except:
                    continue
        else:
            return ImageFont.truetype(font_path, size)
    except:
        pass
    return ImageFont.load_default()
