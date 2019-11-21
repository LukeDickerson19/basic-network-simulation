import random
import time
import hashlib
from constants import *
from message import Message
import pandas as pd



class Node(object):

	def __init__(self, x, y, grid=True):

		# coordinates of this node
		self.x = x
		self.y = y

		self.sk = self.create_random_string() # sk = secret key
		self.pk = '' # pk = public key

		# messages this node has received
		self.mailbox = []

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
		self.neighbors = pd.DataFrame({
			'public_key'     : [],
			'estimated_dist' : []
		}) # other nodes get on this list by returning a ping
		self.potential_neighbors = {

		} # other nodes get on this list by sending this node a ping

		# map of pings to the time they were sent out
		# key   = ping random string
		# value = time ping was sent
		self.pings = {}
		self.prev_ping_t = time.time() - (1 / PING_FREQUENCY)*random.uniform(0, 1) # start pings at random times in period


	def main_loop(self, verbose=False):
		t = time.time() # unix time, example: 1424233311.771502
		# if verbose: print('\nNode %s:' % self.sk)

		# ping on PING_FREQUENCY
		ping = None
		if 1.0 / (t - self.prev_ping_t) <= PING_FREQUENCY:
			ping = self.ping(verbose=verbose)
			self.pings = self.update_ping_list(ping, t)
			self.prev_ping_t = t
			if verbose: print('hi %s' % time.ctime(t))
			if verbose: print('%d messages' % len(self.mailbox))
		messages_to_send = self.respond_to_messages(verbose=verbose)
		if ping != None:
			messages_to_send += [ping]
		return messages_to_send

	def update_ping_list(self, p, t):

		# save most recent ping
		rs, _ = self.parse_ping(p)
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

	def create_random_string(self, string_length=10):#256):
		return ''.join(
			random.choice(ALL_CHARS) for i in range(string_length))

	def ping(self, verbose=False):
		random_string = self.create_random_string()
		m = '\n'.join([
			'PING',
			'Hi,',
			'Send me back this random string',
			'%s' % random_string,
			'and sign it please.',
			'Sincerely,',
			'Node: %s' % self.sk
		])
		# m = \
		# 	'PING!\n' + \
		# 	'Hi Node: %s\n' %  + \
		# 	'This is the random string you sent me.\n' + \
		# 	'%s\n' % old_random_string + \
		# 	'Send me back this new random string.\n' + \
		# 	'%s\n' % new_random_string + \
		# 	'and sign it please.\n' + \
		# 	'\n' + \
		# 	'Sincerely,' + \
		# 	'Node: %s\n' % self.pk)
		if verbose:
			print(time.ctime())
			print(m)
		return self.send_message(m)
	def parse_ping(self, p):
		random_string = p.m.split('\n')[3]
		sender_node   = p.m.split('\n')[-1].split(' ')[1]
		return random_string, sender_node

	def echo(self, m, verbose=False):
		random_string, sender_node = self.parse_ping(m)
		m = '\n'.join([
			'ECHO',
			'Hi Node: %s' % sender_node,
			'This is the string you sent me.',
			'%s' % random_string,
			'Sincerely,',
			'Node: %s' % self.sk
		])
		if verbose:
			print(time.ctime())
			print('echo message:')
			print(m)
		return self.send_message(m)
	def parse_echo(self, e):
		pinging_node  = e.m.split('\n')[1].split(' ')[2]
		random_string = e.m.split('\n')[3]
		echoing_node  = e.m.split('\n')[-1].split(' ')[1]
		return pinging_node, random_string, echoing_node

	def respond_to_messages(self, verbose=False):
		messages_to_send = []
		unread_messages  = []
		for i, message in enumerate(self.mailbox):
			if message.m.startswith('PING'):
				if verbose:
					print(time.ctime())
					print('message %d out of %d messages in mailbox' % (i, len(self.mailbox)))
					print('THEIR')
					print(message.m)
				messages_to_send.append(self.echo(message, verbose=verbose))

			elif message.m.startswith('ECHO'):
				pass
				# check if the random string returned is in the list of random strings you sent out in the near past
				# if yes:
					# add them to your list of neighbors
					# estimate their distance

					# i need some way to take nodes off the list
					# if they dont return a ping, they're taken off

			else: # default of switch (why doesn't python have switches?)
				unread_messages.append(message)

		self.mailbox = unread_messages
		return messages_to_send

	def send_message(self, m, rpk=None):
		# t   = time of sending this message (int)
		# m   = message to be sent (Message object)
		# rpk = receiver public key

		return Message(m, rpk)

	def print_n(self, num_nodes='?', i='?', start_space='    ', newline_start=False):
		print('%s%sNode %s out of %s at (%.4f, %.4f)' \
			% ('\n' if newline_start else '', start_space, i, num_nodes, self.x, self.y))


