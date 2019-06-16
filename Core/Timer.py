from threading import Thread
from logging import getLogger
from time import time
from math import floor

logger = getLogger(__name__)

class Timer(Thread):
    """Create a timed event:\n
        `function` - is the callback which the timer runs (Either Lambda or defined methods)
        `timeout` - is expressed in seconds and represents the time interval"""

    exec = True

    def __init__(self, function, timeout, args=None):
        if not callable(function):
            logger.error("Parameter must be a function")
            exit(1)
        if args is not None:
            self.args = args
        self.function = function
        self.timeout = timeout
        Thread.__init__(self)
        Thread.setName(self, "Background Thread - {}".format(self.function))
        logger.info("Timer Created with time interval of: {}".format(timeout))
        self.start_time = time()
        self.current_time = self.start_time
        Thread.start(self)

    def run(self):
        while self.exec:
            try:
                current = time()
                if floor(current - self.current_time) >= self.timeout:
                    self.function()
                    self.current_time = current
            except TimeoutError:
                self.exec = False

    def dispose(self):
        self.exec = False
        Thread.join(self)
        del self

    def change_timeout(self, timeout):
        self.timeout = timeout
        self.current_time = time()

    def running_time(self):
        if self.exec:
            return floor(time() - self.start_time)
        else:
            return floor(self.current_time - self.start_time)
