from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.utils.functional import cached_property

MAX_RATING = 129
MIN_RATING = 10


class Song(models.Model):
    music_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=64, unique=True)
    alt_title = models.CharField(max_length=64, null=True)
    artist = models.CharField(max_length=64)
    alt_artist = models.CharField(max_length=64, null=True)
    genre = models.CharField(max_length=64)
    bpm_min = models.SmallIntegerField()
    bpm_max = models.SmallIntegerField()

    @property
    def game_version(self):
        return self.music_id // 1000


class Chart(models.Model):
    song = models.ForeignKey(Song)
    type = models.SmallIntegerField(choices=[
        (0, 'SPN'),
        (1, 'SPH'),
        (2, 'SPA'),
        (3, 'DPN'),
        (4, 'DPH'),
        (5, 'DPA')
    ])
    difficulty = models.SmallIntegerField(validators=[
        MaxValueValidator(12),
        MinValueValidator(1)
    ])
    note_count = models.SmallIntegerField()

    class Meta:
        unique_together = ('song', 'type')

    @cached_property
    def avg_ratings(self):
        matched_reviews = Review.objects.filter(chart=self)
        ratings = {}
        for rating_type in ['clear_rating', 'hc_rating', 'exhc_rating',
                            'score_rating']:
            ratings = {**ratings,
                       **matched_reviews.aggregate(Avg(rating_type))}

        for (k, v) in ratings.items():
            ratings[k] = round(v/10, 2)
        print(ratings)
        return ratings

    @property
    def avg_clear_rating(self):
        return self.avg_ratings.get('clear_rating__avg')

    @property
    def avg_hc_rating(self):
        return self.avg_ratings.get('hc_rating__avg')

    @property
    def avg_exhc_rating(self):
        return self.avg_ratings.get('exhc_rating__avg')

    @property
    def avg_score_rating(self):
        return self.avg_ratings.get('score_rating__avg')


class Review(models.Model):
    chart = models.ForeignKey(Chart)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=256, blank=True)
    clear_rating = models.SmallIntegerField(validators=[
        MaxValueValidator(MAX_RATING),
        MinValueValidator(MIN_RATING)
    ])
    hc_rating = models.SmallIntegerField(validators=[
        MaxValueValidator(MAX_RATING),
        MinValueValidator(MIN_RATING)
    ])
    exhc_rating = models.SmallIntegerField(validators=[
        MaxValueValidator(MAX_RATING),
        MinValueValidator(MIN_RATING)
    ])
    score_rating = models.SmallIntegerField(validators=[
        MaxValueValidator(MAX_RATING),
        MinValueValidator(MIN_RATING)
    ])
    characteristics = ArrayField(models.IntegerField(choices=[
        (0, 'Scratching'),
        (1, 'Jacks'),
        (2, 'Speed Changes'),
        (3, 'Charge Notes'),
        (4, 'Scales'),
        (5, 'Chord Scales'),
        (6, 'Denim')
    ]), null=True)
    recommended_options = ArrayField(models.IntegerField(choices=[
        (0, 'Regular'),
        (1, 'Random'),
        (2, 'S-Random'),
        (3, 'R-Random'),
        (4, 'Mirror')
    ]), null=True)

    class Meta:
        unique_together = ('chart', 'user')
