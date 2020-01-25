FROM golang:1.13-alpine as build-lmd
ENV LMD_VERSION=v1.8.1

RUN cd /go/src && \
    apk add git && \
    git clone --branch ${LMD_VERSION} --depth 1 https://github.com/sni/lmd.git app
RUN apk add build-base bash && \
    cd /go/src/app && \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 make

FROM alpine:3.10 as build-thruk

ENV THRUK_VERSION=v2.32

# install requirements for build
RUN apk add --no-cache --update \
      git build-base rsync perl perl-dev gd-dev zlib-dev jpeg-dev libpng-dev\
      freetype-dev expat-dev libwebp-dev mysql-dev findutils chrpath \
      perl-module-install perl-yaml perl-plack perl-file-remove perl-yaml-tiny \
      perl-file-slurp perl-date-calc perl-carp-clan py-yuicompressor

# clone thruk repos
RUN mkdir -p /usr/src/thruk && \
    cd /usr/src/thruk && \
    git clone --branch ${THRUK_VERSION} --depth 1 git://github.com/sni/thruk_libs.git && \
    git clone --branch ${THRUK_VERSION} --depth 1 git://github.com/sni/Thruk.git

# Build thruk libs
RUN cd /usr/src/thruk/thruk_libs && make

# Build Thruk UI
RUN apk add --no-cache --update bash
RUN cd /usr/src/thruk/Thruk && \
    ./configure --prefix=/opt/thruk --with-htmlurl=/ && \
    make && \
    PERL5LIB=/usr/src/thruk/thruk_libs/local-lib/dest/lib/perl5/ make staticfiles && \
    make install && \
    cp -a /usr/src/thruk/thruk_libs/local-lib/dest/lib/perl5/* /opt/thruk/share/lib/ && \
    chown 100.100 /opt/thruk/tmp /opt/thruk/var -R

COPY --from=build-lmd /go/src/app/lmd/lmd /opt/thruk/bin/lmd

FROM alpine:3.10

COPY --from=build-thruk /opt/thruk/ /opt/thruk/

RUN apk add --no-cache --update \
       apache2 apache-mod-fcgid \
       bash perl \
       python3 py3-jinja2 && \
    sed -i 's@^#LoadModule rewrite_module modules/mod_rewrite\.so@LoadModule rewrite_module modules/mod_rewrite.so@' /etc/apache2/httpd.conf

VOLUME /opt/thruk/var

CMD ["/opt/thruk/bin/docker_entrypoint.py"]

ADD log4perl.template.conf /opt/thruk/etc/log4perl.template.conf
ADD apache_thruk.template.conf /opt/thruk/etc/apache_thruk.template.conf
ADD thruk_local.template.conf /opt/thruk/etc/thruk_local.template.conf
ADD docker_entrypoint.py /opt/thruk/bin/docker_entrypoint.py
