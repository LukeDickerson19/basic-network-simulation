import random
import time
import hashlib
from constants import *
from message import Message

class Node:

	def __init__(self, x=None, y=None, grid=True):

		# coordinates of this node
		if grid:
			self.x = x
			self.y = y
		else:
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
		self.pings = {
			'received' : {},
			'sent'     : {}
		}
		self.time_of_last_ping0 = None

	def main_loop(self):
		t = time.time() # unix time, example: 1424233311.771502

		# ping on PING_FREQUENCY
		ping = None
		# if self.time_of_last_ping0 == None \
		# or 1.0 / (t - self.time_of_last_ping0) < PING_FREQUENCY:
		# 	ping = self.ping0()
		# 	self.pings = self.update_ping_list(ping, t)
		# 	self.time_of_last_ping = t

		messages_to_send = [] #self.respond_to_messages()
		return ping, messages_to_send

	def update_ping_list(self, p, t):

		# save most recent ping
		rs = p.m.split('\n')[2] # rs = random string
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

	def ping(self, old_random_string):
		new_random_string = self.create_random_string()
		return Message(
			'PING!\n' + \
			'Hi Node: %s\n' %  + \
			'This is the random string you sent me.\n' + \
			'%s\n' % old_random_string + \
			'Send me back this new random string.\n' + \
			'%s\n' % new_random_string + \
			'and sign it please.\n' + \
			'\n' + \
			'Sincerely,' + \
			'Node: %s\n' % self.pk)

	def ping0(self, old_random_string):
		new_random_string = self.create_random_string()
		return Message(
			'PING!\n' + \
			'If you would like to start a ping cycle with me,\n' + \
			'Send me back this new random string.\n' + \
			'%s\n' % new_random_string + \
			'and sign it please.\n' + \
			'\n' + \
			'Sincerely,' + \
			'Node: %s\n' % self.pk)



	def echo(self, m):
		specifed_random_string_to_echo = m.m.split('\n')[1]
		return self.send_message('ECHO\n' + specifed_random_string_to_echo + '\n' + self.pk)

	def respond_to_messages(self):
		messages_to_send = []
		self_messages_new = []
		for m in self.messages:
			if m.m.startswith('PING'):
				messages_to_send.append(self.echo(m))

				# if m.m.startswith('ECHO'):

			else: # default of switch (why doesn't python have switches?)
				self_messages_new.append(m)


		self.messages = self_messages_new
		return messages_to_send

	def send_message(self, m, rpk=None):
		# t   = time of sending this message (int)
		# m   = message to be sent (Message object)
		# rpk = receiver public key

		return Message(m, rpk)


	def nprint(self, i='?', newline=False):
		print('%sNode %s out of %s at (%.4f, %.4f)' \
			% ('\n' if newline else '    ', i, N, self.x, self.y))


