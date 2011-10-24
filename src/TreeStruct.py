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

#############################
# Module:   TreeStruct.py
# Author:   Emma Goldberg
# Date:     Sept, 2007
#
# Compose a phylogenetic tree from TreeNodes.
# Pulled from my BiSSE library.
#############################


_nodenum = 1   # for LabelNodes()


class TreeNode:
	'''
	    TreeNode contains the properties of a single node (or tip) in a 
	    phylogenetic tree
		  label: a name or number for the node
		  time: the time (on the tree) of the node
		  state: the state of a particular character
		  parent: the node that is this node's ancestor 
	                  (None for the root)
		  daughters: a list of this node's immediate descendants
	                     (None for a tip)
	       length: the time from this node to its ancestor
	                  (computed automatically if times are specified)
	'''
	def __init__(self, label=None, time=None, length=None, state=None, parent=None, \
			daughters=None):
		self.label = label
		self.time = time
		self.state = state
		self.parent = parent
		self.daughters = daughters
		# use node times if given; otherwise, use branch lengths if given
		if self.parent!=None and self.time!=None and self.parent.time!=None:
			self.length = self.time - self.parent.time
		else:
			self.length = length
		# self.cl = [0]*Nstates	# will hold conditional likelihood values


	def PrintNode(self):
		''' prints information about this node '''
		print self.label,
		print ":",
		if self.time != None:
			print "t = %2.4f," % (self.time),
		if self.length != None:
			print "l = %2.4f," % (self.length),
		if self.state != None:
			print "s = %s," % (str(self.state)),
		print "p =",
		if self.parent != None:
			print self.parent.label,
		else:
			print "--",
		print ", d =",
		if self.daughters != None:
			for d in self.daughters:
				print d.label,
		else:
			print "--",
		print ", cl =",
		print self.cl


	def PrintTree(self, indent=2):
		''' prints a list of all descendants from this node '''
		print " "*indent,
		self.PrintNode()
		if self.daughters != None:
			for d in self.daughters:
				d.PrintTree(indent+2)


	def NewickString(self):
		''' returns all descendants from this node as a Newick string '''
		from cStringIO import StringIO
		nstr = StringIO()	# allows for more efficient string concatenation
		nstr.write("(")
		self._NewickStringGuts(nstr)
		nstr.write(");")
		returnme = nstr.getvalue()
		nstr.close()
		return returnme
	def _NewickStringGuts(self, nstr):
		if self.daughters == None:
			nstr.write( str(self.label) )
			if self.length != None:
				nstr.write( ":%f" % (self.length) )
		else:
			nstr.write("(")
			for d in self.daughters:
				d._NewickStringGuts(nstr)
				nstr.write(",")
			nstr.seek(-1, 1)	# remove that last comma
			nstr.write(")")
			#nstr.write( "%s_%s" % (str(self.state), str(self.label)) )
			nstr.write( str(self.label) )
			if self.length != None:
				nstr.write( ":%f" % (self.length) )


	def TipStates(self):
		''' returns a list of tip labels and trait values in left-to-right order '''
		tiplist = []
		self._TipStatesGuts(tiplist)
		return tiplist

	def _TipStatesGuts(self, tiplist):
		if self.daughters == None:
			tiplist.append([self.label, self.state])
		else:
			for d in self.daughters:
				d._TipStatesGuts(tiplist)


	def LabelNodes(self):
		''' give sequential labels to internal nodes lacking labels '''
		global _nodenum	# would be nicer to avoid this...
		if self.daughters != None:
			for d in self.daughters:
				d.LabelNodes()
			self.label = "n%d" % _nodenum 
			_nodenum += 1
			#--------------------------------------------------
			# if self.label == None:
			# 	self.label = "n%d" % _nodenum 
			# 	_nodenum += 1
			#-------------------------------------------------- 
