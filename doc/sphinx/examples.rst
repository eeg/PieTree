.. _examples:

*******************
Gallery of Examples
*******************

The files needed for each example here are included in ``PieTree/examples/``.
The options for each plot style are in the specified configuration file (e.g., ``config1.pie``), and are also shown here as a command line call.
The example tree & states files can also be downloaded separately:

* :download:`example2.ttn <trees/example2.ttn>` (2 states, 42 tips)
* :download:`example3.ttn <trees/example3.ttn>` (3 states, 164 tips)

opt1.pie : example1.pdf
opt3.pie : example3.pdf
opt4.pie : example4.pdf
opt5.pie : example5.pdf

Example 3::

  $ PieTree --treefile example3.ttn --shape radial --color0 "(0.44,0.04,0.67)" \
    --color1 "(1,0.34,0)" --color2 "(0.24,0.62,0.82)" --tipnamesize 0 --nodenamesize 0
  or
  $ PieTree --treefile example3.ttn --optfile config3.pie
