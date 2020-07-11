"""Application entry point."""

import os
import sys
import warnings
from multiprocessing import freeze_support

if __name__ == '__main__':
    # Handle windows multiprocessing errors.
    freeze_support()
    # Remove automatic deprecation warning for matplotlib
    warnings.filterwarnings("ignore", "(?s).*MATPLOTLIBDATA.*", category=UserWarning)
    # Add library to system path.
    sys.path.append(os.path.abspath("../"))

from main import main

if __name__ == '__main__':
    main()

