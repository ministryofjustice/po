# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0004_auto_20150917_1437'),
    ]

    operations = [
        migrations.RenameField(
            model_name='repository',
            old_name='collaborators',
            new_name='contributors',
        ),
    ]
