"""
    Universidad del Valle de Guatemala
    Gustavo Mendez - 18500

    main.py - simple main file to create bmp files (render)
"""

from gl import Render
from utils.constants import *

render = Render()
render.load("./ring.obj", translate=(400, 400, 0), scale=(220, 75, 200), shape=RING)
render.load("./sphere.obj", translate=(400, 400, 0), scale=(250, 250, 350), shape=PLANET)
render.finish(filename="saturn.bmp")
