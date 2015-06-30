import socket
import datetime


ADDR = ('127.0.0.1', 6565)
socket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )

socket.bind(ADDR)
socket.listen(1)


def response_ok():
    content_type = "text/plain"
    content_length = "1354"
    date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    Str = "HTTP/1.1 200 OK" + "\r\n" + date + "\r\n"  + "Content-Type:" + content_type + "\r\n"  + "Content-Length:" + content_length + "\r\n\r\n"
    return Str


def response_error():
    return "500 Server Error \r\n\r\n"


def main():
    while True:
        try:
            conn, addr = socket.accept()
            code = ""
            code = response_ok()
            while True:
                msg = conn.recv(16)
                print msg
                if len(msg) < 16:
                    break
            conn.sendall(code)
            conn.close()
        except KeyboardInterrupt:
            break
