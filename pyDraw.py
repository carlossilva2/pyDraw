#!/usr/bin/env python3

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
try:
    import pygame
except ImportError:
    print("Unable to find Pygame. Please install")
    exit(1)
try:
    import colored_traceback.always
except ImportError:
    print("Colored traceback is advisable, please install...")
    exit(1)
from os import getcwd, listdir, mkdir, environ
from sys import path
import logging as log
from time import strftime, time
from math import floor
from random import randint
from Core.Color import Color
from socket import gethostbyname, gethostname
import platform
if platform.system() == "Windows":
    from ctypes import windll
    windll.shell32.SetCurrentProcessExplicitAppUserModelID('pyDraw.pyDraw.pyDraw.013')

if "Logs" not in listdir("."):
    mkdir("Logs")

if "log {}.bin".format(strftime("%d-%m-%Y")) not in listdir("./Logs"):
    open("./Logs/log {}.bin".format(strftime("%d-%m-%Y")),"w").write("")

if "Sounds" not in listdir("."):
    mkdir("Sounds")

if "Images" not in listdir("."):
    mkdir("Images")

log.basicConfig(filename="Logs/log {}.bin".format(strftime("%d-%m-%Y")),level=log.DEBUG)

class pyDraw:

    __version__ = 0.20

    def __init__(self, sketch):
        self.start_time = time()
        self.current_time = self.start_time
        self.setup_flag = False
        self.draw_flag = False
        self.hold = False
        self.actions_buffer = []
        import Sketch
        self.sketch = Sketch
        self.sketch.canvas = self.size
        log.info("Checked for updates at {0}".format(strftime("%Hh%Mm")))
        pygame.init()
        self.count = 0
        pygame.display.init()
        pygame.display.set_icon(pygame.image.load("pyDraw.ico"))
        d = pre()
        if d == None and (self.width == None or self.height == None):
            log.warning("The method \'pre()\' must be used to define the window dimensions")
            raise Warning("To create a window you must use the CreateCanvas(width,height) method inside the pre() method")
        elif d != None:
            self.width = d.width
            self.height = d.height
        self.apply_system()
        self.screen = pygame.display.set_mode([self.width, self.height], pygame.DOUBLEBUF|pygame.HWSURFACE)
        self.sketch.SCREEN = self.screen
        setScreen(self.screen, self.width, self.height)
        log.info("Screen set - {}x{}".format(self.width,self.height))
        try:
            update()
            setup()
        except Exception as err:
            if err != "name 'MOUSE' is not defined":
                log.error(err)
                print(err)
            self.setup_flag = True
        log.info("Setup ran successfully")
        self.sketch_name = sketch
        pygame.display.update()
        pygame.display.set_caption(sketch)

    def draw(self):
        try:
            if not self.hold and Delay.length != 0:
                self.timed_draw = Timer(draw,Delay.length)
                self.hold = True
            elif self.hold:
                pass
            else:
                draw()
        except Exception as err:
            if self.count == 0:
                if "name 'MOUSE' is not defined" not in str(err):
                    log.error(err)
                    print(err)
                self.draw_flag = True
        if self.count == 0 and self.setup_flag and self.draw_flag:
            log.error("Neither Setup nor Draw are defined. Please use at least one of them")
            exit(1)
        if UPDATE.flag:
            pygame.display.update()
        post()
        self.count += 1

    def spin(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == KEYS['q']):
                onExit()
                if self.hold and Delay.length != 0:
                    self.timed_draw.dispose()
                if ThdMng.length != 0:
                    ThdMng.dispose_all()
                self.release_imports()
                log.info("Exiting...")
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                noLoop.change()
                fill(Color.BLACK)
                text("-- Paused --",40,Color.WHITE,(self.width/2-80,self.height/2-20))
                pygame.display.update()
            elif event.type == pygame.KEYDOWN and event.key == KEYS['u']:
                onUpdate()
                pygame.display.update()
            elif event.type == pygame.KEYDOWN and event.key == KEYS['s']:
                screenshot("{} - {}.jpg".format(self.sketch_name,strftime("%H_%M_%S")))
                log.info("Screenshot taken")
                
            for actions in self.actions_buffer:
                if "KEYPRESS" in actions['action']:
                    if event.type == pygame.KEYDOWN and event.key == KEYS[str(actions['action']).split(".")[1].lower()]:
                        if len(actions['args']) > 0:
                            actions['callback'](actions['args'])
                        else:
                            actions['callback']()
                elif "MOUSEPRESS" in actions['action']:
                    parse = 0
                    if "." in actions['action']:
                        __ac = actions['action'].split(".")[1].lower()
                        if "left" == __ac:
                            parse = 0
                        elif "center" == __ac:
                            parse = 1
                        elif "right" == __ac:
                            parse = 2
                        else:
                            parse = 0
                    if pygame.mouse.get_pressed()[parse] == 1:
                        if len(actions['args']) > 0:
                            actions['callback'](actions['args'])
                        else:
                            actions['callback']()

    def start(self):
        while not self.spin():
            try:
                if not noLoop.flag:
                    self.draw()
                    clock.tick(120)
                    FRAMECOUNT.add(1)
                    self.sketch.FRAMECOUNT = FRAMECOUNT.index
                    self.sketch.mouse = getMouse()
                    if floor(time() - self.current_time) >= 0.6:
                        self.current_time = time()
                        ThdMng.search()
                else:
                    continue
            except (KeyboardInterrupt):
                onExit()
                if ThdMng.length != 0:
                    ThdMng.dispose_all()
                self.release_imports()
                exit(0)
    
    def release_imports(self):
        contents = []
        with open(f'./Projects/{self.sketch_name}/Sketch.py', 'r') as file:
            contents = file.readlines()
            for i in range(len(contents)):
                if "from Core.Minimum import *" in contents[i]:
                    contents[i] = "#PYDRAW_\n"
                    break
            file.close()
        with open(f'./Projects/{self.sketch_name}/Sketch.py', 'w') as buffer:
            buffer.writelines(contents)
            buffer.close()
    
    def on(self, action, callback, *args):
        if "KEYPRESS" in action or "MOUSEPRESS" in action:
            self.actions_buffer.append({
                'action': action,
                'callback': callback,
                'args': args
            })
        self.__self_preserve_actions()
    
    def size(self, width:int, height:int):
        self.width = width
        self.height = height

    def __self_preserve_actions(self):
        to_pop = []
        for index,action in enumerate(self.actions_buffer):
            for i,comparison in enumerate(self.actions_buffer):
                if action['action'] == comparison['action'] and i != index and index not in to_pop:
                    if action['callback'] == comparison['callback']:
                        print(action['action'], i)
                        to_pop.append(i)
        to_pop.sort()
        to_pop.reverse()
        for i in to_pop:
            self.actions_buffer.pop(i)

    def apply_system(self):
        block = {}
        block['os'] = platform.system()
        block['release'] = platform.release()
        block['version'] = platform.version()
        block['platform'] = platform.platform()
        block['processor'] = platform.processor()
        block['hostname'] = gethostname()
        block['ip'] = gethostbyname(gethostname())
        self.sketch.floor = floor
        self.sketch.SYSTEM = block
        self.sketch.WIDTH = self.width
        self.sketch.HEIGHT = self.height
        self.sketch.random = randint
        self.sketch.color = Color()
        self.sketch.on = self.on


def get_sketches():

    def getInput(length):
        choice = ""
        try:
            choice = input("Choose a project: ")
            if int(choice) > length-1 or int(choice) < 0 or choice == None or choice == "":
                raise Exception
        except Exception:
            choice = getInput(length)
        return choice
    
    def add_imports(proj):
        contents = []
        with open(f'./Projects/{proj}/Sketch.py', 'r') as file:
            contents = file.readlines()
            for i in range(len(contents)):
                if "#PYDRAW_" in contents[i]:
                    contents[i] = "from Core.Minimum import *\n"
                    break
            file.close()
        with open(f'./Projects/{proj}/Sketch.py', 'w') as buffer:
            buffer.writelines(contents)
            buffer.close()

    sec = listdir(".")
    if "Projects" not in sec:
        mkdir("./Projects")
    projects = [pr for pr in listdir("./Projects/") if "Sketch.py" in listdir("./Projects/{}/".format(pr,))]
    projects.sort()
    ignored_projects = [pr for pr in listdir("./Projects/") if "Sketch.py" not in listdir("./Projects/{}/".format(pr,))]
    if len(projects) == 0:
        print("You have no projects!")
        exit(1)
    else:
        for index, pr in enumerate(projects):
            if index < 10:
                print(index, " | ",pr,flush=True)
            else:
                print(index, "| ",pr,flush=True)
        #choice = input("Choose a project: ")
        choice = getInput(len(projects))
        if type(choice) != int and (int(choice) < 0 or int(choice) > len(projects) - 1):
            print("You introduced the wrong number, going with the first result",flush=True)
            path.insert(0, './Projects/{0}/'.format(projects[0]))
        else:
            add_imports(projects[int(choice)])
            path.insert(0, './Projects/{0}/'.format(projects[int(choice)]))
    if len(ignored_projects) != 0:
        print("Some Projects have been ignored due to \'Sketch.py\' not being present. Here\'s the list",flush=True)
        for index,data in enumerate(ignored_projects):
            print(index,data)
    print("---------------------------------------------------------------------------------------------------",flush=True)
    return projects[int(choice)]
    
if __name__ == "__main__":
    SKETCH_NAME = get_sketches()
    from Sketch import *
    INSTANCE = pyDraw(SKETCH_NAME)
    INSTANCE.start()
