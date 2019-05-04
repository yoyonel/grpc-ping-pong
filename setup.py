# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import sys
from distutils.command.build_py import build_py as _build_py
from distutils.command.sdist import sdist as _sdist

import setuptools
from setuptools import find_packages
from setuptools import setup
from setuptools.command.develop import develop as _develop

# Find if user has grpc available
try:
    from grpc_tools import command

    GRPC_INSTALLED = True
except ImportError:
    GRPC_INSTALLED = False


class BuildPackageProtos(setuptools.Command):
    """Command to generate project *_pb2.py modules from proto files."""

    description = 'build grpc protobuf modules'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if GRPC_INSTALLED:
            command.build_package_protos(self.distribution.package_dir[''])
        else:
            print("Warning: skipping generation of proto classes "
                  "because grpcio-tools is not installed", file=sys.stderr)


class BuildPyCommand(_build_py):
    """Custom build command."""

    def run(self):
        self.run_command('build_proto_modules')
        _build_py.run(self)


class DevelopCommand(_develop):
    """Custom develop command."""

    def run(self):
        self.run_command('build_proto_modules')
        _develop.run(self)


class SDistCommand(_sdist):
    """Custom sdist command."""

    def run(self):
        self.run_command('build_proto_modules')
        _sdist.run(self)


install_requires = [
    "grpcio",
    "grpcio-tools"
]

tests_requires = [
    "flake8",
    "flake8-html",
    "pytest",
    "pytest-cov",
    "pytest-html",
    "pytest-timeout",
    "tox",
]

# https://docs.python.org/3/distutils/setupscript.html
setup(
    name='grpc_ping_pong',
    version='0.1.0',
    license='None',
    description='This is a bare bones example of creating and using a gRPC ping-pong service and client.',
    author='Lionel ATTY, lasergnu',
    author_email='yoyonel@hotmail.com',
    url='https://github.com/lasergnu/grpc-ping-pong',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    # http://setuptools.readthedocs.io/en/latest/setuptools.html
    # https://github.com/pypa/sampleproject/issues/30
    # https://docs.python.org/3/distutils/sourcedist.html#the-manifest-in-template
    # https://stackoverflow.com/questions/24291695/cannot-include-non-python-files-with-setup-py
    include_package_data=True,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
    keywords=[],
    install_requires=install_requires,
    tests_require=tests_requires,
    extras_require={
        'develop': install_requires + tests_requires,
    },
    entry_points={
        'console_scripts': [
            'grpc_ping_pong_server = grpc_ping_pong.rpc.server.server:main',
            'grpc_ping_pong_client = grpc_ping_pong.rpc.client.send_ping:main',
        ]
    },
    cmdclass={
        'build_py': BuildPyCommand,
        'build_proto_modules': BuildPackageProtos,
        'develop': DevelopCommand,
        'sdist': SDistCommand
    }
)
