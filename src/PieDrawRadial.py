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
# Module:  PieDrawRadial.py
# Author:  Emma Goldberg
# Date:	 Nov, 2011 (orig Feb 2009)
######################################################

'''
Do some initial calculations for scaling the drawing to the canvas.
Do the actual drawing.
'''

from math import pi as M_PI
from math import cos, sin


#--------------------------------------------------
# for the scaling calculations
#-------------------------------------------------- 

def CalcRT(node, r, i, rmax, ntips):
	'''compute the (r, theta) coordinates for each tip and node'''

	if node.length != None:
		r += node.length
	node.r = r

	if r > rmax[0]:
		rmax[0] = r

	if node.daughters != None:
		for d in node.daughters:
			i = CalcRT(d, r, i, rmax, ntips)

	if node.daughters == None:
		node.t = 2 * M_PI * i / ntips
		i += 1
	else:
		sum_t = 0.0
		for d in node.daughters:
			sum_t += d.t
		node.t = sum_t / len(node.daughters)

	return i


def RTtoXY(node):
	'''convert polar to cartesian coordinates'''

	if node.daughters != None:
		for d in node.daughters:
			RTtoXY(d)

	node.x = node.r * cos(node.t)
	node.y = node.r * sin(node.t)


def Xform(c, xy_in):
	'''transform (x, y) coordinates from tree to canvas'''
	# note: xy_in should be an (x, y) tuple

	#--------------------------------------------------
	# return(c.xmargin + xy_in[0] * c.xscale, \
	# 		c.ymargin + xy_in[1] * c.tipspacing)
	#-------------------------------------------------- 
	return (xy_in[0] * c.xscale + c.width/2., xy_in[1] * c.xscale + c.height/2.)


#--------------------------------------------------
# for the drawing
#-------------------------------------------------- 


def PlotTree(cr, c, node, nstates):
	'''calls the drawing functions for the rest of the tree, and recurses'''

	if node.daughters == None:
		DrawTip(cr, c, node, nstates)

	else:
		DrawFork(cr, c, node)
		if c.pieradius > 0:
			if node.state == None:
				print "WARNING: state not specified for %s" % (node.label)
			else:
				DrawPie(cr, c, node, nstates)
		if c.nodenamesize > 0:
			DrawNodeLabel(cr, c, node)

		for d in node.daughters:
			PlotTree(cr, c, d, nstates)


def DrawTip(cr, c, node, nstates):
	'''draw the tip box, border, and label'''

	# the tip box
	(x, y) = Xform(c, (node.x, node.y))
	delta = c.boxsize
	
	# get_matrix here and set_matrix below take care of the rotation
	m = cr.get_matrix()
	cr.translate(x, y)
	cr.rotate(node.t)

	cr.rectangle(0, -delta/2., delta, delta)

	# box border
	if c.rimthick > 0 and c.boxsize > 0:
		cr.set_line_width(c.rimthick)
		cr.set_source_rgb(c.linecolor[0], c.linecolor[1], c.linecolor[2])
		cr.stroke_preserve()

	# tip color
	if node.state in range(nstates):
		i = node.state
		cr.set_source_rgb(c.color[i][0], c.color[i][1], c.color[i][2])
	else:
		cr.set_source_rgb(0.5, 0.5, 0.5)
		print "WARNING: check the state of %s" % node.label

	cr.fill()

	if c.tipnamesize > 0:
		if c.tipnamestatecolor != "yes":
			cr.set_source_rgb(c.textcolor[0], c.textcolor[1], c.textcolor[2])
		cr.set_font_size(c.tipnamesize)
		textheight = cr.text_extents(node.label)[3]
		cr.move_to(delta + c.tipspacing/4., textheight/3.)
		#cr.show_text(node.label)
		cr.show_text((node.label).replace("_", " "))
		# todo: make replacing underscores an option, rather than mandatory?

	cr.set_matrix(m)


def DrawPie(cr, c, node, nstates):
	'''draw the pie chart at each node'''

	(x, y) = Xform(c, (node.x, node.y))
	R = c.pieradius

	# get_matrix here and set_matrix below take care of the rotation
	m = cr.get_matrix()
	cr.translate(x, y)
	cr.rotate(node.t)

	# the outer circle of the pie
	if c.rimthick > 0:
		cr.set_line_width(c.rimthick)
		cr.set_source_rgb(c.linecolor[0], c.linecolor[1], c.linecolor[2])
		#cr.move_to(x, y)
		#cr.arc(x, y, R, 0, 2*M_PI)
		cr.arc(0, 0, R, 0, 2*M_PI)
		cr.stroke()

	# the pie pieces
	angle_start = -M_PI/2
	for i in range(nstates):
		angle_stop = node.state[i] * 2 * M_PI + angle_start
		cr.set_source_rgb(c.color[i][0], c.color[i][1], c.color[i][2])
		# cr.move_to(x, y)
		cr.move_to(0, 0)
		# cr.arc(x, y, R, angle_start, angle_stop)
		cr.arc(0, 0, R, angle_start, angle_stop)
		cr.fill()
		angle_start = angle_stop

	cr.set_matrix(m)


def DrawFork(cr, c, node):
	'''draw the fork to the node's daughters'''

	cr.set_line_width(c.linethick)
	cr.set_source_rgb(c.linecolor[0], c.linecolor[1], c.linecolor[2])

	(x0, y0) = Xform(c, (node.x, node.y))

	(mint, maxt) = (2*M_PI, 0)
	for d in node.daughters:

		if d.t < mint:
			mint = d.t
		if d.t > maxt:
			maxt = d.t

		(xd, yd) = Xform(c, (d.x, d.y))
		xa = node.r * cos(d.t)
		ya = node.r * sin(d.t)
		(xb, yb) = Xform(c, (xa, ya))

		cr.move_to(xd, yd)
		cr.line_to(xb, yb)
		cr.stroke()

	cr.arc(c.width/2., c.height/2., node.r*c.xscale, mint, maxt)
	cr.stroke()


def DrawNodeLabel(cr, c, node):
	'''put text labels by nodes'''

	(x, y) = Xform(c, (node.x, node.y))

	cr.set_source_rgb(c.textcolor[0], c.textcolor[1], c.textcolor[2])
	cr.set_font_size(c.nodenamesize)

	# get_matrix here and set_matrix below take care of the rotation
	m = cr.get_matrix()
	cr.translate(x, y)
	cr.rotate(node.t)

	if node.label != None:
		textheight = cr.text_extents(node.label)[3]
		cr.move_to(0 + c.pieradius + c.tipspacing/5., textheight/2.)
		cr.show_text(node.label)

	cr.set_matrix(m)


def DrawRoot(cr, c, root):
	'''draw the branch leading to the root'''

	(x0, y) = Xform(c, (0, root.y))
	(x, y) = Xform(c, (root.x, root.y))

	cr.set_line_width(c.linethick)
	cr.set_source_rgb(c.linecolor[0], c.linecolor[1], c.linecolor[2])
	cr.move_to(x, y)
	cr.line_to(x0, y)
	cr.stroke()
