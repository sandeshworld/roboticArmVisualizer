# !/usr/bin/env python3

# Copyright: Sandesh Banskota 2021
# Built for fun & independently to apply things I am learning in a Robotic Manipulations Course 
# While trying to visualize the linkages working within angular constraints for assignments,
# I had a hard time finding a tool to create a view movement of custom linkages, so I built this tool
# to allow user to create custom links (length, min & max angles, initial angle) and to modify the angle
# for each point.

# In the future, I would like to work on a few things.
#
# TODO: Further Things to improve on
# Display Local Link Angle Under Each Link Created
# Display Cartesian Coordinate for Each Location
# Add a button to print out vertex angle at each link and respective cartesian coordinate in a CSV file
# add a desired target location to UI (w/ a marker indicating the spot)
# apply a static inverse kinematic solver button, and find a solution to reach the location within the angle constraints 
# develop a static inverse kinematic solver
# Add a kinetics + velocity mode to allow velocity based position control


# from graphics import *
# coding for 2d for now
from tkinter import Tk, Canvas, Button, Frame, BOTH, BOTTOM, Scale, LEFT, Entry, TOP, END, Label, RIGHT

from roboticLinks import *


import math
from tkinter.constants import ALL

screenWidth = 800
screenHeight = 800

deg2rad = math.pi / 180.0

rad2deg = 1.0/deg2rad


class Example(Frame):
    def __init__(self, roboticArm):
        super().__init__()
        
        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)

        self.height = 300
        self.width = 100
        
        # the new link creation box
        self.newLinkInput(self).place(x=0, y=0)

        # object get solution to target box
        self.createTargetInput(self).place(x=screenWidth-int(self.width*1.5), y=0)

        # input.getCanvasObject().place(x=input.width/2, y=screenHeight/2)
        self.roboticArm = roboticArm
        self.links = []
        self.positions = []

        # keeping track of dynamically created buttons to get rid of them later
        self.buttonsList = []
        
        # possible to pass in links programatically
        # link1 = Link(100, 90, minMaxAngles={'maxAngle': 90, 'minAngle': 0}, deg=True)
        # link2 = Link(100, 0, minMaxAngles={'maxAngle': 180, 'minAngle': 0}, deg=True)
        # link3 = Link(50, 90, minMaxAngles={'maxAngle': 90, 'minAngle': 0}, deg=True)
        # self.links = [link1, link2, link3]

        self.links = []
        for i in self.links:
            self.roboticArm.addLink(i)

        self.xTargetVal = 0
        self.yTargetVal = 0
        self.targetSet = False

        # self.positions = self.roboticArm.calculateVertexPositions()
        self.initUI()

    # creates the top left new link creation box
    def newLinkInput(self,root):
        self.myCanvas = Canvas(root, bg="white", height=self.height, width=self.width)

        button = Button(self.myCanvas, text="Add Link", command=self.callbackFromLinkCreate)
        # button.pack(x=self.width/2, y=self.height-35)
        button.pack(side=BOTTOM)
        
        label = Label(self.myCanvas, text="New Link Parameters")
        label.pack(side=TOP)

        self.lengthCanvas = Canvas(self.myCanvas, bg="white")
        Label(self.lengthCanvas, text="length (cm)").pack(side=LEFT)
        self.length = Entry(self.lengthCanvas, width=8)
        self.length.insert(END, '100')
        self.length.pack(side=RIGHT)
        self.lengthCanvas.pack(side=TOP)

        self.minMaxCanvas = Canvas(self.myCanvas, bg="white")
        Label(self.minMaxCanvas, text="min \u03B8, max \u03B8").pack(side=LEFT)
        self.entryRange = Entry(self.minMaxCanvas, width=8)
        self.entryRange.insert(END, '0, 180')
        self.entryRange.pack(side=RIGHT)
        self.minMaxCanvas.pack(side=TOP)

        self.currentAngCanvas = Canvas(self.myCanvas,bg="white")
        Label(self.currentAngCanvas, text="Initial \u03B8  ").pack(side=LEFT)
        self.entryAngle = Entry(self.currentAngCanvas, width=11)
        self.entryAngle.insert(END, '5')
        self.entryAngle.pack(side=RIGHT)
        self.currentAngCanvas.pack(side=TOP)

        return self.myCanvas

    # mostly done -> to do, get the 
    # will implement to a tolerance calculated by threshold > sqrt((goalx-reachx)^2 + (goalx - reachx)^2)
    def createTargetInput(self,root):
        myCanvas = Canvas(root, bg="white", height=self.height, width=self.width)
        
        button = Button(myCanvas, text="Place Target", command=self.callbackFromTargetCreate)
        # button.pack(x=self.width/2, y=self.height-35)
        button.pack(side=BOTTOM)
        
        label = Label(myCanvas, text="Set Target For Arm")
        label.pack(side=TOP)

        self.xTargetCanvas = Canvas(myCanvas, bg="white")
        Label(self.xTargetCanvas, text="x (cm)").pack(side=LEFT)
        self.xTarget = Entry(self.xTargetCanvas, width=8)
        self.xTarget.insert(END, '100')
        self.xTarget.pack(side=RIGHT)
        self.xTargetCanvas.pack(side=TOP)

        self.yTargetCanvas = Canvas(myCanvas, bg="white")
        Label(self.yTargetCanvas, text="y (cm)").pack(side=LEFT)
        self.yTarget = Entry(self.yTargetCanvas, width=8)
        self.yTarget.insert(END, '50')
        self.yTarget.pack(side=RIGHT)
        self.yTargetCanvas.pack(side=TOP)

        return myCanvas

    def callbackFromLinkCreate(self):
        print("New Link Created")

        inputEntryRange = self.entryRange.get()
        minMaxValue = {'maxAngle': 0, 'minAngle': 0}
        inputEntryAngle = 0

        if inputEntryRange == "":
            minMaxValue = None
        else:
            try:
                splitInput = inputEntryRange.split(",")
                if (len(splitInput) != 2):
                    return None
                else:
                    minMaxValue['minAngle'] = float(splitInput[0])
                    minMaxValue['maxAngle'] = float(splitInput[1])
            except:
                return None
        
        try:
            inputEntryAngle = float(self.entryAngle.get())
        except:
            return None

        try:
            length = float(self.length.get())
        except:
            return None

        link = Link(length, inputEntryAngle, minMaxAngles=minMaxValue, deg=True)

        # reset screen after adding link
        self.roboticArm.addLink(link)
        # self.canvas.delete(ALL)

        for b in self.buttonsList:
            print("Button Found & Deleting")
            b.place_forget()

        self.canvas.delete('all')
        self.initUI()
        
    def callbackFromTargetCreate(self):
        print("New Link Created")

        xTarget = self.xTarget.get()
        yTarget = self.yTarget.get()
        minMaxValue = {'maxAngle': 0, 'minAngle': 0}
        inputEntryAngle = 0

        try:
            xTarget = float(self.xTarget.get())
        except:
            return None
        
        try:
            yTarget = float(self.yTarget.get())
        except:
            return None

        

        # create a target
        self.xTargetVal = xTarget + screenWidth/2
        self.yTargetVal = screenHeight/2 - yTarget
        self.targetSet = True

        for b in self.buttonsList:
            print("Button Found & Deleting")
            b.place_forget()

        self.canvas.delete('all')
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
        
        # for link in self.links:
        #         print("Adding: ")
        #         print(link)
        #         self.roboticArm.addLink(link)

        self.links = self.roboticArm.getLinks()
        index = 0
        numLinks = len(self.links)
        
        for link in self.links:
            identifier = str(index)
            b1 = Button(self.canvas, text="+ \u03B8", command=lambda x=link: self.callbackFuncInc(x))
            b1.place(x=index*(screenWidth/numLinks)+20, y=screenHeight-65)
            b2 = Button(self.canvas, text="- \u03B8", command=lambda x=link: self.callbackFuncDec(x))
            b2.place(x=index*(screenWidth/numLinks)+20, y=screenHeight-35)
            self.buttonsList.append(b1)
            self.buttonsList.append(b2)
            index += 1

        self.positions = self.roboticArm.calculateVertexPositions()

        self.angles = self.roboticArm.getLocalAngles()

        if (numLinks > 0):
            # create the target
            if self.targetSet:
                # self.canvas.create_text(self.xTargetVal+3, self.yTargetVal+3, self.xTargetVal-3, self.yTargetVal-3, fill='blue')
                self.canvas.create_text(self.xTargetVal, self.yTargetVal, text="X", font=20, fill='blue')

            self.canvas.create_text(screenWidth/2, 20, text="End Effector [x,y]: [" + 
            str(round(self.positions[-1][0],4)) + ", " + str(round(self.positions[-1][1],4)) + "] cm", font=20, fill='black')


        colors = ['black', 'green', 'blue', 'yellow', 'red','orange']
        for i in range(len(self.links)):
            #handling if more links than color
            if i > (len(colors) - 1):
                color = colors[len(colors) - 1]
            else:
                color = colors[i]

            width = 2

            # create the labels that will be destroyed
            self.canvas.create_text(i*(screenWidth/numLinks)+45, screenHeight-90, text="Link " + str(i) + '\u03B8')
            self.canvas.create_text(i*(screenWidth/numLinks)+45, screenHeight-75, text='\u03B8 =' + str(round(self.angles[i]*rad2deg, 3)))

            screenX = self.positions[i][0] + screenWidth/2
            screenY = screenHeight/2 - self.positions[i][1]
            if i == 0:
                # representing base as black
                self.canvas.create_oval(screenWidth/2+5, screenHeight/2+5, screenWidth/2-5, screenHeight/2-5, fill='black')
                self.canvas.create_line(screenWidth/2, screenHeight/2, screenX, screenY, width=width, fill=color)

            else:
                prevScreenX = self.positions[i-1][0] + screenWidth/2
                prevScreenY = screenHeight/2 - self.positions[i-1][1]
                # create the joints
                self.canvas.create_oval(prevScreenX+3, prevScreenY+3, prevScreenX-3, prevScreenY-3, fill='red')

                #create the lines
                self.canvas.create_line(prevScreenX, prevScreenY, screenX, screenY, width=width, fill=color)

            # representing grabber as yellow
            if (i == (numLinks - 1)):
                self.canvas.create_oval(screenX+5, screenY+5, screenX-5, screenY-5, fill='yellow')

        self.canvas.pack(fill=BOTH, expand=1)
        # self.canvas.place(x=0,y=0)
        


def main():
    root = Tk()

    origin = (0, 0)
    roboticArm = RoboticLinks(origin)

    ex = Example(roboticArm)

    # root.geometry("400x250+300+300")
    root.geometry(str(screenWidth) + "x" + str(screenHeight))
    root.resizable(width=False, height=False)
    root.title("Robotic Arm Kinematics 2D")
    root.mainloop()

main()