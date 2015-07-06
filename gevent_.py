import email.utils
import os
import mimetypes


CRLF = '\r\n'
ROOT = os.path.relpath('webroot')


def server_(socket, address):
    while True:
        try:
            response = ''
            uri = None
            uri_info = []
            try:
                uri = parse_request(socket)
                uri = uri.lstrip("/")
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
            socket.sendall(response)
            socket.close()
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
    response += CRLF + "Content-Type: text/plain" + CRLF + CRLF
    return response


def parse_request(conn):
    fullmsg = ""
    while True:
        msg = conn.recv(1024)
        fullmsg = fullmsg + msg
        if len(msg) < 1024:
            break
    fullmsg = fullmsg.split(CRLF)
    tline1 = fullmsg[0]
    line1 = tline1.split()
    if len(line1) is not 3:
        raise SyntaxError
    if line1[0] != 'GET':
        raise TypeError
    if line1[2] != 'HTTP/1.1':
        raise SyntaxError
    for i in range(len(fullmsg)):
        line = fullmsg[i].split()
        if line[0] == "Host:":
            break
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
        with open(path_, 'rb') as infile:
            msg = infile.read()
            uri_info.append(msg)
            uri_info.append(str(len((msg))))
            content_type = mimetypes.guess_type(path_)
            uri_info.append(content_type[0])
    else:
        raise NameError
    return uri_info


if __name__ == '__main__':
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    patch_all()
    server = StreamServer(('127.0.0.1', 10007), server_)
    print('Starting server on port 10007')
    server.serve_forever()
