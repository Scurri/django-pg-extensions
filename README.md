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
Notes:

- `coverage`, `filelock`, `psycopg2`, `scandir` and `tox` you need `tar.gz` instead of `whl` version.
- If you get an error downloading any library, e.g. `platformdirs`, you can:
    - try to run `python -m pip download --no-cache-dir -r requirements/tests.txt --dest pip-cache`
    - or comment it from the requirements file, download it directly from pipy.org and place it in
      the `pip-cache` folder.

2. Build container:
```
docker-compose build
```

### Tests
Run test against real PostgreSQL instance, using Docker:
```
docker-compose run --rm tox
```

### Building the wheel
```
python setup.py bdist_wheel
```
