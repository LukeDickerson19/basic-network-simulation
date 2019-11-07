import pygame
import time
import copy
import sys
import math
from pygame.locals import QUIT, KEYDOWN
from constants import *
from node import Node
from message import Message
import numpy as np

''' NOTES:

    TO DO:

        i need a cellular automata that has
            nodes constantly joining and leaving the network
            networks constantly spliting and merging

            HOWEVER:
                when a node joins, it joins a network. It does not try to start its own network

                8 sournding squares
                if im 1:
                    if 7 or more of my neighboring squares is 1, i turn to 0
                    if 

                if im 0:


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


    def draw_nodes(self):
        for n in model.nodes:
            if not isinstance(n, Node): continue
            x = int(SCREEN_SCALE*n.x)
            y = int(SCREEN_SCALE*n.y)
            pygame.draw.circle(
                self.surface,
                pygame.Color('cyan'),
                (x, y), 5) # (x,y), radius

    def draw_in_range_connections(self):
        for (n1, n2) in model.connections:
            x1, y1 = int(SCREEN_SCALE*n1.x), int(SCREEN_SCALE*n1.y)
            x2, y2 = int(SCREEN_SCALE*n2.x), int(SCREEN_SCALE*n2.y)
            pygame.draw.line(
                self.surface,
                pygame.Color('blue'),
                (x1, y1), (x2, y2), 1)

    def draw_message_dot(self, d, color):
        sn, rn = d['sender_node'], d['receiver_node']
        mx = int(SCREEN_SCALE * ((d['dist_traveled'] / d['dist_to_travel'])*(rn.x - sn.x) + sn.x))
        my = int(SCREEN_SCALE * ((d['dist_traveled'] / d['dist_to_travel'])*(rn.y - sn.y) + sn.y))
        pygame.draw.circle(
            self.surface,
            pygame.Color(color),
            (mx, my), 2) # (x,y), radius

    def draw_message_circle(self, d, color, fade=True):
        sn = d['sender_node']
        r = d['dist_traveled']
        if fade:
            non_zero_rgb_value = int(255 * ((float(R - r) / R)**10 if r < R else 0.0))
            if color == 'darkgreen': color = (0, non_zero_rgb_value, 0)
            if color == 'cyan':      color = (0, 0, non_zero_rgb_value)
            if color == 'darkred':   color = (non_zero_rgb_value, 0, 0)
        else:
            color = pygame.Color(color)
        r = int(SCREEN_SCALE * r)
        if r > 1:
            x = int(SCREEN_SCALE * sn.x)
            y = int(SCREEN_SCALE * sn.y)
            pygame.draw.circle(
                self.surface,
                color,
                (x, y), r, 1) # (x,y), radius

    def draw_pings(self):
        for d in self.model.mid_delivery_messages:
            if d['sender_node'] == model.nodes[0]: # just draw 1 node's ping right now
                if d['message'].m.startswith('PING'):
                    self.draw_message_circle(d, 'darkgreen', fade=True)
                    self.draw_message_dot(d, 'green')

    def draw_echos(self):
        for d in self.model.mid_delivery_messages:
            if d['receiver_node'] == model.nodes[0]: # just draw 1 node's echo right now
                if d['message'].m.startswith('ECHO'):
                    self.draw_message_circle(d, 'darkred', fade=True)
                    self.draw_message_dot(d, 'red')

    def draw_messages(self):
        for d in self.model.mid_delivery_messages:
            if not d['message'].m.startswith('PING') \
            and not d['message'].m.startswith('ECHO'):
                self.draw_message_circle(d, 'cyan', fade=True)
                self.draw_message_dot(d, 'cyan')

    def draw(self):

        # fill background
        self.surface.fill(pygame.Color('black'))

        self.draw_in_range_connections()
        self.draw_pings()
        self.draw_echos()
        # self.draw_messages()
        self.draw_nodes()

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


class Model(object):
    '''
        Model represents the state of all entities in
        the environment and drawing parameters

    '''

    def __init__(self):
        '''
            initialize model, environment, and default keyboard controller states
        Args:
            width (int): width of window in pixels
            height (int): height of window in pixels
        '''

        # create network
        # self.nodes, self.connections = self.create_network0(verbose=True)
        # self.nodes, self.connections = self.create_network1(verbose=True)
        self.nodes, self.connections = self.create_grid_network(verbose=True)

        # list of messages that are being delivered. Used just for time delay in simulation
        # format: [(receiver_node, delivery_time, message), ...]
        self.mid_delivery_messages = []

        t = time.time()
        self.t1 = t # t1 = time of previous time step (1 time step in the past)
        self.t2 = t # t2 = time of previous cellular

        # window parameters / drawing
        self.show = True # show current model



    # this function updates the model
    def update(self, controller):

        # move message signals forward,
        # deliver message if it's reached the receiver_node,
        # else keep it in the mid_delivery_messages list
        t = time.time()
        new_mid_delivery_messages = []
        for d in self.mid_delivery_messages:
            d['dist_traveled'] += (SIGNAL_SPEED * (t - self.t1))
            if d['dist_traveled'] >= d['dist_to_travel']:
                rn = d['receiver_node']
                m  = d['message']
                rn.messages.append(m)
            else:
                new_mid_delivery_messages.append(d)
        self.mid_delivery_messages = new_mid_delivery_messages

        # run the main loop of each node
        for i, n in enumerate(self.nodes):

            if not isinstance(n, Node): continue

            # every node send out a ping signal and
            # respond to any messages it has received
            n.nprint(i=i+1, newline=True)
            ping, messages_to_send = n.main_loop()
            if ping != None:
                self.add_message_to_mid_delivery_messages(ping, n)
            for m in messages_to_send:
                self.add_message_to_mid_delivery_messages(m, n)

        # update the Nodes in the network every AUTOMATA_PERIOD
        if (t - self.t2) > AUTOMATA_PERIOD:
            self.evolve_grid()
            self.t2 = t

        self.t1 = t # update t1 at end of update()

        #     input()

        # sys.exit()


    def fully_connected_network(self):
        for n in self.nodes:
            neighbors = self.get_direct_neighbors(n)
            if len(neighbors.keys()) == 0:
                return False
        return True

    def get_connections(self, nodes):
        connections = []
        for n0 in nodes:
            if isinstance(n0, Node):
                n1s = self.get_direct_neighbors(n0, nodes)
                for n1 in n1s:
                    if (n0, n1) not in connections \
                    and (n1, n0) not in connections:
                        connections.append((n0, n1))
        return connections

    def get_direct_neighbors(self, n0, nodes, verbose=False):
        neighbors = {} # key = neighboring node, value = range
        for n in nodes:
            if isinstance(n, Node) and n != n0:
                dist = math.sqrt((n.x - n0.x)**2 + (n.y - n0.y)**2)
                if dist <= R:
                    neighbors[n] = dist
        if verbose:
            print('%d Direct Neighbors:' % len(neighbors.keys()))
            for neighbor in neighbors.keys(): neighbor.nprint(newline=False)
        return neighbors

    # return a list of node networks
    def get_networks(self, nodes, verbose=False):

        def get_network_recurrsively(n0, network):
            network += [n0]
            for n in self.get_direct_neighbors(n0, unvisited_nodes):
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
                    n.nprint()

        return networks

    # network 0: N nodes constantly throughout all time steps for the entire simulation
    def create_network0(self, verbose=False):
        nodes = [Node() for _ in range(N)]
        connections = self.get_connections(nodes)
        networks = self.get_networks(nodes, verbose=verbose)
        return nodes, connections
    # def create_network0(self, verbose=False):
    #     self.nodes = [Node()]
    #     while len(self.nodes) < N:
    #         n = Node()
    #         self.nodes.append(n)
    #         if len(self.get_direct_neighbors(n).keys()) == 0:
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

    # network 1: N nodes come in and out randomly over the time steps of the simulation
    def create_network1(self, verbose=False):
        pass

    # cellular automata
    def create_grid_network(self, verbose=False):
        # create grid with one node at the center
        # nodes = np.array([[Node(x, y) for x in range(W)] for y in range(H)]).flatten().tolist()
        nodes = []
        for x in range(W):
            grid_col = []
            for y in range(H):
                grid_col.append(
                    Node(x, y) if x == W / 2 and y == H / 2 else str(x)+','+str(y))
            nodes += grid_col
        connections = self.get_connections(nodes)
        networks = self.get_networks(nodes, verbose=verbose)
        return nodes, connections
    def evolve_cell(self, x0, y0, nodes):

        # get grid neighbors state
        neighbours = []
        for x in range(x0-1, x0+1):
            for y in range(y0-1, y0+1):
                if X_MIN <= x <= X_MAX and Y_MIN <= y <= Y_MAX:
                    if x == x0 and y == y0:
                        cell0 = nodes[x*H+y]
                    else:
                        neighbours.append(nodes[x*H+y])

        # count node neighbours
        nn = 0
        for n in neighbours:
            if n != None:
                nn += 1

        # conways game of life
        if isinstance(cell0, Node):
            if nn < 2:
                return None
            elif 1 < nn < 4:
                return cell0
            elif 3 < nn:
                return None
        else: # cell0 == None
            if nn == 3:
                return Node(x0, y0)
            else:
                return None
    def evolve_grid(self, verbose=False):
        for x in range(W):
            for y in range(H):
                self.nodes[x*H+y] = self.evolve_cell(x, y, self.nodes)

    def add_message_to_mid_delivery_messages(self, message, n0):
        neighbors = self.get_direct_neighbors(n0, self.nodes, verbose=True)
        for neighbor, dist in neighbors.items():
            self.mid_delivery_messages.append({
                'sender_node'    : n0,
                'receiver_node'  : neighbor,
                'dist_traveled'  : 0.00,
                'dist_to_travel' : math.sqrt((n0.x - neighbor.x)**2 + (n0.y - neighbor.y)**2),
                'message'        : message
            })


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
