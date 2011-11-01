#! /usr/bin/env python

#--------------------------------------------------
# Copyright 2008 Emma Goldberg
# 
# This file is part of PieTree.
# 
# PieTree is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# PieTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with PieTree.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------- 

######################################################
# Module:  PieTree.py
# Author:  Emma Goldberg, based on Walter Brisken's PieTree.c
# Date:	 Nov, 2011 (orig Apr 2008)
######################################################

'''
Read in a tree with tip states and node state reconstructions.
Produce a pretty picture of it.
'''

import sys
import cairo

import PieInput
import PieClasses
import PieReadTree
from PieError import PieTreeError


def RunPieTree():

	### work through the user input ###

	(c, root, ntips, nstates) = PieInput.ParseInput()
	# TODO: clean this up -- could create PieTreeXXX already

	# convert the state colors into a list
	# TODO: default to black/white/N shades of gray; allow color names rather than RGB?
	color = range(nstates)
	for i in range(nstates):
		cc = "c.color" + str(i)
		if eval(cc) != None:
			color[i] = PieInput.ParseRGBColor(eval(cc))
			exec "del(" + cc + ")"
		else:
			raise PieTreeError(cc.split(".")[1] + " not specified")
	c.color = color

	c.linecolor = PieInput.ParseRGBColor(c.linecolor)
	c.textcolor = PieInput.ParseRGBColor(c.textcolor)
	if c.backcolor != None:
		c.backcolor = PieInput.ParseRGBColor(c.backcolor)

	# set up the drawing surface

	if c.outformat == "pdf":
		surface = cairo.PDFSurface(c.outfile, c.width, c.height)
	elif c.outformat == "eps":
		surface = cairo.PSSurface(c.outfile, c.width, c.height)
	elif c.outformat == "svg":
		surface = cairo.SVGSurface(c.outfile, c.width, c.height)
	elif c.outformat == "png":
		surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, \
				int(c.width), int(c.height))
	else:	# this should never happen, but just in case...
		raise PieTreeError("output format not found")

	cr = cairo.Context(surface)

	# set background color (defaults to white or transparent)

	if c.backcolor != None:
		cr.set_source_rgb(c.backcolor[0], c.backcolor[1], c.backcolor[2]);
		cr.paint();

	# set font face

	if c.serif == "yes" and c.italic == "yes":
		cr.select_font_face("serif", cairo.FONT_SLANT_ITALIC)
	elif c.serif == "no" and c.italic == "yes":
		cr.select_font_face("sans", cairo.FONT_SLANT_ITALIC)
	elif c.serif == "yes" and c.italic == "no":
		cr.select_font_face("serif", cairo.FONT_SLANT_NORMAL)
	else:
		cr.select_font_face("sans", cairo.FONT_SLANT_NORMAL)


	### now start working with the tree ###

	if c.shape == "rect":
		tree = PieClasses.PieTreeRect(root, ntips, nstates, cr, c)
	elif c.shape == "radial":
		tree = PieClasses.PieTreeRadial(root, ntips, nstates, cr, c)
	else:	# this should never happen, but just in case...
		raise PieTreeError("tree shape not found")

	if c.tipnamesize == 0:
		tipsize = 1e-10
	else:
		tipsize = tree.MaxTipNameSize()

	tree.CalcXY(tipsize)
	tree.PlotTree()


	### misc final stuff ###

	if c.outformat == "png":
		surface.write_to_png(c.outfile)

	# show_page()?

	print "created %s" % c.outfile



if __name__ == "__main__":

	try:
		RunPieTree()
	except PieTreeError, error:
		if error.value != None:
			print "\n" + error.value + "\n"
		sys.exit(1)

### for scale bar, want to round root - longest-tip distance
# def round_to_n(x, n):
#      if n < 1:
#          raise ValueError("number of significant digits must be >= 1")
#      return "%.*e" % (n-1, x)


# for docs: use sphinx
