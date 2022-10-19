import csv
import pickle
import random
import socket
import time
import sys
import packet

packet = packet.packet
def corruptOrNot(probability):
    return random.random() > probability

def recievedNAK(ob, prob, conn):
    ob = conn.recv(1024)
    ob = pickle.loads(ob)
    if(ob.get_AOK() == "NAK"):
        while (ob.get_AOK() == "NAK"):
            print("Recieved NAK from sequence number: ", ob.get_seqNum())
            ob.set_checkSum(corruptOrNot(prob))
            ob = pickle.dumps(ob)
            time.sleep(1)
            conn.send(ob)
            packetRecieve = conn.recv(1024)
            time.sleep(.1)
            ob = pickle.loads(packetRecieve)
    print("ACK from seq number ", ob.get_seqNum())
    return ob

def corruptPacketChecker(ob, conn):
    if(ob.get_checkSum() != True):
        while (ob.get_checkSum() != True):
                ob.set_AON("NAK")
                print(("Corrupted Packet Recieved, Sending NAK, Sequence Number: ", ob.get_seqNum()))
                ob = pickle.dumps(ob)
                time.sleep(1)
                conn.send(ob)
                packetRecieve = conn.recv(1024)
                ob = pickle.loads(packetRecieve)

    ob.set_AON("ACK")
    print("Sending ACK, Checksum good for seq number: ",ob.get_seqNum())
    ob = pickle.dumps(ob)
    time.sleep(1)
    conn.send(ob)
    ob = pickle.loads(ob)
    return ob

def main():                                                         #main function, where our prog starts
    print("Pirate Translator Server")
    print("-----------------------------------\n")
    n = list(sys.argv)  
    port = int(n[1])
    segmentSize = int(n[2])
    packetCorruptProbability = float(n[3])
    host = socket.gethostname()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:       #initiats connection then waits for clients
        stream.bind((host, port))
        stream.listen()
        while True:
            messageToTranslate = ""
            messageToSend = ""
            print("Waiting for connections:")
            conn, addr = stream.accept()
            print("New connection from: ", addr)
            x = True
            while (x == True):
                packetRecieve = conn.recv(1024)
                ob = pickle.loads(packetRecieve)
                ob = corruptPacketChecker(ob, conn)
                if (ob.get_message()[-1] == "!"):
                    x = False
                messageToTranslate = messageToTranslate + ob.get_message()
            messageToTranslate = messageToTranslate[:len(messageToTranslate)-1]
            print(messageToTranslate)
            print("all packets recieved from client, now translating")
            with open('pirate.csv', mode = 'r') as file:
                yarrMaty = csv.reader(file, delimiter=",")
                rosettaStone = list(yarrMaty)
                MTT = messageToTranslate.split()
                for word in MTT:
                    x =1
                    for row in rosettaStone:
                        if (word == row[0].rstrip()):
                            messageToSend += " " + row[1]
                            x+=1
                    if (x==1):
                        messageToSend += " " + word
            messageToSend += "!"
            for i in range(0, len(messageToSend), segmentSize):
                packetToSend = packet(i, corruptOrNot(packetCorruptProbability),222, segmentSize,messageToSend[i:i+segmentSize])
                ob = pickle.dumps(packetToSend)
                time.sleep(1)
                conn.send(ob)
                time.sleep(1)
                ob = pickle.loads(ob)
                ob = recievedNAK(ob, packetCorruptProbability, conn)

main()
