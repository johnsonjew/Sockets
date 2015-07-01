import pytest
import socket
import string
import email.utils


@pytest.fixture(scope='session')
def connection():
    ADDR = ('127.0.0.1', 8764)
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(ADDR)
    return client


def test_all(connection):
    message = "GET /index.html HTTP/1.1" + "\r\n" + "Host: www.example.com"
    connection.sendall(message)
    connection.shutdown(socket.SHUT_WR)
    part = ""
    while True:
        tempPart = connection.recv(16)
        part = part + tempPart
        if len(tempPart) < 16:
            connection.close()
            break
    part_list = string.split(part, '\r\n')
    assert part_list[0].find("200 OK") != -1
    date = email.utils.formatdate(usegmt=True)
    assert part_list[1].find(date) != -1
    assert part_list[2].find("Content-Type:") != -1
    assert part_list[3].find("Content-Length:") != -1


def test_set():
    ADDR = ('127.0.0.1', 8764)
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(ADDR)
    message = "SET /index.html HTTP/1.1" + "\r\n" + "Host: www.example.com"
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
    ADDR = ('127.0.0.1', 8764)
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(ADDR)
    message = "GET /index.html HTTP/1.0" + "\r\n" + "Host: www.example.com"
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


def test_wrongargs():
    ADDR = ('127.0.0.1', 8764)
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(ADDR)
    message = "GET /index.html" + "\r\n" + "Host: www.example.com"
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
    ADDR = ('127.0.0.1', 8764)
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(ADDR)
    message = "SET /index.html HTTP/1.1" + "\r\n" + "Hos: www.example.com"
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
