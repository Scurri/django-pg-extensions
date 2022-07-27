# -*- coding: utf-8 -*-

import re
import csv
from contextlib import closing

import six
from django.db import connections
from django.db.models import AutoField

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO


def _convert_to_csv_form(data):
    """Convert the data to a form suitable for CSV."""
    # NULL values should be an empty column
    if data is None:
        return ''
    # Empty strings should be different to NULL values
    if data == '':
        return '""'
    if isinstance(data, six.text_type) and six.PY2:
        # CSV needs to be encoded to UTF8 on Py2
        return data.encode('UTF-8')
    # Arrays are not supported
    return data


def _fix_empty_string_marks(text):
    """Fix the empty string notation in text to what PostgreSQL expects."""
    # COPY command expects the empty string to be quoted.
    # But csv quotes the double-quotes we put.
    # Replace the quoted values either at the first entry, the last or one in
    # between with "".
    substiture = r'((?<=^)""""""(?=,)|(?<=,)""""""(?=,)|(?<=,)""""""(?=$))'
    replace_with = r'""'
    return re.sub(substiture, replace_with, text, flags=re.M)


def _send_csv_to_postgres(csv_text, conn, table_name, columns):
    """
    Send the CSV file to PostgreSQL for inserting the entries.

    Use the COPY command for faster insertion and less WAL generation.

    :param csv_text: A CSV-formatted string with the data to send.
    :param conn: The connection object.
    """
    fd = StringIO(csv_text)
    # Move the fp to the beginning of the string
    fd.seek(0)
    columns = map(conn.ops.quote_name, columns)
    if six.PY3:
        columns = list(columns)
    cursor = conn.cursor()
    sql = "COPY %s(%s) FROM STDIN WITH CSV"
    try:
        cursor.copy_expert(sql % (table_name, ','.join(columns)), fd)
    finally:
        cursor.close()
        fd.close()


def copy_insert(model, entries, columns=None, using='default', **kwargs):
    """
    Add the given entries to the database using the COPY command.

    The caller is required to handle the transaction.

    :param model: The model class the entries are for.
    :param entries: An iterable of entries to be inserted.
    :param columns: A list of columns that will have to be populated.
        By default, we use all columns but the primary key.
    :param using: The database connection to use.
    """
    table_name = kwargs.get('table_name', model._meta.db_table)
    conn = connections[using]

    if columns is None:
        fields = [
            f for f in model._meta.fields if not isinstance(f, AutoField)
        ]
    else:
        fields = [model._meta.get_field_by_name(col)[0] for col in columns]

    # Construct a StringIO from the entries
    with closing(StringIO()) as fd:
        csvf = csv.writer(fd, lineterminator='\n')
        for e in entries:
            row = [
                _convert_to_csv_form(
                    f.get_db_prep_save(f.pre_save(e, True), connection=conn)
                )
                for f in fields
            ]
            csvf.writerow(row)
        content = _fix_empty_string_marks(fd.getvalue())
    db_columns = [f.column for f in fields]
    _send_csv_to_postgres(content, conn, table_name, db_columns)


def copy_insert_raw(table_name, entries, columns, using='default'):
    conn = connections[using]

    # Construct a StringIO from the entries
    with closing(StringIO()) as fd:
        csvf = csv.writer(fd, lineterminator='\n')
        for e in entries:
            row = [
                _convert_to_csv_form(cell) for cell in e
            ]
            csvf.writerow(row)
        content = _fix_empty_string_marks(fd.getvalue())
    _send_csv_to_postgres(content, conn, table_name, columns)
