#this project is a simulation for a network routing packets to different routers based on port forwarding and destination IP addresses
#the "network.py" works as a server that takes packets in from an outside network and then routes those networks in a LAN to 4 different routers
#the routers are all object of the 'router' class and hold all the rules that help direct traffic around this simulated network
#the packets are their own object class called 'packet'.
#the packets and the routers rules and specificaitons for each router (their ip address, label, and what routers they connect to), are located in 'packets.csv', 'rules.csv', and 'routers.csv'


import csv
import pickle
import socket
import time
import packet
import copy
packet = packet.packet

class router(object):                           #the router class where each router is set up and we load in its specifications and rules
    def __init__(self,ipAddresses, connections, rules):
        self.ipAddresses = ipAddresses
        self.connections = connections
        self.rules = rules
    def get_ipAddresses(self):
        return self.ipAddresses
    def get_connections(self):
        return self.connections
    def get_rules(self):
        return self.rules
    def print_rules(self):
        print(self.rules)
    def packetHandler(self,ob):                                             #this is the start of reading the rules for the router and what it will do with a packet in our network
        if ob.dst_ip_address in self.ipAddresses:                               
            print("Packet has reached its destination IP:" + " Router:  ", self.rules[0][0])
            return "0" , ob
        
        else:
            newRules = self.rules
            while True:
                for i in newRules:
                    if "dst_ip_address="+ob.get_dst_ip() == i[2] or "src_ip_address="+ob.get_src_ip() == i[2] or "src_tl_port="+ob.get_src_tl() == i[2] or "dst_tl_port="+ob.get_dst_tl() == i[2] or "protocol="+ob.get_protocol() ==i[2]:
                        time.sleep(1)
                        if "Forward" in i[1]:
                            if "B" in i[1] and (i[0] == "A" or "D"):
                                print("Packet has been sent to router: B" + "  from Router:  ", self.rules[0][0])
                                return "B", ob
                            elif "C" in i[1] and (i[0] == "A" or "D"):
                                print("Packet has been sent to router: C" + "  from Router:  ",self.rules[0][0])
                                return "C", ob
                            elif "A" in i[1] and (i[0] == "B" or "C"):
                                print("Packet has been sent to router: A" + "  from Router:  ", self.rules[0][0])
                                return "A", ob
                            elif "D" in i[1] and (i[0] == "B" or "C"):
                                print("Packet has been sent to router: D" + "  from Router:  ", self.rules[0][0])
                                return "D", ob

                        elif "Drop" in i[1]:
                            print("Packet Dropped by router " + self.rules[0][0])
                            return "0", ob

                        elif "Modify" in i[1]:
                            temp = i[1]
                #            print(temp)
                            temp = temp.replace('Modify=', '')
               #             print(i[1])
                            if "src_tl_port=" in temp:
                                temp = temp.replace('src_tl_port=', '')
                                ob.set_src_tl(temp)
                                print("Packet dst_ip_address has been changed to: " +temp+ " From Router: ", self.rules[0][0])
                                return self.rules[0][0], ob

                            if "dst_tl_port="in temp:
                                temp = temp.replace('dst_tl_port=', '')
                                ob.set_dst_tl(temp)
                                print("Packet set_dst_ip has been changed to: " +temp+ " From Router: ", self.rules[0][0])
                                return self.rules[0][0], ob

                            if "dst_ip_address=" in temp:
                                temp = temp.replace('dst_ip_address=', '')
                                ob.set_dst_ip(temp)
                                print("Packet set_dst_ip has been changed to: " +temp+ " From Router: ", self.rules[0][0])
                                return self.rules[0][0], ob

                            if "src_ip_address=" in temp:
                                temp = temp.replace('src_ip_address=', '')
                                ob.set_src_ip(temp)
                                print("Packet set_dst_ip has been changed to: " +temp+ " From Router: ", self.rules[0][0])
                                return self.rules[0][0], ob
                            break
                print("Packet dropped by router: ", self.rules[0][0])
                return "0", ob


routerList = [] 
routerRules = []
ruleListA =[]
ruleListB = []
ruleListC =[]
ruleListD=[]
host = socket.gethostname()
port = 5005
def main():                                                         #main function, where our prog starts
    print("'Network' that recieves packets from outside network and moves them around its network.")
    print("-----------------------------------\n")
    
    with open('rules.csv', mode = 'r') as rules:            #reads in our rules from the csv
        readRules = csv.reader(rules, delimiter=",")
        next(readRules, None)
        readRules = csv.reader(rules, delimiter=",")        
        for line in readRules:
            routerRules.append(line)
    rules.close()
    with open('routers.csv', mode = 'r') as file:       #reads in the router specifications to apply to the routers
        reader = csv.reader(file, delimiter=",")
        next(reader, None)
        for line in reader:
            if line[0] == "A":
                for e in routerRules:
                    if e[0] == "A":
                        ruleListA.append(e)
                        routerA = router(copy.deepcopy(line[2]), copy.deepcopy(line[1]), copy.deepcopy(ruleListA))
            if line[0] == "B":
                for e in routerRules:
                    if e[0] == "B":
                        ruleListB.append(e)
                        routerB = router(copy.deepcopy(line[2]), copy.deepcopy(line[1]), copy.deepcopy(ruleListB))
            if line[0] == "C":
                for e in routerRules:
                    if e[0] == "C":
                        ruleListC.append(e)
                        routerC = router(copy.deepcopy(line[2]), copy.deepcopy(line[1]), copy.deepcopy(ruleListC))
            if line[0] == "D":
                for e in routerRules:
                    if e[0] == "D":
                        ruleListD.append(e)
                        routerD = router(copy.deepcopy(line[2]), copy.deepcopy(line[1]), copy.deepcopy(ruleListD))    
    file.close()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:       #initiats connection then waits for clients
        stream.bind((host, port))
        stream.listen()

        while True:                                 #runs forever, but waits for a connection from a client, recieves packets, then handles the return from the routers
            print("Waiting for connections:")
            conn, addr = stream.accept()
            print("New connection from: ", addr)
            packetCounter = 1
            while packetCounter <=8:
                packetRecieve = conn.recv(1024)
                print("Packet " + str(packetCounter)+ " recieved")
                packetCounter = packetCounter+1
                ob = pickle.loads(packetRecieve)
     #           print(ob.get_src_ip())
                if ob.get_src_ip() == "False":
                    break
                nextStep, ob = routerA.packetHandler(ob)
                while (nextStep != "0"):
                    if nextStep == "A":
                        nextStep, ob = routerA.packetHandler(ob)
                    if nextStep == "B":
                        nextStep, ob = routerB.packetHandler(ob)
                    if nextStep == "C":
                        nextStep, ob = routerC.packetHandler(ob)
                    if nextStep == "D":
                        nextStep, ob = routerD.packetHandler(ob)
                conn.send("OK".encode())
                print("\n")

                
main()