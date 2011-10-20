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
# Module:  PieReadTree.py
# Author:  Emma Goldberg, based on my Newick.py
# Date:	 Apr, 2008
######################################################


'''
Read in a file with a Newick string for the tree and 
   a list of tip and node states.
Also contains CountTips()
'''

import sys
import Newick

# TODO: will want each node to have a *vector* for its state(s); need to check the lengths are consistent and return the number of states

def ReadFromFileTTN(filename):
	'''
	Read in one of my .ttn files, with relaxed assumptions:
		tree string is on a single line
		tip and node states come afterwards, in any order
	The comment character # is respected, and blank lines are skipped.
	'''

	# First, form a tree from the Newick string.
	root = Newick.ReadFromFile(filename)

	# Then, deal with the state information if a tree was made.
	if root != -1:
		state_dict = MakeStateDict(filename)
		PutStates(root, state_dict)

	return root


def MakeStateDict(filename):

	# already did error-checking in Newick.ReadFromFile()
	infile = open(filename, "r")
	while 1:
		line = infile.next().strip()
		if line and line[0]!= "#" and line[0]!="[":
			break
			# now at the tree string

	state_dict = {}
	while 1:
		try:
			line = infile.next().strip()
			line = line.partition("#")[0].strip()
			if line and line[0]!= "#" and line[0]!="[":
				(name, state) = line.split()
				if name in state_dict:
					print "WARNING: label %s is used more than once" \
							% (name)
				state_dict[name] = float(state)

		except ValueError:
			print "ERROR: something is wrong with:\n   %s" % (line)
			print "proper format is e.g.:\n   label1   value1\n   " + \
					"label2   value2"
			infile.close()
			sys.exit()

		except StopIteration:
			break

	infile.close()
	return state_dict


def PutStates(node, state_dict):

	try:
		node.state = state_dict[node.label]
	except KeyError:
		#print "ERROR: can't find a state for %s" % (node.label)
		pass

	if node.daughters != None:
		for d in node.daughters:
			PutStates(d, state_dict)


def CountTips(node):
	'''return the number of tips'''

	if node.daughters != None:

		if len(node.daughters) != 2:
			print "NOTE: tree is not strictly bifurcating"
			node.PrintNode()
			#sys.exit()

		count_sum = 0.0
		for d in node.daughters:
			count_sum += CountTips(d)
		return count_sum

	else:
		return 1
