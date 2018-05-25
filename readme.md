# docker-swarm-deploy

Quick start to get a local swarm up and running

## Quick Start

1. Locate the local interface IP address.

```
$ ifconfig en1
en1: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	inet6 fe80::1837:c97f:df86:c36f%en1 prefixlen 64 secured scopeid 0xa 
-->>inet 192.168.0.34 netmask 0xffffff00 broadcast 192.168.0.255
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active
```

In the above case the IP address of the local interface is "192.168.0.34"

2. Modify the .env file at the same level of the docker-compose to include the local interface IP

$ cat .env

```
...
LOCAL_IP=192.168.0.34
...
```

3. Create an account with Etherscan: https://etherscan.io/register

4. Create an Etherscan API KEY by clicking Developers->API-KEYs

5. Modify the .env file at the same level of the docker-compose to include the API key

```
...
ETHEREUM_IO_API_TOKEN=***********************
...
```

6. Modify the .env file at the same level of the docker-compose to include a Ethereum mainnet address that contains tokens or use the sample address provided below

```
...
ETHEREUM_ADDRESS=0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a
...
```
7. Launch the swarm inside docker using the compose file.

```
$ docker-compose up
```
