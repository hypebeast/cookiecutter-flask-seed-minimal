cookiecutter-flask-seed-minimal
===============================

.. image:: https://travis-ci.org/hypebeast/cookiecutter-flask-seed-minimal.svg?branch=master
    :target: https://travis-ci.org/hypebeast/cookiecutter-flask-seed-minimal

A minimal and clean Cookiecutter template for Flask that utilizes best practices (blueprints and application Factory patterns).

It includes uikit, Flask-SQLAlchemy, WTForms, and various testing utilities out of the box.

It doesn't provide user management (e.g. login, registration, etc.) out of the box,
because it's a minimal project template. But it provides support for DBMS and therefore
you can easily add user management by yourself if you want.


Quick Start
-----------

Generate a new project:

  $ pip install cookiecutter

  $ cookiecutter https://github.com/hypebeast/cookiecutter-flask-seed-minimal.git


Features
--------

- Uses uikit_ as frontend library
- Flask-SQLAlchemy
- Easy database migrations with Flask-Migrate
- Flask-WTForms with login and registration forms
- pytest and Factory-Boy for testing (example tests included)
- A simple manage.py script.
- CSS and JS minification using Flask-Assets
- Bower support for frontend package management
- Caching using Flask-Cache
- Useful debug toolbar
- A Fabric file for easy provisioning and deployment (via distutils)
- Procfile for deploying to a PaaS (e.g. Heroku)
- Production stack uses Gunicorn, Nginx and Supervisor
- Alternative you can use Heroku for deployment
- Utilizes best practices: Blueprints and Application Factory patterns

.. _uikit: http://getuikit.com

Screenshot
----------

TODO


Usage
-----

Step 1: Install Cookiecutter
++++++++++++++++++++++++++++

First, get cookiecutter:

  $ pip install cookiecutter

Step 2: Create your new project
+++++++++++++++++++++++++++++++

Now create a new project:

  $ cookiecutter https://github.com/hypebeast/cookiecutter-flask-seed-minimal.git

You'll be prompted for some questions, answer them, then it will create a new Flask project for you.

Example project generation:

  $ cookiecutter https://github.com/hypebeast/cookiecutter-flask-seed-minimal.git
  author (default is "Sebastian Ruml")?
  email (default is "sebastian@sebastianruml.name")?
  github_username (default is "hypebeast")?
  project_name (default is "My Flask App")?
  app_name (default is "myflaskapp")?
  repo_name (default is "myflaskapp")?
  project_short_description (default is "A minimal flasky app.")?

Step 3: Create a repo
+++++++++++++++++++++

Create a git repo and add your new project.

  $ cd cookiecutter-flask-seed-minimal

  $ git init

  $ git add .

  $ git commit


Prompts
-------

Template Variables
++++++++++++++++++

The following variables can be set during project generation:

repo_name
  TODO


License
-------

See License_.

.. _License: /LICENSE.


Credits
-------

This project was inspired by the following projects:

* cookiecutter-flask: https://github.com/sloria/cookiecutter-flask


TODOs
-----

* Fabric: Proper handling of migrations
* Fabric: Deployment to Heroku
* Ansible integration
* Add footer
* Flask-AppConfig integration
