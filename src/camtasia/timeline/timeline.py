from typing import Iterable

from .marker import Marker
from .track import Track


class Timeline:
    """Represents the timeline elements of the Camtasia UI.

    Args:
        timeline_data: The 'timeline' sub-dict of the full (i.e. tscproj file) project dict.
    """

    def __init__(self, timeline_data):
        self._data = timeline_data

        self._tracks = _Tracks(self._data, self)

    @property
    def tracks(self):
        return self._tracks

    @property
    def markers(self) -> Iterable[Marker]:
        """Markers on the timeline (i.e. not media-specific markers)
        """
        for frame in self._data.get('parameters', {}).get('toc', {}).get('keyframes', ()):
            yield Marker(name=frame['value'], time=frame['time'])

    # TODO: Support for editing markers


class _Tracks:
    """Container for Tracks.
    """

    def __init__(self, data, timeline):
        self._data = data
        self._timeline = timeline

    def __len__(self):
        return len(self._track_list)

    def __iter__(self):
        for idx, attrs in enumerate(self._data['trackAttributes']):
            # As far as I can tell, there's only ever one scene. Hence the 0.
            data = self._track_list[idx]
            yield Track(attrs, data, self._timeline)

    def __getitem__(self, track_index):
        for track in self:
            if track.index == track_index:
                return track

        raise KeyError('No track with index {}'.format(track_index))

    def __delitem__(self, track_index):
        for idx, track in enumerate(self):
            if track.index == track_index:
                self._data['trackAttributes'].pop(idx)
                self._track_list.pop(
                    idx)
                return

        raise KeyError('No track with index {}'.format(track_index))

    @property
    def _track_list(self):
        return self._data['sceneTrack']['scenes'][0]['csml']['tracks']

    def insert_track(self, index, name):
        record = {
            "trackIndex": index,
            "medias": [
            ]
        }

        attributes_record = {
            "ident": name,
            "audioMuted": False,
            "videoHidden": False,
            "magnetic": False,
            "metadata": {
                "IsLocked": "False",
                "trackHeight": "33"
            }
        }

        self._track_list.insert(index, record)

        self._data['trackAttributes'].insert(index, attributes_record)

        # Unfortunately, camtasia uses track index as the ID for tracks. So as we insert tracks, we need to manually
        # update the track indices since we may have messed them up.
        for index, record in enumerate(self._track_list):
            record['trackIndex'] = index

        return self[index]
