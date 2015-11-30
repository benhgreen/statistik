# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0008_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='game_version',
            field=models.SmallIntegerField(default=None),
            preserve_default=False,
        ),
    ]
