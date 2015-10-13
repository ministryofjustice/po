# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150916_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='LanguageUsage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_bytes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('products', models.ManyToManyField(to='core.Product')),
            ],
        ),
        migrations.AddField(
            model_name='languageusage',
            name='repository',
            field=models.ForeignKey(related_name='languages', to='github.Repository'),
        ),
    ]
