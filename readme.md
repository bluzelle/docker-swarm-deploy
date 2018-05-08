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
LOCAL_IP=192.168.0.34
```

3. Launch the swarm inside docker using the compose file.

```
$ docker-compose up
```