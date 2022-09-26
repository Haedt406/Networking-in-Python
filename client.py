
import random
import sys
import socket
import time

def main():
    print("Welcome to Rock Paper Scissors with Sockets!")
    print("-----------------------------------\n") 
    n = list(sys.argv)                                                                  #takes arguments from the command line to use as variables
    port = int(n[1])
    players = int(n[2])
    host = socket.gethostname()
    playersMove = input("Please enter either 'rock', 'paper', or 'scissors'")
    playersMove = playersMove.lower()

    if (players == 0):                                                                  #if the option is 0, it causes the client to play against the computer
        choices = ["rock","paper","scissors"]
        compChoice = random.choice(choices)
        print(compChoice)
        if playersMove == compChoice:
            print("Draw")
        elif playersMove == "rock" and compChoice == "paper" or playersMove == "paper" and compChoice == "scissors" or playersMove == "scissors" and compChoice == "rock":
            print("Computer Wins!")
        elif playersMove == "rock" and compChoice == "scissors" or playersMove == "paper" and compChoice == "rock" or playersMove == "scissors" and compChoice == "paper":
            print("You Win!")


    elif (players == 1):                                                                #if option is 1, it connects to the server to play against another client/person
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host,port))
        clientSocket.send(playersMove.encode('utf-8'))
        switch = 0
        while switch != 1:                                                              #waits for a proper response from server in while loop for correct option
            response = clientSocket.recv(1024).decode()
            print(response)
            if (response == "200 OK"):
                switch = 1
            elif (response == "404 Not Found"):
                playersMove = input("Please try again: Enter either 'rock' 'paper' or 'scissors' ")
                time.sleep(1)
                playersMove = playersMove.lower()
                clientSocket.send(playersMove.encode('utf-8'))

        response = clientSocket.recv(1024).decode()                                      #once '200 OK', waits for server to send what player they are, then if they won or not
        print(response)
        response = clientSocket.recv(1024).decode()
        print(response)
    else:
        print("Number of players needs to be either 0 or 1, Please try again.")
    exit()



        



main()