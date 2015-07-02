import socket
import email.utils
import os
import mimetypes
import sys

CRLF = '\r\n'
ROOT = os.path.relpath('webroot')


def server():
    ADDR = ('127.0.0.1', 10007)
    socket_ = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
        )
    socket_.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_.bind(ADDR)
    socket_.listen(20)

    while True:
        try:
            response = ''
            uri = None
            uri_info = []
            try:
                conn, addr = socket_.accept()
                uri = parse_request(conn)
                uri_info = resolve_uri(uri)
                response = response_ok(uri_info)
            except (SyntaxError, IndexError):
                response = response_error(400)
            except TypeError:
                response = response_error(406)
            except NameError:
                response = response_error(404)
            except:
                response = response_error(500)
            conn.sendall(response)
            conn.close()
        except KeyboardInterrupt:
            break


def response_ok(uri_info):
    returnstr = []
    date = email.utils.formatdate(usegmt=True)
    returnstr.append("HTTP/1.1 200 OK")
    returnstr.append("Date: " + date)
    returnstr.append("Content-Type: " + uri_info[2])
    returnstr.append("Content-Length: " + uri_info[1])
    header = CRLF.join(returnstr)
    header = header + CRLF + CRLF + uri_info[0]
    return header


def response_error(error):
    response = "HTTP/1.1 "
    if error == 400:
        response += "400 Bad Request"
    elif error == 404:
        response = "404 Not Found"
    elif error == 406:
        response = "406 Not Acceptable"
    elif error == 500:
        response = "500 Server Error"
    response += CRLF + "Content-Type: text/plain" + CRLF
    return response


def parse_request(conn):
    fullmsg = ""
    while True:
        msg = conn.recv(1024)
        fullmsg = fullmsg + msg
        if len(msg) < 1024:
            break
    fullmsg = fullmsg.split(CRLF)
    try:
        tline1 = fullmsg[0]
        line1 = tline1.split()
    except IndexError:
        raise SyntaxError
    if len(line1) is not 3:
        raise SyntaxError
    if line1[0] != 'GET':
        raise TypeError
    if line1[2] != 'HTTP/1.1':
        raise SyntaxError
    try:
        for i in range(len(fullmsg)):
            line = fullmsg[i].split()
            if line[0] == "Host:":
                break
    except IndexError:
        raise SyntaxError
    return line1[1]


def resolve_uri(uri):
    path_ = os.path.join(ROOT, uri)
    uri_info = []
    if os.path.isdir(path_):
        dir_ = os.listdir(path_)
        uri_info.append(" ".join(dir_))
        bytes = uri_info[0].encode('utf-8')
        uri_info.append(str(len(bytes)))
        uri_info.append('text/html; charset=UTF-8')
    elif os.path.isfile(path_):
        with open(path_, 'r') as infile:
            msg = infile.read()
            uri_info.append(msg)
            uri_info.append(sys.getsizeof(msg))
            uri_info[1] = str(uri_info[1])
            content_type = mimetypes.guess_type(path_)
            uri_info.append(content_type[0])
    else:
        raise NameError
    return uri_info


if __name__ == '__main__':
    server()
