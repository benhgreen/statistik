from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from statistik.constants import (CHART_TYPE_CHOICES,
                                 TECHNIQUE_CHOICES, VERSION_CHOICES, PLAYSIDE_CHOICES,
                                 RECOMMENDED_OPTIONS_CHOICES,
                                 RATING_VALIDATORS, SCORE_CATEGORY_CHOICES,
                                 DIFFICULTY_SPIKE_CHOICES)


class Song(models.Model):
    music_id = models.IntegerField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=64)
    alt_title = models.CharField(max_length=64, null=True, blank=True)
    artist = models.CharField(max_length=64)
    alt_artist = models.CharField(max_length=64, null=True, blank=True)
    genre = models.CharField(max_length=64)
    bpm_min = models.SmallIntegerField()
    bpm_max = models.SmallIntegerField()
    game_version = models.SmallIntegerField(choices=VERSION_CHOICES)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Chart(models.Model):
    song = models.ForeignKey(Song)
    type = models.SmallIntegerField(choices=CHART_TYPE_CHOICES)
    difficulty = models.SmallIntegerField(validators=[
        MaxValueValidator(12),
        MinValueValidator(1)
    ])
    note_count = models.SmallIntegerField(null=True)
    elo_rating = models.FloatField(default=1000)
    elo_rating_hc = models.FloatField(default=1000)

    clickagain_nc = models.FloatField(blank=True, null=True)
    clickagain_hc = models.FloatField(blank=True, null=True)

    def __str__(self):
        return "%s [%s]" % (self.song_id, self.get_type_display())

    class Meta:
        unique_together = ('song', 'type')


class EloReview(models.Model):
    first = models.ForeignKey(Chart, related_name='eloreview_win_set')
    second = models.ForeignKey(Chart, related_name='eloreview_lose_set')
    drawn = models.BooleanField()
    created_at = models.DateTimeField(auto_now=True)
    type = models.SmallIntegerField(choices=SCORE_CATEGORY_CHOICES)
    created_by = models.ForeignKey(User, null=True)


class Review(models.Model):
    chart = models.ForeignKey(Chart)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=256, blank=True)
    clear_rating = models.FloatField(null=True,
                                     validators=RATING_VALIDATORS)
    hc_rating = models.FloatField(null=True,
                                  validators=RATING_VALIDATORS)
    exhc_rating = models.FloatField(null=True,
                                    validators=RATING_VALIDATORS)
    score_rating = models.FloatField(null=True,
                                     validators=RATING_VALIDATORS)
    difficulty_spike = models.SmallIntegerField(default=0,
                                                choices=DIFFICULTY_SPIKE_CHOICES)
    characteristics = ArrayField(
        models.IntegerField(choices=TECHNIQUE_CHOICES), null=True)
    recommended_options = ArrayField(models.IntegerField(
        choices=RECOMMENDED_OPTIONS_CHOICES), null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Review %s:%s' % (self.user_id, self.chart_id)

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

    def __str__(self):
        return 'DJ %s' % self.dj_name
