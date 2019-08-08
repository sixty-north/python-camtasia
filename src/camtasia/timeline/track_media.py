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
    def __init__(self, media_data):
        self._data = media_data

    @property
    def id(self):
        """ID of the media entry on the track."""
        return self._data['id']

    @property
    def markers(self):
        # Keyframes may not exist when e.g. the media has no markers
        keyframes = self._data.get('parameters', {}).get('toc', {}).get('keyframes', ())

        for m in keyframes:
            marker_offset = m['time']

            yield Marker(name=m['value'],
                         time=self.start + (marker_offset - self.media_start))

    @property
    def start(self):
        "The offset (in frames) on the timeline at which the visible media starts."
        return self._data['start']

    @property
    def media_start(self):
        "The offset (in frames) into the underlying media at which the visible media starts."
        return self._data['mediaStart']

    @property
    def duration(self):
        "The duration (in frames) of the media on the timeline."
        return self._data['duration']

    @property
    def source(self):
        """ID of the media-bin source for this media.

        If media does not have a presence in the media-bin (e.g. if it's an annotation), this
        will be None.
        """
        return self._data.get('src', None)

    def __repr__(self):
        return f'Media(start={self.start}, duration={self.duration})'
