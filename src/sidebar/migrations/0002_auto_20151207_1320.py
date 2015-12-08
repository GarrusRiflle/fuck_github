# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sidebar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='toptags',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AddField(
            model_name='toptags',
            name='tag',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='topusers',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='toptags',
            name='size',
            field=models.IntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='topusers',
            name='username',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
