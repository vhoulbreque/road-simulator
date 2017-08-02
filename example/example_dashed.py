'''
    This is a toy example.
    It creates one hundred (70 * 250) RGB images of road lines as seen by a
    1/10th scale car with a dashed line in the middle.
    Saves these pictures in a folder called examples_pictures.
'''

import os
import sys
import numpy as np

sys.path.insert(0, '../src/')

from colors import Yellow, White, DarkShadow
from layers.layers import Background, Crop, Perspective, DrawLines, Symmetric
from layers.noise import Shadows, Filter, NoiseLines, Enhance
from simulator import Simulator


if __name__ == '__main__':

    width_begin, height_begin = 250, 200
    width_end, height_end = 250, 70

    xy0_range = [[x, height_begin] for x in range(0, width_begin+1)]  # add bottom edge of the picture
    xy1_range = [[0, y] for y in range(int(height_begin/2), 0, -1)]  # add left edge of the picture
    xy1_range += [[x, 0] for x in range(0, width_begin+1)]  # add top edge of the picture
    xy1_range += [[width_begin-1, y] for y in range(0, int(height_begin/2))]  # add right edge of the picture
    radius_range = list(range(200, 500)) + list(range(5000, 5300))
    thickness_range = [6, 7, 8, 9, 10]

    width_range = [i for i in range(width_end, 750)]
    angle_max = 20

    white_range = White()
    yellow_range = Yellow()
    shadow_colors = DarkShadow()

    color_range = white_range + yellow_range

    background_layer = Background(n_backgrounds=3,
                                    path='../ground_pics',
                                    n_rot=1, n_res=1, n_crop=1,
                                    input_size=(width_begin, height_begin),
                                    width_range=width_range,
                                    angle_max=angle_max)
    lines_layer = DrawLines(xy0_range, xy1_range, radius_range,
                            thickness_range, color_range,
                            middle_line=(50, 30, 'dashed'))
    symmetry_layer = Symmetric(proba=0.5)
    shadow_layer = Shadows(color=shadow_colors)
    noisylines_layer = NoiseLines(color_range)
    filter_layer = Filter()
    enhance_layer = Enhance()
    perspective_layer = Perspective()
    crop_layer = Crop()

    layers = [background_layer, lines_layer, symmetry_layer, shadow_layer,
                noisylines_layer, filter_layer, enhance_layer,
                perspective_layer, crop_layer]
    simulator = Simulator(layers)

    print(simulator.summary())

    simulator.generate(n_examples=100, path='sample_dashed')
