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
# Module:  PieInputOptions.py
# Author:  Emma Goldberg, based on Walter Brisken's PieTree.c
# Date:	 Apr, 2008
######################################################


'''
Parse options from the command line and input config file.
Set sensible default values.
'''

import sys
import os
from configparse import OptionParser


def ParseCmdLine():
	'''get all the users settings'''

	### set up the command line option parser ###

	parser = OptionParser(version="PieTree 0.2, Apr 2008")

	parser.add_option("--opt", dest="optfile", \
			help="config file containing options")

	parser.add_option("--outfile", dest="outfile", config="true", \
			help="file to which the resulting image is written")

	format_choices = ("pdf", "ps", "svg", "png")
	parser.add_option("--outformat", dest="outformat", type="choice", \
			choices = format_choices, help="image type to be created [" + 
			", ".join(format_choices) + "]", config="true")

	parser.add_option("--pieradius", dest="pieradius", type="float",  \
			help="radius of node reconstruction pie charts", config="true")
	parser.add_option("--boxsize", dest="boxsize", type="float", \
			help="height of tip state box", config="true")
	parser.add_option("--tipspacing", dest="tipspacing", type="float", \
			help="spacing between tip box centers", config="true")

	parser.add_option("--tipnamesize", dest="tipnamesize", type="float", \
			help="font size of tip names", config="true")
	parser.add_option("--nodenamesize", dest="nodenamesize", type="float", \
			help="font size of node names", config="true")

	yesno_choices = ("yes", "no")
	parser.add_option("--italic", dest="italic", type="choice", \
			choices = yesno_choices, help="if text should be italic [" \
			+ ", ".join(yesno_choices) + "]", config="true")
	parser.add_option("--serif", dest="serif", type="choice", \
			choices = yesno_choices, help="if text should be serif " + \
			"(rather than sans-serif) [" + ", ".join(yesno_choices) + "]", \
			config="true")

	parser.add_option("--color0", dest = "color0", type="string", \
			help="color of state 0: (red, green, blue) triplet",  
			config="true")	   
	parser.add_option("--color1", dest = "color1", type="string", \
			help="color of state 1: (red, green, blue) triplet",  
			config="true")	   

	parser.add_option("--textcolor", dest = "textcolor", type="string", \
			help="color of tip and node labels: (red, green, blue) triplet",  
			config="true")	   
	parser.add_option("--tipnamestatecolor", dest="tipnamestatecolor", \
			type="choice", choices = yesno_choices, help="if tip names " + \
			"should be written in their corresponding state colors [" + \
			", ".join(yesno_choices) + "]", config="true")

	parser.add_option("--linecolor", dest = "linecolor", type="string", \
			help="color of connecting lines: (red, green, blue) triplet",  
			config="true")	   
	parser.add_option("--backcolor", dest = "backcolor", type="string", \
			help="background color: (red, green, blue) triplet", config="true")	   

	parser.add_option("--rimthick", dest="rimthick", type="float", \
			help="thickness of pie and tip box borders", \
			config="true")	   
	parser.add_option("--linethick", dest="linethick", type="float", \
			help="thickness of connecting lines", config="true")	   

	parser.add_option("--width", dest="width", type="float", \
			help="width of the entire picture", config="true")	   
	parser.add_option("--height", dest="height", type="float", \
			help="height of the entire picture", config="true")	   
	parser.add_option("--xmargin", dest="xmargin", type="float", \
			help="margin on left and right of picture",  \
			config="true")	   
	parser.add_option("--ymargin", dest="ymargin", type="float", \
			help="margin on top and bottom of picture",  \
			config="true")

	parser.set_defaults( \
			outfile = "pietree", \
			#outformat = "pdf", \	# see suffix stuff below
			pieradius = 7.0, \
			italic = "no", \
			serif = "no", \
			color0 = "(1.0, 1.0, 1.0)", \
			color1 = "(0.0, 0.0, 0.0)", \
			textcolor = "(0.0, 0.0, 0.0)", \
			tipnamestatecolor = "no", \
			linecolor = "(0.0, 0.0, 0.0)", \
			rimthick = 2.0, \
			linethick = 1.0, \
			width = 800.0, \
			xmargin = 20.0, \
			ymargin = 10.0 \
			# fine to leave background color as None
			)
	# see also SetDefaults()

	parser.set_usage("\n       %prog {options; -h for help} {.ttn tree file}")

	(options, args) = parser.parse_args()

	### read in options specified in the opt file ###

	if options.optfile != None:
		if os.path.isfile(options.optfile):
			(options, args) = parser.parse_args(files=[options.optfile])
		else:
			print "WARNING: opt file %s not found" % options.optfile

	### check for various input errors ###

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit()

	if len(args) == 0:
		print "ERROR: need to specify an input tree file."
		parser.print_usage()
		sys.exit()

	### adjust the outfile name and outformat as necessary ###

	suffix = options.outfile.split(".")[-1]

	if suffix.lower() not in format_choices:
		if options.outformat == None:
			options.outformat = "pdf"
		options.outfile = options.outfile + "." + options.outformat

	else:
		if options.outformat == None:
			options.outformat = suffix.lower()
		elif suffix.lower() != options.outformat:
			print "WARNING: outfile suffix (%s) and " % (suffix),
			print "outformat (%s) don't match" % (options.outformat)
			options.outfile = options.outfile + "." + options.outformat

	return (options, args)


def SetDefaults(c, numtips):
	'''set default config values that weren't taken care of in ParseCmdLine'''

	if c.boxsize == None:
		if c.pieradius == 0:
			c.boxsize = 10
		else:
			c.boxsize = c.pieradius * 1.9

	if c.tipnamesize == None:
		if c.boxsize == 0:
			c.tipnamesize = 10
		else:
			c.tipnamesize = c.boxsize

	if c.nodenamesize == None:
		if c.tipnamesize == 0:
			c.nodenamesize = 8
		else:
			c.nodenamesize = c.tipnamesize * 0.75

	if c.tipspacing == None:
		if c.boxsize == 0 and c.pieradius > 0:
			c.tipspacing = c.pieradius * 3
		elif c.boxsize == 0 and c.pieradius == 0:
			if c.tipnamesize > 0:
				c.tipspacing = c.tipnamesize * 1.5
			else:
				c.tipspacing = 10
		else:
			c.tipspacing = c.boxsize * 1.5

	if c.rimthick == None:
		c.rimthick = c.linethick

	if c.height == None:
		#c.height = (numtips + 1) * c.tipspacing	# original
		c.height = numtips * c.tipspacing + 2*c.ymargin


def ParseRGBColor(colstr):
	'''transform a string specifying an RGB color into a 3-element list'''

	failed = False

	colstr = colstr.strip()

	if colstr[0] != "(" or colstr[-1] != ")":
		failed = True

	else:
		colstr = colstr[1:-1]

		collist = colstr.split(",")
		if len(collist) != 3:
			failed = True
		else:
			for i in range(3):
				try:
					collist[i] = float(collist[i].strip())
				except ValueError:
					failed = True

	if failed:
		print "ERROR: RGB colors should be specified like this:",
		print '"(0, 0.5, 0.7)"'
		sys.exit()

	else:
		return collist
