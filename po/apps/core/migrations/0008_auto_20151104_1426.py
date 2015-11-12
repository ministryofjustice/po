# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20151028_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='version',
            field=core.models.VersionField(),
        ),
        migrations.AlterField(
            model_name='package',
            name='version_major',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='version_minor',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='version_patch',
            field=models.IntegerField(null=True),
        ),
    ]
