# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-11-13 03:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BooksManager',
        ),
    ]
