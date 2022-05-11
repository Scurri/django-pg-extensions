# -*- coding: utf-8 -*-
import psycopg2
import pytest
from djangopg.copy import copy_insert

from integration_tests.models import TestModel

TestModel.__test__ = False


def test_connection():
    params = {
        'host': 'djangopg_db',
        'port': 5432,
        'database': 'test_db',
        'user': 'dbuser',
        'password': 'dbpass'
    }
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT version();')
    except psycopg2.Error:
        pytest.fail('Could not connect to PostgreSQL')


@pytest.mark.django_db
@pytest.mark.parametrize('data, result', [
    (('txt', 'text', 11, 21, 'char', 'slug'), ('txt', 'text', 11, 21, 'char', 'slug')),
    ((u'txt', u'text', 11, 21, u'char', u'slug'), (u'txt', u'text', 11, 21, u'char', u'slug')),
    ((b'txt', b'text', 11, 21, b'char', b'slug'), ('txt', 'text', 11, 21, 'char', 'slug'))
])
def test_copy_str(data, result):
    tm = TestModel(txt_array=[data[0], data[1]], int_array=[data[2], data[3]],
                   case_char=data[4], case_slug=data[5])
    copy_insert(TestModel, [tm])
    obj = TestModel.objects.first()
    assert TestModel.objects.count() == 1
    assert obj.txt_array == [result[0], result[1]]
    assert obj.int_array == [result[2], result[3]]
    assert obj.case_char == result[4]
    assert obj.case_slug == result[5]


@pytest.mark.django_db
def test_empty_copy():
    tm = TestModel(txt_array=[], int_array=[], case_char='', case_slug='')
    copy_insert(TestModel, [tm])
    obj = TestModel.objects.first()
    assert TestModel.objects.count() == 1
    assert obj.txt_array == []
    assert obj.int_array == []
    assert obj.case_char == ''
    assert obj.case_slug == ''
