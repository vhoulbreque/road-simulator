import os
import numpy as np

from colors import color_range_init, white_range_init, yellow_range_init, shadow_colors_init
from layers import Background, Crop, Perspective, DrawLines, Shadows, Filter, NoiseLines, Enhance, Symmetric
from simulator import Simulator


if __name__ == '__main__':

    # shadow_colors = shadow_colors_init()
    shadow_colors = [(0, 0, 0)]

    xy0_range = [[x, 200] for x in range(0, 250+1)]  # add bottom edge of the picture
    xy1_range = [[0, y] for y in range(int(200/2), 0, -1)]  # add left edge of the picture
    xy1_range += [[x, 0] for x in range(0, 250+1)]  # add top edge of the picture
    xy1_range += [[249, y] for y in range(0, int(200/2))]  # add right edge of the picture
    radius_range = list(range(200, 500)) + list(range(5000, 5300))
    thickness_range = [6, 7, 8, 9, 10]

    color_range = [(255, 0, 125)]
    white_range = [(255, 255, 255)]
    yellow_range = [(0, 0, 255)]
    # color_range = color_range_init()
    #
    # white_range = white_range_init()
    # yellow_range = yellow_range_init()

    background_layer = Background(n_backgrounds=100, path='gpics', n_rot=1, n_res=1, n_crop=1, input_size=(250, 200))
    lines_layer = DrawLines(xy0_range, xy1_range, radius_range, thickness_range, color_range, white_range, yellow_range)
    symmetry_layer = Symmetric(proba=0.5)
    shadow_layer = Shadows(colors=shadow_colors)
    noisylines_layer = NoiseLines(color_range)
    filter_layer = Filter()
    enhance_layer = Enhance()
    perspective_layer = Perspective()
    crop_layer = Crop()

    layers = [background_layer, lines_layer, symmetry_layer, shadow_layer, noisylines_layer, filter_layer, enhance_layer, perspective_layer, crop_layer]
    simulator = Simulator(layers)
    simulator.generate(n_examples=100, path='dataset')

    n_max = 1 * 1 * 1000
