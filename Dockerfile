FROM zeus/django-base:latest
MAINTAINER Sergey Fursov <geyser85@gmail.com>

ADD build/hovel-build /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa

ADD . /root/src/
RUN pip install -r /root/src/build/pipreq.txt -U

ADD build/supervisor.conf /etc/supervisor/conf.d/
