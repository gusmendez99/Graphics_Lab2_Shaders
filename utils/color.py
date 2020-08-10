"""
    Universidad del Valle de Guatemala
    Gustavo Mendez - 18500

    gl-color.py - simple color functions
"""


def normalize_color(colors_array):
    return [round(i * 255) for i in colors_array]


def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])
