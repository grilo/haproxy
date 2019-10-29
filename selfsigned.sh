#!/usr/bin/env bash

set -eu
set -o pipefail

# Generate self-signed cert
openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
    -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=www.mydomain.com" \
    -keyout mydomain.key -out mydomain.crt

# Append KEY and CRT to mydomain.pem
bash -c 'cat mydomain.key mydomain.crt >> mydomain.pem'

# Specify PEM in haproxy config
echo "
listen haproxy
    bind 0.0.0.0:443 ssl crt mydomain.pem
"
