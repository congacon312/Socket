import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 12345

s.connect(('127.0.0.1', port))
print("Client is conecting")

try:
    while True:

        data = s.recv(1024)

        print("Sever: ", data.decode("utf8"))

        if data == "quit":
            break

        strr = input("Client: ")
        s.sendall(bytes(strr, "utf8"))
finally:
    s.close()
