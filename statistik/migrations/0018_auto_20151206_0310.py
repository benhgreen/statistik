# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0017_auto_20151202_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='chart',
            name='elo_rating_hc',
            field=models.FloatField(default=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eloreview',
            name='type',
            field=models.SmallIntegerField(default=0, choices=[(0, 'NC'), (1, 'HC'), (2, 'EXHC'), (3, 'SCORE')]),
            preserve_default=False,
        ),
    ]
