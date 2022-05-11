# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangopg.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('txt_array', djangopg.fields.TextArrayField(verbose_name=models.TextField(max_length=4))),
                ('int_array', djangopg.fields.IntArrayField(verbose_name=models.IntegerField(max_length=2))),
                ('case_char', djangopg.fields.CaseInsensitiveCharField(max_length=6)),
                ('case_slug', djangopg.fields.CaseInsensitiveSlugField(max_length=6)),
            ],
        ),
    ]
