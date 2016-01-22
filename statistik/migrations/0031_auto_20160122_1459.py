# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0030_auto_20160122_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='difficulty_spike',
            field=models.SmallIntegerField(default=0, choices=[(0, ''), (1, 'Beginning'), (2, 'Middle'), (3, 'End')]),
        ),
    ]
