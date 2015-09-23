# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import daddie.apps.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150916_1357'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='build',
            unique_together=set([('product', 'created')]),
        ),
        migrations.AlterUniqueTogether(
            name='dependency',
            unique_together=set([('package', 'content_type', 'object_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='deployment',
            unique_together=set([('environment', 'build', 'created')]),
        ),
        migrations.AlterUniqueTogether(
            name='package',
            unique_together=set([('name', 'version')]),
        ),
        migrations.RemoveField(
            model_name='deployment',
            name='product',
        ),
    ]
