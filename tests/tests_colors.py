import sys

from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises

sys.path.insert(0, '../src/')
from colors import *


class TestColor():

    @classmethod
    def setup_class(klass):
        pass

    @classmethod
    def teardown_class(klass):
        pass

    def setUp(self):
        """This method is run once before _each_ test method is executed"""

    def teardown(self):
        """This method is run once after _each_ test method is executed"""

    # Color
    def test_init_not_none(self):

        def instantiate_none():
            return Color(name=None)

        c = Color(name='jacques chirac')
        assert_equal(c.name, 'jacques chirac')
        assert_not_equal(c.name, 'jacqueschirac')

        c = Color(name='²&é"\'(-è_çà)=¹~#{[|`\^@`]})^¨$*ù!:;,?./§%µ£¤─')
        assert_equal(c.name, '²&é"\'(-è_çà)=¹~#{[|`\^@`]})^¨$*ù!:;,?./§%µ£¤─')

        assert_raises(ValueError, instantiate_none)

    # ColorRange
    def test_colorrange(self):

        def instantiate_name():
            return ColorRange(name=None)
        def instantiate_redrange():
            return ColorRange(samples=[(234, 123, 11)], red_range=-1)
        def instantiate_noparam():
            return ColorRange()
        def instantiate_notuple():
            return ColorRange(red=(123, 222), green=111, blue=(111, 167))
        def instantiate_outofbounds():
            return ColorRange(red=(123, 222), green=(111, 256), blue=(111, 167))
        def instantiate_reverseorder():
            return ColorRange(red=(223, 222), green=(111, 211), blue=(111, 167))

        c1 = ColorRange(red=(123, 150), green=(123, 128), blue=(10, 16))
        assert_equal(len(c1.colors), len(list(set(c1.colors))))

        c2 = ColorRange(red=(1, 11), green=(111, 122), blue=(26, 211))
        c3 = c1 + c2
        assert_equal(len(c1.colors + c2.colors), len(c3.colors))

        assert_raises(ValueError, instantiate_name)
        assert_raises(ValueError, instantiate_redrange)
        assert_raises(ValueError, instantiate_noparam)
        assert_raises(ValueError, instantiate_notuple)
        assert_raises(ValueError, instantiate_outofbounds)
        assert_raises(ValueError, instantiate_reverseorder)

    # Yellow
    def test_init_yellow(self):

        def instantiate_none():
            return Yellow(name=None)

        samples = [(207, 188, 104), (203, 190, 125), (234, 214, 126),
                    (225, 212, 141), (248, 244, 146), (238, 215, 122),
                    (250, 245, 219), (250, 245, 199)]

        c = Yellow()
        assert_equal(c.name, 'yellow')
        assert_not_equal(c.name, '')

        assert_equal(c.red_range, 5)
        assert_equal(c.green_range, 5)
        assert_equal(c.blue_range, 5)
        assert_equal(c.samples, samples)

        assert_raises(ValueError, instantiate_none)

    # Shadows
    def test_init_shadows(self):
        c = DarkShadow()
        assert_equal(c.name, 'darkshadow')
        assert_not_equal(c.name, '')

        assert_equal(len(c.colors), len(list(set(c.colors))))


    def test_sum(self):
        c1 = Yellow()
        c2 = White()
        c3 = c1 + c2

        assert_equal(len(list(set(c1.colors + c2.colors))), len(list(set(c3.colors))))
        assert_equal(c3.name, 'yellow__white')
