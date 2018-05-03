'''
    All general layers objects.
    A layer has 1 important functions: `call`. This is the function used to
    manipulate the image that goes out of the former layer.

    When you want to create a new layer on your own, you have to follow this
    scheme:

        class MyLayer(Layer):

            def __init__(self, **args, **kwargs):
                # The constructor of the class
                ...

            def call(self, img):
                # Manipulate the img to do whatever the layer is supposed to do
                ...
                return img

            def summary():
                # Gives information about what is in this layer
                # Optional
                ...

'''

import os
import numpy as np

from tqdm import tqdm
from PIL import Image, ImageDraw
from math import sqrt, atan2, pi
from random import randint, shuffle, choice, gauss, random

from basic_objects import Point, RoadLine, Circle


class Layer():

    '''
        Root Object of Layer.
        By default, identity layer.
    '''

    def __init__(self, name='Layer'):
        if name is None: raise ValueError('name must be different from None')
        self.name = name

    def call(self, img):
        if img is None: raise ValueError('img is None')
        return img

    def summary(self):
        return self.name


class DrawLines(Layer):

    '''
        This layer draws the border of the road (constituted of 2 lines.)
        A line in the middle was available in a previous version. It is
        coming soon.
    '''

    def __init__(self, xy0_range=None, xy1_range=None, radius_range=None,
                    thickness_range=None, color_range=None, middle_line=None,
                    name='DrawLines', input_size=(250, 200)):

        super(DrawLines, self).__init__()

        width_begin, height_begin = input_size

        if xy0_range is None:
            xy0_range = [[x, height_begin] for x in range(0, width_begin+1)]
        if xy1_range is None:
            xy1_range = [[0, y] for y in range(int(height_begin/2), 0, -1)]
            xy1_range += [[x, 0] for x in range(0, width_begin+1)]
            xy1_range += [[width_begin-1, y] for y in range(0, int(height_begin/2))]
        if radius_range is None:
            radius_range = list(range(200, 500)) + list(range(5000, 5300))
        if thickness_range is None:
            thickness_range = [6, 7, 8, 9, 10]
        if color_range is None:
            from colors import White, Yellow
            color_range = White() + Yellow()

        # if name is None:
        #     raise ValueError('name must be different from None')
        # if not all([r is not None and len(r)> 0 and isinstance(r, list) for r in [xy0_range, xy1_range, radius_range, thickness_range]]):
        #     raise ValueError('xy0_range, xy1_range, radius_range and thickness_range must not be None or empty lists')
        # if not all([all([isinstance(r, list) for r in l]) for l in [xy0_range, xy1_range]]):
        #     raise ValueError('xy0_range and xy1_range must be composed of lists')
        # if not all([all([len(r) == 2 for r in l]) for l in [xy0_range, xy1_range]]):
        #     raise ValueError('xy0_range and xy1_range must be lists of 2 item long lists')
        # if not all([all([isinstance(r, int) for r in l]) for l in [radius_range, thickness_range]]):
        #     raise ValueError('radius_range and thickness_range must be composed of integers')
        # if color_range is None:
        #     raise ValueError('color_range must be different from None')
        # if len(color_range.colors) == 0:
        #     raise ValueError('color_range must have at least one color')
        # if middle_line is not None:
        #     if len(middle_line) != 3:
        #         raise ValueError('middle_line needs to be a tuple of length 3 when not None')
        #     if not all([(isinstance(middle_line[i], float) or isinstance(middle_line[i], int)) and middle_line[i] >= 0 for i in range(len(middle_line)-1)]):
        #         raise ValueError('The 2 first elements of middle_line must be int or float')
        #     if not middle_line[2] in [None, 'dashed', 'plain']:
        #         raise ValueError('The third element of middle_line must be None, \'dashed\' or \'plain\'')

        self.xy0_range = xy0_range
        self.xy1_range = xy1_range
        self.radius_range = radius_range
        self.thickness_range = thickness_range
        self.color_range = color_range
        self.input_size = input_size
        self.width = self.input_size[0]
        self.height = self.input_size[1]
        if middle_line is not None:
            self.middle_line_plain = middle_line[0]
            self.middle_line_empty = middle_line[1]
            self.middle_line_type = middle_line[2]
        else:
            self.middle_line_plain = None
            self.middle_line_empty = None
            self.middle_line_type = None

        self.name = name

    def call(self, im):

        def middle_line2dir_gas(curr_line, pose):
            radius = curr_line.radius
            pt0 = Point(curr_line.x0, curr_line.y0)
            pt1 = Point(curr_line.x1, curr_line.y1)
            center = pts2center(pt0, pt1, radius)
            vect = 0.5 * (pt0 + pt1) - center
            target_pt = center + vect * (radius/vect.norm())

            target_vect = target_pt - pose
            angle = atan2(target_vect.x, -target_vect.y) * 6 / pi
            gas = 0.5
            output = angle, gas
            return output

        def middle_lines_generator(xy0_range, xy1_range, radius_range, thickness_range, color_range):

            index = int(gauss(len(xy0_range)//2, 50))
            while index >= len(xy0_range) or index < 0:
                index = int(gauss(len(xy0_range)//2, 50))
            x0, y0 = xy0_range[index]

            index = int(gauss(len(xy1_range)//2, 100))
            while index >= len(xy1_range) or index < 0:
                index = int(gauss(len(xy1_range)//2, 100))
            x1, y1 = xy1_range[index]

            radius = radius_range[randint(0, len(radius_range)-1)]
            thickness = thickness_range[randint(0, len(thickness_range)-1)]
            color = color_range.colors[randint(0, len(color_range.colors)-1)]

            return RoadLine(x0, y0, x1, y1, radius, thickness=thickness, color=color)

        def middleline2drawing(img, line, width=55, right_turn=True, color_range=None):

            # Real lines
            line1 = line.copy()
            line2 = line.copy()
            middle_line = line.copy()

            line1.color = choice(color_range.colors)
            line2.color = choice(color_range.colors)
            middle_line.color = choice(color_range.colors)

            draw = ImageDraw.Draw(img)

            draw_line(draw, line1 - int(width/2), right_turn=right_turn)
            draw_line(draw, line2 + int(width/2), right_turn=right_turn)
            if self.middle_line_type == 'dashed':
                draw_line(draw, middle_line, right_turn=right_turn,
                            plain=self.middle_line_plain,
                            empty=self.middle_line_empty)
            elif self.middle_line_type == 'plain':
                draw_line(draw, middle_line, right_turn=right_turn)

            # Noise lines
            if randint(0, 1):
                line1 = line.copy()
                line2 = line.copy()
                line1.color = choice(color_range.colors)
                line2.color = choice(color_range.colors)

                width_noise = (1.4 + 3 * random()) * width

                draw_line(draw, line1 - int(width_noise/2), right_turn=right_turn)
                draw_line(draw, line2 + int(width_noise/2), right_turn=right_turn)

            return img

        def draw_circle(draw, circle):
            thickness = circle.thickness
            color = circle.color

            x0 = circle.center.x - circle.radius
            y0 = circle.center.y - circle.radius
            x1 = circle.center.x + circle.radius
            y1 = circle.center.y + circle.radius

            start = 0
            end = 360

            if circle.empty == 0:
                for i in range(0,thickness):
                    diff = i - int(thickness/2)
                    xy = [x0+diff, y0, x1+diff, y1]
                    draw.arc(xy, start, end, fill=color)
            else:
                plain_angle = float(circle.plain)/circle.radius
                empty_angle = float(circle.empty)/circle.radius
                for i in range(0,thickness):
                    diff = i - int(thickness/2)
                    xy = [x0+diff, y0, x1+diff, y1]
                    for angle in range(0, int(2*pi/(plain_angle+empty_angle))):
                        start = angle * (plain_angle+empty_angle)
                        end = start + plain_angle
                        draw.arc(xy, start*(180/pi), end*(180/pi), fill=color)

        def pts2center(pt1, pt2, radius, right_turn=True):
            vect = pt2 - pt1
            vect_orthog = Point(-vect.y, vect.x)

            vect_orthog = vect_orthog * (1/vect_orthog.norm())
            middle = (pt1 + pt2) * 0.5

            triangle_height = sqrt(radius*radius - (vect.norm() * 0.5 * vect.norm() * 0.5 ))
            center = middle + vect_orthog * triangle_height

            # make sure the center is on the correct side of the points
            #it is on the right by default
            symmetry = True
            if center.x > middle.x:
                symmetry = False
            if not right_turn: symmetry = not symmetry
            # if not, take the symmetric point with respect to the middle
            if symmetry:
                center = 2 * middle - center
            return center

        def draw_lines(img, line1, line2, right_turn=True):
            draw = ImageDraw.Draw(img)
            draw_line(draw, line1, right_turn=right_turn)
            draw_line(draw, line2, right_turn=right_turn)
            return img

        def draw_line(draw, line, right_turn=True, plain=1, empty=0):

            if line.y1 > line.y0:
                x0, y0 = line.x1, line.y1
                x1, y1 = line.x0, line.y0
            else:
                x0, y0 = line.x0, line.y0
                x1, y1 = line.x1, line.y1

            if x0 == x1:
                draw.line([x0, y0, x1, y1], fill=line.color, width=line.thickness)
            else:
                radius = line.radius
                pt0 = Point(x0, y0)
                pt1 = Point(x1, y1)
                center = pts2center(pt0, pt1, radius, right_turn=right_turn)
                thickness = line.thickness
                color = line.color

                circle1 = Circle(center, radius,thickness=thickness, color=color)

                if empty != 0:
                    circle1.plain = plain
                    circle1.empty = empty

                draw_circle(draw, circle1)

        if im is None:
            raise ValueError('img is None')

        img = im.copy()

        pose = Point(self.width/2, self.height)

        # max_width = 200
        # min_width = 100

        # if midline.x0 >= 125:
        #     width = randint(max(min_width, 2 * midline.x0 - 250), max(max_width, 2 * midline.x0 - 250))
        # else:
        #     width = randint(max(min_width, 250 - 2 * midline.x0),  max(max_width, 250 - 2 * midline.x0))

        midline = middle_lines_generator(self.xy0_range, self.xy1_range, self.radius_range, self.thickness_range, self.color_range)
        while 2 * midline.x0 - self.width > 140:
            midline = middle_lines_generator(self.xy0_range, self.xy1_range, self.radius_range, self.thickness_range, self.color_range)
        width = randint(max(70, 2 * midline.x0 - self.width), 140)

        img = middleline2drawing(img, midline, width=width, right_turn=True,
                                    color_range=self.color_range)

        angle, gas = middle_line2dir_gas(midline, pose)

        return img, angle, gas

    def summary(self):
        return '{}'.format(self.name)


class Symmetric(Layer):
    '''
        This layer creates the symmetric of an image.
    '''

    def __init__(self, proba=0.5, name='Symmetric'):

        super(Symmetric, self).__init__()

        if name is None:
            raise ValueError('name must be different from None')
        if proba is None or not (isinstance(proba, float) or isinstance(proba, int)) or not (0 <= proba <= 1):
            raise ValueError('The probability must be a float or integer and 0 <= proba <= 1')

        self.proba = proba
        self.name = name

    def call(self, img):

        if img is None:
            raise ValueError('img is None')

        width, height = img.size
        sym = img.copy()

        symmetry = False
        if random() < self.proba:
            from_points = [(0, 0), (width-1, 0), (width-1, height-1), (0, height-1)]
            new_points = [(width-1, 0), (0, 0), (0, height-1), (width-1, height-1)]
            coeffs = find_coeffs(new_points, from_points)
            sym = sym.transform((width, height), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
            symmetry = True
        return sym, symmetry

    def summary(self):
        return '{}\t{}'.format(self.name, self.proba)


class Perspective(Layer):
    '''
        This layer creates the perspective of an image.
    '''

    def __init__(self, output_dim=(250, 70), name='Perspective'):

        if name is None:
            raise ValueError('name must be different from None')

        super(Perspective, self).__init__()

        self.new_width = output_dim[0]
        self.new_height = output_dim[1]
        self.name = name

    def call(self, img):

        if img is None:
            raise ValueError('img is None')

        width, height = img.size
        from_points = [(0, 0), (width-1, 0), (width-1, height-1), (0, height-1)]
        new_points = [(self.new_width-1, 0),
                        (self.new_width+self.new_width-1, 0),
                        (self.new_width*2+self.new_width-1, self.new_height-1),
                        (0, self.new_height-1)]
        coeffs = find_coeffs(new_points, from_points)
        img = img.transform((self.new_width+self.new_width*2, self.new_height),
                                Image.PERSPECTIVE, coeffs, Image.BICUBIC)
        return img


class Crop(Layer):

    '''
        This layer crops the image.
    '''

    def __init__(self, output_dim=(250, 70), name='Crop'):

        if name is None:
            raise ValueError('name must be different from None')

        super(Crop, self).__init__()

        self.new_width = output_dim[0]
        self.new_height = output_dim[1]
        self.name = name

    def call(self, img):
        if img is None: raise ValueError('img is None')

        width = img.width
        height = img.height

        x_shift = self.new_width

        img = img.crop((x_shift-1, 0, width-x_shift-1, self.new_height))

        return img


class Background(Layer):
    '''
        This layer is an input layer.
        It generates the inputs from background images.
    '''

    def __init__(self, n_backgrounds, path, n_rot=1, n_res=1, n_crop=1,
                    input_size=(250, 200), output_size=(250, 70),
                    width_range=None, angle_max=20, name='Background'):

        if width_range is None:
            width_range = [i for i in range(output_size[0], output_size[0] + 500)]

        if name is None:
            raise ValueError('name must be different from None')

        if not isinstance(n_backgrounds, int):
            raise ValueError('The number of backgrounds to generate must be an integer')
        if n_backgrounds <= 0:
            raise ValueError('The number of backgrounds to generate must be positive')

        if not os.path.exists(path):
            raise ValueError('The path `{}` does not exist'.format(path))
        if not os.path.isdir(path):
            raise ValueError('The path `{}` is not a directory'.format(path))
        if len(os.listdir(path)) == 0:
            raise ValueError('There are no images at path `{}`'.format(path))

        if not all([isinstance(item, int) and item >= 0 for item in [n_rot, n_res, n_crop]]):
            raise ValueError('The number of rotations, resizing and cropping must all be positive. Not `{}`'.format(str([n_rot, n_res, n_crop])))

        if not isinstance(input_size, tuple):
            raise ValueError('input_size must be a tuple : `{}`'.format(str(input_size)))
        if not (len(input_size) == 2):
            raise ValueError('input_size must be 2 dimensional: `{}`'.format(len(input_size)))
        if not (isinstance(input_size[0], int) and isinstance(input_size[1], int) and input_size[0] >= 0 and input_size[1] >= 0):
            raise ValueError('input_size must be 2 dimensional: `{}`'.format(len(input_size)))

        if not isinstance(width_range, list) or len(width_range) == 0:
            raise ValueError('width_range must be a non-empty list or None')
        if max(width_range) < input_size[0]:
            # Because resizing during generation needs to be done on a higher
            # width
            # TODO: not a good test
            raise ValueError('TODO')

        super(Background, self).__init__()

        self.n_backgrounds = n_backgrounds
        self.path = path
        self.n_rot = n_rot
        self.n_res = n_res
        self.n_crop = n_crop
        self.input_size = input_size
        self.width_range = width_range
        angle_max = angle_max % 360
        self.angles_range = [i for i in range(0, angle_max)] + [i for i in range(360-angle_max, 360)] + [i for i in range(180-angle_max, 180+angle_max)]
        self.backgrounds = self.generate_all_backgrounds()

        self.name = name

    def generate_all_backgrounds(self):
        width, height = self.input_size

        # Choice of the background image
        backgrounds = []
        image_names = os.listdir(self.path)
        n = min([len(image_names), self.n_backgrounds])
        for index in tqdm(range(n), desc='loading images'):
            background = Image.open(os.path.join(self.path, image_names[index])).convert('RGB')
            backgrounds.append(background)

        # Generation of the rotations
        new_backgrounds = []
        for i in tqdm(range(len(backgrounds)), desc='rotating images'):
            background = backgrounds[i]
            for j in range(self.n_rot):
                b = background.copy()
                # Choice of a rotation angle
                angle_rotation = self.angles_range[randint(0, len(self.angles_range)-1)]
                b = b.rotate(angle_rotation)
                new_backgrounds.append(b)

        backgrounds = new_backgrounds
        if len(backgrounds) >= self.n_backgrounds:
            shuffle(backgrounds)
            backgrounds = backgrounds[:self.n_backgrounds]

        # Generation of the resized images
        new_backgrounds = []
        for i in tqdm(range(len(backgrounds)), desc='resizing images'):
            for j in range(self.n_res):
                b = backgrounds[i]
                # Choice of the resize size
                index = randint(0, len(self.width_range)-1)
                new_width = self.width_range[index]
                new_height = int(4 * new_width / 5)
                b = b.resize((new_width, new_height), .ANTIALIAS)
                new_backgrounds.append(b)

        backgrounds = new_backgrounds
        if len(backgrounds) >= self.n_backgrounds:
            shuffle(backgrounds)
            backgrounds = backgrounds[:self.n_backgrounds]

        # Generation of the cropped images
        new_backgrounds = []
        for i in tqdm(range(len(backgrounds)), desc='cropping images'):
            background = backgrounds[i]
            for j in range(self.n_crop):
                b = background.copy()
                # Choice of the rectangle to crop
                x0, y0 = randint(0, b.width - width), randint(0, b.height - height)
                x1, y1 = x0 + width, y0 + height
                b = b.crop((x0, y0, x1, y1))
                new_backgrounds.append(b)

        backgrounds = new_backgrounds
        shuffle(backgrounds)
        backgrounds = backgrounds[:self.n_backgrounds]
        return backgrounds

    def summary(self):
        return '{}\t{}\t{}\t{}\t{}'.format(self.name, self.n_backgrounds,
                                            self.n_res, self.n_rot, self.n_crop)


# Function to find the points to apply a transformation between 2 points in an
# image
def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = np.matrix(matrix, dtype=np.float)
    B = np.array(pb).reshape(8)

    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)
