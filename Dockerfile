FROM python:3.7

RUN set -ex \
    && RUN_DEPS=" locales " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

RUN echo es_CL.UTF-8 UTF-8 >> /etc/locale.gen && locale-gen

ADD requirements.txt /requirements.txt

RUN set -ex \
    && BUILD_DEPS=" build-essential " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install -U pip \
    && pip install --no-cache-dir -r /requirements.txt \
    \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /code/
ADD . /code/

ENV FLASK_ENV=development
ENV FLASK_APP=/code/app.py


