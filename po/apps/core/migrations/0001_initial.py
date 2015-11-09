# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='AlertType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('priority', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('build', models.ForeignKey(to='core.Build')),
            ],
            options={
                'verbose_name_plural': 'dependencies',
            },
        ),
        migrations.CreateModel(
            name='Deployment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('environment', models.CharField(max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('build', models.ForeignKey(related_name='deployments', to='core.Build')),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('version_major', models.IntegerField(null=True, editable=False, blank=True)),
                ('version_minor', models.IntegerField(null=True, editable=False, blank=True)),
                ('version_patch', models.IntegerField(null=True, editable=False, blank=True)),
                ('version', models.CharField(max_length=20)),
                ('source', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('contact_name', models.CharField(max_length=30)),
                ('contact_email', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='service',
            field=models.ForeignKey(related_name='products', to='core.Service'),
        ),
        migrations.AddField(
            model_name='deployment',
            name='product',
            field=models.ForeignKey(related_name='deployments', to='core.Product'),
        ),
        migrations.AddField(
            model_name='dependency',
            name='package',
            field=models.ForeignKey(related_name='dependants', to='core.Package'),
        ),
        migrations.AddField(
            model_name='build',
            name='dependencies',
            field=models.ManyToManyField(to='core.Package', through='core.Dependency'),
        ),
        migrations.AddField(
            model_name='build',
            name='product',
            field=models.ForeignKey(related_name='builds', to='core.Product'),
        ),
        migrations.AddField(
            model_name='alert',
            name='category',
            field=models.ForeignKey(related_name='alerts', to='core.AlertType'),
        ),
        migrations.AddField(
            model_name='alert',
            name='package',
            field=models.ForeignKey(related_name='alerts', to='core.Package'),
        ),
    ]
