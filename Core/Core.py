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
from math import e,pi,sin
import colored_traceback.always
from os import listdir, mkdir, cpu_count
from threading import Thread, active_count, current_thread
from threading import enumerate as enumerate_thread
from logging import getLogger
from copy import deepcopy,copy
from pyautogui import size
from tkinter import Tk, Scale, Frame, HORIZONTAL

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

EMPTY = 0

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
SCREEN = None

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
      if thread is not current_thread():
        thread.join()
        if thread.is_alive():
          thread.join()
        self.finished_threads.append(thread)
    self.active_threads = []
    self.length = len(self.active_threads)
  
  def search(self):
    if active_count() > len(self.active_threads):
      for t in enumerate_thread():
        if t not in self.active_threads:
          self.add(t)
    else:
      for t in self.active_threads:
        if t not in enumerate_thread():
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
  
  def copy(self):
    return deepcopy(self)

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
  
def mousePressed():
  if pygame.mouse.get_pressed()[0]:
    return True
  else:
    return False

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
  
class Slider:

  def __init__(self,start,min,max,orientation="VERTICAL", override=None, name="Slider",WD=300):
    if start < min or start > max:
      raise ValueError("Start is out of bounds")
    self.min = min
    self.max = max
    self.start = start
    self.orientation = orientation
    #if override is None:
      #self.master = Tk()
    #else:
      #self.master = override
    self.master = Tk() if override is None else override
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

if __name__ == '__main__':
  print("run `python3 pyDraw.py` instead")