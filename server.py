import socket
import datetime


def response_ok():
    returnstr = []
    content_type = "text/plain"
    content_length = "1354"
    date = datetime.datetime.strftime(datetime.datetime.now(),
                                      '%Y-%m-%d %H:%M')
    returnstr.append("HTTP/1.1 200 OK")
    returnstr.append("Date:" + date)
    returnstr.append("Content-Type:" + content_type)
    returnstr.append("Content-Length:" + content_length)
    header = '\r\n'.join(returnstr)
    return header


def response_error():
    return "500 Server Error \r\n\r\n"


if __name__ == '__main__':
    ADDR = ('127.0.0.1', 8000)
    socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
        )

    socket.bind(ADDR)
    socket.listen(1)

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
