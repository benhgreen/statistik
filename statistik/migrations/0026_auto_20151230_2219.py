# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0025_auto_20151230_0438'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='music_id',
            new_name='id',
        ),
    ]
