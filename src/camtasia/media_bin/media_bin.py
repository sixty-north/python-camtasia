import datetime
from enum import Enum
from pathlib import Path
import shutil
from typing import Iterable, Tuple

from pymediainfo import MediaInfo
from xml.etree.ElementTree import ParseError


class MediaType(Enum):
    # NB: These must match camtasia's codes for media types, i.e. as used in 'sourceBin/sourceTracks/type'.
    Video = 0
    Image = 1
    Audio = 2


class IntEncodedTime:
    """Times encoded as integers.

    Media times are sometimes reported using a special encoding where the three least significant digits represent
    milliseconds and everything else represents seconds. This class represents that encoding, and provides support for
    converting to other useful domains (e.g. frames).

    This is intentionally not interchangeable with other number types so that we don't accidentally compare it to e.g.
    time represented in frames.
    """

    def __init__(self, encoded_time):
        self._seconds, self._milliseconds = divmod(encoded_time, 1000)

    @property
    def seconds(self):
        return self._seconds

    @property
    def milliseconds(self):
        return self._milliseconds

    def to_frame(self, frame_rate=30):
        return int((self.seconds + self.milliseconds / 1000) * frame_rate)

    def __str__(self):
        return f'{self.seconds}s{self.milliseconds}ms'

    def __repr__(self):
        return f'IntEncodedTime(encoded_time={self.seconds + self.milliseconds * 1000})'


class Media:
    def __init__(self, data):
        self._data = data

    @property
    def source(self) -> Path:
        return Path(self._data['src'])

    @property
    def identity(self):
        return self.source.stem

    @property
    def type(self):
        return MediaType(self._data['sourceTracks'][0]['type'])

    @property
    def rect(self):
        return tuple(self._data['rect'])

    @property
    def range(self) -> Tuple[IntEncodedTime, IntEncodedTime]:
        """The start and stop times of the media as a `(start, stop)` tuple.

        Each tuple element is an int-encoded time where the three least significant digits represent milliseconds and
        everything else represents seconds.

        Returns: A two-tuple of `IntEncodedTime`s.
        """

        return tuple(map(IntEncodedTime, self._data['sourceTracks'][0]['range']))

    @property
    def last_modification(self):
        return datetime.datetime.strptime(
            self._data['lastMod'], '%Y%m%dT%H%M%S')

    @property
    def id(self):
        return self._data['id']

    def __repr__(self):
        return f'Media(id={self.id}, source="{self.source}")'


class MediaBin:
    """Represents the media-bin element of the UI.

    You can iterate over the MediaBin to access its invidivual Media objects.

    Args:
        data: The 'sourceBin' subdict of the overall project dict.
        root_path: Path to root directory of project.
    """

    def __init__(self, media_bin_data, root_path):
        self._data = media_bin_data
        self._root_path = root_path

    def __len__(self):
        return len(self._data)

    def __iter__(self) -> Iterable[Media]:
        """Get iterator of Media instances in this bin.
        """
        for record in self._data:
            yield Media(record)

    def __getitem__(self, media_id):
        """Get the media with the specified ID.

        Args:
            media_id: ID of the media to get.

        Returns: A Media instance.

        Raises:
            KeyError: The specified media is not contained in this MediaBin.
        """
        for media in self:
            if media.id == media_id:
                return media

        raise KeyError('No media with id {}'.format(media_id))

    def __delitem__(self, media_id):
        """Remove the specified Media from the MediaBin.

        Args:
            media_id: The ID of the media to be removed.

        Raises:
            KeyError: The specified media is not contained in this MediaBin.
        """

        for idx, record in enumerate(self._data):
            if record['id'] == media_id:
                self._data.pop(idx)
                return

        raise KeyError('No media with id{}'.format(media_id))

    def import_media(self, file_path: Path):
        """Import new media into the project.

        All imported media will be copied into a new directory under the 'media' subdirectory of the project structure.

        Args:
            file_path: Path to media to import.

        Returns: A Media instance for the newly imported media.

        Raises:
            FileExistsError: Destination media directory already exists.
            FileNotFoundError: `file_path` does not exist.
            OSError: Other errors copying file.
            ValueError: `file_path` can't be parsed as a media file.
        """

        try:
            media_info = MediaInfo.parse(file_path)
        except ParseError as e:
            raise ValueError(f'Unable to parse media file {file_path}') from e

        # Copy the file into the project's media directory
        timestamp = datetime.datetime.now()
        media_dir = self._root_path / 'media' / str(timestamp.timestamp())
        media_dir.mkdir(parents=True)
        dest = shutil.copy(file_path, media_dir)

        # find next media ID
        max_media_id = max((rec['id'] for rec in self._data), default=0)
        next_media_id = max_media_id + 1

        # TODO: The actual media info always seems to be the second element. Look into this.
        track = media_info.tracks[1].to_data()
        media_type = _get_media_type(track)

        to_json = {
            MediaType.Video: _visual_track_to_json,
            MediaType.Image: _visual_track_to_json,
            MediaType.Audio: _audio_track_to_json,
        }[media_type]

        json_data = to_json(track, next_media_id, str(
            Path(dest).relative_to(self._root_path)), timestamp)

        self._data.append(json_data)

        return self[next_media_id]


def _visual_track_to_json(track, media_id, source_file, timestamp):
    media_rect = (0, 0, track['width'], track['height'])
    return {
        "id": media_id,
        # str(Path(dest).relative_to(self._root_path)),
        "src": source_file,
        "rect": media_rect,
        "lastMod": _datetime_to_str(timestamp),
        "sourceTracks": [
            {
                "range": [0, int(track.get('duration', 1))],
                "type": _get_media_type(track).value,
                # TODO: Not sure what this is! round(float(track.get('frame_rate', 600))),
                "editRate": 1000,
                "trackRect": media_rect,
                "sampleRate": 0,
                "bitDepth": track.get('bit_depth', 0),
                "numChannels": 0,
                "integratedLUFS": 100.0,
                "peakLevel": -1.0,

                # TODO: ? This is empty for images in the examples. For movies it's a sequence of UUIDs like this.
                # "metaData": "2b7b6a01-7a1f-11e2-83d0-0017f200be7f;2b7b6af0-7a1f-11e2-83d0-0017f200be7f;2b7b6af1-7a1f-11e2-83d0-0017f200be7f;2b7b6af2-7a1f-11e2-83d0-0017f200be7f;2b7b6af3-7a1f-11e2-83d0-0017f200be7f;2b7b6af5-7a1f-11e2-83d0-0017f200be7f;2b7b6af6-7a1f-11e2-83d0-0017f200be7f;2b7b6af7-7a1f-11e2-83d0-0017f200be7f;2b7b6af8-7a1f-11e2-83d0-0017f200be7f;2b7b6af9-7a1f-11e2-83d0-0017f200be7f;2b7b6afa-7a1f-11e2-83d0-0017f200be7f;2b7b6afb-7a1f-11e2-83d0-0017f200be7f;2b7b6afc-7a1f-11e2-83d0-0017f200be7f;"
                "metaData": ""
            }
        ]
    }


def _audio_track_to_json(track, media_id, source_file, timestamp):
    return {
        "id": media_id,
        "src": source_file,
        "rect": [0, 0, 0, 0],
        "lastMod": _datetime_to_str(timestamp),
        "sourceTracks": [
            {
                "range": [0, int(track['samples_count'])],
                "type": _get_media_type(track).value,
                "editRate": track['sampling_rate'],  # TODO: Is this right?
                "trackRect": [0, 0, 0, 0],
                "sampleRate": track['sampling_rate'],
                "bitDepth": track['bit_depth'],
                "numChannels": track['channel_s'],
                "integratedLUFS": -21.8965729218104,  # TODO: No idea!
                "peakLevel": 1.0,  # TODO: No idea!
                "metaData": ""
            }
        ]
    }


def _get_media_type(track):
    "Maps a `pymediainfo.Track.kind_of_stream` to a `MediaType`."
    return {
        'Image': MediaType.Image,
        'Video': MediaType.Video,
        'Audio': MediaType.Audio,
    }[track['kind_of_stream']]


def _datetime_to_str(dt):
    """Convert datetime object to camtasia lastMod format.

    <year><month><day>T<hour><minute><second>, e.g. 20190606T103830
    """
    return f'{dt.year}{dt.month:02}{dt.day:02}T{dt.hour:02}{dt.minute:02}{dt.second:02}'


# Here's an example of the project file's media-bin format for video:

#  "sourceBin" : [
#      {
#        "id" : 1,
#        "src" : "./recordings/1559817572.462711/Rec 6-6-2019.trec",
#        "rect" : [0, 0, 5120, 2880],
#        "lastMod" : "20190606T103830",
#        "sourceTracks" : [
#          {
#            "range" : [0, 1032],
#            "type" : 0,
#            "editRate" : 30,
#            "trackRect" : [0, 0, 5120, 2880],
#            "sampleRate" : 0,
#            "bitDepth" : 0,
#            "numChannels" : 0,
#            "integratedLUFS" : 100.0,
#            "peakLevel" : -1.0,
#            "metaData" : "2b7b6a01-7a1f-11e2-83d0-0017f200be7f;2b7b6af0-7a1f-11e2-83d0-0017f200be7f;2b7b6af1-7a1f-11e2-83d0-0017f200be7f;2b7b6af2-7a1f-11e2-83d0-0017f200be7f;2b7b6af3-7a1f-11e2-83d0-0017f200be7f;2b7b6af5-7a1f-11e2-83d0-0017f200be7f;2b7b6af6-7a1f-11e2-83d0-0017f200be7f;2b7b6af7-7a1f-11e2-83d0-0017f200be7f;2b7b6af8-7a1f-11e2-83d0-0017f200be7f;2b7b6af9-7a1f-11e2-83d0-0017f200be7f;2b7b6afa-7a1f-11e2-83d0-0017f200be7f;2b7b6afb-7a1f-11e2-83d0-0017f200be7f;2b7b6afc-7a1f-11e2-83d0-0017f200be7f;"
#          }
#        ]
#      }
#    ],

# And here's an example for audio:
# "sourceBin": [
# {
#       "id" : 2,
#       "src" : "./media/1600841055.810413/example.wav",
#       "rect" : [0, 0, 0, 0],
#       "lastMod" : "20200923T060323",
#       "sourceTracks" : [
#         {
#           "range" : [0, 357210],
#           "type" : 2,
#           "editRate" : 44100,
#           "trackRect" : [0, 0, 0, 0],
#           "sampleRate" : 44100,
#           "bitDepth" : 16,
#           "numChannels" : 2,
#           "integratedLUFS" : -21.8965729218104,
#           "peakLevel" : 1.0,
#           "metaData" : ""
#         }
#       ]
#     }
# ]
