import datetime
from pathlib import Path
from typing import Iterable

# "sourceBin" : [
#     {
#       "id" : 1,
#       "src" : "./recordings/1559817572.462711/Rec 6-6-2019.trec",
#       "rect" : [0, 0, 5120, 2880],
#       "lastMod" : "20190606T103830",
#       "sourceTracks" : [
#         {
#           "range" : [0, 1032],
#           "type" : 0,
#           "editRate" : 30,
#           "trackRect" : [0, 0, 5120, 2880],
#           "sampleRate" : 0,
#           "bitDepth" : 0,
#           "numChannels" : 0,
#           "integratedLUFS" : 100.0,
#           "peakLevel" : -1.0,
#           "metaData" : "2b7b6a01-7a1f-11e2-83d0-0017f200be7f;2b7b6af0-7a1f-11e2-83d0-0017f200be7f;2b7b6af1-7a1f-11e2-83d0-0017f200be7f;2b7b6af2-7a1f-11e2-83d0-0017f200be7f;2b7b6af3-7a1f-11e2-83d0-0017f200be7f;2b7b6af5-7a1f-11e2-83d0-0017f200be7f;2b7b6af6-7a1f-11e2-83d0-0017f200be7f;2b7b6af7-7a1f-11e2-83d0-0017f200be7f;2b7b6af8-7a1f-11e2-83d0-0017f200be7f;2b7b6af9-7a1f-11e2-83d0-0017f200be7f;2b7b6afa-7a1f-11e2-83d0-0017f200be7f;2b7b6afb-7a1f-11e2-83d0-0017f200be7f;2b7b6afc-7a1f-11e2-83d0-0017f200be7f;"
#         }
#       ]
#     }
#   ],


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
    """
    def __init__(self, media_bin_data):
        self._data = media_bin_data

    @property
    def media(self) -> Iterable[Media]:
        for record in self._data:
            yield Media(record)
