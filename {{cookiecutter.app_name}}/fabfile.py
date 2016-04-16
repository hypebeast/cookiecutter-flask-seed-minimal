#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Fabric script for provisioning and deployment.

This is a simple Fabric script that handles the following tasks:

1. Bootstrapping/Provisioning the server(s)
2. Deploying the application

For deployment the following technology stack is used:

- Gunicorn
- Nginx
- Supervisorctl

During bootstrapping the following tasks are executed:

- Install all required packages and applications
- Create application directory and virtualenv
- Create and copy all required config files

The following assumptions are made:

- It's assumed that Debian or Ubuntu runs on the server

"""
from fabric.api import env, local, settings, sudo, cd, lcd, put, run, prefix
from fabric.colors import green
from fabric.contrib.files import exists

from {{ cookiecutter.app_name }} import __version__


# CONFIG

app_name = '{{ cookiecutter.app_name }}'

local_app_dir = '.'
local_config_dir = './deploy'

remote_app_home_dir = '/opt'
remote_app_dir = '{}/{}'.format(remote_app_home_dir, '{{cookiecutter.app_name}}')
remote_log_dir = '{}/{}'.format('/var/log', '{{cookiecutter.app_name}}')
remote_tmp_dir = '/tmp'

dist_package_name = '{}-{}.tar.gz'.format(app_name, __version__)
dist_package_file = '{}/{}'.format(remote_tmp_dir, dist_package_name)

env.user = 'xxxxx'  # Change: user for deployment
env.hosts = ['xxxxx', 'xxxxx']  # Change: hosts to deploy to
env.activate = 'source {}/{}'.format(remote_app_dir, 'env/bin/activate')

# END CONFIG


# HELPERS

def info(message):
    """Print info message."""
    print(green(message))


def package_installed(pkg_name):
    """Check if a package is already installed."""
    cmd = 'dpkg-query -l \"{}\" | grep -q ^.i'.format(pkg_name)
    with settings(warn_only=True):
        result = sudo(cmd)
    return result.succeeded


def yes_install(pkg_name):
    """ref: http://stackoverflow.com/a/10439058/1093087."""
    sudo('apt-get --force-yes --yes install %s' % (pkg_name))

# END HELPERS

# BOOTSTRAPING HELPERS

PACKAGES = (
    'python',
    'python-dev',
    'python-pip',
    'python-virtualenv',
    'nginx',
    'supervisor',
    'python-setuptools',
    'python-psycopg2',
    'git-core',
)


def install_packages():
    """Install required packages."""
    sudo('apt-get update')
    for package in PACKAGES:
        if not package_installed(package):
            yes_install(package)


def create_app_dir():
    """Create the application directory and setup a virtualenv."""
    # create app dir
    if exists(remote_app_dir) is False:
        sudo('mkdir -p ' + remote_app_dir)

    # create virtual env
    with cd(remote_app_dir):
        if exists(remote_app_dir + '/env') is False:
            sudo('virtualenv env')

    # Change permissions
    sudo('chown {}:{} {} -R'.format(env.user, env.user, remote_app_dir))

    # Create log dir
    if exists(remote_log_dir) is False:
        sudo('mkdir {}'.format(remote_log_dir))


def configure_supervisor():
    """Configure supervisor.

    Installs supervisor configuration for the application and register it.
    """
    with lcd(local_config_dir):
        with cd('/etc/supervisor/conf.d'):
            put('./supervisor.conf', './{{ cookiecutter.app_name }}.conf', use_sudo=True)
            sudo('supervisorctl reread')
            sudo('supervisorctl update')


def configure_nginx():
    """Configure nginx.

    Installs nginx config for the application.
    """
    # copy configuration
    with lcd(local_config_dir):
        with cd('/etc/nginx/sites-available'):
            put('./nginx.conf', './{}.conf'.format(app_name), use_sudo=True)

    # enable configuration
    if exists('/etc/nginx/sites-enabled/{}.conf'.format(app_name)) is False:
        sudo('ln -s /etc/nginx/sites-available/{}.conf'.format(app_name) +
             ' /etc/nginx/sites-enabled/{}.conf'.format(app_name))

    # reload configuration
    sudo('service nginx reload')

# END BOOTSTRAPING HELPERS


# DEPLOYMENT HELPERS

def pack():
    """Create a new source distribution as tarball."""
    local('python setup.py sdist --formats=gztar', capture=False)


def copy_dist_package():
    """Copy the dist package to the remote host(s)."""
    put('./dist/%s' % (dist_package_name), remote_tmp_dir)

    with cd(remote_app_dir):
        put('./deploy/gunicorn_start.sh', './gunicorn_start.sh')


def install_dist_package():
    """Install the dist package on the remote host(s)."""
    with cd(remote_app_dir):
        with prefix(env.activate):
            sudo('pip install {}'.format(dist_package_file))

    # remove dist package
    run('rm {}'.format(dist_package_file))

# END DEPLOYMENT HELPERS


# Supervisor

def status():
    """Return the status of the app."""
    sudo('supervisorctl status')


def restart_app():
    """Restart the app."""
    sudo('supervisorctl restart {{cookiecutter.app_name}}')


def start_app():
    """Restart the app."""
    sudo('supervisorctl start {{cookiecutter.app_name}}')

# END MANAGEMENT


# BOOTSTRAPING

def bootstrap():
    """Provisioning the server."""
    info('Provisioning server')

    # Install all packages
    install_packages()
    # Create application directory and setup virtualenv
    create_app_dir()
    # Configure supervisor
    configure_supervisor()
    # Configure Nginx
    configure_nginx()

    info('DONE - Provisioning server')


# END BOOTSTRAPING


# DEPLOYMENT

def deploy():
    """Deploy the application.

    Tasks:

    1. Copy dist package to remote host
    2. Install dist package
    3. Install requirements
    """
    info('Start deploying application')

    info('Copy dist package to the remote host')
    copy_dist_package()

    info('Install application')
    install_dist_package()

    info('Restarting application')
    restart_app()

    info('DONE - deploying application')

# END DEPLOYMENT
