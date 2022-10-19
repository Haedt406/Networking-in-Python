import random
import sys
import socket
import time
import pickle
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

def main():
    print("Pirate Translator.")
    print("-----------------------------------\n") 
    n = list(sys.argv)                                                                  #takes arguments from the command line to use as variables
    port = int(n[1])
    segmentSize = int(n[2])
    packetCorruptProbability = float(n[3])
    wholeReturn = ""
    host = socket.gethostname()
    toTranslate = input("Please enter the phrase you would like to translate to pirate speak")
    toTranslate = toTranslate.lower()
    toTranslate += "!"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
 #   clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host,port))
        for i in range(0, len(toTranslate), segmentSize):
            packetToSend = packet(i, corruptOrNot(packetCorruptProbability),222, segmentSize,toTranslate[i:i+segmentSize])
            ob = pickle.dumps(packetToSend)
            conn.send(ob)
            time.sleep(1)
            ob = pickle.loads(ob)
            ob = recievedNAK(ob, packetCorruptProbability, conn)
        print("All packets sent to server")
        x = True
        while (x == True):
            packetRecieve = conn.recv(1024)
            ob = pickle.loads(packetRecieve)
            ob = corruptPacketChecker(ob, conn)
            if (ob.get_message()[-1] == "!"):
                x = False
            wholeReturn = wholeReturn + ob.get_message()
        wholeReturn = wholeReturn[:len(wholeReturn)-1]
        print("Translated Message: ", wholeReturn)
        conn.close()

main()
