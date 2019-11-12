#!/usr/bin/env python3

import logging
import os
import subprocess
import sys
import json
import time
import random
import socket
import requests

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from http.server import HTTPServer, SimpleHTTPRequestHandler

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

no_gap_swarms = []

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

    ####Add node to BluzelleDockerSwarm
    node_name = "node_{}".format(node_id)
    node_host = "HOST_PUB_IP"
    node_port = 51010
    node_uuid = uuid

    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
        'X-API-Key': 'BLUZELLE_API_KEY'
    }

    data = {
            "host": node_host,
            "name": node_name,
            "port": node_port,
            "uuid": node_uuid
    }
    response = requests.patch('https://cpr.bluzelle.com/api/v1/swarms/SWARM_NODE_NAME', headers=headers, data=data)

    if response.status_code == 200:
      logger.debug("Peer Added to CPR")
    else:
      logger.debug("Something went wrong, did not add node to CPR")

def make_node_config(node_id, same_port=False):
  return {
      "swarm_id": "SWARM_NODE_NAME",
      "listener_address": "0.0.0.0",
      "listener_port": 51010,
      "bootstrap_url": "${SWARM_BOOTSTRAP_URL}",
      "debug_logging": "${NODE_DEBUG_LOGGING}",
      "log_to_stdout": True,
      "audit_enabled": True,
      "public_key_file": "/opt/bluzelle/swarm_home/node_{}/public-key.pem".format(node_id),
      "private_key_file": "/opt/bluzelle/swarm_home/node_{}/private-key.pem".format(node_id),
      "crypto_enabled_outgoing": True,
      "crypto_enabled_incoming": True,
      "chaos_testing_enabled": False,
      "monitor_address": "${STATSD_COLLECTOR}",
      "monitor_port": 8125,
      "stack": "SWARM_NODE_ENV",
      "monitor_max_timers" : 100,
      # "mem_storage": False
  }


def generate_configs(num_nodes, working_directory, same_port=False):
    peers=[]
    for node_id in range(0, num_nodes):
        node_id = "{0}_{1}".format(node_id,"SWARM_NODE_NAME")
        node_path = get_node_path(node_id, working_directory)
        try:
            os.mkdir(node_path)
        except OSError as e:
            print(str(e))
            logger.info("Config directory already exists for: {}".format(node_id))
            return

        run_command("openssl ecparam -name secp256k1 -genkey -noout -out {}/private-key.pem".format(node_path))
        run_command("openssl ec -in {0}/private-key.pem -pubout -out {0}/public-key.pem".format(node_path))

        # enter node info in CPR
        uuid = get_node_uuid(node_id, working_directory)
        make_peerlist_entry(uuid, node_id, same_port)

        # node config
        config = make_node_config(node_id, same_port)
        logger.debug("config: {}".format(json.dumps(config)))
        with open(os.path.join(get_node_path(node_id, working_directory), "bluzelle.json.template"), "w") as outfile:
            json.dump(config, outfile, sort_keys=True, indent=4, ensure_ascii=True)

    logger.info('')
    logger.info('')

    # create local peerslist (will always be one node unless another node is put up)
    headers = {
        'accept': 'application/json',
    }
    response = requests.get('https://cpr.bluzelle.com/api/v1/swarms', headers=headers)
    obj = json.loads(response.text)
    # this will be replaced by the bash script
    peers = obj["SWARM_NODE_NAME"]

    logger.debug(map(lambda peer: json.dumps(peer), peers))
    with open(os.path.join(working_directory, "peerlist.json"), "w") as outfile:
        json.dump(peers, outfile, ensure_ascii=True, sort_keys=True, indent=4)

    # for serving the newly created peerslist locally
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()

if __name__ == "__main__":

    parser = ArgumentParser(description="generate-config", formatter_class=RawDescriptionHelpFormatter)


    parser.add_argument("-o", "--output", type=str, default="/opt/bluzelle/swarm_home", help="output directory for generated configurations")
    parser.add_argument("-n", "--nodes", type=int, default=1, help="number of nodes to generate configurations")
    parser.add_argument("--sameport", action='store_true', help="Create a peerlist with all nodes on the same port")

    args = parser.parse_args()
    generate_configs(args.nodes, args.output, args.sameport)
