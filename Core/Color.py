import json
from logging import getLogger
from pygame import Color as pyCol

logger = getLogger(__name__)

class Color:
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (128, 128, 128)
    PINK = (255, 0, 255)
    AQUA = (0, 255, 255)
    YELLOW = (255, 255, 0)
    ORANGE = (200, 100, 50)

    __colors = {
        "red": RED,
        "green": GREEN,
        "blue": BLUE,
        "white": WHITE,
        "black": BLACK,
        "grey": GREY,
        "pink": PINK,
        "aqua": AQUA,
        "yellow": YELLOW,
        "orange": ORANGE
    }

    def __init__(self, color=None):
        if color is not None and "#" not in color and color.lower() not in self.__colors:
            raise AttributeError("Color not found")
        self.tup = False
        if color is not None:
            if "#" not in color:
                self.selected = self.__colors[color.lower()]
                self.tup = True
            else:
                self.hexa = color.upper()
                hexar = str(color).replace("#", "").upper()
                if len(hexar) == 3:
                    r = int(str(hexar[0])+str(hexar[0]), 16)
                    g = int(str(hexar[1])+str(hexar[1]), 16)
                    b = int(str(hexar[2])+str(hexar[2]), 16)
                else:
                    r = int(hexar[0:2], 16)
                    g = int(hexar[2:4], 16)
                    b = int(hexar[4:6], 16)
                self.code = (r, g, b)

    def get(self):
        if self.tup:
            return self.selected
        else:
            return self.code

    def __repr__(self):
        if self.tup:
            return str(self.selected)
        else:
            return str(self.hexa)

    @staticmethod
    def fromHex(code):
        hexar = str(code).replace("#", "").upper()
        if len(hexar) == 3:
            r = int(str(hexar[0])+str(hexar[0]), 16)
            g = int(str(hexar[1])+str(hexar[1]), 16)
            b = int(str(hexar[2])+str(hexar[2]), 16)
        else:
            r = int(hexar[0:2], 16)
            g = int(hexar[2:4], 16)
            b = int(hexar[4:6], 16)
        return (r, g, b)

    @staticmethod
    def fromDecimal(code):
        if type(code) != tuple:
            raise TypeError("Code must be a tuple")
        r = str(hex(code[0])).replace("0x", "")
        g = str(hex(code[1])).replace("0x", "")
        b = str(hex(code[2])).replace("0x", "")
        if r == "0":
            r = "00"
        if g == "0":
            g = "00"
        if b == "0":
            b = "00"
        hexar = "#{}{}{}".format(r, g, b).upper()
        return hexar

    def loadCustomColors(self):
        try:
            data = json.load(open(r"./Lib/custom_colors.json", "r"))
            for key in data.keys():
                r = int(data[key]["r"])
                g = int(data[key]["g"])
                b = int(data[key]["b"])
                self._colors[key] = (r, g, b)
        except FileNotFoundError as err:
            logger.error(err)

    def getColor(self, color):
        if color is not None and "#" not in color and color.lower() not in self.__colors:
            raise AttributeError("Color not found")
        self.selected = self.__colors[color.lower()]
        self.tup = True
        return self.selected
    
    @staticmethod
    def from_hsla(h):
        """
        Convert HSLA Color Mode to RGB
        """
        color = pyCol(0)
        color.hsla = h, 100, 50, 1
        return color
