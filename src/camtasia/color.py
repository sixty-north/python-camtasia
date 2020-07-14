def hex_rgb(argument):
    """Convert the argument string to a tuple of integers.
    """
    h = argument.lstrip("#")
    num_digits = len(h)
    if num_digits == 3:
        return (
            int(h[0], 16),
            int(h[1], 16),
            int(h[2], 16),
        )
    elif num_digits == 4:
        return (
            int(h[0], 16),
            int(h[1], 16),
            int(h[2], 16),
            int(h[3], 16),
        )
    elif num_digits == 6:
        return (
            int(h[0:2], 16),
            int(h[2:4], 16),
            int(h[4:6], 16),
        )
    elif num_digits == 8:
        return (
            int(h[0:2], 16),
            int(h[2:4], 16),
            int(h[4:6], 16),
            int(h[6:8], 16),
        )
    else:
        raise ValueError(f"Could not interpret {argument!r} as RGB or RGBA hex color")


class RGBA:

    MINIMUM_CHANNEL = 0
    MAXIMUM_CHANNEL = 255

    @classmethod
    def from_hex(cls, color):
        channels = hex_rgb(color)
        if len(channels) == 3:
            return cls(*channels, alpha=cls.MAXIMUM_CHANNEL)
        return cls(*channels)

    @classmethod
    def from_floats(cls, red, green, blue, alpha):
        return cls(
            red * cls.MAXIMUM_CHANNEL,
            green * cls.MAXIMUM_CHANNEL,
            blue * cls.MAXIMUM_CHANNEL,
            alpha * cls.MAXIMUM_CHANNEL,
        )

    def __init__(self, red, green, blue, alpha):
        if not (self.MINIMUM_CHANNEL <= red <= self.MAXIMUM_CHANNEL):
            raise ValueError(
                f"RGBA red channel {red} out of range {self.MINIMUM_CHANNEL} "
                f"to {self.MAXIMUM_CHANNEL}"
            )

        if not (self.MINIMUM_CHANNEL <= green <= self.MAXIMUM_CHANNEL):
            raise ValueError(
                f"RGBA green channel {green} out of range {self.MINIMUM_CHANNEL} "
                f"to {self.MAXIMUM_CHANNEL}"
            )

        if not (self.MINIMUM_CHANNEL <= blue <= self.MAXIMUM_CHANNEL):
            raise ValueError(
                f"RGBA blue channel {blue} out of range {self.MINIMUM_CHANNEL} "
                f"to {self.MAXIMUM_CHANNEL}"
            )

        if not (self.MINIMUM_CHANNEL <= alpha <= self.MAXIMUM_CHANNEL):
            raise ValueError(
                f"RGBA alpha channel {alpha} out of range {self.MINIMUM_CHANNEL} "
                f"to {self.MAXIMUM_CHANNEL}"
            )

        self._red = red
        self._green = green
        self._blue = blue
        self._alpha = alpha

    @property
    def red(self):
        return self._red

    @property
    def green(self):
        return self._green

    @property
    def blue(self):
        return self._blue

    @property
    def alpha(self):
        return self._alpha

    def as_tuple(self):
        return (self.red, self.green, self.blue, self.alpha)

    def _key(self):
        return self.as_tuple()

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._key() == other._key()

    def __hash__(self):
        return hash(self._key())

    def __repr__(self):
        return (
            f"{type(self).__name__}(red={self.red}, green={self.green}, "
            f"blue={self.blue}, alpha={self.alpha})"
        )