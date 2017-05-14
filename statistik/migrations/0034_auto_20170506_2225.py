# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistik', '0033_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='game',
            field=models.SmallIntegerField(null=True, choices=[(0, 'IIDX'), (1, 'DDR')]),
        ),
        migrations.AlterField(
            model_name='chart',
            name='type',
            field=models.SmallIntegerField(choices=[(0, 'SPN'), (1, 'SPH'), (2, 'SPA'), (3, 'DPN'), (4, 'DPH'), (5, 'DPA'), (100, 'BEG'), (101, 'BSP'), (102, 'DSP'), (103, 'ESP'), (104, 'CSP'), (105, 'BDP'), (106, 'DDP'), (107, 'EDP'), (108, 'CDP')]),
        ),
        migrations.AlterField(
            model_name='song',
            name='game_version',
            field=models.SmallIntegerField(choices=[(1, '1st'), (2, '2nd'), (3, '3rd'), (4, '4th'), (5, '5th'), (6, '6th'), (7, '7th'), (8, '8th'), (9, '9th'), (10, '10th'), (11, 'RED'), (12, 'HS'), (13, 'DD'), (14, 'GO'), (15, 'DJT'), (16, 'EMP'), (17, 'SIR'), (18, 'RA'), (19, 'LIN'), (20, 'TRI'), (21, 'SPD'), (22, 'PEN'), (23, 'COP'), (24, 'SIN'), (101, '1st'), (102, '2nd'), (103, '3rd'), (104, '4th'), (105, '5th'), (106, 'MAX'), (107, 'MAX2'), (108, 'EXT'), (109, 'SN'), (110, 'SN2'), (111, 'X'), (112, 'X2'), (113, 'X3'), (114, '2013'), (115, '2014'), (116, 'A')]),
        ),
    ]
