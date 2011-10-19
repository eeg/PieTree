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
# Module:  PieDraw.py
# Author:  Emma Goldberg, based on Walter Brisken's PieTree.c
# Date:	 Apr, 2008
######################################################


'''
Do some initial calculations for scaling the drawing to the canvas.
Do the actual drawing.
'''

from math import pi as M_PI


#--------------------------------------------------
# for the scaling calculations
#-------------------------------------------------- 


def MaxTipNameSize(cr, node, tipsize):
	'''find longest (widest) tip name'''
	if node.daughters == None:
		thistipsize = cr.text_extents(node.label)[2]	# get the width
		if thistipsize > tipsize[0]:
			tipsize[0] = thistipsize
	else:
		for d in node.daughters:
			MaxTipNameSize(cr, d, tipsize)


def CalcXY(node, x, i, xmax):
	'''compute the (x, y) coordinate for each tip and node'''

	if node.length != None:
		x += node.length
	node.x = x

	if x > xmax[0]:
		xmax[0] = x

	if node.daughters != None:
		for d in node.daughters:
			i = CalcXY(d, x, i, xmax)

	if node.daughters == None:
		node.y = i
		i += 1
		return i
	else:
		sum_y = 0.0
		for d in node.daughters:
			sum_y += d.y
		node.y = sum_y / len(node.daughters)

	return i


def Xform(c, xy_in):
	'''transform (x, y) coordinates from tree to canvas'''
	# note: xy_in should be an (x, y) tuple

	return(c.xmargin + xy_in[0] * c.xscale, \
			c.ymargin + xy_in[1] * c.tipspacing)


def DrawRoot(cr, c, root):
	'''draw the branch leading to the root'''

	(x0, y) = Xform(c, (0, root.y))
	(x, y) = Xform(c, (root.x, root.y))

	cr.set_line_width(c.linethick)
	cr.set_source_rgb(c.linecolor[0], c.linecolor[1], c.linecolor[2])
	cr.move_to(x, y)
	cr.line_to(x0, y)
	cr.stroke()


#--------------------------------------------------
# for the drawing
#-------------------------------------------------- 


def PlotTree(cr, c, node):
	'''calls the drawing functions for the rest of the tree, and recurses'''

	if node.daughters == None:
		DrawTip(cr, c, node)

	else:
		DrawFork(cr, c, node)
		if c.pieradius > 0:
			if node.state == None:
				print "WARNING: state not specified for %s" % (node.label)
			else:
				DrawPie(cr, c, node)
		if c.nodenamesize > 0:
			DrawNodeLabel(cr, c, node)

		for d in node.daughters:
			PlotTree(cr, c, d)


def DrawTip(cr, c, node):
	'''draw the tip box, border, and label'''

	# the tip box
	(x, y) = Xform(c, (node.x, node.y))
	delta = c.boxsize

	cr.rectangle(x - delta/2., y-delta/2., delta, delta)

	# box border
	if c.rimthick > 0 and c.boxsize > 0:
		cr.set_line_width(c.rimthick)
		cr.set_source_rgb(c.linecolor[0], c.linecolor[1], c.linecolor[2])
		cr.stroke_preserve()

	# tip color
	if node.state == 0:
		cr.set_source_rgb(c.color0[0], c.color0[1], c.color0[2])
	elif node.state == 1:
		cr.set_source_rgb(c.color1[0], c.color1[1], c.color1[2])
	else:
		cr.set_source_rgb(0.5, 0.5, 0.5)
		print "WARNING: check the state of %s" % node.label

	cr.fill()

	if c.tipnamesize > 0:
		if c.tipnamestatecolor != "yes":
			cr.set_source_rgb(c.textcolor[0], c.textcolor[1], c.textcolor[2])
		cr.set_font_size(c.tipnamesize)
		textheight = cr.text_extents(node.label)[3]
		#cr.move_to(x + delta, y + textheight/2.)
		#cr.move_to(x + delta/2. + c.tipspacing/4., y + textheight/2.)
		cr.move_to(x + delta/2. + c.tipspacing/4., y + textheight/3.)
		cr.show_text(node.label)
	# vertical alignment of text may not be quite right


def DrawPie(cr, c, node):
	'''draw the pie chart at each node'''

	R = c.pieradius
	(x, y) = Xform(c, (node.x, node.y))

	# the outer circle of the pie
	if c.rimthick > 0:
		cr.set_line_width(c.rimthick)
		cr.set_source_rgb(c.linecolor[0], c.linecolor[1], c.linecolor[2])
		cr.move_to(x, y)
		cr.arc(x, y, R, 0, 2*M_PI)
		cr.stroke()

	# the pie piece for state 0
	angle0 = (1. - node.state) * 2 * M_PI - M_PI/2
	if node.state != 1:
		cr.set_source_rgb(c.color0[0], c.color0[1], c.color0[2])
		cr.move_to(x, y)
		cr.arc(x, y, R, -M_PI/2, angle0)
		cr.fill()

	# the pie piece for state1
	angle1 = node.state * 2 * M_PI
	if node.state != 0:
		cr.set_source_rgb(c.color1[0], c.color1[1], c.color1[2])
		cr.move_to(x, y)
		cr.arc(x, y, R, angle0, angle0+angle1)
		cr.fill()


def DrawFork(cr, c, node):
	'''draw the (rectangular) fork to the node's daughters'''

	cr.set_line_width(c.linethick)
	cr.set_source_rgb(c.linecolor[0], c.linecolor[1], c.linecolor[2])

	(x0, y0) = Xform(c, (node.x, node.y))

	for d in node.daughters:
		(x, y) = Xform(c, (d.x, d.y))
		cr.move_to(x0, y0)
		cr.line_to(x0, y)
		cr.line_to(x, y)
		cr.stroke()


def DrawNodeLabel(cr, c, node):
	'''put text labels by nodes'''

	(x, y) = Xform(c, (node.x, node.y))
	cr.set_source_rgb(c.textcolor[0], c.textcolor[1], c.textcolor[2])
	cr.set_font_size(c.nodenamesize)
	if node.label != None:
		textheight = cr.text_extents(node.label)[3]
		#cr.move_to(x + c.pieradius + c.boxsize/4., y + textheight/2.)
		cr.move_to(x + c.pieradius + c.tipspacing/5., y + textheight/2.)
		cr.show_text(node.label)
