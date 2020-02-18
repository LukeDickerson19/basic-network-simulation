import random
import time
import hashlib
from constants import *
from message import Message
import pandas as pd



class Node(object):

	def __init__(self, x, y, t, grid=True):

		# coordinates of this node
		self.x = x
		self.y = y

		self.sk = self.create_random_string() # sk = secret key
		self.pk = '' # pk = public key

		# messages this node has received
		# [(message1, time_received_message1), (message2, time_received_message2), ...]
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
			'Public Key'     : [],
			'Estimated Dist' : []
		}).set_index('Public Key') # other nodes get on this list by returning a ping, other nodes get taken off this list by not returning a ping
		self.potential_neighbors = {

		} # other nodes get on this list by sending this node a ping

		# map of pings to the time they were sent out
		# key   = ping random string
		# value = time ping was sent
		self.pings = {}
		if TIME_OR_ITERATION_BASED:
			self.prev_ping_t = t - (1 / PING_FREQUENCY)*random.uniform(0, 1)  # start pings at random times in period (to desyncronize the nodes' pings)
		else:
			self.prev_ping_t = -1 - random.randint(0, 1 / PING_FREQUENCY) # -1 to avoid ZeroDivisionError

	def main_loop(self, t, verbose=False):
		# if verbose: print('\nNode %s:' % self.sk)

		messages_to_send = []

		# ping on PING_FREQUENCY
		if 1.0 / (t - self.prev_ping_t) <= PING_FREQUENCY:
			ping = self.ping(verbose=False)
			self.pings = self.update_ping_list(ping, t)
			self.prev_ping_t = t
			messages_to_send.append(ping)

		# respond to any messages received
		more_messages_to_send, update_console_display = \
			self.respond_to_messages(verbose=verbose)
		messages_to_send += more_messages_to_send

		# remove nodes from neighbors list if they haven't responded to our previous ping in time
		for neighbor in self.neighbors.iterrows():

			# if the amount of time it would take for a neighboring device to respond to our ping
			# at the very edge of our signal range R, has surpassed the max round trip duration
			# since our previous ping
			whuuut = self.prev_ping_t
			max_possible_ping_time = (2 * R) / SIGNAL_SPEED
			if whuuut > max_possible_ping_time:

				# remove them from the list of neighbors
				pass

		return messages_to_send, update_console_display

	def respond_to_messages(self, verbose=False):
		messages_to_send = []
		unread_messages  = []
		update_console_display = False
		for j, (message, t) in enumerate(self.mailbox):

			if message.m.startswith('PING'):
				messages_to_send.append(
					self.echo(message))#, verbose=verbose))

			elif message.m.startswith('ECHO'):
				update_console_display |= \
					self.process_echo(message, t, verbose=verbose) # |= is OR EQUALS

			else:

				############# insert response to blue messages here #############
				#################################################################

				unread_messages.append(message)

		self.mailbox = unread_messages
		return messages_to_send, update_console_display

	def update_ping_list(self, p, t):

		# save most recent ping
		rs, _ = self.parse_ping(p)
		self.pings[rs] = t

		# trim old pings that are out of range R
		pings = {}
		for rs, pt in self.pings.items():
			# rs = random string
			# pt = ping time

			time_since_ping = t - pt
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
	def process_echo(self, e, t, verbose=False):

		# pn = ping node      <string>
		# rs = random string  <string>
		# en = echoing node   <string>
		pn, rs, en = self.parse_echo(e)

		# check if the random string returned is in the list
		# of random strings you sent out in the near past
		try:
			pt = self.pings[rs]
		except:
			return False

		# update the Estimated Distance of the echoing node
		ed = ((t - pt) / 2.0) * SIGNAL_SPEED # ed = estimated distance
		if en in self.neighbors.index: # update an existing neighbor's estimated dist
			self.neighbors.at[en, 'Estimated Dist'] = ed
			return True		
		else: # else it wasn't in the list b/c its a new neighbor, so append it's estimated dist
			self.neighbors.loc[en] = [ed]
			return True
		return False

	def send_message(self, m, rpk=None):
		# t   = time of sending this message (int)
		# m   = message to be sent (Message object)
		# rpk = receiver public key

		return Message(m, rpk)

	def print_n(self, num_nodes='?', i='?', start_space='    ', newline_start=False):
		print('%s%sNode %s out of %s at (%.4f, %.4f)' \
			% ('\n' if newline_start else '', start_space, i, num_nodes, self.x, self.y))


