# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangopg.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice_text', models.CharField(max_length=200, null=True, blank=True)),
                ('votes', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=200, null=True, blank=True)),
                ('pub_date', models.DateTimeField(null=True, verbose_name=b'date published', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('txt_array', djangopg.fields.TextArrayField(null=True, verbose_name=models.TextField(max_length=4), blank=True)),
                ('int_array', djangopg.fields.IntArrayField(null=True, verbose_name=models.IntegerField(max_length=2), blank=True)),
                ('case_char', djangopg.fields.CaseInsensitiveCharField(max_length=6)),
                ('case_slug', djangopg.fields.CaseInsensitiveSlugField(max_length=6)),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(to='integration_tests.Poll'),
        ),
    ]
