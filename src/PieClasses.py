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
# Module:  PieClasses.py
# Author:  Emma Goldberg
# Date:     Nov, 2011 (orig Apr 2008)
######################################################

from math import cos, sin, pi
import cairo
import TreeStruct

#--------------------------------------------------
# For drawing a tree of any shape
#--------------------------------------------------

class PieTree():
    '''
    This class contains:
       * tree root
       * tree attributes: ntips, nstates
       * node/tip drawing functions
          further fleshed out in the rectangular and radial subclasses
       * cairo surface to be drawn to
       * plotting variables
    '''

    def __init__(self, root, ntips, nstates, surface, plot_values):
        self.root = root
        self.ntips = ntips
        self.nstates = nstates
        self.surface = surface
        self.plot_vars = plot_values

    def MaxTipNameSize(self):
        '''Find the longest (widest) tip name in this tree.'''

        # todo: extract answer by using return rather than list
        def MTNS(node, cr, tipsize):
            if node.daughters == None:
                thistipsize = cr.text_extents(node.label)[2]
                if thistipsize > tipsize[0]:
                    tipsize[0] = thistipsize
            else:
                for d in node.daughters:
                    MTNS(d, cr, tipsize)

        tipsize = [-1]
        MTNS(self.root, self.surface, tipsize)

        return tipsize[0]

    def PlotTree(self):
        '''Calls the drawing functions for the whole tree.'''

        def PT(tree, node):

            if node.daughters == None:
                tree.DrawTip(node)

            else:
                tree.DrawFork(node)

                if tree.plot_vars.pieradius > 0:
                    if node.state != None:
                        tree.DrawPie(node)
                    else:
                        print "NOTE: state not specified for %s" \
                                % (node.label)

                if tree.plot_vars.nodenamesize > 0:
                    tree.DrawNodeLabel(node)

                for d in node.daughters:
                    PT(tree, d)

        self.DrawRoot()
        PT(self, self.root)

    def DrawTipMore(self, node, (x,y), delta):
        '''Finish the work of DrawTip.'''

        c = self.plot_vars
        cr = self.surface

        # box border
        if c.rimthick > 0 and c.boxsize > 0:
            cr.set_line_width(c.rimthick)
            cr.set_source_rgb(c.linecolor[0], c.linecolor[1], \
                    c.linecolor[2])
            cr.stroke_preserve()

        # tip color
        if node.state in range(self.nstates):
            i = node.state
            cr.set_source_rgb(c.color[i][0], c.color[i][1], c.color[i][2])
        else:
            cr.set_source_rgb(0.5, 0.5, 0.5)
            print "WARNING: check the state of %s" % node.label
        cr.fill()

        # tip label
        if c.tipnamesize > 0:
            if c.tipnamestatecolor != "yes":
                cr.set_source_rgb(c.textcolor[0], c.textcolor[1], \
                        c.textcolor[2])
            cr.set_font_size(c.tipnamesize)
            textheight = cr.text_extents(node.label)[3]
            cr.move_to(x + delta/2. + c.tipspacing/4., y + textheight/3.)
            if c.underscorespace == "yes":
                cr.show_text((node.label).replace("_", " "))
            else:
                cr.show_text(node.label)

    def DrawPieMore(self, node, (x,y)):
        '''Finish the work of DrawPie.'''

        c = self.plot_vars
        cr = self.surface

        R = c.pieradius

        # the outer circle of the pie
        if c.rimthick > 0:
            cr.set_line_width(c.rimthick)
            cr.set_source_rgb(c.linecolor[0], c.linecolor[1], \
                    c.linecolor[2])
            cr.move_to(x, y)
            cr.arc(x, y, R, 0, 2*pi)
            cr.stroke()

        # the pie pieces
        angle_start = -pi/2
        for i in range(self.nstates):
            angle_stop = node.state[i] * 2 * pi + angle_start
            cr.set_source_rgb(c.color[i][0], c.color[i][1], c.color[i][2])
            cr.move_to(x, y)
            cr.arc(x, y, R, angle_start, angle_stop)
            cr.fill()
            angle_start = angle_stop

    def DrawNodeLabelMore(self, node, (x,y)):
        '''Finish the work of DrawNodeLabel.'''

        c = self.plot_vars
        cr = self.surface

        cr.set_source_rgb(c.textcolor[0], c.textcolor[1], c.textcolor[2])
        cr.set_font_size(c.nodenamesize)

        if node.label != None:
            textheight = cr.text_extents(node.label)[3]
            cr.move_to(x + c.pieradius + c.tipspacing/5., y + textheight/2.)
            if c.underscorespace == "yes":
                cr.show_text((node.label).replace("_", " "))
            else:
                cr.show_text(node.label)

    def DrawScalebar(self):
        '''Display the time scale.'''

        c = self.plot_vars
        cr = self.surface

        cr.set_line_width(c.linethick)
        cr.set_source_rgb(c.linecolor[0], c.linecolor[1], c.linecolor[2])

        # size of the label
        showme = str(c.scalebar["length"])
        tw = (cr.text_extents(showme)[2], cr.text_extents(showme)[3])
        # note: "%.*e" % (n-1, x) rounds to n digits

        x0 = self.Xform( (self.root.x, 0) )[0]
        x1 = self.Xform( (self.root.x + c.scalebar["length"], 0) )[0]
        y = c.height - c.ymargin/2
        y0 = y - tw[1]
        y1 = y + tw[1]

        # actual scalebar
        cr.move_to(x0, y)
        cr.line_to(x1, y)
        cr.stroke()

        # whiskers
        cr.move_to(x0, y0)
        cr.line_to(x0, y1)
        cr.stroke()
        cr.move_to(x1, y0)
        cr.line_to(x1, y1)
        cr.stroke()

        # label
        cr.move_to((x0 + x1 - tw[0]) / 2., y0)
        cr.set_font_size(c.scalebar["textsize"])
        cr.show_text(showme)


#--------------------------------------------------
# For drawing a rectangular tree
#--------------------------------------------------

class PieTreeRect(PieTree):
    '''For plotting a rectangularly-oriented tree.'''

    def CalcXY(self, tipsize):
        '''Compute the (x, y) coordinate for each tip and node.
           These are stored as .x and .y node attributes.
           Also store horizontal scaling info as .xmax and .xscale.'''

        # todo: extract answer by using return rather than list
        def CXY(node, x, i, xmax):

            if node.length != None:
                x += node.length
            node.x = x

            if x > xmax[0]:
                xmax[0] = x

            if node.daughters != None:
                for d in node.daughters:
                    i = CXY(d, x, i, xmax)

            if node.daughters == None:
                node.y = i
                i += 1
            else:
                sum_y = 0.0
                for d in node.daughters:
                    sum_y += d.y
                node.y = sum_y / len(node.daughters)

            return i

        c = self.plot_vars

        xmax = [-1]
        CXY(self.root, 0, 0.5, xmax)
        c.xmax = xmax[0]
        c.xscale = (c.width - 2*c.xmargin - c.tipspacing - tipsize - \
                c.pieradius) / c.xmax

    def Xform(self, (x,y)):
        '''Transform (x, y) coordinates from tree to canvas.'''

        c = self.plot_vars
        return(c.xmargin + c.pieradius + c.linethick + x * c.xscale, \
                c.ymargin + y * c.tipspacing)

    def DrawTip(self, node):
        '''Draw the tip box, border, and label.'''

        c = self.plot_vars
        cr = self.surface

        # the tip box
        (x, y) = self.Xform( (node.x, node.y) )
        delta = c.boxsize
        cr.rectangle(x - delta/2., y-delta/2., delta, delta)

        # everything else
        self.DrawTipMore(node, (x,y), delta)

    def DrawPie(self, node):
        '''Draw the pie chart at this node.'''

        xy = self.Xform( (node.x, node.y) )
        self.DrawPieMore(node, xy) 

    def DrawFork(self, node):
        '''Draw the fork to this node's daughters.'''

        c = self.plot_vars
        cr = self.surface

        cr.set_line_width(c.linethick)
        cr.set_source_rgb(c.linecolor[0], c.linecolor[1], c.linecolor[2])

        (x0, y0) = self.Xform( (node.x, node.y) )

        for d in node.daughters:
            (x, y) = self.Xform( (d.x, d.y) )
            cr.move_to(x0, y0)
            cr.line_to(x0, y)
            cr.line_to(x, y)
            cr.stroke()

    def DrawNodeLabel(self, node):
        '''Put the text label by this node.'''

        xy = self.Xform( (node.x, node.y) )
        self.DrawNodeLabelMore(node, xy)

    def DrawRoot(self):
        '''Draw the branch leading to the root.'''

        c = self.plot_vars
        cr = self.surface

        (x0, y) = self.Xform( (0, self.root.y) )
        (x, y) = self.Xform( (self.root.x, self.root.y) )

        cr.set_line_width(c.linethick)
        cr.set_source_rgb(c.linecolor[0], c.linecolor[1], c.linecolor[2])
        cr.move_to(x, y)
        cr.line_to(x0, y)
        cr.stroke()


#--------------------------------------------------
# For drawing a circular tree
#--------------------------------------------------

class PieTreeRadial(PieTree):
    '''For plotting a radially-oriented tree.'''

    def CalcXY(self, tipsize):
        '''Compute the (x, y) and (r, theta) coordinate for each tip 
           and node.  These are stored as node attributes .x .y .r .t.
           Also store horizontal scaling info as .xmax and .xscale.'''

        def CalcRT(node, r, i, rmax, ntips):
            '''Compute the (r, theta) coordinates for each tip and node.
               These are stored as .r and .t attributes.'''

            if node.length != None:
                r += node.length
            node.r = r

            if r > rmax[0]:
                rmax[0] = r

            if node.daughters != None:
                for d in node.daughters:
                    i = CalcRT(d, r, i, rmax, ntips)

            if node.daughters == None:
                node.t = 2 * pi * i / ntips
                i += 1
            else:
                sum_t = 0.0
                for d in node.daughters:
                    sum_t += d.t
                node.t = sum_t / len(node.daughters)

            return i

        def RTtoXY(node):
            '''Convert polar to Cartesian coordinates.'''

            if node.daughters != None:
                for d in node.daughters:
                    RTtoXY(d)

            node.x = node.r * cos(node.t)
            node.y = node.r * sin(node.t)

        c = self.plot_vars

        rmax = [-1]
        CalcRT(self.root, 0, 0, rmax, self.ntips)
        RTtoXY(self.root)

        c.xmax = rmax[0] * 2
        c.xscale = (c.width - 2*c.xmargin - 2*c.tipspacing - 2*tipsize - \
                2*c.pieradius) / c.xmax

    def Xform(self, (x,y)):
        '''transform (x, y) coordinates from tree to canvas'''

        c = self.plot_vars
        return (x * c.xscale + c.width/2., y * c.xscale + c.height/2.)

    def DrawTip(self, node):
        '''Draw the tip box, border, and label.'''

        c = self.plot_vars
        cr = self.surface

        # the tip box
        (x, y) = self.Xform( (node.x, node.y) )
        delta = c.boxsize
        m = cr.get_matrix()  # for rotation, with set_matrix below
        cr.translate(x, y)
        cr.rotate(node.t)
        cr.rectangle(0, -delta/2., delta, delta)

        # everything else
        self.DrawTipMore(node, (0,0), delta*2)

        cr.set_matrix(m)

    def DrawPie(self, node):
        '''Draw the pie chart at this node.'''

        cr = self.surface

        (x, y) = self.Xform( (node.x, node.y) )
        m = cr.get_matrix()  # for rotation, with set_matrix below
        cr.translate(x, y)
        cr.rotate(node.t)

        self.DrawPieMore(node, (0,0)) 

        cr.set_matrix(m)

    def DrawFork(self, node):
        '''Draw the fork to this node's daughters.'''

        c = self.plot_vars
        cr = self.surface

        cr.set_line_width(c.linethick)
        cr.set_source_rgb(c.linecolor[0], c.linecolor[1], c.linecolor[2])

        (x0, y0) = self.Xform( (node.x, node.y) )

        (mint, maxt) = (2*pi, 0)
        for d in node.daughters:

            if d.t < mint:
                mint = d.t
            if d.t > maxt:
                maxt = d.t

            (xd, yd) = self.Xform( (d.x, d.y) )
            xa = node.r * cos(d.t)
            ya = node.r * sin(d.t)
            (xb, yb) = self.Xform( (xa, ya) )

            cr.move_to(xd, yd)
            cr.line_to(xb, yb)
            cr.stroke()

        cr.arc(c.width/2., c.height/2., node.r*c.xscale, mint, maxt)
        cr.stroke()

    def DrawNodeLabel(self, node):
        '''Put the text label by this node.'''

        cr = self.surface

        (x, y) = self.Xform( (node.x, node.y) )
        m = cr.get_matrix()  # for rotation, with set_matrix below
        cr.translate(x, y)
        cr.rotate(node.t)

        self.DrawNodeLabelMore(node, (0, 0) )

        cr.set_matrix(m)

    def DrawRoot(self):
        '''Draw the branch leading to the root.'''
        pass
