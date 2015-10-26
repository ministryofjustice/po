FROM phusion/baseimage:0.9.16

ENV DEBIAN_FRONTEND noninteractive

RUN add-apt-repository ppa:nginx/stable

RUN apt-get update

RUN apt-get -y install \
    binutils \
    build-essential \
    git-core \
    libpq-dev \
    nginx-full \
    python-dev \
    python-software-properties \
    software-properties-common \
    wget

# See Ubuntu bug #1306991 - can't use ubuntu provided pip
RUN curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python2.7

RUN mkdir -p /var/log/gunicorn /var/log/nginx/po
RUN touch /var/log/gunicorn/access.log /var/log/gunicorn/error.log
RUN chown -R www-data:www-data /var/log/gunicorn
RUN chmod -R g+s /var/log/gunicorn

ADD ./docker/nginx.conf /etc/nginx/nginx.conf

ADD ./docker/nginx.service /etc/service/nginx/run
ADD ./docker/gunicorn.service /etc/service/gunicorn/run

VOLUME ["/var/log/nginx", "/var/log/gunicorn"]

ENV APP_HOME /srv/po
WORKDIR ${APP_HOME}
ADD . ${APP_HOME}
RUN rm -rf ${APP_HOME}/.git
RUN chown -R www-data: ${APP_HOME}
RUN cd ${APP_HOME}
RUN pip install -r requirements.txt
RUN ./manage.py collectstatic --noinput

EXPOSE 80

CMD ["/sbin/my_init"]
