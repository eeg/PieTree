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
# Date:     Apr, 2008
######################################################


'''
Read in a file with a Newick string for the tree and 
   a list of tip and node states.
Also contains CountTips()
'''

import sys
import Newick
from PieError import PieTreeError

# TODO: will want each node to have a *vector* for its state(s); need to check the lengths are consistent and return the number of states

def ReadFromFileTTN(filename):
    '''
    Read in one of my .ttn files, with relaxed assumptions:
        tree string is on a single line
        tip and node states come afterwards, in any order
            tip state is an integer [0 ... nstates]
            node state has nstates numbers
    The comment character # is respected, and blank lines are skipped.
    '''

    # First, form a tree from the Newick string.
    root = Newick.ReadFromFile(filename)

    if root == None:
        nstates = 0

    # Then, deal with the state information if a tree was made.
    else:
        state_dict = MakeStateDict(filename)
        nstates = max(map(len, state_dict.values()))
        PutStates(root, state_dict, nstates)

    return (root, nstates)


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
                (name, state) = line.split(None, 1)
                if name in state_dict:
                    print "WARNING: label %s is used more than once" \
                            % (name)
                state_dict[name] = map(float, state.split())
                # lengths of state lists will be checked later, in PutStates

        except ValueError:
            infile.close()
            raise PieTreeError("Problem reading character states.  " + \
                    "Something is wrong with:\n   " + line + \
                    "\nProper format is, e.g.:\n   tip1   tipstate\n" + \
                    "   node1   state0   state1")

        except StopIteration:
            break

    infile.close()
    return state_dict


def PutStates(node, state_dict, nstates):

    try:
        state = state_dict[node.label]

        # for a tip
        if node.daughters == None:
            if len(state) != 1:
                raise PieTreeError("specify each tip state as a single value, e.g.,\n   tip1  1")
            state = int(state[0])
            if state not in range(nstates):
                raise PieTreeError('invalid state "' + str(state) + '" for tip "' \
                                    + str(node.label) + '"')

            node.state = state

        # for a node
        else:
            if len(state) != nstates:
                raise PieTreeError("incorrect number of state values given for node " + node.label + " (" + str(nstates) + " expected)")
            if abs(sum(state) - 1) > 0.01:
                raise PieTreeError("sum of states for each node should sum to 1")
            node.state = state

    except KeyError:
        # raise PieTreeError("can't find a state for " + node.label)
        pass

    if node.daughters != None:
        for d in node.daughters:
            PutStates(d, state_dict, nstates)


def CountTips(node):
    '''return the number of tips'''

    if node.daughters != None:

        if len(node.daughters) != 2:
            print "NOTE: tree is not strictly bifurcating"
            node.PrintNode()

        count_sum = 0.0
        for d in node.daughters:
            count_sum += CountTips(d)
        return count_sum

    else:
        return 1

def AssignNodeTimes(node, root_time=0):
    '''
    Use given branch lengths to assign node times.
    '''

    if node.parent == None:
        node.time = root_time
    else:
        node.time = node.parent.time + node.length

    if node.daughters != None:
        for d in node.daughters:
            AssignNodeTimes(d, root_time)
