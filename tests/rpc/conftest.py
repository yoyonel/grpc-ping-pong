import grpc
import pytest

from grpc_ping_pong.rpc.server.server import serve
from proto.ping_pb2_grpc import PingPongStub


@pytest.fixture(scope="session", autouse=True)
def start_core_rpc_server(request):
    """
    Spawn an instance of the rpc service, and close it at the end of test sessions
    :param request:
    :type request:
    :return:
    :rtype:
    """
    server, insecure_port = serve(block=False)
    assert server is not None
    pytest.insecure_port = insecure_port

    def _kill_server():
        server.stop(0)

    request.addfinalizer(_kill_server)


@pytest.fixture
def core_rpc_stub():
    """Create a new rpc stub and connect to the server"""
    channel = grpc.insecure_channel(
        f'localhost:{pytest.__dict__.get("insecure_port")}')
    return PingPongStub(channel)
