import socket
import string
import email.utils


def test_text():
    ADDR = ('127.0.0.1', 10007)
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(ADDR)
    msg = "GET sample.txt HTTP/1.1"+"\r\n"+"Host: www.example.com"+"\r\n\r\n"
    client.sendall(msg)
    client.shutdown(socket.SHUT_WR)
    part = ""
    while True:
        tempPart = client.recv(16)
        part = part + tempPart
        if len(tempPart) < 16:
            client.close()
            break
    part_list = string.split(part, '\r\n')
    assert part_list[0].find("200 OK") != -1
    date = email.utils.formatdate(usegmt=True)
    assert part_list[1].find(date) != -1
    assert part_list[2].find("Content-Type: text/plain") != -1
    assert part_list[3].find("Content-Length:") != -1
    assert part_list[5].find("This is a very simple text file") != -1


def test_directory():
    ADDR = ('127.0.0.1', 10007)
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(ADDR)
    msg = "GET images HTTP/1.1"+"\r\n"+"Host: www.example.com"+"\r\n\r\n"
    client.sendall(msg)
    client.shutdown(socket.SHUT_WR)
    part = ""
    while True:
        tempPart = client.recv(16)
        part = part + tempPart
        if len(tempPart) < 16:
            client.close()
            break
    part_list = string.split(part, '\r\n')
    assert part_list[0].find("200 OK") != -1
    date = email.utils.formatdate(usegmt=True)
    assert part_list[1].find(date) != -1
    assert part_list[2].find("Content-Type: text/html") != -1
    assert part_list[3].find("Content-Length:") != -1
    assert part_list[5].find("JPEG_example.jpg") != -1


def test_jpg():
    ADDR = ('127.0.0.1', 10007)
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(ADDR)
    msg = "GET images/JPEG_example.jpg HTTP/1.1"+"\r\n"+"Host: www.example.com"+"\r\n\r\n"
    client.sendall(msg)
    client.shutdown(socket.SHUT_WR)
    part = ""
    while True:
        tempPart = client.recv(16)
        part = part + tempPart
        if len(tempPart) < 16:
            client.close()
            break
    part_list = string.split(part, '\r\n')
    assert part_list[0].find("200 OK") != -1
    date = email.utils.formatdate(usegmt=True)
    assert part_list[1].find(date) != -1
    assert part_list[2].find("Content-Type: image/jpeg") != -1
    assert part_list[3].find("Content-Length:") != -1


def test_png():
    ADDR = ('127.0.0.1', 10007)
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(ADDR)
    msg = "GET images/sample_1.png HTTP/1.1"+"\r\n"+"Host: www.example.com"+"\r\n\r\n"
    client.sendall(msg)
    client.shutdown(socket.SHUT_WR)
    part = ""
    while True:
        tempPart = client.recv(16)
        part = part + tempPart
        if len(tempPart) < 16:
            client.close()
            break
    part_list = string.split(part, '\r\n')
    assert part_list[0].find("200 OK") != -1
    date = email.utils.formatdate(usegmt=True)
    assert part_list[1].find(date) != -1
    assert part_list[2].find("Content-Type: image/png") != -1
    assert part_list[3].find("Content-Length:") != -1


def test_notthere():
    ADDR = ('127.0.0.1', 10007)
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(ADDR)
    msg = "GET imthebest HTTP/1.1"+"\r\n"+"Host: www.example.com"+"\r\n\r\n"
    client.sendall(msg)
    client.shutdown(socket.SHUT_WR)
    part = ""
    while True:
        tempPart = client.recv(16)
        part = part + tempPart
        if len(tempPart) < 16:
            client.close()
            break
    part_list = string.split(part, '\r\n')
    assert part_list[0].find("404 Not Found") != -1
    assert part_list[1].find("Content-Type: text/plain") != -1


def test_wrongbreak():
    ADDR = ('127.0.0.1', 10007)
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(ADDR)
    message = "GET sample.txt HTTP/1.1"+"\n"+"Host: www.example.com"+"\r\n\r\n"
    client.sendall(message)
    client.shutdown(socket.SHUT_WR)
    part = ""
    while True:
        tempPart = client.recv(16)
        part = part + tempPart
        if len(tempPart) < 16:
            client.close()
            break
    part_list = string.split(part, '\r\n')
    assert part_list[0].find("400 Bad Request") != -1


def test_set():
    ADDR = ('127.0.0.1', 10007)
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(ADDR)
    message = "SET sample.txt HTTP/1.1"+"\r\n"+"Host: www.example.com"+"\r\n\r\n"
    client.sendall(message)
    client.shutdown(socket.SHUT_WR)
    part = ""
    while True:
        tempPart = client.recv(16)
        part = part + tempPart
        if len(tempPart) < 16:
            client.close()
            break
    part_list = string.split(part, '\r\n')
    assert part_list[0].find("406 Not Acceptable") != -1


def test_wronghttp():
    ADDR = ('127.0.0.1', 10007)
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(ADDR)
    message = "GET sample.txt HTTP/1.0"+"\r\n"+"Host: www.example.com"+"\r\n\r\n"
    client.sendall(message)
    client.shutdown(socket.SHUT_WR)
    part = ""
    while True:
        tempPart = client.recv(16)
        part = part + tempPart
        if len(tempPart) < 16:
            client.close()
            break
    part_list = string.split(part, '\r\n')
    assert part_list[0].find("400 Bad Request") != -1


def test_wrongargs():
    ADDR = ('127.0.0.1', 10007)
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(ADDR)
    message = "GET sample.txt"+"\r\n"+"Host: www.example.com"+"\r\n\r\n"
    client.sendall(message)
    client.shutdown(socket.SHUT_WR)
    part = ""
    while True:
        tempPart = client.recv(16)
        part = part + tempPart
        if len(tempPart) < 16:
            client.close()
            break
    part_list = string.split(part, '\r\n')
    assert part_list[0].find("400 Bad Request") != -1


def test_nohost():
    ADDR = ('127.0.0.1', 10007)
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(ADDR)
    message = "GET sample.txt HTTP/1.0"+"\r\n"+"Hos: www.example.com"+"\r\n\r\n"
    client.sendall(message)
    client.shutdown(socket.SHUT_WR)
    part = ""
    while True:
        tempPart = client.recv(16)
        part = part + tempPart
        if len(tempPart) < 16:
            client.close()
            break
    part_list = string.split(part, '\r\n')
    assert part_list[0].find("400 Bad Request") != -1
