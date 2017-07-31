'''
    Noise Layers are for now on just layers like the ones in layers.
'''

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

    '''
        Root Object of Noise.
        By default, identity layer.
    '''

    def __init__(self):
        self.name = 'Noise'

    def call(self, img):
        if img is None: raise ValueError('img is None')
        return img

    def summary(self):
        return self.name


class Shadows(Noise):

    '''
        Adds shadows to the image.
    '''

    def __init__(self, color):

        super(Shadows, self).__init__()

        if color is None:
            raise Exception
        self.color = color
        self.name = 'Shadows'

    def call(self, img):

        if img is None: raise ValueError('img is None')

        x1 = randint(0, img.width)
        x2 = randint(0, img.width)
        y1 = randint(0, img.height)
        y2 = 10000000
        c = choice(self.color.colors)

        while abs(y2 - y1) > 75:
            if randint(0, 1):
                y2 = randint(y1, img.height)
            else:
                y2 = randint(0, y1)

        draw = ImageDraw.Draw(img)
        draw.rectangle((x1, y1, x2, y2), fill=c, outline=c)
        del draw

        return img


class Filter(Noise):

    '''
        Adds filters to the image.
    '''

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

        if img is None: raise ValueError('img is None')

        im_n = img.copy()

        gauss_blur_low, gauss_blur_high = 0, self.gauss_blur
        blur_low, blur_high = gauss_blur_high, gauss_blur_high + self.blur
        smooth_low, smooth_high = blur_high, blur_high + self.smooth
        smooth_more_low, smooth_more_high = smooth_high, smooth_high + self.smooth_more
        rank_low, rank_high = smooth_more_high, smooth_more_high + self.rank_filter

        r = random()
        if gauss_blur_low <= r <= gauss_blur_high:
            im_n = im_n.filter(ImageFilter.GaussianBlur(1))
        elif blur_low < r <= blur_high:
            im_n = im_n.filter(ImageFilter.BLUR)
        elif smooth_low < r <= smooth_high:
            im_n = im_n.filter(ImageFilter.SMOOTH)
        elif smooth_more_low < r <= smooth_more_high:
            im_n = im_n.filter(ImageFilter.SMOOTH_MORE)
        elif rank_low < r <= rank_high:
            im_n = im_n.filter(ImageFilter.RankFilter(size=3, rank=7))
        else:
            pass
        return im_n


class NoiseLines(Noise):

    '''
        Adds noise lines to the image i.e. lines randomly on the picture.
    '''

    def __init__(self, color_range, n_lines_max=1, proba_line=0.33):

        super(NoiseLines, self).__init__()

        self.color_range = color_range
        self.n_lines_max = n_lines_max
        self.proba_line = proba_line

        self.name = 'NoiseLines'


    def call(self, img):

        def draw_line_dep(im, x1, y1, x2, y2, fill, width=1):
            draw = ImageDraw.Draw(im)
            draw.line((x1, y1, x2, y2), fill=fill, width=width)
            del draw
            return im

        if img is None: raise ValueError('img is None')

        n = randint(0, self.n_lines_max)
        for i in range(n):
            if random() > self.proba_line: continue
            x1 = randint(0, img.width)
            x2 = randint(0, img.width)
            y1 = randint(0, img.height)
            y2 = randint(0, img.height)
            width = randint(1, 10)
            fill = choice(self.color_range.colors)
            img = draw_line_dep(img, x1, y1, x2, y2, fill, width=width)

        return img


class Enhance(Noise):

    '''
        Adds enhancements filters to the image.
    '''

    def __init__(self, contrast=0, brightness=0, sharpness=0, color=0):
        super(Enhance, self).__init__()
        self.name = 'Enhance'

        self.contrast = contrast
        self.brightness = brightness
        self.sharpness = sharpness
        self.color = color

    def call(self, img):

        if img is None: raise ValueError('img is None')

        im_n = img.copy()

        r = random()
        contrast_low, contrast_high = 0, self.contrast
        brightness_low, brightness_high = contrast_high, contrast_high + self.brightness
        sharpness_low, sharpness_high = brightness_high, brightness_high + self.sharpness
        color_low, color_high = sharpness_high, sharpness_high + self.color

        if contrast_low <= r < contrast_high:
            factor_contrast = randint(5, 10)/10
            enhancer = ImageEnhance.Contrast(im_n)
            im_n = enhancer.enhance(factor_contrast)
        elif brightness_low <= r < brightness_high:
            factor_brightness = randint(5, 15)/10
            enhancer = ImageEnhance.Brightness(im_n)
            im_n = enhancer.enhance(factor_brightness)
        elif sharpness_low <= r < sharpness_high:
            factor_sharpen = randint(0, 20)/10
            enhancer = ImageEnhance.Sharpness(im_n)
            im_n = enhancer.enhance(factor_sharpen)
        elif color_low <= r < color_high:
            factor_color = randint(0, 20)/10
            enhancer = ImageEnhance.Color(im_n)
            im_n = enhancer.enhance(factor_color)
        else:
            pass

        return im_n
