

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

        can current router hardware communicate directly with each other, if they're in range?
            probably not, we need something that extends MILES, not the area of a house

    TO DO:

        NOW:

            display stuff


                the the block_printer fucks up when the text has more lines than the console can display
                    depending one however zoomed in the console text is
                    it would be awesome if this could be accounted for                

                percieved neighbors needs to be updated automatically
                    also, it might just be because its not auto-updated,
                    but why is it taking so long for a node to perceive all its neighbors?
                        it should take just one ping and subsequent echo to notice it

                i need some way to take other nodes off a nodes neighbors list
                if they dont return a ping, they're taken off

                t needs to be paused to when movement and signals a both simulaniously paused

                make it so you can click a button (r) and start the simulation over
                    reset t also

                make it so when you click on a node
                    information appears about
                        its neighbors' public keys, their estimated distance, and their actual distance

                    ... for some reason its not updating the terminal display when the number of neighbors
                    ... for the selected devices changes
                    ... its also saying sd.n.neighbors is an empty pd dataframe when it shouldn't be empty

                        don't forget, the neighbors field in the console dispay is its ACTUAL neighbors,
                            not the neighbors the sd thinks it has, the
                        maybe make a list of actual neighbors and actual dist,
                        and then make a separate list of believed neighbors

                        1st figure out how to update it the moment it changes
                        then figure out how to display the proper number of ACTUAL neighbors
                        then figure out how to display the actual distance from those neighbors
                        then figure out how to display the df of the believed neighbors
                        then check to see how accurate the estimated distance is from the real distance
                            especially after you change the variables below!

                increase signal speed a lot
                increase ping period a little bit
                decrease device speed a lot
                increase R a little bit
                    determine average walking speed of person in km/s
                    determine speed of light in km/s
                        if signal blasted past R in one time step would that fuck up anything
                    determine signal range of average cellphone in km
                    determine range of average cell tower:
                        45 miles
                        https://www.google.com/search?q=cell+tower+range&oq=cell+tower+range&aqs=chrome..69i57j0l5.3071j0j7&sourceid=chrome&ie=UTF-8

            controls stuff

                make it so you can send a message manually from one node to another
                and you can select from a list of all possible messages a node can make in the terminal

                    might need to create child class for node 1st to display all possible messages

                verify message display is working properly

                set up basic pk sk thing and fix display to support it
                    sha256

        EVENTUALLY:

            maybe pygame clock is better than time.time()
                clock = pygame.time.Clock()

            make simulation faster by:

                model could probably be made faster if we didn't copy over so much data
                    its done to avoid messing up the iteration by deleting during an iteration though
                        if we could find a way to delete without messing up the iteration,
                            for lists we could iterate by index and then decrement the index when we delete
                            what about dictionaries though?
                                aren't dictionary keys a set in python?
                                    does deleting from a set mess up iterating over it?

                    searching through the code for places where we don't have to copy over data
                    could be done simultaniously while we are searching for places to thread

                model could be faster if we did more stuff in parallel using

                    async lib
                        https://realpython.com/async-io-python/

                        Efficient Parallel Graph Algorithms in Python
                        https://pdfs.semanticscholar.org/54b9/22a51e5aa04e7512720348c2deda33e2e4ee.pdf

                    or just use basic threading
                        see threading_example1.py

                        once you thread it:
                            in the console output
                            change fps global variable to
                                model.fps
                                view.fps
                                controller.fps

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
                            for c in connections[d0]: # self.get_direct_neighbors(n0, unvisited_nodes):
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
                        #     if len(self.get_direct_neighbors(n).keys()) == 0:
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
                        connections = self.get_network_state(nodes)
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

                        connections = self.get_network_state(nodes)
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
                        self.connections = self.get_network_state(self.nodes)

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
                            self.evolve_grid(verbose=False)
                            self.t2 = t

                ####################################################################################


            maybe use this to improve device movement
            https://github.com/florimondmanca/pyboids
            where each boid has its own destination

        '''

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # don't display Pygame Intro at start of program
os.environ['SDL_VIDEO_WINDOW_POS'] = "650,10" # set GUI window start position
import time
import copy
import sys
import math
import random
import pandas as pd
from pygame.locals import QUIT, KEYDOWN
from constants import *
from node import Node
from device import Device
from message import Message
import numpy as np
from block_printer import BlockPrinter

# global variables
bp = BlockPrinter()
fps = 0 # frames per second

# print block to the console
def update_console(caller=''):
    caller = caller+'\n' if False else '' # display/mute caller output
    # return

    # simulation metrics
    sim_mtrcs = '\nSIMULATION METRICS:\n'
    sim_mtrcs += 'fps = %d\n' % fps

    # gui settings
    df = view.settings
    df = df.assign(STATE=lambda df : df.STATE.replace([True, False], ['ON', 'OFF'])) # convert True/False to ON/OFF
    df_title = '\nSIMULATION SETTINGS:\n'
    gui_settings = df_title + df.to_string() + '\n'

    # selected device info
    sd = model.selected_device
    selected_device_info = '\nSELECTED DEVICE:\n'
    if sd != None:

        selected_device_info += \
            '      Device No.:      %d\n' % sd.num + \
            '      Node Public Key: %s\n' % sd.n.sk

        pn = sd.n.neighbors # perceived neighbors (according to selected device)
        num_pn = pn.shape[0]
        an = model.connections[sd] # an = actual neighbors (according to simulation)
        an = pd.DataFrame({
            'Public Key'  : list(map(lambda d : d.n.sk, an.keys())),
            'Actual Dist' : list(an.values()),
            'Device No.'  : list(map(lambda d : d.num, an.keys()))
        })
        num_an = an.shape[0]
        selected_device_info += '%d Perceived Neighbor%s and %d Actual Neighbor%s:\n' % (
            num_pn, '' if num_pn == 1 else 's',
            num_an, '' if num_an == 1 else 's')
        both = pn.merge(an, how='outer')
        both['Error Dist'] = both['Estimated Dist'] - both['Actual Dist']
        both.sort_values('Estimated Dist', inplace=True, na_position='last')
        both.fillna('', inplace=True)
        both.reset_index(inplace=True, drop=True)
        both.index += 1
        both = both[['Public Key',  'Device No.', 'Estimated Dist', 'Actual Dist', 'Error Dist']]
        selected_device_info += both.to_string() + '\n'

    else:
        selected_device_info += 'None\n'

    # network info
    network_info = '\nNETWORK INFO:\n'
    network_info += '%d Devices in the Network\n' % len(model.devices)
    num_sub_nets = len(model.sub_networks)
    network_info += '%d Sub-Network%s:\n' % (num_sub_nets, '' if num_sub_nets == 1 else 's')
    sub_net_counts = list(map(lambda sub_net : len(sub_net), model.sub_networks))
    max_spaces1, max_spaces2 = len(str(num_sub_nets)), len(str(max(sub_net_counts)))
    for i, (num_devices, sub_net) in enumerate(zip(sub_net_counts, model.sub_networks)):
        i += 1
        sub_net_devices = set(map(lambda d : d.num, sub_net))
        num_spaces1 = max_spaces1 - len(str(i))
        num_spaces2 = max_spaces2 - len(str(num_devices))
        network_info += '   sub_net %d %shas %d %sdevice%s:%s %s\n' % (
            i,
            ' '*num_spaces1,
            num_devices,
            ' '*num_spaces2,
            '' if num_devices == 1 else 's', ' ' if num_devices == 1 else '', # plural or singular
            sub_net_devices)

    # print them in a stationary block
    bp.print(
        caller + \
        sim_mtrcs + \
        gui_settings + \
        selected_device_info + \
        network_info)



class View(object):

    def __init__(self, model):

        self.model = model
        self.screen = pygame.display.set_mode(SCREEN_SIZE) # a pygame screen
        self.surface = pygame.Surface(SCREEN_SIZE) # a pygame surface is the thing you draw on

        self.show_controls = False # toggle control display

        init_settings = [
            ('space', 'pause movement', model.pause_devices),
            ('s', 'pause signals', model.pause_signals),
            ('n',  'device number', True),
            ('c',  'connections',  True),
            ('d',  'message dots', True),
            ('r',  'signal rings', True),
            ('f',  'node signal flash', True),
            ('p0', 'pings of selected device', True),
            ('e0', 'echos of selected device', False),
            ('m0', 'messages of selected device', False),
            ('p1', 'pings of direct neighbors of selected device', False),
            ('e1', 'echos of direct neighbors of selected device', True),
            ('m1', 'messages of direct neighbors of selected device', False)
        ]
        self.settings = pd.DataFrame({
            'KEY'   : list(map(lambda x : x[0], init_settings)),
            'DRAW'  : list(map(lambda x : x[1], init_settings)),
            'STATE' : list(map(lambda x : x[2], init_settings))
        }).set_index('KEY')


    def draw(self):

        # fill background
        self.surface.fill(pygame.Color(BACKGROUND_COLOR[0]))


        self.draw_selected_device_range()
        if self.model.selected_device != None and self.settings.at['r', 'STATE']:
            self.draw_signals()
        if self.settings.at['c', 'STATE']:
            self.draw_in_range_connections()
        if self.model.selected_device != None and self.settings.at['d', 'STATE']:
            self.draw_messages()
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
            color = pygame.Color(SELECTED_DEVICE_COLOR[0])
            pygame.draw.circle(
                self.surface,
                color,
                (x, y), r)

    def draw_devices(self):
        if self.settings.at['n', 'STATE']:
            fontcolor = DEVICE_NUM_TEXT_COLOR[1]
            fontsize = 3 * DEVICE_SIZE
            basicfont = pygame.font.SysFont(None, fontsize)
        sd = self.model.selected_device
        for d in model.devices:
            if not isinstance(d, Device): continue
            x = int(SCREEN_SCALE*d.n.x)
            y = int(SCREEN_SCALE*d.n.y)
            color =  self.get_device_color(sd, d, d.sent_messages, self.model.dt)
            pygame.draw.circle(
                self.surface,
                color,
                (x, y), DEVICE_SIZE) # (x,y), radius
            if self.settings.at['n', 'STATE']:
                text_render = basicfont.render('%d' % d.num, True, fontcolor)
                x += DEVICE_SIZE * 0.90
                y += DEVICE_SIZE * 0.90
                self.surface.blit(text_render, (x, y)) # draw text
    def get_device_color(self, sd, d, sent_messages, dt):

        if  (not self.settings.at['f', 'STATE']) or \
            (sd == None) or \
            (sd != d and (not (d in self.model.connections[sd]))):
            return pygame.Color(DEVICE_DEFAULT_COLOR[0])

        if d == sd: # selected device
            _p, _e, _m = self.settings.at['p0', 'STATE'], self.settings.at['e0', 'STATE'], self.settings.at['m0', 'STATE']
        else: # neighbor
            _p, _e, _m = self.settings.at['p1', 'STATE'], self.settings.at['e1', 'STATE'], self.settings.at['m1', 'STATE']
        p, e, m = False, False, False
        for m in sent_messages:
            if _m:
                m = True
                d.message_dist = 0
                d.most_recent_message_type = 'message'
            elif _p and m.m.startswith('PING'):
                p = True
                d.ping_dist = 0
                if ((not _m) or (d.message_dist != 0)):
                    d.most_recent_message_type = 'ping'
            elif _e and m.m.startswith('ECHO'):

                # if self.settings.at['e1', 'STATE']: only do echo's meant for the sd (if e1 )
                # if self.settings.at['e0', 'STATE']: draw all its (the sd's) echos
                if self.settings.at['e1', 'STATE']:
                    _, rs, _ = d.n.parse_echo(m) # rs = random string
                    if rs not in sd.n.pings.keys():
                        continue

                e = True
                d.echo_dist = 0
                if ((not _m) or (d.message_dist != 0)) and ((not _p) or (d.ping_dist != 0)):
                    d.most_recent_message_type = 'echo'

        if p:
            ping_color = DEVICE_PING_COLOR[1]
        else:
            if d.ping_dist != None:
                d.ping_dist += SIGNAL_SPEED * dt
                if d.ping_dist > R:
                    d.ping_dist = None
                    ping_color = DEVICE_DEFAULT_COLOR[1]
                else:
                    ping_color = faded_color(
                        DEVICE_PING_COLOR[1],
                        DEVICE_DEFAULT_COLOR[1],
                        f=1.0 - (float(R - d.ping_dist) / R)**2)
            else:
                ping_color = DEVICE_DEFAULT_COLOR[1]

        if e:
            echo_color = DEVICE_ECHO_COLOR[1]
        else:
            if d.echo_dist != None:
                d.echo_dist += SIGNAL_SPEED * dt
                if d.echo_dist > R:
                    d.echo_dist = None
                    echo_color = DEVICE_DEFAULT_COLOR[1]
                else:
                    echo_color = faded_color(
                        DEVICE_ECHO_COLOR[1],
                        DEVICE_DEFAULT_COLOR[1],
                        f=1.0 - (float(R - d.echo_dist) / R)**2)
            else:
                echo_color = DEVICE_DEFAULT_COLOR[1]

        if m:
            message_color = DEVICE_MESSAGE_COLOR[1]
        else:
            if d.message_dist != None:
                d.message_dist += SIGNAL_SPEED * dt
                if d.message_dist > R:
                    d.message_dist = None
                    message_color = DEVICE_DEFAULT_COLOR[1]
                else:
                    message_color = faded_color(
                        DEVICE_MESSAGE_COLOR[1],
                        DEVICE_DEFAULT_COLOR[1],
                        f=1.0 - (float(R - d.message_dist) / R)**2)
            else:
                message_color = DEVICE_DEFAULT_COLOR[1]

        # if d == d0:
        #     print(d.most_recent_message_type)

        if _m and d.most_recent_message_type == 'message': return message_color
        if _p and d.most_recent_message_type == 'ping':    return ping_color
        if _e and d.most_recent_message_type == 'echo':    return echo_color
        return pygame.Color(DEVICE_DEFAULT_COLOR[0])

    def draw_in_range_connections(self):
        for edge in model.edges:
            edge = tuple(edge)
            d1, d2 = edge[0], edge[1]
            x1, y1 = int(SCREEN_SCALE*d1.n.x), int(SCREEN_SCALE*d1.n.y)
            x2, y2 = int(SCREEN_SCALE*d2.n.x), int(SCREEN_SCALE*d2.n.y)
            pygame.draw.line(
                self.surface,
                pygame.Color(CONNECTION_COLOR[0]),
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
            # if not signal['message_type'] == 'echo': continue
            d0 = signal['sender_device']
            if not (
                (
                    d0 == sd and (
                        (self.settings.at['m0', 'STATE']) or
                        (self.settings.at['p0', 'STATE'] and signal['message_type'] == 'ping') or
                        (self.settings.at['e0', 'STATE'] and signal['message_type'] == 'echo')
                    )
                ) or (
                    d0 in self.model.connections[sd] and (
                        (self.settings.at['m1', 'STATE']) or
                        (self.settings.at['p1', 'STATE'] and signal['message_type'] == 'ping') or
                        (self.settings.at['e1', 'STATE'] and signal['message_type'] == 'echo')
                    )
                )
            ): continue

            color = DOT_MESSAGE_COLOR[0]
            if signal['message_type'] == 'ping': color = DOT_PING_COLOR[0]
            if signal['message_type'] == 'echo': color = DOT_ECHO_COLOR[0]
            self.draw_message_dot(signal, color, sd)
    def draw_message_dot(self, signal, color, sd):
        sn, sp = signal['sender_device'].n, signal['send_pt']
        cx, cy, r = sp[0], sp[1], signal['dist_traveled'] # circle variables
        for _edge in self.model.edges:
            edge = tuple(_edge)

            # filter which dots to draw
            if sd not in edge: continue # only draw signals going to/from sd
            if signal['message_type'] == 'echo': # only draw echo dot to intended receiver_node
                nd = edge[0] if edge[1] == sd else edge[1] # nd = neighboring device (of selected device)
                rd = nd if sn == sd.n else sd # rd = receiver device
                rn_id, _, _ = sd.n.parse_echo(signal['message']) # receiver node according to echo message
                if rd.n.sk != rn_id: continue
                if {rd, signal['sender_device']} != _edge: continue # only draw on the edge with both sender and receiver device
            if signal['message_type'] == 'ping':
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
                    (x, y), DOT_SIZE) # (x,y), radius

    def draw_signals(self):
        sd = self.model.selected_device
        sd_conns = self.model.connections[sd] if sd != None else None
        for signal in self.model.signals:

            d0 = signal['sender_device']
            if not (
                (
                    d0 == sd and (
                        (self.settings.at['m0', 'STATE']) or
                        (self.settings.at['p0', 'STATE'] and signal['message_type'] == 'ping') or
                        (self.settings.at['e0', 'STATE'] and signal['message_type'] == 'echo')
                    )
                ) or (
                    d0 in self.model.connections[sd] and (
                        (self.settings.at['m1', 'STATE']) or
                        (self.settings.at['p1', 'STATE'] and signal['message_type'] == 'ping') or
                        (self.settings.at['e1', 'STATE'] and signal['message_type'] == 'echo')
                    )
                )
            ): continue

            if signal['message_type'] == 'echo': # only draw echo dot to intended receiver_node
                rn_id, _, _ = sd.n.parse_echo(signal['message']) # rn_id = receiver node id

                if d0 == sd:
                    pass # draw signal for all echos
                else:
                    # only draw signal if the echo is intended for sd
                    if rn_id == sd.n.sk:
                        pass
                    else:
                        continue

            color = SIGNAL_MESSAGE_COLOR[1]
            if signal['message_type'] == 'ping': color = SIGNAL_PING_COLOR[1]
            if signal['message_type'] == 'echo': color = SIGNAL_ECHO_COLOR[1]
            self.draw_signal_ring(signal, color, sd, fade=True)
    def draw_signal_ring(self, signal, color, sd, fade=True):
        if fade:

            def faded_color(col1, col2, f=1.0):
                # col1 = (r1, g1, b1)
                # col2 = (r2, g2, b2)
                # f = fade = float between 0 and 1
                # return the interpolation of col1 and col2 at point f
                return (
                    int(col1[0] + (col2[0] - col1[0])*f),
                    int(col1[1] + (col2[1] - col1[1])*f),
                    int(col1[2] + (col2[2] - col1[2])*f))

            r = signal['dist_traveled'] # r = model radius
            _r = int(SCREEN_SCALE * r) # _r = display radius
            f = 1.0 - (float(R - r) / R)**4
            if _r > SIGNAL_RING_THICKNESS:
                x, y = signal['send_pt']
                _x, _y = int(SCREEN_SCALE * x), int(SCREEN_SCALE * y)
                dx, dy = x - sd.n.x, y - sd.n.y
                dist_sd_to_send_pt = math.sqrt(dx**2 + dy**2)
                if dist_sd_to_send_pt + r <= R:
                    # signal all inside R, no intersect
                    # dist_sd_sent_pt is always <=R,
                    # b/c we're never going to draw the signal ring for a device outside of sd's range

                    pygame.draw.circle(
                        self.surface,
                        faded_color(
                            color,
                            SELECTED_DEVICE_COLOR[1],
                            f=f),
                        (_x, _y), _r,
                        SIGNAL_RING_THICKNESS)

                else: # there is an intersect

                    theta1 = -np.arctan2(dy, dx)
                    theta2 = np.pi - np.arccos((r**2 + dist_sd_to_send_pt**2 - R**2) / (2*r*dist_sd_to_send_pt))
                    a1 = theta1 + theta2
                    a2 = theta1 - theta2
                    rect = [_x - _r, _y - _r, 2*_r, 2*_r]

                    pygame.draw.arc(
                        self.surface,
                        faded_color(
                            color,
                            SELECTED_DEVICE_COLOR[1],
                            f=f),
                        rect,
                        a1, a2,
                        SIGNAL_RING_THICKNESS)
                    pygame.draw.arc(
                        self.surface,
                        faded_color(
                            color,
                            BACKGROUND_COLOR[1],
                            f=f),
                        rect,
                        a2, a1,
                        SIGNAL_RING_THICKNESS)

        else:
            r = int(SCREEN_SCALE * signal['dist_traveled'])
            if r > SIGNAL_RING_THICKNESS:
                x = int(SCREEN_SCALE * signal['send_pt'][0])
                y = int(SCREEN_SCALE * signal['send_pt'][1])
                color = pygame.Color(color)
                pygame.draw.circle(
                    self.surface,
                    color,
                    (x, y), r,
                    SIGNAL_RING_THICKNESS) # (x,y), radius


class Model(object):

    def __init__(self):

        # create devices, connections and edges
        # devices: [Device(), Device(), ...]
        # connections: {keys=devices : value={key=neighbor_device, value=distance}}
        # edges: [{device0, device1}, {device2, device0}, ...]
        self.devices = self.init_moving_devices(verbose=False)
        self.connections, self.edges, self.sub_networks = None, None, None

        # list of signals that are being broadcast. Used to simulate signal time delay in simulation
        # format: [{'sender_device':<Device>, 'dist_traveled':<float>, 'send_pt':<(float, float)>, 'message':<str>}, ...]
        self.signals = []

        t = time.time()
        self.t1 = t # t1 = time of previous time step (1 time step in the past)

        # controller variables
        self.selected_device = None  # device user clicked on
        self.pause_devices   = False # pause/play movement
        self.pause_signals   = False # pause/play signals


    # main_loop of the model
    def update(self, verbose=False):

        t = time.time()
        self.dt = t - self.t1
        # if verbose: print('%s\nt = %s' % ('-'*180, t))

        # update devices, connections, and edges, and sub-networks
        if not self.pause_devices:
            self.get_network_state(self.devices)

        # move message signals forward,
        # deliver message if it's reached a node,
        # remove it when its travelled R,
        # and run each devices'/nodes' main_loop
        if not self.pause_signals:
            signals_outside_range = []
            for signal in self.signals:

                # move message forward
                prev_signal_dist = signal['dist_traveled']
                signal['dist_traveled'] += (SIGNAL_SPEED * self.dt)
                if signal['dist_traveled'] > R: signal['dist_traveled'] = R

                # deliver message if it's reached a node
                sd, sp = signal['sender_device'], signal['send_pt']
                x, y = sp[0], sp[1]
                for d in self.devices:
                    if d != sd:

                        # if the signal just passed d, put the signal's message
                        # and the current time in device d's mailbox
                        dist_sp_to_d = math.sqrt((d.n.x - x)**2 + (d.n.y - y)**2)
                        if prev_signal_dist <= dist_sp_to_d <= signal['dist_traveled'] \
                        and d not in signal['receiver_devices']:
                            d.n.mailbox.append((signal['message'], t))
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
                sent_messages, updt_cnsl_dsply = \
                    d.main_loop(verbose=False)#d==self.selected_device)
                if d == self.selected_device and updt_cnsl_dsply:
                    update_console(caller='selected device perceived neighbor update')
                for message in sent_messages:

                    if message.m.startswith('PING'):   message_type = 'ping'
                    elif message.m.startswith('ECHO'): message_type = 'echo'
                    else:                              message_type = 'message'

                    self.signals.append({
                        'sender_device'    : d,
                        'dist_traveled'    : 0.00,
                        'send_pt'          : (d.n.x, d.n.y),
                        'message'          : message,
                        'message_type'     : message_type,
                        'receiver_devices' : set() # ensures that a signal doesn't pass a node twice
                    })

        # move the devices
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

        # update t1 at end of update()
        self.t1 = t

    # create devices that move around the map
    def init_moving_devices(self, verbose=False):

        ''' create devices,

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

    # determine which devices are currently within signal range of each other
    def get_network_state(self, devices, verbose=False):
        connections = {}  # {keys=devices : value={key=neighbor_device, value=distance}}
        edges = []        # [{device0, device1}, {device2, device0}, ...]
        sub_networks = [] # [{device0, device1, device2}, {device3, device4}, ...]

        # create connections and edges data structure,
        # also make deep copy of devices in unvisted_devices for creating sub_networks in the next iteration
        unvisited_devices = set()
        for d0 in devices:
            if not isinstance(d0, Device): continue
            neighbors = self.get_direct_neighbors(d0, devices)
            connections[d0] = neighbors
            for d in neighbors.keys():
                if {d0, d} not in edges:
                    edges.append({d0, d})
            unvisited_devices.add(d0)
        self.connections = connections
        self.edges = edges

        # find all sub_networks
        # useful source for set operations:
        # https://dev.to/svinci/intersection-union-and-difference-of-sets-in-python-4gkn
        while unvisited_devices != set():

            # pick a random device in list of unvisited devices
            d0 = unvisited_devices.pop()
            neighbors = set(connections[d0].keys())
            d0_and_neighbors = {d0} | neighbors

            # if any of d0 or it's neighbors are in a sub_net
            # put d0 and all its neighbors in that sub_net
            sub_nets_to_add_to = {}
            for i, sub_net in enumerate(sub_networks):
                intersect = sub_net & d0_and_neighbors
                if len(intersect) > 0:
                    sub_nets_to_add_to[i] = sub_net

            # if d0_and_neighbors intersected exactly 1 sub_net,
            # add them to that sub_net
            if len(sub_nets_to_add_to) == 1:
                i = list(sub_nets_to_add_to.keys())[0]
                sub_net = sub_nets_to_add_to[i]
                sub_networks[i] = sub_net | d0_and_neighbors # | = union

            # elif d0_and_neighbors intersected multiple sub_nets,
            # merge all the sub_nets together and add them to that
            elif len(sub_nets_to_add_to) > 1:
                merged_sub_net = set()
                for i, sub_net in sub_nets_to_add_to.items():
                    merged_sub_net = merged_sub_net | sub_net
                    sub_networks.remove(sub_net)
                merged_sub_net = merged_sub_net | d0_and_neighbors
                sub_networks.append(merged_sub_net)

            # else d0_and_neighbors didn't intersect any sub_nets,
            # so create a new sub_net for them
            else: # len(sub_nets_to_add_to) == 0:
                sub_networks.append(d0_and_neighbors)

        # update networks in console output if it changed
        sub_networks.sort()
        if sub_networks != self.sub_networks:
            self.sub_networks = sub_networks # this must be set before we call update_console
            update_console(caller='update sub-networks')
        else: self.sub_networks = sub_networks

        if verbose:

            print('\nNetwork State:')
            print('%d Devices in the network\n' % len(devices))

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

            num_sub_nets = len(sub_networks)
            print('\n%d Sub-Networks:' % len(sub_networks))
            sub_net_counts = list(map(lambda sub_net : len(sub_net), sub_networks))
            max_spaces1 = len(str(num_sub_nets))
            max_spaces2 = len(str(max(sub_net_counts)))
            for i, (num_devices, sub_net) in enumerate(zip(sub_net_counts, sub_networks)):
                i += 1
                sub_net_devices = set(map(lambda d : d.num, sub_net))
                num_spaces1 = max_spaces1 - len(str(i))
                num_spaces2 = max_spaces2 - len(str(num_devices))
                print('   sub_net %d %shas %d %sdevice%s:%s %s' % (
                    i,
                    ' '*num_spaces1,
                    num_devices,
                    ' '*num_spaces2,
                    '' if num_devices == 1 else 's', ' ' if num_devices == 1 else '', # plural or singular
                    sub_net_devices))
            print()

    # determine which devices are within signal range of device d0
    # {key=neighboring device : value=distance}
    def get_direct_neighbors(self, d0, devices, verbose=False):
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

                if   event.button == 4:
                    if verbose: print('mouse wheel scroll up')
                elif event.button == 5:
                    if verbose: print('mouse wheel scroll down')
                elif event.button == 1:
                    if verbose: print('mouse left click')
                    self.model.selected_device = self.select_or_deselect_device(mx, my, verbose=False)
                    update_console(caller='selected device')
                elif event.button == 3:
                    if verbose: print('mouse right click') # 2 finger click on Mac
                else:
                    if verbose: print('event.button = %d' % event.button)

        elif event.key == pygame.K_SPACE: # toggle pause/play of movement of devices
            if verbose: print('space bar')
            self.model.pause_devices = not self.model.pause_devices
            self.update_view_settings('space')

        elif event.key == pygame.K_s: # toggle pause/play of signals in actual simulation
            self.model.pause_signals = not self.model.pause_signals
            self.update_view_settings('s')

        elif event.key == pygame.K_d: self.update_view_settings('r') # toggle draw message dots
        elif event.key == pygame.K_r: self.update_view_settings('r') # toggle draw signal rings
        elif event.key == pygame.K_c: self.update_view_settings('c') # toggle draw connection lines
        elif event.key == pygame.K_f: self.update_view_settings('f') # toggle draw node flash from signal
        elif event.key == pygame.K_n: self.update_view_settings('n') # toggle draw device number

        elif event.key == pygame.K_RETURN:
            if verbose: print('self.buffer = %s' % self.buffer)

            if   self.buffer == 'p0': self.update_view_settings('p0') # toggle drawing pings of selected device
            elif self.buffer == 'p1': self.update_view_settings('p1') # toggle drawing pings of direct neighbors of selected device
            elif self.buffer == 'e0': self.update_view_settings('e0') # toggle drawing echos of selected device
            elif self.buffer == 'e1': self.update_view_settings('e1') # toggle drawing echos of direct neighbors of selected device
            elif self.buffer == 'm0': self.update_view_settings('m0') # toggle drawing messages of selected device
            elif self.buffer == 'm1': self.update_view_settings('m1') # toggle drawing messages of direct neighbors of selected device

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
    def update_view_settings(self, key, verbose=False):
        current_state = self.view.settings.loc[key]['STATE']
        self.view.settings.at[key, 'STATE'] = not current_state
        update_console(caller='update view state')
        if verbose: print('%s = %s' % (key, self.view.settings.loc[key]['STATE']))

    # click a device to select/deselect it
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

    # setup
    pygame.init()
    model = Model()
    view = View(model)
    controller = Controller(model, view)


    # frame rate variables
    start_time = time.time()
    iterations = 0

    while True:

        # output frame rate
        iterations += 1
        if time.time() - start_time > 1:
            start_time += 1
            fps = iterations
            update_console(caller='update frame rate')
            iterations = 0

        # handle user input
        for event in pygame.event.get():
            if event.type == QUIT: # Xing out of window
                pygame.quit()
                sys.exit()
            else:
                controller.handle_event(event, verbose=False)

        # update the model
        model.update(verbose=False)

        # display the view
        view.draw()
        view.screen.blit(view.surface, (0, 0))
        pygame.display.update()

        # time.sleep(1.0) # control frame rate (in seconds)
