# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0029_auto_20160122_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='difficulty_spike',
            field=models.SmallIntegerField(choices=[(0, 'None'), (1, 'Beginning'), (2, 'Middle'), (3, 'End')], null=True),
        ),
    ]
