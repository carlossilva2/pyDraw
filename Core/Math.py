from math import sqrt, pow, pi
from numpy import arange
from random import shuffle, uniform
from copy import deepcopy
from decimal import Decimal, DecimalException, getcontext
from Core.Vector import Vector2


def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)


def isPrime(n):
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True


def dist(a, b, c, d):
    return sqrt(pow(a - c, 2) + pow(b - d, 2))


def fibonacci(n):
    if n < 2:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def mapping(x, in_min, in_max, out_min, out_max):
    "Map values"
    if type(x) == int:
        return int((x - in_min) / (in_max - in_min) * (out_max - out_min) + out_min)
    elif type(x) == float:
        return float((x - in_min) / (in_max - in_min) * (out_max - out_min) + out_min)


class Noise:
    tiledim = len(arange(-pi / 2, pi / 2, 0.1))
    p = []

    def __init__(self):
        for _ in range(2*self.tiledim):
            self.p.append(0)

        self.permutation = []
        for value in range(self.tiledim):
            self.permutation.append(value)
        shuffle(self.permutation)

        for i in range(self.tiledim):
            self.p[i] = self.permutation[i]
            self.p[self.tiledim+i] = self.p[i]

    def fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def lerp(self, t, a, b):
        return a + t * (b - a)

    def grad(self, hash, x, y, z):
        h = hash & 15
        if h < 8:
            u = x
        else:
            u = y

        if h < 4:
            v = y
        else:
            if h == 12 or h == 14:
                v = x
            else:
                v = z
        if h & 1 == 0:
            first = u
        else:
            first = -u

        if h & 2 == 0:
            second = v
        else:
            second = -v

        return first + second

    def noise(self, x, y=0.0, z=0.0):
        X = int(x) & (self.tiledim-1)
        Y = int(y) & (self.tiledim-1)
        Z = int(z) & (self.tiledim-1)

        x -= int(x)
        y -= int(y)
        z -= int(z)

        u = self.fade(x)
        v = self.fade(y)
        w = self.fade(z)

        A = self.p[X]+Y
        AA = self.p[A]+Z
        AB = self.p[A+1]+Z
        B = self.p[X+1]+Y
        BA = self.p[B]+Z
        BB = self.p[B+1]+Z

        return self.lerp(w, self.lerp(v, self.lerp(u, self.grad(self.p[AA], x, y, z), self.grad(self.p[BA], x-1, y, z)), self.lerp(u, self.grad(self.p[AB], x, y-1, z), self.grad(self.p[BB], x-1, y-1, z))), self.lerp(v, self.lerp(u, self.grad(self.p[AA+1], x, y, z-1), self.grad(self.p[BA+1], x-1, y, z-1)), self.lerp(u, self.grad(self.p[AB+1], x, y-1, z-1), self.grad(self.p[BB+1], x-1, y-1, z-1))))


class Matrix:
    rows = 0
    cols = 0
    size = ""
    arr = []

    def __init__(self, rows=None, cols=None):
        if rows != None or cols != None:
            self.rows = rows
            self.cols = cols
            self.size = "{}x{}".format(cols, rows,)
            for i in range(rows):
                self.arr.append([])
                for _ in range(cols):
                    self.arr[i].append([])
        else:
            print("Uninitialized Matrix")

    @property
    def get(self):
        return self.arr

    def clean(self):
        if len(self.arr) > self.rows:
            difference = int(len(self.arr) - self.rows)
            for _ in range(difference):
                self.arr.pop(-1)

        for i in range(len(self.arr)):
            if len(self.arr[i]) > self.cols:
                diff = (len(self.arr[i]) - self.cols)
                for _ in range(diff):
                    self.arr[i].pop(-1)

    @property
    def getSize(self):
        return [self.cols, self.rows]

    @property
    def getValue(self, x, y):
        return self.arr[y][x]

    def setValue(self, x, y, val):
        if type(val) == int:
            self.arr[y][x] = val

    def setMatrix(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.size = "{}x{}".format(cols, rows,)
        for i in range(rows):
            self.arr.append([])
            for _ in range(cols):
                self.arr[i].append([])

    def print(self):
        for y in range(self.rows):
            for x in range(self.cols):
                print(self.arr[y][x], end=" ")
            print("")

    @staticmethod
    def fromArray(data):
        temp = Matrix(len(data), 1)
        for y in range(temp.rows):
            for x in range(temp.cols):
                temp.setValue(x, y, data[y])
        return temp

    @staticmethod
    def subtract(a, b):
        if a.rows != b.rows or a.cols != b.cols:
            print("Columns and rows of A must match Columns and Rows of B.")
            return
        temp = Matrix(a.rows, b.cols)
        for y in range(temp.rows):
            for x in range(temp.cols):
                temp.setValue(x, y, a[x][y]-b[x][y])
        return temp

    def toArray(self):
        temp = []
        for y in range(self.rows):
            for x in range(self.cols):
                temp.append(self.arr[y][x])
        return temp

    def randomize(self):
        for y in range(self.rows):
            for x in range(self.cols):
                self.arr[y][x] = uniform(0, 1)

    def add(self, n):
        if isinstance(n, Matrix):
            if n.rows != self.rows or n.cols != self.cols:
                print("Columns and rows of A must match Columns and Rows of B.")
                return
            for y in range(self.rows):
                for x in range(self.cols):
                    self.arr[y][x] += n.arr[y][x]
            return self
        else:
            for y in range(self.rows):
                for x in range(self.cols):
                    self.arr[y][x] += n
            return self

    @staticmethod
    def transpose(matrix):
        temp = Matrix(matrix.cols, matrix.rows)
        for y in range(temp.rows):
            for x in range(temp.cols):
                temp.setValue(x, y, matrix.arr[x][y])
        return temp

    @staticmethod
    def multiply(a, b):
        a = a.copy()
        b = b.copy()
        if a.cols != b.rows:
            print("Columns and rows of A must match Columns and Rows of B.")
            return
        temp = Matrix(a.rows, b.cols)
        for y in range(temp.rows):
            for x in range(temp.cols):
                sumz = 0
                for k in range(a.cols):
                    sumz += (a.getValue(k, y) * b.getValue(x, k))
                temp.setValue(x, y, sumz)
        return temp

    def copy(self):
        return deepcopy(self)


class Mathcontext:

    def __init__(self, context):
        self.context = context
        getcontext().prec = self.context

    def get(self):
        return self.context

    def set_rounding(self, method):
        getcontext().rounding = method


class BigDecimal:

    def __init__(self, value):
        self.init_value = value
        self.value = Decimal(value)

    def __repr__(self):
        return str(self.value)

    def divide(self, value):
        self.value = self.value / value
        return self.value

    def add(self, value):
        self.value = self.value + value
        return self.value

    def subtract(self, value):
        self.value = self.value - value
        return self.value

    def multiply(self, value):
        self.value = self.value * value
        return self.value

    def print(self):
        print(self.value)


class Quadratic:

    def __init__(self, equation):
        self.equation = equation
        self.parts = self.equation.split(" ")
        self.a = 0
        self.b = 0
        self.c = 0
        for part in self.parts:
            if "x2" in part:
                if len(part) == 2:
                    self.a = 1
                elif len(part) == 3 and part[0] == "-":
                    self.a = -1
                else:
                    self.a = int(part[:-2])
            elif "x" in part:
                if len(part) == 2:
                    if part[0] == "+":
                        self.b = 1
                    elif part[0] == "-":
                        self.b = -1
                else:
                    self.b = int(part[:-1])
            elif "x" not in part and "x2" not in part:
                self.c = int(part)

    def __repr__(self):
        add = self.equation.replace(" ", "").replace("x2", "x²")
        return str(add)

    def get_zeros(self):
        bsqrd = pow(self.b, 2)
        part2 = 4 * self.a * self.c
        part1 = self.b * -1
        part3 = 2 * self.a
        part4 = bsqrd - part2
        pos_part = 0
        neg_part = 0
        if part4 < 0:
            return None
        elif part4 == 0:
            pos_part = ((part1 + sqrt(part4)) / part3)
            return [Vector2(pos_part, 0)]
        else:
            pos_part = ((part1 + sqrt(part4)) / part3)
            neg_part = ((part1 - sqrt(part4)) / part3)
            return [Vector2(neg_part, 0), Vector2(pos_part, 0)]

    def get_y(self, x):
        a = self.a * x**2
        b = self.b * x
        result = a + b + self.c
        return result
