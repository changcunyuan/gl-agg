#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# OpenGL Anti-Grain Geometry (GL-AGG) - Version 0.1
# A high quality OpenGL rendering engine
# Copyright (C) 2012 Nicolas P. Rougier. All rights reserved.
# Contact: Nicolas.Rougier@gmail.com
#          http://code.google.com/p/gl-agg/
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY NICOLAS P. ROUGIER ''AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL NICOLAS P. ROUGIER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of Nicolas P. Rougier.
# ----------------------------------------------------------------------------
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
from shader import Shader
from vertex_buffer import VertexBuffer
from grid import Grid


class Collection(object):

    def __init__(self):
        self._transform = [0.0,0.0,1.0,0.0]


    def set_scale(self, scale):
        """ """
        self._transform[2] = scale


    def set_offset(self, offset):
        """ """
        self._transform[0] = offset[0]
        self._transform[1] = offset[1]


    def set_transform(self, transform):
        """ """
        self._transform = list(transform)


    def set_colors(self, colors):
        """ """

        self._buffer.vertices['color'] = colors
        self._dirty = True

    def set_linewidths(self, linewidths):
        """ """

        self._buffer.vertices['thickness'] = linewidths
        self._dirty = True


    def set_antialiased(self, antialiased):
        """ """
        self._buffer.vertices['support'] = antialiased
        self._dirty = True


    def draw(self):
        """ """
        if self._dirty:
            self._buffer.upload()
            self._dirty = False
        self._shader.bind()
        self._shader.uniformf('Transform', *self._transform)
        self._buffer.draw( gl.GL_TRIANGLES )
        self._shader.unbind()




class LineCollection(Collection):

    def __init__ (self, segments, linewidths = 1.0, colors = (0,0,0,1),
                  caps = (1,1), transforms = (0,0,1,0), antialiased = 0.75):
        """ """

        Collection.__init__(self)
        self.dtype = np.dtype( [('position',  'f4', 3),
                                ('tex_coord', 'f4', 2),
                                ('color',     'f4', 4),
                                ('transform', 'f4', 4),
                                ('tangent',   'f4', 2),
                                ('cap',       'f4', 2),
                                ('length',    'f4', 1),
                                ('thickness', 'f4', 1),
                                ('support',   'f4', 1)] )
        vertices = np.zeros(0, dtype = self.dtype)
        self._buffer = VertexBuffer(vertices)
        self.append(segments, linewidths, colors, caps, transforms, antialiased)
        vert = open('./line.vert').read()
        frag = open('./line.frag').read()
        self._shader = Shader(vert,frag)



    def append(self, segments, linewidths = 1.0, colors = (0,0,0,1),
               caps = (1,1), transforms = (0,0,1,0), antialiased = 0.75):
        """ """

        linewidths  = np.atleast_1d(linewidths)
        colors      = np.atleast_2d(colors)
        caps        = np.atleast_2d(caps)
        transforms  = np.atleast_2d(transforms)
        antialiased = np.atleast_1d(antialiased)

        for i,segment in enumerate(segments):
            thickness    = linewidths[ i % len(linewidths)]
            color        = colors[ i % len(colors)]
            cap          = caps[ i % len(caps)]
            transform    = transforms[ i % len(transforms)]
            support      = antialiased[ i % len(antialiased)]

            # Points as array
            P = np.array(segment).reshape(len(segment),3).astype(float)

            # Tangent vectors 
            T = np.zeros_like(P)
            T[:-1] = P[1:] - P[:-1]
            T[-1] = T[-2]
            T = T[:,0:2]
            L = np.sqrt(T[:,0]**2 + T[:,1]**2)
            T /= L.reshape(len(P),1)

            # Lengths
            L = np.cumsum(L)
            L[1:] = L[:-1]
            L[0] = 0
            length = L[-1]

            # Special case for start and end caps
            L[0],L[-1]  = -1, length+1

            n = len(P)
            vertices = np.zeros(n, dtype = self.dtype)
            vertices['position'] = P
            vertices['tangent']  = T
            vertices['thickness'] = thickness
            vertices['color'] = color
            vertices['cap'] = cap
            vertices['length'] = length
            vertices['support'] = support
            vertices['transform'] = transform
            vertices['tex_coord'][:,0] = L
            vertices = np.repeat(vertices, 2)
            vertices['tex_coord'][0::2,1] = -1
            vertices['tex_coord'][1::2,1] = +1
            indices = np.resize( np.array([0,1,2,1,2,3], dtype=np.uint32), (n-1)*(2*3))
            indices += np.repeat( 2*np.arange(n-1), 6)
            self._buffer.append( vertices, indices )

        self._dirty = True



class CircleCollection(Collection):

    def __init__ (self, centers, radii, linewidths = 1.0,
                  edgecolors = (0,0,0,1), facecolors = (0,0,0,1),
                  transforms = (0,0,1,0), antialiased = 0.75):
        """ """

        Collection.__init__(self)
        self.dtype = np.dtype( [('position',  'f4', 3),
                                ('tex_coord', 'f4', 2),
                                ('color',     'f4', 4),
                                ('facecolor', 'f4', 4),
                                ('transform', 'f4', 4),
                                ('radius',    'f4', 1),
                                ('thickness', 'f4', 1),
                                ('support',   'f4', 1)] )
        vertices = np.zeros(0, dtype = self.dtype)
        self._buffer = VertexBuffer(vertices)
        self.append(centers, radii, linewidths, edgecolors, facecolors, transforms, antialiased)
        vert = open('./circle.vert').read()
        frag = open('./circle.frag').read()
        self._shader = Shader(vert,frag)



    def append (self, centers, radii, linewidths = 1.0,
                edgecolors = (0,0,0,1), facecolors = (0,0,0,1),
                transforms = (0,0,1,0), antialiased = 0.75):
        """ """

        linewidths  = np.atleast_1d(linewidths)
        radii       = np.atleast_1d(radii)
        edgecolors  = np.atleast_2d(edgecolors)
        facecolors  = np.atleast_2d(facecolors)
        transforms  = np.atleast_2d(transforms)
        antialiased = np.atleast_1d(antialiased)

        for i,center in enumerate(centers):
            thickness    = linewidths[ i % len(linewidths)]
            edgecolor    = edgecolors[ i % len(edgecolors)]
            facecolor    = facecolors[ i % len(facecolors)]
            radius       = radii[ i % len(radii)]
            transform    = transforms[ i % len(transforms)]
            support      = antialiased[ i % len(antialiased)]

            # Points as array
            P = np.array(center).reshape(1,3).astype(float)
            vertices = np.zeros(1, dtype = self.dtype)
            vertices['position'] = P
            vertices['thickness'] = thickness
            vertices['color'] = edgecolor
            vertices['facecolor'] = facecolor
            vertices['radius'] = radius
            vertices['support'] = support
            vertices['transform'] = transform
            vertices = np.repeat(vertices, 4)
            vertices['tex_coord'][0::4] = -1,-1
            vertices['tex_coord'][1::4] = +1,-1
            vertices['tex_coord'][2::4] = +1,+1
            vertices['tex_coord'][3::4] = -1,+1
            indices = np.array([0,1,2,0,2,3], dtype=np.uint32)
            self._buffer.append( vertices, indices )

        self._dirty = True


class EllipseCollection(Collection):

    def __init__ (self, centers, radii, linewidths = 1.0,
                  edgecolors = (0,0,0,1), facecolors = (0,0,0,1),
                  transforms = (0,0,1,0), antialiased = 0.75):
        """ """

        Collection.__init__(self)
        self.dtype = np.dtype( [('position',  'f4', 3),
                                ('tex_coord', 'f4', 2),
                                ('color',     'f4', 4),
                                ('facecolor', 'f4', 4),
                                ('transform', 'f4', 4),
                                ('radius',    'f4', 2),
                                ('thickness', 'f4', 1),
                                ('support',   'f4', 1)] )
        vertices = np.zeros(0, dtype = self.dtype)
        self._buffer = VertexBuffer(vertices)
        self.append(centers, radii, linewidths, edgecolors, facecolors, transforms, antialiased)
        vert = open('./ellipse.vert').read()
        frag = open('./ellipse.frag').read()
        self._shader = Shader(vert,frag)



    def append (self, centers, radii, linewidths = 1.0,
                edgecolors = (0,0,0,1), facecolors = (0,0,0,1),
                transforms = (0,0,1,0), antialiased = 0.75):
        """ """

        linewidths  = np.atleast_1d(linewidths)
        radii       = np.atleast_2d(radii)
        edgecolors  = np.atleast_2d(edgecolors)
        facecolors  = np.atleast_2d(facecolors)
        transforms  = np.atleast_2d(transforms)
        antialiased = np.atleast_1d(antialiased)

        for i,center in enumerate(centers):
            thickness    = linewidths[ i % len(linewidths)]
            edgecolor    = edgecolors[ i % len(edgecolors)]
            facecolor    = facecolors[ i % len(facecolors)]
            radius       = radii[ i % len(radii)]
            transform    = transforms[ i % len(transforms)]
            support      = antialiased[ i % len(antialiased)]

            # Points as array
            P = np.array(center).reshape(1,3).astype(float)
            vertices = np.zeros(1, dtype = self.dtype)
            vertices['position'] = P
            vertices['thickness'] = thickness
            vertices['color'] = edgecolor
            vertices['facecolor'] = facecolor
            vertices['radius'] = radius
            vertices['support'] = support
            vertices['transform'] = transform
            vertices = np.repeat(vertices, 4)
            vertices['tex_coord'][0::4] = -1,-1
            vertices['tex_coord'][1::4] = +1,-1
            vertices['tex_coord'][2::4] = +1,+1
            vertices['tex_coord'][3::4] = -1,+1
            indices = np.array([0,1,2,0,2,3], dtype=np.uint32)
            self._buffer.append( vertices, indices )

        self._dirty = True
