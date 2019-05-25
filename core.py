"""
MIT License

Copyright (c) 2019 Carlos Silva

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pygame
from time import sleep,strftime,time
from dataclasses import dataclass
from math import sqrt,pow,e,pi,cos,sin,floor
import colored_traceback.always
from random import uniform, randint, shuffle, random
from numpy import arange
from os import listdir, mkdir, cpu_count
from threading import Thread, active_count
import threading
from logging import getLogger
from copy import deepcopy,copy
from xlsxwriter import Workbook
from decimal import Decimal, DecimalException, getcontext
from pyautogui import size
from tkinter import Tk, Scale, Frame, HORIZONTAL
import json

logger = getLogger(__name__)

START_TIME = time()
clock = pygame.time.Clock()

KEYS = {
  "a": 97,
  "b": 98,
  "c": 99,
  "d": 100,
  "e": 101,
  "f": 102,
  "g": 103,
  "h": 104,
  "i": 105,
  "j": 106,
  "k": 107,
  "l": 108,
  "m": 109,
  "n": 110,
  "o": 111,
  "p": 112,
  "q": 113,
  "r": 114,
  "s": 115,
  "t": 116,
  "u": 117,
  "v": 118,
  "w": 119,
  "x": 120,
  "y": 121,
  "z": 122
}

def keyPressed(char):
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN and event.key == KEYS[str(char).lower()]:
      return True
    else:
      return False

class stuff:
  screen = None
  width = 0
  height = 0

@dataclass
class Offset:
  x: int or float
  y: int or float

  def set(self, x, y):
    self.x = int(x)
    self.y = int(y)

offset = Offset(0,0)
sc = stuff()
PI = pi
TWO_PI = 2 * pi
CPUS = cpu_count()

def running_time():
  return round(time()-START_TIME,2)

def getFPS():
  return round(clock.get_fps())

def forceUpdate():
  pygame.display.update()

def getScreenInfo():
  return [size().width,size().height]

def translate(x, y):
  offset.set(x,y)

def setScreen(screen,w, h):
  sc.screen = screen
  sc.width = w
  sc.height = h

class ThreadManager:

  def __init__(self):
    self.active_threads = []
    self.length = len(self.active_threads)
    self.finished_threads = []

  def get(self):
    return self.active_threads, self.finished_threads
  
  def dispose_all(self):
    for thread in self.active_threads:
      if thread is not threading.current_thread():
        thread.join()
        if thread.is_alive():
          thread.join()
        self.finished_threads.append(thread)
    self.active_threads = []
    self.length = len(self.active_threads)
  
  def search(self):
    if active_count() > len(self.active_threads):
      for t in threading.enumerate():
        if t not in self.active_threads:
          self.add(t)
    else:
      for t in self.active_threads:
        if t not in threading.enumerate():
          self.active_threads.remove(t)
          self.length = len(self.active_threads)
  
  def add(self, thd):
    self.active_threads.append(thd)
    self.length = len(self.active_threads)
  
ThdMng = ThreadManager()

def line(start, end, color, width=1):
  """
  draw a line in ```surface``` starting at ```start``` and ending at ```end```
  """
  if type(start) != list:
    raise TypeError("Start must be a list")
  if type(end) != list:
    raise TypeError("End must be a list")
  elif type(color) != tuple:
    raise TypeError("Color must be a tuple")
  elif type(width) != int:
    raise TypeError("Width must be an integer")
  start[0] += offset.x
  start[1] += offset.y
  end[0] += offset.x
  end[1] += offset.y
  pygame.draw.line(sc.screen, color, start, end, width)

class ProgressBar:
  """
    @param `pos` Vector2 object\n
    @param `maxW` Maximum width\n
    @param `maxH` Maximum height\n
    @param `minV` Minimum value\n
    @param `maxV` Maximum value\n
    @param `WD` Window width\n
    --------------Options-------------\n
    @param `color` Color of the progress bar\n
    @param `orientation` Orientation of the progress bar (VERTICAL/HORIZONTAL)\n
    @param `tooltip` If text at the end is visible
  """
  def __init__(self,pos,maxW,maxH,minV,maxV,WD,color=(0,255,0),orientation="HORIZONTAL",tooltip=True):
    self.pos = pos
    self.max_width = maxW
    self.max_height = int(mapping(maxH,0,WD,1,7))
    self.color = color
    self.orientation = orientation
    self.value = 0
    self.min = minV
    self.max = maxV
    self.tooltip = tooltip
    self.width = WD
  
  def update(self, val):
    self.value = val
  
  def show(self):
    if self.orientation is "HORIZONTAL":
      x = mapping(self.value,self.min,self.max,0,self.max_width)
      line([self.pos.x,self.pos.y],[self.pos.x+x,self.pos.y],self.color,self.max_height)
      if self.tooltip:
        if x < self.width-17:
          text(str(self.value),17,Color.WHITE,(self.pos.x+x,self.pos.y))
    elif "VERTICAL" in self.orientation:
      if "DOWN" in self.orientation:
        y = mapping(self.value,self.min,self.max,0,self.max_width)
        line([self.pos.x,self.pos.y],[self.pos.x,y+self.pos.y],self.color,self.max_height)
        if self.tooltip:
          if y < self.width-17:
            text(str(self.value),17,Color.WHITE,(self.pos.x,self.pos.y+y))
      elif "UP" in self.orientation:
        y = mapping(self.value,self.min,self.max,0,self.max_width)
        line([self.pos.x,self.pos.y],[self.pos.x,self.pos.y-y],self.color,self.max_height)
        if self.tooltip:
          if self.pos.y-y > 10:
            text(str(self.value),17,Color.WHITE,(self.pos.x,self.pos.y-y-10))
  
  def update_color(self,color):
    self.color = color

def rect(color, rect, width=0):
  a = rect[0]
  a += offset.x
  b = rect[1]
  b += offset.y
  pygame.draw.rect(sc.screen, color, (a,b,rect[2],rect[3]), width)

def ellipse(color, rect, width=0):
  "Draw an ellipse"
  if type(rect) != list:
    raise TypeError("Rect must be a list containing ```[x_position,y_position,width,height]```")
  elif type(width) != int:
    raise TypeError("Width must be an integer")
  rect[0] += offset.x
  rect[1] += offset.y
  pygame.draw.ellipse(sc.screen, color, rect, width)

def circle(color, center, radious, width=0):
  "Draw a circle"
  if type(center) != tuple:
    raise TypeError("Center must be a tuple")
  elif type(radious) != int:
    raise TypeError("Width must be an integer")
  a = center[0]
  a += offset.x
  b = center[1]
  b += offset.y
  pygame.draw.circle(sc.screen, color, (a,b), radious, width)

def text(content, size, color, position):
  "Creates text on screen"
  if type(content) != str:
    raise TypeError("Content must be a string")
  elif type(color) != tuple:
    raise TypeError("Color must be a tuple")
  elif type(size) != int:
    raise TypeError("Size must be an integer")
  elif type(position) != tuple:
    raise TypeError("Position must be a tuple")
  font = pygame.font.SysFont('Arial', size)
  disp = font.render(content, False, color)
  a = position[0]
  a += offset.x
  b = position[1]
  b += offset.y
  sc.screen.blit(disp, (a,b))

def screenshot(name):
  "Take screenshot of screen"
  if type(name) != str:
    raise TypeError("Content must be a string")
  if "Screenshots" not in listdir("."):
    mkdir("./Screenshots")
  pygame.image.save(sc.screen,"./Screenshots/{}".format(name))

def arc(color, rect, start_angle, stop_angle, width=1):
  if type(rect) != tuple:
    raise TypeError("Rect must be a tuple")
  elif type(color) != tuple:
    raise TypeError("Color must be a tuple")
  elif type(start_angle) != float or type(start_angle) != int:
    raise TypeError("Start angle must be an integer or float")
  elif type(stop_angle) != float or type(stop_angle) != int:
    raise TypeError("Stop angle must be an integer or float")
  a = rect[0]
  a += offset.x
  b = rect[1]
  b += offset.y
  pygame.draw.arc(sc.screen, color, (a,b,rect[2],rect[3]), start_angle, stop_angle, width)

def createMathGrid():
  line([sc.width/2,0],[sc.width/2,sc.height],Color.WHITE)
  line([0,sc.height/2],[sc.width,sc.height/2],Color.WHITE)
  size = 5
  for i in range(sc.width):
    if i % 20 == 0:
      translate(i,0)
      line([0,sc.height/2 - size],[0,sc.height/2 + size],Color.WHITE)
  translate(0,0)
  for i in range(sc.height):
    if i % 20 == 0:
      translate(0,i)
      line([sc.width/2 - size,0],[sc.width/2 + size,0],Color.WHITE)

def mapping(x, in_min, in_max, out_min, out_max):
    "Map values"
    if type(x) == int:
      return int((x - in_min) / (in_max - in_min) * (out_max - out_min) + out_min)
    elif type(x) == float:
      return float((x - in_min) / (in_max - in_min) * (out_max - out_min) + out_min)

def from_hsla(h):
    """
    Convert HSLA Color Mode to RGB
    """
    color = pygame.Color(0)
    color.hsla = h, 100, 50, 1
    return color

def post():
  "Code to execute after update.\nThis method is ``Overridable``"
  pass

def onExit():
  "Code to execute on exit.\nThis method is ``Overridable``"
  pass

def onUpdate():
  "Code to execute on manual update.\nThis method is ``Overridable``"
  pass

def pre():
  "Code to execute before everything.\nThis method is ``Overridable``"
  return CreateCanvas(1, 1)

def string_to_tuple(string):
  if type(string) is not str:
    raise TypeError("Parameter must be String type")
  return tuple(int(x) for x in string)

def fill(color):
  "Fills screen with a color"
  if type(color) != tuple:
    raise TypeError("Color must be a tuple")
  sc.screen.fill(color)

class Sleep:
  def __init__(self, length):
    self.length = length

Delay = Sleep(0)

def delay(leng):
  "Delay execution. \n``leng`` is in seconds"
  Delay.length = leng

def update():
  pygame.display.update()
  
def factorial(n):
  if n == 1:
      return 1
  else:
      return n * factorial(n - 1)

def isPrime(n):
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False

    return True

def dist(a, b, c, d):
  return sqrt(pow(a - c, 2) + pow(b - d, 2))

@dataclass
class Counter:
  index: int or float

  def add(self, n):
    self.index += n

  def sub(self, n):
    self.index -= n
  
  def mult(self, n):
    self.index *= n
  
  def divide(self, n):
    self.index /= n
  
  def print(self):
    print(self.index)

FRAMECOUNT = Counter(0)

@dataclass
class Vector2:
  x: int or float
  y: int or float
  
  type = "Vector2"

  def __repr__(self):
    return str("({},{})".format(self.x,self.y))

  def add(self, vect):
    if vect.type != self.type:
      raise TypeError("Argument must be Vector2")
    self.x += vect.x
    self.y += vect.y

  def subtract(self, vect):
    if vect.type != self.type:
      raise TypeError("Argument must be Vector2")
    self.x -= vect.x
    self.y -= vect.y

  def multiply(self, vect):
    if vect.type != self.type:
      raise TypeError("Argument must be Vector2")
    self.x *= vect.x
    self.y *= vect.y
  
  def multiply_scalar(self,scalar):
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
  
  def restore_values(self, vect):
    if vect.type != self.type:
      raise TypeError("Argument must be Vector2")
    self.x = vect.x
    self.y = vect.y

  def copy(self):
    return deepcopy(Vector2(self.x,self.y))
  
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
    part1 = (vec2.x - vec1.x) ** 2
    part2 = (vec2.y - vec1.y) ** 2
    part3 = part1 + part2
    return sqrt(part3)
    
@dataclass
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

  _colors = {
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

  def __init__(self,color=None):
    if color is not None and "#" not in color and color.lower() not in self._colors:
      raise AttributeError("Color not found")
    self.tup = False
    if color is not None:
      if "#" not in color:
        self.selected = self._colors[color.lower()]
        self.tup = True
      else:
        self.hexa = color.upper()
        hexar = str(color).replace("#","").upper()
        if len(hexar) == 3:
          r = int(str(hexar[0])+str(hexar[0]),16)
          g = int(str(hexar[1])+str(hexar[1]),16)
          b = int(str(hexar[2])+str(hexar[2]),16)
        else:
          r = int(hexar[0:2],16)
          g = int(hexar[2:4],16)
          b = int(hexar[4:6],16)
        self.code = (r,g,b)
  
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
    hexar = str(code).replace("#","").upper()
    if len(hexar) == 3:
      r = int(str(hexar[0])+str(hexar[0]),16)
      g = int(str(hexar[1])+str(hexar[1]),16)
      b = int(str(hexar[2])+str(hexar[2]),16)
    else:
      r = int(hexar[0:2],16)
      g = int(hexar[2:4],16)
      b = int(hexar[4:6],16)
    return (r,g,b)
  
  @staticmethod
  def fromDecimal(code):
    if type(code) != tuple:
      raise TypeError("Code must be a tuple")
    r = str(hex(code[0])).replace("0x","")
    g = str(hex(code[1])).replace("0x","")
    b = str(hex(code[2])).replace("0x","")
    if r == "0":
      r = "00"
    if g == "0":
      g = "00"
    if b == "0":
      b = "00"
    hexar = "#{}{}{}".format(r,g,b).upper()
    return hexar
  
  def loadCustomColors(self):
    try:
      data = json.load(open(r"./Lib/custom_colors.json","r"))
      for key in data.keys():
        r = int(data[key]["r"])
        g = int(data[key]["g"])
        b = int(data[key]["b"])
        self._colors[key] = (r,g,b)
    except FileNotFoundError as err:
      logger.error(err)
  
  def getColor(self,color):
    if color is not None and "#" not in color and color.lower() not in self._colors:
      raise AttributeError("Color not found")
    self.selected = self._colors[color.lower()]
    self.tup = True
    return self.selected


@dataclass
class Dimensions:
  width: int
  height: int

window = None


def CreateCanvas(width, height):
  window = Dimensions(width, height)
  return window

@property
def getSize():
  return window

def Vertex(points, color, width=1, close=False):
  result = []
  for p in points:
      result.append((p.x+offset.x,p.y+offset.y))

  if len(result) >= 2:
    pygame.draw.lines(sc.screen, color, close, result, width)

def getPixelArray(screen):
  return pygame.PixelArray(screen)

def paintPixel(pos,color,pixar):
  pixar[pos.x][pos.y] = color

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

  def grad(self,hash, x, y, z):
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
    if h&1 == 0: 
      first = u
    else:        
      first = -u

    if h&2 == 0: 
      second = v
    else:        
      second = -v

    return first + second
      
  def noise(self, x,y=0.0,z=0.0):
    X = int(x) & (self.tiledim-1)
    Y = int(y) & (self.tiledim-1)
    Z = int(z) & (self.tiledim-1)
    
    x -= int(x)
    y -= int(y)
    z -= int(z)
    
    u = self.fade(x)
    v = self.fade(y)
    w = self.fade(z)
    
    A = self.p[X  ]+Y; AA = self.p[A]+Z; AB = self.p[A+1]+Z
    B = self.p[X+1]+Y; BA = self.p[B]+Z; BB = self.p[B+1]+Z
    
    return self.lerp(w, self.lerp(v, self.lerp(u,self.grad(self.p[AA  ],x  ,y  ,z  ), self.grad(self.p[BA  ],x-1,y  ,z  )), self.lerp(u,self.grad(self.p[AB  ],x  ,y-1,z  ), self.grad(self.p[BB  ],x-1,y-1,z  ))), self.lerp(v, self.lerp(u,self.grad(self.p[AA+1],x  ,y  ,z-1), self.grad(self.p[BA+1],x-1,y  ,z-1)), self.lerp(u,self.grad(self.p[AB+1],x  ,y-1,z-1), self.grad(self.p[BB+1],x-1,y-1,z-1))))

def fps30():
  return 1 / 30

def fps60():
  return 1 / 60

def fps144():
  return 1 / 144

def getMouse():
  pos = pygame.mouse.get_pos()
  return Vector2(pos[0], pos[1])
  
@dataclass
class Value:
  value: int or float

  def update(self, n):
    self.value = n

class Matrix:
  rows = 0
  cols = 0
  size = ""
  arr = []

  def __init__(self,rows=None,cols=None):
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
    return [self.cols,self.rows]
  
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
    temp = Matrix(len(data),1)
    for y in range(temp.rows):
      for x in range(temp.cols):
        temp.setValue(x,y,data[y])
    return temp
  
  @staticmethod
  def subtract(a, b):
    if a.rows != b.rows or a.cols != b.cols:
      print("Columns and rows of A must match Columns and Rows of B.")
      return
    temp = Matrix(a.rows,b.cols)
    for y in range(temp.rows):
      for x in range(temp.cols):
        temp.setValue(x,y,a[x][y]-b[x][y])
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
        self.arr[y][x] = uniform(0,1)

  def add(self,n):
    if isinstance(n,Matrix):
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
    temp = Matrix(matrix.cols,matrix.rows)
    for y in range(temp.rows):
      for x in range(temp.cols):
        temp.setValue(x,y,matrix.arr[x][y])
    return temp
  
  @staticmethod
  def multiply(a,b):
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
          sumz += (a.getValue(k,y) * b.getValue(x,k))
        temp.setValue(x,y,sumz)
    return temp
  
  def copy(self):
    return deepcopy(self)

class Ball:
  gravity = 9.8
  vacuum = False
  bounciness = 1

  def __init__(self, x, y, radious, weight, init_speed=0, color=Color.WHITE):
    self.pos = Vector2(x,y)
    self.radious = radious
    self.weight = weight
    self.initialSpeed = init_speed
    self.currentSpeed = init_speed
    self.color = color
    self.lastY = 0
    if self.initialSpeed == 0 and self.currentSpeed == 0:
      self.currentSpeed = 1
    self.descending = True
  
  def setVacuum(self, vac=False):
    self.vacuum = vac
  
  def setBounce(self, value):
    if value > 1.0 or value < 0.0:
      raise ArithmeticError("Value must be between 0 and 1")
    self.bounciness = value

  def update(self):
    if self.currentSpeed > 90.0:
      self.currentSpeed = 90

    if self.descending:
      if self.vacuum:
        self.currentSpeed *= 1.07
      else:
        self.currentSpeed *= mapping(float(self.weight),0,100,1.03,1.1)
    else:
      if self.vacuum:
        self.currentSpeed *= 0.93 * self.bounciness
      else:
        self.currentSpeed *= mapping(float(self.weight),0,100,0.94,0.86) * self.bounciness
      if (self.pos.y < self.lastY+0.025 and self.pos.y > self.lastY-0.025 and self.currentSpeed < 0.5):
        self.descending = True

    if self.descending:
      self.pos.y += self.currentSpeed
    else:
      self.pos.y -= self.currentSpeed

    if self.pos.y > sc.height and self.descending:
      self.currentSpeed = self.currentSpeed * 0.9999
      self.pos.y -= self.currentSpeed
      self.descending = False

    ellipse(self.color, [self.pos.x-self.radious, self.pos.y-self.radious, self.radious * 2, self.radious * 2],8)
    ellipse(Color.RED, [self.pos.x-self.radious+2, self.pos.y-self.radious+2, (self.radious-2) * 2, (self.radious-2) * 2])
    self.lastY = self.pos.y

  
  def print(self, x, y, logger=False):
    size = 15
    if logger:
      print("------\nX: {}\nY:{}\nLast Y: {}\nInitial Speed: {}\nCurrent Speed:{}\nWeight: {}\n------".format(self.pos.x, self.pos.y, self.lastY,self.initialSpeed, self.currentSpeed, self.weight))
    text("Descending: {}".format(self.descending), size, Color.WHITE, (x,y))
    text("Current Speed:  {}".format(round(self.currentSpeed, 1)), 15, Color.WHITE, (x, y+size+1))
    text("Weight:  {}".format(self.weight), 15, Color.WHITE, (x, y + size*2 + 1))
    
  def setScreen(self, w, h):
    self.width = w
    self.height = h

class Supershape:
  n1 = 1
  n2 = 1
  n3 = 1
  m = 5
  a = 1
  b = 1
  updates = 0
  osc = 0

  def __init__(self):
    print("Supershape started")
    print("%dx%d" % (sc.width,sc.height))

  def update(self):
    self.updates += 1
    points = []

    radious = 100
    total = 200
    increment = float((pi * 2) / total)

    for angle in arange(0.0, pi * 2, increment):
      r = self.calc(angle)
      x = radious * r * cos(angle)
      y = radious * r * sin(angle)

      points.append(Vector2(int(x), int(y)))
    return points
    
  def calc(self,theta):
    part1 = (1 / self.a) * cos(theta * self.m / 4)
    part1 = abs(part1)
    part1 = pow(part1, self.n2)
    
    part2 = (1 / self.b) * sin(theta * self.m / 4)
    part2 = abs(part2)
    part2 = pow(part2, self.n3)

    part3 = pow(part1 + part2, 1 / self.n1)
    
    if part3 == 0:
      return 0
    ans = 1 / part3
    return ans

class Flag:

  flag = None

  def __init__(self, default=True):
    self.flag = default
  
  def get(self):
    return self.flag
  
  def change(self):
    self.flag = not self.flag
    return self.flag

noLoop = Flag(False)

def no_Loop():
  noLoop.change()

UPDATE = Flag(True)

def noUpdate():
  UPDATE.flag = False

def fibonacci(n):
  if n < 2:
    return n
  else:
    return fibonacci(n - 1) + fibonacci(n - 2)
  
def mousePressed():
  if pygame.mouse.get_pressed()[0]:
    return True
  else:
    return False

class Node(object):

  def __init__(self, data, next=None, previous=None):
    self.data = data
    self.next = next
    self.previous = previous
  
  def set_next(self, next):
    self.next = next
  
  def set_data(self, data):
    self.data = data
  
class LinkedList(object):

  def __init__(self, root=None):
    self.root = root
    self.current_node = self.root
    self.size = 0

  def __repr__(self):
    return str(self.current_node.data)

  def add(self, data):
    node = Node(data)
    node.next = self.root

    if self.root is not None:
      self.root.previous = node
      
    self.root = node
    self.current_node = node
    self.size += 1
  
  def remove(self, data):
    node = self.root
    prev = None

    while node is not None:
      if node.data == data:
        if prev:
          prev.set_next(node.next)
        else:
          self.root = node
        self.size -= 1
        return True
      else:
        prev = node
        node = node.next
    return False
  
  def find(self, data):
    node = self.root
    while node is not None:
      if node.data == data:
        return node
      else:
        node = node.next
    return None
  
  def print(self):
    node = self.root
    while node is not None:
      print("%d" % node.data, end=" ")
      node = node.next
    print()
    del node
  
  def next(self):
    if self.current_node.next is not None:
      self.current_node = self.current_node.next
      return True
    else:
      return False
  
  def hasNext(self, node):
    if node.next is None:
      return False
    else:
      return True

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

class Array:

  def __init__(self, slots, initialize=None):
    self.length = slots
    self.data = [initialize] * slots
  
  def set(self,pos,val=None,function=None):
    if pos < self.length - 1 and pos >= 0:
      if function is not None and val is None:
        self.data[pos] = function(self.data[pos])
      elif function is None and val is not None:
        self.data[pos] = val
  
  def get(self):
    return self.data

  def getValue(self,index):
    return self.data[index]
  
  def search(self, value):
    indexes = []
    for index, data in enumerate(self.data):
      if data == value:
        indexes.append(index)
    if len(indexes) == 1:
      return indexes[0]
    elif len(indexes) == 0:
      return None
    else:
      return indexes
  
  def remove(self, index, value=None):
    if index < self.length and index >= 0 and type(index) == int and value is None:
      self.data.pop(index)
    elif value is not None:
      newArr = self.copy()
      for _ in newArr.search(value):
        newArr.data.remove(value)
      return newArr
    else:
      raise IndexError
  
  def copy(self):
    return deepcopy(self)

  @staticmethod
  def listToArray(a):
    if type(a) is list:
      newArray = Array(len(a),0)
      newArray.data = deepcopy(a)
      newArray.length = len(a)
      return newArray

  def swap(self,i,j):
    value = self.data[i]
    self.data[i] = self.data[j]
    self.data[j] = value
    del value
  
  def reverse(self):
    test = reversed(deepcopy(self.data))
    self.data = test
    del test
  
  def concat(self, data):
    test = deepcopy(self.data) + data
    self.data = test
    del test
  
  def splice(self,index):
    value = self.getValue(index)
    self.remove(index)
    newList = []
    newList.append(value)
    del value
    return newList
  
  def print(self):
    for d in self.data:
      print(d, end=" ")
    print()

class MouseDraw(Thread):
  
  exec = True

  def __init__(self):
    Thread.__init__(self)
    Thread.setName(self, "Mouse Capture")
    logger.info("Mouse capture initialized - {}".format(strftime("%H:%M:%S - %Y/%m/%d")))
    self.start_time = time()
    Thread.start(self)
    self.history = []
  
  def __repr__(self):
    return str(self.history)

  def run(self):
    runs = 0
    while self.exec:
      try:
        if mousePressed():
          print("Hello", flush=True)
          while mousePressed():
            self.history.append(getMouse())
          if not mousePressed():
            print("outside", flush=True)
            self.exec = False
        sleep(0.05)
      except Exception as err:
        logger.info(str(err))
  
  def dispose(self):
    logger.info("Finished coordinates collection - {} seconds".format(time()-self.start_time))
    Thread.join(self)
    if len(self.history) != 0:
      logger.info("Collected {} points".format(len(self.history)))
      return self.history
    else:
      del self

class Timer(Thread):
  """Create a timed event:\n
    `function` - is the callback which the timer runs (Either Lambda or defined methods)
    `timeout` - is expressed in seconds and represents the time interval"""

  exec = True

  def __init__(self, function, timeout):
    if not callable(function):
      logger.error("Parameter must be a function")
      exit(1)
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

class Spreadsheet:
  def __init__(self, name):
    if "Spreadsheets" not in listdir("."):
      mkdir("Spreadsheets")
    self.book = Workbook("Spreadsheets/{0}.xlsx".format(name))
    self.worksheet = self.book.add_worksheet()
    self.BOLD = self.book.add_format({"bold": True})
    self.ITALIC = self.book.add_format({"italic": True})

  def write(self, cell, data, format=None):
    if format is None:
      self.worksheet.write(str(cell),data)
    else:
      self.worksheet.write(str(cell),data,format)
  
  def write_num_notation(self,row,column,data,format):
    if type(row) is not int or type(column) is not int:
      raise TypeError("Row and Column must be integers")
      exit(1)

    if format is None:
      self.worksheet.write(row,column,data)
    else:
      self.worksheet.write(row,column,data,format)

  def add_image(self, row, column, path):
    if type(row) is not int or type(column) is not int:
      raise TypeError("Row and Column must be integers")
      exit(1)
    self.worksheet.insert_image(row, column, str(path))

  def format_column(self, column, spacing):
    if len(column) > 1:
      print("Column must be a single character")
    else:
      self.worksheet.set_column("{0}:{0}".format(column.upper()),spacing)

  def finish(self):
    self.book.close()

class Mathcontext:

  def __init__(self,context):
    self.context = context
    getcontext().prec = self.context

  def get(self):
    return self.context
  
  def set_rounding(self, method):
    getcontext().rounding = method

class BigDecimal:

  def __init__(self,value):
    self.init_value = value
    self.value = Decimal(value)

  def __repr__(self):
    return str(self.value)
  
  def divide(self,value):
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
    add = self.equation.replace(" ","").replace("x2","x²")
    return str(add)
  
  def get_zeros(self):
    bsqrd = pow(self.b,2)
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
      return [Vector2(pos_part,0)]
    else:
      pos_part = ((part1 + sqrt(part4)) / part3)
      neg_part = ((part1 - sqrt(part4)) / part3)
      return [Vector2(neg_part,0), Vector2(pos_part,0)]
  
  def get_y(self, x):
    a = self.a * x**2
    b = self.b * x
    result = a + b + self.c
    return result

class Sorting:

  def __init__(self, arr):
    self.array = arr
    self.original = arr
    self.history = []
    self.length = len(self.array)

  def __repr__(self):
    return str(self.array)

  def get(self):
    return self.array

  def BubbleSort(self, reverse=False):
    a = deepcopy(self)
    start = time()
    for i in range(a.length):
      for j in range(a.length):
        if not reverse:
          if a.array[i] < a.array[j]:
            aux = a.array[i]
            a.array[i] = a.array[j]
            a.array[j] = aux
            a.history.append(deepcopy(a.array))
        else:
          if a.array[i] > a.array[j]:
            aux = a.array[i]
            a.array[i] = a.array[j]
            a.array[j] = aux
            a.history.append(deepcopy(a.array))
    end = time()
    print("Algorithm: {}".format("BubbleSort"),"|","Time ellapsed: {}{}".format(end-start,"s"),"|","Moves: {}".format(len(a.history)), flush=True)
    return a
  
  def InsertionSort(self,save=False):
    a = deepcopy(self)
    start = time()
    for i in range(1, a.length): 
        key = a.array[i]
        j = i-1
        while j >= 0 and key < a.array[j] : 
          a.array[j + 1] = a.array[j] 
          j -= 1
          if save:
            a.history.append(deepcopy(a.array))
        a.array[j + 1] = key 
        if save:
          a.history.append(deepcopy(a.array))
    end = time()
    print("Algorithm: {}".format("InsertionSort"),"|","Time ellapsed: {}{}".format(end-start,"s"),"|","Moves: {}".format(len(a.history)), flush=True)
    return a

  def QuickSort(self):
    a = deepcopy(self)
    start = time()
    self.__quicks(a.array,0,a.length-1)
    end = time()
    print("Algorithm: {}".format("QuickSort"),"|","Time ellapsed: {}{}".format(end-start,"s"),"|","Moves: {}".format(len(a.history)), flush=True)
    return a

  def __countingSort(self, arr, exp1): 
    n = len(arr) 
    output = [0] * (n) 
    count = [0] * (10) 
  
    for i in range(0, n): 
        index = (arr[i]/exp1) 
        count[ (index)%10 ] += 1
  
    for i in range(1,10): 
        count[i] += count[i-1] 
  
    i = n-1
    while i>=0: 
        index = int(arr[i]/exp1) 
        output[ count[ (index)%10 ] - 1] = arr[i] 
        count[ (index)%10 ] -= 1
        i -= 1
    i = 0
    for i in range(0,len(arr)): 
        arr[i] = output[i] 
  
  def RadixSort(self): 
    a = deepcopy(self)
    start = time()
    max1 = max(a.array) 
    exp = 1
    while max1 / exp > 0: 
      self.__countingSort(a.array,exp) 
      exp *= 10
    end = time()
    print("Algorithm: {}".format("RadixSort"),"|","Time ellapsed: {}{}".format(end-start,"s"),"|","Moves: {}".format(len(a.history)), flush=True)
    return a

  def __quicks(self,arr,low,high): 
    if low < high:
      pi = self.__partition(arr,low,high)
      self.__quicks(arr, low, pi-1) 
      self.__quicks(arr, pi+1, high)  
  
  def __partition(self,arr,low,high): 
    i = low - 1
    pivot = arr[high]
  
    for j in range(low , high): 
      if arr[j] <= pivot: 
        i = i+1 
        arr[i],arr[j] = arr[j],arr[i] 
  
    arr[i+1],arr[high] = arr[high],arr[i+1] 
    return (i + 1)
  
  def ShellSort(self):
    a = deepcopy(self)
    gap = a.length//2
    start = time()
    while gap > 0: 
      for i in range(gap,a.length): 
        temp = a.array[i] 
        j = i 
        while  j >= gap and a.array[j-gap] >temp: 
          a.array[j] = a.array[j-gap] 
          j -= gap
          a.history.append(deepcopy(a.array))
        a.array[j] = temp
        a.history.append(deepcopy(a.array))
      gap //= 2
    end = time()
    print("Algorithm: {}".format("ShellSort"),"|","Time ellapsed: {}{}".format(end-start,"s"),"|","Moves: {}".format(len(a.history)), flush=True)
    return a
  
  def __insertionSort(self,b): 
    for i in range(1, len(b)): 
      up = b[i] 
      j = i - 1
      while j >=0 and b[j] > up:  
        b[j + 1] = b[j] 
        j -= 1
      b[j + 1] = up     
    return b      
              
  def BucketSort(self): 
    a = deepcopy(self)
    start = time()
    arr = [] 
    slot_num = 10 
    for i in range(slot_num): 
      arr.append([]) 
    for j in a.array: 
      index_b = int(slot_num * j)  
      arr[index_b].append(j) 
    
    for i in range(slot_num): 
      arr[i] = self.__insertionSort(arr[i]) 
    
    k = 0
    for i in range(slot_num): 
      for j in range(len(arr[i])): 
        a.array[k] = arr[i][j] 
        k += 1
        a.history.append(deepcopy(a.array))    
    end = time()
    print("Algorithm: {}".format("BucketSort"),"|","Time ellapsed: {}{}".format(end-start,"s"),"|","Moves: {}".format(len(a.history)), flush=True)
    return a
  
  def SelectionSort(self):
    a = deepcopy(self)
    start = time()
    for i in range(a.length): 
      min_idx = i 
      for j in range(i+1, a.length): 
        if a.array[min_idx] > a.array[j]: 
          min_idx = j 
      a.array[i], a.array[min_idx] = a.array[min_idx], a.array[i]
      a.history.append(deepcopy(a.array))
    end = time()
    print("Algorithm: {}".format("SelectionSort"),"|","Time ellapsed: {}{}".format(end-start,"s"),"|","Moves: {}".format(len(a.history)), flush=True)
    return a
  
  def StoogeSort(self):
    a = deepcopy(self)
    start = time()
    self.__stooge(a.array, 0, a.length-1)
    end = time()
    print("Algorithm: {}".format("StoogeSort"),"|","Time ellapsed: {}{}".format(end-start,"s"),"|","Moves: {}".format(len(a.history)), flush=True)
    return a

  def __stooge(self,arr,l,h):
    if l >= h: 
      return
      
    if arr[l]>arr[h]: 
      t = arr[l] 
      arr[l] = arr[h] 
      arr[h] = t 

    if h-l + 1 > 2: 
      t = (int)((h-l + 1)/3) 
      self.__stooge(arr, l, (h-t)) 
      self.__stooge(arr, l + t, (h)) 
      self.__stooge(arr, l, (h-t))

  def __getNextGap(self,gap):
    gap = (gap * 10)/13
    if gap < 1: 
      return 1
    return int(gap) 
  
  def CombSort(self, save=False): 
    a = deepcopy(self)
    start = time()
    n = a.length
  
    gap = n 
    swapped = True
  
    while gap !=1 or swapped == 1: 
      gap = self.__getNextGap(gap) 
      
      swapped = False
      
      for i in range(0, n-gap): 
        if a.array[i] > a.array[i + gap]: 
          a.array[i], a.array[i + gap]=a.array[i + gap], a.array[i] 
          swapped = True
          if save:
            a.history.append(deepcopy(a.array))
    end = time()
    print("Algorithm: {}".format("CombSort"),"|","Time ellapsed: {}{}".format(end-start,"s"),"|","Moves: {}".format(len(a.history)), flush=True)
    return a
  
  def PigeonholeSort(self, save=False):
    a = deepcopy(self)
    start = time()
    my_min = min(a.array) 
    my_max = max(a.array) 
    size = my_max - my_min + 1
    
    holes = [0] * size 
    
    for x in a.array: 
      assert type(x) is int, "integers only please"
      holes[x - my_min] += 1
    i = 0
    for count in range(size): 
      while holes[count] > 0: 
        holes[count] -= 1
        a.array[i] = count + my_min 
        i += 1
        if save:
          a.history.append(deepcopy(a.array))
    end = time()
    print("Algorithm: {}".format("PigeonholeSort"),"|","Time ellapsed: {}{}".format(end-start,"s"),"|","Moves: {}".format(len(a.history)), flush=True)
    return a
  
  def CocktailSort(self):
    a = deepcopy(self)
    starting = time()
    swapped = True
    start = 0
    end = a.length-1
    while (swapped == True): 

      swapped = False

      for i in range (start, end): 
        if (a.array[i] > a.array[i + 1]) : 
          a.array[i], a.array[i + 1]= a.array[i + 1], a.array[i] 
          swapped = True
          a.history.append(deepcopy(a.array))

      if (swapped == False): 
        break
      
      swapped = False
      
      end = end-1
      
      for i in range(end-1, start-1, -1): 
        if (a.array[i] > a.array[i + 1]): 
          a.array[i], a.array[i + 1] = a.array[i + 1], a.array[i] 
          a.history.append(deepcopy(a.array))
          swapped = True
      
      start = start + 1
    
    end = time()
    print("Algorithm: {}".format("CocktailSort "),"|","Time ellapsed: {}{}".format(end-starting,"s"),"|","Moves: {}".format(len(a.history)), flush=True)
    return a
  
class Slider:

  def __init__(self,start,min,max,orientation="VERTICAL", override=None, name="Slider",WD=300):
    if start < min or start > max:
      raise ValueError("Start is out of bounds")
    self.min = min
    self.max = max
    self.start = start
    self.orientation = orientation
    if override is None:
      self.master = Tk()
    else:
      self.master = override
    self.master.title(name)
    self.master.protocol("WM_DELETE_WINDOW", self.no_exit)
    if self.orientation == "VERTICAL":
      self.slider = Scale(self.master,from_=self.min,to=self.max, length=mapping(self.max, self.min,self.max,0,WD))
    elif self.orientation == "HORIZONTAL":
      self.slider = Scale(self.master,from_=self.min,to=self.max, length=mapping(self.max, self.min,self.max,0,WD), orient=HORIZONTAL)
    self.slider.set(self.start)
    self.slider.pack()
    self.frame = Frame(self.master)
  
  def no_exit(self):
    pass
    
  def update(self):
    self.frame.update()
  
  def get(self):
    return self.slider.get()
  
  def dispose(self):
    self.frame.destroy()

class Image(object):

  def __init__(self, file=None, image=None):
    if file is not None and image is None:
      self.path = "./Images/{}".format(file)
      self.image = pygame.image.load(self.path)
    elif file is None and image is not None:
      self.image = image
    self.angle = 0

  def show(self,pos):
    sc.screen.blit(self.image,(pos.x,pos.y))
  
  def toString(self):
    return pygame.image.tostring(self.image,"RGBA")
  
  def scale(self, newW, newH):
    self.image = pygame.transform.scale(self.image,(newW,newH))

  def rotate(self, angle):
    self.angle = angle
    self.image = pygame.transform.rotate(self.image,self.angle)
  
  @staticmethod
  def fromString(string, size):
    return Image(image=pygame.image.fromstring(string,size,"RGBA"))

if __name__ == '__main__':
  print("run `python3 pyDraw.py` instead")