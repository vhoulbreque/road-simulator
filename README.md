# Road Simulator

The road_simulator is part of the 'ironcar' project.
To see what the ironcar project is, go to the [ironcar repository](https://github.com/vinzeebreak/ironcar).

This simulator generates 'false' pictures of a road as seen by a 1/10th car with a wide angle camera. We used it to get (250 * 70) RGB dimensional images. It is quite fast (I mean, at least faster than driving the car ourselves), and far more accurate in the learning process (less approximations of curves etc).

These are examples of what can be generated (very simply):

![dashed line 1](images/example0.jpg)  ![dashed line 2](images/example1.jpg)  ![dashed line 3](images/example2.jpg)  ![dashed line 4](images/example4.jpg)  

![plain line 1](images/example5.jpg)  ![plain line 2](images/example6.jpg)  ![plain line 3](images/example7.jpg)  ![plain line 4](images/example8.jpg)  


## Getting started

```python
import sys
sys.path.insert(0, '../src/')
```

In this simulator, each model of generation is composed of layers. The simpliest type of generator is the `Simulator`.
```python
from simulator import Simulator

simulator = Simulator()
```

Then, we add layers to our generator:

```python
from colors import White
from layers.layers import Background, DrawLines, Perspective, Crop

white = White()

simulator.add(Background(n_backgrounds=3, path='../ground_pics', input_size=(250, 200)))
simulator.add(DrawLines(input_size=(250, 200), color_range=white))
simulator.add(Perspective())
simulator.add(Crop())
```

White object gives a range of white-ish colors to draw the lines. They may not appear exactly white on the images.  
Now, let's generate the images. We just need to write:

```python
simulator.generate(n_examples=100, path='my_dataset')
```
