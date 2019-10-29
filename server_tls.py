#!/usr/bin/env python

import logging
import argparse
import socket
import ssl


protocol = {
    "1.0": ssl.PROTOCOL_TLSv1,
    "1.1": ssl.PROTOCOL_TLSv1_1,
    "1.2": ssl.PROTOCOL_TLSv1_2,
}

def server(hostname, port, tls_version):

    server_listen = (hostname, port)

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((hostname, port))
    sock.listen(1)
    logging.info("Server listening on: %s", server_listen)

    while True:
        try:
            client_socket, client_address = sock.accept()
            ssl_socket = ssl.wrap_socket(client_socket,
                                         server_side=True,
                                         certfile="mydomain.pem",
                                         cert_reqs=ssl.CERT_NONE,
                                         ssl_version=protocol.get(tls_version))
        except ssl.SSLError as e:
            logging.debug("Handshake: %s", e)
            continue

        logging.info("Client connected: %s (%s)", client_address, ssl_socket.cipher())
        ssl_socket.close()

if __name__ == "__main__":

    desc = "Basic TLS test server."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-s', '--server',
                        help="Server hostname to bind to.",
                        default='localhost')
    parser.add_argument('-t', '--tls',
                        help="TLSvX to use (%s)." % (','.join(protocol.keys())),
                        required=True)
    parser.add_argument('-p', '--port',
                        help="Server port to bind to.",
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

    server(args.server, int(args.port), args.tls)
