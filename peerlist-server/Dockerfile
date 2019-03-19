FROM ubuntu:16.04
MAINTAINER support@bluzelle.com

RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
        gettext-base \
        python

EXPOSE 8080
RUN mkdir -p /var/www
RUN mkdir -p /opt/bluzelle/ \
    &&  mkdir -p /opt/bluzelle/swarm_home

COPY generate-config.py /opt/bluzelle/generate_config.py
RUN chmod a+x /opt/bluzelle/generate_config.py

ARG NUM_NODES

ENTRYPOINT /opt/bluzelle/generate_config.py -n ${NUM_NODES} \
    && envsubst < /opt/bluzelle/swarm_home/peerlist.json.template > /var/www/peerlist.json \
    && cd /var/www \
    && python -m SimpleHTTPServer 8080



