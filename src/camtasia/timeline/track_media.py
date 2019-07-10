from ..frame_stamp import FrameStamp
from .marker import Marker


class TrackMedia:
    """Individual media elements on a track on the timeline.

    The relationship between the underlying media and that visible on the timeline on the timeline is a bit involved:

        v--media-start--v
        -------------------------------------------------------
        | underlying media                                    |
        -------------------------------------------------------
                        |---- visible part of media ----|
                        |                               |
    v--start------------v                               v
    -------------------------------------------------------------------------------
    |  timeline                                                                   |
    -------------------------------------------------------------------------------

    So `media-start` is the offset into the full, underlying media where the visble part starts.

    `start` is the offset into the *timeline* where the visible part starts.

    Media marker timestamps are calculated from the start of the underlying media. So in order to calculate the
    timeline-relative timestamp for a media marker you need to take `start`, `media-start`, and the marker's timestamp
    into account::

        start + (marker_time - media_start)
    """
    def __init__(self, media_data, frame_rate):
        self._data = media_data
        self._frame_rate = frame_rate

    @property
    def markers(self):
        # Keyframes may not exist when e.g. the media has no markers
        keyframes = self._data.get('parameters', {}).get('toc', {}).get('keyframes', ())

        for m in keyframes:
            marker_offset = FrameStamp(frame_number=m['time'],
                                       frame_rate=self._frame_rate)

            yield Marker(name=m['value'],
                         time=self.start + (marker_offset - self.media_start))

    @property
    def start(self):
        "The offset on the timeline at which the visible media starts."
        return FrameStamp(frame_number=self._data['start'],
                          frame_rate=self._frame_rate)

    @property
    def media_start(self):
        "The offset into the underlying media at which the visible media starts."
        return FrameStamp(frame_number=self._data['mediaStart'],
                          frame_rate=self._frame_rate)

    @property
    def duration(self):
        return FrameStamp(frame_number=self._data['duration'],
                          frame_rate=self._frame_rate)

    @property
    def source(self):
        """ID of the media-bin source for this media.
        """
        return self._data['src']

    def __repr__(self):
        return f'Media(start={self.start}, duration={self.duration})'
