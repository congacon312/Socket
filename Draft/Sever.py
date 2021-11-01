import socket

HOST = "127.0.0.1"
PORT = 1234
FORMART = "utf8"



def  recvlist(conn):

    item = conn.recv(1024).decode(FORMART)

    list =[]

    list.append(item)
    conn.sendall(item.encode(FORMART))
    item = conn.recv(1024).decode(FORMART)

    while(item != "end"):
        list.append(item)

        conn.sendall(item.encode(FORMART))
        item = conn.recv(1024).decode(FORMART)
    
    return list




#--------------------------------------------main-------------------------------------
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("SEVER SIDE")


s.bind((HOST, PORT))
s.listen()
print("Waiting Client")


#-------try except------------------
try:
    conn, add = s.accept()
    print("Client: ", add , " connect")
    print("connect: ", conn.getsockname())

    mgs = None

    while mgs != "Exit":
        mgs = conn.recv(1024).decode(FORMART)
        print("Sever: ", mgs)

        if(mgs == "list"):
            #reponse
            conn.sendall(mgs.encode(FORMART))

            list = recvlist(conn)
            print("List: ", list)


except:
    print("Do not connect to Client")

print("End")

conn.close()