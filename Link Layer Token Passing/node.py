import random
import sys
import socket
import time

def main():
    print("Link Layer Token Passing")
    print("-----------------------------------\n") 
    n = list(sys.argv)                                                                
    sendPort = int(n[1])                                            #takes arguments from the command line to use as variables
    recievePort = int(n[2])
    buffer = int(n[3])
    isHead = int(n[4])
    nodeNum = int(n[5])
    host = socket.gethostname()
    connectionIn = (host,recievePort)
    connectionOut = (host,sendPort)
    Socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # outSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    Socket.bind(connectionIn)
    # outSocket.bind(connectionOut)
    # Socket.connect((connectionIn))
    # outSocket.connect((connectionOut))
    print("Node is starting")
    if (isHead == 1):
            print("I am starting with the token!")
            input("Waiting to send until ring is set up... Press enter to start the head")

    while (True):
        if (isHead == 1):
            time.sleep(1)
            if buffer == 0:
                print("I have nothing to send... sending token to next node")
                Socket.sendto(str("token").encode(), connectionOut)
                isHead =0
            else:
                print("Sending packet out to internet...")
                buffer-=1
                Socket.sendto(str("packet").encode(),connectionOut)
                print("Packet Sent")
                Socket.sendto(str("token").encode(),connectionOut)
                print("Token Passed")
                isHead=0
        else:
            print("waiting")
            data = Socket.recvfrom(1024)
            # data = data.decode()
            # print("data recieved, data: ", data)
            value = data[0].decode()
            # print(data[0].decode())
            # if 'token' in data[0].decode():
            #     print("TRUE")
            if value == "packet":
                print("Packet recieved")
                if random.SystemRandom().randrange(0,4) == 0:
                    print("Added to buffer")
                    buffer +=1
            if value == "token":
                print("Token recieved")
                isHead=1
            time.sleep(1)
main()