nodeSize = 50
carSize = int(nodeSize / 3) - 2

speed = 1

north = 0
east = 1
south = 2
west = 3

steps = [(0, -1), (1, 0), (0, 1), (-1, 0), (0, 0)]

offsets = [(6 + (nodeSize / 2), 0), (0, 6 + (nodeSize / 2)), (4, 0), (0, 4)]

linearCases = {'H': (1, 3), 'V': (0, 2), '1': (2, 3), '2': (1, 0), '3': (0, 3), '4': (2, 1)}

stateDirections = [(1, 3), (0, 2), (0, 1), (2, 1), (2, 3), (0, 3)]
stateCases = {0: (1, 3), 1: (0, 2), 2: (3, 0, 2, 1), 3: (0, 1, 3, 2), 4: (0, 3, 1, 2), 5: (1, 0, 2, 3)}

defaultLightState = 100
maxLightState = 500

optimizingConditions = (300, 20)

def add(a, b):
    return tuple(sum(i) for i in zip(a, b))

def road(direction):
    if direction in [0, 2]:
        return 'V'
    elif direction in [1, 3]:
        return 'H'

def opp(direction):
    if direction == 0:
        return 2
    elif direction == 1:
        return 3
    elif direction == 2:
        return 0
    elif direction == 3:
        return 1
