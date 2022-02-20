from concurrent import futures
from urllib import response
import logging

import grpc
import argparse
import proto.groupChat_pb2 as groupChat
import proto.groupChat_pb2_grpc as rpc

class GroupChatServer(rpc.GroupChatServerServicer):
    #Constructor to initialize the group and history of chat
    def __init__(self, group):
        self.history = []
        self.group = [int(clientId) for clientId in group]
    
    #Method to send the stream of messages to all clients that are in group and listening
    def msgStream(self, request, context):
        ptr = 0
        flag = True
        if int(request.clientId) not in self.group:
            flag = False
        while flag:
            while ptr < len(self.history):
                text = self.history[ptr]
                ptr += 1
                if int(text.clientId) == int(request.clientId):
                    continue
                yield text
    
    #Method that recieves the message from user and add it to history and replies with a recived response
    def SendMsg(self, request, context):
        if int(request.clientId) in self.group:
            logging.info(request)
            print(request)
            self.history.append(request)
        response = groupChat.Blank()
        response.received = True
        return response

class GrpcServer:
    #Server initialization
    def __init__(self, port = 11912, clientIds = [1,2,3]) -> None:
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        rpc.add_GroupChatServerServicer_to_server(GroupChatServer(clientIds), self.server)
        self.server.add_insecure_port('0.0.0.0:' + str(port))
    
    #Server start method
    def startServer(self):
        logging.basicConfig(filename='serverLogs.log', level=logging.INFO)
        print('Starting server. Listening...')
        logging.info('Starting server. Listening...')
        self.server.start()
        self.server.wait_for_termination()
    
    #Server stop method
    def stopServer(self):
        self.server.stop(grace=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Group Chat Server by Karandeep Parashar"
    )
    parser.add_argument('-p', '--port', help = 'Port', default= 11912)
    parser.add_argument('-c','--clientIds', nargs="+", help = "Client Group", default=[1, 2, 3])
    args = parser.parse_args()
    port = args.port
    serve = GrpcServer(port, args.clientIds)
    serve.startServer()