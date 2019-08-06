"""Support for creating annotations that can be added to tracks.
"""
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Color:
    red: float
    green: float
    blue: float

    def __post_init__(self):
        for comp in ('red', 'green', 'blue'):
            if not 0.0 <= getattr(self, comp) <= 1.0:
                raise ValueError(
                    f'Color {comp} component must be in the range [0.0, 1.0].')


class HorizontalAlignment(Enum):
    Left = 'left'
    Center = 'center'
    Right = 'right'


class VerticalAlignment(Enum):
    Top = 'top'
    Center = 'center'
    Bottom = 'bottom'


def text(text,
         font_name,
         font_weight,
         font_size=96.0,
         font_color=Color(1.0, 1.0, 1.0),
         height=250.0,
         width=400.0,
         horizontal_alignment=HorizontalAlignment.Center,
         vertical_alignment=VerticalAlignment.Center,
         line_spacing=0.0
         ):
    return {
        "kind": "remix",
        "shape": "text",
        "style": "basic",
        "height": float(height),
        "line-spacing": line_spacing,
        "width": float(width),
        "word-wrap": 1.0,
        "horizontal-alignment": horizontal_alignment.value,
        "resize-behavior": "resizeText",
        "text": text,
        "vertical-alignment": vertical_alignment.value,
        "font": {
            "color-blue": font_color.red,
            "color-green": font_color.green,
            "color-red": font_color.blue,
            "size": font_size,
            "tracking": 0.0,
            "name": font_name,
            "weight": font_weight
        },
        "textAttributes": {
            "type": "textAttributeList",
            "keyframes": [
                {
                    "endTime": 0,
                    "time": 0,
                    "value": None,
                    "duration": 0
                }
            ]
        }
    }
