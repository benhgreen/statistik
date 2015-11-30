# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0003_auto_20151113_0502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='difficulty',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)]),
        ),
    ]
