from django.db import models
from djangopg.fields import (
    TextArrayField, IntArrayField,
    CaseInsensitiveCharField, ArrayField, CaseInsensitiveSlugField
)


class TestModel(models.Model):
    # char_array = ArrayField(models.CharField(max_length=1))
    txt_array = TextArrayField(models.TextField(max_length=4))
    int_array = IntArrayField(models.IntegerField(max_length=2))
    case_char = CaseInsensitiveCharField(max_length=6)
    case_slug = CaseInsensitiveSlugField(max_length=6)
