from django.test import TestCase
from unittest import skip
from statistik.controller import (get_charts_by_ids, get_charts_by_query,
                                  create_new_user, get_chart_data)
from statistik.models import Song, Chart, Review

SAMPLE_SONG_DATA = [{
    'music_id': 1,
    'title': 'Boys Like You',
    'artist': 'Who Is Fancy',
    'genre': 'Pop',
    'bpm_min': 120,
    'bpm_max': 120,
    'game_version': 1
}, {
    'music_id': 2,
    'title': 'Gangster Trippin',
    'artist': 'Fatboy Slim',
    'genre': 'Pop',
    'bpm_min': 120,
    'bpm_max': 120,
    'game_version': 1
}]

SAMPLE_USER_DATA = [{
    'username': 'ben',
    'password': 'lel',
    'dj_name': 'blarg',
    'playside': 0,
    'best_techniques': [],
    'location': 'USA'
},{
    'username': 'jimwich',
    'password': 'asdfasdf',
    'dj_name': 'fdsaa',
    'playside': 1,
    'best_techniques': [],
    'location': 'USA'
}]

SAMPLE_REVIEW_DATA = [{
    'text': 'afdklj',
    'clear_rating': 1.0,
    'hc_rating': 2.0,
    'exhc_rating': 3.0,
    'score_rating': 4.0,
    'characteristics': [0, 1],
    'recommended_options': []

},{
    'text': 'asdfsadfdsf',
    'clear_rating': 1.5,
    'hc_rating': 3.0,
    'exhc_rating': 4.0,
    'score_rating': 0.0,
    'characteristics': [0, 1],
    'recommended_options': []

}]


def create_some_songs():
    return [Song.objects.create(**song_data) for song_data in SAMPLE_SONG_DATA]

def create_some_charts(songs):
        return [Chart.objects.create(song=song,
                                     type=0,
                                     difficulty=1,
                                     note_count=0)
                for song in songs]


def create_some_users():
    return [create_new_user(user_data) for user_data in SAMPLE_USER_DATA]


def create_some_reviews(charts, users):
    return [Review.objects.create(chart=charts[0],
                                  user=users[x],
                                  **review_data)
            for x, review_data in enumerate(SAMPLE_REVIEW_DATA)]

# TODO: Fix or get rid of these tests as they're currently failing
@skip("These tests are broken...please fix or remove me :(")
class SongTests(TestCase):
    def setUp(self):
        self.songs = create_some_songs()
        self.charts = create_some_charts(self.songs)
        self.users = create_some_users()
        self.reviews = create_some_reviews(self.charts, self.users)

    def test_get_charts(self):
        """
        Test filtering charts by id and query
        """
        r = get_charts_by_ids([1, 2])
        self.assertEqual(len(r), 2)

        r = get_charts_by_query(version=1)
        self.assertEqual(len(r), 2)

        r = get_charts_by_query(version=1, difficulty=10)
        self.assertEqual(len(r), 0)

        r = get_charts_by_query(version=1, play_style='DP')
        self.assertEqual(len(r), 0)


    def test_get_chart_data(self):
        """
        Test review averaging and organizing
        """
        chart_data = get_chart_data(difficulty=1, user=self.users[0])
        self.assertEqual(len(chart_data), 2)

        song1 = chart_data[0]
        self.assertEqual(song1.get('title'), SAMPLE_SONG_DATA[0].get('title'))
        self.assertEqual(song1.get('id'), SAMPLE_SONG_DATA[0].get('music_id'))
        self.assertEqual(song1.get('avg_clear_rating'), 1.2)
        self.assertEqual(song1.get('avg_hc_rating'), 2.5)
        self.assertEqual(song1.get('avg_exhc_rating'), 3.5)
        self.assertEqual(song1.get('avg_score_rating'), 2.0)
        self.assertIsNone(song1.get('has_reviewed'))

        song2 = chart_data[1]
        self.assertEqual(song2.get('title'), SAMPLE_SONG_DATA[1].get('title'))
        self.assertEqual(song2.get('id'), SAMPLE_SONG_DATA[1].get('music_id'))
        self.assertIsNone(song2.get('avg_clear_rating'))
        self.assertIsNone(song2.get('has_reviewed'))
