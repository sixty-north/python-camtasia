from itertools import islice

from camtasia.timeline.marker import Marker


class TestTimelineTracks:
    def test_timeline_initially_has_two_tracks(self, project):
        assert len(project.timeline.tracks) == 2

    def test_iteration(self, project):
        tracks = list(project.timeline.tracks)
        assert len(tracks) == 2

    def test_insert_adds_track(self, project):
        track = project.timeline.tracks.insert_track(2, 'test-track')
        assert len(project.timeline.tracks) == 3
        assert track.name == 'test-track'

    def test_get_track_by_index(self, project):
        project.timeline.tracks.insert_track(2, 'test-track')
        track = project.timeline.tracks[2]
        assert track.name == 'test-track'

    def test_delete_track_removes_track(self, project):
        project.timeline.tracks.insert_track(2, 'test-track')
        del project.timeline.tracks[2]
        assert len(project.timeline.tracks) == 2


class TestTimelineMarkers:
    def test_timeline_initially_has_no_markers(self, project):
        assert len(list(project.timeline.markers)) == 0


class TestCannedTimeline:
    def test_number_tracks(self, simple_video):
        assert len(list(simple_video.timeline.tracks)) == 1

    def test_first_track(self, simple_video):
        track = next(islice(simple_video.timeline.tracks, 1))
        assert track.name == 'populated-track'
        assert not track.audio_muted
        assert not track.video_hidden

    def test_first_track_medias(self, simple_video):
        track = next(islice(simple_video.timeline.tracks, 1))
        media = next(islice(track.medias, 1))
        markers = sorted(media.markers, key=lambda x: x.time)
        assert markers == [
            Marker(time=60, name='media-marker-1'),
            Marker(time=120, name='media-marker-2'),
        ]

    def test_second_media_markers_are_empty(self, simple_video):
        track = next(islice(simple_video.timeline.tracks, 1))
        media = next(islice(track.medias, 1, 2))
        markers = list(media.markers)
        assert markers == []

    def test_timeline_markers(self, simple_video):
        markers = sorted(simple_video.timeline.markers, key=lambda x: x.time)
        assert markers == [
            Marker(time=150, name='marker-1'),
            Marker(time=300, name='marker-2'),
            Marker(time=450, name='marker-3'),
            Marker(time=600, name='marker-4'),
            Marker(time=750, name='marker-5'),
            Marker(time=900, name='marker-6'),
        ]
