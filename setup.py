#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from distutils.core import setup

if not hasattr(sys, 'version_info') or sys.version_info < (2,5,0):
    raise SystemExit("python-directadmin requires Python 2.5 or higher to work")

_description = "python-directadmin is a Python implementation " \
               "of Directadmin Panel Control Web API."

setup(name='python-directadmin', \
      version='0.3', \
      description='Python implementation of Directadmin\'s Web API', \
      long_description=_description, \
      author='Andrés Gattinoni', \
      author_email='andresgattinoni@gmail.com', \
      license='GPL v.3', \
      url='http://code.google.com/p/python-directadmin/', \
      download_url='http://code.google.com/p/python-directadmin/downloads/list', \
      packages=['directadmin'], \
      scripts=['scripts/da_suspension', 'scripts/da_console'], \
      platforms=['POSIX'], \
      classifiers=[
        'Development Status :: 3 - Alpha', \
        'Environment :: Console', \
        'Environment :: Web Environment', \
        'Intended Audience :: Developers', \
        'License :: OSI Approved :: GNU General Public License (GPL)', \
        'Operating System :: POSIX', \
        'Programming Language :: Python', \
        'Topic :: Internet', \
        'Topic :: Software Development :: Libraries :: Python Modules', \
        'Topic :: System :: Monitoring' \
      ])
