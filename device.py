import random
from constants import *
from node import Node
import numpy as np

'''

    Each device has a start and stop point
        they're "powered on" at point A (random location on edge of map)
        they move to point B (random location on a different edge of map)
            avoiding other nodes along the way
                by making node velocity very small, if a node is surrounded by a bunch of nodes and its
                vector sum pushes it into a node it will be closer the next time but not NEAR at all
                colliding and now that its closer its new vector sum will push it away from the node
                its getting closer to colliding with, and the nodes will never collide with each other
        then they "shut down" at point B

        This causes the networks the devices form to:
            grow
            shrink
            split
            merge
        which makes the simulation much more realistic
	'''


class Device(object):

    def __init__(self, devices):

        self.src, self.dst = self.set_source_and_destination(devices)
        self.vel = self.set_velocity()
        # print('src = (%.4f, %.4f)' % (self.src[0], self.src[1]))
        self.n = Node(self.src[0], self.src[1], grid=False)

    def set_source_and_destination(self, devices):

        # pick a random side
        sides = ['left', 'right', 'top', 'bottom']
        src_side = random.choice(sides)

        # pick a portion of the side that no other node is at
        src = None
        while src == None:
            if src_side == 'left':   src = (0, H * random.uniform(0, 1))
            if src_side == 'right':  src = (W, H * random.uniform(0, 1))
            if src_side == 'top':    src = (W * random.uniform(0, 1), H)
            if src_side == 'bottom': src = (W * random.uniform(0, 1), 0)
            for d in devices:
                if d.n.x == src[0] and d.n.y == src[1]:
                    src = None
                    break

        # pick a random other side
        sides.remove(src_side)
        dst_side = random.choice(sides)

        # pick a portion of that other side
        if dst_side == 'left':   dst = (0, H * random.uniform(0, 1))
        if dst_side == 'right':  dst = (W, H * random.uniform(0, 1))
        if dst_side == 'top':    dst = (W * random.uniform(0, 1), H)
        if dst_side == 'bottom': dst = (W * random.uniform(0, 1), 0)

        return src, dst

    def set_velocity(self):
        vel = random.gauss(AVG_VEL, STD_DEV_VEL) # normal distribution
        vel = MIN_VEL if vel < MIN_VEL else vel
        vel = MAX_VEL if vel > MAX_VEL else vel
        return vel

    def reached_dst(self):
        dst_dist = math.sqrt((self.n.x - self.dst[0])**2 + (self.n.y - self.dst[1])**2)
        return dst_dist <= MAX_DST_DIST

    def move(self, close_devices, verbose=False):
        # print('\n\n\n')
        x, y = self.n.x, self.n.y
        # print('(x, y) = (%.4f, %.4f)' % (x, y))
        # print('self.dst = (%.4f, %.4f)' % (self.dst[0], self.dst[1]))
        dx, dy = self.dst[0]-x, self.dst[1]-y # x and y dist to dst
        # print('(dx, dy) = (%.4f, %.4f)' % (dx, dy))
        dst_dist = math.sqrt(dx**2 + dy**2) # distance to destination
        theta0 = np.arctan2(dy, dx) # v0 = angle to dst
        # print('theta0 = %.4f' % theta0)
        mag = min(self.vel, dst_dist)
        # print('mag = min(self.vel, dst_dist) = min(%.4f, %.4f) = %.4f' % (self.vel, dst_dist, mag))
        v0 = (mag * np.cos(theta0), mag * np.sin(theta0)) # v0 = vector to destination
        v_sum = v0
        # print('v0    = (%.4f, %.4f)' % (v_sum[0], v_sum[1]))
        for d, dist in close_devices.items():
            theta = np.arctan2(d.n.y-y, d.n.x-x) + np.pi
            mag = 0.0025 * float(1 / dist)
            # print('dist = %.4f   mag = %.4f   theta = %.4f' % (dist, mag, theta))
            v = (mag * np.cos(theta), mag * np.sin(theta)) # v0 = vector to destination
            # print('v = (%.4f, %4f)' % (v[0], v[1]))
            v_sum = (v_sum[0] + v[0], v_sum[1] + v[1])
        mag = math.sqrt(v_sum[0]**2 + v_sum[1]**2)
        # print('mag = %.4f' % mag)
        if mag > MAX_VEL:
        	theta = np.arctan2(v_sum[1], v_sum[0])
        	v_sum = (MAX_VEL * np.cos(theta), MAX_VEL * np.sin(theta))
        # print('v_sum = (%.4f, %.4f)' % (v_sum[0], v_sum[1]))
        self.n.x += v_sum[0]
        self.n.y += v_sum[1]
        if self.n.x < 0: self.n.x = 0
        if self.n.x > W: self.n.x = W
        if self.n.y < 0: self.n.y = 0
        if self.n.y > W: self.n.y = H
        return self.reached_dst()


    def print_d(self, num_devices, i='?', start_space='    ', newline_start=False):
        self.n.print_n(num_devices, i=i, start_space=start_space, newline_start=newline_start)
