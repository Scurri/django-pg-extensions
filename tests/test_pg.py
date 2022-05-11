import psycopg2
import pytest


@pytest.fixture(scope='session')
def connection():
    params = {
        # 'host': '170.20.128.2',
        'host': 'djangopg_db',
        'port': 5432,
        'database': 'test_db',
        'user': 'dbuser',
        'password': 'dbpass'
    }
    conn = psycopg2.connect(**params)
    yield conn


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
def test_copy():
    from djangopg.copy import copy_insert
    from tests.data import TestModel
    tm = TestModel(txt_array=['txt', 'text'],
                   int_array=[11, 21], case_char='char', case_slug='slug')
    copy_insert(TestModel, [tm], using='default')
