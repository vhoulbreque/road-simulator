from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import PIL
import os

from colors import *
from layers import *
from basic_objects import *

from PIL import Image, ImageDraw
from math import sqrt, atan2, pi
from random import randint
import numpy as np
import random


from random import randint
from tqdm import tqdm
import os
from random import choice



class Simulator():


    def __init__(self, layers):

        self.layers = layers
        self.input_images = layers[0].backgrounds


    def generate(self, n_examples, path):

        if n_examples <= 0:
            raise Exception

        if os.path.exists(path):
            print('The path `{}` already exists !'.format(path))
        else:
            os.makedirs(path)

        for i in tqdm(range(n_examples)):
            index = randint(0, len(self.input_images)-1)
            ii = self.input_images[index].copy()
            new_img, new_name = self.generate_one_image(ii)
            new_img.save(os.path.join(path, 'frame_' + str(i) + new_name))
        print('DONE')

    def generate_one_image(self, img):

        sym = False

        im = img.copy()
        for layer in self.layers:
            if not isinstance(layer, Background):
                if isinstance(layer, DrawLines):
                    im, angle, gas = layer.call(im)  # Arguments
                elif isinstance(layer, Symmetric):
                    im, sym = layer.call(im)  # Arguments
                else:
                    im = layer.call(im)  # Arguments

        if sym:
            angle = -angle
        name = '_gas_' + str(gas) + '_dir_' +  str(angle) + '.jpg'
        return im, name
