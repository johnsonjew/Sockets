import server
import pytest
import socket

@pytest.fixture(scope='session')
def connection():
    ADDR = ('127.0.0.1', 6565)
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP
    )
    client.connect(ADDR)
    return client

def test_client(connection):
    try:
        connection.sendall('abc')
        part
        while True:
            tempPart
            part = part + client.recv(16)
            connection.shutdown(socket.SHUT_WR)
            if len(tempPart) < 16:
                break
        content_type = "text/plain"
        content_length = "1354"
        date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        Str = "HTTP/1.1 200 OK" + "\r\n" + date + "\r\n"  + "Content-Type:" + content_type + "\r\n"  + "Content-Length:" + content_length + "\r\n\r\n"
        assert part == Str
    except Exception as e:
        print e
