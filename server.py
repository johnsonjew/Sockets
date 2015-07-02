import socket
import email.utils
import os
from os.path import isfile, isdir

CRLF = '\r\n'

def server():
    ADDR = ('127.0.0.1', 9990)
    socket_ = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
        )
    socket_.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_.bind(ADDR)
    socket_.listen(20)

    while True:
        try:
            conn, addr = socket_.accept()
            code = ""
            fullmsg = ""
            while True:
                msg = conn.recv(16)
                fullmsg = fullmsg + msg
                if len(msg) < 16:
                    break
            fullmsg = fullmsg.split(CRLF)
            response = ''
            try:
                returnstr = parse_request(fullmsg)
                response = response_ok(returnstr)
            except SyntaxError or IndexError:
                response = "400 Bad Request \r\n\r\n"
            except TypeError:
                response = "406 Not Acceptable \r\n\r\n"
            conn.sendall(response)
            conn.close()
        except KeyboardInterrupt:
            break

def response_ok(uri):
    returnstr = []
    content_type = "text/plain"
    bytes = uri.encode('utf-8')
    content_length = str(len(bytes))
    date = email.utils.formatdate(usegmt=True)
    returnstr.append("HTTP/1.1 200 OK")
    returnstr.append("Date:" + date)
    returnstr.append("Content-Type:" + content_type)
    returnstr.append("Content-Length:" + content_length)
    header = CRLF.join(returnstr)
    header = header + CRLF + uri
    return header


def response_error():
    return "500 Server Error \r\n\r\n"


def parse_request(fullmsg):
    try:
        tline1 = fullmsg[0]
        line1 = tline1.split()
        tline2 = fullmsg[1]
        line2 = tline2.split()
    except:
        raise SyntaxError
    if len(line1) is not 3 or len(line2)is not 2:
        raise SyntaxError
    if len(line1) is not 3 or len(line2)is not 2:
        raise SyntaxError
    if line1[0] != 'GET':
        raise TypeError
    if line1[2] != 'HTTP/1.1':
        raise SyntaxError
    if line2[0] != 'Host:':
        raise SyntaxError
    return line1[1]


def resolve_uri(returnstr):
    path = 'webroot' + returnstr

    if isdir:
        list_dir = os.listdir(path)
        for dir in list_dir:
            return dir
    if isfile:
        with open(path, 'r') as infile:
            msg = infile.read()
            return msg


if __name__ == '__main__':
    server()
