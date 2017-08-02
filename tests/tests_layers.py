import sys
import os
import shutil

from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises

sys.path.insert(0, '../src/')
from layers.layers import *
from colors import *


class TestLayer():

    @classmethod
    def setup_class(klass):
        os.makedirs('test_empty_folder')

    @classmethod
    def teardown_class(klass):
        shutil.rmtree('test_empty_folder', ignore_errors=True)

    def setUp(self):
        """This method is run once before _each_ test method is executed"""

    def teardown(self):
        """This method is run once after _each_ test method is executed"""

    # Layer
    def test_layer(self):

        def instantiate_none():
            return Layer(name=None)

        def call_none():
            l = Layer()
            l.call(img=None)

        l = Layer(name='jacques chirac')
        assert_equal(l.name, 'jacques chirac')
        assert_not_equal(l.name, 'jacqueschirac')

        l = Layer(name='²&é"\'(-è_çà)=¹~#{[|`\^@`]})^¨$*ù!:;,?./§%µ£¤─')
        assert_equal(l.name, '²&é"\'(-è_çà)=¹~#{[|`\^@`]})^¨$*ù!:;,?./§%µ£¤─')

        assert_raises(ValueError, instantiate_none)
        assert_raises(ValueError, call_none)


    # DrawLines
    def test_drawlines(self):

        def instantiate_name_none():
            c = White()
            return DrawLines(name=None, xy0_range=[(20, 20)], xy1_range=[(20, 20)], radius_range=[10, 11], thickness_range=[2, 10], color_range=c)
        def instantiate_noparam():
            return DrawLines()
        def instantiate_rangenone():
            c = White()
            return DrawLines(xy0_range=None, xy1_range=[(20, 20)], radius_range=[10, 11], thickness_range=[2, 10], color_range=c)
        def instantiate_rangesnone():
            c = White()
            return DrawLines(xy0_range=None, xy1_range=None, radius_range=None, thickness_range=None, color_range=c)
        def instantiate_emptylist():
            c = White()
            return DrawLines(xy0_range=[], xy1_range=None, radius_range=None, thickness_range=None, color_range=c)
        def instantiate_colornone():
            return DrawLines(xy0_range=[(20, 20)], xy1_range=[(20, 20)], radius_range=[10, 11], thickness_range=[2, 10], color_range=None)
        def instantiate_xy0notuple():
            c = White()
            return DrawLines(xy0_range=[20, 20], xy1_range=[(20, 20)], radius_range=[10, 11], thickness_range=[2, 10], color_range=c)
        def instantiate_thicknesstuple():
            c = White()
            return DrawLines(xy0_range=[(20, 20)], xy1_range=[(20, 20)], radius_range=[10, 11], thickness_range=[(2, 10)], color_range=c)
        def call_none():
            c = White()
            d = DrawLines(xy0_range=[(20, 20)], xy1_range=[(20, 20)], radius_range=[10, 11], thickness_range=[2, 10], color_range=c)
            d.call(None)

        assert_raises(ValueError, instantiate_name_none)
        assert_raises(TypeError, instantiate_noparam)
        assert_raises(ValueError, instantiate_rangenone)
        assert_raises(ValueError, instantiate_rangesnone)
        assert_raises(ValueError, instantiate_emptylist)
        assert_raises(ValueError, instantiate_colornone)
        assert_raises(ValueError, instantiate_xy0notuple)
        assert_raises(ValueError, instantiate_thicknesstuple)
        assert_raises(ValueError, call_none)

    # Symmetric
    def test_symmetric(self):

        def instantiate_name_none():
            return Symmetric(name=None)
        def instantiate_probaNone():
            return Symmetric(proba=None)
        def instantiate_probabig():
            return Symmetric(proba=1.00001)
        def instantiate_probastr():
            return Symmetric(proba='0.5')
        def call_none():
            d = Symmetric()
            d.call(None)

        assert_raises(ValueError, instantiate_name_none)
        assert_raises(ValueError, instantiate_probaNone)
        assert_raises(ValueError, instantiate_probabig)
        assert_raises(ValueError, instantiate_probastr)
        assert_raises(ValueError, call_none)

    # Perspective
    def test_perspective(self):

        def instantiate_name_none():
            return Perspective(name=None)
        def call_none():
            d = Perspective()
            d.call(None)

        assert_raises(ValueError, instantiate_name_none)
        assert_raises(ValueError, call_none)

    # Crop
    def test_crop(self):

        def instantiate_name_none():
            return Crop(name=None)
        def call_none():
            d = Crop()
            d.call(None)

        assert_raises(ValueError, instantiate_name_none)
        assert_raises(ValueError, call_none)


    # Background
    def test_background(self):

        def instantiate_name_none():
            return Background(n_backgrounds=1, path='../ground_pics', name=None)
        def instantiate_nobackgrounds():
            return Background(n_backgrounds=0, path='../ground_pics')
        def instantiate_foldernotexist():
            return Background(n_backgrounds=10, path='ground_pics')
        def instantiate_folderisfile():
            return Background(n_backgrounds=10, path='../ground_pics/20170617_102623.jpg')
        def instantiate_nresnegative():
            return Background(n_backgrounds=10, path='../ground_pics', n_res=-1)
        def instantiate_inputsizenotuple():
            return Background(n_backgrounds=10, path='../ground_pics', input_size=222)
        def instantiate_inputsizeno2():
            return Background(n_backgrounds=10, path='../ground_pics', input_size=(222, 111, 444))
        def instantiate_inputsizenegative():
            return Background(n_backgrounds=10, path='../ground_pics', input_size=(222, -111))
        def instantiate_widthnone():
            return Background(n_backgrounds=10, path='../ground_pics', width_range=None)
        def instantiate_widthnotlist():
            return Background(n_backgrounds=10, path='../ground_pics', width_range=(99, 100))
        def instantiate_widthemptylist():
            return Background(n_backgrounds=10, path='../ground_pics', width_range=[])
        def call_none():
            d = Crop()
            d.call(None)

        assert_raises(ValueError, instantiate_name_none)
        assert_raises(ValueError, instantiate_nobackgrounds)
        assert_raises(ValueError, instantiate_foldernotexist)
        assert_raises(ValueError, instantiate_folderisfile)
        assert_raises(ValueError, instantiate_nresnegative)
        assert_raises(ValueError, instantiate_inputsizenotuple)
        assert_raises(ValueError, instantiate_inputsizeno2)
        assert_raises(ValueError, instantiate_inputsizenegative)
        assert_raises(ValueError, instantiate_widthnone)
        assert_raises(ValueError, instantiate_widthnotlist)
        assert_raises(ValueError, instantiate_widthemptylist)
        assert_raises(ValueError, call_none)
