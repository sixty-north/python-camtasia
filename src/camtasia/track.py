from camtasia.media import Media


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
