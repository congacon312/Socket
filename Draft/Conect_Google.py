import socket
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM chỉ giao thức TCP
    print("socket successfully created")

except socket.error as err:
    print("socket created failed with error %s" %(err))

port = 80 #port co dih de ket noi voi google

try:
    host_ip = socket.gethostbyname("www.google.com") #lay dia chi ip cua google
except socket.gaierror:

    print("there was an error resolving the host")
    sys.exit()

s.connect((host_ip,port))
print('The socket has successfully conected to google %s' %(host_ip))