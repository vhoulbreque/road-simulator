import PIL
import os
import sys
import numpy as np

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from math import sqrt, atan2, pi
from random import randint, shuffle, choice, gauss, random
from tqdm import tqdm

from basic_objects import Point, RoadLine, Circle

sys.path.insert(0, '../')
from layers.layers import Layer


class Noise(Layer):

    def __init__(self):
        self.name = 'Noise'
        pass

    def call(self, img):
        return img

    def summary(self):
        return self.name


class Shadows(Noise):

    def __init__(self, colors):

        super(Shadows, self).__init__()

        if colors is None:
            raise Exception
        self.colors = colors
        self.name = 'Shadows'


    def call(self, img):
        x1 = randint(0, img.width)
        x2 = randint(0, img.width)
        y1 = randint(0, img.height)
        y2 = 10000000
        while abs(y2 - y1) > 75:  # TODO: stop hardcoded values
            if randint(0, 1):
                y2 = randint(y1, img.height)
            else:
                y2 = randint(0, y1)
        color = choice(self.colors)
        draw = ImageDraw.Draw(img)
        draw.rectangle((x1, y1, x2, y2), fill=color, outline=color)
        del draw
        return img


class Filter(Noise):

    def __init__(self, blur=0, gauss_blur=0, smooth=0, smooth_more=0, rank_filter=0):
        if blur + gauss_blur + smooth + smooth_more + rank_filter > 1:
            raise Exception
        if not all(item >= 0 for item in [blur, gauss_blur, smooth, smooth_more, rank_filter]):
            raise Exception

        super(Filter, self).__init__()

        self.blur = blur
        self.gauss_blur = gauss_blur
        self.smooth = smooth
        self.smooth_more = smooth_more
        self.rank_filter = rank_filter
        self.name = 'Filter'


    def call(self, img):

        im_n = img.copy()

        n = randint(0, 5)
        if n == 0:
            im_n = im_n.filter(ImageFilter.GaussianBlur(1))
        elif n == 1:
            im_n = im_n.filter(ImageFilter.BLUR)
        elif n == 2:
            im_n = im_n.filter(ImageFilter.SMOOTH)
        elif n == 3:
            im_n = im_n.filter(ImageFilter.SMOOTH_MORE)
        elif n == 4:
            im_n = im_n.filter(ImageFilter.RankFilter(size=3, rank=7))
        else:
            pass
        return im_n


class NoiseLines(Noise):

    def __init__(self, color_range):

        super(NoiseLines, self).__init__()

        self.color_range = color_range
        self.name = 'NoiseLines'


    def call(self, img):

        def draw_line_dep(im, x1, y1, x2, y2, fill, width=1):
            draw = ImageDraw.Draw(im)
            draw.line((x1, y1, x2, y2), fill=fill, width=width)
            del draw
            return im

        n = randint(0, 1)
        for i in range(n):
            if randint(0, 3) != 0: continue
            x1 = randint(0, img.width)
            x2 = randint(0, img.width)
            y1 = randint(0, img.height)
            y2 = randint(0, img.height)
            width = randint(1, 10)
            fill = choice(self.color_range)
            img = draw_line_dep(img, x1, y1, x2, y2, fill, width=width)

        return img


class Enhance(Noise):

    def __init__(self, contrast=0, brightness=0, sharpness=0, color=0):
        super(Enhance, self).__init__()
        self.name = 'Enhance'


    def call(self, img):
        n = randint(0, 4)

        im_n = img.copy()

        if n == 0:
            factor_contrast = randint(5, 10)/10
            enhancer = ImageEnhance.Contrast(im_n)
            im_n = enhancer.enhance(factor_contrast)
        elif n == 1:
            factor_brightness = randint(5, 15)/10
            enhancer = ImageEnhance.Brightness(im_n)
            im_n = enhancer.enhance(factor_brightness)
        elif n == 2:
            factor_sharpen = randint(0, 20)/10
            enhancer = ImageEnhance.Sharpness(im_n)
            im_n = enhancer.enhance(factor_sharpen)
        elif n == 3:
            factor_color = randint(0, 20)/10
            enhancer = ImageEnhance.Color(im_n)
            im_n = enhancer.enhance(factor_color)
        else:
            pass

        return im_n
