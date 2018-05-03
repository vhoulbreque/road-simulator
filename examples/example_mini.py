from roadsimulator.simulator import Simulator
from roadsimulator.colors import Yellow, White, DarkShadow
from roadsimulator.layers.layers import Background, DrawLines, Perspective, Crop


simulator = Simulator()

white = White()

simulator.add(Background(n_backgrounds=3, path='../ground_pics', input_size=(250, 200)))
simulator.add(DrawLines(input_size=(250, 200)))
simulator.add(Perspective())
simulator.add(Crop())

simulator.generate(n_examples=100, path='my_dataset')
