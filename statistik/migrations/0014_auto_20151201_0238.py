# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0013_auto_20151130_0632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='clear_rating',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(12.9), django.core.validators.MinValueValidator(1.0)], null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='exhc_rating',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(12.9), django.core.validators.MinValueValidator(1.0)], null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='hc_rating',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(12.9), django.core.validators.MinValueValidator(1.0)], null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='score_rating',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(12.9), django.core.validators.MinValueValidator(1.0)], null=True),
        ),
    ]
