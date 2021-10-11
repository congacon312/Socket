import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("successfully created socket")
port = 12345

s.bind(('127.0.0.1', port))

print("socket binded to %s" % (port))

s.listen(5)
print("socket is listening...")

while True:
    c, addr = s.accept() #luu dia chi cua client ket noi voi sever
    print('Got connection from ',addr)

    data = input('Enter Message: ')
    #c.send('Sever: %s' %(str).encode())
    c.sendall(bytes(data, "utf8"))
    c.close()

    break
