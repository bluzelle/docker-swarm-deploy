FROM ubuntu:14.04
MAINTAINER support@bluzelle.com

RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
        apt-transport-https \
        gettext-base \
        libjsoncpp-dev \
        software-properties-common \
        python-software-properties

RUN sh -c "echo 'deb https://bluzelle.jfrog.io/bluzelle/debian-local all stable' >> /etc/apt/sources.list"

RUN set -x \
    && add-apt-repository ppa:ubuntu-toolchain-r/test \
    && apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates --allow-unauthenticated \
        bluzelle-swarmdb \
        libstdc++6

ARG SWARM_NAME

COPY templates/config.json.template /tmp

RUN mkdir -p /tmp/swarm_home && cd /tmp/swarm_home

WORKDIR /tmp/swarm_home

ENTRYPOINT mkdir -p ${SWARM_NAME} \
    && cd ${SWARM_NAME} \
    && envsubst < /tmp/config.json.template > config-${SWARM_NAME}.json \
    && swarm -c config-${SWARM_NAME}.json
