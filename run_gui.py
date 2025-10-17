#!/usr/bin/env python3
"""Run the ACSC GUI"""

import sys
import os

sys.path.insert(0, '/workspace')
os.environ['QT_QPA_PLATFORM'] = 'xcb'

from acsc.gui import main

if __name__ == "__main__":
    main()