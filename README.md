# Moberries home assignment

Implement following logic using Django Rest Framework

Imagine a simplified pizza ordering services with following functionality:

1. Create order.
Order data:
- pizza id
- pizza size (30cm/50cm)
- customer name
- customer address (just plain text)
2. Update order
3. Remove order
4. See a list of customer orders

Tasks:

1. Design Model/DB structure (PostgreSQL)
2. Design and implement API for the described web service. Please note:
- You don’t have to take care about authentication etc, we are just interested in structure and data modelling.
- You don’t have to implement any UI, just the API endpoints
- Use Viewsets
3. Write test(s) for at least one of these endpoint(s)

## How to start

As far as the application is deployed through docker-compose you have to install docker-compose and docker tools. When tools are installed on your operating system then you can execute:

```sh
docker-compose up init
```

for initialization of DB and then:

```sh
docker-compose up -d start
```

in the root directory of the application. As result, you obtain 2 docker containers: Api and Database.

Your terminal can also be attached to containers and see any logs from the application:

```sh
docker logs -f app-api
```

You can access the application from your browser by address `http://localhost:8000`. Full REST interfaces information are available in `http://localhost:8000/swagger`.
**All responses which provide a data do it in JSON format.**

## Configuration

Some parameters of the application could be configured by changing of `env/local.env`:
  - **POSTGRES_HOST** - host alias for database inside containers.
  - **POSTGRES_DB** - database name
  - **POSTGRES_USER** - postgres user
  - **POSTGRES_PASSWORD** - postgres password

## Run tests

You can run all unit tests by executing:

```sh
docker-compose up run_tests
```

The whole process of unit testing, results, and a code coverage are shown in the terminal:

```sh
app-test     | ...................................................
app-test     | ----------------------------------------------------------------------
app-test     | Ran 51 tests in 0.383s
app-test     |
app-test     | OK
app-test     | Creating test database for alias 'default'...
app-test     | System check identified no issues (0 silenced).
app-test     | Destroying test database for alias 'default'...
app-test     | Name                                       Stmts   Miss  Cover   Missing
app-test     | ------------------------------------------------------------------------
app-test     | __init__.py                                    0      0   100%
app-test     | pizza/__init__.py                              0      0   100%
app-test     | pizza/enums.py                                 1      0   100%
app-test     | pizza/migrations/0001_initial.py               6      0   100%
app-test     | pizza/migrations/__init__.py                   0      0   100%
app-test     | pizza/mixins/__init__.py                       0      0   100%
app-test     | pizza/mixins/customer_nested_resource.py      19      0   100%
app-test     | pizza/mixins/mark_as_deleted.py                7      0   100%
app-test     | pizza/models/__init__.py                       0      0   100%
app-test     | pizza/models/customer.py                      10      1    90%   16
app-test     | pizza/models/customer_address.py              11      1    91%   18
app-test     | pizza/models/order.py                         17      0   100%
app-test     | pizza/models/pizza.py                          9      1    89%   15
app-test     | pizza/serializers/__init__.py                  0      0   100%
app-test     | pizza/serializers/customer.py                 14      0   100%
app-test     | pizza/serializers/customer_address.py         14      0   100%
app-test     | pizza/serializers/order.py                    33      0   100%
app-test     | pizza/serializers/pizza.py                    13      0   100%
app-test     | pizza/settings.py                             14      0   100%
app-test     | pizza/urls.py                                 11      0   100%
app-test     | pizza/views/__init__.py                        0      0   100%
app-test     | pizza/views/customer.py                        7      0   100%
app-test     | pizza/views/customer_address.py               10      0   100%
app-test     | pizza/views/order.py                          10      0   100%
app-test     | pizza/views/pizza.py                           7      0   100%
app-test     | ------------------------------------------------------------------------
app-test     | TOTAL                                        213      3    99%
```

## Testing environment

The application was tested in a system with:
  - MacBook Pro (Intel Core i5 2,3 GHz, 8 GB DDR3)
  - MacOS High Sierra (10.13.3)
  - Docker-compose (1.22.0, build f46880f)
  - Docker (18.06.1-ce, build e68fc7a)

## Application environment

The application was built on a base of:
  - Python 3.7.1
  - Django 2.1.2
  - Django Rest Framework 3.8.2
  - psycopg2 2.7.5
  - Docker container postgres:11.0-alpine

and consists of 3 docker containers:
  - db (postgres:11.0-alpine)
  - app-api (custom built on base of python:3.7.1-alpine3.8)
  - app-init (custom built on base of python:3.7.1-alpine3.8)
  - app-test (custom built on base of python:3.7.1-alpine3.8)

For unit tests are used:
  - built-in unittest library
  - built-in mock library
  - Coverage 4.5.1

## TODO
  - Testing libraries are included in a production environment. The libraries should be split into two environments: production and testing
  - Api runs with manage.py runserver, should be tuned for production environment with uWsgi and Nginx for example