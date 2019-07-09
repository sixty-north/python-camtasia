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

        self._tracks = _Tracks(self._data, self._frame_rate)

    @property
    def tracks(self):
        return self._tracks

    @property
    def markers(self) -> Iterable[Marker]:
        """Markers on the timeline (i.e. not media-specific markers)
        """
        for frame in self._data.get('parameters', {}).get('toc', {}).get('keyframes', ()):
            yield Marker(name=frame['value'], time=FrameStamp(frame_number=frame['time'], frame_rate=self._frame_rate))

    # TODO: Support for editing markers


class _Tracks:
    """Container for Tracks.
    """

    def __init__(self, data, frame_rate):
        self._data = data
        self._frame_rate = frame_rate

    def __iter__(self):
        for idx, attrs in enumerate(self._data['trackAttributes']):
            # As far as I can tell, there's only ever one scene. Hence the 0.
            data = self._data['sceneTrack']['scenes'][0]['csml']['tracks'][idx]
            yield Track(attrs, data, self._frame_rate)

    def __getitem__(self, track_index):
        for track in self:
            if track.index == track_index:
                return track

        raise KeyError('No track with index {}'.format(track_index))

    def __delitem__(self, track_index):
        for idx, track in enumerate(self):
            if track.index == track_index:
                self._data['trackAttributes'].pop(idx)
                self._data['sceneTrack']['scenes'][0]['csml']['tracks'].pop(
                    idx)
                return

        raise KeyError('No track with index {}'.format(track_index))

    # TODO: Insert new track
