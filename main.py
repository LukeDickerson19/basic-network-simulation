import pygame
import time
import math
from pygame.locals import QUIT, KEYDOWN
from constants import *
from node import Node
from message import Message



''' NOTES:

    TO DO:

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
        
    def draw(self):

        # fill background
        self.surface.fill(pygame.Color('black'))

        # draw nodes
        for n in model.nodes:
            x = int(SCREEN_SCALE*n.x)
            y = int(SCREEN_SCALE*n.y)
            pygame.draw.circle(
                self.surface,
                pygame.Color('blue'),
                (x, y), 5) # (x,y), radius


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

        # list of messages that are being delivered # used just for time delay in simulation
        # sorted by delivery_time. [(receiver_node, delivery_time, p), ...]
        self.mid_delivery_messages = []

        # create network
        self.nodes = self.create_network0(verbose=True)
        # self.nodes = self.create_network1()


        #window parameters / drawing
        self.show = True # show current model

    def fully_connected_network(self):
        for n in self.nodes:
            neighbors = self.find_neighbors_in_range(n)
            if len(neighbors.keys()) == 0:
                return False
        return True

    # network 0: N nodes constantly throughout all time steps for the entire simulation
    def create_network0(self, verbose=False):
        self.nodes = [Node()]
        while len(self.nodes) < N:
            n = Node()
            self.nodes.append(n)
            if len(self.find_neighbors_in_range(n).keys()) == 0:
                self.nodes.remove(n)
        return self.nodes
    # def create_network0(self, verbose=False):
    #     self.nodes = [Node() for _ in range(N)]
    #     while not self.fully_connected_network():
    #         print('Fail')
    #         self.nodes = [Node() for _ in range(N)]
    #     if verbose:
    #         print('Created network0 of %d nodes' % N)
    #     return self.nodes

    # network 1: N nodes come in and out randomly over the time steps of the simulation
    def create_network1(self):
        pass

    def find_neighbors_in_range(self, n0, verbose=False):
        neighbors = {} # key = neighboring node, value = range
        for n in self.nodes:
            if n != n0:
                dist = math.sqrt((n.x - n0.x)**2 + (n.y - n0.y)**2)
                if dist <= R:
                    neighbors[n] = dist
        if verbose:
            print('%d Direct Neighbors:' % len(neighbors.keys()))
            for neighbor in neighbors.keys(): neighbor.nprint(newline=False)
        return neighbors

    def travel_time(self, dist):
        return float(dist) / SIGNAL_SPEED

    def add_message_to_mid_delivery_messages(self, ping, n0):
        neighbors = self.find_neighbors_in_range(n0, verbose=True)
        for neighbor, dist in neighbors.items():
            self.mid_delivery_messages.append({
                'receiver_node' : neighbor,
                'delivery_time' : time.time() + self.travel_time(dist),
                'message'       : ping
            })


    # this function updates the model
    def update(self, controller):

        # model, deliver any messages that need to be delivered
        t = time.time()
        for d in self.mid_delivery_messages:
            dt = d['delivery_time']
            if dt < t:
                rn = d['receiver_node']
                m  = d['message']
                rn.messages.append(m)

        for i, n in enumerate(self.nodes):
    
            # every node send out a ping signal and
            # respond to any messages it has
            n.nprint(i=i+1, newline=True)
            p, es = n.main_loop()
            self.add_message_to_mid_delivery_messages(p, n)
            for echo in es:
                self.add_message_to_mid_delivery_messages(e, n)

        #     input()

        # sys.exit()


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
