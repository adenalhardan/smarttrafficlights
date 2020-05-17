from Tkinter import *
from PIL import Image, ImageTk

from timer import *
import constants as c
import images as img

class Light:
    def eliminateStates(self, states):
        directions = []
        validStates = []

        for i in range(4):
            if self.map[c.add(self.node, c.steps[i])] == c.road(i):
                directions.append(i)

        for i in range(6):
            if c.stateDirections[i][0] in directions and c.stateDirections[i][1] in directions:
                validStates.append(states[i])
            else:
                validStates.append(0)

        return validStates

    def updateImage(self):
        if self.state == 0:
            self.canvas.create_image(self.node[0] * c.nodeSize, self.node[1] * c.nodeSize, image = img.get('horizontalLight'), anchor = NW)
        elif self.state == 1:
            self.canvas.create_image(self.node[0] * c.nodeSize, self.node[1] * c.nodeSize, image = img.get('verticalLight'), anchor = NW)
        elif self.state == 2:
              self.canvas.create_image(self.node[0] * c.nodeSize, self.node[1] * c.nodeSize, image = img.get('neCornerLight'), anchor = NW)
        elif self.state == 3:
            self.canvas.create_image(self.node[0] * c.nodeSize, self.node[1] * c.nodeSize, image = img.get('seCornerLight'), anchor = NW)
        elif self.state == 4:
            self.canvas.create_image(self.node[0] * c.nodeSize, self.node[1] * c.nodeSize, image = img.get('swCornerLight'), anchor = NW)
        elif self.state == 5:
            self.canvas.create_image(self.node[0] * c.nodeSize, self.node[1] * c.nodeSize, image = img.get('nwCornerLight'), anchor = NW)

    def updateState(self):
        if self.state == 5:
            self.state = 0
        else:
            self.state += 1

        while self.states[self.state] == 0:
            if self.state == 5:
                self.state = 0
            else:
                self.state += 1


        self.updateImage()

        self.timer = Timer(self.states[self.state], self.updateState)

    def __init__(self, node, states, map, canvas):
        self.node = node
        self.map = map

        self.canvas = canvas

        self.states = self.eliminateStates(states)

        self.state = 0

        while self.states[self.state] == 0:
            if self.state == 5:
                self.state = 0
            else:
                self.state += 1

        self.updateImage()

        self.timer = Timer(self.states[self.state], self.updateState)
