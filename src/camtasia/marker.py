from dataclasses import dataclass


@dataclass
class Marker:
    "A marker in the project timeline."
    time: int
    end_time: int
    value: str
    duration: int  # this seems like a calculated value, yet it's stored in the JSON. Should we store it or calculate it?
