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

if "Logs" not in listdir("."):
    mkdir("Logs")

if "log {}.bin".format(strftime("%d-%m-%Y")) not in listdir("./Logs"):
    open("./Logs/log {}.bin".format(strftime("%d-%m-%Y")),"w").write("")

if "Sounds" not in listdir("."):
    mkdir("Sounds")

if "Images" not in listdir("."):
    mkdir("Images")

log.basicConfig(filename="Logs/log {}.bin".format(strftime("%d-%m-%Y")),level=log.DEBUG)

#path.insert(0,'pyDraw/')
class pyDraw:

    __version__ = 0.11

    def __init__(self, sketch):
        self.start_time = time()
        self.current_time = self.start_time
        self.setup_flag = False
        self.draw_flag = False
        self.hold = False
        log.info("Checked for updates at {0}".format(strftime("%Hh%Mm")))
        pygame.init()
        self.count = 0
        pygame.display.init()
        pygame.display.set_icon(pygame.image.load("pyDraw.ico"))
        d = pre()
        if d == None:
            log.warning("The method \'pre()\' must be used to define the window dimensions")
            raise Warning("To create a window you must use the CreateCanvas(width,height) method inside the pre() method")
        else:
            self.width = d.width
            self.height = d.height
        environ['WIDTH'] = str(self.width)
        environ['HEIGHT'] = str(self.height)
        self.screen = pygame.display.set_mode([self.width, self.height])
        setScreen(self.screen, self.width, self.height)
        log.info("Screen set - {}x{}".format(self.width,self.height))
        try:
            update()
            setup()
        except Exception as err:
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
                print(ThdMng.length)
                if ThdMng.length != 0:
                    ThdMng.dispose_all()
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

    def start(self):
        while not self.spin():
            try:
                if not noLoop.flag:
                    self.draw()
                    clock.tick(120)
                    FRAMECOUNT.add(1)
                    if floor(time() - self.current_time) >= 0.6:
                        self.current_time = time()
                        ThdMng.search()
                else:
                    continue
            except (KeyboardInterrupt):
                print("\nExiting...")
                onExit()
                if ThdMng.length != 0:
                    ThdMng.dispose_all()
                del self
                exit(0)

def get_sketches():

    def getInput(length):
        choice = ""
        try:
            choice = input("Choose a project: ")
            if int(choice) > length-1 or int(choice) < 0 or choice is None or choice is "":
                raise Exception
        except Exception:
            choice = getInput(length)
        return choice

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
