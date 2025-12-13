# Runtime hook for VMM-FRC
# This hook runs before the main application starts

import os
import sys

# Suppress Qt plugin warnings
os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.*=false'

# Set VTK environment for PyVista
os.environ['VTK_SMP_BACKEND_IN_USE'] = 'Sequential'
