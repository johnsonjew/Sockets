import socket

ADDR = ('127.0.0.1', 8000)

client = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )

client.connect(ADDR)
msg = "do you hear me"

try:
    client.sendall(msg)
    while True:
        part = client.recv(16)
        client.shutdown(socket.SHUT_WR)
        print part
        if len(part) < 16:
            break
except Exception as e:
    print e
