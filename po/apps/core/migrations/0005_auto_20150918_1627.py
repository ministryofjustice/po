# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import po.apps.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150918_1548'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='package',
            options={'select_on_save': True},
        ),
        migrations.AlterField(
            model_name='package',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterUniqueTogether(
            name='package',
            unique_together=set([('name', 'version', 'source')]),
        ),
    ]
