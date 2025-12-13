# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for VMM-FRC (Virtual Microstructure Modeling for Fiber Reinforced Polymer Composites)
"""

import sys
from pathlib import Path
import PySide6

block_cipher = None

# Get the project root directory
project_root = Path(SPECPATH)

# Get PySide6 installation path for plugins
pyside6_path = Path(PySide6.__file__).parent

a = Analysis(
    ['run_gui.py'],
    pathex=[str(project_root)],
    binaries=[
        # InSegt KM-Tree DLL
        (str(project_root / 'vmm' / 'insegt' / 'models' / 'km_dict_lib.dll'), 'vmm/insegt/models'),
    ],
    datas=[
        # Include PySide6 plugins (required for Qt to work)
        (str(pyside6_path / 'plugins' / 'platforms'), 'PySide6/plugins/platforms'),
        (str(pyside6_path / 'plugins' / 'styles'), 'PySide6/plugins/styles'),
        (str(pyside6_path / 'plugins' / 'imageformats'), 'PySide6/plugins/imageformats'),
        # Include assets (parameters and logo)
        (str(project_root / 'assets'), 'assets'),
        # Include InSegt modules
        (str(project_root / 'vmm' / 'insegt'), 'vmm/insegt'),
    ],
    hiddenimports=[
        # NumPy and SciPy
        'numpy',
        'numpy.core._methods',
        'numpy.lib.format',
        'scipy',
        'scipy.ndimage',
        'scipy.special',
        'scipy.special._ufuncs_cxx',
        'scipy.linalg.cython_blas',
        'scipy.linalg.cython_lapack',
        'scipy.sparse.csgraph._validation',

        # Numba
        'numba',
        'numba.core.types',

        # Pandas
        'pandas',
        'pandas._libs.tslibs.timedeltas',

        # Image processing
        'skimage',
        'skimage.io',
        'skimage.filters',
        'skimage.morphology',
        'cv2',

        # PyDICOM
        'pydicom',
        'pydicom.encoders.gdcm',
        'pydicom.encoders.pylibjpeg',

        # 3D visualization
        'pyvista',
        'pyvistaqt',
        'vtkmodules',
        'vtkmodules.all',
        'vtkmodules.util.numpy_support',
        'vtkmodules.qt.QVTKRenderWindowInteractor',

        # Qt/PySide6
        'PySide6',
        'PySide6.QtCore',
        'PySide6.QtWidgets',
        'PySide6.QtGui',

        # Matplotlib
        'matplotlib',
        'matplotlib.backends.backend_qt5agg',

        # OpenPyXL
        'openpyxl',

        # VMM modules
        'vmm',
        'vmm.analysis',
        'vmm.io',
        'vmm.gui',
        'vmm.simulation',

        # InSegt modules
        'vmm.insegt',
        'vmm.insegt.models',
        'vmm.insegt.models.kmdict',
        'vmm.insegt.models.gaussfeat',
        'vmm.insegt.models.utils',
        'vmm.insegt.fiber_model',
        'vmm.insegt.annotators',
        'vmm.insegt.annotators.dual_panel_annotator',
        'vmm.insegt.annotators.insegtannotator',
        'vmm.insegt.annotators.annotator',

        # Pillow
        'PIL',
        'PIL.Image',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['runtime_hook.py'],
    excludes=[
        'tkinter',
        '_tkinter',
        'tcl',
        'tk',
        # Exclude PyQt5 to avoid Qt binding conflict with PySide6
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtWidgets',
        'PyQt5.QtGui',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VMM-FRC',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/vmm_logo.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='VMM-FRC',
)
