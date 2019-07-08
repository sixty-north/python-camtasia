import datetime
from pathlib import Path
import shutil
from typing import Iterable

from pymediainfo import MediaInfo
from xml.etree.ElementTree import ParseError


class Media:
    def __init__(self, data):
        self._data = data

    @property
    def source(self):
        return Path(self._data['src'])

    @property
    def rect(self):
        return tuple(self._data['rect'])

    @property
    def last_modification(self):
        return datetime.datetime.strptime(
            self._data['lastMod'], '%Y%m%dT%H%M%S')

    def __repr__(self):
        return f'Media(source="{self.source}")'


class MediaBin:
    """Represents the media-bin element of the UI.

    Args:
        data: The 'sourceBin' subdict of the overall project dict.
        root_path: Path to root directory of project.
    """

    def __init__(self, media_bin_data, root_path):
        self._data = media_bin_data
        self._root_path = root_path

    @property
    def media(self) -> Iterable[Media]:
        for record in self._data:
            yield Media(record)

    def import_media(self, file_path: Path):
        """Import new media into the project.

        All imported media will be copied into a new directory under the 'media' subdirectory of the project structure.

        Args: 
            file_path: Path to media to import.

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
        media_rect = (0, 0, track['width'], track['height'])

        # Update the project data
        self._data.append({
            "id": next_media_id,
            "src": str(Path(dest).relative_to(self._root_path)),
            "rect": media_rect,
            "lastMod": _datetime_to_str(timestamp),
            "sourceTracks": [
                {
                    "range": [0, int(track.get('frame_count', 1))],
                    "type": _get_media_type(track),
                    "editRate": round(float(track.get('frame_rate', 600))),
                    "trackRect": media_rect,
                    "sampleRate": 0,
                    "bitDepth": track.get('bit_depth', 0),
                    "numChannels": 0,
                    "integratedLUFS": 100.0,
                    "peakLevel": -1.0,

                    # TODO: ? This is empty to images in the examples. For movies it's a sequence of UUIDs like this.
                    # "metaData": "2b7b6a01-7a1f-11e2-83d0-0017f200be7f;2b7b6af0-7a1f-11e2-83d0-0017f200be7f;2b7b6af1-7a1f-11e2-83d0-0017f200be7f;2b7b6af2-7a1f-11e2-83d0-0017f200be7f;2b7b6af3-7a1f-11e2-83d0-0017f200be7f;2b7b6af5-7a1f-11e2-83d0-0017f200be7f;2b7b6af6-7a1f-11e2-83d0-0017f200be7f;2b7b6af7-7a1f-11e2-83d0-0017f200be7f;2b7b6af8-7a1f-11e2-83d0-0017f200be7f;2b7b6af9-7a1f-11e2-83d0-0017f200be7f;2b7b6afa-7a1f-11e2-83d0-0017f200be7f;2b7b6afb-7a1f-11e2-83d0-0017f200be7f;2b7b6afc-7a1f-11e2-83d0-0017f200be7f;"
                    "metaData": ""
                }
            ]
        })


def _get_media_type(track):
    "Maps a track's kind-of-stram to a Camtasia media type."
    return {
        'Image': 1,
        'Movie': 0,
    }[track['kind_of_stream']]


def _datetime_to_str(dt):
    """Convert datetime object to camtasia lastMod format.

    <year><month><day>T<hour><minute><second>, e.g. 20190606T103830
    """
    return f'{dt.year}{dt.month:02}{dt.day:02}T{dt.hour:02}{dt.minute:02}{dt.second:02}'


# Here's an example of the project file's media-bin format:

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

