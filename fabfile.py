#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'

from fabric.api import *


PROJECT_NAME = 'pybbm_org'
PROJECT_PROCESS = 'pybbm'

PROJECT_BASEDIR = '/home/zeus/webapps/%s' % PROJECT_PROCESS
PROJECT_ROOT = '/home/zeus/webapps/%s/%s'% (PROJECT_PROCESS, PROJECT_NAME)
PROJECT_SOURCE = 'git@github.com:hovel/%s.git' % PROJECT_NAME
#noinspection PyRedeclaration
env.hosts = ['zeus@pybbm.org']


def install():
    with cd(PROJECT_BASEDIR):
        run('git clone %s' % PROJECT_SOURCE)
        run('virtualenv env')
        run('pip-2.7 -E env install -r %s/build/pipreq.txt' % PROJECT_NAME)

def fu():
    local('./manage.py test pybb')
    with cd(PROJECT_ROOT):
        run('git fetch')
        run('git checkout origin/master')
        run('pip -E ../env install pybbm --upgrade --no-deps')
        run('../env/bin/python manage.py syncdb')
        run('../env/bin/python manage.py migrate')
        run('../env/bin/python manage.py collectstatic --noinput')
        run('/home/zeus/webapps/%s/gunicorn.sh restart' % PROJECT_PROCESS)