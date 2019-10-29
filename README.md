# HAProxy test

## Why?

Basic tests of a very basic sidecar pattern with HAProxy, no
containers were harmed during the making of these scripts.

Everything below was tested in Ubuntu 19.04.

Note: the scripts aren't very robust. The test_* ones are
particularly finnicky and may leave processes stranded if they
don't terminate correctly.

## Getting started

Generate a self-signed certificate:

```
bash selfsigned.sh
```

Download and build a static version of HAProxy:
```
bash build.sh
```

## Run tests

### Offload
The file `test_weakserver.sh` is evidence a client using a higher TLS version
is able to connect to a server using a weaker cypher. This is called "Offloading".

```
bash test_weakserver.sh
```

### Bridge
The file `test_strongserver.sh` is evidence a client using a lower TLS version
is able to connect to a server using a stronger cypher. This is called "Bridging".

See: https://www.haproxy.com/documentation/haproxy/deployment-guides/tls-infrastructure/
