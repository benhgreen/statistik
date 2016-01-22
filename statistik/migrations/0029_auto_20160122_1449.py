# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0028_auto_20151230_2221'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='song',
            options={'ordering': ['title']},
        ),
        migrations.AddField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 1, 22, 14, 49, 33, 718769)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='difficulty_spike',
            field=models.SmallIntegerField(null=True, choices=[(0, ''), (1, 'Beginning'), (2, 'Middle'), (3, 'End')]),
        ),
    ]
