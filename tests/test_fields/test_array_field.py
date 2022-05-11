# -*- coding: utf-8 -*-

import unittest

import six

from djangopg.fields import (
    ArrayField, TextArrayField, IntArrayField, CaseInsensitiveMixin
)


class DbTypeTestCase(unittest.TestCase):
    """Tests for the db_type."""

    def test_type_is_always_array(self):
        f = ArrayField()
        setattr(f, '_type', 'int')
        self.assertIn('[]', f.db_type(None))

    def test_respects_type_of_class(self):
        custom_type = 'int'
        f = ArrayField()
        setattr(f, '_type', custom_type)
        self.assertIn(custom_type, f.db_type(None))


class OperatorsTestCase(unittest.TestCase):
    """Tests for the allowed operators."""

    def test_invalid_operator_raises_type_error(self):
        f = ArrayField()
        self.assertRaises(TypeError, f.get_prep_lookup, 'contains', 'str')

    def test_valid_operators_return_value(self):
        value = [1, 2, 3, ]
        f = ArrayField()
        for op in ArrayField._allowed_operators:
            self.assertEqual(value, f.get_prep_lookup(op, value))


class PythonValueTestCase(unittest.TestCase):
    """Tests for converting the database value to Python type."""

    def setUp(self):
        self.f = ArrayField()

    def test_none_returns_none(self):
        self.assertIsNone(self.f.to_python(None))

    def test_empty_list_returns_empty_list(self):
        self.assertEqual(self.f.to_python([]), [])

    def test_list_returns_list(self):
        self.assertEqual(self.f.to_python([1, 2]), [1, 2])

    def test_wrong_type(self):
        with self.assertRaises(TypeError):
            self.f.to_python({})


class ConversionToPythonTestCase(unittest.TestCase):
    """Test specific conversion to django types."""

    def test_populated_array_of_varchar_returns_list_of_unicode(self):
        f = TextArrayField()
        res = f.to_python(['a', 'b'])
        self.assertIsInstance(res, list)
        for element in res:
            self.assertIsInstance(element, six.text_type)

    def test_populated_array_of_int_returns_list_of_int(self):
        f = IntArrayField()
        res = f.to_python([1, 2])
        self.assertIsInstance(res, list)
        for element in res:
            self.assertIsInstance(element, int)

    def test_none_returns_none(self):
        f = TextArrayField()
        self.assertIsNone(f.to_python(None))
        self.assertIsNone(f.to_python(''))


class DbValueTestCase(unittest.TestCase):
    """Tests for converting the Python value to database type."""

    def setUp(self):
        self.f = ArrayField()

    def test_none_returns_none(self):
        # psycopg2 will convert None to NULL
        self.assertIsNone(self.f.get_prep_value(None))

    def test_empty_list_returns_empty_list(self):
        # psycopg2 will convert [] to {}
        self.assertEqual(self.f.get_prep_value([]), [])

    def test_list_returns_list(self):
        value = [1, 2, 3, ]
        self.assertEqual(self.f.get_prep_value(value), value)


class CaseInsensitiveMixinTest(unittest.TestCase):
    def setUp(self):
        self.mixin = CaseInsensitiveMixin()

    def test_db_type(self):
        self.assertEqual(self.mixin.db_type(''), 'citext')

    def test_str_returns_str(self):
        self.assertEqual(self.mixin.to_python('some_str'), 'some_str')

    def test_unicode_returns_str(self):
        self.assertEqual(self.mixin.to_python(u'some_str'), u'some_str')

    def test_none_returns_none(self):
        self.assertIsNone(self.mixin.to_python(None))

    def test_any_type_returns_string(self):
        self.assertEqual(self.mixin.to_python({1: '1'}), "{1: '1'}")
        if six.PY2:
            self.assertEqual(self.mixin.to_python({'1'}), u"set(['1'])")
        else:
            self.assertEqual(self.mixin.to_python({'1'}), "{'1'}")
