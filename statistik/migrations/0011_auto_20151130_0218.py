# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0010_auto_20151128_0422'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='location',
            field=models.CharField(default='USA', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='play_side',
            field=models.SmallIntegerField(default=0, choices=[(0, '1P'), (1, '2P')]),
            preserve_default=False,
        ),
    ]
