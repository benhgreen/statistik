import statistics
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.utils.functional import cached_property
from statistik.constants import (MAX_RATING, CHART_TYPE_CHOICES,
                                 TECHNIQUE_CHOICES, MIN_RATING,
                                 VERSION_CHOICES, PLAYSIDE_CHOICES,
                                 RECOMMENDED_OPTIONS_CHOICES)


class Song(models.Model):
    music_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=64, unique=True)
    alt_title = models.CharField(max_length=64, null=True)
    artist = models.CharField(max_length=64)
    alt_artist = models.CharField(max_length=64, null=True)
    genre = models.CharField(max_length=64)
    bpm_min = models.SmallIntegerField()
    bpm_max = models.SmallIntegerField()
    game_version = models.SmallIntegerField(choices=VERSION_CHOICES)


class Chart(models.Model):
    song = models.ForeignKey(Song)
    type = models.SmallIntegerField(choices=CHART_TYPE_CHOICES)
    difficulty = models.SmallIntegerField(validators=[
        MaxValueValidator(12),
        MinValueValidator(1)
    ])
    note_count = models.SmallIntegerField()

    class Meta:
        unique_together = ('song', 'type')


class Review(models.Model):
    chart = models.ForeignKey(Chart)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=256, blank=True)
    clear_rating = models.FloatField(null=True,
                                     validators=[
                                         MaxValueValidator(MAX_RATING),
                                         MinValueValidator(MIN_RATING)
                                     ])
    hc_rating = models.FloatField(null=True,
                                  validators=[
                                      MaxValueValidator(MAX_RATING),
                                      MinValueValidator(MIN_RATING)
                                  ])
    exhc_rating = models.FloatField(null=True,
                                    validators=[
                                        MaxValueValidator(MAX_RATING),
                                        MinValueValidator(MIN_RATING)
                                    ])
    score_rating = models.FloatField(null=True,
                                     validators=[
                                         MaxValueValidator(MAX_RATING),
                                         MinValueValidator(MIN_RATING)
                                     ])
    characteristics = ArrayField(
        models.IntegerField(choices=TECHNIQUE_CHOICES), null=True)
    recommended_options = ArrayField(models.IntegerField(
        choices=RECOMMENDED_OPTIONS_CHOICES), null=True)

    class Meta:
        unique_together = ('chart', 'user')


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    dj_name = models.CharField(max_length=6)
    location = models.CharField(max_length=64)
    play_side = models.SmallIntegerField(choices=PLAYSIDE_CHOICES)
    best_techniques = ArrayField(
        models.IntegerField(choices=TECHNIQUE_CHOICES), size=3)
    max_reviewable = models.SmallIntegerField(validators=[
        MaxValueValidator(12),
        MinValueValidator(0)
    ])
