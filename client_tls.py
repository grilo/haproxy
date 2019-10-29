#!/usr/bin/env python

import logging
import os
import argparse
import socket
import ssl
import sys


protocol = {
    "1.0": ssl.PROTOCOL_TLSv1,
    "1.1": ssl.PROTOCOL_TLSv1_1,
    "1.2": ssl.PROTOCOL_TLSv1_2,
}

def client(hostname, port, tls_version):

    if not tls_version in protocol:
        raise ValueError("Invalid protocol version: %s" % (tls_version))
    context = ssl.SSLContext(protocol.get(tls_version))
    context.verify_mode = ssl.CERT_NONE
    ssl_socket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

    try:
        # Connect the socket to the port on the server given by the caller
        logging.info("Client connecting to: %s", (hostname, port))
        ssl_socket.connect((hostname, port))
        logging.info("Server is using TLS: %s", tls_version)
        ssl_socket.send("Hello world!")
        ssl_socket.close()
        sys.exit(0)
    except ssl.SSLError:
        logging.warning("Server is NOT using TLS: %s", tls_version)
        sys.exit(1)

if __name__ == "__main__":

    desc = "Basic TLS test client."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-s', '--server',
                        help="Server hostname to connect to.",
                        default='localhost')
    parser.add_argument('-t', '--tls',
                        help="TLSvX to use (%s)." % (','.join(protocol.keys())),
                        required=True)
    parser.add_argument('-p', '--port',
                        help="Server port to connect to.",
                        required=True)
    parser.add_argument('-v', '--verbose',
                        help="Increase output verbosity.",
                        action='store_true')
    args = parser.parse_args()

    log_format = '%(asctime)s::%(levelname)s::%(module)s::%(message)s'
    logging.basicConfig(format=log_format)
    logging.getLogger().setLevel(logging.INFO)
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    client(args.server, int(args.port), args.tls)
