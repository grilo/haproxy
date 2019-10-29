#!/usr/bin/env bash

set -eu
set -o pipefail

haproxy-2.0.8/haproxy-bin/usr/local/sbin/haproxy -d -f config
