#this is our outside network that will read in the data for each packet from 'packets.csv' and then sent to the 'network'

import csv
import socket
import time
import pickle
import packet

packet = packet.packet              #initiates the packet class to be used as our packets

def main():                                             #our main function
    print("Outside Network that sends in packets")
    print("-----------------------------------\n") 
    port = 5005                                                 #i set the port to 5005
    packetList = []
    counter = 0
    host = socket.gethostname()
    with open('packets.csv', mode = 'r') as file:           #reads in the data from 'packets.csv' to create a packet
            reader = csv.reader(file)
            next(reader, None)
            for line in reader:
                packetList.append(line)            
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:         #sets up our sockets and then is used to communicate with 'network'
        conn.connect((host,port)) 
        for i in packetList:
            print(i)
            time.sleep(1)
            if counter ==8:
                packetToSend = packet("False","False","False","False","False")
            else:
                packetToSend = packet(i[0],i[1],i[2],i[3], i[4])
            print(packetToSend.get_src_ip(),packetToSend.get_dst_ip(), packetToSend.get_src_tl(), packetToSend.get_dst_tl(), (packetToSend.get_protocol()))            
            ob = pickle.dumps(packetToSend)
            conn.send(ob)
            time.sleep(1)  
            packetRecieve = conn.recv(1024)
            print(packetRecieve.decode())
            counter+=1
        conn.close()   

main()