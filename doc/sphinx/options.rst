.. _options:

*******************
List of All Options
*******************

Recall that option names must be preceded with ``--`` when used on the command line.
Alternatively, they can be placed in a file whose first line is ``[pietree]``.
See :ref:`usage-options`.

Input and output logistics
--------------------------

``treefile``
  Name of file containing tree and tip states.  See :ref:`usage-treefile`.

``optfile``
  Name of file containing formatting options.   See :ref:`usage-options`.

``outfile``
  Name for the output file.
  If it doesn’t have a suffix (like ``.pdf``), an appropriate one will be appended.
  [default is ``pietree``]

``outformat``
  File format of the output image.
  If an ``outfile`` with a suffix is also specified, ``outformat`` takes precedence and an appropriate suffix will be appended.

  ``= pdf`` Adobe’s format [the default]

  ``= eps``  (encapsulated) postscript

  ``= svg`` scalable vector graphics (works with Inkscape and Illustrator)

  ``= png`` portable network graphics (lossless bitmap)

``width``
  Width of the canvas.  The image is scaled horizontally to match this width.

  ``=`` any positive number [default is 800]

``height``
  Height of the canvas.  Doesn't affect scaling of the image.

  ``=`` any positive number

  [default is determined by tree size for ``shape = rect`` or is ``width`` for ``shape = radial``]

``xmargin``
  Margin size on the left and right of the image.
  For ``shape = radial``, these are based on the longest tip name.

  ``=`` any positive number [default is 20]

``ymargin``
  Margin size on the top and bottom of the image.
  For ``shape = radial``, top and bottom margins are better controlled with ``height``.


  ``=`` any positive number [default is 10]

Graphical elements
------------------

``shape``
  Shape in which the tree is drawn.

  ``= rect`` rectangular, with all the tips on the right [the default]

  ``= radial`` radial, with the tips along the outside of a circle

``colorX`` 
  Color representing state ``X``.  Replace ``X`` with ``0``, ``1``, etc.

  ``= "(R, G, B)"`` see :ref:`colornote`

  [defaults: ``color0 = "(1, 1, 1)"`` (white), ``color1 = "(0, 0, 0)"`` (black), no defaults for additional states]

``pieradius``
  Radius of the pie chart showing the node reconstruction.

  ``=`` any positive number [default is 7]

``boxsize``
  Height of the box showing the tip state.

  ``=`` any positive number [default is 1.9 * ``pieradius``]

``rimthick``
  Thickness of the lines around the pies and boxes.

  ``=`` any positive number [default is 2]

``linethick``
  Thickness of the branch lines.

  ``=`` any positive number [default is 1]

``linecolor``
  Color of the branches of the tree and other lines.

  ``= "(R, G, B)"`` see :ref:`colornote` [default is black]

``backcolor``
  Color of the image background.

  ``= "(R, G, B)"`` see :ref:`colornote` [default is transparent for ``outformat = png``, white otherwise]

``tipspacing``

  ``=`` any positive number [default is 1.5 * ``boxsize``]

Text formatting
---------------

``tipnamesize``
  Font size of the tip labels.

  ``=`` any positive number [default is ``boxsize``]

``nodenamesize``
  Font size of the internal node labels.

  ``=`` any positive number [default is 0.75 * ``tipnamesize``]

``italic``
  Whether to italicize the text

  ``= yes`` italics

  ``= no`` normal upright [the default]

``serif``
  Whether to use a serif font.

  ``= yes`` serif font

  ``= no`` sans-serif font [the default]

``underscorespace``
  Whether to replace ``_`` with a space in tip and node names.

  ``= yes`` do replace underscores

  ``= no`` don't replace underscores [the default]

``textcolor``
  Color of tip and node labels

  ``= "(R, G, B)"`` see :ref:`colornote` [default is black]

``tipnamestatecolor``
  Whether to color the tip text label according to the tip state.

  ``= yes`` take tip label color from tip state

  ``= no`` use ``textcolor`` for tip label [the default]

.. _colornote:

Note on RGB colors
------------------

``R``, ``G``, and ``B`` are the values for the red, green, and blue components of the color.
Each takes a value between 0 and 1.
These three numbers must be separated with commas and the whole thing surrounded with parentheses.  On the command line, put quote marks outside the parentheses.
For example, ``color0 = (0.24, 0.62, 0.82)`` in an option file, and ``--color0 = "(0.24, 0.62, 0.82)"`` on the command line.
