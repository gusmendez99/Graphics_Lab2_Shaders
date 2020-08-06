"""
    Universidad del Valle de Guatemala
    Gustavo Mendez - 18500

    main.py - simple main file to create bmp files (render)
"""

from gl import Render

render = Render()
#render.load("./sphere.obj", translate=(400, 400, 0), scale=(600, 600, 1000))
render.load("./ring.obj", translate=(400, 400, 0), scale=(200, 70, 300))
render.load("./sphere.obj", translate=(400, 400, 0), scale=(300, 300, 300))
# Testing flat shading
# render.triangle(V3(10, 10, 1), V3(1000, 700, 1), V3(1000, 10, 1), color=gl_color.color(255, 0, 0))
render.glFinish(filename="planet.bmp")
