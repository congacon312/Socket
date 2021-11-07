from os import name
import socket


HOST = "127.0.0.1"
PORT = 1234
FORMART = "utf8"




#--------------------------------------------declaration func--------------------------------------

def sendList(list, client):
    for item in list:
        client.sendall(item.encode(FORMART))
        #reponse
        client.recv(1024)

    client.sendall("end".encode(FORMART))

def  handle(client):
    print("client: ", client.getsockname())

    mgs = None

    while mgs != "Exit":
        mgs = input("Message: ")
        client.sendall(mgs.encode(FORMART))

        list = ["baby", "pro", "player"]

        if (mgs == "list"):
            #wait reponse
            client.recv(1024)
            sendList(list, client)

def sendName(client: socket.socket, name):
    client.sendall(name.encode(FORMART))


#------------------------------------------------------------main-------------------------
print("CLIENT SIDE")
client  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
name = input("Please Enter Name: ")

try:
    client.connect((HOST, PORT))
    sendName(client, name)
    handle(client)
    
except:
    print("Do not connect to Sever")

client.close()