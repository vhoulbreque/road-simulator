import sys
import os
import shutil

from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises

sys.path.insert(0, '../src/')
from simulator import *
from layers.layers import *
from colors import *


class TestSimulator():

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

    # Simulator
    def test_init_not_none(self):

        def instantiate_none():
            return Simulator(layers=None)
        def instantiate_layerstuple():
            return Simulator(layers=(0, 9))
        def instantiate_layersemptylist():
            return Simulator(layers=[])
        def instantiate_layersliststr():
            return Simulator(layers=['E', 'F'])
        def instantiate_layernobackgroundfirst():
            l1 = Perspective()
            l2 = Crop()
            return Simulator(layers=[l1, l2])
        def instantiate_backgroundemptylist():
            l1 = Background(n_backgrounds=1, path='../ground_pics')
            l1.backgrounds = []
            l2 = Crop()
            return Simulator(layers=[l1, l2])

        assert_raises(ValueError, instantiate_none)
        assert_raises(ValueError, instantiate_layerstuple)
        assert_raises(ValueError, instantiate_layersemptylist)
        assert_raises(ValueError, instantiate_layersliststr)
        assert_raises(ValueError, instantiate_layernobackgroundfirst)
        assert_raises(ValueError, instantiate_backgroundemptylist)

        l1 = Background(n_backgrounds=3, path='../ground_pics', width_range=[749, 750])
        l2 = Crop()
        l3 = Perspective()
        l4 = Symmetric()

        simulator = Simulator(layers=[l1, l2, l3, l4])
        assert_equal([layer.name for layer in simulator.layers], ['Background', 'Crop', 'Perspective', 'Symmetric'])
