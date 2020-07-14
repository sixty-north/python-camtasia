from numbers import Real

from marshmallow import Schema, fields, post_load
from marshmallow_oneofschema import OneOfSchema

from camtasia.color import RGBA

COLOR_KEY = "color"

COMPENSATION_KEY = "clrCompensation"
COLOR_ALPHA_KEY = "color-alpha"
COLOR_RED_KEY = "color-red"
COLOR_GREEN_KEY = "color-green"
COLOR_BLUE_KEY = "color-blue"
DEFRINGE_KEY = "defringe"
TOLERANCE_KEY = "tolerance"
SOFTNESS_KEY = "softness"
INVERT_EFFECT_KEY = "invertEffect"
CHROMA_KEY_NAME = "ChromaKey"
VISUAL_EFFECTS_CATEGORY = "categoryVisualEffects"





def rgba(argument):
    channels = hex_rgb(argument)
    if len(channels) == 3:
        return (*channels, 255)
    return channels


def rgb(argument):
    channels = hex_rgb(argument)
    if channels[3] != 255:
        raise ValueError("Alpha argument not 0xFF for RGB color")
    return channels[:3]


class Effect:

    def __init__(self, *, name, category):
        self._name = name
        self._category = category

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name!r}, category={self.category!r})"

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._key() == other._key()

    def __hash__(self):
        return hash(self._key())

    def _key(self):
        return (self.name, self.category)


class VisualEffect(Effect):

    def __init__(self, *, name):
        super().__init__(name=name, category=VISUAL_EFFECTS_CATEGORY)


class ChromaKeyEffect(VisualEffect):

    DEFAULT_TOLERANCE = 0.1
    MINIMUM_TOLERANCE = 0.0
    MAXIMUM_TOLERANCE = 1.0

    DEFAULT_SOFTNESS = 0.1
    MINIMUM_SOFTNESS = 0.0
    MAXIMUM_SOFTNESS = 1.0

    DEFAULT_DEFRINGE = 0.0
    MINIMUM_DEFRINGE = -1.0
    MAXIMUM_DEFRINGE = 1.0

    DEFAULT_INVERTED = False

    DEFAULT_COLOR = RGBA(0, 255, 0, 255)

    DEFAULT_COMPENSATION = 0.0  # Confusingly, this is called "hue" in the Camtasia GUI.
    MINIMUM_COMPENSATION = 0.0
    MAXIMUM_COMPENSATION = 1.0

    def __init__(self, tolerance=None, softness=None, hue=None, defringe=None, inverted=None, compensation=None):
        super().__init__(name=CHROMA_KEY_NAME)

        if tolerance is None:
            tolerance = self.DEFAULT_TOLERANCE

        if not (self.MINIMUM_TOLERANCE <= tolerance <= self.MAXIMUM_TOLERANCE):
            raise ValueError(
                f"{self.name} tolerance out of range {self.MINIMUM_TOLERANCE} "
                f"to {self.MAXIMUM_TOLERANCE}"
            )

        if softness is None:
            softness = self.DEFAULT_SOFTNESS

        if not (self.MINIMUM_SOFTNESS <= softness <= self.MAXIMUM_SOFTNESS):
            raise ValueError(
                f"{self.name} softness out of range {self.MINIMUM_SOFTNESS} "
                f"to {self.MAXIMUM_SOFTNESS}"
            )

        if defringe is None:
            defringe = self.DEFAULT_DEFRINGE

        if not (self.MINIMUM_DEFRINGE <= defringe <= self.MAXIMUM_DEFRINGE):
            raise ValueError(
                f"{self.name} defringe out of range {self.MINIMUM_DEFRINGE} "
                f"to {self.MAXIMUM_DEFRINGE}"
            )

        if compensation is None:
            compensation = self.DEFAULT_COMPENSATION

        if not (self.MINIMUM_COMPENSATION <= compensation <= self.MAXIMUM_COMPENSATION):
            raise ValueError(
                f"{self.name} compensation out of range {self.MINIMUM_COMPENSATION} "
                f"to {self.MAXIMUM_COMPENSATION}"
            )

        if inverted is None:
            inverted = self.DEFAULT_INVERTED

        if hue is None:
            hue = self.DEFAULT_COLOR
        elif isinstance(hue, str):
            hue = RGBA.from_hex(hue)

        self._tolerance = tolerance
        self._softness = softness
        self._defringe = defringe
        self._inverted = inverted
        self._hue = hue
        self._compensation = compensation

    @property
    def tolerance(self):
        return self._tolerance

    @property
    def softness(self):
        return self._softness

    @property
    def defringe(self):
        return self._defringe

    @property
    def inverted(self):
        return self._inverted

    @property
    def compensation(self):
        return self._compensation

    @property
    def hue(self):
        return self._hue

    @property
    def alpha(self):
        return self._hue.alpha / RGBA.MAXIMUM_CHANNEL

    @property
    def red(self):
        return self._hue.red / RGBA.MAXIMUM_CHANNEL

    @property
    def green(self):
        return self._hue.green / RGBA.MAXIMUM_CHANNEL

    @property
    def blue(self):
        return self._hue.blue / RGBA.MAXIMUM_CHANNEL

    @property
    def parameters(self):
        return Parameters(self)

    @property
    def metadata(self):
        return {
            f"default-{self.name}-{key}": self._metadata_value(value) for key, value in self._metadata().items()
        }

    @staticmethod
    def _metadata_value(value):
        """Render a metadata value in the way Camtasia expects
        """
        if isinstance(value, Real):
            if value == 0:
                value = 0
        return str(value).replace(" ", "")


    def _metadata(self):
        return {
            COLOR_KEY: self.DEFAULT_COLOR.as_tuple(),
            DEFRINGE_KEY: self.DEFAULT_DEFRINGE,
            INVERT_EFFECT_KEY: int(self.DEFAULT_INVERTED),
            SOFTNESS_KEY: self.DEFAULT_SOFTNESS,
            TOLERANCE_KEY: self.DEFAULT_TOLERANCE,
            COMPENSATION_KEY: self.DEFAULT_COMPENSATION,
        }

    def _key(self):
        return super()._key() + (
            self.tolerance,
            self.softness,
            self.defringe,
            self.inverted,
            self.compensation,
            self.red,
            self.green,
            self.blue,
            self.alpha,
        )

    def __repr__(self):
        return (
            f"{type(self).__name__}(tolerance={self.tolerance}, softness={self.softness}, "
            f"hue={self.hue}, defringe={self.defringe}, inverted={self.inverted}, "
            f"compensation={self.compensation})"
        )


class Parameters:

    def __init__(self, effect):
        self._effect = effect

    def __getattr__(self, name):
        return getattr(self._effect, name)


class ChromaKeyEffectParametersSchema(Schema):
    compensation = fields.Float(data_key=COMPENSATION_KEY)
    alpha = fields.Float(data_key=COLOR_ALPHA_KEY)
    red = fields.Float(data_key=COLOR_RED_KEY)
    green = fields.Float(data_key=COLOR_GREEN_KEY)
    blue = fields.Float(data_key=COLOR_BLUE_KEY)
    defringe = fields.Float(data_key=DEFRINGE_KEY)
    enabled = fields.Constant(1)
    inverted = fields.Function(
        data_key=INVERT_EFFECT_KEY,
        serialize=lambda obj: float(obj.inverted),
        deserialize=lambda b: bool(b)
    )
    softness = fields.Float(data_key=SOFTNESS_KEY)
    tolerance = fields.Float(tolerance=TOLERANCE_KEY)


class ChromaKeyEffectSchema(Schema):

    category = fields.Str(data_key="category")
    parameters = fields.Nested(ChromaKeyEffectParametersSchema)

    @post_load
    def make_chroma_key_effect(self, data, **kwargs):
        parameters = data["parameters"]
        return ChromaKeyEffect(
            tolerance=parameters["tolerance"],
            softness=parameters["softness"],
            hue=RGBA.from_floats(
                red=parameters["red"],
                green=parameters["green"],
                blue=parameters["blue"],
                alpha=parameters["alpha"],
            ),
            defringe=parameters["defringe"],
            inverted=parameters["inverted"],
            compensation=parameters["compensation"]
        )


class EffectSchema(OneOfSchema):
    type_schemas = {
        CHROMA_KEY_NAME: ChromaKeyEffectSchema,
    }

    type_field = "effectName"

    def get_obj_type(self, obj):
        return obj.name

