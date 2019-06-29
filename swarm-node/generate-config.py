#!/usr/bin/env python3

import logging
import os
import subprocess
import sys
import json
import web3
import time
import random
import socket

from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from web3.personal import Personal

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

# required to have these files in the peerlist-server directoryimport web3
# infura = infura link including API key
i = open("infura", "r")
w3 = Web3(HTTPProvider(i.readline()))

# web3pkey = private key (in hex) of ropsten account
# ropsten_account = wallet address in ropsten
f = open("web3pkey", "r")
ra = open("ropsten_account", "r")

acct = w3.eth.account.privateKeyToAccount(f.readline())
contract_address = Web3.toChecksumAddress(ra.readline())

abi = '''
[
    {
      "constant": true,
      "inputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "swarmList",
      "outputs": [
        {
          "name": "",
          "type": "string"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function",
      "signature": "0x1065707e"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "isActive",
      "outputs": [
        {
          "name": "",
          "type": "bool"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function",
      "signature": "0x22f3e2d4"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "ownerAddress",
      "outputs": [
        {
          "name": "",
          "type": "address"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function",
      "signature": "0x8f84aa09"
    },
    {
      "inputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "constructor",
      "signature": "constructor"
    },
    {
      "constant": false,
      "inputs": [
        {
          "name": "swarmID",
          "type": "string"
        },
        {
          "name": "swarmSize",
          "type": "uint256"
        },
        {
          "name": "swarmGeo",
          "type": "string"
        },
        {
          "name": "isTrusted",
          "type": "bool"
        },
        {
          "name": "swarmType",
          "type": "string"
        },
        {
          "name": "swarmCost",
          "type": "uint256"
        },
        {
          "name": "nodeList",
          "type": "string[]"
        }
      ],
      "name": "addSwarm",
      "outputs": [
        {
          "name": "success",
          "type": "bool"
        }
      ],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function",
      "signature": "0x8b0a5c90"
    },
    {
      "constant": false,
      "inputs": [
        {
          "name": "swarmID",
          "type": "string"
        }
      ],
      "name": "removeSwarm",
      "outputs": [
        {
          "name": "",
          "type": "bool"
        }
      ],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function",
      "signature": "0x1aa75a45"
    },
    {
      "constant": false,
      "inputs": [
        {
          "name": "swarmID",
          "type": "string"
        },
        {
          "name": "nodeHost",
          "type": "string"
        },
        {
          "name": "nodeName",
          "type": "string"
        },
        {
          "name": "nodePort",
          "type": "uint256"
        },
        {
          "name": "nodeUUID",
          "type": "string"
        }
      ],
      "name": "addNode",
      "outputs": [
        {
          "name": "success",
          "type": "bool"
        }
      ],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function",
      "signature": "0xd3e8abe0"
    },
    {
      "constant": false,
      "inputs": [
        {
          "name": "swarmID",
          "type": "string"
        },
        {
          "name": "nodeUUID",
          "type": "string"
        }
      ],
      "name": "removeNode",
      "outputs": [
        {
          "name": "",
          "type": "bool"
        }
      ],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function",
      "signature": "0xc324563a"
    },
    {
      "constant": true,
      "inputs": [
        {
          "name": "swarmID",
          "type": "string"
        }
      ],
      "name": "getNodeCount",
      "outputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function",
      "signature": "0x44be43cd"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "getSwarmCount",
      "outputs": [
        {
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function",
      "signature": "0xbf82a335"
    },
    {
      "constant": true,
      "inputs": [
        {
          "name": "swarmID",
          "type": "string"
        }
      ],
      "name": "getSwarmInfo",
      "outputs": [
        {
          "name": "size",
          "type": "uint256"
        },
        {
          "name": "geo",
          "type": "string"
        },
        {
          "name": "trust",
          "type": "bool"
        },
        {
          "name": "swarmtype",
          "type": "string"
        },
        {
          "name": "cost",
          "type": "uint256"
        },
        {
          "name": "nodelist",
          "type": "string[]"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function",
      "signature": "0x101c1360"
    },
    {
      "constant": true,
      "inputs": [
        {
          "name": "swarmID",
          "type": "string"
        },
        {
          "name": "nodeUUID",
          "type": "string"
        }
      ],
      "name": "getNodeInfo",
      "outputs": [
        {
          "name": "nodeCount",
          "type": "uint256"
        },
        {
          "name": "nodeHost",
          "type": "string"
        },
        {
          "name": "nodeName",
          "type": "string"
        },
        {
          "name": "nodePort",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function",
      "signature": "0xcc8575cb"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "getSwarmList",
      "outputs": [
        {
          "name": "",
          "type": "string[]"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function",
      "signature": "0x0043d7e7"
    },
    {
      "constant": true,
      "inputs": [
        {
          "name": "swarmID",
          "type": "string"
        }
      ],
      "name": "getNodeList",
      "outputs": [
        {
          "name": "",
          "type": "string[]"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function",
      "signature": "0x46e76d8b"
    },
    {
      "constant": false,
      "inputs": [],
      "name": "deactivateContract",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function",
      "signature": "0xbca353be"
    }
  ]
'''

contract_instance = w3.eth.contract(address=contract_address, abi=abi)
no_gap_swarms = []

def run_command(command):
  logger.debug("Executing: {}".format(command))
  with open(os.devnull) as dev_null:
      subprocess.call(command, shell=True, stderr=dev_null, stdout=dev_null)

def get_host_ip():
  return ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
    if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), 
    s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, 
    socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

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
    node_host = get_host_ip()
    # node_port = 51010 + (0 if same_port else node_id)
    node_port = 51010
    # node_http_port = 8080 + node_id
    # node_http_port = 8080
    node_uuid = uuid

    gas_price = w3.toWei(30, 'gwei')
    swarm_list = contract_instance.functions.getSwarmList().call()

    for swarm in swarm_list:
      if swarm != '' or swarm not in no_gap_swarms:
        no_gap_swarms.append(swarm)

    if "BluzelleDockerSwarm" not in no_gap_swarms:
      ####Add the BluzelleDockerSwarm test
      txn_add = contract_instance.functions.addSwarm("BluzelleDockerSwarm", 
      10,
      "REGION_COUNTRY",
      True,
      "Disk",
      10,
      []).buildTransaction({
        'chainId': 3,
        'nonce': w3.eth.getTransactionCount(acct.address, block_identifier="pending"),
        'gas': 500000,
        'gasPrice': gas_price
      })
      f = open("web3pkey", "r")
      signed_txn_add = w3.eth.account.signTransaction(txn_add, private_key=f.readline())
      tx_hash = w3.eth.sendRawTransaction(signed_txn_add.rawTransaction)
      logger.info('')
      logger.info('Adding Swarm...')
      tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash,timeout=600)
      logger.info('Finished adding of swarm.')

    logger.info('CURRENT SWARM LIST: {}'.format(no_gap_swarms))
    logger.info('NUMBER OF SWARMS: {}'.format(str(contract_instance.functions.getSwarmCount().call())))
    txn = contract_instance.functions.addNode("BluzelleDockerSwarm", 
    node_host,
    node_name,
    # node_http_port,
    node_port,
    node_uuid).buildTransaction({
      'chainId': 3,
      'nonce': w3.eth.getTransactionCount(acct.address, block_identifier="pending"),
      'gas': 500000,
      'gasPrice': gas_price
    })
    f = open("web3pkey", "r")
    signed_txn = w3.eth.account.signTransaction(txn, private_key=f.readline())
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    logger.info('')
    logger.info('Adding Node {} to Swarm...'.format(node_id))
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash,timeout=600)
    logger.info('Finished adding Node to Swarm.')

    return {
        'name': "node_{}".format(node_id),
        'host': "${LOCAL_IP}",
        'port':  51010,
        # 'http_port': 8080,
        'uuid': uuid
    }


def make_node_config(node_id, same_port=False):
    return {
        "swarm_id": "SWARM_NODE_NAME",
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
        "monitor_address": "${STATSD_COLLECTOR}",
        "monitor_port": 8125,
        "swarm_info_esr_address": "ESR_CONTRACT_ADDRESS",
        "stack": "SWARM_NODE_ENV",
        "monitor_max_timers" : 100
    }


def generate_configs(num_nodes, working_directory, same_port=False):
    peers = []
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

        uuid = get_node_uuid(node_id, working_directory)

        peers.append(make_peerlist_entry(uuid, node_id, same_port))

        config = make_node_config(node_id, same_port)

        logger.debug("config: {}".format(json.dumps(config)))

        with open(os.path.join(get_node_path(node_id, working_directory), "bluzelle.json.template"), "w") as outfile:
            json.dump(config, outfile, sort_keys=True, indent=4, ensure_ascii=True)

    logger.info('')
    logger.info('')

    no_gap_nodes = []
    swarm_nodes = contract_instance.functions.getNodeList("BluzelleDockerSwarm").call()
    
    for nodes in swarm_nodes:
      if nodes != '':
        no_gap_nodes.append(nodes)

    for swarm_node in no_gap_nodes:
      node_info = contract_instance.functions.getNodeInfo("BluzelleDockerSwarm",swarm_node).call()
      logger.info("--------ADDED NODE INFO TO ESR--------")
      logger.info('NODE UUID: {}'.format(swarm_node))
      logger.info('NODE HOST: {}'.format(str(node_info[1])))
      # logger.info('NODE HTTP PORT: {}'.format(str(node_info[2])))
      logger.info('NODE NAME: {}'.format(str(node_info[3])))
      logger.info('NODE PORT: {}'.format(str(node_info[4])))
      logger.info("--------------------------------------")

    logger.debug(map(lambda peer: json.dumps(peer), peers))
    with open(os.path.join(working_directory, "peerlist.json.template"), "w") as outfile:
        json.dump(peers, outfile, ensure_ascii=True, sort_keys=True, indent=4)


if __name__ == "__main__":

    parser = ArgumentParser(description="generate-config", formatter_class=RawDescriptionHelpFormatter)


    parser.add_argument("-o", "--output", type=str, default="/opt/bluzelle/swarm_home", help="output directory for generated configurations")
    parser.add_argument("-n", "--nodes", type=int, default=1, help="number of nodes to generate configurations")
    parser.add_argument("--sameport", action='store_true', help="Create a peerlist with all nodes on the same port")

    args = parser.parse_args()
    generate_configs(args.nodes, args.output, args.sameport)