# !/usr/bin/env python3

# Copyright: Sandesh Banskota 2021

# from graphics import *
# coding for 2d for now
from tkinter import Tk, Canvas, Button, Frame, BOTH, BOTTOM

import math
from tkinter.constants import ALL

screenWidth = 800
screenHeight = 800

deg2rad = math.pi / 180.0

class Link:
    # should return
    def __str__(self):
        return ("radius: " + str(self.radius) + "\n"
              + "(Min, Max Angles): (" + str(self.minAngle) + ", " + str(self.maxAngle) + ")\n"
              + "Local Angle: " + str(self.currentLocalAngle) + "\n"
              + "Global Angle: " + str(self.currentGlobalAngle) + "\n"
              + "Vertex Position: " + str(self.vertexLocation) + "\n"
              )

    def __init__(self, radius, localAngle, minMaxAngles=None, deg=False) -> None:
        self.radius = radius

        # in a dictionary format so in the future can change it to work with 3d
        if minMaxAngles == None:
            self.minAngle = -math.inf
            self.maxAngle = math.inf
        else:
            self.minAngle = minMaxAngles['minAngle']
            self.maxAngle = minMaxAngles['maxAngle']

        self.next = None
        self.prev = None

        self.currentLocalAngle = None
        self.currentGlobalAngle = None
        
        self.vertexLocation = None

        if deg:
            self.setLocalAngle(localAngle, deg=True)
        else:
            self.setLocalAngle(localAngle)
    
    # relative angle at the joint
    def setLocalAngle(self, angle, deg=False):
        # if it is the first link, global will be the same
        # print("just something to not throw error")

        # in the future can add something here so if a particular link angle is changed,
        # all global angles after this link are changed
        

        if deg:
            # ensuring the angle does not exceed the limits
            angle =  self.minAngle if (angle < self.minAngle) else angle
            angle = self.maxAngle if (angle > self.maxAngle) else angle

            self.currentLocalAngle = angle * deg2rad
        else:
            # ensuring the angle does not exceed the limits
            angle =  (deg2rad * self.minAngle) if (angle < self.minAngle*deg2rad) else angle
            angle = (deg2rad * self.maxAngle) if (angle > self.maxAngle*deg2rad) else angle

            self.currentLocalAngle = angle

    def setGlobalAngle(self, angle):
        self.currentGlobalAngle = angle

    def setVertexLocation(self, location):
        self.vertexLocation = location

    def getVertexLocation(self):
        return self.vertexLocation

    def getLocalAngle(self):
        return self.currentLocalAngle

    def getGlobalAngle(self):
        return self.currentGlobalAngle

    def getRadius(self):
        return self.radius

class RoboticLinks:
    def __init__(self, origin) -> None:
        # store for whether dealing with 2d or 3d link problem
        self.dim = 0
        if len(origin) == 2:
            self.dim = 2
        elif len(origin) == 3:
            self.dim = 3
        else:
            return ValueError

        # instantiating link
        self.listOfLinkObjects = []

        self.lastLink = None
        self.baseLink = None

    def addLink(self, link):
        if (self.baseLink == None):
            self.baseLink = link
            self.lastLink = link
            self.listOfLinkObjects.append(link)
        else:
            link.prev = self.lastLink
            self.lastLink.next = link
            self.lastLink = link
            self.listOfLinkObjects.append(link)

    def calculateVertexPositions(self):
        # will store value of each vertex
        vertexPositions = []
        
        position = []
        globalAngle = 0
        for link in self.listOfLinkObjects:
            if (link.prev == None):
                globalAngle = link.getLocalAngle()
                link.setGlobalAngle(globalAngle)
                position = [link.getRadius()*math.cos(link.getGlobalAngle()), link.getRadius()*math.sin(link.getGlobalAngle())]
                link.setVertexLocation(position)
                vertexPositions.append(position)
            else:
                # update global angle to include previous angle
                print("here")
                print(globalAngle)
                globalAngle += link.getLocalAngle()
                link.setGlobalAngle(globalAngle)
                print(globalAngle)

                position = [sum(x) for x in zip(position, [link.getRadius()*math.cos(link.getGlobalAngle()), link.getRadius()*math.sin(link.getGlobalAngle())])]
                link.setVertexLocation(position)
                vertexPositions.append(position)
        
        return vertexPositions

    def getLinks(self):
        return self.listOfLinkObjects

    def printLinks(self):
        for links in self.listOfLinkObjects:
            print(links)


class Example(Frame):

    def __init__(self, roboticArm):
        super().__init__()
        self.roboticArm = roboticArm
        self.positions = []


        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)

        self.links = self.roboticArm.getLinks()
        index = 0
        numLinks = len(self.links)
        for link in self.links:
            identifier = str(index)
            Button(self, text="Inc." + str(index), command=lambda x=link: self.callbackFuncInc(x)).place(x=index*(screenWidth/numLinks)+20, y=screenHeight-65)
            Button(self, text="Dec." + str(index), command=lambda x=link: self.callbackFuncDec(x)).place(x=index*(screenWidth/numLinks)+20, y=screenHeight-35)
            index += 1


        # self.positions = self.roboticArm.calculateVertexPositions()
        self.initUI()


    def callbackFuncInc(self,link):
        print("increase pressed for " + str(link.getLocalAngle()))
        link.setLocalAngle(link.currentLocalAngle+5*deg2rad)
        self.canvas.delete(ALL)
        self.initUI()
        # self.positions = self.roboticArm.calculateVertexPositions()

    def callbackFuncDec(self,link):
        print("decrease pressed for " + str(link.getLocalAngle()))
        link.setLocalAngle(link.currentLocalAngle-5*deg2rad)
        self.canvas.delete(ALL)
        
        self.initUI()
        # self.positions = self.roboticArm.calculateVertexPositions()

    def initUI(self):

        self.positions = self.roboticArm.calculateVertexPositions()

        numLinks = len(self.links)
        colors = ['black', 'green', 'blue', 'yellow', 'red','orange']
        for i in range(len(self.links)):
            #handling if more links than color
            if i > (len(colors) - 1):
                color = colors[len(colors) - 1]
            else:
                color = colors[i]

            width = 2

            # create the labels that will be destroyed
            self.canvas.create_text(i*(screenWidth/numLinks)+60, screenHeight-75, text="Link " + str(i) + '\u03B8')

            screenX = self.positions[i][0] + screenWidth/2
            screenY = screenHeight/2 - self.positions[i][1]
            if i == 0:
                self.canvas.create_line(screenWidth/2, screenHeight/2, screenX, screenY, width=width, fill=color)
            else:
                prevScreenX = self.positions[i-1][0] + screenWidth/2
                prevScreenY = screenHeight/2 - self.positions[i-1][1]
                self.canvas.create_line(prevScreenX, prevScreenY, screenX, screenY, width=width, fill=color)
        
        
        self.canvas.pack(fill=BOTH, expand=1)


def main():
    root = Tk()

    origin = (0, 0)
    roboticArm = RoboticLinks(origin)

    
    link1 = Link(100, 90, minMaxAngles={'maxAngle': 90, 'minAngle': 0}, deg=True)
    link2 = Link(100, 0, minMaxAngles={'maxAngle': 180, 'minAngle': 0}, deg=True)
    link3 = Link(50, 90, minMaxAngles={'maxAngle': 90, 'minAngle': 0}, deg=True)

    # add links to object
    links = [link1, link2, link3]
    
    for link in links:
            roboticArm.addLink(link)

    ex = Example(roboticArm)

    # root.geometry("400x250+300+300")
    root.geometry(str(screenWidth) + "x" + str(screenHeight))
    root.resizable(width=False, height=False)
    root.title("Robotic Arm Kinematics 2D")
    root.mainloop()

main()