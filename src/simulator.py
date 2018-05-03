import os

from tqdm import tqdm
from random import randint

from layers.layers import Background, DrawLines, Symmetric


class Simulator():

    '''
        The simulator is most importantly a list of layers.
    '''

    def __init__(self, layers=None):

        from layers.layers import Layer

        if layers is None:
            layers = []
        if not isinstance(layers, list):
            raise ValueError('')
        if layers != [] and not all([isinstance(l, Layer) for l in layers]):
            raise ValueError('')

        self.layers = layers
        self.input_images = None

    def add(self, layer):
        self.layers.append(layer)

    def generate(self, n_examples, path):

        if n_examples <= 0:
            raise ValueError('n_examples must be strictly positive, not {}'.format(n_examples))
        if len(self.layers) == 0:
            raise ValueError('there are no layers in the simulator model')
        if not isinstance(self.layers[0], Background):
            raise ValueError('')
        if len(self.layers[0].backgrounds) == 0:
            raise ValueError('')

        self.input_images = self.layers[0].backgrounds

        if os.path.exists(path):
            print('The path `{}` already exists !'.format(path))
        else:
            os.makedirs(path)

        for i in tqdm(range(n_examples)):
            index = randint(0, len(self.input_images)-1)
            ii = self.input_images[index].copy()
            new_img, new_name = self.generate_one_image(ii)
            new_img.save(os.path.join(path, 'frame_' + str(i) + new_name))

    def generate_one_image(self, img):

        if img is None:
            raise ValueError('img must be different from None')

        sym = False

        im = img.copy()
        for layer in self.layers:
            if not isinstance(layer, Background):
                if isinstance(layer, DrawLines):
                    im, angle, gas = layer.call(im)
                elif isinstance(layer, Symmetric):
                    im, sym = layer.call(im)
                else:
                    im = layer.call(im)

        if sym:
            angle = -angle
        name = '_gas_' + str(gas) + '_dir_' +  str(angle) + '.jpg'
        return im, name


    def summary(self):

        summaries = [layer.summary() for layer in self.layers]

        s = 'Summary:\nNumber of layers: {}\n{}'.format(len(self.layers), '\n'.join(summaries))
        return s
