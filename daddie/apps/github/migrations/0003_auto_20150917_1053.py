# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0002_auto_20150917_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='collaborators',
            field=models.IntegerField(default=1, editable=False),
        ),
        migrations.AddField(
            model_name='repository',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 17, 10, 53, 12, 84623, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='repository',
            name='description',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AddField(
            model_name='repository',
            name='private',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='repository',
            name='updated',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='repository',
            name='url',
            field=models.CharField(default='', max_length=255, editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='repository',
            name='name',
            field=models.CharField(max_length=100, editable=False),
        ),
    ]
