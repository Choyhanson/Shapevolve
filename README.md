# Shapevolve
A genetic algorithm to recreate artworks using simple shapes, with Python 3.

Evan Zheng, July 2020.

Initially designed on Google Colab with Jupyter Notebooks. Module built with assistance from PyCharm. Work-in-progress.

## How to use:

### CLI interface:
This has only been tested with Python 3.8.

Change the directory to where `__main__.py` is located. Then, run the following command:

`python __main__.py path/to/image_file.png`

You can also run `help` for more information on command line options.

### Module:
Here is some sample code to demonstrate how to use the module.

```
from shapevolve.evolver import Evolver
from PIL import Image

evolver = Evolver(Image.open("path/to/image.png")) # Sets up the Evolver object.

genome = evolver.evolve() # Evolves the genome.

image = genome.render_scaled_image() # Gets a numpy array that represents the evolved image.

genome.save_genome("path/to/save_checkpoint.pkl") # Saves the genome for later use.
```

More sample code can be found in `samples.py`, [here.](https://github.com/richmondvan/Shapevolve/blob/master/circlevolve/samples.py)

## Libraries and APIs used:

### Third-party libraries used:
- [NumPy](https://numpy.org/) for numerical computation with matrices
- [ColorThief](https://github.com/fengsp/color-thief-py) for grabbing color palettes from images
- [Scikit-Image](https://scikit-image.org/) for computing image simularity
- [OpenCV](https://opencv.org/) for building images from circles
- [Pillow](https://github.com/python-pillow/Pillow) for image preprocessing
- [Matplotlib](https://matplotlib.org/) for image display

### Built-in libraries used:
- [Pickle](https://docs.python.org/3/library/pickle.html) for checkpoint saves and loads.
- [Argparse](https://docs.python.org/3/library/argparse.html) for the CLI interface.

## License:
See [LICENSE](https://github.com/richmondvan/Shapevolve/blob/master/LICENSE) file.

## Thanks:
Ahmed Khalf's [Circle-Evolution](https://github.com/ahmedkhalf/Circle-Evolution) module provided a great deal of inspiration.
