from concurrent import futures
import grpc
import logging
import os
import signal
import sys
from time import sleep

from proto.ping_pb2_grpc import add_PingPongServicer_to_server

from grpc_ping_pong.rpc.server.services_imp.pingpong import PingPong


logger = logging.getLogger('pythie.storage.server.daemon')


SIGNALS = [signal.SIGINT, signal.SIGTERM]


def _signal_handler(sig, stack):
    """ Empty signal handler used to override python default one """
    pass


def serve(
    block=True,
    grpc_host_and_port=os.environ.get("GRPC_PING_PONG_GRPC_HOST_AND_PORT", '[::]:50051')
):
    """
    Start a new instance of the ping pong service.

    If the server can't be started, a ConnectionError exception is raised

    :param block: If True, block until interrupted. If False, start the server and return directly
    :type block: bool

    :param grpc_host_and_port:
    :type grpc_host_and_port: str

    :return: If ``block`` is True, return nothing. If ``block`` is False, return the server instance
    :rtype: None | grpc.server
    """

    # Register signal handler, only if blocking
    if block:
        for sig in SIGNALS:
            signal.signal(sig, _signal_handler)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_PingPongServicer_to_server(PingPong(), server)

    port = server.add_insecure_port(grpc_host_and_port)
    if port == 0:
        logger.error("Failed to start gRPC server on {}".format(grpc_host_and_port))
        raise ConnectionError

    logger.info("Starting pythie videomonitoring server on {}...".format(grpc_host_and_port))
    server.start()
    logger.info("Ready and waiting for connections.")

    if not block:
        return server

    # Wait for a signal before exiting
    sig = signal.sigwait(SIGNALS)
    logger.info('Signal {} received, shutting down...'.format(sig))

    server.stop(5).wait()


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    try:
        serve(block=True)
    except ConnectionError:
        sys.exit(1)


if __name__ == "__main__":
    main()
