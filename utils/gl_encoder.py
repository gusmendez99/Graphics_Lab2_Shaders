"""
    Universidad del Valle de Guatemala
    Gustavo Mendez - 18500

    gl-encoder.py - simple encoder functions
"""

import struct

def char(myChar):
		return struct.pack('=c', myChar.encode('ascii'))

def word(myChar):
	return struct.pack('=h', myChar)
	
def dword(myChar):
	return struct.pack('=l', myChar)