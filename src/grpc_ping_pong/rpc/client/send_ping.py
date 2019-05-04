import argparse
import grpc
import logging
import os

from proto.ping_pb2 import Ping
from proto.ping_pb2_grpc import PingPongStub


logger = logging.getLogger('grpc.pingpong.client')


def process(args):
    """

    Env variables:
    - GRPC_PING_PONG_GRPC_HOST_AND_PORT (default='[::]:50051')

    Args:
        args (namedtuple):

    Returns:

    """
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    grpc_host_and_port = os.environ.get("GRPC_PING_PONG_GRPC_HOST_AND_PORT", '[::]:50051')
    logger.debug("grpc_host_and_port: {}".format(grpc_host_and_port))
    client = PingPongStub(grpc.insecure_channel(grpc_host_and_port))

    # construct Ping message
    ping = Ping(message=args.message, delaySeconds=args.delaySeconds)
    # Sending Ping message
    logger.debug("Send ping message:\n{}".format(ping))

    # Retrieve Pong response
    pong = client.SendPing(ping).message
    logger.debug("Returning pong message: {}".format(pong))

    logger.info(pong)


def build_parser(parser=None, **argparse_options):
    """

    Args:
        parser (argparse.ArgumentParser):
        **argparse_options (dict):

    Returns:

    """
    if parser is None:
        parser = argparse.ArgumentParser(**argparse_options)

    #
    parser.add_argument('--message',
                        type=str,
                        default="Hello world!",
                        help='message',
                        metavar='')
    #
    parser.add_argument('--delaySeconds', dest="delaySeconds",
                        default=1.0,
                        type=float,
                        help='delay seconds',
                        metavar='')
    # Options
    parser.add_argument("-v", "--verbose",
                        action="store_true", default=False,
                        help="increase output verbosity")
    # return parsing
    return parser


def parse_arguments():
    """

    Returns:
        argparse.Namespace:
    """
    # return parsing
    return build_parser().parse_args()


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    args = parse_arguments()
    process(args)


if __name__ == '__main__':
    main()
