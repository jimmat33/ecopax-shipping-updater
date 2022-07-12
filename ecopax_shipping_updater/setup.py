'''
docstr
'''
# pylint: disable=W0611
# pylint: disable=W0402
from distutils.core import setup
import py2exe

py2exe.patch_distutils()

setup(windows=[
    {'script': 'ecopax_shipping_updater.py',
     'icon_resources': [(1, 'gui_icon.ico')],
     'dest_base': 'Ecopax Shipping Update Tool'}])
