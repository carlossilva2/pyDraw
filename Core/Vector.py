from math import sqrt, cos, sin, pi
from copy import deepcopy


#@dataclass
class Vector2:

    def __init__(self,x,y, override=False):
        self.x = x
        self.y = y
        self.override = override

    type = "Vector2"

    def __repr__(self):
        return str("({},{})".format(self.x, self.y))

    def add(self, vect):
        if not isinstance(vect, Vector2):
            raise TypeError("Argument must be Vector2")
        self.x += vect.x
        self.y += vect.y

    def subtract(self, vect):
        if not isinstance(vect, Vector2):
            raise TypeError("Argument must be Vector2")
        self.x -= vect.x
        self.y -= vect.y

    def multiply(self, vect):
        if not isinstance(vect, Vector2):
            raise TypeError("Argument must be Vector2")
        self.x *= vect.x
        self.y *= vect.y

    def multiply_scalar(self, scalar):
        self.x *= scalar
        self.y *= scalar

    def normalize(self):
        sqrdlength = self.length_squared
        if sqrdlength > 0:
            length = self.length
            self.x /= length
            self.y /= length
        del sqrdlength

    def dot(self, vect):
        rx = self.x * vect.x
        ry = self.y * vect.y
        return rx + ry

    def magnitude(self):
        sqrdlength = self.x * self.x + self.y * self.y
        return sqrt(sqrdlength)

    def copy(self):
        return deepcopy(Vector2(self.x, self.y))

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def length_squared(self):
        return self.x ** 2 + self.y ** 2

    def rotate(self, angle):
        radian = float(((360-angle)*pi) / 180)
        cs = cos(radian)
        sn = sin(radian)
        newX = int(cs * self.x - sn * self.y)
        newY = int(sn * self.x + cs * self.y)
        self.x = newX
        self.y = newY
        del cs
        del sn
        del radian
        del newX
        del newY

    def setMag(self, mag):
        self.mag = self.magnitude()
        self.x = self.x * mag / self.mag
        self.y = self.y * mag / self.mag

    @staticmethod
    def fromAngle(angle):
        return Vector2(cos(angle), sin(angle))

    @staticmethod
    def distance(vec1, vec2):
        if not isinstance(vec1, Vector2) or not isinstance(vec2, Vector2):
            raise TypeError("Argument must be Vector2")
        part1 = (vec2.x - vec1.x) ** 2
        part2 = (vec2.y - vec1.y) ** 2
        part3 = part1 + part2
        return sqrt(part3)

    def __add__(self, other):
        if not isinstance(other, Vector2):
            raise TypeError
        return Vector2(self.x + other.x, self.y + other.y) if not self.override else self.add(other)

    def __sub__(self, other):
        if not isinstance(other, Vector2):
            raise TypeError
        return Vector2(self.x - other.x, self.y - other.y) if not self.override else self.add(other)

#@dataclass
class Vector3:
    x: int
    y: int
    z: int

    type = "Vector3"

    def add(self, vect):
        if vect.type != self.type:
            raise TypeError("Argument must be Vector3")
        self.x += vect.x
        self.y += vect.y
        self.z += vect.z

    def sub(self, vect):
        if vect.type != self.type:
            raise TypeError("Argument must be Vector3")
        self.x -= vect.x
        self.y -= vect.y
        self.z -= vect.z

    def mult(self, vect):
        if vect.type != self.type:
            raise TypeError("Argument must be Vector3")
        self.x *= vect.x
        self.y *= vect.y
        self.z *= vect.z

    def print(self):
        print("({},{},{})".format(self.x, self.y, self.z))
