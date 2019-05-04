install:
	# preinstall GRPC dependancies
	@pip install grpcio grpcio-tools
	# install package
	@python setup.py install

protos:
	@python setup.py build_proto_modules

wheel:
	@echo "Building python project..."
	@python setup.py bdist_wheel

sdist:
	@echo "Building python project..."
	@python setup.py sdist

server:
	@grpc_ping_pong_server

# ╰─ make client client_params='--message "hello, toto!" --delaySeconds 0.5' 
# Received message 'hello, toto!', delaying 0.5s...
# 2019-05-04 15:48:00,832 - grpc.pingpong.client - INFO - Thanks, friend!
# client_params:="--help"
client:
	@grpc_ping_pong_client ${client_params}

clean-cache:
	@find . -name "*.pyc" -exec rm -Rf {} \;
	@find . -type d -name "__pycache__" -exec rm -Rf {} \;

clean-protos:
	@find . -name "*pb2*" -exec rm -Rf {} \;

fclean: clean-protos clean-cache
	@rm -Rf build dist
