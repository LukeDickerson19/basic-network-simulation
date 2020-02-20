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
			'Public Key'            : [],
			'Estimated Dist'        : [],
			'Most Recent Echo Time' : []
		}).set_index('Public Key') # other nodes get on this list by returning a ping, other nodes get taken off this list by not returning a ping
		self.potential_neighbors = {

		} # other nodes get on this list by sending this node a ping

		# map of pings to the time they were sent out
		self.pings = {} # {key = ping random string, value = time ping was sent}
		if TIME_OR_ITERATION_BASED:
			self.prev_ping_t = t - (1 / PING_FREQUENCY)*random.uniform(0, 1)  # start pings at random times in period (to desyncronize the nodes' pings)
		else:
			self.prev_ping_t = -1 - random.randint(0, 1 / PING_FREQUENCY) # -1 to avoid ZeroDivisionError

	def main_loop(self, t, verbose=False):
		# if verbose: print('\nNode %s:' % self.sk)

		messages_to_send = []

		# ping on PING_FREQUENCY
		if PING_PERIODICALLY:
			if 1.0 / (t - self.prev_ping_t) <= PING_FREQUENCY:

				# remove nodes from neighbors list if they haven't responded to our previous ping in time
				# (if this isn't done on PING_FREQUENCY, the simulation fps is WAY slower)
				self.neighbors = self.neighbors[t - self.neighbors['Most Recent Echo Time'] <= MAX_POSSIBLE_PING_TIME]

				# then send the next ping
				ping = self.ping(t, verbose=False)
				messages_to_send.append(ping)

		# respond to any messages received
		more_messages_to_send, update_console_display = \
			self.respond_to_messages(verbose=verbose)
		messages_to_send += more_messages_to_send

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

				# unread_messages.append((message, t))
				# messages_to_send.append(message) # causes message cycles D-:
				pass

		self.mailbox = unread_messages
		return messages_to_send, update_console_display

	def update_ping_list(self, p, t):

		# trim old pings that are out of range R
		pings = {}
		for rs, pt in self.pings.items():
			# rs = random string
			# pt = ping time

			time_since_ping = t - pt
			if time_since_ping < MAX_POSSIBLE_PING_TIME:
				pings[rs] = pt

		# save most recent ping
		rs, _ = self.parse_ping(p)
		pings[rs] = t

		return pings

	def create_random_string(self, string_length=10):#256):
		return ''.join(
			random.choice(ALL_CHARS) for i in range(string_length))

	def ping(self, t, verbose=False):
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

		ping = self.send_message(m)
		self.pings = self.update_ping_list(ping, t)
		self.prev_ping_t = t
		return ping
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
			return False # return False to not update the console output display b/c this is an echo to a ping someone else sent

		# update the Estimated Distance of the echoing node
		ed = ((t - pt) / 2.0) * SIGNAL_SPEED # ed = estimated distance
		self.neighbors.loc[en] = [ed, t] # add new neighbor, or update existing neighbor

		return True # return True to update the console output display

	def send_message(self, m, rpk=None):
		# t   = time of sending this message (int)
		# m   = message to be sent (Message object)
		# rpk = receiver public key

		return Message(m, rpk)

	def print_n(self, num_nodes='?', i='?', start_space='    ', newline_start=False):
		print('%s%sNode %s out of %s at (%.4f, %.4f)' \
			% ('\n' if newline_start else '', start_space, i, num_nodes, self.x, self.y))


