import socket
import threading
import time
import queue
import sys

global playerDic                                                                   #our dictionary and list are global variables that are accessed by all threads
playerDic = {}
global players
players = []
ourQ = queue.Queue()                                                                #our queue we use to determine if both players have connected/used for the thread that handles determining who wins in RPS()

def RPS():
    while True:
        test = ""
        player1Output = ourQ.get()                                                     #waits for input to take off of the queue by .get()
        player2Output = ourQ.get()
        time.sleep(1)
        if (playerDic[players[1]]) == (playerDic[players[0]]):                       
            test = "Draw"
        elif (playerDic[players[0]]) == "rock" and (playerDic[players[1]]) == "paper" or (playerDic[players[0]]) == "paper" and (playerDic[players[1]]) == "scissors" or (playerDic[players[0]]) == "scissors" and (playerDic[players[1]]) == "rock":
            test ="Player 2 Wins!"
        elif (playerDic[players[0]]) == "paper" and (playerDic[players[1]]) == "rock" or (playerDic[players[0]]) == "scissors" and (playerDic[players[1]]) == "paper" or (playerDic[players[0]]) == "rock" and (playerDic[players[1]]) == "scissors":
            test ="Player 1 Wins!"
        for each_socket in players:
            each_socket.send(test.encode())
            each_socket.close
        playerDic.clear()
        players.clear()
   
def main():                                                         #main function, where our prog starts
    print("Rock Paper Scissors with Sockets Server")
    print("-----------------------------------\n")
    n = list(sys.argv)  
    port = int(n[1])
    host = socket.gethostname()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:       #initiats connection then waits for clients
        stream.bind((host, port))
        stream.listen(2)
        print("Waiting for connections:")
        thread = threading.Thread(target=RPS, args=())
        thread.start()
        while True:
            conn, addr = stream.accept()
            players.append(conn)
            print("New connection")
            thread = threading.Thread(target=handler, args=(conn,addr))         #starts our threads for the clients
            thread.start()

def handler(conn,addr):                                                         #our threads main function
    switch = 0
#    time.sleep(1)
    while switch != 1:                                                          #waits for a proper response from client
        playerChoice = conn.recv(1024).decode()
        if (playerChoice == "rock") or (playerChoice == "paper") or (playerChoice == "scissors"):
            conn.send("200 OK".encode('utf-8'))
            ourQ.put(playerChoice)                                              #sets an option in the queue
            playerDic.update({conn: playerChoice})
            if (len(players) == 1):
                print("Player 1 selected " + playerChoice)
                conn.send("Hello Player 1".encode())
            elif (len(players) == 2):
                print("Player 2 selected " + playerChoice)
                conn.send("Hello Player 2".encode())
            switch = 1
        else:
            conn.send("404 Not Found".encode('utf-8'))
main()