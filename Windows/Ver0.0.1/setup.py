from distutils.core import setup
import py2exe

images = [('images'), ['C:\\Users\\hanjiung\\project\\test\\image\\shield_warning.png', ]]

setup(
    windows=['main.py', 'CheckFileFrame.py'],
    options=
    {
        'py2exe':
        {
            'includes':["PyQt5", "PyQt5.QtGui", 'qt_material','win10toast','time','PyQt5.QtWidgets' ],
            'bundle_files':2,
        }
    },
    zipfile=None
)
