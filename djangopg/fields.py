# -*- coding: utf-8 -*-

import six
from django.db import models
from django.utils.encoding import smart_text


class ArrayField(six.with_metaclass(models.SubfieldBase, models.Field)):
    """Base class for fields of type array."""

    _allowed_operators = [
        'exact', 'isnull', 'array_contains',
        'array_contained', 'array_overlaps',
    ]

    def db_type(self, connection):
        return '%s[]' % self._type

    def to_python(self, value):
        # Psycopg2 uses lists for arrays
        if value is None or value == '':
            # The check for empty strings is needed, because to_python
            # is called on empty constructors.
            return None
        if not isinstance(value, list):
            raise TypeError("Expected list, got {}".format(type(value)))
        return value

    def get_prep_value(self, value):
        return value

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type not in self._allowed_operators:
            raise TypeError('Invalid operator {}'.format(lookup_type))
        return value

    def get_db_prep_lookup(self, lookup_type, value, connection, prepared=False):
        prep_value = super(ArrayField, self).get_db_prep_lookup(
            lookup_type, value, connection, prepared
        )
        if prep_value is None and lookup_type.startswith('array_'):
            prep_value = self.get_db_prep_value(
                value, connection=connection, prepared=prepared
            )
            return [prep_value]


class TextArrayField(ArrayField):
    """Field for arrays of VARCHAR."""

    description = 'Text array'
    _type = 'text'

    def to_python(self, value):
        value = super(TextArrayField, self).to_python(value)
        if value is None:
            return None
        return list(map(smart_text, value))


class IntArrayField(ArrayField):
    """Field for arrays of INT."""

    description = 'INT array'
    _type = 'int'


class CaseInsensitiveMixin(object):
    """Add a case-insensitive variant of text fields."""

    def db_type(self, connection):
        return 'citext'

    def to_python(self, value):
        if isinstance(value, six.text_type) or value is None:
            return value
        return smart_text(value)


class CaseInsensitiveCharField(six.with_metaclass(
        models.SubfieldBase, CaseInsensitiveMixin, models.CharField)):
    """Case-insensitive CharField."""
    pass


class CaseInsensitiveSlugField(six.with_metaclass(
        models.SubfieldBase, CaseInsensitiveMixin, models.SlugField)):
    """Case-insensitive SlugField."""
    pass
