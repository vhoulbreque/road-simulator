'''
    These basic objects include lines and objects needed to build these lines
    (such as circles)

'''

from math import sqrt


class RoadLine:
    '''
        This is a RoadLine. In fact, a RoadLine is not a real line (except when
        the road is straight). A RoadLine represents the line of the center of
        the road. Like this, it is easier to create the 2 real lines that
        constitute the borders of the road.
    '''

    def __init__(self, x0, y0, x1, y1, radius, thickness=10, color=(255, 255, 255)):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.radius = radius
        self.thickness = thickness
        self.color = color

    def copy(self):
        new_line = RoadLine(self.x0, self.y0, self.x1, self.y1, self.radius,
                                thickness=self.thickness, color=self.color)
        return new_line

    def __add__(self, scalar):
        return RoadLine(self.x0 + scalar, self.y0, self.x1 + scalar, self.y1,
                        self.radius, thickness=self.thickness, color=self.color)

    def __sub__(self, scalar):
        return RoadLine(self.x0 - scalar, self.y0, self.x1 - scalar, self.y1,
                        self.radius, thickness=self.thickness, color=self.color)

    def print_line(self):
        print(' point0 : ', self.x0, self.y0, ' point1: ', self.x1, self.y1,
                ' radius: ', self.radius , ' color: ', self.color,
                ' thickness: ', self.thickness)


class Circle:

    def __init__(self, center, radius, thickness=10, color=(255, 255, 255),
                    plain=300, empty=0):

        if thickness <= 0:
            raise ValueError('thickness must be stricly positive (not {})'.format(thickness))
        if color is None:
            raise ValueError('color must be different from None')
            
        self.center = center
        self.radius = radius
        self.thickness = thickness
        self.color = color
        self.plain = plain
        self.empty = empty


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, pt):
        return Point(self.x + pt.x, self.y + pt.y)

    def __sub__(self, pt):
        return Point(self.x - pt.x, self.y - pt.y)

    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def norm(self):
        return sqrt(float(self.x)*float(self.x) + float(self.y)*float(self.y))
