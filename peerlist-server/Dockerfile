FROM ubuntu:16.04
MAINTAINER support@bluzelle.com

RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
        gettext-base \
        python

EXPOSE 8080
RUN mkdir -p /var/www

COPY templates/peerlist.json.template /tmp/peerlist.json.template

ENTRYPOINT envsubst < /tmp/peerlist.json.template > /var/www/peerlist.json \
    && cd /var/www \
    && python -m SimpleHTTPServer 8080



