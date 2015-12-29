# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0022_eloreview_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='clickagain_hc',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='chart',
            name='clickagain_nc',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='eloreview',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='characteristics',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(choices=[(0, 'Scratching'), (1, 'Jacks'), (2, 'Speed Changes'), (3, 'Charge Notes'), (4, 'Scales'), (5, 'Chord Scales'), (6, 'Denim'), (7, 'Trills'), (8, 'Rolls'), (9, 'Chords')]), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='review',
            name='recommended_options',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(choices=[(0, 'Regular'), (1, 'Random'), (2, 'S-Random'), (3, 'R-Random'), (4, 'Mirror'), (5, 'Flip'), (6, 'Regular Left'), (7, 'Random Left'), (8, 'S-Random Left'), (9, 'R-Random Left'), (10, 'Mirror Left'), (11, 'Regular Right'), (12, 'Random Right'), (13, 'S-Random Right'), (14, 'R-Random Right'), (15, 'Mirror Right')]), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='song',
            name='title',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='best_techniques',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(choices=[(0, 'Scratching'), (1, 'Jacks'), (2, 'Speed Changes'), (3, 'Charge Notes'), (4, 'Scales'), (5, 'Chord Scales'), (6, 'Denim'), (7, 'Trills'), (8, 'Rolls'), (9, 'Chords')]), size=3),
        ),
    ]
