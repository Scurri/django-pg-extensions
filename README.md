# Django PostgreSQL Extensions
This package tries to expose functionality from PostgreSQL to django
applications.

Python 2.7 or 3.4+ is required.

## Features
- Support for the COPY command.
- Support for ARRAYs. Out of the box support for INT and TEXT arrays. The
  operators @> (contains), <@ (is contained by) and && (overlaps with) are
  supported.
- Case-insensitive variants of `CharField` and `SlugField`.

### Building Docker container
1. In order to run tests (using Docker containers) you need download the following Python packages:
```
pip download --no-cache-dir -r requirements/tests.txt --dest pip-cache
```
Note: `coverage`, `filelock`, `psycopg2`, `scandir` and `tox` you need `tar.gz` instead of `whl` version.

2. Build container:
```
docker-compose build
```

### Tests
Run test against real PostgreSQL instance, using Docker:
```
docker-compose run --rm tox
```

### Known issue
An issue was found during development of unit tests. Please check the following code snippet:
```python
assert TestModel.objects.count() == 0
tm = TestModel(txt_array=[], int_array=[], case_char='', case_slug='')
copy_insert(TestModel, [tm])
assert TestModel.objects.count() == 1
assert TestModel.objects.filter(txt_array=[], int_array=[], case_char='', case_slug='').exists()
```
The snipped fails with the following traceback:
```python
self = <django.db.models.lookups.Exact object at 0x7f41cbffb050>, compiler = <django.db.models.sql.compiler.SQLCompiler object at 0x7f41cbfeed50>
connection = <djangopg.postgresql_psycopg2.base.DatabaseWrapper object at 0x7f41d0b290d0>

def as_sql(self, compiler, connection):
    lhs_sql, params = self.process_lhs(compiler, connection)
    rhs_ql, rhs_params = self.process_rhs(compiler, connection)
>   params.extend(rhs_params)
E   TypeError: 'NoneType' object is not iterable

.tox/py27/lib/python2.7/site-packages/django/db/models/lookups.py:220: TypeError
```
