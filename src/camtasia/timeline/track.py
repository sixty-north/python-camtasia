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
            self._add_image(bin_media, start)
        elif bin_media.type == MediaType.Video:
            pass
        else:
            raise ValueError(
                'Unsupported media type: {}'.format(bin_media.type))

    def _next_media_id(self):
        max_media_id = max((rec['id'] for rec in self._data['medias']), default=0)
        return max_media_id + 1

    def _add_image(self, bin_media, start):
        record = {
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
            "duration": 150,
            "mediaStart": 0,
            "mediaDuration": 1,
            "scalar": 1,
            "metadata": {
                "clipSpeedAttribute": False,
                "default-scale": "1.0",
                "effectApplied": "none"
            },
            "animationTracks": {

            }
        }

        # TODO: Check that it doesn't overlap something else on the timeline.

        self._data['medias'].append(record)

    def __repr__(self):
        return f'Track(name="{self.name}")'

# Example of image file
#

# Example of screen-recording
#
# {
#                     "id" : 6,
#                     "_type" : "ScreenVMFile",
#                     "src" : 1,
#                     "trackNumber" : 0,
#                     "attributes" : {
#                       "ident" : "fnord"
#                     },
#                     "parameters" : {
#                       "scale0" : {
#                         "type" : "double",
#                         "defaultValue" : 0.25,
#                         "interp" : "eioe"
#                       },
#                       "scale1" : {
#                         "type" : "double",
#                         "defaultValue" : 0.25,
#                         "interp" : "eioe"
#                       },
#                       "cursorScale" : {
#                         "type" : "double",
#                         "defaultValue" : 1.0,
#                         "interp" : "linr"
#                       },
#                       "cursorOpacity" : {
#                         "type" : "double",
#                         "defaultValue" : 1.0,
#                         "interp" : "linr"
#                       }
#                     },
#                     "effects" : [

#                     ],
#                     "start" : 1070,
#                     "duration" : 1032,
#                     "mediaStart" : 0,
#                     "mediaDuration" : 1032,
#                     "scalar" : 1,
#                     "metadata" : {
#                       "clipSpeedAttribute" : false,
#                       "default-scale" : "0.25",
#                       "effectApplied" : "none"
#                     },
#                     "animationTracks" : {

#                     }
#                   }
