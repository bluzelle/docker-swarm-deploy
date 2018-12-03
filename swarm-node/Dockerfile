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

ARG DEBIAN_COMPONENT=stable

RUN sh -c "echo 'deb https://bluzelle.jfrog.io/bluzelle/debian-local all $DEBIAN_COMPONENT' >> /etc/apt/sources.list"
RUN sh -c "echo 'deb http://ppa.launchpad.net/maarten-fonville/protobuf/ubuntu trusty main' >> /etc/apt/sources.list"


RUN set -x \
    && add-apt-repository ppa:ubuntu-toolchain-r/test \
    && apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates --allow-unauthenticated \
        bluzelle-swarmdb \
        libprotobuf-dev \
        protobuf-compiler \
        libstdc++6



ARG SWARM_NAME

RUN mkdir -p /opt/swarm_home
RUN cd /opt/swarm_home \
    && wget -c "https://raw.githubusercontent.com/bluzelle/swarmDB/devel/scripts/generate-key" \
    && chmod a+x generate-key


COPY templates/config.json.template /opt/swarm_home

WORKDIR /opt/swarm_home

ENTRYPOINT mkdir -p ${SWARM_NAME} \
    && echo "--- INTIAILIZING SWARM KEYS ---" \
    && bash /opt/swarm_home/generate-key /opt/swarm_home/${SWARM_NAME} \
    && cd ${SWARM_NAME} \
    && echo "--- CREATING SWARM CONFIGURATION ---" \
    && envsubst < /opt/swarm_home/config.json.template > /opt/swarm_home/${SWARM_NAME}/config-${SWARM_NAME}.json \
    && cat /opt/swarm_home/${SWARM_NAME}/config-${SWARM_NAME}.json \
    && echo "--- STARTING SWARM NODE ${SWARM_NAME} ---" \
    && swarm -c /opt/swarm_home/${SWARM_NAME}/config-${SWARM_NAME}.json
