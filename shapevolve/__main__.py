"""Application entry point."""

import os
import sys

from main import main

if __name__ == '__main__':
    sys.path.append(os.path.abspath("../"))
    main()

