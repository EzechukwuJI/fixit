# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-17 00:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fixitTradesmen', '0002_tradesman_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='fixitTradesmen.Tradesman', verbose_name=b'For '),
        ),
        migrations.AlterField(
            model_name='joblist',
            name='tradesman',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixitTradesmen.Tradesman', verbose_name=b'Job Executed by'),
        ),
    ]