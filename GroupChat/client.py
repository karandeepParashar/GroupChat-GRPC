import threading
from tkinter import *
from tokenize import String
import os
import grpc
import argparse
import proto.groupChat_pb2 as groupChat
import proto.groupChat_pb2_grpc as rpc
import logging

class Client:
    #Constructor for intializing class level variables opening connection with server
    def __init__(self, testMode, clientId, server_ip, port):
        self.testMode = testMode
        self.receivedMessages = []
        self.clientId = clientId
        channel = grpc.insecure_channel(server_ip + ':' + str(port))
        self.connection = rpc.GroupChatServerStub(channel)
        threading.Thread(target=self.__recieveIncomingMessages, daemon=True).start()
        if not testMode:
            #self.getInput()
            self.buildUI()
    
    #Build UI using Tkinter
    def buildUI(self):
        self.root = Tk()
        frame = Frame(self.root, width=350, height=350)
        frame.pack()
        self.root.withdraw()
        self.root.deiconify()
        self.window = frame
        self.__setup_ui()
        self.window.mainloop()
    
    #Method for incoming message Stream of messages from server
    def __recieveIncomingMessages(self):
        for text in self.connection.msgStream(groupChat.ClientInfo(clientId = self.clientId)):
            logging.info("Received: S[{}] {}".format(text.clientId, text.message))
            print("Received: S[{}] {}".format(text.clientId, text.message))
            if not self.testMode:
                self.chat_list.insert(END, "[{}] {}\n".format(text.clientId, text.message))
            self.receivedMessages.append((text.clientId, text.message))
    
    #Method to send messages to the server
    def sendMessage(self, message):
        if message is not '':
            text = groupChat.Msg()
            text.clientId = self.clientId
            text.message = message
            logging.info("Sent: S[{}] {}".format(text.clientId, text.message))
            print("Sent: S[{}] {}".format(text.clientId, text.message))
            if not self.testMode:
                self.chat_list.insert(END, "[{}] {}\n".format(text.clientId, text.message))
                self.entry_message.delete(0, END)
            response = self.connection.SendMsg(text)
    #Get message from UI to sendMessage
    def getMessageFromUI(self, event):
        message = self.entry_message.get()
        self.sendMessage(message)
    
    #Method to take input of text message from user
    def getInput(self):
        while True:
            txt = input("Enter your message!\n")
            if txt == "exit()":
                os._exit(0)
            self.sendMessage(txt)
    
    #Setup the variables and requirements for UI
    def __setup_ui(self):
        self.chat_list = Text()
        self.chat_list.pack(side=TOP)
        self.lbl_username = Label(self.window, text=self.clientId)
        self.lbl_username.pack(side=LEFT)
        self.entry_message = Entry(self.window, bd=5)
        self.entry_message.bind('<Return>', self.getMessageFromUI)
        self.entry_message.focus()
        self.entry_message.pack(side=BOTTOM)
    
    #Method to destroy the UI
    def destroyUI(self):
        self.root.destroy()
       
#Method to start the client
def startClient(testMode, clientId, server_ip = 'localhost', port = 11912):
    logging.basicConfig(filename='clientLogs.log', level=logging.INFO)
    log_text = "Client " + clientId + " starting....."
    logging.info(log_text)
    print(log_text)
    clientObj = Client(testMode, clientId, server_ip, port)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Group Chat Client by Karandeep Parashar"
    )
    parser.add_argument('-c', '--clientId', help = 'ClientId')
    parser.add_argument('-i', '--server_ip', help = 'IP-Address', default= 'localhost')
    parser.add_argument('-p', '--port', help = 'Port', default= 11912)
    args = parser.parse_args()
    testMode = False
    startClient(testMode, args.clientId, args.server_ip, args.port)