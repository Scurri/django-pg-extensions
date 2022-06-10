from django.db import models
from djangopg.fields import (
    TextArrayField, IntArrayField, CaseInsensitiveCharField,
    CaseInsensitiveSlugField)


class TestModel(models.Model):
    txt_array = TextArrayField(models.TextField(max_length=4), blank=True, null=True)
    int_array = IntArrayField(models.IntegerField(max_length=2), blank=True, null=True)
    case_char = CaseInsensitiveCharField(max_length=6)
    case_slug = CaseInsensitiveSlugField(max_length=6)


class Poll(models.Model):
    question = models.CharField(max_length=200, blank=True, null=True)
    pub_date = models.DateTimeField('date published', blank=True, null=True)


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200, blank=True, null=True)
    votes = models.IntegerField(blank=True, null=True)
