from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Color:
    red: float
    green: float
    blue: float
    opacity: float = 1.0

    def __post_init__(self):
        for comp in ('red', 'green', 'blue', 'opacity'):
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


class FillStyle(Enum):
    Solid = 'solid'
    Gradient = 'gradient'


class StrokeStyle(Enum):
    Solid = 'solid'
    Dash = 'dash'
    Dot = 'dot'
    DashDot = 'dashdot'
    DashDotDot = 'dashdotot'
