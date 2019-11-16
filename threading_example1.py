
'''

    Description:

        Example of how to do basic threading

    Relation to this repo:
        
        we don't need to lock any of the data (aka the model) for this process though
        we just need to create
            a thread for the Model's main_loop
            a thread for the Controller's main_loop
            a thread for the Views main_loop
                the View thread can be split into:
                    a thread that updates the gui
                    a thread that updates the console output
                each of the view's threads will have a boolean
                    if the boolean is True  the thread will be stared and it will continually run the update function of the gui/console output
                    if the boolean is False the thread will be terminated

            each of these thread are 3 branches of threads branching off the root thread in a thread tree
                just start with these 3 branches and see how much faster the program runs
                    keep a version of just 1 thread to compare the new and old versions
                        keeping different versions will allow for comparing later stages in the tree as well

        the display variables would have to be in the model
            could they be kept in the View somehow?
                yes, and if the controller thread modifies the 


    Other things to Research:

        Google:
            python threading lock vs semaphore
            python threading mutex

        python multiprocessing - completely different library that could be better than (or use in tandem with) threading
        https://docs.python.org/3.4/library/multiprocessing.html?highlight=process


    Source:

        Where I originally got the example below
        https://realpython.com/intro-to-python-threading/

        format python logger lib to use milliseconds:
        https://stackoverflow.com/questions/31328300/python-logging-module-logging-timestamp-to-include-microsecond/31335874

        Threading Docs
        https://docs.python.org/3/library/threading.html

        Get thread id in logger
        https://javawithravi.com/how-to-display-thread-id-in-python-logs/

    '''

import logging
import threading
import time
# import datetime as dt

def thread_fn1(name):
    logging.info("Thread %s: starting", name)
    time.sleep(3)
    logging.info("Thread %s: finishing", name)

def thread_fn2(name):
    logging.info("Thread %s: starting", name)
    time.sleep(6)
    logging.info("Thread %s: finishing", name)


if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    # logging.basicConfig(
    #     format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
    #     level=logging.INFO,
    #     datefmt='%Y-%m-%d %H:%M:%S')

    # formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(threadName)s\tfunction[%(funcName)s]\t%(pathname)s:%(lineno)d\t%(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')



    t1 = threading.Thread(target=thread_fn1, args=('1',))

    logging.info("Main right before starting thread t1")
    t1.start()
    logging.info("Main right after  starting thread t1")

    t2 = threading.Thread(target=thread_fn2, args=('2',))
    t2.start()

    i = 0
    while t1.is_alive() or t2.is_alive():
        logging.info('hi %d' % i)
        i += 1
        time.sleep(1)

    logging.info("Main all done")

    