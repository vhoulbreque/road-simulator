


class Color():

    def __init__(self, name=None):
        self.name = name


class ColorRange(Color):

    def __init__(self, name=None, red=None, green=None, blue=None, samples=None, red_range=0, green_range=0, blue_range=0, colors=None):

        super(Color, self).__init__()

        self.name = name
        self.colors = []

        if not colors:
            if samples is not None:
                if not all([color >= 0 for color in [red_range, green_range, blue_range]]):
                    raise Exception

                for (r, g, b) in samples:
                    for red in range(max(0, r - red_range), min(r + red_range, 255)):
                        for green in range(max(0, g - green_range), min(g + green_range, 255)):
                            for blue in range(max(0, b - blue_range), min(b + blue_range, 255)):
                                t = (red, green, blue)
                                self.colors.append(t)
            else:
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


    def __init__(self, name='yellow'):

        local_samples = [(207, 188, 104), (203, 190, 125), (234, 214, 126), (225, 212, 141),
                       (248, 244, 146), (238, 215, 122), (250, 245, 219), (250, 245, 199)]

        color = ColorRange(samples=local_samples, red_range=5, green_range=5, blue_range=5)
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


    def __init__(self, name='white'):

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


    def __init__(self, name='darkshadow'):

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
