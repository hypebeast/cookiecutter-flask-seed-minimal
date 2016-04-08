#!/usr/bin/env python
"""Setup script."""
import {{ cookiecutter.app_name }}
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

README = open('README.rst').read()
LICENSE = open('LICENSE').read()

project = '{{ cookiecutter.project_name }}'

setup(
    name=project,
    version={{cookiecutter.app_name}}.__version__,
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}',
    description='{{ cookiecutter.project_short_description }}',
    long_description=(README),
    license=(LICENSE),
    author='{{ cookiecutter.author }}',
    author_email='{{ cookiecutter.email }}',
    packages=['{{ cookiecutter.app_name }}'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools == 20.2.2',
        'wheel == 0.29.0',
        'Flask == 0.10.1',
        'MarkupSafe == 0.23',
        'Werkzeug == 0.11.4',
        'Jinja2 == 2.8',
        'itsdangerous == 0.24',
        'Flask-SQLAlchemy == 2.1',
        'psycopg2 == 2.6.1',
        'SQLAlchemy == 1.0.12',
        'Flask-Migrate == 1.8.0',
        'Flask-WTF == 0.12',
        'WTForms == 2.1',
        'gunicorn == 19.1.1',
        'Flask-Assets == 0.11',
        'cssmin == 0.2.0',
        'jsmin == 2.0.11',
        'Flask-Login == 0.3.2',
        'Flask-Bcrypt == 0.7.1',
        'Flask-Cache == 0.13.1',
        'Flask-DebugToolbar == 0.10.0'
    ],
    scripts=['manage.py'],
    test_suite='tests',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]
)
