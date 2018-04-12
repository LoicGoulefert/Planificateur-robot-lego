#!/usr/bin/python3

from socket import *
import time, _thread

def send_data(messages):
	host = ('127.0.0.2', 5000)
	s = socket(AF_INET, SOCK_STREAM)
	s.connect(host)

	# Faut d'abord envoyer le nb de trames qu'on va envoyer
	for m in messages:
		s.send(m.encode())

	s.close()


if __name__ == '__main__':
	messages = ['a 1 1, b 0 4\n', 'A 0 0, B 4 4\n', 'A DOWN', 'B UP', 'A RIGHT', 'B LEFT', 'B UP', 'A UP', 'A RIGHT', 
	'B UP', 'B RIGHT', 'B UP', 'B LEFT', 'A RIGHT\n']
	send_data(messages)

