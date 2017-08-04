import sys
sys.path.insert(0, '../src/')

from simulator import Simulator

simulator = Simulator()

from colors import Yellow, White, DarkShadow
from layers.layers import Background, DrawLines, Perspective, Crop

white = White()

simulator.add(Background(n_backgrounds=3, path='../ground_pics', input_size=(250, 200)))
simulator.add(DrawLines(input_size=(250, 200)))
simulator.add(Perspective())
simulator.add(Crop())

simulator.generate(n_examples=100, path='my_dataset')
