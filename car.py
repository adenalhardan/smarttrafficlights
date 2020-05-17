from Tkinter import *
from PIL import Image, ImageTk

import copy

import constants as c
import images as img

class Car:
    def __init__(self, id, app, spawnNode, endNode, map, canvas):
        self.id = id
        self.app = app

        self.spawnNode = spawnNode
        self.endNode = endNode

        self.map = map

        self.path = {}

        self.canvas = canvas

        self.isTurning = False

        self.time = 0

        self.ended = False

        for i in range(4):
            if self.map[c.add(self.spawnNode, c.steps[i])] == c.road(i):
                self.direction = i

                self.x = (self.spawnNode[0] * c.nodeSize) + c.offsets[i][0]
                self.y = (self.spawnNode[1] * c.nodeSize) + c.offsets[i][1]

                if i == 0:
                    self.y += (c.nodeSize - c.carSize)
                elif i == 3:
                    self.x += (c.nodeSize - c.carSize)

        self.canvasObject = self.canvas.create_image(self.x, self.y, image = img.get('car'), anchor = NW)

        self.path = self.findPath(self.spawnNode, self.direction, self.path)

    def end(self):
        self.canvas.delete(self.canvasObject)
        self.app.endCar(self.id, self.time)
        self.ended = True

    def getNode(self, x = None, y = None):
        if x is None and y is None:
            return (int(self.canvas.coords(self.canvasObject)[0] / c.nodeSize), int(self.canvas.coords(self.canvasObject)[1] / c.nodeSize))
        else:
            return (int(x / c.nodeSize), int(y / c.nodeSize))

    def getNextNode(self, direction):
        if direction in [0, 3]:
            coords = (self.x + (c.steps[direction][0] * c.speed), self.y + (c.steps[direction][1] * c.speed))
        elif direction == 1:
            coords = (self.x + (c.steps[direction][0] * c.speed) + c.carSize, self.y + (c.steps[direction][1] * c.speed))
        elif direction == 2:
            coords = (self.x + (c.steps[direction][0] * c.speed), self.y + (c.steps[direction][1] * c.speed) + c.carSize)

        return self.getNode(coords[0], coords[1])

    def turn(self):
        conditions = [False, False, False, False]

        if self.map[self.getNode()] not in ['L', '1', '2', '3', '4']:
            conditions[0] = self.y > ((self.getNextNode(self.path[self.getNode()])[1] * c.nodeSize) + c.offsets[self.path[self.getNextNode(self.path[self.getNode()])]][1])
            conditions[1] = self.x < ((self.getNextNode(self.path[self.getNode()])[0] * c.nodeSize) + c.offsets[self.path[self.getNextNode(self.path[self.getNode()])]][0])
            conditions[2] = self.y < ((self.getNextNode(self.path[self.getNode()])[1] * c.nodeSize) + c.offsets[self.path[self.getNextNode(self.path[self.getNode()])]][1])
            conditions[3] = self.x > ((self.getNextNode(self.path[self.getNode()])[0] * c.nodeSize) + c.offsets[self.path[self.getNextNode(self.path[self.getNode()])]][0])

        elif self.map[self.getNode()] in ['L', '1', '2', '3', '4']:
            conditions[0] = self.y - c.speed > ((self.getNode()[1] * c.nodeSize) + c.offsets[self.path[self.getNode()]][1])
            conditions[1] = self.x + c.speed < ((self.getNode()[0] * c.nodeSize) + c.offsets[self.path[self.getNode()]][0])
            conditions[2] = self.y + c.speed < ((self.getNode()[1] * c.nodeSize) + c.offsets[self.path[self.getNode()]][1])
            conditions[3] = self.x - c.speed > ((self.getNode()[0] * c.nodeSize) + c.offsets[self.path[self.getNode()]][0])

        if conditions[self.direction]:
            self.canvas.move(self.canvasObject, c.steps[self.direction][0] * c.speed, c.steps[self.direction][1] * c.speed)
        else:
            self.isTurning = False

    def move(self):
        self.canvas.tag_raise(self.canvasObject)

        if self.getNextNode(self.direction) in self.path and self.app.collision(self.id) == False:
            if self.direction != self.path[self.getNextNode(self.direction)]:
                self.isTurning = True

            if self.map[self.getNextNode(self.direction)] == 'L':
                if (self.map[self.getNode()] != 'L' and self.app.checkLight(self.id, self.getNextNode(self.direction)) == True) or self.map[self.getNode()] == 'L':
                    if self.isTurning == True:
                        self.turn()
                    else:
                        self.canvas.move(self.canvasObject, c.steps[self.direction][0] * c.speed, c.steps[self.direction][1] * c.speed)

            elif self.map[self.getNextNode(self.direction)] in ['1', '2', '3', '4']:
                if self.isTurning == True:
                    self.turn()
                else:
                    self.canvas.move(self.canvasObject, c.steps[self.direction][0] * c.speed, c.steps[self.direction][1] * c.speed)

            elif self.map[self.getNextNode(self.direction)] in ['H', 'V', 'S']:
                if self.getNode() == self.endNode:
                    self.end()

                self.canvas.move(self.canvasObject, c.steps[self.direction][0] * c.speed, c.steps[self.direction][1] * c.speed)

    def update(self):
        self.time += 1

        self.x = self.canvas.coords(self.canvasObject)[0]
        self.y = self.canvas.coords(self.canvasObject)[1]

        if self.getNode() in self.path and self.isTurning == False:
            self.direction = self.path[self.getNode()]

        self.move()

    def findPath(self, node, direction, path):
        path = copy.deepcopy(path)

        while self.map[c.add(node, c.steps[direction])] in c.linearCases:
            i = c.linearCases[self.map[c.add(node, c.steps[direction])]]

            if direction == i[0]:
                path[node] = direction
                node = c.add(node, c.steps[direction])

                if self.map[node] in ['1', '2', '3', '4']:
                    direction = c.opp(i[1])

            elif direction == i[1]:
                path[node] = direction
                node = c.add(node, c.steps[direction])

                if self.map[node] in ['1', '2', '3', '4']:
                    direction = c.opp(i[0])

        if self.map[c.add(node, c.steps[direction])] == 'L':
            path[node] = direction
            node = c.add(node, c.steps[direction])

            if node in path:
                return {}
            else:
                paths = [{}, {}, {}, {}]
                minPath = {}

                for i in range(4):
                    if self.map[c.add(node, c.steps[i])] == c.road(i) and c.add(node, c.steps[i]) not in path:
                        paths[i] = self.findPath(node, i, path)

                for i in range(4):
                    if self.endNode not in paths[i]:
                       paths[i] = {}

                for i in range(4):
                    if paths[i] != {}:
                        minPath = paths[i]

                if minPath != {}:
                    for i in range(4):
                        if paths[i] != {} and len(paths[i]) < len(minPath):
                            minPath = paths[i]

                path.update(minPath)
                return path

        elif self.map[c.add(node, c.steps[direction])] == 'S':
            path[node] = direction
            node = c.add(node, c.steps[direction])

            if node == self.endNode:
                path[node] = direction
                return path
            else:
                return {}

    def __del__(self):
        print('car gone')
