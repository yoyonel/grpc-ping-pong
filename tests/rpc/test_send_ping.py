import pytest
import sys

import grpc_ping_pong.rpc.client.send_ping as send_ping


@pytest.mark.timeout(1)
def test_send_ping(core_rpc_stub, monkeypatch):
    with monkeypatch.context() as m:
        m.setenv('GRPC_PING_PONG_GRPC_HOST_AND_PORT',
                 f'localhost:{pytest.insecure_port}')
        m.setattr(sys, 'argv',
                  ['send_ping.py',
                   '--message', 'test', '--delaySeconds', '0.142'])
        #
        send_ping.main()
