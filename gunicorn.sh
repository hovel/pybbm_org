#!/bin/bash

#   ~~~~~~~~~~~
#
#   Script to control gunicorn for start, stop, reload etc.
#
#   Usage:
#       $ ./gunicorn.sh {start|stop|restart|reload|status}
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# *** change these paths ***
VIRTUAL_ACTIVATE=/home/zeus/.virtualenvs/pybbmorg/bin/activate
SITE_INSTANCE=/home/zeus/pybbmorg
# -----------------------------------------------------------------------------

CONFIG_FILE=/home/zeus/pybbmorg/conf/gunicorn.conf.py
LOG_FILE=/home/zeus/logs/pybbmorg-error.log
PID_FILE=/home/zeus/pybbmorg/wsgi.pid
CALL_INFO="$0 $*"


if [ $(whoami) == 'root' ]; then
    info "Error: Don't run this script as 'root' !"
    exit 1
fi


function verbose_eval {
    echo "--------------------------------------------------------------------"
    echo $*
    echo "--------------------------------------------------------------------"
    eval $*
}


function tail_log {
    sleep 5
    (
        set -x
        tail ${LOG_FILE}
    )
}


function do_start {
    logger start gunicorn by ${CALL_INFO}
    verbose_eval source ${VIRTUAL_ACTIVATE}
    (
        cd ${SITE_INSTANCE}
        python manage.py run_gunicorn -c ${CONFIG_FILE}
    )
    echo "gunicorn start..."
    tail_log
}


function do_stop {
    logger stop gunicorn by ${CALL_INFO}
    if [ -f ${PID_FILE} ]; then
        PID=`cat ${PID_FILE}`
        rm ${PID_FILE}
        (
            set -x
            kill -15 $PID
        )
        sleep 1
    else
        echo "PID file '${PID_FILE}' not exists."
    fi
    echo "gunicorn stopped..."
    tail_log
}

function do_reload {
    logger reload gunicorn by ${CALL_INFO}
    if [ -f ${PID_FILE} ]; then
        PID=`cat ${PID_FILE}`
        (
            set -x
            kill -HUP $PID
        )
    else
        echo "Error: PID file '${PID_FILE}' not exists!"
    fi
    echo "gunicorn reload..."
    tail_log
}


function do_status {
    echo call info: ${CALL_INFO}
    (
        set -x
        netstat --protocol=unix -nlp | grep python
        tail ${LOG_FILE}
    )
}

case "$1" in
    start)
        do_start
        ;;
    stop)
        do_stop
        ;;
    status)
        do_status
        ;;
    restart)
        do_stop
        do_start
        ;;
    reload)
        do_reload
        ;;
    *)
        echo $"Usage: $0 {start|stop|restart|reload|status}"
        exit 1
esac
