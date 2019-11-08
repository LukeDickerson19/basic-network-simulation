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
from message import Message
import numpy as np

''' NOTES:

    TO DO:

        add verbose statements to update and use them to debug it, then debug display

        keep ping the way it was originally made,
        but increase the speed, and decrease the period
        because in reality, if they ping/pong back and forth it will take up unnessessary amounts of band width

        make each node has a start and stop point
            they're born at point A (random location)
            they move to point B (random location)
                avoiding other nodes along the way (not nessessary)
            then they die at point B

            could this achieve networks:
                growing
                shrinking
                splitting
                merging

            variable number of nodes
            theres a minimum number and a max
            initially create halfway between
            when a node n0 reaches its destination dst
                create 0, 1 or 2 nodes
                    if there was N_MIN nodes before n0 reached its dst
                        create 2
                    elif there was N_MAX nodes before n0 reached its dst
                        create 0
                    else:
                        random([0, 1, 2])
                        # near N_MIN
                            0 low chance
                            1 medium chance
                            2 high chance
                        # near N_MAX
                            0 high chance
                            1 medium chance
                            2 low chance


            for each node:
                v0 = get vector to dest
                v = v0
                for close nodes cn
                    get angle to node
                    get opposite angle
                    vect_magnitude by their closeness (1 / dist)
                    vector sum to v

                make velocity like 1 pixel or very small so
                if a node is surrounded by a bunch of nodes and its vector sum pushes it into a node
                it will be closer the next time but not NEAR at all colliding and now that its closer
                its new vector sum will push it away from the node its getting closer to colliding with

                each message will need a sent_pos = (x, y) to exand from where it was sent originally


            maybe use this
            https://github.com/florimondmanca/pyboids
            where each boid has its own destination




        i need a cellular automata that has
            nodes constantly joining and leaving the network
            networks constantly growing, shrinking, splitting and merging

            HOWEVER:
                when a node joins, it joins a network. It does not try to start its own network

                8 sournding squares
                if im 1:
                    if 7 or more of my neighboring squares is 1, i turn to 0
                    if

                if im 0:

        then do create_random_network
            see constants.py
            fixed number of nodes in a specifed


        display:

            why is there so many echos?
                i think each echo is technically to everyone, and its the matching message that specifies who its for

                make it so the ping

            make it so dark blue circle outline that emits from each node to represent sending a message
            draw

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

            maybe make messages of all kinds fade as they get farther away


        see create_network0
            figure out how to get a fully connected network that is distributed evenly
            over the entire area ... more or less

    SOURCES:

        https://www.pygame.org/docs/

    OTHER:

    IDEAS:

        if the first neighbor can verify the sender is who they say they are, they can pass on that verification, and then verify they're who THEY say they are, and the 2nd neighbor can verify the same, ... and a path can be built

        what if you used the position triangluation to verify that someone isn't using a server farm to run a bunch of nodes
        in order for nodes to count they need to be spread out (and moving frequenty? what about desktops) to exibit normal device behavior

        '''


class PyGameView(object):
    '''
        PyGameView controls the display
    '''

    def __init__(self, model, show_view=True):

        self.model = model
        self.screen = pygame.display.set_mode(SCREEN_SIZE) # a pygame screen
        self.surface = pygame.Surface(SCREEN_SIZE) # a pygame surface is the thing you draw on

        self.show_view = show_view # toggle display
        self.show_controls = False # toggle control display


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

    def draw(self):

        # fill background
        self.surface.fill(pygame.Color('black'))

        self.draw_in_range_connections()
        self.draw_pings()
        self.draw_echos()
        # self.draw_messages()
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

    def move(self, close_devices):
        x, y = self.n.x, self.n.y
        dx, dy = x-self.dst[0], y-self.dst[1] # x and y dist to dst
        dst_dist = math.sqrt(dx**2 + dy**2) # distance to destination
        theta0 = np.arctan2(dx, dy) # v0 = angle to dst
        mag = min(self.vel, dst_dist)
        v0 = (mag * np.cos(theta0), mag * np.sin(theta0)) # v0 = vector to destination
        v_sum = v0
        for d, dist in close_devices.items():
            theta = np.arctan2(x-d.n.x, y-d.n.y) + np.pi
            mag = float(1 / dist)
            v = (mag * np.cos(theta0), mag * np.sin(theta0)) # v0 = vector to destination
            v_sum = (v_sum[0] + v[0], v_sum[1] + v[1])
        self.n.x += v_sum[0]
        self.n.y += v_sum[1]

    def print_d(self, num_devices, i='?', start_space='    ', newline_start=False):
        self.n.print_n(num_devices, i=i, start_space=start_space, newline_start=newline_start)

class Model(object):

    def __init__(self):
        '''
            initialize model, environment, and default keyboard controller states
        Args:
            width (int): width of window in pixels
            height (int): height of window in pixels
        '''

        # create network
        # self.nodes, self.connections = self.create_random_network(verbose=True)
        # self.nodes, self.connections = self.create_grid_network(verbose=True)
        self.devices = self.create_variable_network(verbose=True)
        self.connections, self.edges = self.set_connections(self.devices, verbose=True)

        # list of messages that are being delivered. Used just for time delay in simulation
        # format: [(receiver_node, delivery_time, message), ...]
        self.mid_delivery_messages = []

        t = time.time()
        self.t1 = t # t1 = time of previous time step (1 time step in the past)
        self.t2 = t # t2 = time of previous cellular

        # window parameters / drawing
        self.show = True # show current model

    def update(self, controller):

        # move message signals forward,
        # deliver message if it's reached the receiver_node,
        # else keep it in the mid_delivery_messages list
        t = time.time()
        new_mid_delivery_messages = []
        for mdm in self.mid_delivery_messages:
            mdm['dist_traveled'] += (SIGNAL_SPEED * (t - self.t1))
            sp, rn = mdm['send_pt'], mdm['receiver_device'].n
            dist_send_pt_to_rn = math.sqrt((sp[0] - rn.x)**2 + (sp[1] - rn.y)**2)
            if mdm['dist_traveled'] >= dist_send_pt_to_rn: # reached receiver device
                rd = d['receiver_device']
                m  = d['message']
                rd.n.messages.append(m)
            else:
                new_mid_delivery_messages.append(mdm)
        self.mid_delivery_messages = new_mid_delivery_messages

        # run the main loop of each node
        for i, d in enumerate(self.devices):

            if not isinstance(d, Device): continue

            # every node send out a ping signal on and
            # respond to any messages it has received
            # n.print_n(i=i+1, newline_start=True)
            ping, sent_messages = d.n.main_loop()

            if ping != None:
                self.add_message_to_mid_delivery_messages(ping, d)
            for m in sent_messages:
                self.add_message_to_mid_delivery_messages(m, d)

        # move the devices, and update connections and edges
        for d in self.devices:
            d.move(self.connections[d])
        self.connections, self.edges = self.set_connections(self.devices)


        # # update the Nodes in the network every AUTOMATA_PERIOD
        # if (t - self.t2) > AUTOMATA_PERIOD:
        #     self.evolve_grid(verbose=True)
        #     self.t2 = t

        self.t1 = t # update t1 at end of update()

        #    input()
        # sys.exit()

    def set_connections(self, devices, verbose=False):
        connections = {} # {keys=devices, value={key=neighbor_device, value=distance}}
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
                d0.print_d(num_devices, i=i+1)
                num_neighbors = len(neighbors)
                print('    has %d direct neighbor(s)' % num_neighbors)
                if num_neighbors > 0:
                    for j, neighbor in enumerate(neighbors):
                        neighbor.print_d(num_neighbors, i=j+1, start_space='        ')
            print('\n%d Edges:' % len(edges))
            for i, edge in enumerate(edges):
                print('   edge %d' % (i+1))
                edge[0].print_d(2, i=1, start_space='        ')
                edge[1].print_d(2, i=2, start_space='        ')
                print()
            print()
        return connections, edges

    def set_direct_neighbors(self, d0, devices, verbose=False):
        neighbors = {} # key = neighboring device, value = distance
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

    def add_message_to_mid_delivery_messages(self, message, d0):
        for neighbor, dist in self.connections[d0].items():
            self.mid_delivery_messages.append({
                'sender_device'    : d0,
                'receiver_device'  : neighbor,
                'dist_traveled'    : 0.00,
                'send_pt'          : (d0.n.x, d0.n.y),
                'message'          : message
            })

    def create_variable_network(self, verbose=False):
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
    def get_num_nodes_to_create(self):
        current_num_nodes = len(self.nodes)
        min_nodes_possible_to_create = max(N_MIN - current_num_nodes, N_CREATE_MIN)
        max_nodes_possible_to_create = min(N_MAX - current_num_nodes, N_CREATE_MAX)
        return random.uniform(min_nodes_possible_to_create, max_nodes_possible_to_create)


    def fully_connected_network(self):
        for n in self.nodes:
            neighbors = self.set_direct_neighbors(n)
            if len(neighbors.keys()) == 0:
                return False
        return True
    # return a list of node networks
    def get_networks(self, nodes, verbose=False):

        def get_network_recurrsively(n0, network):
            network += [n0]
            for n in self.set_direct_neighbors(n0, unvisited_nodes):
                if n not in network:
                    network = get_network_recurrsively(n, network)
            return network

        networks = []
        nodes = list(filter(lambda n : isinstance(n, Node), nodes)) # for cellular automata
        unvisited_nodes = copy.deepcopy(nodes)
        while len(unvisited_nodes) > 0:
            n0 = unvisited_nodes[0]
            network = get_network_recurrsively(n0, [])
            networks.append(network)
            for n in network:
                unvisited_nodes.remove(n)

        if verbose:
            print('\n%d Networks:' % len(networks))
            for i, network in enumerate(networks):
                print('\nNetwork %d has %d node(s)' % (i+1, len(network)))
                for n in network:
                    n.print_n()

        return networks
    # network 0: N nodes constantly throughout all time steps for the entire simulation
    def create_random_network(self, verbose=False):
        nodes = [Node() for _ in range(N)]
        connections = self.set_connections(nodes)
        networks = self.get_networks(nodes, verbose=verbose)
        return nodes, connections
    # def create_network0(self, verbose=False):
    #     self.nodes = [Node()]
    #     while len(self.nodes) < N:
    #         n = Node()
    #         self.nodes.append(n)
    #         if len(self.set_direct_neighbors(n).keys()) == 0:
    #             self.nodes.remove(n)
    #     return self.nodes
    # def create_network0(self, verbose=False):
    #     self.nodes = [Node() for _ in range(N)]
    #     while not self.fully_connected_network():
    #         print('Fail')
    #         self.nodes = [Node() for _ in range(N)]
    #     if verbose:
    #         print('Created network0 of %d nodes' % N)
    #     return self.nodes

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


class PyGameKeyboardController(object):
    '''
        Keyboard controller that responds to keyboard input
    '''


    def __init__(self):

        self.paused = False


    def handle_event(self, event):
        if event.type != KEYDOWN:
            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse_pos = pygame.mouse.get_pos()
                print('mouse position = (%d,%d)' % (mouse_pos[0], mouse_pos[1]))

                if event.button == 4:
                    print('mouse wheel scroll up')
                elif event.button == 5:
                    print('mouse wheel scroll down')
                elif event.button == 1:
                    print('mouse left click')
                elif event.button == 3:
                    print('mouse right click')
                else:
                    print('event.button = %d' % event.button)
        elif event.key == pygame.K_SPACE:
            self.paused = not self.paused
        elif event.key == pygame.K_k:
            view.show_controls = not view.show_controls
        elif event.key == pygame.K_v:
            view.show_view = not view.show_view
        elif event.key == pygame.K_UP:
            print('up arrow')
        elif event.key == pygame.K_DOWN:
            print('down arrow')
        elif event.key == pygame.K_LEFT:
            print('left arrow')
        elif event.key == pygame.K_RIGHT:
            print('right arrow')
        else: pass

        # another way to do it, gets keys currently pressed
        keys = pygame.key.get_pressed()  # checking pressed keys
        if keys[pygame.K_UP]:
            pass # etc. ...



if __name__ == '__main__':

    # pygame setup
    pygame.init()
    model = Model()
    view = PyGameView(model, show_view=True)
    controller = PyGameKeyboardController()

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
                controller.handle_event(event)

        # update the model
        if not controller.paused:
            model.update(controller)

        # display the view
        if view.show_view:
            view.draw()
            view.screen.blit(view.surface, (0,0))
            pygame.display.update()

            # time.sleep(1.0) # control frame rate (in seconds)

    pygame.quit()
    sys.exit()
