===============================
{{ cookiecutter.app_name }}
===============================

A flasky app.


Quickstart
----------

First, set your app's secret key as an environment variable.

.. code-block:: bash

    export {{ cookiecutter.app_name | upper }}_SECRET='something-really-secret'


Then run the following commands to bootstrap your environment.


::

    git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.app_name }}
    cd {{ cookiecutter.app_name }}
    pip install -r requirements/dev.txt
    bower install
    python manage.py server

You will see a pretty welcome screen.

If you want to use a database, install your desired DBMS and run the following to create your app's database tables and perform the initial migration:

::

    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    python manage.py server



Deployment
----------

In your production environment, make sure the ``{{ cookiecutter.app_name | upper }}_ENV`` environment variable is set to ``"prod"``.


Shell
-----

To open the interactive shell, run ::

    python manage.py shell

By default, you will have access to ``app``, and the ``db`` model.


Running Tests
-------------

To run all tests, run ::

    python manage.py test


Linting
-------

To run the linter, run ::

    python manage.py lint


Migrations
----------

Whenever a database migration needs to be made. Run the following commands:
::

    python manage.py db migrate

This will generate a new migration script. Then run:
::

    python manage.py db upgrade

To apply the migration.

For a full migration command reference, run ``python manage.py db --help``.
