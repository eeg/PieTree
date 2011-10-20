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
# Module:  PieInput.py
# Author:  Emma Goldberg
# Date:	 Nov, 2011 (orig Apr 2008)
######################################################

'''
Parse options from the command line and input config file.
Read in and check the tree/states file.
Set sensible default values.
'''

import sys
import os
import argparse
import ConfigParser

import PieReadTree

# NOTE: In the opt file, the first line should be [pietree].  Instead, to fake the config file section header, see http://stackoverflow.com/questions/2819696/parsing-properties-file-in-python/2819788#2819788

def ParseInput():
	'''get all the user's specifications'''

	# First, we need just the tree input file.  This is required up front to
	# determine how many states are being used.  We should look for the name
	# of this file in both the options/config file, if any, and on the command
	# line.

	parser1 = argparse.ArgumentParser(add_help=False)

	parser1.add_argument('--version', action='version', version="PieTree 0.4, Nov 2011")

	parser1.add_argument("--treefile", \
			help="TTN file with tree and states")

	parser1.add_argument("--optfile", \
			help="config file containing options")

	(args, remaining_argv) = parser1.parse_known_args()

	if args.optfile:
		config = ConfigParser.SafeConfigParser()
		config.read(args.optfile)
		try:
			from_config = dict(config.items("pietree"))
		except ConfigParser.NoSectionError:
			print "\nERROR: The first line of the config file '" + \
					args.optfile + "' must be [pietree].\n"
			sys.exit()
	else:
		from_config = {}

	# the tree filename; command line takes precedence
	if args.treefile:
		treefile = args.treefile
	elif "treefile" in from_config:
		treefile = from_config["treefile"]
	else:
		treefile = None

	print treefile
	if treefile:
		root = PieReadTree.ReadFromFileTTN(treefile)
		if root == -1:
			print "\nERROR: failed to read tree from file " + treefile + "\n"
			nstates = 1    # TODO: make this 2, for the help message
		else:
			nstates = 2    # TODO: get this from the input file
	else:
		root = -1
		nstates = 1

	# Now that we know how many states there are, we can parse the rest of the
	# options.  (The number of states was really only needed to know how many
	# state colors to look for.)

	# the real parser, inheriting from the initial one used above
	parser = argparse.ArgumentParser(parents=[parser1], \
			description=__doc__)
			#formatter_class=argparse.RawDescriptionHelpFormatter)

	for i in range(nstates):
		parser.add_argument("--color"+str(i), help="color of state "+str(i)+": (red, green, blue) triplet")

	parser.add_argument("--outfile", \
			help="file to which the resulting image is written")

	format_choices = ("pdf", "ps", "svg", "png")
	parser.add_argument("--outformat", \
			choices = format_choices, help="image type to be created [" + 
			", ".join(format_choices) + "]")

	shape_choices = ("rect", "radial")
	parser.add_argument("--shape", choices = shape_choices, \
			help="tree shape [" + ", ".join(shape_choices) + "]")

	parser.add_argument("--pieradius", type=float, help="radius of node reconstruction pie charts")
	parser.add_argument("--boxsize", type=float, \
			help="height of tip state box")
	parser.add_argument("--tipspacing", type=float, \
			help="spacing between tip box centers")

	parser.add_argument("--tipnamesize", type=float, \
			help="font size of tip names")
	parser.add_argument("--nodenamesize", type=float, \
			help="font size of node names")

	yesno_choices = ("yes", "no")
	parser.add_argument("--italic", \
			choices = yesno_choices, help="if text should be italic [" \
			+ ", ".join(yesno_choices) + "]")
	parser.add_argument("--serif", \
			choices = yesno_choices, help="if text should be serif " + \
			"(rather than sans-serif) [" + ", ".join(yesno_choices) + "]")

	parser.add_argument("--textcolor", \
			help="color of tip and node labels: (red, green, blue) triplet")  
	parser.add_argument("--tipnamestatecolor", \
			choices = yesno_choices, help="if tip names " + \
			"should be written in their corresponding state colors [" + \
			", ".join(yesno_choices) + "]")

	parser.add_argument("--linecolor", \
			help="color of connecting lines: (red, green, blue) triplet")
	parser.add_argument("--backcolor", \
			help="background color: (red, green, blue) triplet")	   

	parser.add_argument("--rimthick", type=float, \
			help="thickness of pie and tip box borders")
	parser.add_argument("--linethick", type=float, \
			help="thickness of connecting lines")

	parser.add_argument("--width", type=float, \
			help="width of the entire picture")	   
	parser.add_argument("--height", type=float, \
			help="height of the entire picture")	   
	parser.add_argument("--xmargin", type=float, \
			help="margin on left and right of picture")
	parser.add_argument("--ymargin", type=float, \
			help="margin on top and bottom of picture")

	parser.set_defaults( \
			outfile = "pietree", \
			#outformat = "pdf", \	# see suffix stuff below
			shape = "rect", \
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
			xmargin = 10.0, \
			ymargin = 10.0 \
			# fine to leave background color as None
			)
	# see also SetDefaults()

	if from_config:
		parser.set_defaults(**from_config)

	options = parser.parse_args(remaining_argv)

	if len(sys.argv)==1:
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

	return (options, root)


def SetDefaults(c, numtips):
	'''set default config values that weren't taken care of in ParseInput'''

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
		if c.shape == "rect":
			#c.height = (numtips + 1) * c.tipspacing	# original
			c.height = numtips * c.tipspacing + 2*c.ymargin
		else:
			c.height = c.width


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
