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

## Running the tests
Just run, from the root directory:
```
pip install -U -r requirements/build.txt
tox
```
