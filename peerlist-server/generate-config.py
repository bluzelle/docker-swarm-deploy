#!/usr/bin/env python2.7

import logging
import os
import subprocess
import sys
import json

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def run_command(command):
    logger.debug("Executing: {}".format(command))
    with open(os.devnull) as dev_null:
        subprocess.call(command, shell=True, stderr=dev_null, stdout=dev_null)


def get_node_path(node_id, working_directory):
    node_name = "node_{}".format(node_id)
    return os.path.join(working_directory, node_name)


def get_node_uuid(node_id, working_directory):
    node_name = "node_{}".format(node_id)
    node_path = os.path.join(working_directory, node_name)

    with open(os.path.join(node_path, "public-key.pem")) as node_pub_key:

        lines = []
        for line in node_pub_key:
            lines.append(line)

        node_uuid = "".join(map(lambda x: x.strip(), lines[1:-1]))
        logger.debug("uuid: {}".format(node_uuid))
        return node_uuid


def make_peerlist_entry(uuid, node_id, same_port=False):
    return {
        'name': "node_{}".format(node_id),
        'host': "${LOCAL_IP}",
        'port':  51010 + (0 if same_port else node_id),
        'http_port': 8080 + node_id,
        'uuid': uuid
    }


def make_node_config(node_id, same_port=False):
    return {
        "listener_address": "0.0.0.0",
        "listener_port": 51010,
        "ethereum": "${ETHEREUM_ADDRESS}",
        "ethereum_io_api_token": "${ETHEREUM_IO_API_TOKEN}",
        "bootstrap_url": "${SWARM_BOOTSTRAP_URL}",
        "debug_logging": "${NODE_DEBUG_LOGGING}",
        "log_to_stdout": True,
        "audit_enabled": True,
        "public_key_file": "/opt/bluzelle/swarm_home/node_{}/public-key.pem".format(node_id),
        "private_key_file": "/opt/bluzelle/swarm_home/node_{}/private-key.pem".format(node_id),
        "crypto_enabled_outgoing": True,
        "crypto_enabled_incoming": True,
        "chaos_testing_enabled": False,
        "monitor_address": "graphite",
        "monitor_port": 8125
    }


def generate_configs(num_nodes, working_directory, same_port=False):

    peers = []

    for node_id in range(0, num_nodes):
        node_path = get_node_path(node_id, working_directory)
        try:
            os.mkdir(node_path)
        except OSError:
            logger.info("Config directory already exists for: {}".format(node_id))
            return

        run_command("openssl ecparam -name secp256k1 -genkey -noout -out {}/private-key.pem".format(node_path))
        run_command("openssl ec -in {0}/private-key.pem -pubout -out {0}/public-key.pem".format(node_path))

        uuid = get_node_uuid(node_id, working_directory)

        peers.append(make_peerlist_entry(uuid, node_id, same_port))

        config = make_node_config(node_id, same_port)

        logger.debug("config: {}".format(json.dumps(config)))

        with open(os.path.join(get_node_path(node_id, working_directory), "bluzelle.json.template"), "w") as outfile:
            json.dump(config, outfile, sort_keys=True, indent=4, ensure_ascii=True)

    logger.debug(map(lambda peer: json.dumps(peer), peers))
    with open(os.path.join(working_directory, "peerlist.json.template"), "w") as outfile:
        json.dump(peers, outfile, ensure_ascii=True, sort_keys=True, indent=4)


if __name__ == "__main__":

    parser = ArgumentParser(description="generate-config", formatter_class=RawDescriptionHelpFormatter)


    parser.add_argument("-o", "--output", type=str, default="/opt/bluzelle/swarm_home", help="output directory for generated configurations")
    parser.add_argument("-n", "--nodes", type=int, default=3, help="number of nodes to generate configurations")
    parser.add_argument("--sameport", action='store_true', help="Create a peerlist with all nodes on the same port")

    args = parser.parse_args()
    generate_configs(args.nodes, args.output, args.sameport)





