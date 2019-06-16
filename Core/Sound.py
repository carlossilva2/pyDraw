import pygame
from logging import getLogger
from threading import Thread

logger = getLogger(__name__)

class Sound(Thread):

    exec = True
    soun = False

    def __init__(self, name):
        Thread.__init__(self)
        self.path = "./Sounds/{}".format(name)
        pygame.mixer.init()
        pygame.mixer.music.load(self.path)
        self.vol = 0
        self.volume(100)
        self.playing = False
        Thread.start(self)

    def run(self):
        while self.exec:
            self.playing = pygame.mixer.music.get_busy()
            if self.soun:
                try:
                    pygame.mixer.music.load(self.path)
                    pygame.mixer.music.play()
                    self.soun = False
                except Exception as err:
                    logger.error(err)

    def play(self):
        self.soun = True

    def stop(self):
        pygame.mixer.music.stop()

    def dispose(self):
        self.exec = False
        self.soun = False
        Thread.join(self)

    def load(self, name):
        self.path = "./Sounds/{}".format(name)
        pygame.mixer.music.load(self.path)

    def volume(self, value):
        if type(value) != int or (value < 0 or value > 100):
            raise ValueError("value must be an integer and between 0 and 100")
        pygame.mixer.music.set_volume(int(value))
        self.vol = value
