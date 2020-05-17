from random import *

import constants as c
import images as img

class LightOptimizer:
    def __init__(self, positions, epsilon, speed):
        self.positions = positions
        self.epsilon = epsilon
        self.speed = speed

        self.n = len(positions)

        self.states = {}

        for i in range(self.n):
            self.states[self.positions[i]] = [c.defaultLightState for j in range(6)]

        self.q = [[[0, 0] for i in range(6)] for j in range(self.n)]

        self.action = [0, 0, 0]

        self.oldMean = 0
        self.newMean = 0

    def validAction(self, light, state, operation):
        if operation == 0:
            if self.states[self.positions[light]][state] <= 1:
                return False
        elif operation == 1:
            if self.states[self.positions[light]][state] >= c.maxLightState:
                return False

        return True

    def maxQAction(self):
        max = [0, 0, 0]

        for i in range(self.n):
            for j in range(6):
                for k in range(2):
                    if self.q[i][j][k] > self.q[max[0]][max[1]][max[2]]:
                        max = [i, j, k]

        return max


    def performAction(self, newMean):
        self.oldMean = self.newMean
        self.newMean = newMean

        self.q[self.action[0]][self.action[1]][self.action[2]] = self.oldMean - self.newMean

        if random() < self.epsilon:
            light = randint(0, self.n - 1)
            state = randint(0, 5)
            operation = randint(0, 1)
        else:
            light, state, operation = self.maxQAction()

        if self.validAction(light, state, operation):
            self.action = (light, state, operation)

            if operation == 0:
                self.states[self.positions[light]][state] -= 1
            elif operation == 1:
                self.states[self.positions[light]][state] -= 1

            print(str(self.action) + ': ' + str(self.states[self.positions[light]][state]))
