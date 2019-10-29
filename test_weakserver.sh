#!/usr/bin/env bash

set -eu
set -o pipefail


function connect() {
    local protocol="$1"
    local port="$2"
    echo "Testing TLS client: $protocol//$port"
    python client_tls.py -p $port -t $protocol
}

echo ""
echo "###########################"
echo "Test validates client TLS 1.2 connects"
echo "to server using TLS 1.1 through HAProxy."
echo "###########################"
echo ""

PORT=9000
TLS=1.1
echo "Running Weak Server on port $PORT with TLS $TLS"
python server_tls.py -p 9000 -t 1.1 &
WEAKSERVER=$!

echo "Starting HAProxy with weakserver (10000)"
haproxy-2.0.8/haproxy-bin/usr/local/sbin/haproxy -f weakserver &
HAPROXY=$!

echo "Waiting 2 seconds for startup..."
sleep 2
python client_tls.py -p 10000 -t 1.0 || echo "Test passed."
python client_tls.py -p 10000 -t 1.1 || echo "Test passed."
python client_tls.py -p 10000 -t 1.2 && echo "Test passed." || echo "Test failed."

echo "Shutting down HAProxy"
kill $HAPROXY

echo "Shutting down weakserver"
kill $WEAKSERVER
