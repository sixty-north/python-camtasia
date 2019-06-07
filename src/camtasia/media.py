from camtasia.frame_stamp import FrameStamp
from camtasia.marker import Marker


class Media:
    def __init__(self, media_data, frame_rate):
        self._data = media_data
        self._frame_rate = frame_rate

    @property
    def markers(self):
        for m in self._data['parameters']['toc']['keyframes']:
            marker_offset = FrameStamp(frame_number=m['time'],
                                       frame_rate=self._frame_rate)

            # The frame-stamps for media markers are stored relative to the media-start of the media, so we have to add
            # media-start to the marker time to get the actual marker time.
            print(marker_offset + self.media_start)
            yield Marker(name=m['value'],
                         time=self.start + (marker_offset - self.media_start))

    @property
    def start(self):
        "Where the media visible starts on the timeline."
        return FrameStamp(frame_number=self._data['start'],
                          frame_rate=self._frame_rate)

    @property
    def media_start(self):
        "The offset into the underlying media at which the media starts."
        return FrameStamp(frame_number=self._data['mediaStart'],
                          frame_rate=self._frame_rate)

    @property
    def duration(self):
        return FrameStamp(frame_number=self._data['duration'],
                          frame_rate=self._frame_rate)

    def __repr__(self):
        return f'Media(start={self.start}, duration={self.duration})'
