#!/usr/bin/env python
from fabric.api import *
import urllib
import urllib2
import os
try:
    from statictv.settings import CLOUDFLARE_TOKEN, CLOUDFLARE_EMAIL
except ImportError:
    CLOUDFLARE_TOKEN = None
    CLOUDFLARE_EMAIL = None

PROJECT_NAME = 'pybbm_org'
HOME = '/home/zeus'
CONTROL_PATH = '%s/control' % HOME
PROJECT_SOURCE = 'git@github.com:hovel/pybbm_org.git'
PROJECT_BASEDIR = '%s/%s' % (HOME, PROJECT_NAME)
PYTHON_PATH = '%s/.virtualenvs/%s/bin/python' % (HOME, PROJECT_NAME)
PIP_PATH = '%s/.virtualenvs/%s/bin/pip' % (HOME, PROJECT_NAME)
env.use_ssh_config = True
env.sudo_user = 'zeus'

all_hosts = []
i = 1
while True:
    host = os.environ.get('HOST%s' % i)
    if host:
        all_hosts.append(host)
    else:
        break
    i += 1
env.hosts = all_hosts


def uninstall():
    with cd(HOME):
        sudo('rm -rf %s' % PROJECT_BASEDIR)


def install():
    with cd(HOME):
        sudo('mkvirtualenv %s' % PROJECT_NAME)
        sudo('git clone %s %s' % (PROJECT_SOURCE, PROJECT_NAME))
        sudo('touch %s/logs/%s.log' % (HOME, PROJECT_NAME))
        sudo('touch %s/logs/%s-error.log' % (HOME, PROJECT_NAME))
    update_settings()
    put_nginx_config()
    put_backup_script()
    put_supervisord_settings()
    update()
    start()


def update_repo():
    with cd(PROJECT_BASEDIR):
        sudo('git pull')
        sudo('git checkout master')


def update_requirements():
    with cd(PROJECT_BASEDIR):
        sudo('%s install -r build/pipreq.txt -U' % PIP_PATH)


def update_db():
    db_backup()
    with cd(PROJECT_BASEDIR):
        sudo('%s manage.py syncdb' % PYTHON_PATH)
        sudo('%s manage.py migrate' % PYTHON_PATH)


def update_static():
    with cd(PROJECT_BASEDIR):
        sudo('%s manage.py collectstatic --noinput' % PYTHON_PATH)


def update_settings():
    with cd(CONTROL_PATH):
        sudo('git pull')
    with cd(PROJECT_BASEDIR):
        sudo('cp %s/%s/settings_local.py %s/pybbm_org/settings_local.py' % (CONTROL_PATH, PROJECT_NAME, PROJECT_BASEDIR))


def update():
    update_repo()
    update_requirements()
    update_db()
    update_static()
    update_settings()
    restart()
    purge_cloudflare_static()


def start():
    with cd(PROJECT_BASEDIR):
        sudo('supervisorctl -c %s/supervisord/supervisord.conf start %s_gunicorn' % (HOME, PROJECT_NAME))


def stop():
    with cd(PROJECT_BASEDIR):
        sudo('supervisorctl -c %s/supervisord/supervisord.conf stop %s_gunicorn' % (HOME, PROJECT_NAME))


def restart():
    with cd(PROJECT_BASEDIR):
        sudo('supervisorctl -c %s/supervisord/supervisord.conf restart %s_gunicorn' % (HOME, PROJECT_NAME))


def db_backup():
    with cd(PROJECT_BASEDIR):
        sudo('./db_backup.sh')


def put_backup_script():
    with cd(CONTROL_PATH):
        sudo('git pull')
    with cd(PROJECT_BASEDIR):
        sudo('cp %s/%s/db_backup.sh %s/db_backup.sh' % (CONTROL_PATH, PROJECT_NAME, PROJECT_BASEDIR))


def put_supervisord_settings():
    with cd(CONTROL_PATH):
        sudo('git pull')
    with cd(PROJECT_BASEDIR):
        sudo('cp %s/%s/%s_sv.conf %s/supervisord/conf/%s_sv.conf' % (CONTROL_PATH, PROJECT_NAME, PROJECT_NAME, HOME, PROJECT_NAME))

    sudo('supervisorctl -c %s/supervisord/supervisord.conf reread' % HOME)
    sudo('supervisorctl -c %s/supervisord/supervisord.conf update' % HOME)


def put_nginx_config():
    with cd(CONTROL_PATH):
        sudo('git pull')
    with settings(sudo_user='root'), cd(CONTROL_PATH):
        sudo('cp %s/%s.conf /etc/nginx/conf.d/%s.conf' % (PROJECT_NAME, PROJECT_NAME, PROJECT_NAME))
        sudo('/etc/init.d/nginx restart')


def purge_cloudflare_static():
    token = os.environ.get('CLOUDFLARE_TOKEN', CLOUDFLARE_TOKEN)
    email = os.environ.get('CLOUDFLARE_EMAIL', CLOUDFLARE_EMAIL)
    if not token or not email:
        print 'purge static files failed'
        return

    response = urllib2.urlopen('https://www.cloudflare.com/api_json.html',
                               data=urllib.urlencode({
                                   'a': 'fpurge_ts',
                                   'tkn': token,
                                   'email': email,
                                   'z': 'pybbm.org',
                                   'v': '1'
                               }))
    print response.read()