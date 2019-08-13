"""Callout annotations.
"""

from .types import Color, FillStyle, HorizontalAlignment, StrokeStyle, VerticalAlignment


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


def square(text,
           font_name,
           font_weight,
           font_size=64.0,
           font_color=Color(0.0, 0.0, 0.0),
           fill_color=Color(1.0, 1.0, 1.0),
           fill_style=FillStyle.Solid,
           stroke_color=Color(0, 0.5, 0.5),
           stroke_width=2.0,
           stroke_style=StrokeStyle.Solid,
           height=150.0,
           width=350.0,
           horizontal_alignment=HorizontalAlignment.Center,
           vertical_alignment=VerticalAlignment.Center,
           line_spacing=0.0):
    return {
        "kind": "remix",
        "shape": "text-rectangle",
        "style": "basic",
        "fill-color-blue": fill_color.blue,
        "fill-color-green": fill_color.green,
        "fill-color-opacity": fill_color.opacity,
        "fill-color-red": fill_color.red,
        "height": float(height),
        "line-spacing": line_spacing,
        "stroke-color-blue": stroke_color.blue,
        "stroke-color-green": stroke_color.green,
        "stroke-color-opacity": stroke_color.opacity,
        "stroke-color-red": stroke_color.red,
        "stroke-width": float(stroke_width),
        "tail-x": 0.0,
        "tail-y": -20.0,
        "width": float(width),
        "word-wrap": 1.0,
        "fill-style": fill_style.value,
        "horizontal-alignment": horizontal_alignment.value,
        "resize-behavior": "resizeText",
        "stroke-style": stroke_style.value,
        "text": text,
        "vertical-alignment": vertical_alignment.value,
        "font": {
            "color-blue": font_color.blue,
            "color-green": font_color.green,
            "color-opacity": font_color.opacity,
            "color-red": font_color.red,
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
