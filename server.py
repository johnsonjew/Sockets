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


def parse_request(fullmsg):
    split = string.split(fullmsg, ' ')

if __name__ == '__main__':
    ADDR = ('127.0.0.1', 8000)
    socket_ = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
        )
    socket_.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_.bind(ADDR)
    socket_.listen(1)

    while True:
        try:
            conn, addr = socket_.accept()
            code = ""
            fullmsg = ""
            while True:
                fullmsg = fullmsg + msg
                msg = conn.recv(16)
                if len(msg) < 16:
                    break
            fullmsg = string.split(fullmsg, '\r\n')
            response = parse_request(fullmsg)
            conn.sendall(code)
            conn.close()
        except KeyboardInterrupt:
            break
