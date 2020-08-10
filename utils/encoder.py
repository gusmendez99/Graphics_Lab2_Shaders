"""
    Universidad del Valle de Guatemala
    Gustavo Mendez - 18500

    gl-encoder.py - simple encoder functions
"""

import struct


def char(my_char):
    return struct.pack("=c", my_char.encode("ascii"))


def word(my_char):
    return struct.pack("=h", my_char)


def dword(my_char):
    return struct.pack("=l", my_char)
