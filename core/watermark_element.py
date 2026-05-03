from dataclasses import dataclass

@dataclass
class WatermarkElement:
    text: str = "PREVIEW"
    font_path: str = "/System/Library/Fonts/Helvetica.ttc"
    font_size: float = 36.0
    opacity: int = 50
    rotation: float = 0.0
    pos_x: float = 0.0
    pos_y: float = 0.0
    color: tuple = (255, 255, 255)
    scale: float = 1.0
