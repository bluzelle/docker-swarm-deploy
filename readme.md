# docker-swarm-deploy

Quick start to get a local swarm up and running.

## Quick Start

1. Clone this repository.

2. Locate the local interface IP address.

```
$ ifconfig en1
en1: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	inet6 fe80::1837:c97f:df86:c36f%en1 prefixlen 64 secured scopeid 0xa
-->>inet 192.168.0.34 netmask 0xffffff00 broadcast 192.168.0.255
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active
```

In the above case, the IP address of the local interface is `192.168.0.34`.

If you do not see `inet <ipaddress>`, run `ifconfig` and comb through manually to find your local IP address.

3. Modify the .env file at the root of the repository to include the local interface IP.

```
...
LOCAL_IP=192.168.0.34
...
```

4. Create an account with Etherscan: https://etherscan.io/register

5. Create an Etherscan API KEY by clicking Developers -> API-KEYs.

6. Modify the .env to include the Api-Key Token.

```
...
ETHEREUM_IO_API_TOKEN=***********************
...
```

7. Modify the .env file to include an Ethereum mainnet address that contains tokens or use the sample address provided below.

```
...
ETHEREUM_ADDRESS=0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a
...
```
8. Launch the swarm inside docker using the compose file.

```
$ docker-compose pull && docker-compose run
```
