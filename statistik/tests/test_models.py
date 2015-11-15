from django.contrib.auth.models import User
from django.test import TestCase
from statistik.models import Review, Chart, Song

TEST_USER = User()

TEST_SONG = Song(
    music_id=420,
    title='Invoker',
    artist='Caladborg',
    genre='TRIBE CORE',
    bpm_min=195,
    bpm_max=195
)

TEST_CHART = Chart(
    song=TEST_SONG,
    type=5,
    difficulty=12,
    note_count=1212
)

TEST_REVIEWS = [Review(
    user_id=x,
    chart_id=1,
    clear_rating=120 + x,
    hc_rating=110 + x,
    exhc_rating=100 + x,
    score_rating=90 + x,
    text='lel'
    ) for x in range(1, 5)]

class ModelsTest(TestCase):
    def setUp(self):
        self.user = TEST_USER
        self.song = TEST_SONG
        self.chart = TEST_CHART
        self.reviews = TEST_REVIEWS

        self.user.save()
        self.song.save()
        self.chart.save()
        for review in TEST_REVIEWS:
            review.save()


    def test_averages(self):
        self.assertEqual(self.chart.avg_clear_rating, 12.25)
        self.assertEqual(self.chart.avg_hc_rating, 11.25)
        self.assertEqual(self.chart.avg_exhc_rating, 10.25)
        self.assertEqual((self.chart.avg_score_rating, 9.25))

