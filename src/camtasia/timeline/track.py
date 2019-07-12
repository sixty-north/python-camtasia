from .track_media import TrackMedia
from camtasia.media_bin import MediaType


class Track:
    """A track on the timeline.

    Args:
        attributes: The 'trackAttributes' record for this track.
        data: the entry in the 'timeline' record for this track.
        timeline: The Timeline instance containing this Track.
    """

    def __init__(self, attributes, data, timeline):
        self._attributes = attributes
        self._data = data
        self._medias = _Medias(data, timeline)

    @property
    def name(self):
        return self._attributes['ident']

    @property
    def index(self):
        return self._data['trackIndex']

    @property
    def audio_muted(self):
        return self._attributes['audioMuted']

    @property
    def video_hidden(self):
        return self._attributes['videoHidden']

    @property
    def medias(self):
        return self._medias

    def __repr__(self):
        return f'Track(name="{self.name}")'


class _Medias:
    """Collection of medias on a specific track.
    """

    def __init__(self, data, timeline):
        self._data = data
        self._timeline = timeline

    def __len__(self):
        return len(self._data['medias'])

    def __iter__(self):
        for media_data in self._data['medias']:
            yield TrackMedia(media_data)

    def __getitem__(self, media_id):
        """Get a TrackMedia by ID.

        Args:
            media_id: The ID of the media to get.

        Returns: A TrackMedia instance.

        Raises:
            KeyError: There is no TrackMedia with the given ID.
        """
        for media in self:
            if media.id == media_id:
                return media

        raise KeyError(f'No TrackMedia with id={media_id}')

    def __delitem__(self, media_id):
        if not any(m.id == media_id for m in self):
            raise KeyError(f'No TrackMedia with id={media_id}')

        self._data['medias'] = [m for m in self if m.id != media_id]

    def add_media(self, bin_media, start, duration=None):
        if bin_media.type == MediaType.Image:
            record = self._image_record(bin_media, start, duration)
        elif bin_media.type == MediaType.Video:
            record = self._video_record(bin_media, start, duration)
        else:
            raise ValueError(
                'Unsupported media type: {}'.format(bin_media.type))

        new_media = TrackMedia(record)

        if any(_overlaps(new_media, m) for m in self):
            raise ValueError(f'Track media overlaps existing media: {new_media}')

        self._data['medias'].append(record)
        return self[record['id']]

    def _next_media_id(self):
        max_media_id = max((media.id
                            for track in self._timeline.tracks
                            for media in track.medias),
                           default=0)

        return max_media_id + 1

    def _video_record(self, bin_media, start, duration):
        return {
            "id": self._next_media_id(),
            "_type": "ScreenVMFile",
            "src": bin_media.id,
            "trackNumber": 0,  # TODO: Is this correct? What is this?
            "attributes": {
                "ident": bin_media.identity
            },
            "parameters": {
                "scale0": {
                    "type": "double",
                            "defaultValue": 0.25,
                            "interp": "eioe"
                },
                "scale1": {
                    "type": "double",
                            "defaultValue": 0.25,
                            "interp": "eioe"
                },
                "cursorScale": {
                    "type": "double",
                            "defaultValue": 1.0,
                            "interp": "linr"
                },
                "cursorOpacity": {
                    "type": "double",
                            "defaultValue": 1.0,
                            "interp": "linr"
                }
            },
            "effects": [

            ],
            "start": start,
            "duration": bin_media.range[1] if duration is None else duration,
            "mediaStart": bin_media.range[0],
            "mediaDuration": bin_media.range[1],
            "scalar": 1,
            "metadata": {
                "clipSpeedAttribute": False,
                "default-scale": "0.25",
                "effectApplied": "none"
            },
            "animationTracks": {

            }
        }

    def _image_record(self, bin_media, start, duration):
        return {
            "id": self._next_media_id(),
            "_type": "IMFile",
            "src": bin_media.id,
            "trackNumber": 0,
            "trimStartSum": 0,
            "attributes": {
                "ident": bin_media.identity
            },
            "parameters": {
                "scale0": {
                    "type": "double",
                            "defaultValue": 1.0,
                            "interp": "eioe"
                },
                "scale1": {
                    "type": "double",
                            "defaultValue": 1.0,
                            "interp": "eioe"
                }
            },
            "effects": [

            ],
            "start": start,
            "duration": 150 if duration is None else duration,
            "mediaStart": bin_media.range[0],
            "mediaDuration": bin_media.range[1],
            "scalar": 1,
            "metadata": {
                "clipSpeedAttribute": False,
                "default-scale": "1.0",
                "effectApplied": "none"
            },
            "animationTracks": {

            }
        }


def _overlaps(media_a, media_b):
    "Determines if two TrackMedia overlap."
    a1 = media_a.start
    a2 = media_a.start + media_a.duration - 1
    b1 = media_b.start
    b2 = media_b.start + media_b.duration - 1
    return a1 <= b2 and b1 <= a2

