import sys
import os
import shutil

from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises

sys.path.insert(0, '../src/')
from layers.layers import *
from layers.noise import *
from colors import *


class TestLayer():

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

    # Layer
    def test_init_not_none(self):

        def instantiate_namenone():
            return Noise(name=None)

        def call_none():
            l = Noise()
            l.call(img=None)

        l = Noise(name='jacques chirac')
        assert_equal(l.name, 'jacques chirac')
        assert_not_equal(l.name, 'jacqueschirac')

        l = Noise(name='²&é"\'(-è_çà)=¹~#{[|`\^@`]})^¨$*ù!:;,?./§%µ£¤─')
        assert_equal(l.name, '²&é"\'(-è_çà)=¹~#{[|`\^@`]})^¨$*ù!:;,?./§%µ£¤─')

        assert_raises(ValueError, instantiate_namenone)
        assert_raises(ValueError, call_none)

    # Shadows
    def test_shadows(self):

        def instantiate_namenone():
            return Shadows(name=None)
        def instantiate_colornone():
            return Shadows(color=None)
        def call_none():
            l = Shadows()
            l.call(img=None)

        assert_raises(ValueError, instantiate_namenone)
        assert_raises(ValueError, instantiate_colornone)
        assert_raises(ValueError, call_none)

    # Filter
    def test_filter(self):

        def instantiate_namenone():
            return Filter(name=None)
        def instantiate_blurnone():
            return Filter(blur=None)
        def instantiate_sumgreater1():
            return Filter(blur=0.2, gauss_blur=0.2, smooth=0.2, smooth_more=0.2, rank_filter=0.5)
        def instantiate_paramnegative():
            return Filter(blur=1, gauss_blur=-0.5)
        def call_none():
            l = Filter()
            l.call(img=None)

        assert_raises(ValueError, instantiate_namenone)
        assert_raises(ValueError, instantiate_blurnone)
        assert_raises(ValueError, instantiate_sumgreater1)
        assert_raises(ValueError, instantiate_paramnegative)
        assert_raises(ValueError, call_none)

    # NoiseLines
    def test_noiselines(self):

        c = White()

        def instantiate_namenone():
            return NoiseLines(name=None, color_range=c)
        def instantiate_colornone():
            return NoiseLines(color_range=None)
        def instantiate_nlinesmaxnegative():
            return NoiseLines(n_lines_max=-1, color_range=c)
        def instantiate_nlinesmaxfloat():
            return NoiseLines(n_lines_max=0.2, color_range=c)
        def instantiate_probatoobig():
            return NoiseLines(proba_line=2, color_range=c)
        def instantiate_probanotfloat():
            return NoiseLines(proba_line='zidane', color_range=c)
        def call_none():
            l = NoiseLines(color_range=c)
            l.call(img=None)

        assert_raises(ValueError, instantiate_namenone)
        assert_raises(ValueError, instantiate_colornone)
        assert_raises(ValueError, instantiate_nlinesmaxnegative)
        assert_raises(ValueError, instantiate_nlinesmaxfloat)
        assert_raises(ValueError, instantiate_probatoobig)
        assert_raises(ValueError, instantiate_probanotfloat)
        assert_raises(ValueError, call_none)

        nl = NoiseLines(color_range=c, proba_line=1)
        assert_equal(nl.proba_line, 1)

    # Enhance
    def test_enhance(self):

        def instantiate_namenone():
            return Enhance(name=None)
        def instantiate_contrastnone():
            return Enhance(contrast=None)
        def instantiate_sumgreater1():
            return Enhance(contrast=0.2, brightness=0.2, sharpness=0.2, color=0.5)
        def instantiate_paramnegative():
            return Enhance(contrast=1, sharpness=-0.5)
        def instantiate_paramnegative2():
            return Enhance(contrast=2, sharpness=-1.5)
        def instantiate_paramstr():
            return Enhance(color='E')
        def call_none():
            l = Enhance()
            l.call(img=None)

        assert_raises(ValueError, instantiate_namenone)
        assert_raises(ValueError, instantiate_contrastnone)
        assert_raises(ValueError, instantiate_sumgreater1)
        assert_raises(ValueError, instantiate_paramnegative)
        assert_raises(ValueError, instantiate_paramnegative2)
        assert_raises(ValueError, instantiate_paramstr)
        assert_raises(ValueError, call_none)
