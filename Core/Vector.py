from math import sqrt, cos, sin, pi, atan2, acos
from copy import deepcopy

def wtf(x, in_min, in_max, out_min, out_max):
    "Map values"
    if type(x) == int:
        return int((x - in_min) / (in_max - in_min) * (out_max - out_min) + out_min)
    elif type(x) == float:
        return float((x - in_min) / (in_max - in_min) * (out_max - out_min) + out_min)

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
        sqrdlength = self.length_squared()
        if sqrdlength > 0:
            length = self.length()
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
        return self
    
    def angleBetween(self,vect):
        if not isinstance(vect,Vector2):
            raise TypeError("Argument must be Vector2")
        dotmag = self.dot(vect) / (self.magnitude() * vect.magnitude())
        angle = acos(wtf(dotmag,-1,1,-1,1))
        return angle

    def setMag(self, mag):
        self.mag = self.magnitude()
        self.x = self.x * mag / self.mag
        self.y = self.y * mag / self.mag
    
    def heading(self):
        return atan2(self.y, self.x)

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

class Vector3:

    def __init__(self,x,y,z, override=False):
        self.x = x
        self.y = y
        self.z = z
        self.override = override
        raise NotImplementedError("Still under development")

    type = "Vector3"

    def __repr__(self):
        return str("({},{},{})".format(self.x, self.y,self.z))

    def add(self, vect):
        if not isinstance(vect, Vector3):
            raise TypeError("Argument must be Vector3")
        self.x += vect.x
        self.y += vect.y
        self.z += vect.z

    def subtract(self, vect):
        if not isinstance(vect, Vector3):
            raise TypeError("Argument must be Vector3")
        self.x -= vect.x
        self.y -= vect.y
        self.z -= vect.z

    def multiply(self, vect):
        if not isinstance(vect, Vector3):
            raise TypeError("Argument must be Vector3")
        self.x *= vect.x
        self.y *= vect.y
        self.z *= vect.z

    def multiply_scalar(self, scalar):
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar

    def normalize(self):
        sqrdlength = self.length_squared()
        if sqrdlength > 0:
            length = self.length
            self.x /= length
            self.y /= length
            self.z /= length
        del sqrdlength

    def dot(self, vect):
        rx = self.x * vect.x
        ry = self.y * vect.y
        rz = self.z * vect.z
        return rx + ry + rz

    def magnitude(self):
        sqrdlength = self.x * self.x + self.y * self.y + self.z * self.z
        return sqrt(sqrdlength)

    def copy(self):
        return deepcopy(Vector3(self.x, self.y, self.z, self.override))

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def length_squared(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

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
        self.z = self.z * mag / self.mag

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
