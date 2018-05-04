'''All general layers objects.
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

from PIL import Image, ImageDraw
from math import sqrt, atan2, pi
from random import randint, shuffle, choice, gauss, random

from .utils import find_coeffs
from ..basic_objects import Point, RoadLine, Circle


class Layer():
    '''Root Object of Layer.
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
    '''This layer draws the border of the road (constituted of 2 lines.)'''

    def __init__(self, xy0_range=None,
                    xy1_range=None,
                    radius_range=None,
                    thickness_range=None,
                    color_range=None,
                    middle_line=None,
                    name='DrawLines',
                    input_size=(250, 200)):
        """
        Arguments:
            xy0_range: A list of length-2 arrays.
                Every array is a coordinate [x, y].
                Every coordinate corresponds to the position of the lower
                intersection of the middle line.
            xy1_range: A list of length-2 arrays.
                Every array is a coordinate [x, y].
                Every coordinate corresponds to the position of the upper
                intersection of the middle line.
            radius_range: A list of > 0 integers.
                The middle line is in fact a circle.
                The bigger the radius, the straighter the line.
            thickness_range: A list of > 0 integers.
                The lines' thickness will be randomly drawn in the list.
            color_range: A `Colorange` object,
                containing all the RGB triplets of color.
            middle_line: triplet of int.
                plain = middle_line[0]
                empty = middle_line[1]
                line_type = middle_line[2]
            name: A string,
                the name of the layer so that it's easy to recognize it.
            input_size: 2-tuple of int,
                the size of the input image (width, height)
        """

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
            from ..colors import White, Yellow
            color_range = White() + Yellow()

        self.xy0_range = xy0_range
        self.xy1_range = xy1_range
        self.radius_range = radius_range
        self.thickness_range = thickness_range
        self.color_range = color_range

        self.input_size = input_size
        self.width = self.input_size[0]
        self.height = self.input_size[1]

        # Is there a VISIBLE middle line ? (the middle line always exists)
        # TODO: quite complex to have a 3-tuple for middle_line...
        if middle_line is not None:
            self.middle_line_plain = middle_line[0]
            self.middle_line_empty = middle_line[1]
            self.middle_line_type = middle_line[2]
            self.middle_line_color_range = middle_line[3]
        else:
            # Make it invisible by default
            self.middle_line_plain = None
            self.middle_line_empty = None
            self.middle_line_type = None
            self.middle_line_color_range = color_range

        self.max_width = 300
        self.name = name

    def call(self, im):

        def dir_gas(curr_line, pose):
            """
            Calculates the (dir, gas) values given the position
            of the car compared to the middle line.

            Arguments:
                curr_line: A `RoadLine` object,
                    the middle line.
                pose: A `Point` object,
                    indicates the position of the car on the image.

            Returns:
                A couple (angle, gas), the angle of the car given its position
                compared to the middle line and the gas value.
                For now, the gas value is constant.
            """

            radius = curr_line.radius
            pt0 = Point(curr_line.x0, curr_line.y0)
            pt1 = Point(curr_line.x1, curr_line.y1)
            center = pts2center(pt0, pt1, radius)
            vect = 0.5 * (pt0 + pt1) - center
            target_pt = center + vect * (radius/vect.norm())
            target_vect = target_pt - pose
            angle = atan2(target_vect.x, -target_vect.y) * 6 / pi

            gas = 0.5

            return angle, gas

        def generate_middle_line(xy0_range, xy1_range, radius_range, thickness_range, color_range):
            """Creates the middle line of the road. The middle line position,
            thickness, radius and color is randomly drawn from the different
            range arguments.

            Arguments:
                xy0_range: A list of length-2 arrays.
                    Every array is a coordinate [x, y].
                    Every coordinate corresponds to the position of the lower
                    intersection of the middle line.
                xy1_range: A list of length-2 arrays.
                    Every array is a coordinate [x, y].
                    Every coordinate corresponds to the position of the upper
                    intersection of the middle line.
                radius_range: A list of > 0 integers.
                    The middle line is in fact a circle.
                    The bigger the radius, the straighter the line.
                thickness_range: A list of > 0 integers.
                    The lines' thickness will be randomly drawn in the list.
                color_range: list of `Color` objects # TODO

            Returns:
                A `RoadLine` object
            """

            # A RoadLine is constituted of 2 points, (x0, y0) and (x1, y1)

            # First, let's choose the (x0, y0) one.
            index = int(gauss(len(xy0_range)//2, 50))
            while index >= len(xy0_range) or index < 0:
                index = int(gauss(len(xy0_range)//2, 50))
            x0, y0 = xy0_range[index]

            while 2 * x0 - self.width > self.max_width:
                index = int(gauss(len(xy0_range)//2, 50))
                while index >= len(xy0_range) or index < 0:
                    index = int(gauss(len(xy0_range)//2, 50))
                x0, y0 = xy0_range[index]

            # Secondly, let's choose the (x1, y1) one.
            index = int(gauss(len(xy1_range)//2, 100))
            while index >= len(xy1_range) or index < 0:
                index = int(gauss(len(xy1_range)//2, 100))
            x1, y1 = xy1_range[index]

            # The bigger the radius, the straighter the line.
            radius = radius_range[randint(0, len(radius_range)-1)]
            thickness = thickness_range[randint(0, len(thickness_range)-1)]
            color = color_range.colors[randint(0, len(color_range.colors)-1)]

            return RoadLine(x0, y0, x1, y1, radius, thickness=thickness, color=color)

        def draw_lines(img, line, width=55, right_turn=True, color_range=None):
            """Draws the visible lines on the image.

            Arguments:
                img: A `PIL.Image` object,
                    the image to modify.
                line: A `RoadLine` object,
                    the middle line.
                width: > 0 integer,
                    the distance between the 2 outer lines.
                right_turn: A Boolean,
                    does the road goes to the right ?
                    If `False`, goes to the left by symmetry.
                color_range: A `ColorRange` object,
                    the different RGB values the line can take.

            Returns:
                The modified image.
            """

            # Real lines
            line1 = line.copy()
            line2 = line.copy()
            middle_line = line.copy()

            line1.color = choice(color_range.colors)
            line2.color = choice(color_range.colors)
            middle_line.color = choice(self.middle_line_color_range.colors)

            draw = ImageDraw.Draw(img)

            # Draw the outer lines
            draw_one_line(draw, line1 - int(width/2), right_turn=right_turn)
            draw_one_line(draw, line2 + int(width/2), right_turn=right_turn)

            # Draw the middle line if visible, depending on the type
            if self.middle_line_type == 'dashed':
                draw_one_line(draw, middle_line, right_turn=right_turn,
                            plain=self.middle_line_plain,
                            empty=self.middle_line_empty)
            elif self.middle_line_type == 'plain':
                draw_one_line(draw, middle_line, right_turn=right_turn)

            # Noise lines
            # TODO: these lines should be of a different color (like shadows...)
            if randint(0, 1):
                line1 = line.copy()
                line2 = line.copy()
                line1.color = choice(color_range.colors)
                line2.color = choice(color_range.colors)

                width_noise = (1.4 + 3 * random()) * width

                draw_one_line(draw, line1 - int(width_noise/2), right_turn=right_turn)
                draw_one_line(draw, line2 + int(width_noise/2), right_turn=right_turn)

            return img

        def draw_circle(draw, circle):
            """Draws a circle on a `ImageDraw` object.

            Arguments:
                draw: A `PIL.Draw` object.

                circle: A `Circle` object.

            """

            thickness = circle.thickness
            color = circle.color

            x0 = circle.center.x - circle.radius
            y0 = circle.center.y - circle.radius
            x1 = circle.center.x + circle.radius
            y1 = circle.center.y + circle.radius

            start = 0
            end = 360

            if circle.empty == 0:
                for i in range(0, thickness):
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
            """To draw a circle given 2 points and a radius, we need the center
            of the circle. We calculate it here.

            Arguments:
                pt1: A `Point` object,
                    the first point belonging to the circle.
                pt2: A `Point` object,
                    the second point belonging to the circle.
                radius: An integer,
                    the radius of the circle.
                right_turn: A Boolean,
                    does the road goes to the right ?
                    If `False`, goes to the left by symmetry.

            Returns:
                A `Point` object modelizing the center of the circle.
            """

            vect = pt2 - pt1
            vect_orthog = Point(-vect.y, vect.x)

            vect_orthog = vect_orthog * (1/vect_orthog.norm())
            middle = (pt1 + pt2) * 0.5

            triangle_height = sqrt(radius*radius - (vect.norm() * 0.5 * vect.norm() * 0.5 ))
            center = middle + vect_orthog * triangle_height

            # Make sure the center is on the correct side of the points
            symmetry = True
            if center.x > middle.x:
                symmetry = False
            if not right_turn:
                symmetry = not symmetry

            # If not, take the symmetric point with respect to the middle
            if symmetry:
                center = 2 * middle - center

            return center

        def draw_one_line(draw, line, right_turn=True, plain=1, empty=0):
            """Draws a line on the image.
            The method used to draw a line depends o the radius of the line,
            and if the line is dashed or not.

            Arguments:
                draw: A `PIL.ImageDraw` object,
                    represents the image on which the lines
                    are drawn.
                line: A `RoadLine` object,
                    the line to draw.
                right_turn: A Boolean,
                    does the road goes to the right ?
                    If `False`, goes to the left by symmetry.
                plain: An integer,
                    tells the proportion of 'plain' line.
                    If empty is 0, the line is 'plain'.
                empty: An integer,
                    tells the proportion of 'empty' line.
                    If 0, the line is 'plain'. If not, the line is dashed.

            Returns:
                img: A `PIL.Image` object,
                    the modified image.
                angle: A float,
                    the angle to get to the right position considering
                    the current picture, the position of the car, and the
                    position of the middle line.
                gas: A float,
                    the gas value.
            """

            if line.y1 > line.y0:
                x0, y0 = line.x1, line.y1
                x1, y1 = line.x0, line.y0
            else:
                x0, y0 = line.x0, line.y0
                x1, y1 = line.x1, line.y1

            if x0 == x1:
                # Straight line
                draw.line([x0, y0, x1, y1], fill=line.color, width=line.thickness)
            else:
                radius = line.radius
                pt0 = Point(x0, y0)
                pt1 = Point(x1, y1)
                center = pts2center(pt0, pt1, radius, right_turn=right_turn)
                thickness = line.thickness
                color = line.color

                circle1 = Circle(center, radius, thickness=thickness, color=color)

                # That is, the line is dashed
                if empty != 0:
                    circle1.plain = plain
                    circle1.empty = empty

                draw_circle(draw, circle1)

        if im is None:
            raise ValueError('img is None')

        img = im.copy()

        # Current position of the car (the car is generally in the middle of
        # the lower bound of the image)
        pose = Point(self.width/2, self.height)

        # Middle line
        midline = generate_middle_line(self.xy0_range,
                                        self.xy1_range,
                                        self.radius_range,
                                        self.thickness_range,
                                        self.middle_line_color_range)

        # TODO: change this so that the distance between the 2 lines can be chosen
        # by the user
        # 200: harcoded value
        # 100: harcoded value
        width = randint(max(180, 2 * midline.x0 - self.width), self.max_width)

        # Draw all the visible lines
        img = draw_lines(img, midline, width=width, right_turn=True,
                                    color_range=self.color_range)

        # Get the angle and gas depending on the position of
        # the car with respect to the middle line.
        angle, gas = dir_gas(midline, pose)

        return img, angle, gas

    def summary(self):
        """Returns a string describing this layer"""

        return '{}'.format(self.name)


class Symmetric(Layer):
    '''This layer creates the symmetric of an image.'''

    def __init__(self, proba=0.5, name='Symmetric'):
        """
        Arguments:
            proba: A float,
                the probability to use the symmetric instead of the original
                image. On the original image, the lines are always going to
                the right.

            name: A string,
                the name of the layer
        """

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
            # Symmetry according to PIL..
            sym = sym.transform((width, height), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
            symmetry = True
        return sym, symmetry

    def summary(self):
        """Returns a string describing this layer"""

        return '{}\t{}'.format(self.name, self.proba)


class Perspective(Layer):
    '''This layer creates the perspective of an image.'''

    def __init__(self, output_dim=(250, 70), name='Perspective'):
        """
        Arguments:
            output_dim: A tuple of 2-integers, (width, height),
                the output dimensions of the image after perspective.

            name: A string,
                the name of the layer
        """

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
    '''This layer crops the image.'''

    def __init__(self, output_dim=(250, 70), name='Crop'):
        """
        Arguments:
            output_dim: A tuple of 2-integers, (width, height),
                the output dimensions of the image after crop.

            name: A string,
                the name of the layer
        """

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
    '''This layer is an input layer.
    It generates the inputs from background images.
    '''

    def __init__(self, n_backgrounds, path, n_rot=1, n_res=1, n_crop=1,
                    input_size=(250, 200), output_size=(250, 70),
                    width_range=None, angle_max=20, name='Background'):
        """

        Arguments:
            n_backgrounds: An integer,
                the number of backgrounds.
            path: A string,
                the path to the folder where background images
                are stocked.
            n_rot: A > 0 integer,
                the number of backgrounds to generate
                by rotating the existing background.
            n_res: A > 0 integer,
                the number of backgrounds to generate
                by resizing the existing background.
            n_crop: A > 0 integer,
                the number of backgrounds to generate
                by cropping the existing background.
            input_size:

            output_size:

            width_range:

            angle_max:

            name: a string,
                the name of the layer
        """

        # TODO: how to decrease the amount of ValueError ?
        # TODO: how to increase readibility ?
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
        """Generates backgrounds via:
            - choice of background image
            - rotation
            - resizing
            - cropping

        Returns:
            List of images of backgrounds.
        """

        from tqdm import tqdm

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
                b = b.resize((new_width, new_height), Image.ANTIALIAS)
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
        """Returns a string describing the layer"""

        return '{}\t{}\t{}\t{}\t{}'.format(self.name, self.n_backgrounds,
                                            self.n_res, self.n_rot, self.n_crop)
