from collections import ChainMap

from camtasia.effects import EffectSchema
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

    def add_media(self, bin_media, start, duration=None, *, effects=None):
        """Add media from the bin to the track.

        Args:
            bin_media: The `media_bin.Media` to insert into the timeline.
            start: The frame on the timeline at which the media starts.
            duration: The duration in frames of the media on the timeline.
            effects: An optional sequence of Effect objects.

        Raises:
            ValueError: The type of the bin media is unsupported.
            ValueError: The media can't be inserted because it overlaps existing media on the track.
        """
        if bin_media.type == MediaType.Image:
            record = self._image_record(bin_media, start, duration, effects)
        elif bin_media.type == MediaType.Video:
            record = self._video_record(bin_media, start, duration, effects)
        elif bin_media.type == MediaType.Audio:
            record = self._audio_record(bin_media, start, duration, effects)  # TODO: Probably need to add _audio_record() method
        else:
            raise ValueError(
                'Unsupported media type: {}'.format(bin_media.type))

        return self._insert_media(record)

    def add_annotation(self, annotation, start, duration=None, translation=(0, 0)):
        """Adds a new annotation to the track.

        Args:
            annotation: The annotation record dict, as produced by functions in the `annotations` package.
            start: The frame at which the annotation should start.
            duration: The duration in frames of the annotation.
            translation: A `(x-translation, y-translation)` tuple describing how to translate the annotation.

        Raises:
            ValueError: The annotation can't be inserted because it overlaps existing media on the track.
        """
        record = self._annotation_record(
            annotation, start, duration, translation)
        return self._insert_media(record)

    def _insert_media(self, record):
        new_media = TrackMedia(record)

        if any(_overlaps(new_media, m) for m in self):
            raise ValueError(
                f'Track media overlaps existing media: {new_media}')

        self._data['medias'].append(record)
        return self[record['id']]

    def _next_media_id(self):
        max_media_id = max((media.id
                            for track in self._timeline.tracks
                            for media in track.medias),
                           default=0)

        return max_media_id + 1

    def _annotation_record(self, annotation, start, duration, translation):
        duration = 150 if duration is None else duration

        return {
            "id": self._next_media_id(),
            "_type": "Callout",
            "def": annotation,
            "attributes": {
                "autoRotateText": True
            },
            "effects": [

            ],
            "start": start,
            "duration": duration,
            "mediaStart": 0,
            "mediaDuration": duration,
            "scalar": 1,
            "metadata": {
                "AppliedThemeId": "",
                "clipSpeedAttribute": False,
                "default-scale": "1",
                "effectApplied": "none"
            },
            "animationTracks": {

            },
            "parameters": {
                "translation0": translation[0],
                "translation1": translation[1]
            }
        }

    def _video_record(self, bin_media, start, duration, effects):
        duration = bin_media.range[1].to_frame() if duration is None else duration

        if duration > bin_media.range[1].to_frame():
            return self._stiched_video_record(bin_media, start, duration)

        if effects is None:
            effects = []

        effect_schema = EffectSchema()

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
                            "defaultValue": 1.0,
                            "interp": "eioe"
                },
                "scale1": {
                    "type": "double",
                            "defaultValue": 1.0,
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
                effect_schema.dump(effect) for effect in effects
            ],
            "start": start,
            "duration": duration,
            "mediaStart": bin_media.range[0].to_frame(),
            "mediaDuration": duration,
            "scalar": 1,
            "metadata": dict(ChainMap(
                {
                    "clipSpeedAttribute": False,
                    "default-scale": "1.0",
                    "effectApplied": "none" if len(effects) == 0 else effects[-1].name,
                },
                *(effect.metadata for effect in effects)
            )),
            "animationTracks": {

            }
        }

    def _image_record(self, bin_media, start, duration, effects=None):
        if effects is None:
            effects = []

        effect_schema = EffectSchema()

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
                effect_schema.dump(effect) for effect in effects
            ],
            "start": start,
            "duration": 150 if duration is None else duration,
            "mediaStart": bin_media.range[0].to_frame(),
            "mediaDuration": bin_media.range[1].to_frame(),
            "scalar": 1,
            "metadata": dict(ChainMap(
                {
                    "clipSpeedAttribute": False,
                    "default-scale": "1.0",
                    "effectApplied": "none" if len(effects) == 0 else effects[-1].name,
                },
                *(effect.metadata for effect in effects)
            )),
            "animationTracks": {

            }
        }

    def _audio_record(self, bin_media, start, duration, effects):
        duration = bin_media.range[1].to_frame() if duration is None else duration

        if duration > bin_media.range[1].to_frame():
            return self._stiched_video_record(bin_media, start, duration)

        if effects is None:
            effects = []

        effect_schema = EffectSchema()

        return {
            "id": self._next_media_id(),
            "_type": "AMFile",
            "src": bin_media.id,
            "trackNumber": 0,  # TODO: Is this correct? What is this?
            "attributes": {
                "ident": bin_media.identity,
                "gain": 1.0,
                "mixToMono": False,
                "channelNumber": "0,1"

            },
             "effects": [
            ],
            "start": start,
            "duration": duration,
            "mediaStart": bin_media.range[0].to_frame(),
            "mediaDuration": duration,
            "scalar": 1,
            "metadata": dict(ChainMap(
                {
                    "clipSpeedAttribute": False,
                    "effectApplied": "none" if len(effects) == 0 else effects[-1].name,
                },
                *(effect.metadata for effect in effects)
            )),
            "animationTracks": {
            }
        }

    def _stiched_video_record(self, bin_media, start, duration):
        "Video which is extended past its end with still."

        assert duration > bin_media.range[1].to_frame(), "Stitching/extending video unnecessarily."

        return {
            "id": self._next_media_id(),
            "_type": "StitchedMedia",
            "minMediaStart": 0,
            "attributes": {
                "ident": bin_media.identity,
                "gain": 1.0,
                "mixToMono": False
            },
            "parameters": {
                "cursorOpacity": 1.0,
                "cursorScale": 1.0
            },
            "medias": [
                {
                    "id": self._next_media_id(),
                    "_type": "VMFile",
                    "src": bin_media.id,
                    "trackNumber": 0,  # TODO: What is this?
                    "attributes": {
                        "ident": bin_media.identity,
                    },
                    "effects": [

                    ],
                    "start": 0,
                    "duration": bin_media.range[1].to_frame(),
                    "mediaStart": 0,
                    "mediaDuration": bin_media.range[1].to_frame(),
                    "scalar": 1,
                    "metadata": {
                        "clipSpeedAttribute": False,
                        "default-scale": "1.0",
                        "effectApplied": "none"
                    },
                    "animationTracks": {

                    }
                },
                {
                    "id": self._next_media_id(),
                    "_type": "IMFile",
                    "src": bin_media.id,
                    "trackNumber": 0,
                    "trimStartSum": 0,
                    "attributes": {
                        "ident": "Frame of {}".format(bin_media.identity)
                    },
                    "effects": [

                    ],
                    "start": bin_media.range[1].to_frame(),
                    "duration": 108001,  # This appears to be a magic constant of some sort.

                    "mediaStart": bin_media.range[1].to_frame() - 1,
                    "mediaDuration": 1,
                    "scalar": 1,
                    "animationTracks": {

                    }
                }
            ],
            "effects": [

            ],
            "start": start,
            "duration": duration,
            "mediaStart": 0,
            "mediaDuration": duration,
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
