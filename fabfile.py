#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'

from fabric.api import *


PROJECT_NAME = 'pybbm_org'
PROJECT_PROCESS = 'pybbm'

PROJECT_BASEDIR = '/home/geyser/%s' % PROJECT_NAME
PROJECT_ROOT = '/home/geyser/%s/%s' % (PROJECT_NAME, PROJECT_NAME)
PROJECT_SOURCE = 'git@github.com:hovel/%s.git' % PROJECT_NAME
env.hosts = ['geyser@ec2-50-17-136-53.compute-1.amazonaws.com']


def fu():
    with cd(PROJECT_ROOT):
        run('git fetch')
        run('git pull origin master')
        run('git checkout master')
        run('%s/env/bin/pip install -r %s/build/pipreq.txt -U' % (PROJECT_BASEDIR, PROJECT_ROOT))
        run('%s/env/bin/python %s/manage.py syncdb' % (PROJECT_BASEDIR, PROJECT_ROOT) )
        run('%s/env/bin/python %s/manage.py migrate' % (PROJECT_BASEDIR, PROJECT_ROOT))
        run('%s/env/bin/python %s/manage.py collectstatic --noinput' % (PROJECT_BASEDIR, PROJECT_ROOT))
        run('kill -HUP `cat %s/log/pidfile`' % PROJECT_BASEDIR)