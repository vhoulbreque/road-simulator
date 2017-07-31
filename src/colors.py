class Color():
    '''
        Root Object of Colors.
        By default, does nothing.
    '''

    def __init__(self, name=''):
        if name is None:
            raise ValueError('name must be different from None')
        self.name = name


class ColorRange(Color):

    def __init__(self, name='', red=None, green=None, blue=None, samples=None,
                    red_range=0, green_range=0, blue_range=0, colors=None):


        if name is None:
            raise ValueError('name must be different from None')

        super(Color, self).__init__()

        self.name = name
        self.colors = []

        if not colors:
            if samples is not None:
                if not all([color >= 0 for color in [red_range, green_range, blue_range]]):
                    raise ValueError('All ranges must be positive, not {}'.format(str([red_range, green_range, blue_range])))

                for (r, g, b) in samples:
                    for red in range(max(0, r - red_range), min(r + red_range, 255)):
                        for green in range(max(0, g - green_range), min(g + green_range, 255)):
                            for blue in range(max(0, b - blue_range), min(b + blue_range, 255)):
                                t = (red, green, blue)
                                self.colors.append(t)
            else:
                if not all([color is not None for color in [red, green, blue]]):
                    raise ValueError('red, green and blue must be different from None, not {}'.format([red, green, blue]))
                if not all([isinstance(color, tuple) and len(color) == 2 and 0 <= color[0] <= 255 for color in [red, green, blue]]):
                    raise ValueError('red, green and blue must be tuples of length 2 and their values must be between 0 and 255, not {}'.format([red, green, blue]))
                red_low, red_high = red
                green_low, green_high = green
                blue_low, blue_high = blue
                for red in range(red_low, red_high + 1):
                    for green in range(green_low, green_high + 1):
                        for blue in range(blue_low, blue_high + 1):
                            t = (red, green, blue)
                            self.colors.append(t)
        else:
            self.colors = colors

        self.red = red
        self.green = green
        self.blue = blue

        self.samples = samples

        self.red_range = red_range
        self.green_range = green_range
        self.blue_range = blue_range


    def __add__(self, color_range):
        name = self.name + '__' + color_range.name
        colors = list(set(self.colors + color_range.colors))
        return ColorRange(name=name, colors=colors)


class Yellow(ColorRange):
    '''
        Color Yellow. This color is created from sample taken on pictures of the
        ground in the hangar.
    '''


    def __init__(self, name='yellow'):

        local_samples = [(207, 188, 104), (203, 190, 125), (234, 214, 126),
                         (225, 212, 141), (248, 244, 146), (238, 215, 122),
                         (250, 245, 219), (250, 245, 199)]

        color = ColorRange(samples=local_samples, red_range=5, green_range=5,
                            blue_range=5)
        # super(ColorRange, self).__init__(samples=local_samples, red_range=5,
        #                                      green_range=5, blue_range=5)

        self.name = name
        self.samples = color.samples

        self.red = color.red
        self.green = color.green
        self.blue = color.blue

        self.red_range = color.red_range
        self.green_range = color.green_range
        self.blue_range = color.blue_range

        self.colors = color.colors


class White(ColorRange):
    '''
        Color White. This color was created by hand, by looking at
        http://www.rapidtables.com/web/color/RGB_Color.htm
    '''

    def __init__(self, name='white'):

        if name is None:
            raise ValueError('name must be different from None')

        color = ColorRange(red=(230, 255), green=(230, 255), blue=(190, 255))
        # super(ColorRange, self).__init__(red=(230, 255), green=(230, 255),
        #                                     blue=(190, 255))

        self.name = name
        self.samples = color.samples

        self.red = color.red
        self.green = color.green
        self.blue = color.blue


        self.red_range = color.red_range
        self.green_range = color.green_range
        self.blue_range = color.blue_range

        self.colors = color.colors


class DarkShadow(ColorRange):
    '''
        Shadow Colors. Created by looking at
        http://www.rapidtables.com/web/color/RGB_Color.htm
    '''

    def __init__(self, name='darkshadow'):

        if name is None:
            raise ValueError('name must be different from None')

        super(ColorRange, self).__init__()

        colors = []
        for i in range(0, 150):
            for j in range(0, 10):
                for k in range(0, 10):
                    t1 = (i, i+j, i+k)
                    t2 = (i+j, i, i+k)
                    t3 = (i+j, i+k, i)
                    colors.append(t1)
                    colors.append(t2)
                    colors.append(t3)

        for i in range(0, 30):
            for j in range(0, 30):
                for k in range(0, 30):
                    t = (i, j, k)
                    if t not in colors:
                        colors.append(t)

        self.colors = colors
        self.name = name
