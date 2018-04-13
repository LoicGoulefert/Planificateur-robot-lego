#!/usr/bin/python3

from socket import *

"""The client just sends messages to the server."""

def send_data(messages):
	"""Connect to the server, then send each string in the array "messages" to the server."""
	host = ('127.0.0.2', 5000)
	s = socket(AF_INET, SOCK_STREAM)
	s.connect(host)

	for m in messages:
		#Add size checking (< 2048), or maybe the planner will do this
		print('Sending : ' + m)
		s.send(m.encode())
		answer = s.recv(2048).decode()
		print('Answer : ' + answer)

	s.close()


if __name__ == '__main__':
	messages = ['#1a 1 1,c 2 3', '#2b 0 4', '#3A 0 0,B 4 4', \
	'#4A DOWN,B UP,A RIGHT,B LEFT,B UP,A UP,A RIGHT,B UP,B RIGHT,B UP,B LEFT,A RIGHT',  \
	'#4B LEFT,B LEFT,B DOWN,B RIGHT,B DOWN', '#cm1.txt']
	send_data(messages)
