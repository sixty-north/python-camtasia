from dataclasses import dataclass
from datetime import timedelta
from typing import Tuple


@dataclass
class FrameStamp:
    """Timestamp in terms of frame and framerate.

    Times in Camtasia projects are generally reported in terms of frames. To turn these into clock times, you need to
    also know a frame rate. This class captures those two bits of data.
    """
    frame_number: int
    frame_rate: int

    @property
    def frame_time(self) -> Tuple[timedelta, int]:
        """A tuple of seconds-resolution-time and sub-second frames.

        This matches the typical Camtasia UI time reporting where time is only reported at second resolution, and
        sub-second timing is reported in frames.
        """
        seconds, sub_frames = divmod(self.frame_number, self.frame_rate)

        return (timedelta(seconds=seconds), sub_frames)

    @property
    def time(self) -> timedelta:
        "The time of the frame as a high-resolution (i.e. subsecond) timedelta."
        seconds = self.frame_number / self.frame_rate
        return timedelta(seconds=seconds)

    def __str__(self):
        secs, frame = self.frame_time
        return f'{secs};{frame}'

    def __lt__(self, rhs):
        return self.time < rhs.time
