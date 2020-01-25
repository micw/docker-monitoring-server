FROM alpine:3.10

RUN apk add --update --no-cache icinga2
RUN mkdir -p /run/icinga2 && \
    chown icinga /run/icinga2

RUN icinga2 feature enable compatlog && \
    icinga2 feature enable checker

ADD features /etc/icinga2/features-enabled
ADD config/ /etc/icinga2/conf.d/


CMD icinga2 daemon

