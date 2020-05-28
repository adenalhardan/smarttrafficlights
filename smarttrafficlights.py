from Tkinter import *
from PIL import Image, ImageTk

from random import *
import time
import math

from car import *
from light import *
from lightoptimizer import *

import constants as c
import images as img

class App:
    def loadMap(self, fileName):
        map = {}

        with open(fileName, "r") as file:
            data = [line.split() for line in file]

            for i in range(len(data)):
                for j in range(len(data[0])):
                    map[(i, j)] = data[i][j]

            return map, len(data), len(data[0])

    def drawMap(self):
        for i in range(self.mapLength):
            for j in range(self.mapHeight):
                if self.map[(i, j)] == 'U':
                    self.canvas.create_image(i * c.nodeSize, j * c.nodeSize, image = img.get('undefined'), anchor = NW)
                elif self.map[(i, j)] == 'S':
                    self.canvas.create_image(i * c.nodeSize, j * c.nodeSize, image = img.get('spawn'), anchor = NW)
                elif self.map[(i, j)] == 'H':
                    self.canvas.create_image(i * c.nodeSize, j * c.nodeSize, image = img.get('horizontalRoad'), anchor = NW)
                elif self.map[(i, j)] == 'V':
                    self.canvas.create_image(i * c.nodeSize, j * c.nodeSize, image = img.get('verticalRoad'), anchor = NW)
                elif self.map[(i, j)] == 'L':
                    self.canvas.create_image(i * c.nodeSize, j * c.nodeSize, image = img.get('light'), anchor = NW)
                elif self.map[(i, j)] == '1':
                    self.canvas.create_image(i * c.nodeSize, j * c.nodeSize, image = img.get('neCorner'), anchor = NW)
                elif self.map[(i, j)] == '2':
                    self.canvas.create_image(i * c.nodeSize, j * c.nodeSize, image = img.get('seCorner'), anchor = NW)
                elif self.map[(i, j)] == '3':
                    self.canvas.create_image(i * c.nodeSize, j * c.nodeSize, image = img.get('swCorner'), anchor = NW)
                elif self.map[(i, j)] == '4':
                    self.canvas.create_image(i * c.nodeSize, j * c.nodeSize, image = img.get('nwCorner'), anchor = NW)
                else:
                    print("Invalid Map Value at (" + str(i) + ", " + str(j) + ')')

    def getCarNodes(self):
        spawn = 0
        end = 0

        while spawn == end:
            spawn = randint(0, len(self.leafNodes) - 1)
            end = randint(0, len(self.leafNodes) - 1)

        return spawn, end

    def buildCar(self):
        spawn, end = self.getCarNodes()

        if self.isSpawnOpen(spawn):
            self.cars.append(Car(len(self.cars), self, self.leafNodes[spawn], self.leafNodes[end], self.map, self.canvas))


    def isSpawnOpen(self, spawn):
        for car in self.cars:
            if car.ended == False and car.spawnNode == self.leafNodes[spawn] and car.getNode() == self.leafNodes[spawn]:
                return False

        return True

    def checkLight(self, id, node):
        car = self.cars[id]
        light = self.lights[node]

        i = c.stateCases[light.state]

        if light.state < 2:
            if car.isTurning == False and car.direction in [i[0], i[1]]:
                return True
            else:
                return False
        else:
            if car.isTurning == True and car.direction == i[0] and car.path[car.getNextNode(car.direction)] == i[1]:
                return True
            elif car.isTurning == True and car.direction == i[2] and car.path[car.getNextNode(car.direction)] == i[3]:
                return True
            else:
                return False

    def updateCars(self):
        for car in self.cars:
            if car.ended == False:
                car.update()

    def updateLights(self):
        for i in range(self.mapLength):
            for j in range(self.mapHeight):
                if (i, j) in self.lights:
                    self.lights[(i, j)].timer.update()
                    self.lights[(i, j)].states = self.optimizer.states[(i, j)]

    def collision(self, id):
        if self.map[self.cars[id].getNextNode(self.cars[id].direction)] == 'S':
            return False

        for car in self.cars:
            if car.ended == False and id != car.id and self.cars[id].direction == car.direction and car.getNode() in [self.cars[id].getNode(), self.cars[id].getNextNode(self.cars[id].direction)]:
                if self.cars[id].direction == 0:
                    if self.cars[id].y > car.y and self.cars[id].y - c.speed <= car.y + c.carSize:
                        return True

                elif self.cars[id].direction == 1:
                    if self.cars[id].x < car.x and self.cars[id].x + c.carSize + c.speed >= car.x:
                        return True

                elif self.cars[id].direction == 2:
                    if self.cars[id].y < car.y and self.cars[id].y + c.carSize + c.speed >= car.y:
                        return True

                elif self.cars[id].direction == 3:
                    if self.cars[id].x > car.x and self.cars[id].x - c.speed <= car.x + c.carSize:
                        return True

        return False

    def endCar(self, id, time):
        self.sum += time
        self.endedCars += 1
        self.mean = self.sum / self.endedCars

        self.meanTimeLabel['text'] = 'Mean Time: ' + str(self.mean)

        if self.optimizing:
            self.statusLabel['text'] = 'Optimizing... (Mean Down by ' + str(self.unomptimizedMean - self.mean) + ')'

    def batchEnded(self):
        for car in self.cars:
            if car.ended == False:
                return False

        return True

    def loop(self):
        try:
            while True:
                if len(self.cars) < self.batchSize:
                    self.buildCar()

                if self.batchEnded():
                    self.batch += 1
                    self.batchLabel['text'] = 'Batch: ' + str(self.batch)

                    self.cars = []

                    if self.optimizing:
                        self.optimizer.performAction(self.mean)
                    else:
                        if self.mean - self.oldMean <= c.optimizingCondition:
                            self.optimizing = True
                            self.unomptimizedMean = self.mean
                        else:
                            self.oldMean = self.mean

                self.updateCars()
                self.updateLights()

                self.window.update()

        except TclError:
            pass

    def __init__(self):
        self.batchSize = 10

        self.cars = []
        self.lights = {}
        self.leafNodes = []

        self.defaultStates = [300, 300, 300, 300, 300, 300]

        self.map, self.mapLength, self.mapHeight = self.loadMap("mapdata.txt")

        self.window = Tk()
        self.window.title("Smart Traffic Lights")
        self.window.geometry(str(self.mapLength * c.nodeSize) + 'x' + str((self.mapHeight + 1) * c.nodeSize))
        self.window.resizable(False, False)

        self.outputFrame = Frame(self.window)
        self.outputFrame.pack(side = TOP)

        self.batch = 0

        self.batchLabel = Label(self.outputFrame, text = 'Batch: 0')
        self.batchLabel.pack(side = TOP)

        self.sum = 0
        self.endedCars = 0
        self.mean = 0

        self.meanTimeLabel = Label(self.outputFrame, text = 'Mean Time:')
        self.meanTimeLabel.pack(side = TOP)

        self.optimizing = False

        self.oldMean = 0
        self.unomptimizedMean = 0

        self.statusLabel = Label(self.outputFrame, text = 'Reaching Stable Mean Time...')
        self.statusLabel.pack(side = TOP)

        self.mapFrame = Frame(self.window)
        self.mapFrame.pack(side = TOP)

        self.canvas = Canvas(self.mapFrame, width = self.mapLength * c.nodeSize, height = self.mapHeight * c.nodeSize)
        self.canvas.pack(side = TOP)

        self.drawMap()

        self.lightPositions = []

        for i in range(self.mapLength):
            for j in range(self.mapHeight):
                if self.map[(i, j)] == 'L':
                    self.lights[(i, j)] = Light((i, j), [c.defaultLightState] * 6, self.map, self.canvas)
                    self.lightPositions.append((i, j))

                elif self.map[(i, j)] == 'S':
                    self.leafNodes.append((i, j))

        self.optimizer = LightOptimizer(self.lightPositions, 0.1, 300)

if __name__ == '__main__':
    app = App()
    app.loop()
