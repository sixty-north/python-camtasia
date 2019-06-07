from dataclasses import dataclass

from camtasia.frame_stamp import FrameStamp


@dataclass
class Marker:
    name: str
    time: FrameStamp
