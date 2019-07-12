class TestTrack:
    def test_track_name(self, project):
        project.timeline.tracks.insert_track(2, 'test-track')
        track = project.timeline.tracks[2]
        assert track.name == 'test-track'

    def test_track_index(self, project):
        project.timeline.tracks.insert_track(2, 'test-track')
        track = project.timeline.tracks[2]
        assert track.index == 2

    def test_track_audio_muted(self, project):
        project.timeline.tracks.insert_track(2, 'test-track')
        track = project.timeline.tracks[2]
        assert track.audio_muted == False

    def test_track_video_hidden(self, project):
        project.timeline.tracks.insert_track(2, 'test-track')
        track = project.timeline.tracks[2]
        assert track.video_hidden == False

    def test_initially_has_no_medias(self, project):
        project.timeline.tracks.insert_track(2, 'test-track')
        track = project.timeline.tracks[2]
        assert len(track.medias) == 0


