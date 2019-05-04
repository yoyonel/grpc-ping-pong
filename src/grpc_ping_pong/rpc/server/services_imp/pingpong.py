from time import sleep

from proto.ping_pb2 import Pong
from proto.ping_pb2_grpc import PingPongServicer


class PingPong(PingPongServicer):
    pong_return_msg = "Thanks, friend!"

    def SendPing(self, request, context):
        print(f"Received message '{request.message}', "
              f"delaying {request.delaySeconds}s...")

        if request.delaySeconds:
            sleep(request.delaySeconds)
        return Pong(message=self.pong_return_msg)
