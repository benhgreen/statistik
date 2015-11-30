# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0005_auto_20151113_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='clear_rating',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(129), django.core.validators.MinValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='exhc_rating',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(129), django.core.validators.MinValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='hc_rating',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(129), django.core.validators.MinValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='score_rating',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(129), django.core.validators.MinValueValidator(10)]),
        ),
    ]
