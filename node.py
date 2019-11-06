import random
import time
import hashlib
from constants import *
from message import Message

class Node:

	def __init__(self):

		# coordinates of this node
		self.x = random.uniform(X_MIN, X_MAX)
		self.y = random.uniform(Y_MIN, Y_MAX)

		self.sk = self.create_random_string() # sk = secret key
		self.pk = '' # pk = public key

		# messages this node has received
		self.messages = []

		''' Graph of nodes this node is connected to.

			key:   neighbor's public key
			value: {
				'known_min_distance'  : 4.556284
				'claimed_coordinates' : (10.0, 12.5),
				'neighbors' : { ... repeats ... }	
			}
	
			Example:			
			self.neighbors = {
				0 : {
						'pk0' : {
							'known_min_distance'  : 4.556284
							'claimed_coordinates' : (10.0, 12.5),
							'neighbors' : { ... }
						},
						'pk1' : {
				
						},
						'pk2' : {
				
						}
				},
				1 : {
	
				}

			}

			'''
		self.neighbors = {}

		# map of pings to the time they were sent out
		# key   = ping random string
		# value = time ping was sent
		self.pings = {}

	def main_loop(self):
		t = time.time() # unix time, example: 1424233311.771502
		p = self.ping()
		self.pings = self.update_ping_list(p, t)
		es = self.respond_to_messages()
		return p, es

	def update_ping_list(self, p, t):

		# save most recent ping
		rs = p.m.split('\n')[1] # rs = random string
		self.pings[rs] = t

		# trim old pings that are out of range R
		pings = {}
		for rs, pt in self.pings.items():
			# rs = random string
			# pt = ping time
			time_since_ping = time.time() - pt
			max_time_since_ping = (2.0 * R) / SIGNAL_SPEED
			if time_since_ping < max_time_since_ping:
				pings[rs] = pt

		return pings

	def create_random_string(self, string_length=256):
		return ''.join(
			random.choice(ALL_CHARS) for i in range(string_length))

	def ping(self):
		random_string = self.create_random_string()
		return Message(
			'PING, send me back this exact random string\n%s\nand your public key.' \
			% random_string)

	def echo(self, m):
		specifed_random_string_to_echo = m.m.split('\n')[1]
		return self.send_message('ECHO\n' + specifed_random_string_to_echo + '\n' + self.pk)


	def respond_to_messages(self):

		for m in self.messages:
			
			if m.m.startswith('PING'): self.echo(m)
			# if m.m.startswith('ECHO'):

		self.messages = []

		return []


	def send_message(self, m, rpk=None):
		# t   = time of sending this message (int)
		# m   = message to be sent (Message object)
		# rpk = receiver public key

		return Message(m, rpk)


	def nprint(self, i='?', newline=False):
		print('%sNode %s out of %s at (%.4f, %.4f)' \
			% ('\n' if newline else '    ', i, N, self.x, self.y))


