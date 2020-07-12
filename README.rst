Shapevolve
==========

A genetic algorithm to recreate artworks using simple shapes, with
Python 3.

Evan Zheng, July 2020.

Initially designed on Google Colab with Jupyter Notebooks. Module built
with assistance from PyCharm.

.. image:: ./images/starrynightgif.gif

Sample Results:
---------------

The Starry Night:

.. image:: ./images/starrynight.png_result.png

Mona Lisa:

.. image:: ./images/monalisa.jpg_result.png

Girl with a Pearl Earring:

.. image:: ./images/pearlearring.jpg_result.png

The Great Wave off Kanagawa:

.. image:: ./images/greatwave.jpg_result.png

How to install and use:
-----------------------
Standalone executable: (Windows)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Head over to `releases`_ and download the latest executable, ``shapevolve.exe``.

In the command line:

Change the directory using ``cd`` to where the executable is located.

Then, run ``shapevolve.exe path/to/image_file.png`` to run the program with an image as input.

You can also run ``shapevolve.exe -h`` to view additional options.

Module:
~~~~~~~

Install shapevolve from PyPI using the following command:

``pip install shapevolve``

Here is some sample code to demonstrate how to use the module.

::

   from shapevolve.evolver import Evolver
   from PIL import Image

   evolver = Evolver(Image.open("path/to/image.png")) # Sets up the Evolver object.

   genome = evolver.evolve() # Evolves the genome.

   image = genome.render_scaled_image() # Gets a numpy array that represents the evolved image.

   genome.save_genome("path/to/save_checkpoint.pkl") # Saves the genome for later use.

More sample code can be found in ``samples.py``, `here.`_

Libraries and APIs used:
------------------------

Third-party libraries used:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `NumPy`_ for numerical computation with matrices
-  `ColorThief`_ for grabbing color palettes from images
-  `Scikit-Image`_ for computing image simularity
-  `OpenCV`_ for building images from circles
-  `Pillow`_ for image preprocessing
-  `Matplotlib`_ for image display
-  `PyInstaller`_ for building an executable file.

Built-in libraries used:
~~~~~~~~~~~~~~~~~~~~~~~~

-  `Pickle`_ for checkpoint saves and loads.
-  `Argparse`_ for the CLI interface.

License:
--------

See `LICENSE`_ file.

Thanks:
-------

Ahmed Khalf’s `Circle-Evolution`_ module provided a great deal of
inspiration.

.. _releases: https://github.com/richmondvan/Shapevolve/releases
.. _here.: https://github.com/richmondvan/Shapevolve/blob/master/shapevolve/samples.py
.. _NumPy: https://numpy.org/
.. _ColorThief: https://github.com/fengsp/color-thief-py
.. _Scikit-Image: https://scikit-image.org/
.. _OpenCV: https://opencv.org/
.. _Pillow: https://github.com/python-pillow/Pillow
.. _Matplotlib: https://matplotlib.org/
.. _PyInstaller: https://www.pyinstaller.org/
.. _Pickle: https://docs.python.org/3/library/pickle.html
.. _Argparse: https://docs.python.org/3/library/argparse.html
.. _LICENSE: https://github.com/richmondvan/Shapevolve/blob/master/LICENSE
.. _Circle-Evolution: https://github.com/ahmedkhalf/Circle-Evolution
