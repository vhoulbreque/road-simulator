from setuptools import setup
from setuptools import find_packages

setup(name='roadsimulator',
      version='0.1',
      description='Easy-to-use road simulator for little self-driving cars',
      url='https://github.com/vinzeebreak/road_simulator',
      author='Ironcar Team',
      author_email='vincenthoulbreque+ironcar@gmail.com',
      license='MIT',
      install_requires=[
          'Pillow==5.1.0',
          'tqdm==4.23.2',
          'numpy==1.14.2'
      ],
      extras_require={
          'tests': ['nose==1.3.7'],
      },
      zip_safe=False,
      packages=find_packages())
