# -*- coding: utf-8 -*-

"""
Tests for the COPY command support.
"""
import csv
import unittest
from datetime import datetime
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

import pytest
import six
from mock import patch

from djangopg.copy import (
    _convert_to_csv_form, copy_insert, copy_insert_raw, _send_csv_to_postgres
)
from tests.data import Poll, Choice


# @pytest.mark.django_db
# @patch('django.db.backends.utils.CursorWrapper')
# class SendCsvToPostgresTestCase(unittest.TestCase):
#     def test_send_csv_to_postgres(self, p_cursor_mock):
#         from django.db import connections
#
#         table_name = Poll._meta.db_table
#         _send_csv_to_postgres(
#             '1,2', connections['memory'], table_name, ['1', '2']
#         )
#         sql = p_cursor_mock.return_value.copy_expert.call_args[0][0]
#         self.assertEqual(
#             sql,
#             u'COPY {}("1","2") FROM STDIN WITH CSV'.format(table_name)
#         )


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
        self.assertIsInstance(res, six.string_types)

    def test_encoding_for_unicode_is_utf8_(self):
        data = u'Δοκιμή'
        res = _convert_to_csv_form(data)
        expected = data
        if six.PY2:
            expected = data.encode('UTF-8')
        self.assertEqual(res, expected)

    def test_str_is_returned_attached(self):
        data = u'Δοκιμή'
        s = data.encode('UTF-8')
        res = _convert_to_csv_form(s)
        expected = s
        self.assertEqual(res, expected)


@patch('djangopg.copy._send_csv_to_postgres')
class ColumnsTestCase(unittest.TestCase):
    """Tests for the columns used in copy."""

    def setUp(self):
        self.entries = [
            Poll(question="Question1", pub_date=datetime.now()),
            Poll(question="Question2", pub_date=datetime.now()),
        ]

    def test_all_non_pk_columns_are_used_if_none_specified(self, pmock):
        copy_insert(Poll, self.entries, using='memory')
        columns = pmock.call_args[0][3]
        self.assertEqual(len(columns), 2)

    def test_specified_columns_only_are_used(self, pmock):
        copy_insert(Poll, self.entries, columns=['question'], using='memory')
        columns = pmock.call_args[0][3]
        self.assertEqual(len(columns), 1)
        self.assertEqual(columns[0], 'question')

        copy_insert(Poll, self.entries, columns=['pub_date'], using='memory')
        columns = pmock.call_args[0][3]
        self.assertEqual(len(columns), 1)
        self.assertEqual(columns[0], 'pub_date')

        copy_insert(Poll, self.entries, columns=['question', 'pub_date'], using='memory')
        columns = pmock.call_args[0][3]
        self.assertEqual(len(columns), 2)
        self.assertEqual(columns[0], 'question')
        self.assertEqual(columns[1], 'pub_date')

    def test_copy_insert_raw(self, pmock):
        copy_insert_raw(Poll, [[self.entries[0]]], columns=['question'], using='memory')
        columns = pmock.call_args[0][3]
        content = pmock.call_args[0][0]
        self.assertEqual(content, 'Poll object\n')
        self.assertEqual(len(columns), 1)


@patch('djangopg.copy._send_csv_to_postgres')
class CsvTestCase(unittest.TestCase):
    """Tests for the CSV formatting."""

    def test_csv_generated_number_of_lines(self, pmock):
        p = Poll(question='Q')
        copy_insert(Poll, [p], using='memory')
        fd = StringIO(pmock.call_args[0][0])
        lines = fd.readlines()
        self.assertEqual(len(lines), 1)

    def test_csv_generated_is_valid(self, pmock):
        p = Poll(question='Q')
        copy_insert(Poll, [p], using='memory')
        fd = StringIO(pmock.call_args[0][0])
        csvf = csv.reader(fd)
        rows = [row for row in csvf]
        self.assertEqual(rows[0][0], 'Q')
        self.assertEqual(rows[0][1], '')


@patch('djangopg.copy._send_csv_to_postgres')
class ForeingKeyFieldTestCase(unittest.TestCase):
    """Tests for handling of foreign key fields."""

    def test_actual_foreign_key_value_is_extracted_correctly(self, pmock):
        p = Poll(pk=1)
        c = Choice(poll=p, choice_text='Text', votes=0)
        copy_insert(Choice, [c], using='memory')
        fd = pmock.call_args[0][0]
        csvf = csv.reader(fd)
        rows = [row for row in csvf]
        data = rows[0]
        self.assertEqual(int(data[0]), 1)


@patch('djangopg.copy._send_csv_to_postgres')
class EmptyStringTestCase(unittest.TestCase):
    """Test handling of empty strings."""

    def setUp(self):
        p = Poll(pk=1)
        self.c = Choice(poll=p)

    def test_empty_string_start(self, pmock):
        copy_insert(Choice, [self.c], columns=['choice_text', 'poll', 'votes'], using='memory')
        csv_file = pmock.call_args[0][0]
        self.assertEqual('"",1,\n', csv_file)

    def test_empty_string_end(self, pmock):
        copy_insert(Choice, [self.c], columns=['poll', 'votes', 'choice_text'], using='memory')
        csv_file = pmock.call_args[0][0]
        self.assertEqual('1,,""\n', csv_file)

    def test_empty_string_middle(self, pmock):
        copy_insert(Choice, [self.c], columns=['poll', 'choice_text', 'votes'], using='memory')
        csv_file = pmock.call_args[0][0]
        self.assertEqual('1,"",\n', csv_file)

    def test_empty_string_start_newline(self, pmock):
        copy_insert(
            Choice, [self.c, self.c], columns=['choice_text', 'poll', 'votes'], using='memory'
        )
        csv_file = pmock.call_args[0][0]
        self.assertEqual('"",1,\n"",1,\n', csv_file)

    def test_empty_string_end_newline(self, pmock):
        copy_insert(
            Choice, [self.c, self.c], columns=['poll', 'votes', 'choice_text'], using='memory'
        )
        csv_file = pmock.call_args[0][0]
        self.assertEqual('1,,""\n1,,""\n', csv_file)

    def test_no_empty_string(self, pmock):
        copy_insert(
            Choice, [self.c, self.c], columns=['poll', 'choice_text', 'votes'], using='memory'
        )
        csv_file = pmock.call_args[0][0]
        self.assertEqual('1,"",\n1,"",\n', csv_file)
