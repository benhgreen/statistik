# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0031_auto_20160122_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='note_count',
            field=models.SmallIntegerField(null=True),
        ),
    ]
