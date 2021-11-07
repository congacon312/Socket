from os import name
import socket
import threading

HOST = "127.0.0.1"
PORT = 1234
FORMART = "utf8"


# --------------------------------------------declaration func--------------------------------------
def recvlist(conn: socket):

    item = conn.recv(1024).decode(FORMART)

    list = []

    while(item != "end"):
        list.append(item)

        conn.sendall(item.encode(FORMART))
        item = conn.recv(1024).decode(FORMART)

    return list


def handleClient(conn, add):
    print("connect: ", conn.getsockname())
    name = recvName(conn)
    print("Wellcome ", name)
    mgs = None

    while mgs != "Exit":
        mgs = conn.recv(1024).decode(FORMART)
        print("Client ", conn.getsockname(), ": ", mgs)

        if(mgs == "list"):
            # reponse
            conn.sendall(mgs.encode(FORMART))

            list = recvlist(conn)
            print("List: ", list)

    print("End connect ", conn.getsockname())
    conn.close()


def recvName(conn):
    name = None
    # reponse
    name = conn.recv(1024).decode(FORMART)

    return name


# --------------------------------------------main-------------------------------------
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("SEVER SIDE")


s.bind((HOST, PORT))
s.listen()
print("Waiting Client")

nsocket = 0

# -------try except------------------
while(nsocket < 3):
    try:
        conn, add = s.accept()

        thr = threading.Thread(target=handleClient, args=(conn, add))
        thr.daemon = True
        #vo deamon bang true thi thr se kill toan bo Client => end Sever
        #voi deamon bang false Sever se doi cac Client hoat dong xong => end
        thr.start()

    except:
        print("Do not connect to Client")

    nsocket += 1


print("End All")
input()
s.close()
