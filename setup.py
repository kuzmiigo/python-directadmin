#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(name='python-directadmin', \
      version='0.3', \
      description='Python implementation of Directadmin\'s Web API', \
      author='Andrés Gattinoni', \
      author_email='andresgattinoni@gmail.com', \
      url='http://code.google.com/p/python-directadmin/', \
      packages=['directadmin'], \
      data_files=[('directadmin', ['LICENSE'])], \
      scripts=['scripts/da_suspension', 'scripts/da_console'], \
      license='GPL v.3', \
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
