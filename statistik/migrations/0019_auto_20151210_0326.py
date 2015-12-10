# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0018_auto_20151206_0310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='elo_rating',
            field=models.FloatField(default=1000),
        ),
        migrations.AlterField(
            model_name='chart',
            name='elo_rating_hc',
            field=models.FloatField(default=1000),
        ),
    ]
