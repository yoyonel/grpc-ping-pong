"""
"""
from grpc_ping_pong.rpc.server.services_imp.pingpong import PingPong

from proto.ping_pb2 import Ping
from tests.conftest import CatchTime


def test_search_server(core_rpc_stub):
    # construct Ping message
    delay_seconds = 0.142
    ping = Ping(message="test", delaySeconds=delay_seconds)
    with CatchTime() as t:
        # Sending Ping message and retrieve pong response
        msg_pong = core_rpc_stub.SendPing(ping)
        assert msg_pong.message == PingPong.pong_return_msg
    assert float(t) > delay_seconds
