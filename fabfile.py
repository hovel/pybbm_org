#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'

from fabric.api import *


PROJECT_NAME = 'pybbm'
PROJECT_PROCESS = 'pybbm'

PROJECT_BASEDIR = '/home/zeus/webapps/%s' % PROJECT_PROCESS
PROJECT_ROOT = '/home/zeus/webapps/%s/%s'% (PROJECT_PROCESS, PROJECT_NAME)
PROJECT_SOURCE = 'ssh://hg@bitbucket.org/zeus/%s' % PROJECT_NAME
#noinspection PyRedeclaration
env.hosts = ['zeus@web223.webfaction.com']


def install():
    with cd(PROJECT_BASEDIR):
        run('hg clone %s' % PROJECT_SOURCE)
        run('virtualenv env')
        run('pip-2.7 -E env install -r %s/build/pipreq.txt' % PROJECT_NAME)

def fu():
    local('./manage.py test pybb')
    with cd(PROJECT_ROOT):
        run('hg pull')
        run('hg update -C default')
        run('pip -E ../env install -e hg+http://bitbucket.org/zeus/pybb#egg=pybb --upgrade --no-deps')
        run('../env/bin/python manage.py syncdb')
        run('../env/bin/python manage.py migrate')
        run('../env/bin/python manage.py collectstatic --noinput')
        run('/home/zeus/webapps/%s/gunicorn.sh restart' % PROJECT_PROCESS)