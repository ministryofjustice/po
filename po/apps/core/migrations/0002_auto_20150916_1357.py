# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='build',
            name='dependencies',
        ),
        migrations.RemoveField(
            model_name='dependency',
            name='build',
        ),
        migrations.AddField(
            model_name='dependency',
            name='content_type',
            field=models.ForeignKey(default=None, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dependency',
            name='object_id',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
    ]
