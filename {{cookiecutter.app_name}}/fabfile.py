#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
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

Examples:

- https://github.com/disassembler/fabric-example/blob/master/fabfile.py
- https://gist.github.com/starenka/1225493
- http://prakhar.me/articles/flask-on-nginx-and-gunicorn/
"""
import os

from fabric.contrib.console import confirm
from fabric.api import abort, env, local, settings, task, sudo, cd, lcd, put, run, prefix, get
from fabric.colors import red, green
from fabric.contrib.files import exists

from {{cookiecutter.app_name}} import __version__


########## CONFIG

env.user = 'xxxxx' # Change: user used for deployment
env.hosts = ['xxxxx', 'xxxxx'] # Change: hosts to deploy to
env.activate = "source %s/%s" % (remote_app_dir, "env/bin/activate")

app_name = '{{cookiecutter.app_name}}'

local_app_dir = '.'
local_config_dir = './config'

remote_app_home_dir = '/opt'
remote_app_dir = os.path.join(remote_app_home_dir, '{{cookiecutter.app_name}}')
remote_log_dir = os.path.join('/var/log', '{{cookiecutter.app_name}}')
remote_tmp_dir = '/tmp'

dist_package_name = "{}-{}.tar.gz".format(app_name, __version__)
dist_package_file = "{}/{}".format(remote_tmp_dir, dist_package_name)

########## END CONFIG


########## HELPERS

def info(message):
    """Print info message."""
    print(green(message))


def package_installed(pkg_name):
    """ref: http:superuser.com/questions/427318/#comment490784_427339"""
    cmd_f = 'dpkg-query -l "%s" | grep -q ^.i'
    cmd = cmd_f % (pkg_name)
    with settings(warn_only=True):
        result = sudo(cmd)
    return result.succeeded


def yes_install(pkg_name):
    """ref: http://stackoverflow.com/a/10439058/1093087"""
    sudo('apt-get --force-yes --yes install %s' % (pkg_name))

########## END HELPERS

########## BOOTSTRAPING HELPERS

PACKAGES = (
    'python',
    'python-dev',
    'python-pip',
    'python-virtualenv',
    'nginx',
    'supervisor',
)


def install_packages():
    """ Install required packages. """
    sudo('apt-get update')
    for package in PACKAGES:
        if not package_installed(package):
            yes_install(package)


def create_app_dir():
    """ Create the application directory and setup a virtualenv.
    """
    # create app dir
    if exists(remote_app_dir) is False:
        sudo('mkdir -p ' + remote_app_dir)

    # create virtual env
    with cd(remote_app_dir):
        if exists(remote_app_dir + '/env') is False:
            sudo('virtualenv env')

    # Change permissions
    sudo('chown pi:pi ' + remote_app_dir + ' -R')

    # Create log dir
    if exists(remote_log_dir) is False:
        sudo('mkdir %s' % (remote_log_dir))


########## END BOOTSTRAPING HELPERS


########## DEPLOYMENT HELPERS

def pack():
    """Create a new source distribution as tarball."""
    local('python setup.py sdist --formats=gztar', capture=False)


def copy_dist_package():
    """Copy the dist package to the remote host(s)."""
    put('./dist/%s' % (dist_package_name), remote_tmp_dir)


def install_dist_package():
    """Install the dist package on the remote host(s)."""
    with cd(remote_app_dir):
        with prefix(env.activate):
            sudo('pip install %s' % (dist_package_file))

    # remove dist package
    run('rm %s' % (dist_package_file))


def copy_migrations():
    """Copy migration scripts to remote host"""
    local('tar czf migrations.tar.gz migrations', capture=False)
    put('migrations.tar.gz', remote_app_dir, use_sudo=True)

    with cd(remote_app_dir):
        sudo('rm -rf migrations')
        sudo('tar xzf migrations.tar.gz')
        sudo('rm migrations.tar.gz')

    local('rm migrations.tar.gz')


def change_permissions():
    sudo('chown {}:{} {} -R'.format(run_user, run_user, remote_app_dir))

########## END DEPLOYMENT HELPERS


########## Supervisor

def status():
    """Return the status of the app."""
    sudo('supervisorctl status')


def restart_app():
    """Restart the app."""
    sudo('supervisorctl restart {{cookiecutter.app_name}}')


def start_app():
    """Restart the app."""
    sudo('supervisorctl start {{cookiecutter.app_name}}')


def restart_app():
    """Restart the app."""
    sudo('supervisorctl restart {{cookiecutter.app_name}}')

########## END MANAGEMENT


########## BOOTSTRAPING

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


########## END BOOTSTRAPING


########## DEPLOYMENT

def deploy():
    """Deploy the application.

    Tasks:

    1. Copy dist package to remote host
    2. Install dist package
    3. Install requirements
    4. Run migrations
    """
    info("DEPLOYING APPLICATION")

    info("Copy dist package to the remote host")
    copy_dist_package()

    info("Install application")
    install_dist_package()

    # info("Install requirements")
    # install_requirements()

    change_permissions()

    info("Run migrations")
    copy_migrations()
    make_migrations()

    info("DONE DEPLOYING APPLICATION")


########## END DEPLOYMENT
