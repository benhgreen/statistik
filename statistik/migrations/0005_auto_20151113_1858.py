# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0004_auto_20151113_0544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='clear_rating',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(1299), django.core.validators.MinValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='exhc_rating',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(1299), django.core.validators.MinValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='hc_rating',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(1299), django.core.validators.MinValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='score_rating',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(1299), django.core.validators.MinValueValidator(100)]),
        ),
    ]
