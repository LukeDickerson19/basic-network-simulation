import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import copy
import sys
import math
import random
from pygame.locals import QUIT, KEYDOWN
from constants import *
from node import Node
from device import Device
from message import Message
import numpy as np



''' NOTES:

    DESCRIPTION:

    USAGE:

        
        toggle seeing:
            edges between nodes - w/ "c"
            selected device's:
                pings    - w/ "p0 *enter*"
                echos    - w/ "e0 *enter*"
                messages - w/ "m0 *enter*"
            devices' in range of selected device:
                pings    - w/ "p1 *enter*"
                echos    - w/ "e1 *enter*"
                messages - w/ "m1 *enter*"
            signal rings        - w/ "r"
            message dots        - w/ "d"            

    SOURCES:

        https://www.pygame.org/docs/

        PyGame color Codes
        https://www.webucator.com/blog/2015/03/python-color-constants-module/

    OTHER:

    IDEAS:

        if the first neighpbor can verify the sender is who they say they are, they can pass on that verification, and then verify they're who THEY say they are, and the 2nd neighbor can verify the same, ... and a path can be built

        what if you used the position triangluation to verify that someone isn't using a server farm to run a bunch of nodes
        in order for nodes to count they need to be spread out (and moving frequenty? what about desktops) to exibit normal device behavior

    TO DO:

        NOW:

            signal stuff

                draw signals better

                    something is wrong with the way the colors of the signals are displayed.
                        pings's appear green when they should be red



                    make signal ring's opaqueness increase as r approaches R
                        apparently this is much harder than it seems because
                        the draw.circle fn. in pygame doesn't take an alpha value
                            so we need to make the color of the ring fade to the
                            background color instead of decreasing the alpha value
                                but theres 2 possible background colors,
                                    BACKGROUND_COLOR black (0, 0, 0)
                                    SELECTED_DEVICE_COLOR gray8 (20, 20, 20)

                                    so instead of creating a circle we would need
                                    to create 2 arcs. 1 arc fades to
                                        BACKGROUND_COLOR and the other fades to 
                                        SELECTED_DEVICE_COLOR

                                        to find the 2 angles where the arcs are separated
                                        we need to find the intercept of 2 overlapping circles
                                            (w/ known coordinates and radii)

                    make node turn red, green, white right before it sends a message
                        give them a time delay
                            perhaps fade from signal_color to NODE_DEFAULT_COLOR after signal is sent

                    make each node have a number in its circle in the display (just its index in the list of all nodes)

                    make it so you can click on a node

                        when you click on a node, information appears about
                        its public key
                        its messages list

                        make it so you can change R (and maybe other constants) mid simulation

                    make it so you can send a message manually from one node to another

                self.model.selected_device
                    view pings, incoming echoes, outgoing/incoming messages

                how much faster are the signals simulated paused/unpaused?

                keep ping the way it was originally made,
                but increase the speed, and decrease the period
                because in reality, if they ping/pong back and forth it will take up unnessessary amounts of band width
                    so doing it on a period is better

            controls stuff

                manually send message to another node


        EVENTUALLY:

            model could probably be made faster if we didn't copy over so much data
                its done to avoid messing up the iteration by deleting during an iteration though
                    if we could find a way to delete without messing up the iteration,
                        for lists we could iterate by index and then decrement the index when we delete
                        what about dictionaries though?
                            aren't dictionary keys a set in python?
                                does deleting from a set mess up iterating over it?

            model could be faster if we did more stuff in parallel using async lib
                https://realpython.com/async-io-python/

            make static map and cellular automata maps
                figure out how to get a fully connected network that is distributed evenly
                over the entire area ... more or less

                #################### these model functions to be fixed #############################

                    # create devices that are stationary in the map
                    def init_static_devices(self, verbose=False):
                        pass

                    # return boolean flagging if ALL the devices form 1 fully connected network
                    def fully_connected_network(self, devices, connections):
                        for d, c in connections.items():
                            if len(c) == 0:
                                return False
                        return True

                    # return a list of node networks
                    def get_networks(self, devices, connections, verbose=False):

                        def get_network_recurrsively(d0, connections, network):
                            network += [n0]
                            for c in connections[d0]: # self.set_direct_neighbors(n0, unvisited_nodes):
                                nd = c.keys[0] # nd = neighboring device
                                if nd not in network:
                                    network = get_network_recurrsively(d, connections, network)
                            return network

                        networks = []
                        devices = list(filter(lambda d : isinstance(d, Device), devices)) # for cellular automata
                        unvisited_devices = copy.deepcopy(devices)
                        while len(unvisited_devices) > 0:
                            d0 = unvisited_devices[0]
                            network = get_network_recurrsively(d0, connections, [])
                            networks.append(network)
                            for d in network:
                                unvisited_devices.remove(d)

                        if verbose:
                            print('\n%d Networks:' % len(networks))
                            for i, network in enumerate(networks):
                                print('\nNetwork %d has %d device(s)' % (i+1, len(network)))
                                for d in network:
                                    d.print_d()

                        return networks

                    # network 0: N nodes constantly throughout all time steps for the entire simulation
                    def create_random_network(self, verbose=False):

                        # self.nodes = [Node()]
                        # while len(self.nodes) < N:
                        #     n = Node()
                        #     self.nodes.append(n)
                        #     if len(self.set_direct_neighbors(n).keys()) == 0:
                        #         self.nodes.remove(n)
                        # return self.nodes

                        # self.nodes = [Node() for _ in range(N)]
                        # while not self.fully_connected_network():
                        #     print('Fail')
                        #     self.nodes = [Node() for _ in range(N)]
                        # if verbose:
                        #     print('Created network0 of %d nodes' % N)
                        # return self.nodes

                        nodes = [Node() for _ in range(N)]
                        connections = self.set_connections(nodes)
                        networks = self.get_networks(nodes, verbose=verbose)
                        return nodes, connections

                    # cellular automata
                    def create_grid_network(self, verbose=False):
                        # create grid with one node at the center
                        # nodes = np.array([[Node(x, y) for x in range(W)] for y in range(H)]).flatten().tolist()
                        nodes = []
                        for x in range(W):
                            grid_col = []
                            for y in range(H):
                                grid_col.append(
                                    Node(x, y) if (x, y) in AUTOMATA_START_POSITIONS['one_center'] else str(x)+','+str(y))
                            nodes += grid_col
                        if verbose:
                            for y in range(H):
                                s = ''
                                for x in range(W):
                                    s += ('N' if isinstance(nodes[x*H+y], Node) else '*') + ' '
                                print(s)

                        connections = self.set_connections(nodes)
                        # networks = self.get_networks(nodes, verbose=verbose)
                        return nodes, connections
                    def evolve_grid(self, verbose=False):

                        def evolve_cell(x0, y0, nodes):

                            # get grid neighbors state
                            # print('Finding Neighbours (x0, y0) = (%d, %d)' % (x0, y0))
                            neighbours = []
                            for x in range(x0-1, x0+2):
                                for y in range(y0-1, y0+2):

                                    # no wrap around
                                    if 0 <= x < W and 0 <= y < H:
                                        if not (x == x0 and y == y0):
                                            # print('x = %d y = %d   %s' % (x, y, 'ALIVE' if isinstance(nodes[x*H+y], Node) else 'dead'))
                                            neighbours.append(nodes[x*H+y])

                                    # # wrap around
                                    # x = W-1 if x == -1 else x
                                    # x = 0 if x == W else x
                                    # y = H-1 if y == -1 else y
                                    # y = 0 if y == H else y
                                    # if not (x == x0 and y == y0):
                                    #     print('x = %d y = %d   %s' % (x, y, 'ALIVE' if isinstance(nodes[x*H+y], Node) else 'dead'))
                                    #     neighbours.append(nodes[x*H+y])

                            # count neighbouring nodes

                            nn = len(list(filter(lambda n : isinstance(n, Node), neighbours)))
                            # print('nn = %d' % nn)

                            def conways_game_of_life():
                                cell0 = nodes[x0*H+y0]
                                dead = str(x0)+','+str(y0)
                                print('cell0 at (%d, %d)' % (x0, y0))
                                if isinstance(cell0, Node):
                                    print('ALIVE')
                                    if nn < 2: # Death by isolation
                                        print('Death by isolation')
                                        return dead
                                    elif 1 < nn < 4: # Survival
                                        print('Survival')
                                        return cell0
                                    elif 3 < nn: # Death by overcrowding
                                        print('Death by overcrowding')
                                        return dead
                                else: # cell0 == None
                                    print('dead')
                                    if nn == 3: # Births
                                        print('birth')
                                        return Node(x0, y0)
                                    else:
                                        print('stay dead')
                                        return dead
                            def forest_fire():
                                cell0 = nodes[x0*H+y0]
                                empty   = str(x0)+','+str(y0)
                                burning = empty + ' burning'
                                print('cell0 at (%d, %d)' % (x0, y0))
                                if isinstance(cell0, Node):
                                    print('tree')
                                    if nn < 0: # A tree will burn if at least one neighbor is burning
                                        print('tree will burn if at least one neighbor is burning')
                                        return burning
                                    else:
                                        # A tree ignites with probability F even if no neighbor is burning
                                        return cell0 if random.uniform(0, 1) <= F else burning
                                else: # not a tree
                                    if cell0.endswith(' burning'): # A burning cell turns into an empty cell
                                        print('burning')
                                        return empty
                                    else: # An empty space fills with a tree with probability p
                                        print('empty')
                                        return Node(x0, y0) if random.uniform(0, 1) <= P else cell0
                            def forest():
                                cell0 = nodes[x0*H+y0]
                                empty = str(x0)+','+str(y0)
                                pn = float(nn/8) # percent neighbors
                                if isinstance(cell0, Node): # tree
                                    # the more trees there are around a tree,
                                    # the more likely the tree will die (become an empty space)
                                    # a tree will not die if it has no neighbours
                                    return cell0 if nn == 0 or random.uniform(0, 1) <= 1.00 - pn*percent_trees else empty

                                else: # empty
                                    # a tree can only grow if there is at least 1 neighbor
                                    # the less nn there are around an empty space the more likely a tree will grow
                                    # nn: min=0, max=8
                                    # probablility: min=0, max=100
                                    # if few  neighbors: high likelyhood
                                    # if many neighbors: low  likelyhood 8n 1/9 p
                                    return Node(x0, y0) if nn > 0 and random.uniform(0, 1) <= 1.00 - pn*percent_trees else empty

                            return forest()

                        # for forest growth
                        num_trees = len(list(filter(lambda n :     isinstance(n, Node), self.nodes)))
                        num_empty = len(list(filter(lambda n : not isinstance(n, Node), self.nodes)))
                        percent_trees = float(num_trees) / num_empty

                        nodes = []
                        for x in range(W):
                            for y in range(H):
                                # print()
                                nodes.append(evolve_cell(x, y, self.nodes))

                        # ensure we never delete all the nodes
                        if nodes:
                            non_empty_nodes = []
                            for n in self.nodes:
                                if isinstance(n, Node):
                                    non_empty_nodes.append(n)
                        nodes = [non_empty_nodes[random.randint(len(non_empty_nodes))]] if nodes == [] else nodes

                        self.nodes = nodes
                        self.connections = self.set_connections(self.nodes)

                        if verbose:
                            print('Grid Evolution')
                            for y in range(H):
                                s = ''
                                for x in range(W):
                                    s += ('N' if isinstance(self.nodes[x*H+y], Node) else '*') + ' '
                                print(s)
                            print('------------------------------------------------------')


                    this was at the end of model.update()

                        # update the Nodes in the network every AUTOMATA_PERIOD
                        if (t - self.t2) > AUTOMATA_PERIOD:
                            self.evolve_grid(verbose=True)
                            self.t2 = t

                ####################################################################################


            maybe use this to improve device movement
            https://github.com/florimondmanca/pyboids
            where each boid has its own destination

        '''



class View(object):

    def __init__(self, model):

        self.model = model
        self.screen = pygame.display.set_mode(SCREEN_SIZE) # a pygame screen
        self.surface = pygame.Surface(SCREEN_SIZE) # a pygame surface is the thing you draw on

        self.show_controls = False # toggle control display

        self.c = True # draw connections
        self.d = True # draw message dots
        self.r = True # draw signal rings
        self.p0 = False # draw pings of selected device
        self.p1 = False # draw pings of direct neighbors of selected device
        self.e0 = False # draw echos of selected device
        self.e1 = False # draw echos of direct neighbors of selected device
        self.m0 = False # draw messages of selected device
        self.m1 = False # draw messages of direct neighbors of selected device


    def draw(self):

        # fill background
        self.surface.fill(pygame.Color(BACKGROUND_COLOR))


        self.draw_selected_device_range()
        if self.model.selected_device != None:
            if self.r: self.draw_signals()
        if self.c:
            self.draw_in_range_connections()
        if self.model.selected_device != None:
            if self.d: self.draw_messages()
        # self.draw_paths_to_dst()
        self.draw_devices()

        # # example shapes
        # pygame.draw.circle(self.surface, pygame.Color('green'), (250,250), 10) # (x,y), radius
        # pygame.draw.line(self.surface,   (255,255,255), (310, 320), (330, 340), 4) # (start_x, start_y), (end_x, end_y), thickness
        # pygame.draw.rect(self.surface,   pygame.Color('red'), [300, 350, 40, 100]) # [x,y,width,height]

        # # draw control key
        # if self.show_controls:
        #     for n, line in enumerate(CONTROL_KEY):
        #         self.draw_text(line, 10, 50+14*n, 20)
        # #else: self.draw_text("h = toggle help", 30, 1, 20)

        # update display
        pygame.display.update()

    def draw_selected_device_range(self):
        sd = self.model.selected_device
        if sd != None:
            x = int(SCREEN_SCALE * sd.n.x)
            y = int(SCREEN_SCALE * sd.n.y)
            r = int(SCREEN_SCALE * R)
            col = 20 # 0=black, 255=white, we want dark dark gray
            pygame.draw.circle(
                self.surface,
                (col, col, col),
                (x, y), r)

    def draw_devices(self):
        for d in model.devices:
            if not isinstance(d, Device): continue
            x = int(SCREEN_SCALE*d.n.x)
            y = int(SCREEN_SCALE*d.n.y)
            pygame.draw.circle(
                self.surface,
                pygame.Color(d.n.color),
                (x, y), 5) # (x,y), radius

    def draw_in_range_connections(self):
        for edge in model.edges:
            edge = tuple(edge)
            d1, d2 = edge[0], edge[1]
            x1, y1 = int(SCREEN_SCALE*d1.n.x), int(SCREEN_SCALE*d1.n.y)
            x2, y2 = int(SCREEN_SCALE*d2.n.x), int(SCREEN_SCALE*d2.n.y)
            pygame.draw.line(
                self.surface,
                pygame.Color(CONNECTION_COLOR),
                (x1, y1), (x2, y2), 1)

    def draw_paths_to_dst(self):
        for d in self.model.devices:
            x1, y1 = int(SCREEN_SCALE * d.n.x),    int(SCREEN_SCALE * d.n.y)
            x2, y2 = int(SCREEN_SCALE * d.dst[0]), int(SCREEN_SCALE * d.dst[1])
            pygame.draw.line(
                self.surface,
                (255, 255, 255),
                (x1, y1), (x2, y2), 1) # (start_x, start_y), (end_x, end_y), thickness
            pygame.draw.circle(
                self.surface,
                (255, 0, 0),
                (x2, y2), 5) # (x,y), radius

    def draw_messages(self):
        sd = self.model.selected_device
        for signal in self.model.signals:

            # filter which dots to draw
            # if signal['sender_device'] != sd: continue
            # if not signal['message'].m.startswith('ECHO'): continue
            d0 = signal['sender_device']
            if not (
                (
                    d0 == sd and (
                        (self.m0) or
                        (self.p0 and signal['message'].m.startswith('PING')) or
                        (self.e0 and signal['message'].m.startswith('ECHO'))
                    )
                ) or (
                    d0 in self.model.connections[sd] and (
                        (self.m1) or
                        (self.p1 and signal['message'].m.startswith('PING')) or
                        (self.e1 and signal['message'].m.startswith('ECHO'))
                    )
                )
            ): continue

            color = DOT_MESSAGE_COLOR
            if signal['message'].m.startswith('PING'): color = DOT_PING_COLOR
            if signal['message'].m.startswith('ECHO'): color = DOT_ECHO_COLOR
            self.draw_message_dot(signal, color, sd)
    def draw_message_dot(self, signal, color, sd):
        sn, sp = signal['sender_device'].n, signal['send_pt']
        cx, cy, r = sp[0], sp[1], signal['dist_traveled'] # circle variables
        for _edge in self.model.edges:
            edge = tuple(_edge)

            # filter which dots to draw
            if sd not in edge: continue # only draw signals going to/from sd
            if signal['message'].m.startswith('ECHO'): # only draw echo dot to intended receiver_node
                nd = edge[0] if edge[1] == sd else edge[1] # nd = neighboring device (of selected device)
                rd = nd if sn == sd.n else sd # rd = receiver device
                rn_id = signal['message'].m.split('\n')[1].split(' ')[2] # receiver node according to echo message
                if rd.n.sk != rn_id: continue
                if {rd, signal['sender_device']} != _edge: continue # only draw on the edge with both sender and receiver device
            if signal['message'].m.startswith('PING'):
                if signal['sender_device'] != sd: # if a neighboring device is sending the ping
                    # only draw it on the edge between that neighboring device and sd
                    if {signal['sender_device'], sd} != _edge: continue

            # if just one, XOR, of the connection endpoints is within the signal ring
            n1, n2 = edge[0].n, edge[1].n
            dist_sp_to_d1 = math.sqrt((n1.x - cx)**2 + (n1.y - cy)**2)
            d1_in_signal_ring = signal['dist_traveled'] >= dist_sp_to_d1
            dist_sp_to_d2 = math.sqrt((n2.x - cx)**2 + (n2.y - cy)**2)
            d2_in_signal_ring = signal['dist_traveled'] >= dist_sp_to_d2
            if d1_in_signal_ring != d2_in_signal_ring: # != is XOR (exclusive OR)

                # print()
                # print('(cx, cy) = (%.4f, %.4f)'  % (cx, cy))
                # n1.print_n()
                # n2.print_n()

                # 2D linear equation: y = m*x + b
                m = (n2.y - n1.y) / (n2.x - n1.x) # m = rise / run
                b = n2.y - m*n2.x

                # print('m = %.4f' % m)
                # print('b = %.4f' % b)
                # print('r = %.4f' % r)

                # quadratic for x
                _a = m**2 + 1.0
                _b = 2*(m*(b - cy) - cx)
                _c = cx**2 + (b - cy)**2 - r**2
                b2_minus_4ac = _b**2 - 4*_a*_c
                b2_minus_4ac = 0 if b2_minus_4ac < 0 else b2_minus_4ac

                # print('_a = %.4f' % _a)
                # print('_b = %.4f' % _b)
                # print('_c = %.4f' % _c)

                x_intercept_plus  = (-_b + math.sqrt(b2_minus_4ac)) / (2*_a)
                x_intercept_minus = (-_b - math.sqrt(b2_minus_4ac)) / (2*_a)

                # print('x_intercept_plus  = %.4f' % x_intercept_plus)
                # print('x_intercept_minus = %.4f' % x_intercept_minus)

                # quadratic for y
                _a = (1.0 / m**2) + 1.0
                _b = -((2 / m)*((b / m) + cx) + 2*cy)
                _c = ((b / m) + cx)**2 + cy**2 - r**2
                b2_minus_4ac = _b**2 - 4*_a*_c
                b2_minus_4ac = 0 if b2_minus_4ac < 0 else b2_minus_4ac

                # print('_a = %.4f' % _a)
                # print('_b = %.4f' % _b)
                # print('_c = %.4f' % _c)

                y_intercept_plus  = (-_b + math.sqrt(b2_minus_4ac)) / (2*_a)
                y_intercept_minus = (-_b - math.sqrt(b2_minus_4ac)) / (2*_a)

                # print('y_intercept_plus  = %.4f' % y_intercept_plus)
                # print('y_intercept_minus = %.4f' % y_intercept_minus)
                # print()

                x_min, x_max = (n1.x, n2.x) if n1.x <= n2.x else (n2.x, n1.x)
                x = int(SCREEN_SCALE * (x_intercept_plus if x_min <= x_intercept_plus <= x_max else x_intercept_minus))

                y_min, y_max = (n1.y, n2.y) if n1.y <= n2.y else (n2.y, n1.y)
                y = int(SCREEN_SCALE * (y_intercept_plus if y_min <= y_intercept_plus <= y_max else y_intercept_minus))

                # source: https://www.analyzemath.com/Calculators/find_points_of_intersection_of_circle_and_line.html

                pygame.draw.circle(
                    self.surface,
                    pygame.Color(color),
                    (x, y), 3) # (x,y), radius

    def draw_signals(self):
        sd = self.model.selected_device
        sd_conns = self.model.connections[sd] if sd != None else None
        for signal in self.model.signals:

            d0 = signal['sender_device']
            if not (
                (
                    d0 == sd and (
                        (self.m0) or
                        (self.p0 and signal['message'].m.startswith('PING')) or
                        (self.e0 and signal['message'].m.startswith('ECHO'))
                    )
                ) or (
                    d0 in self.model.connections[sd] and (
                        (self.m1) or
                        (self.p1 and signal['message'].m.startswith('PING')) or
                        (self.e1 and signal['message'].m.startswith('ECHO'))
                    )
                )
            ): continue

            if signal['message'].m.startswith('ECHO'): # only draw echo dot to intended receiver_node
                rn_id = signal['message'].m.split('\n')[1].split(' ')[2] # rn_id = receiver node id
                if d0 == sd:
                    pass # draw signal for all echos
                else:
                    # only draw signal if the echo is intended for sd
                    if rn_id == sd.n.sk:
                        pass
                    else:
                        continue

            color = SIGNAL_MESSAGE_COLOR
            if signal['message'].m.startswith('PING'): color = SIGNAL_PING_COLOR
            if signal['message'].m.startswith('ECHO'): color = SIGNAL_ECHO_COLOR
            self.draw_signal_ring(signal, color, sd, fade=True)
    def draw_signal_ring(self, signal, color, sd, fade=False):
        if fade:
            r = signal['dist_traveled']
            if int(SCREEN_SCALE * r) > 1:
                x = signal['send_pt'][0]
                y = signal['send_pt'][1]
                dx, dy = x - sd.n.x, y - sd.n.y
                dist_sd_to_send_pt = math.sqrt(dx**2 + dy**2)
                if dist_sd_to_send_pt + r <= R:
                    # signal all inside R, no intersect
                    # dist_sd_sent_pt is always <=R,
                    # b/c we're never going to draw the signal ring for a device outside of sd's range

                    r = int(SCREEN_SCALE * r)
                    x = int(SCREEN_SCALE * x)
                    y = int(SCREEN_SCALE * y)

                    color = pygame.Color(color)

                    pygame.draw.circle(
                        self.surface,
                        color,
                        (x, y), r, 1) # (x,y), radius

                else: # there is an intersect

                    print('\nsd = (%.4f, %.4f)' % (sd.n.x, sd.n.y))
                    print('(x, y) = (%.4f, %.4f)' % (x, y))
                    print('(dx, dy) = (%.4f, %.4f)' % (dx, dy))
                    theta1 = np.arctan2(dy, dx)# + np.pi
                    print('theta1 = %.4f' % theta1)
                    theta1 = theta1 % (np.pi)
                    # if theta1 > np.pi / 2:
                    #     theta1 = np.pi - theta1
                    # elif theta1 < -np.pi / 2:
                    #     theta1 = -np.pi - theta1
                    # theta1 = theta1 - np.pi if abs(theta1) > np.pi / 2 else theta1
                    print('theta1 = %.4f' % theta1)
                    theta2 = np.pi - np.arccos((r**2 + dist_sd_to_send_pt**2 - R**2) / (2*r*dist_sd_to_send_pt))
                    # print(r, R, theta1)#, theta2)

                    a1 = theta1# + theta2
                    a2 = theta1 - theta2

                    r = int(SCREEN_SCALE * r)
                    x = int(SCREEN_SCALE * x)
                    y = int(SCREEN_SCALE * y)
                    rect = [x - r, y - r, 2*r, 2*r]
                    
                    pygame.draw.line(
                        self.surface,
                        (0,255,255),
                        (x, y),
                        (x + r*np.cos(theta1),
                        y + r*np.sin(theta1)), 4) # (start_x, start_y), (end_x, end_y), thickness

                    pygame.draw.arc(
                        self.surface,
                        pygame.Color('red'),
                        rect,
                        0, a1, 1) # (x,y), radius
                    # pygame.draw.arc(
                    #     self.surface,
                    #     pygame.Color('blue'),
                    #     rect,
                    #     a2, a1, 1) # (x,y), radius


        else:
            color = pygame.Color(color)
            r = int(SCREEN_SCALE * signal['dist_traveled'])
            if int(SCREEN_SCALE * r) > 1:
                x = int(SCREEN_SCALE * signal['send_pt'][0])
                y = int(SCREEN_SCALE * signal['send_pt'][1])
                pygame.draw.circle(
                    self.surface,
                    color,
                    (x, y), r, 1) # (x,y), radius

    def draw_text(self, text, x, y, size, \
        text_color=(100, 100, 100), \
        background_color=BACKGROUND_COLOR):

        # make text
        basicfont = pygame.font.SysFont(None, size)
        text_render = basicfont.render(text, True, text_color)
        text_width = text_render.get_width()
        text_height = text_render.get_height()

        # draw background
        pygame.draw.rect(self.surface, background_color, \
            [x, y, text_width+50, text_height])

        # draw text
        self.surface.blit(text_render, (x, y))


class Model(object):

    def __init__(self):

        # create devices, connections and edges
        # devices: [Device(), Device(), ...]
        # connections: {keys=devices : value={key=neighbor_device, value=distance}}
        # edges: [{device0, device1}, {device2, device0}, ...]
        self.devices = self.init_moving_devices(verbose=False)
        self.connections, self.edges = self.set_connections(self.devices, verbose=False)

        # list of signals that are being broadcast. Used to simulate signal time delay in simulation
        # format: [{'sender_device':<Device>, 'dist_traveled':<float>, 'send_pt':<(float, float)>, 'message':<str>}, ...]
        self.signals = []

        t = time.time()
        self.t1 = t # t1 = time of previous time step (1 time step in the past)

        # window parameters / drawing
        self.show = True # show current model

        # controller variables
        self.selected_device = None # device user clicked on
        self.pause_devices  = False # pause/play movement
        self.pause_nodes    = False # pause/play signals


    # main_loop of the model
    def update(self, verbose=False):

        t = time.time()
        # if verbose: print('%s\nt = %s' % ('-'*180, t))

        # move message signals forward,
        # deliver message if it's reached a node,
        # remove it when its travelled R 
        if not self.pause_nodes:
            signals_outside_range = []
            for signal in self.signals:

                # move message forward
                prev_signal_dist = signal['dist_traveled']
                signal['dist_traveled'] += (SIGNAL_SPEED * (t - self.t1))
                if signal['dist_traveled'] > R: signal['dist_traveled'] = R

                # deliver message if it's reached a node
                sd, sp = signal['sender_device'], signal['send_pt']
                x, y = sp[0], sp[1]
                for d in self.devices:
                    if d != sd:

                        # put the signal's message in device d's mailbox if the signal just passed d
                        dist_sp_to_d = math.sqrt((d.n.x - x)**2 + (d.n.y - y)**2)
                        if prev_signal_dist <= dist_sp_to_d <= signal['dist_traveled'] \
                        and d not in signal['receiver_devices']:
                            d.n.mailbox.append(signal['message'])
                            signal['receiver_devices'].add(d)

                # remove message that have reached the max signal range
                if signal['dist_traveled'] == R:
                    signals_outside_range.append(signal)
            for signal in signals_outside_range:
                self.signals.remove(signal)

            # run the main loop of each node
            for i, d in enumerate(self.devices):

                if not isinstance(d, Device): continue

                # every node sends out a ping signal on a timed interval
                # and responds to any messages it has received immediately
                # n.print_n(i=i+1, num_nodes=len(devices), newline_start=True)
                sent_messages = d.n.main_loop(verbose=False)#d==self.selected_device)
                for message in sent_messages:
                    self.signals.append({
                        'sender_device'    : d,
                        'dist_traveled'    : 0.00,
                        'send_pt'          : (d.n.x, d.n.y),
                        'message'          : message, # this  
                        'receiver_devices' : set() # ensures that a signal doesn't pass a node twice
                    })

        ''' move the devices, and update devices, connections and edges

            there are a variable number of nodes on the map at any given time
                ranging from N_MIN to N_MAX
            the simulation starts with the midway point between N_MIN and N_MAX
            when a node n0 reaches its destination dst
                the simulation creates 0, 1 or 2 nodes
                    if there are now <= N_MIN nodes left
                        create 2
                    elif there are now >= N_MAX nodes left
                        create 0
                    else:
                        randomly pick between 0, 1, and 2
                        if the number of nodes left is closer to N_MIN
                            0 has a low chance
                            1 has a medium chance
                            2 has a high chance
                        elif  the number of nodes left is closer to N_MAX
                            0 has a high chance
                            1 has a medium chance
                            2 has a low chance

            '''
        if not self.pause_devices:
            devices = []
            num_devices_that_reached_their_dst = 0
            for d in self.devices:
                reached_dst = d.move(self.connections[d], verbose=False)
                if reached_dst:
                    num_devices_that_reached_their_dst += 1
                    if d == self.selected_device:
                        self.selected_device = None
                else:
                    devices.append(d)
            while num_devices_that_reached_their_dst > 0:
                num_devices_that_reached_their_dst -= 1
                num_devices_left = len(devices)
                if num_devices_left <= N_MIN:
                    num_devices_to_add = 2
                elif num_devices_left >= N_MAX:
                    num_devices_to_add = 0
                else:
                    # print('N_MAX=%d   N_MIN=%d    num_devices_left=%d' % (N_MAX, N_MIN, num_devices_left))
                    a = N_MAX - num_devices_left
                    b = num_devices_left - N_MIN
                    c = N_MAX - N_MIN
                    # print(a, b, c)
                    # print(float(a) / c) # this is larger when were closer to N_MIN
                    # print(float(b) / c) # this is small when were closer to N_MIN
                    p1 = 0.30 # p1 = probability of adding 1 device
                    p0 = (1.00-p1)*(float(b) / c) # p0 = probability of adding 0 devices
                    p2 = (1.00-p1)*(float(a) / c) # p2 = probability of adding 2 devices
                    # print('p0=%.2f   p1=%.2f   p2=%.2f' % (p0, p1, p2))
                    rn = random.uniform(0, 1)
                    if 0.00 <= rn <= p0:    num_devices_to_add = 0
                    if p0    < rn <= p0+p1: num_devices_to_add = 1
                    if p0+p1 < rn <= 1.00:  num_devices_to_add = 2
                    # print('num_devices_to_add = %d' % num_devices_to_add)
                while num_devices_to_add > 0:
                    num_devices_to_add -= 1
                    devices.append(Device(devices))

            self.devices = devices
            self.connections, self.edges = self.set_connections(self.devices)


        self.t1 = t # update t1 at end of update()

    # create devices that move around the map
    def init_moving_devices(self, verbose=False):
        devices = []
        n_to_create = int(((N_MAX - N_MIN) / 2) + N_MIN) # create halfway between N_MIN and N_MAX
        while n_to_create > 0:
            n_to_create -= 1
            devices.append(Device(devices))
        if verbose:
            print('Nodes:')
            num_devices = len(devices)
            for i, d in enumerate(devices):
                d.print_d(num_devices, i=i+1)
        return devices

    # determine which devices are current within signal range of each other
    # {keys=devices, value={key=neighbor_device : value=distance}}
    def set_connections(self, devices, verbose=False):
        connections = {} # {keys=devices : value={key=neighbor_device, value=distance}}
        edges = [] # [{device0, device1}, {device2, device0}, ...]
        for d0 in devices:
            if not isinstance(d0, Device): continue
            neighbors = self.set_direct_neighbors(d0, devices)
            connections[d0] = neighbors
            for d in neighbors.keys():
                if {d0, d} not in edges:
                    edges.append({d0, d})
        if verbose:
            print('\nConnections:')
            num_devices = len(devices)
            for i, (d0, neighbors) in enumerate(connections.items()):
                print()
                d0.print_d(num_devices=num_devices, i=i+1)
                num_neighbors = len(neighbors)
                print('    has %d direct neighbor(s)' % num_neighbors)
                if num_neighbors > 0:
                    for j, neighbor in enumerate(neighbors):
                        neighbor.print_d(num_devices=num_neighbors, i=j+1, start_space='        ')
            print('\n%d Edges:' % len(edges))
            for i, edge in enumerate(edges):
                edge = tuple(edge)
                d1, d2 = edge[0], edge[1]
                print('   edge %d' % (i+1))
                d1.print_d(num_devices=2, i=1, start_space='        ')
                d2.print_d(num_devices=2, i=2, start_space='        ')
                print()
            print()
        return connections, edges

    # determine which devices are within signal range of device d0
    # {key=neighboring device : value=distance}
    def set_direct_neighbors(self, d0, devices, verbose=False):
        neighbors = {} # {key = neighboring device : value = distance}
        for d in devices:
            if not isinstance(d0, Device): continue
            if d != d0:
                dist = math.sqrt((d.n.x - d0.n.x)**2 + (d.n.y - d0.n.y)**2)
                if dist <= R:
                    neighbors[d] = dist
        if verbose:
            print('%d Direct Neighbors:' % len(neighbors.keys()))
            for neighbor in neighbors.keys(): neighbor.print_d(newline_start=False)
        return neighbors


class Controller(object):

    # NOTE mouse must be over GUI for keyboard commands to be noticed
    def __init__(self, model, view):

        self.model = model
        self.view = view
        self.paused = False
        self.buffer = ''


    # respond to any user input
    def handle_event(self, event, verbose=False):
        if event.type != KEYDOWN:
            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse_pos = pygame.mouse.get_pos()
                mx, my = mouse_pos[0], mouse_pos[1]
                if verbose: print('mouse position = (%d,%d)' % (mx, my))

                if event.button == 4:
                    if verbose: print('mouse wheel scroll up')
                elif event.button == 5:
                    if verbose: print('mouse wheel scroll down')
                elif event.button == 1:
                    if verbose: print('mouse left click')
                    self.model.selected_device = self.select_or_deselect_device(mx, my, verbose=True)

                elif event.button == 3:
                    if verbose: print('mouse right click') # 2 finger click on Mac
                else:
                    if verbose: print('event.button = %d' % event.button)

        elif event.key == pygame.K_SPACE:
            if verbose: print('space bar')
            self.model.pause_devices = not self.model.pause_devices

        elif event.key == pygame.K_n:
            if verbose: print('n')
            self.model.pause_nodes = not self.model.pause_nodes

        elif event.key == pygame.K_d:
            if verbose: print('d')
            self.view.d = not self.view.d # toggle draw message dots

        elif event.key == pygame.K_r:
            if verbose: print('r')
            self.view.r = not self.view.r # toggle draw signal rings

        elif event.key == pygame.K_c:
            if verbose: print('c')
            self.view.c = not self.view.c # toggle draw connection lines

        elif event.key == pygame.K_RETURN:
            print('self.buffer = %s' % self.buffer)
            if self.buffer == 'p0':
                self.view.p0 = not self.view.p0
                if verbose: print('p0 = %s' % self.view.p0)
            elif self.buffer == 'p1':
                self.view.p1 = not self.view.p1
                if verbose: print('p1 = %s' % self.view.p1)
            elif self.buffer == 'e0':
                self.view.e0 = not self.view.e0
                if verbose: print('e0 = %s' % self.view.p1)
            elif self.buffer == 'e1':
                self.view.e1 = not self.view.e1
                if verbose: print('e1 = %s' % self.view.e1)
            elif self.buffer == 'm0':
                self.view.m0 = not self.view.m0
                if verbose: print('m0 = %s' % self.view.m0)
            elif self.buffer == 'm1':
                self.view.m1 = not self.view.m1
                if verbose: print('m1 = %s' % self.view.m0)
            else:
                if verbose: print('unknown buffer: %s' % self.buffer)
            self.buffer = ''

        elif event.key == pygame.K_UP:
            if verbose: print('up arrow')
        elif event.key == pygame.K_DOWN:
            if verbose: print('down arrow')
        elif event.key == pygame.K_LEFT:
            if verbose: print('left arrow')
        elif event.key == pygame.K_RIGHT:
            if verbose: print('right arrow')
        else:
            # print(event.key)
            # print('[%s]' %event.unicode)
            # print()
            self.buffer += event.unicode
            print(self.buffer, end="\r", flush=True)

        # # another way to do it, gets keys currently pressed
        # keys = pygame.key.get_pressed()  # checking pressed keys
        # if keys[pygame.K_UP]:
        #     pass # etc. ...

    # click unselected device to select it,
    # click selected device again to deselect it
    def select_or_deselect_device(self, mx, my, verbose=False):
        x, y = mx / SCREEN_SCALE, my / SCREEN_SCALE # mx and my are scaled to display, not the model
        selected_device = self.find_closest_device(x, y, verbose=False)
        if model.selected_device == None:
            return selected_device
        else:
            if model.selected_device == selected_device:
                return None
            else:
                return selected_device

    # return the device in the model that is currently closest to the point (x, y)
    def find_closest_device(self, x, y, verbose=False):
        closest_device = None
        closest_dist = 5*W # init closest_dist bigger than any possible dist
        for d in self.model.devices:
            dist = math.sqrt((x - d.n.x)**2 + (y - d.n.y)**2)
            if dist < closest_dist:
                closest_device = d
                closest_dist = dist
        if verbose:
            if closest_device != None:
                print('closest device to (%.4f, %.4f) is at (%.4f, %.4f)' \
                    % (x, y, closest_device.n.x, closest_device.n.y))
            else:
                print('closest device is None')
        return closest_device


if __name__ == '__main__':

    # pygame setup
    pygame.init()
    model = Model()
    view = View(model)
    controller = Controller(model, view)

    # frame rate variables
    start_time = time.time()
    iterations = 0

    while True:

        # output frame rate
        if OUTPUT_FRAME_RATE:
            iterations += 1
            if time.time() - start_time > 1:
                start_time += 1
                print('%s fps' % iterations)
                iterations = 0

        # handle user input
        for event in pygame.event.get():
            if event.type == QUIT: # Xing out of window
                pygame.quit()
                sys.exit()
            else:
                controller.handle_event(event, verbose=True)

        # update the model
        model.update(verbose=True)

        # display the view
        view.draw()
        view.screen.blit(view.surface, (0,0))
        pygame.display.update()
        # time.sleep(1.0) # control frame rate (in seconds)
