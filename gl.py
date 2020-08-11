"""
    Universidad del Valle de Guatemala
    Gustavo Mendez - 18500

    gl.py - all logic to create a bmp file
"""

from utils.color import color, normalize_color
from utils.math import barycentric, bbox, cross, dot, V2, V3, norm
from utils.encoder import char, dword, word
from utils.constants import PLANET, RING
from math import sqrt

from obj import Obj

BLACK = 0, 0, 0
# Saturn color intervals, up to center
MELON = 136, 195, 222
BROWN = 105, 145, 170
LAVENDER = 156, 152, 164

class Render(object):
    # glInit dont needed, 'cause we have an __init__ func
    def __init__(self):
        self.framebuffer = []
        self.width = 800
        self.height = 800
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_width = 800
        self.viewport_height = 800
        self.clear()

        self.zbuffer = [
            [-float('inf') for x in range(self.width)] for y in range(self.height)
        ]
        # For shader use
        self.shape = None

    def point(self, x, y, color):
        self.framebuffer[y][x] = color

    def create_window(self, width, height):
        self.height = height
        self.width = width

    def viewport(self, x, y, width, height):
        # Setting viewport initial values
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_height = height
        self.viewport_width = width

    def clear(self):
        r, g, b = BLACK
        bg_color = color(r, g, b)
        self.framebuffer = [
            [bg_color for x in range(self.width)] for y in range(self.height)
        ]

    def clear_color(self, r=1, g=1, b=1):
        # get normalized colors as array
        normalized = normalize_color([r, g, b])
        clearColor = color(normalized[0], normalized[1], normalized[2])

        self.framebuffer = [
            [clearColor for x in range(self.width)] for y in range(self.height)
        ]

    def triangle(self, A, B, C):
        xmin, xmax, ymin, ymax = bbox(A, B, C)

        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                P = V2(x, y)
                w, v, u = barycentric(A, B, C, P)
                if w < 0 or v < 0 or u < 0:
                    # point is outside
                    continue

                z = A.z * u + B.z * v + C.z * w

                r, g, b = self.shader(
                    x, y
                )

                shader_color = color(r, g, b)

                if z > self.zbuffer[y][x]:
                    self.point(x, y, shader_color)
                    self.zbuffer[y][x] = z

    def check_ellipse(self, x, y, a, b):
        return round((x ** 2) * (b ** 2)) + ((y ** 2) * (a ** 2)) <= round(a ** 2) * (
            b ** 2
        )

    def radius(self,x,y):
        return int(sqrt(x*x + y*y))

    def shader(self, x=0, y=0):
        # Planet bounds:
        # Y: 275 - 525

        shader_color = BLACK
        current_shape = self.shape

        # For gradient color
        r1, g1, b1 = BLACK
        r2, g2, b2 = BLACK
        percentage = 1

        if current_shape == PLANET:
            if y >= 375 and y <= 425:
                r1, g1, b1 = MELON
                r2, g2, b2 = BROWN
                percentage = abs(y - 400)

            if (y > 325 and y < 375) or (y > 425 and y < 475):
                if y < 450 or y > 350:
                    r1, g1, b1 = MELON
                    r2, g2, b2 = BROWN
                    percentage = abs(y - 400)

                if y >= 450 or y <= 350:
                    r1, g1, b1 = BROWN
                    r2, g2, b2 = LAVENDER
                    if y >= 450:
                        percentage = abs(y - 450)
                    else:
                        percentage = abs(y - 350)

            if (y <= 325 and y >= 260) or (y <= 540 and y >= 475):
                if y < 500 or y > 300:
                    r1, g1, b1 = BROWN
                    r2, g2, b2 = LAVENDER                    
                    if y <= 325:
                        percentage = abs(y - 350)
                    else:
                        percentage = abs(y - 450)

                if y >= 500 or y <= 300:
                    r1, g1, b1 = LAVENDER
                    r2, g2, b2 = LAVENDER
                    if y <= 300:
                        percentage = abs(y - 300)
                    else:
                        percentage = abs(y - 500)

                
            # Gradient Function
            percentage = (percentage / 50)
            r = r1 + percentage * (r2 - r1)
            g = g1 + percentage * (g2 - g1)
            b = b1 + percentage * (b2 - b1)
            shader_color = r, g, b


            # Saturn gradient lines
            if (y % 40) in range(0, 14):
                r, g, b = shader_color
                r *= 0.98
                g *= 0.98
                b *= 0.98
                shader_color = r, g, b

        # Ring bounds:
        # X - Hole: 200 - 600
        # Y - Hole: 380 - 420
        # So, if we use the equation of an ellipse, where a > b
        # the value must be a=200 and b=20
        elif current_shape == RING:
            # Filling from inside to outside
            x0, y0 = x - 400, y - 400
            a, b = 250, 25

            # First ellipse
            is_ellipse = self.check_ellipse(x0, y0, a, b)
            if is_ellipse:
                shader_color = 66, 76, 84
            else:
                # Second ellipse
                a += 70
                b += 5
                is_ellipse = self.check_ellipse(x0, y0, a, b)
                if is_ellipse:
                    shader_color = 94, 102, 116
                else:
                    # Third ellipse
                    a += 8
                    b += 5
                    is_ellipse = self.check_ellipse(x0, y0, a, b)
                    if is_ellipse:
                        shader_color = 0, 0, 0
                    else:
                        # Fourth ellipse
                        a += 65
                        b += 10
                        is_ellipse = self.check_ellipse(x0, y0, a, b)
                        if is_ellipse:
                            shader_color = 62, 72, 78

            # Saturn gradient lines
            

        b, g, r = shader_color
        b /= 255
        g /= 255
        r /= 255

        intensity = 1

        if current_shape == RING:
            intensity = self.radius(x - 400, y - 450) / 400
            intensity = 1 - (intensity * 0.90) ** 4
        elif current_shape == PLANET:
            intensity = (self.radius(x - 620, y - 590) + 50) / 400
            intensity = 1 - (intensity * 0.95) ** 4

        b *= intensity
        g *= intensity
        r *= intensity

        if intensity > 0:
            return r, g, b
        else:
            return 0, 0, 0

    def load(self, filename="default.obj", translate=[0, 0], scale=[1, 1], shape=None):
        model = Obj(filename)
        self.shape = shape

        # light = V3(0.7, 0.7, 0.5)

        for face in model.faces:
            vcount = len(face)

            if vcount == 3:
                face1 = face[0][0] - 1
                face2 = face[1][0] - 1
                face3 = face[2][0] - 1

                v1 = model.vertices[face1]
                v2 = model.vertices[face2]
                v3 = model.vertices[face3]

                x1 = round((v1[0] * scale[0]) + translate[0])
                y1 = round((v1[1] * scale[1]) + translate[1])
                z1 = round((v1[2] * scale[2]) + translate[2])

                x2 = round((v2[0] * scale[0]) + translate[0])
                y2 = round((v2[1] * scale[1]) + translate[1])
                z2 = round((v2[2] * scale[2]) + translate[2])

                x3 = round((v3[0] * scale[0]) + translate[0])
                y3 = round((v3[1] * scale[1]) + translate[1])
                z3 = round((v3[2] * scale[2]) + translate[2])

                a = V3(x1, y1, z1)
                b = V3(x2, y2, z2)
                c = V3(x3, y3, z3)

                vn0 = model.normals[face[0][2] - 1]
                vn1 = model.normals[face[1][2] - 1]
                vn2 = model.normals[face[2][2] - 1]

                self.triangle(a, b, c)

            else:
                face1 = face[0][0] - 1
                face2 = face[1][0] - 1
                face3 = face[2][0] - 1
                face4 = face[3][0] - 1

                v1 = model.vertices[face1]
                v2 = model.vertices[face2]
                v3 = model.vertices[face3]
                v4 = model.vertices[face4]

                x1 = round((v1[0] * scale[0]) + translate[0])
                y1 = round((v1[1] * scale[1]) + translate[1])
                z1 = round((v1[2] * scale[2]) + translate[2])

                x2 = round((v2[0] * scale[0]) + translate[0])
                y2 = round((v2[1] * scale[1]) + translate[1])
                z2 = round((v2[2] * scale[2]) + translate[2])

                x3 = round((v3[0] * scale[0]) + translate[0])
                y3 = round((v3[1] * scale[1]) + translate[1])
                z3 = round((v3[2] * scale[2]) + translate[2])

                x4 = round((v4[0] * scale[0]) + translate[0])
                y4 = round((v4[1] * scale[1]) + translate[1])
                z4 = round((v4[2] * scale[2]) + translate[2])

                a = V3(x1, y1, z1)
                b = V3(x2, y2, z2)
                c = V3(x3, y3, z3)
                d = V3(x4, y4, z4)

                self.triangle(a, b, c)
                self.triangle(a, c, d)

    def finish(self, filename="out.bmp"):
        # starts creating a new bmp file
        f = open(filename, "bw")

        f.write(char("B"))
        f.write(char("M"))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # image header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # Finishing placing points
        try:
            for x in range(self.height):
                for y in range(self.width):
                    f.write(self.framebuffer[x][y])
        except:
            print("Your obj file is too big. Try another scale/translate values")

        f.close()
