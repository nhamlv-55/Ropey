# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc

import indgen_conn_pb2
import indgen_conn_pb2_grpc


class Greeter(indgen_conn_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return indgen_conn_pb2.HelloReply(message='Hello, %s!' % request.name)

    def SendLemma(self, request, context):
        print(request.lemma)
        return indgen_conn_pb2.Ack(ack_message='Ack!')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    indgen_conn_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

# get the seed smt2




if __name__ == '__main__':
    logging.basicConfig()
    serve()
