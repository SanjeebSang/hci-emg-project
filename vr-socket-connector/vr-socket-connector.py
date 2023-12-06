import socket
 
hostname = socket.gethostname()
UDP_IP = socket.gethostbyname(hostname)
print(f"Hostname: {UDP_IP}")
UDP_PORT = 5005

def socket_setup():
    print("UDP target IP: %s" % UDP_IP)
    print("UDP target port: %s" % UDP_PORT)

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    return sock


def socket_send(sock):
    MESSAGE = b"Hello, World!"

    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

def socket_read(sock):   
    sock.bind((UDP_IP, UDP_PORT))
    
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("received message: %s" % data)

def main():
    sock = socket_setup()
    socket_read(sock)

if __name__ == '__main__': 
    main()