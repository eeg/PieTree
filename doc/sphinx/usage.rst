.. _usage:

*****
Usage
*****

When running |PT|, you provide it with

.. FIXME

* an `input data file <FIXME>`_, containing the Newick-formatted tree and a list of the tip and node states

* optionally (but likely), some `formatting options <FIXME>`_

If no input is provided, a usage message will be printed summarizing the options::

  $ PieTree.py
  usage: PieTree.py [-h] [--version] [--treefile TREEFILE] [--optfile OPTFILE]
                  [--outformat {pdf,ps,svg,png}] [--shape {rect,radial}]
                  ... and a bunch more options

Quick Start
===========

There is a sample tree file called ``example.ttn`` in ``PieTree/examples/``.
To use it (again, adjust paths as necessary)::

  $ PieTree.py --treefile example.ttn
  created pietree.pdf

.. FIXME: make sure example runs; show output image
