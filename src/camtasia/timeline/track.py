from .media import Media
from camtasia.media_bin import MediaType


class Track:
    def __init__(self, attributes, data, frame_rate):
        self._attributes = attributes
        self._data = data
        self._frame_rate = frame_rate

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
        for media_data in self._data['medias']:
            yield Media(media_data, self._frame_rate)

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

    def __repr__(self):
        return f'Track(name="{self.name}")'
