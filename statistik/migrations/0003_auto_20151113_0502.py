# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('statistik', '0002_auto_20151113_0255'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('clear_rating', models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(0)])),
                ('hc_rating', models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(0)])),
                ('exhc_rating', models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(0)])),
                ('score_rating', models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(0)])),
                ('characteristics', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(choices=[(0, 'Scratching'), (1, 'Jacks'), (2, 'Speed Changes'), (3, 'Charge Notes'), (4, 'Scales'), (5, 'Chord Scales'), (6, 'Denim')]), size=None)),
                ('chart', models.ForeignKey(to='statistik.Chart')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='song',
            name='game_version',
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set([('chart', 'user')]),
        ),
    ]
