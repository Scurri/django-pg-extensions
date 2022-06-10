# -*- coding: utf-8 -*-

import unittest
from datetime import datetime

import pytest

from djangopg.copy import (
    _convert_to_csv_form, copy_insert, copy_insert_raw
)
from .resource_app.models import Choice, Poll, TestModel


class DataConversionTestCase(unittest.TestCase):
    """Tests for converting pieces of data to a suitable form."""

    def test_none_is_converted_to_empty_string(self):
        data = None
        res = _convert_to_csv_form(data)
        expected = ''
        self.assertEqual(res, expected)

    def test_empty_string_is_double_quotes(self):
        data = ''
        res = _convert_to_csv_form(data)
        expected = '""'
        self.assertEqual(res, expected)

    def test_integer_remains_integer(self):
        data = 5
        res = _convert_to_csv_form(data)
        expected = data
        self.assertEqual(res, expected)

    def test_unicode_is_encoded(self):
        data = u'Δοκιμή'
        res = _convert_to_csv_form(data)
        self.assertIsInstance(res, str)

    def test_encoding_for_unicode_is_utf8_(self):
        data = u'Δοκιμή'
        res = _convert_to_csv_form(data)
        expected = data.encode('UTF-8')
        self.assertEqual(res, expected)

    def test_str_is_returned_attached(self):
        data = u'Δοκιμή'
        s = data.encode('UTF-8')
        res = _convert_to_csv_form(s)
        expected = s
        self.assertEqual(res, expected)


@pytest.mark.django_db
class ColumnsTestCase(unittest.TestCase):
    """Tests for the columns used in copy."""

    def setUp(self):
        self.entries = [
            Poll(question="Question1", pub_date=datetime.now()),
            Poll(question="Question2", pub_date=datetime.now()),
        ]

    def test_all_non_pk_columns_are_used_if_none_specified(self):
        copy_insert(Poll, self.entries)
        qs = Poll.objects.all()
        values = qs.values_list(flat=False)
        for no, q, p in values:
            assert "Question{}".format(no) in q
            assert isinstance(p, datetime)
        self.assertEqual(len(values), 2)

    def test_specified_columns_only_are_used(self):
        copy_insert(Poll, self.entries, columns=['question'])
        qs = Poll.objects.all()
        values = qs.values_list('question', flat=True)
        assert len(values) == 2
        assert "Question1" in values
        assert "Question2" in values

        copy_insert(Poll, self.entries, columns=['pub_date'])
        qs = Poll.objects.all()
        values = qs.values_list('pub_date', flat=True)
        self.assertEqual(len(values), 4)
        assert isinstance(values[2], datetime)
        assert isinstance(values[3], datetime)

        copy_insert(Poll, self.entries, columns=['question', 'pub_date'])
        qs = Poll.objects.all()
        values = qs.values_list('question', flat=True)
        self.assertEqual(len(values), 6)
        assert "Question1" == values[4]
        assert "Question2" == values[5]

    def test_copy_insert_raw(self):
        copy_insert_raw(Poll._meta.db_table, [[self.entries[0]]], columns=['question'])
        qs = Poll.objects.all()
        values = qs.values_list('question', flat=True)
        self.assertEqual(len(values), 1)
        assert "Poll object" in values


@pytest.mark.django_db
class ForeingKeyFieldTestCase(unittest.TestCase):
    """Tests for handling of foreign key fields."""

    def test_actual_foreign_key_value_is_extracted_correctly(self):
        p = Poll(pk=1)
        c = Choice(poll=p, choice_text='Text', votes=0)
        copy_insert(Choice, [c])
        qs = Choice.objects.all()
        values = qs.values()
        assert values[0]['poll_id'] == 1


@pytest.mark.django_db
class EmptyStringTestCase(unittest.TestCase):
    """Test handling of empty strings."""

    def setUp(self):
        p = Poll(pk=1)
        self.c = Choice(poll=p)

    def test_empty_string_start(self):
        copy_insert(Choice, [self.c], columns=['choice_text', 'poll', 'votes'])
        qs = Choice.objects.all()
        values = qs.values()
        assert {'votes': None, 'choice_text': None, u'id': 6, u'poll_id': 1} == values[0]

    def test_empty_string_end(self):
        copy_insert(Choice, [self.c], columns=['poll', 'votes', 'choice_text'])
        qs = Choice.objects.all()
        values = qs.values()
        assert {'votes': None, 'choice_text': None, u'id': 2, u'poll_id': 1} == values[0]

    def test_empty_string_middle(self):
        copy_insert(Choice, [self.c], columns=['poll', 'choice_text', 'votes'])
        qs = Choice.objects.all()
        values = qs.values()
        assert {'votes': None, 'choice_text': None, u'id': 5, u'poll_id': 1} == values[0]

    def test_empty_string_start_newline(self):
        copy_insert(
            Choice, [self.c, self.c], columns=['choice_text', 'poll', 'votes']
        )
        qs = Choice.objects.all()
        values = qs.values()
        assert {'votes': None, 'choice_text': None, u'id': 7, u'poll_id': 1} == values[0]

    def test_empty_string_end_newline(self):
        copy_insert(
            Choice, [self.c, self.c], columns=['poll', 'votes', 'choice_text']
        )
        qs = Choice.objects.all()
        values = qs.values()
        assert {'votes': None, 'choice_text': None, u'id': 3, u'poll_id': 1} == values[0]

    def test_no_empty_string(self):
        copy_insert(
            Choice, [self.c, self.c], columns=['poll', 'choice_text', 'votes']
        )
        qs = Choice.objects.all()
        values = qs.values()
        assert {'votes': None, 'choice_text': None, u'id': 9, u'poll_id': 1} == values[0]
