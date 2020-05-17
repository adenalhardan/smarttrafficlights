from Tkinter import *
from PIL import Image, ImageTk

import constants as c

images = {
    'horizontalRoad': ['roadimage.png', c.nodeSize, c.nodeSize, 0, None],
    'verticalRoad': ['roadimage.png', c.nodeSize, c.nodeSize, -90, None],

    'undefined': ['undefinedimage.png', c.nodeSize, c.nodeSize, 0, None],
    'light': ['lightimage.png', c.nodeSize, c.nodeSize, 0, None],
    'spawn': ['spawnimage.png', c.nodeSize, c.nodeSize, 0, None],

    'neCorner': ['cornerimage.png', c.nodeSize, c.nodeSize, 0, None],
    'seCorner': ['cornerimage.png', c.nodeSize, c.nodeSize, -90, None],
    'swCorner': ['cornerimage.png', c.nodeSize, c.nodeSize, -180, None],
    'nwCorner': ['cornerimage.png', c.nodeSize, c.nodeSize, -270, None],

    'car': ['carimage.png', c.carSize, c.carSize, 0, None],

    'horizontalLight': ['straightlightimage.png', c.nodeSize, c.nodeSize, 0, None],
    'verticalLight': ['straightlightimage.png', c.nodeSize, c.nodeSize, -90, None],

    'neCornerLight': ['cornerlightimage.png', c.nodeSize, c.nodeSize, 0, None],
    'seCornerLight': ['cornerlightimage.png', c.nodeSize, c.nodeSize, -90, None],
    'swCornerLight': ['cornerlightimage.png', c.nodeSize, c.nodeSize, -180, None],
    'nwCornerLight': ['cornerlightimage.png', c.nodeSize, c.nodeSize, -270, None],
}

def get(name):
    if name in images:
        if images[name][4] is None:
            images[name][4] = ImageTk.PhotoImage(Image.open(images[name][0]).rotate(images[name][3]).resize((images[name][1], images[name][2]), Image.NEAREST))

        return images[name][4]

    else:
        return None
