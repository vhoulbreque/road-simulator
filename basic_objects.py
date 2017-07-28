from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import PIL
import os

from colors import *
from layers import *


from PIL import Image, ImageDraw
from math import sqrt, atan2, pi
from random import randint
import numpy as np
import random


from random import randint
from tqdm import tqdm
import os
from random import choice

class RoadLine:
    def __init__(self, x0, y0, x1, y1, radius, thickness=10, color=(255, 255, 255)):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.radius = radius
        self.thickness = thickness
        self.color = color

    def copy(self):
        new_line = RoadLine(self.x0, self.y0, self.x1, self.y1, self.radius, thickness=self.thickness, color=self.color)
        return new_line

    def __add__(self, scalar):
        return RoadLine(self.x0 + scalar, self.y0, self.x1 + scalar, self.y1, self.radius, thickness=self.thickness, color=self.color)

    def __sub__(self, scalar):
        return RoadLine(self.x0 - scalar, self.y0, self.x1 - scalar, self.y1, self.radius, thickness=self.thickness, color=self.color)

    def print_line(self):
        print(" point0 : ", self.x0, self.y0, " point1: ", self.x1, self.y1, " radius: ", self.radius , " color: ", self.color, " thickness: ", self.thickness)

class Circle:
    def __init__(self, center, radius,thickness=10, color=(255, 255, 255), plain=300, empty=0):
        self.center = center
        self.radius = radius
        self.thickness = thickness
        self.color = color
        self.plain = plain
        self.empty = empty

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, pt):
        return Point(self.x + pt.x, self.y + pt.y)

    def __sub__(self, pt):
        return Point(self.x - pt.x, self.y - pt.y)

    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def norm(self):
        return sqrt(float(self.x)*float(self.x) + float(self.y)*float(self.y))
