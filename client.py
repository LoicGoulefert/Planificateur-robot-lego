#!/usr/bin/python3

# Libs
from socket import socket, AF_INET, SOCK_STREAM
import pickle

# Others

"""The client sends messages or objects to the server.

Packets identifiers for messages(first 2 char of each message):
#1 -> coord. objectives
#2 -> coord. static objectives
#3 -> coord. robots
#4 -> move list => Will be replaced
#0 -> End of communication
"""

CHUNK_SIZE = 4096  # Maximum message size the server can receive


def send_data(messages, IPAdr='127.0.0.2', port=5000):
    """Connect to the server, then send each string
    in the array "messages" to the server.
    Close the socket when it's done.

    Parameters:
        messages: list of strings, the messages to be sent
        IPAdr: string, IP of the server
        port: int, port we're emitting on
    """
    host = (IPAdr, port)
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(host)

    for m in messages:
        print('[CLIENT]Sending ({} bytes) : {} '.format(len(m), m))
        s.send(m.encode())
        answer = s.recv(CHUNK_SIZE).decode()
        print('[CLIENT]Answer : ' + answer)

    s.close()


def send_object(obj, IPAdr='127.0.0.2', port=5000):
    """Send a pickled object to the server.
    Close the socket when it's done.

    Parameters:
        obj: The object to be sent
        IPAdr: string, IP of the server
        port: int, port we're emitting on
    """
    host = (IPAdr, port)
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(host)

    pickled_obj = pickle.dumps(obj)
    size = len(pickled_obj)

    print('[CLIENT]Sending size of pickled obj.')
    s.send(str(size).encode())
    answer = s.recv(CHUNK_SIZE).decode()
    print('[CLIENT]Answer : ' + answer)

    print('[CLIENT]Sending object ({} bytes)'.format(len(pickled_obj)))
    s.send(pickle.dumps(obj))
    answer = s.recv(CHUNK_SIZE).decode()
    print('[CLIENT]Answer : ' + answer + '\n')

    s.close()

if __name__ == '__main__':
    pass
