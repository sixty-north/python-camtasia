from camtasia.frame_stamp import FrameStamp
from camtasia.marker import Marker


class Media:
    def __init__(self, media_data, frame_rate):
        self._data = media_data
        self._frame_rate = frame_rate

    @property
    def markers(self):
        for m in self._data['parameters']['toc']['keyframes']:
            yield Marker(name=m['value'],
                         time=FrameStamp(frame_number=m['time'],
                                         frame_rate=self._frame_rate))

    @property
    def start(self):
        return FrameStamp(frame_number=self._data['start'],
                          frame_rate=self._frame_rate)

    @property
    def duration(self):
        return FrameStamp(frame_number=self._data['duration'],
                          frame_rate=self._frame_rate)

    def __repr__(self):
        return f'Media(start={self.start}, duration={self.duration})'


class Track:
    def __init__(self, attributes, data, frame_rate):
        self._attributes = attributes
        self._data = data
        self._frame_rate = frame_rate

    @property
    def name(self):
        return self._attributes['ident']

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

    def __repr__(self):
        return f'Track(name="{self.name}")'
