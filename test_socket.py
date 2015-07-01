import pytest
import socket
import string
import datetime


@pytest.fixture(scope='session')
def connection():
    ADDR = ('127.0.0.1', 8585)
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(ADDR)
    return client


def test_client(connection):
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
    import pdb; pdb.set_trace()
    assert part_list[0].find("200 OK") != -1
    date = datetime.datetime.strftime(datetime.datetime.now(),
                                      '%Y-%m-%d %H:%M')
    assert part_list[1].find(date) != -1
    assert part_list[2].find("Content-Type:") != -1
    assert part_list[3].find("Content-Length:") != -1
