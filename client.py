#!/usr/bin/python3

# Libs
from socket import socket, AF_INET, SOCK_STREAM

"""The client just sends messages to the server.

Packets identifiers (first 2 char of each message):
#c -> config file name (must be the same on both sides)
#1 -> coord. objectives
#2 -> coord. static objectives
#3 -> coord. robots
#4 -> move list
#0 -> End of communication
"""


def send_data(messages, IPAdr='127.0.0.2', port=5000):
    """Connect to the server, then send each string
    in the array "messages" to the server.
    """
    host = (IPAdr, port)
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(host)

    for m in messages:
        # Add size checking (< 2048), or maybe the planner will do this
        print('Sending : ' + m)
        s.send(m.encode())
        answer = s.recv(2048).decode()
        print('Answer : ' + answer)

    s.close()


if __name__ == '__main__':
    # messages = [
    #     '#1a 1 1,c 2 3', '#2b 0 4', '#3A 0 0,B 4 4',
    #     '#4A DOWN,B UP,A RIGHT,B LEFT,B UP,A UP,A RIGHT,B UP,'
    #     'B RIGHT,B UP,B LEFT,A RIGHT',
    #     '#4B LEFT,B LEFT,B DOWN,B RIGHT,B DOWN', '#cm1.txt']

    # send_data(messages)
    pass
