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

    SOURCES:

        https://www.pygame.org/docs/

        PyGame color Codes
        https://www.webucator.com/blog/2015/03/python-color-constants-module/

    OTHER:

    IDEAS:

        if the first neighbor can verify the sender is who they say they are, they can pass on that verification, and then verify they're who THEY say they are, and the 2nd neighbor can verify the same, ... and a path can be built

        what if you used the position triangluation to verify that someone isn't using a server farm to run a bunch of nodes
        in order for nodes to count they need to be spread out (and moving frequenty? what about desktops) to exibit normal device behavior

    TO DO:

        NOW:

            do signal stuff
                make mid_delivery_messages not have a receiver node
                    if distance between the send_pt and a device is inbetween the
                    the message distance_travelled before and after this timestep
                        (where the message dist_travelled is incremented by SIGNAL_SPEED)
                        then deliver the message to the device
                            we need to make it somehow account for the fact that if the device
                            is right on the edge between
                                d1, dist_travelled, and
                                d2, dist_travelled + SIGNAL_SPEED
                            and then it moves from >d2 to <d2, it could receive the signal twice
                            we also need to make sure the sender_node doesn't receive its own signal
                                however so long as MAX_VEL of a device is less than the SIGNAL_SPEED,
                                if we move the devices AND THEN send the message and give the message
                                a starting dist_travelled of SIGNAL_SPEED then ... idk ...
                                ... i think the sender_node won't receive the message
                    if dist_travelled >= R:
                        delete signal

                draw signals better

                    circles underneath everything else

                    why is there so many echos?
                        i think each echo is technically to everyone, and its the matching message that specifies who its for

                        make it so the ping

                    make each node have a number in its circle in the display (just its index in the list of all nodes)

                    make it so you can click on a node

                        when you click on a node, information appears about
                        its public key
                        its messages list

                        make it so you can toggle viewing that nodes range

                        make it so you can toggle drawing connection lines to this node's direct neighbors

                        make it so you can change R (and maybe other constants) mid simulation

                    make it so you can send a message manually from one node to another

                    make it so you can toggle drawing all connection lines between nodes (dark blue)
                    make it so pings are sent out as green line segments along the connection line
                    make it so echos are sent out as red   line segments along the connection line

                    make it so you can toggle drawing messages as expanding circles
                        pings are dark green circles
                        echos are dark red circles
                        messages are dark blue circles

                self.model.selected_device
                    view pings, incoming echoes, outgoing/incoming messages

                how much faster are the signals simulated paused/unpaused?

                keep ping the way it was originally made,
                but increase the speed, and decrease the period
                because in reality, if they ping/pong back and forth it will take up unnessessary amounts of band width
                    so doing it on a period is better

            do controls
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

                #################### these need to be fixed ###############################

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

                ###########################################################################


            maybe use this to improve device movement
            https://github.com/florimondmanca/pyboids
            where each boid has its own destination

        '''



class View(object):

    def __init__(self, model, show_view=True):

        self.model = model
        self.screen = pygame.display.set_mode(SCREEN_SIZE) # a pygame screen
        self.surface = pygame.Surface(SCREEN_SIZE) # a pygame surface is the thing you draw on

        self.show_view = show_view # toggle display
        self.show_controls = False # toggle control display


    def draw(self):

        # fill background
        self.surface.fill(pygame.Color('black'))

        self.draw_selected_device_range()
        self.draw_in_range_connections()
        # self.draw_pings()
        # self.draw_echos()
        # self.draw_messages()
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
                pygame.Color('cyan'),
                (x, y), 5) # (x,y), radius

    def draw_in_range_connections(self):
        for (d1, d2) in model.edges:
            x1, y1 = int(SCREEN_SCALE*d1.n.x), int(SCREEN_SCALE*d1.n.y)
            x2, y2 = int(SCREEN_SCALE*d2.n.x), int(SCREEN_SCALE*d2.n.y)
            pygame.draw.line(
                self.surface,
                pygame.Color('blue'),
                (x1, y1), (x2, y2), 1)

    def draw_paths_to_dst(self):
        for d in self.model.devices:
            x1, y1 = int(SCREEN_SCALE * d.n.x),    int(SCREEN_SCALE * d.n.y)
            x2, y2 = int(SCREEN_SCALE * d.dst[0]), int(SCREEN_SCALE * d.dst[1])
            pygame.draw.line(
                self.surface,
                (255,255,255),
                (x1, y1), (x2, y2), 1) # (start_x, start_y), (end_x, end_y), thickness
            pygame.draw.circle(
                self.surface,
                (255,0,0),
                (x2, y2), 5) # (x,y), radius

    def draw_message_dot(self, mdm, color):
        sn, rn = mdm['sender_device'].n, mdm['receiver_device'].n
        dist_sn_to_rn = math.sqrt((sn.x - rn.x)**2 + (sn.y - rn.y)**2)
        x = int(SCREEN_SCALE * ((mdm['dist_traveled'] / dist_sn_to_rn)*(rn.x - sn.x) + sn.x))
        y = int(SCREEN_SCALE * ((mdm['dist_traveled'] / dist_sn_to_rn)*(rn.y - sn.y) + sn.y))
        pygame.draw.circle(
            self.surface,
            pygame.Color(color),
            (x, y), 2) # (x,y), radius

    def draw_message_circle(self, mdm, color, fade=True):
        r = mdm['dist_traveled']
        if fade:
            non_zero_rgb_value = int(255 * ((float(R - r) / R)**10 if r < R else 0.0))
            if color == 'darkgreen': color = (0, non_zero_rgb_value, 0)
            if color == 'cyan':      color = (0, 0, non_zero_rgb_value)
            if color == 'darkred':   color = (non_zero_rgb_value, 0, 0)
        else:
            color = pygame.Color(color)
        r = int(SCREEN_SCALE * r)
        if r > 1:
            x = int(SCREEN_SCALE * mdm['send_pt' ][0])
            y = int(SCREEN_SCALE * mdm['send_pt' ][1])
            pygame.draw.circle(
                self.surface,
                color,
                (x, y), r, 1) # (x,y), radius

    def draw_pings(self):
        for mdm in self.model.mid_delivery_messages:
            if mdm['sender_device'] != model.devices[0]: continue # just draw 1 device's ping right now
            if mdm['message'].m.startswith('PING'):
                self.draw_message_circle(mdm, 'darkgreen', fade=True)
                self.draw_message_dot(mdm, 'green')

    def draw_echos(self):
        for mdm in self.model.mid_delivery_messages:
            if mdm['receiver_device'] != model.devices[0]: continue # just draw 1 device's return echos right now
            if mdm['message'].m.startswith('ECHO'):
                self.draw_message_circle(mdm, 'darkred', fade=True)
                self.draw_message_dot(mdm, 'red')

    def draw_messages(self):
        for mdm in self.model.mid_delivery_messages:
            if not mdm['message'].m.startswith('PING') \
            and not mdm['message'].m.startswith('ECHO'):
                self.draw_message_circle(mdm, 'cyan', fade=True)
                self.draw_message_dot(mdm, 'cyan')

    def draw_text(self, text, x, y, size, \
        text_color = (100, 100, 100), \
        background_color = (0, 0, 0)):

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

        # create devices
        self.devices = self.init_moving_devices(verbose=False)
        self.connections, self.edges = self.set_connections(self.devices, verbose=False)

        # list of messages that are being delivered. Used just for time delay in simulation
        # format: [(receiver_node, delivery_time, message), ...]
        self.mid_delivery_messages = []

        t = time.time()
        self.t1 = t # t1 = time of previous time step (1 time step in the past)
        self.t2 = t # t2 = time of previous cellular

        # window parameters / drawing
        self.show = True # show current model

        # controller variables
        self.selected_device = None # device user clicked on
        self.pause_movement  = False # pause/play movement


    # main_loop of the model
    def update(self, verbose=False):

        t = time.time()
        # if verbose: print('%s\nt = %s' % ('-'*80, t))

        # # move message signals forward,
        # # deliver message if it's reached the receiver_node,
        # # else keep it in the mid_delivery_messages list
        # new_mid_delivery_messages = []
        # for mdm in self.mid_delivery_messages:
        #     mdm['dist_traveled'] += (SIGNAL_SPEED * (t - self.t1))
        #     sp, rn = mdm['send_pt'], mdm['receiver_device'].n
        #     dist_send_pt_to_rn = math.sqrt((sp[0] - rn.x)**2 + (sp[1] - rn.y)**2)
        #     if mdm['dist_traveled'] >= dist_send_pt_to_rn: # reached receiver device
        #         rn.messages.append(mdm['message'])
        #     else:
        #         new_mid_delivery_messages.append(mdm)
        # self.mid_delivery_messages = new_mid_delivery_messages

        # # run the main loop of each node
        # for i, d in enumerate(self.devices):

        #     if not isinstance(d, Device): continue

        #     # every node send out a ping signal on and
        #     # respond to any messages it has received
        #     # n.print_n(i=i+1, newline_start=True)
        #     ping, sent_messages = d.n.main_loop()

        #     if ping != None:
        #         self.add_message_to_mid_delivery_messages(ping, d)
        #     for m in sent_messages:
        #         self.add_message_to_mid_delivery_messages(m, d)

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
        if not self.pause_movement:
            devices = []
            num_devices_that_reached_their_dst = 0
            for d in self.devices:
                reached_dst = d.move(self.connections[d], verbose=False)
                if reached_dst:
                    num_devices_that_reached_their_dst += 1
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


        # # update the Nodes in the network every AUTOMATA_PERIOD
        # if (t - self.t2) > AUTOMATA_PERIOD:
        #     self.evolve_grid(verbose=True)
        #     self.t2 = t

        self.t1 = t # update t1 at end of update()

        #    input()
        # sys.exit()

    # determine which devices are current within signal range of each other
    # {keys=devices, value={key=neighbor_device : value=distance}}
    def set_connections(self, devices, verbose=False):
        connections = {} # {keys=devices : value={key=neighbor_device, value=distance}}
        edges = []
        for d0 in devices:
            if not isinstance(d0, Device): continue
            neighbors = self.set_direct_neighbors(d0, devices)
            connections[d0] = neighbors
            for d in neighbors.keys():
                if (d0, d) not in edges \
                and (d, d0) not in edges:
                    edges.append((d0, d))
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
                print('   edge %d' % (i+1))
                edge[0].print_d(num_devices=2, i=1, start_space='        ')
                edge[1].print_d(num_devices=2, i=2, start_space='        ')
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

    # put message from device d0 in list of messages that are mid-delivery
    def add_message_to_mid_delivery_messages(self, message, d0):
        for neighbor, dist in self.connections[d0].items():
            self.mid_delivery_messages.append({
                'sender_device'    : d0,
                'receiver_device'  : neighbor,
                'dist_traveled'    : 0.00,
                'send_pt'          : (d0.n.x, d0.n.y),
                'message'          : message
            })

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


class Controller(object):

    def __init__(self, model, view):

        self.model = model
        self.view = view
        self.paused = False


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
            self.model.pause_movement = not self.model.pause_movement

        elif event.key == pygame.K_k:
            if verbose: print('k')
            view.show_controls = not view.show_controls

        elif event.key == pygame.K_v:
            if verbose: print('v')
            view.show_view = not view.show_view

        elif event.key == pygame.K_UP:
            if verbose: print('up arrow')
        elif event.key == pygame.K_DOWN:
            if verbose: print('down arrow')
        elif event.key == pygame.K_LEFT:
            if verbose: print('left arrow')
        elif event.key == pygame.K_RIGHT:
            if verbose: print('right arrow')
        else: pass

        # # another way to do it, gets keys currently pressed
        # keys = pygame.key.get_pressed()  # checking pressed keys
        # if keys[pygame.K_UP]:
        #     pass # etc. ...

    # click unselected device to select it,
    # click selected device again to deselect it
    def select_or_deselect_device(self, mx, my, verbose=False):
        x, y = mx / SCREEN_SCALE, my / SCREEN_SCALE # mx and my are scaled to display, not the model
        selected_device = self.find_closest_device(x, y, verbose=True)
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
    view = View(model, show_view=True)
    controller = Controller(model, view)

    # loop variable setup
    running = True
    start_time = time.time()
    iterations = 0



    while running:

        # output frame rate
        if OUTPUT_FRAME_RATE:
            iterations += 1
            if time.time() - start_time > 1:
                start_time += 1
                print('%s fps' % iterations)
                iterations = 0

        # handle user input
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            else:
                controller.handle_event(event, verbose=True)

        # update the model
        model.update(verbose=True)

        # display the view
        if view.show_view:
            view.draw()
            view.screen.blit(view.surface, (0,0))
            pygame.display.update()

            # time.sleep(1.0) # control frame rate (in seconds)

    pygame.quit()
    sys.exit()
