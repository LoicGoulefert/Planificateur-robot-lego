#!/usr/bin/python3

from socket import *

"""The client just sends messages to the server."""

def send_data(messages):
	host = ('127.0.0.2', 5000)
	s = socket(AF_INET, SOCK_STREAM)
	s.connect(host)

	# Faut d'abord envoyer le nb de trames qu'on va envoyer
	for m in messages:
		print('Sending : ' + m)
		s.send(m.encode())
		answer = s.recv(2048).decode()
		print('Answer : ' + answer)

	s.close()


if __name__ == '__main__':
	messages = ['#1a 1 1,c 2 3', '#2b 0 4', '#3A 0 0,B 4 4', \
	'#4A DOWN,B UP,A RIGHT,B LEFT,B UP,A UP,A RIGHT,B UP,B RIGHT,B UP,B LEFT,A RIGHT']
	send_data(messages)

