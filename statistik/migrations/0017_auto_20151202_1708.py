# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0016_auto_20151201_0739'),
    ]

    operations = [
        migrations.CreateModel(
            name='EloReview',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('drawn', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='chart',
            name='elo_rating',
            field=models.FloatField(default=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eloreview',
            name='first',
            field=models.ForeignKey(related_name='eloreview_win_set', to='statistik.Chart'),
        ),
        migrations.AddField(
            model_name='eloreview',
            name='second',
            field=models.ForeignKey(related_name='eloreview_lose_set', to='statistik.Chart'),
        ),
    ]
