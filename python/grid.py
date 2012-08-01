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


class Grid(object):

    def __init__(self,
                 major_lines        = (1.00, 1.00, 0.75),
                 major_lines_color  = (0.75, 0.75, 0.75, 1.00),
                 major_ticks        = (5.00, 5.00, 1.50),
                 major_ticks_color  = (0.00, 0.00, 0.00, 1.00),
                 minor_lines        = (0.10, 0.10, 0.25),
                 minor_lines_color  = (0.75, 0.75, 0.75, 1.00),
                 minor_ticks        = (2.50, 2.50, 1.00),
                 minor_ticks_color  = (0.00, 0.00, 0.00, 1.00) ):
        self._major_lines          = np.array(major_lines)
        self._major_lines_color    = np.array(major_lines_color)
        self._major_ticks          = np.array(major_ticks)
        self._major_ticks_color    = np.array(major_ticks_color)
        self._minor_lines          = np.array(minor_lines)
        self._minor_lines_color    = np.array(minor_lines_color)
        self._minor_ticks          = np.array(minor_ticks)
        self._minor_ticks_color    = np.array(minor_ticks_color)

        vert = open('./grid.vert').read()
        frag = open('./grid.frag').read()
        self._shader = Shader(vert,frag)
        self._transform = 0.0,0.0,100.0,0.0

        w,h = 512,512
        vertices = np.array( [ ((0, 0), (0,0)),
                               ((w, 0), (w,0)),
                               ((w, h), (w,h)),
                               ((0, h), (0,h)) ],
                             dtype = [('position','f4',2), ('tex_coord','f4',2)] )
        vertices['position'] += .315,.315
        indices = np.array( [0,1,2, 0,2,3 ], dtype=np.uint32 )
        self._buffer = VertexBuffer(vertices,indices)


    def set_transforms(self, transforms):
        """ """

        self._transform = transforms


    def update(self):
        """ """

        _,_,w,h = gl.glGetIntegerv(gl.GL_VIEWPORT)
        self._buffer.vertices['position'][0] = 0, 0
        self._buffer.vertices['position'][1] = w, 0
        self._buffer.vertices['position'][2] = w, h
        self._buffer.vertices['position'][3] = 0, h
        self._buffer.vertices['position'] += .315, .315
        self._buffer.vertices['tex_coord'][0] = 0, 0
        self._buffer.vertices['tex_coord'][1] = w, 0
        self._buffer.vertices['tex_coord'][2] = w, h
        self._buffer.vertices['tex_coord'][3] = 0, h
        self._buffer.upload()


    def draw(self):

        x,y,scale,rotation = self._transform
        _,_,w,h = gl.glGetIntegerv(gl.GL_VIEWPORT)

        shader = self._shader
        shader.bind()
        shader.uniformf( 'size',               w,h)
        shader.uniformf( 'offset',             x,y)

        x,y,t   = self._major_lines
        r,g,b,a = self._major_lines_color
        shader.uniformf( 'major_lines',        x*scale, y*scale, max(t,1.0) )
        shader.uniformf( 'major_lines_color',  r,g,b,a*min(t,1.0) )

        x,y,t   = self._major_ticks
        r,g,b,a = self._major_ticks_color
        shader.uniformf( 'major_ticks',        x,y,max(t,1.0) )
        shader.uniformf( 'major_ticks_color',  r,g,b,a*min(t,1.0) )

        x,y,t   = self._minor_lines
        r,g,b,a = self._minor_lines_color
        shader.uniformf( 'minor_lines',        x*scale, y*scale, max(t,1.0) )
        shader.uniformf( 'minor_lines_color',  r,g,b,a*min(t,1.0) )

        x,y,t   = self._minor_ticks
        r,g,b,a = self._minor_ticks_color
        shader.uniformf( 'minor_ticks',        x,y,max(t,1.0) )
        shader.uniformf( 'minor_ticks_color',  r,g,b,a*min(t,1.0) )

        self._buffer.draw( gl.GL_TRIANGLES )
        shader.unbind()
        
