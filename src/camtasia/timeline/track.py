from .track_media import TrackMedia
from camtasia.media_bin import MediaType


class Track:
    def __init__(self, attributes, data):
        self._attributes = attributes
        self._data = data
        self._medias = _Medias(data)

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
    def __init__(self, data):
        self._data = data

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

    def add_media(self, bin_media, start):
        if bin_media.type == MediaType.Image:
            record = self._image_record(bin_media, start)
        elif bin_media.type == MediaType.Video:
            record = self._video_record(bin_media, start)
        else:
            raise ValueError(
                'Unsupported media type: {}'.format(bin_media.type))

        # TODO: Check that it doesn't overlap something else on the timeline.

        self._data['medias'].append(record)

    def _next_media_id(self):
        max_media_id = max((rec['id']
                            for rec in self._data['medias']), default=0)
        return max_media_id + 1

    def _video_record(self, bin_media, start):
        return {
            "id": self._next_media_id(),
            "_type": "ScreenVMFile",
            "src": 1,
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
            "duration": bin_media.range[1],
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

    def _image_record(self, bin_media, start):
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
            "duration": 150,  # This seems to be camtasia's behavior. 
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

