

class Message(object):

    def __init__(self, m, receiver_public_key=None):

        self.time_sent = None
        self.m = m
        self.rpk = receiver_public_key

    def set_time_sent(self, t):
        # t = time sent (int)
        self.time_sent = t

    def print_m(self):
        print('Message:\n%s\n' % self.m)

