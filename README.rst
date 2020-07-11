Shapevolve
==========

`View on Github. <https://github.com/richmondvan/Shapevolve>`_

`See the website and API reference. <https://richmondvan.github.io/shapevolve/>`_

A genetic algorithm to recreate artworks using simple shapes, with
Python 3.

Evan Zheng, July 2020.

Initially designed on Google Colab with Jupyter Notebooks. Module built
with assistance from PyCharm. Work-in-progress.


Sample images:
--------------

The Starry Night:

.. image:: ./_images/starrynight.png_result.png

Mona Lisa:

.. image:: ./_images/monalisa.jpg_result.png

Girl with a Pearl Earring:

.. image:: ./_images/pearlearring.jpg_result.png

The Great Wave off Kanagawa:

.. image:: ./_images/greatwave.jpg_result.png


How to use:
-----------

CLI interface:
~~~~~~~~~~~~~~

This has only been tested with Python 3.8.

Change the directory to where ``__main__.py`` is located. Then, run the
following command:

``python __main__.py path/to/image_file.png``

You can also run ``python __main__.py -h`` for more information on command line options.

Module:
~~~~~~~

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

.. _here.: https://github.com/richmondvan/Shapevolve/blob/master/circlevolve/samples.py
.. _NumPy: https://numpy.org/
.. _ColorThief: https://github.com/fengsp/color-thief-py
.. _Scikit-Image: https://scikit-image.org/
.. _OpenCV: https://opencv.org/
.. _Pillow: https://github.com/python-pillow/Pillow
.. _Matplotlib: https://matplotlib.org/
.. _Pickle: https://docs.python.org/3/library/pickle.html
.. _Argparse: https://docs.python.org/3/library/argparse.html
.. _LICENSE: https://github.com/richmondvan/Shapevolve/blob/master/LICENSE
.. _Circle-Evolution: https://github.com/ahmedkhalf/Circle-Evolution