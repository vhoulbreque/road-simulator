from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import PIL
import os

from colors import *
from basic_objects import *

from PIL import Image, ImageDraw
from math import sqrt, atan2, pi
from random import randint
import numpy as np
from random import shuffle


from random import randint
from tqdm import tqdm
import os
from random import choice



WIDTHS = [i for i in range(250, 750)]
ANGLE_ROT_MAX = 20
ANGLES = [i for i in range(0, ANGLE_ROT_MAX)] + [i for i in range(360-ANGLE_ROT_MAX, 360)] + [i for i in range(180-ANGLE_ROT_MAX, 180+ANGLE_ROT_MAX)]


class Layer():

    def __init__(self):
        pass


    def call(self):
        pass


class DrawLines(Layer):

    def __init__(self, xy0_range, xy1_range, radius_range, thickness_range, color_range, white_range, yellow_range):
        self.xy0_range = xy0_range
        self.xy1_range = xy1_range
        self.radius_range = radius_range
        self.thickness_range = thickness_range
        self.color_range = color_range
        self.white_range = white_range
        self.yellow_range = yellow_range
        super(DrawLines, self).__init__()

    def middle_lines_generator(xy0_range, xy1_range, radius_range, thickness_range, color_range):

        index = int(random.gauss(len(xy0_range)//2, 50))
        while index >= len(xy0_range) or index < 0:
            index = int(random.gauss(len(xy0_range)//2, 50))
        x0, y0 = xy0_range[index]

        index = int(random.gauss(len(xy1_range)//2, 100))
        while index >= len(xy1_range) or index < 0:
            index = int(random.gauss(len(xy1_range)//2, 100))
        x1, y1 = xy1_range[index]

        radius = radius_range[randint(0, len(radius_range)-1)]
        thickness = thickness_range[randint(0, len(thickness_range)-1)]
        color = color_range[randint(0, len(color_range)-1)]

        return RoadLine(x0, y0, x1, y1, radius, thickness=thickness, color=color)


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
            pt0 = point(x0, y0)
            pt1 = point(x1, y1)
            center = pts2center(pt0, pt1, radius, right_turn=right_turn)
            thickness = line.thickness
            color = line.color

            circle1 = circle(center, radius, thickness=thickness, color=color)

            if empty != 0:
                circle1.plain = plain
                circle1.empty = empty

            draw_circle(draw, circle1)


    def call(self, im):

        def middle_line2dir_gas(curr_line, pose):
            radius = curr_line.radius
            pt0 = Point(curr_line.x0, curr_line.y0)
            pt1 = Point(curr_line.x1, curr_line.y1)
            center = pts2center(pt0, pt1, radius)
            vect = 0.5 * (pt0+pt1) - center
            target_pt = center + vect * (radius/vect.norm())

            target_vect = target_pt - pose
            angle = atan2(target_vect.x, -target_vect.y) * 6 / pi
            gas = 0.5
            output = angle, gas
            return output

        def middle_lines_generator(xy0_range, xy1_range, radius_range, thickness_range, color_range):

            index = int(random.gauss(len(xy0_range)//2, 50))
            while index >= len(xy0_range) or index < 0:
                index = int(random.gauss(len(xy0_range)//2, 50))
            x0, y0 = xy0_range[index]

            index = int(random.gauss(len(xy1_range)//2, 100))
            while index >= len(xy1_range) or index < 0:
                index = int(random.gauss(len(xy1_range)//2, 100))
            x1, y1 = xy1_range[index]

            radius = radius_range[randint(0, len(radius_range)-1)]
            thickness = thickness_range[randint(0, len(thickness_range)-1)]
            color = color_range[randint(0, len(color_range)-1)]

            return RoadLine(x0, y0, x1, y1, radius, thickness=thickness, color=color)

        def middleline2drawing(img, line, width=55, right_turn=True, color_range=None):
            # Real lines
            line1 = line.copy()
            line2 = line.copy()
            line1.color = random.choice(color_range)
            line2.color = random.choice(color_range)
            img = draw_lines(img, line1 - int(width/2), line2 + int(width/2), right_turn=right_turn)

            # Noise lines
            if randint(0, 1):
                line1 = line.copy()
                line2 = line.copy()
                line1.color = random.choice(color_range)
                line2.color = random.choice(color_range)
                width_noise = (1.4 + 3 * random.random()) * width
                img = draw_lines(img, line1 - int(width_noise/2), line2 + int(width_noise/2), right_turn=right_turn)
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
            middle = (pt1+pt2) * 0.5

            triangle_height = sqrt(radius*radius - (vect.norm() * 0.5 * vect.norm() * 0.5 ) )
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

        def draw_line(draw, line, right_turn=True):

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
                draw_circle(draw, circle1)

        img = im.copy()

        pose = Point(250/2, 200)

        max_width = 200
        min_width = 100

        # if midline.x0 >= 125:
        #     width = randint(max(min_width, 2 * midline.x0 - 250), max(max_width, 2 * midline.x0 - 250))
        # else:
        #     width = randint(max(min_width, 250 - 2 * midline.x0),  max(max_width, 250 - 2 * midline.x0))

        midline = middle_lines_generator(self.xy0_range, self.xy1_range, self.radius_range, self.thickness_range, self.color_range)
        while 2 * midline.x0 - 250 > 140:
            midline = middle_lines_generator(self.xy0_range, self.xy1_range, self.radius_range, self.thickness_range, self.color_range)
        width = randint(max(70, 2 * midline.x0 - 250), 140)

        img = middleline2drawing(img, midline, width=width, right_turn=True, color_range=self.color_range)

        angle, gas = middle_line2dir_gas(midline, pose)

        return img, angle, gas


class Noise():

    def __init__(self):
        pass


    def call(self, img):
        pass


class Shadows(Noise):

    def __init__(self, colors):
        if colors is None:
            raise Exception
        self.colors = colors
        super(Shadows, self).__init__()

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
        color = random.choice(self.colors)
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

        self.blur = blur
        self.gauss_blur = gauss_blur
        self.smooth = smooth
        self.smooth_more = smooth_more
        self.rank_filter = rank_filter
        super(Filter, self).__init__()

    def call(self, img):

        # TODO: no hardcoded value
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
        self.color_range = color_range
        super(NoiseLines, self).__init__()

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


class Background(Layer):

    def __init__(self, n_backgrounds, path, n_rot=1, n_res=1, n_crop=1, input_size=(250, 200)):
        self.n_backgrounds = n_backgrounds
        self.path = path
        self.n_rot = n_rot
        self.n_res = n_res
        self.n_crop = n_crop
        self.backgrounds = None
        self.input_size = input_size
        self.generate_all_backgrounds()
        super(Background, self).__init__()

    def generate_all_backgrounds(self):
        width, height = self.input_size

        # Choice of the background image
        backgrounds = []
        image_names = os.listdir(self.path)
        for index in tqdm(range(len(image_names)), desc='loading images'):
            background = Image.open(os.path.join(self.path, image_names[index])).convert('RGB')
            backgrounds.append(background)

        new_backgrounds = []
        for i in tqdm(range(len(backgrounds)), desc='rotating images'):
            background = backgrounds[i]
            for j in range(self.n_rot):
                b = background.copy()
                # Choice of a rotation angle
                angle_rotation = ANGLES[randint(0, len(ANGLES)-1)]
                b = b.rotate(angle_rotation)
                new_backgrounds.append(b)

        backgrounds = new_backgrounds
        print(len(backgrounds))

        new_backgrounds = []
        for i in tqdm(range(len(backgrounds)), desc='resizing images'):
            for j in range(self.n_res):
                b = backgrounds[i]
                # Choice of the resize size
                index = randint(0, len(WIDTHS)-1)
                new_width = WIDTHS[index]
                new_height = int(4 * new_width / 5)
                b = b.resize((new_width, new_height), PIL.Image.ANTIALIAS)
                new_backgrounds.append(b)

        backgrounds = new_backgrounds
        print(len(backgrounds))

        new_backgrounds = []
        for i in tqdm(range(len(backgrounds)), desc='loading images'):
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
        self.backgrounds = backgrounds


class Symmetric(Layer):

    def __init__(self, proba=0.5):
        self.proba = proba
        super(Symmetric, self).__init__()

    def call(self, img):

        width, height = img.size
        sym = img.copy()

        symmetry = False
        if random.random() < self.proba:
            from_points = [(0, 0), (width-1, 0), (width-1, height-1), (0, height-1)]
            new_points = [(width-1, 0), (0, 0), (0, height-1), (width-1, height-1)]
            coeffs = find_coeffs(new_points, from_points)
            sym = sym.transform((width, height), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
            symmetry = True
        return sym, symmetry


class Perspective(Layer):

    def __init__(self):
        super(Perspective, self).__init__()

    def call(self, img):

        width, height = img.size
        from_points = [(0, 0), (249, 0), (249, 199), (0, 199)]
        new_points = [(253-1, 0), (253+250-1, 0), (253*2+250-1, 70-1), (0, 70-1)]
        coeffs = find_coeffs(new_points, from_points)
        img = img.transform((250+253*2, 70), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
        return img


class Crop(Layer):

    def __init__(self):
        super(Crop, self).__init__()

    def call(self, img):
        width = img.width
        height = img.height
        x_shift = 253
        img = img.crop((x_shift-1, 0, width-x_shift-1, height))
        return img


def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = np.matrix(matrix, dtype=np.float)
    B = np.array(pb).reshape(8)

    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)
