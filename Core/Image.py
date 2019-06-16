import pygame
from Core.Core import sc

class Image(object):

    def __init__(self, file=None, image=None):
        if file is not None and image is None:
            self.path = "./Images/{}".format(file)
            self.image = pygame.image.load(self.path)
        elif file is None and image is not None:
            self.image = image
        self.angle = 0

    def show(self, pos):
        sc.screen.blit(self.image, (pos.x, pos.y))

    def toString(self):
        return pygame.image.tostring(self.image, "RGBA")

    def scale(self, newW, newH):
        self.image = pygame.transform.scale(self.image, (newW, newH))

    def rotate(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, self.angle)

    @staticmethod
    def fromString(string, size):
        return Image(image=pygame.image.fromstring(string, size, "RGBA"))
