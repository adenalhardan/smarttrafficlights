from random import *

from car import Car

class Traffic:
    cars = []
    nodes = {}

    def __init__(self, batchSize, mapLength, mapHeight, map, canvas, CARSIZE):
        self.batchSize = batchSize

        self.mapLength = mapLength
        self.mapHeight = mapHeight
        self.map = map

        self.canvas = canvas

        self.CARSIZE = CARSIZE

    def quantizeNodes(self):
        n = 0

        for i in range(self.mapLength):
            for j in range(self.mapHeight):
                if self.map[i][j] == 'S':
                    self.nodes[n] = (i, j)
                    n += 1

        return n

    def getCarNodes(self, n):
        while True:
            spawn = randint(0, n)
            end = randint(0, n)

            if spawn != end:
                break

        return spawn, end

    def buildCars(self):
        n = self.quantizeNodes()

        for i in range(self.batchSize):
            spawn, end = self.getCarNodes(n)
            self.cars.append(Car(spawn, end, self.nodes, self.mapLength, self.mapHeight, self.map, self.canvas, self.CARSIZE))

    def drawCars(self):
        for i in range(self.batchSize):
            self.cars[i].draw()
