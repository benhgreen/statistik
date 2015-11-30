# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0012_auto_20151130_0227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='clear_rating',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(12.9), django.core.validators.MinValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='exhc_rating',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(12.9), django.core.validators.MinValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='hc_rating',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(12.9), django.core.validators.MinValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='score_rating',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(12.9), django.core.validators.MinValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='song',
            name='game_version',
            field=models.SmallIntegerField(choices=[(1, '1st'), (2, '2nd'), (3, '3rd'), (4, '4th'), (5, '5th'), (6, '6th'), (7, '7th'), (8, '8th'), (9, '9th'), (10, '10th'), (11, 'RED'), (12, 'HS'), (13, 'DD'), (14, 'GO'), (15, 'DJT'), (16, 'EMP'), (17, 'SIR'), (18, 'RA'), (19, 'LIN'), (20, 'TRI'), (21, 'SPD'), (22, 'PEN'), (23, 'COP')]),
        ),
    ]
