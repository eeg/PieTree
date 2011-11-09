.. _preliminaries:

*************
Preliminaries
*************

Background
==========

Purpose
-------

|PT| is a program for drawing pretty pictures of phylogenetic trees.
Its main purpose is displaying discrete character states, including ancestral state reconstructions.
Its name comes from using a pie chart to show the probability of a node being in the various possible states.

|PT| doesn't do any kind of analysis---it just produces images.
Carrying out ancestral state reconstruction in another program and assembling the results for use with |PT| is illustrated in :ref:`treefile`.

History
-------

The first incarnation of |PT| was written in C by Walter Brisken in 2007.
In  2008, I rewrote it all in Python (as an excuse to practice Python and learn about the Cairo graphics library) and gave it a more useable interface.
Features have been gradually accumulating since then.

Feedback
--------

Please send bug reports, feature requests, and any other comments to me at eeg@uic.edu.

License
-------

|PT| is released under the `GNU General Public License <http://www.gnu.org/licenses/>`_.


Installation
============

Dependencies
------------

|PT| requires:

* The `Python <http://python.org>`_ programming language, version 2.5.x, 2.6.x, or 2.7.x
* The `Cairo <http://cairographics.org>`_ graphics library, version 1.4.x or greater
* The `pycairo <http://cairographics.org/pycairo>`_ Python module for cairo
* The Python module `argparse <http://docs.python.org/library/argparse.html>`_
* Some other Python modules that seem to be standard on all installations.

When the dependencies are satisfied, this should work without errors::

  $ python
  Python 2.6.5
  >>> import cairo
  >>> import argparse

Linux
+++++

On Ubuntu::

  $ sudo apt-get install python-cairo
  $ sudo easy_install argparse

On Gentoo or Fedora, the package is called ``pycairo`` instead.

Mac OS X
++++++++

These instructions are courtesy of Lesley Lancaster, for Leopard 10.5.7 in Aug 2009 (and corrected by a MacPorts manager).

* Install `Xcode <http://developer.apple.com/technology/Xcode.html>`_ developer tools for Mac
* Install `MacPorts <http://www.macports.org>`_
* Install ``py25-cairo`` using MacPorts::

  $ sudo port install py25-cairo

Windows
+++++++

It shouldn't be hard, but I haven't tried.

PieTree itself
--------------

The latest version of |PT| is available from `<http://www.uic.edu/~eeg/code.html>`_.

The program to run is ``PieTree/src/PieTree.py``.
How to add this to your path is a matter of personal taste.
Here are examples of two possibilities::

  $ ln -s /home/emma/PieTree/src/PieTree.py /home/emma/bin/PieTree
  # or
  $ alias PieTree="/home/emma/PieTree/src/PieTree.py"

The rest of this documentation assumes that running simply ``PieTree`` calls the program.
