## gRPC Ping Pong

[gRPC](http://www.grpc.io/) is a high performance, 
open-source universal RPC framework that can help make your Python services blazing fast.
This is a bare bones example of creating and using a gRPC ping-pong service and client.

## Installing

Under a python virtualenv:
```bash
# mkvirtualenv -p /usr/bin/python3.7 p3.7_grpc-ping-pong

╰─ pip install grpcio grpcio-tools
Collecting grpcio
[...]
Successfully installed grpcio-1.20.1 grpcio-tools-1.20.1 protobuf-3.7.1 six-1.12.0

# install the package (build proto files)
╰─ python setup.py install
[...]
running build_proto_modules
creating build
creating build/lib
creating build/lib/grpc_ping_pong
copying src/grpc_ping_pong/__init__.py -> build/lib/grpc_ping_pong
creating build/lib/proto
copying src/proto/ping_pb2.py -> build/lib/proto
copying src/proto/__init__.py -> build/lib/proto
copying src/proto/ping_pb2_grpc.py -> build/lib/proto
[...]
```

## Running

Using console scripts entry points: `grpc_ping_pong_server` and `grpc_ping_pong_client`

### In one terminal, launch the GRPC server:
```
╰─ grpc_ping_pong_server
2019-05-04 14:58:30,537 - pythie.storage.server.daemon - INFO - Starting pythie videomonitoring server on [::]:50051...
2019-05-04 14:58:30,538 - pythie.storage.server.daemon - INFO - Ready and waiting for connections.
[...]
Received message 'hello, grpc!', delaying 1.0s...
```

### In another terminal, launch a (ping-pong) client:
```
╰─ grpc_ping_pong_client --message 'hello, grpc!' --delaySeconds 1.0 -v
2019-05-04 15:03:29,708 - grpc.pingpong.client - DEBUG - grpc_host_and_port: [::]:50051
2019-05-04 15:03:29,709 - grpc.pingpong.client - DEBUG - Send ping message:
message: "hello, grpc!"
delaySeconds: 1.0

2019-05-04 15:03:30,713 - grpc.pingpong.client - DEBUG - Returning pong message: Thanks, friend!
2019-05-04 15:03:30,713 - grpc.pingpong.client - INFO - Thanks, friend!
```

## Using Makefile

```sh
################
# Installation
################
╰─ make install

################
# Running
################
# - Server
╰─ make server

# - Client
╰─ make client
```

## Credits

Initial version from
https://github.com/lasergnu/grpc-ping-pong