# -*- coding: utf-8 -*-
import psycopg2
import pytest

from .resource_app.models import TestModel

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
