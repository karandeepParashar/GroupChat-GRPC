import argparse
import server
import client
import proto.groupChat_pb2 as chat
import threading
import time
import os

def test_case_1():
  print("Running Test Case 1:")
  time.sleep(1)
  alice = client.Client(True, "1", 'localhost', 11912)
  sentMessage = "Hi, I am Alice."
  alice.sendMessage(sentMessage)
  print("Waiting for 5 seconds")
  time.sleep(5)
  bob = client.Client(True, "2", 'localhost', 11912)
  chad = client.Client(True, "3", 'localhost', 11912)
  print('Bob and Chad comes online.')
  time.sleep(1)
  print("Waiting for 1 second for Alice's message to be delievered")
  sender, recievedMessageBob = bob.receivedMessages[-1]
  sender, recievedMessageChad = chad.receivedMessages[-1]
  try:
    assert sentMessage == recievedMessageBob
    assert sentMessage == recievedMessageChad
    print("--- Test Case 1 Passed ---")
  except AssertionError:
      print("Test Case 1 Failed")
  return alice, bob, chad

def test_case_2(alice, bob, chad):
    print("Running Test Case 2:")
    newMessage = "Hi, I am Bob. This testing session has been a pleasure."
    bob.sendMessage(newMessage)
    print("Waiting for 1 second for Bob's Message to be delivered")
    time.sleep(1)
    senderAlice, recievedMessageAlice = alice.receivedMessages[-1]
    senderChad, recievedMessageChad = chad.receivedMessages[-1]
    senderBob, recievedMessageBob = bob.receivedMessages[-1]
    try:
        assert senderAlice == bob.clientId and recievedMessageAlice == newMessage
        assert senderChad == bob.clientId and recievedMessageChad == newMessage
        assert senderBob != bob.clientId and recievedMessageBob != newMessage
        print("--- Test Case 2 Passed ---")
    except AssertionError:
        print("Test Case 2 Failed")

def test_case_3(alice, bob, chad):
    print("Running Test Case 3:")
    newMessage = "It's me Alice again. Sending this for third test case."
    alice.sendMessage(newMessage)
    print("Waiting for 1 second for Alice's Message to be delivered")
    time.sleep(1)
    senderAlice, recievedMessageAlice = alice.receivedMessages[-1]
    senderChad, recievedMessageChad = chad.receivedMessages[-1]
    senderBob, recievedMessageBob = bob.receivedMessages[-1]
    try:
        assert senderAlice != alice.clientId and recievedMessageAlice != newMessage
        assert senderChad == alice.clientId and recievedMessageChad == newMessage
        assert senderBob == alice.clientId and recievedMessageBob == newMessage
        print("--- Test Case 3 Passed ---")
    except AssertionError:
        print("Test Case 3 Failed")

def test_case_4():
    time.sleep(1)
    print("Running Test Case 4:")
    doug = client.Client(True, "4", 'localhost', 11912)
    print("Doug comes online.")
    senderAlice, recievedMessageAlice = alice.receivedMessages[-1]
    senderChad, recievedMessageChad = chad.receivedMessages[-1]
    senderBob, recievedMessageBob = bob.receivedMessages[-1]
    try:
        assert len(doug.receivedMessages) == 0
        print("--- Test Case 4 Passed ---")
    except AssertionError:
        print("Test Case 4 Failed")
    return doug

def test_case_5(alice, bob, chad, doug):
    print("Running Test Case 5:")
    newMessage = "It's me Doug. I'm an outsider, checking if I can reach anyone."
    doug.sendMessage(newMessage)
    print("Waiting for 1 second for Doug's Message to be attempt delivery")
    time.sleep(1)
    senderAlice, recievedMessageAlice = alice.receivedMessages[-1]
    senderChad, recievedMessageChad = chad.receivedMessages[-1]
    senderBob, recievedMessageBob = bob.receivedMessages[-1]
    try:
        assert senderAlice != doug.clientId and recievedMessageAlice != newMessage
        assert senderChad != doug.clientId and recievedMessageChad != newMessage
        assert senderBob != doug.clientId and recievedMessageBob != newMessage
        print("--- Test Case 5 Passed ---")
    except AssertionError:
        print("Test Case 5 Failed")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Group Chat Server by Karandeep Parashar"
    )
    parser.add_argument('-p', '--port', help = 'Port', default= 11912)
    parser.add_argument('-i', '--server_ip', help = 'IP-Address', default= '0.0.0.0')
    args = parser.parse_args()
    port = args.port
    serve = server.GrpcServer(11912, [1,2,3])
    serverThread = threading.Thread(target = serve.startServer, args= [], daemon = True)
    serverThread.start()
    alice, bob, chad = test_case_1()
    test_case_2(alice, bob, chad)
    test_case_3(alice, bob, chad)
    doug = test_case_4()
    test_case_5(alice, bob, chad, doug)
    os._exit(0)