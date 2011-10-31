.. _installation:

************
Installation
************

Dependencies
============

|PT| requires:

* The `Python <http://python.org>`_ programming language, version 2.5.x, 2.6.x, or 2.7.x
* The `Cairo <http://cairographics.org>`_ graphics library, version 1.4.x or greater
* The `pycairo <http://cairographics.org/pycairo>`_ Python module for cairo
* The Python module `argparse <http://docs.python.org/library/argparse.html>`_
* Some other Python modules that seem to be standard on all installations.

Linux
-----

On Ubuntu::

  $ sudo apt-get install python-cairo
  $ sudo easy_install argparse

On Gentoo or Fedora, the package is called ``pycairo`` instead.

Mac OS X
--------

These instructions are courtesy of Lesley Lancaster, for Leopard 10.5.7 in Aug 2009 (and corrected by a MacPorts manager).

* Install `Xcode <http://developer.apple.com/technology/Xcode.html>`_ developer tools for Mac
* Install `MacPorts <http://www.macports.org>`_
* Install ``py25-cairo`` using MacPorts::

  $ sudo port install py25-cairo

Windows
-------

It's possible, but I haven't tried.

PieTree itself
==============

Once Python and cairo are working, i.e., this works without errors::

  $ python
  Python 2.6.5
  >>> import cairo
  >>> import argparse

then |PT| should run fine.
The latest version is available from `<http://www.uic.edu/~eeg/code.html>`_.

The program to run is ``PieTree/src/PieTree.py``.
You can put this in your path, or provide the full path when you call it.
The rest of this documentation assumes that simply ``PieTree.py`` gets to the executable.
