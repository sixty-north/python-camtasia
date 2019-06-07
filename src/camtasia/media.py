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

