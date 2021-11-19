# Copyright: Sandesh Banskota 2021
# Contains classes and methods needed to represent robotic arm motions and abstractions

import math

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

        self.vertexPositions = []
        self.angles = []


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
        self.vertexPositions = []
        
        position = []
        globalAngle = 0
        for link in self.listOfLinkObjects:
            if (link.prev == None):
                globalAngle = link.getLocalAngle()
                link.setGlobalAngle(globalAngle)
                position = [link.getRadius()*math.cos(link.getGlobalAngle()), link.getRadius()*math.sin(link.getGlobalAngle())]
                link.setVertexLocation(position)
                self.vertexPositions.append(position)
            else:
                # update global angle to include previous angle
                print("here")
                print(globalAngle)
                globalAngle += link.getLocalAngle()
                link.setGlobalAngle(globalAngle)
                print(globalAngle)

                position = [sum(x) for x in zip(position, [link.getRadius()*math.cos(link.getGlobalAngle()), link.getRadius()*math.sin(link.getGlobalAngle())])]
                link.setVertexLocation(position)
                self.vertexPositions.append(position)
        
        return self.vertexPositions
    
    def getLocalAngles(self):
        self.angles = []
        for link in self.listOfLinkObjects:
            self.angles.append(link.getLocalAngle())
        return self.angles


    def getLinks(self):
        return self.listOfLinkObjects

    def printLinks(self):
        for links in self.listOfLinkObjects:
            print(links)

    # def getSolutionToTarget(self, xyCoord):
    #     numOfVertex = len(self.vertexPositions)
    #     i = numOfVertex - 1

    #     while (i > 0):
    #         if (self.vertexPositions[i] 


    #     if i < len(points) - 2:
    #         endpoint = solve_ik(i+1, endpoint, target)
    #     current_point = points[i]

    #     angle = (endpoint-current_point).angle_to(target-current_point)
    #     angles[i] += angle

    #     return current_point + (endpoint-current_point).rotate(angle)
