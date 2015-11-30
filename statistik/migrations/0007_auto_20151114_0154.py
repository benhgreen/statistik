# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0006_auto_20151114_0029'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='recommended_options',
            field=django.contrib.postgres.fields.ArrayField(null=True, size=None, base_field=models.IntegerField(choices=[(0, 'Regular'), (1, 'Random'), (2, 'S-Random'), (3, 'R-Random'), (4, 'Mirror')])),
        ),
        migrations.AddField(
            model_name='review',
            name='text',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='review',
            name='characteristics',
            field=django.contrib.postgres.fields.ArrayField(null=True, size=None, base_field=models.IntegerField(choices=[(0, 'Scratching'), (1, 'Jacks'), (2, 'Speed Changes'), (3, 'Charge Notes'), (4, 'Scales'), (5, 'Chord Scales'), (6, 'Denim')])),
        ),
    ]
