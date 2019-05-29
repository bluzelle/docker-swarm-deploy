FROM ubuntu:14.04
MAINTAINER support@bluzelle.com

RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
        apt-transport-https \
        gettext-base \
        libjsoncpp-dev \
        software-properties-common \
        python-software-properties \
        wget \
        libsnappy-dev

ARG DEBIAN_COMPONENT=unstable

RUN sh -c "echo 'deb https://bluzelle.jfrog.io/bluzelle/debian-local all $DEBIAN_COMPONENT' >> /etc/apt/sources.list"
RUN sh -c "echo 'deb http://ppa.launchpad.net/maarten-fonville/protobuf/ubuntu trusty main' >> /etc/apt/sources.list"


RUN set -x \
    && add-apt-repository ppa:ubuntu-toolchain-r/test \
    && apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates --allow-unauthenticated \
        bluzelle-swarmdb \
        libprotobuf-dev \
        protobuf-compiler \
        libstdc++6 \
        python3

ARG SWARM_NAME

RUN mkdir -p /etc/signalfx/

COPY signalfx/agent.yaml /etc/signalfx/agent.yaml

RUN mkdir -p /opt/bluzelle/ \
    &&  mkdir -p /opt/bluzelle/swarm_home

WORKDIR /opt/bluzelle/swarm_home/


ENTRYPOINT cd ${SWARM_NAME} \
    && echo "--- CREATING SWARM CONFIGURATION ---" \
    && envsubst < /opt/bluzelle/swarm_home/${SWARM_NAME}/bluzelle.json.template > /opt/bluzelle/swarm_home/${SWARM_NAME}/bluzelle.json \
    && cat /opt/bluzelle/swarm_home/${SWARM_NAME}/bluzelle.json \
    && echo "--- STARTING SWARM NODE ${SWARM_NAME} ---" \
    && swarm -c /opt/bluzelle/swarm_home/${SWARM_NAME}/bluzelle.json

