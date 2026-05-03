from PIL import Image, ImageDraw
from core.font_manager import load_font

class WatermarkParams:
    def __init__(self, text="PREVIEW", font_path=None, font_size=36,
                 opacity=50, rotation=0, mode="single",
                 tile_spacing_x=200, tile_spacing_y=150, scale=1.0,
                 pos_x=None, pos_y=None, color=(255,255,255)):
        self.text = text
        self.font_path = font_path or "/System/Library/Fonts/Helvetica.ttc"
        self.font_size = int(font_size)
        self.opacity = int(255 * opacity / 100)
        self.rotation = rotation
        self.mode = mode
        self.tile_spacing_x = tile_spacing_x
        self.tile_spacing_y = tile_spacing_y
        self.scale = scale
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color

def apply_watermark(image, params: WatermarkParams):
    if params.scale != 1.0:
        new_w = int(image.width * params.scale)
        new_h = int(image.height * params.scale)
        image = image.resize((new_w, new_h), Image.Resampling.LANCZOS)

    if image.mode != "RGBA":
        image = image.convert("RGBA")

    font = load_font(params.font_path, params.font_size)
    overlay = Image.new("RGBA", image.size, (0,0,0,0))

    if params.mode == "single":
        draw = ImageDraw.Draw(overlay)
        bbox = draw.textbbox((0,0), params.text, font=font)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        if tw <= 0 or th <= 0:
            return image.convert("RGB")

        padding = max(20, int(max(tw, th) * 0.3))
        layer_w = tw + padding * 2
        layer_h = th + padding * 2
        txt_layer = Image.new("RGBA", (layer_w, layer_h), (0,0,0,0))
        d = ImageDraw.Draw(txt_layer)
        color_rgba = (*params.color, params.opacity)
        d.text((padding - bbox[0], padding - bbox[1]), params.text, font=font, fill=color_rgba)

        if params.rotation != 0:
            try:
                txt_layer = txt_layer.rotate(params.rotation, expand=1,
                                             resample=Image.BICUBIC, fillcolor=(0,0,0,0))
            except:
                pass

        if params.pos_x is not None and params.pos_y is not None:
            x = int(params.pos_x - txt_layer.width / 2)
            y = int(params.pos_y - txt_layer.height / 2)
        else:
            x = (image.width - txt_layer.width) // 2
            y = (image.height - txt_layer.height) // 2

        overlay.paste(txt_layer, (x, y), txt_layer)

    result = Image.alpha_composite(image, overlay)
    return result.convert("RGB")
