from time import sleep

from proto.ping_pb2 import Pong
from proto.ping_pb2_grpc import PingPongServicer


class PingPong(PingPongServicer):
    def SendPing(self, request, context):
        print("Received message '{}', delaying {}s...".format(request.message, request.delaySeconds))
        if request.delaySeconds:
            sleep(request.delaySeconds)
        return Pong(message="Thanks, friend!")
