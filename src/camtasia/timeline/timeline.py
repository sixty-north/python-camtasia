from typing import Iterable

from ..frame_stamp import FrameStamp
from .marker import Marker
from .track import Track


class Timeline:
    """Represents the timeline elements of the Camtasia UI.

    Args:
        timeline_data: The 'timeline' sub-dict of the full (i.e. tscproj file) project dict.
    """

    def __init__(self, timeline_data, frame_rate):
        self._data = timeline_data
        self._frame_rate = frame_rate

    @property
    def tracks(self) -> Iterable[Track]:
        for idx, attrs in enumerate(self._data['trackAttributes']):
            # As far as I can tell, there's only ever one scene. Hence the 0.
            data = self._data['sceneTrack']['scenes'][0]['csml']['tracks'][idx]
            yield Track(attrs, data, self._frame_rate)

    @property
    def markers(self) -> Iterable[Marker]:
        """Markers on the timeline (i.e. not media-specific markers)
        """
        for frame in self._data['parameters']['toc']['keyframes']:
            yield Marker(name=frame['value'], time=FrameStamp(frame_number=frame['time'], frame_rate=self._frame_rate))
