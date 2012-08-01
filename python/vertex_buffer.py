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
import sys
import ctypes
import numpy as np
import OpenGL
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut



class VertexAttribute(object):
    def __init__(self, count, gltype, stride, offset):
        self.count  = count
        self.gltype = gltype
        self.stride = stride
        self.offset = ctypes.c_void_p(offset)

class VertexAttribute_color(VertexAttribute):
    def __init__(self, count, gltype, stride, offset):
        assert count in (3, 4), \
            'Color attributes must have count of 3 or 4'
        VertexAttribute.__init__(self, count, gltype, stride, offset)
    def enable(self):
        gl.glColorPointer(self.count, self.gltype, self.stride, self.offset)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

class VertexAttribute_edge_flag(VertexAttribute):
    def __init__(self, count, gltype, stride, offset):
        assert count == 1, \
            'Edge flag attribute must have a size of 1'
        assert gltype in (gl.GL_BYTE, gl.GL_UNSIGNED_BYTE, gl.GL_BOOL), \
            'Edge flag attribute must have boolean type'
        VertexAttribute.__init__(self, 1, gltype, stride, offset)
    def enable(self):
        gl.glEdgeFlagPointer(self.stride, self.offset)
        gl.glEnableClientState(gl.GL_EDGE_FLAG_ARRAY)

class VertexAttribute_fog_coord(VertexAttribute):
    def __init__(self, count, gltype, stride, offset):
        VertexAttribute.__init__(self, count, gltype, stride, offset)
    def enable(self):
        gl.glFogCoordPointer(self.count, self.gltype, self.stride, self.offset)
        gl.glEnableClientState(gl.GL_FOG_COORD_ARRAY)

class VertexAttribute_normal(VertexAttribute):
    def __init__(self, count, gltype, stride, offset):
        assert count == 3, \
            'Normal attribute must have a size of 3'
        assert gltype in (gl.GL_BYTE, gl.GL_SHORT,
                          gl.GL_INT, gl.GL_FLOAT, gl.GL_DOUBLE), \
                                'Normal attribute must have signed type'
        VertexAttribute.__init__(self, 3, gltype, stride, offset)
    def enable(self):
        gl.glNormalPointer(self.gltype, self.stride, self.offset)
        gl.glEnableClientState(gl.GL_NORMAL_ARRAY)

class VertexAttribute_secondary_color(VertexAttribute):
    def __init__(self, count, gltype, strude, offset):
        assert count == 3, \
            'Secondary color attribute must have a size of 3'
        VertexAttribute.__init__(self, 3, gltype, stride, offset)
    def enable(self):
        gl.glSecondaryColorPointer(3, self.gltype, self.stride, self.offset)
        gl.glEnableClientState(gl.GL_SECONDARY_COLOR_ARRAY)

class VertexAttribute_tex_coord(VertexAttribute):
    def __init__(self, count, gltype, stride, offset):
        assert gltype in (gl.GL_SHORT, gl.GL_INT, gl.GL_FLOAT, gl.GL_DOUBLE), \
            'Texture coord attribute must have non-byte signed type'
        VertexAttribute.__init__(self, count, gltype, stride, offset)
    def enable(self):
        gl.glTexCoordPointer(self.count, self.gltype, self.stride, self.offset)
        gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)

class VertexAttribute_position(VertexAttribute):
    def __init__(self, count, gltype, stride, offset):
        assert count > 1, \
            'Vertex attribute must have count of 2, 3 or 4'
        assert gltype in (gl.GL_SHORT, gl.GL_INT, gl.GL_FLOAT, gl.GL_DOUBLE), \
            'Vertex attribute must have signed type larger than byte'
        VertexAttribute.__init__(self, count, gltype, stride, offset)
    def enable(self):
        gl.glVertexPointer(self.count, self.gltype, self.stride, self.offset)
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

class VertexAttribute_generic(VertexAttribute):
    def __init__(self, name, count, gltype, stride, offset, normalized=False ):
        assert count in (1, 2, 3, 4), \
            'Generic attributes must have count of 1, 2, 3 or 4'
        VertexAttribute.__init__(self, count, gltype, stride, offset)
        self.name = name
        self.index = -1
        self.normalized = normalized
    def enable(self):
        if self.index == -2:
            return;
        elif self.index == -1:
            program = gl.glGetIntegerv( gl.GL_CURRENT_PROGRAM )
            if program > 0:
                self.index = gl.glGetAttribLocation(program,self.name)
                if self.index == -1:
                    self.index == -2
                    return;
            else:
                return
        gl.glVertexAttribPointer( self.index, self.count, self.gltype,
                                  self.normalized, self.stride, self.offset )
        gl.glEnableVertexAttribArray( self.index )

class VertexBufferException(Exception):
    pass

class VertexBuffer(object):
    ''' '''
    def __init__(self, vertices, indices = None):
        gltypes = { 'float32': gl.GL_FLOAT,
                    'float'  : gl.GL_DOUBLE, 'float64': gl.GL_DOUBLE,
                    'int8'   : gl.GL_BYTE,   'uint8'  : gl.GL_UNSIGNED_BYTE,
                    'int16'  : gl.GL_SHORT,  'uint16' : gl.GL_UNSIGNED_SHORT,
                    'int32'  : gl.GL_INT,    'uint32' : gl.GL_UNSIGNED_INT }
        dtype = vertices.dtype
        names = dtype.names or []
        stride = vertices.itemsize
        offset = 0
        self.attributes = {}
        self.generic_attributes = []

        if indices is None:
            indices = np.arange(vertices.size,dtype=np.uint32)

        for name in names:
            if dtype[name].subdtype is not None:
                gtype = str(dtype[name].subdtype[0])
                count = reduce(lambda x,y:x*y, dtype[name].shape)
            else:
                gtype = str(dtype[name])
                count = 1
            if gtype not in gltypes.keys():
                raise VertexBufferException('Data type not understood')
            gltype = gltypes[gtype]
            if name in['position', 'color', 'normal', 'tex_coord',
                       'fog_coord', 'secondary_color', 'edge_flag']:
                vclass = 'VertexAttribute_%s' % name
                attribute = eval(vclass)(count,gltype,stride,offset)
                self.attributes[name[0]] = attribute
            else:
                attribute = VertexAttribute_generic(name,count,gltype,stride,offset)
                self.generic_attributes.append(attribute)
            offset += dtype[name].itemsize

        self.vertices_data = np.zeros(1, dtype)
        self.vertices_size = 0
        self.vertices_capacity = 1

        self.indices_data = np.zeros(1, dtype=np.uint32)
        self.indices_size = 0
        self.indices_capacity = 1

        self.objects = []

        self.append(vertices, indices)

        self.vertices_id = gl.glGenBuffers(1)
        gl.glBindBuffer( gl.GL_ARRAY_BUFFER, self.vertices_id )
        gl.glBufferData( gl.GL_ARRAY_BUFFER, self.vertices_data, gl.GL_STATIC_DRAW )
        gl.glBindBuffer( gl.GL_ARRAY_BUFFER, 0 )

        self.indices_id = gl.glGenBuffers(1)
        gl.glBindBuffer( gl.GL_ELEMENT_ARRAY_BUFFER, self.indices_id )
        gl.glBufferData( gl.GL_ELEMENT_ARRAY_BUFFER, self.indices_data, gl.GL_STATIC_DRAW )
        gl.glBindBuffer( gl.GL_ELEMENT_ARRAY_BUFFER, 0 )


    def append(self, vertices, indices = None):

        vertices = vertices.view(dtype=self.vertices_data.dtype)

        if indices is None:
            indices = np.arange(vertices.size,dtype=np.uint32)
        else:
            indices = indices.view(dtype=self.indices_data.dtype)

        # Test if current vertices capacity is big enough to hold new data
        if self.vertices_size + vertices.size  >= self.vertices_capacity:
            capacity = int(2**np.ceil(np.log2(self.vertices_size + len(vertices))))
            self.vertices_data = np.resize(self.vertices_data, capacity)
            self.vertices_capacity = len(self.vertices_data)

        # Test if current indices capacity is big enough to hold new data
        if self.indices_size + indices.size  >= self.indices_capacity:
            capacity = int(2**np.ceil(np.log2(self.indices_size + len(indices))))
            self.indices_data = np.resize(self.indices_data, capacity)
            self.indices_capacity = len(self.indices_data)

        # Add vertices data
        vstart, vend = self.vertices_size, self.vertices_size+len(vertices)
        self.vertices_data[vstart:vend] = vertices.ravel()

        # Add indices data and update them relatively to vertices new place
        istart, iend = self.indices_size, self.indices_size+len(indices)
        self.indices_data[istart:iend] = indices.ravel() + self.vertices_size

        # Keep track of new object
        self.objects.append( (vstart,vend,istart,iend) )

        # Update vertices, indices and transforms size
        self.vertices_size += vertices.size
        self.indices_size  += indices.size


    def get_vertices(self):
        """
        """
        return self.vertices_data[:self.vertices_size]
    vertices = property(get_vertices)

    def get_indices(self):
        """
        """
        return self.indices_data[:self.indices_size]
    indices = property(get_indices)

    def __len__(self):
        """
        """
        return len(self.objects)

    def __getitem__(self, key):
        """
        """
        vstart,vend,istart,iend = self.objects[key]
        return self.vertices_data[vstart:vend], self.indices_data[istart:iend]-vstart

    def __delitem__(self, key):
        """
        """
        vstart,vend,istart,iend,tstart,tend = self.objects[key]
        del self.objects[key]

        # Remove vertices
        vsize = self.vertices_size-vend
        self.vertices_data[vstart:vstart+vsize] = self.vertices_data[vend:vend+vsize]
        self.vertices_size -= vsize

        # Remove vertices
        msize = self.transforms_size-tend
        self.transforms_data[tstart:tstart+msize] = self.transforms_data[tend:tend+msize]
        self.transforms_size -= 1

        # Remove indices and update remaining indices
        isize = self.indices_size-iend
        self.indices_data[iend:iend+isize] -= vend-vstart
        self.indices_data[istart:istart+isize] = self.indices_data[iend:iend+isize]
        self.indices_size -= isize

        # Update all subsequent objects 
        for i in range(key, len(self.objects)):
            _vstart,_vend,_istart,_iend,_tstart,_tend = self.objects[i]
            self.objects[i] = [_vstart-vsize, _vend-vsize, \
                               _istart-isize, _iend-isize ]


    def upload(self):
        gl.glBindBuffer( gl.GL_ARRAY_BUFFER, self.vertices_id )
        gl.glBufferData( gl.GL_ARRAY_BUFFER,
                         self.vertices_data[:self.vertices_size], gl.GL_DYNAMIC_DRAW )
        gl.glBindBuffer( gl.GL_ARRAY_BUFFER, 0 )
        gl.glBindBuffer( gl.GL_ELEMENT_ARRAY_BUFFER, self.indices_id )
        gl.glBufferData( gl.GL_ELEMENT_ARRAY_BUFFER,
                         self.indices_data[:self.indices_size], gl.GL_DYNAMIC_DRAW )
        gl.glBindBuffer( gl.GL_ELEMENT_ARRAY_BUFFER, 0 )


    def draw( self, mode=gl.GL_TRIANGLES, what='pnctesf' ):
        gl.glPushClientAttrib( gl.GL_CLIENT_VERTEX_ARRAY_BIT )
        gl.glBindBuffer( gl.GL_ARRAY_BUFFER, self.vertices_id )
        gl.glBindBuffer( gl.GL_ELEMENT_ARRAY_BUFFER, self.indices_id )
        for attribute in self.generic_attributes:
            attribute.enable()
        for c in self.attributes.keys():
            if c in what:
                self.attributes[c].enable()
        gl.glDrawElements( mode, self.indices_size, gl.GL_UNSIGNED_INT, None)
        gl.glBindBuffer( gl.GL_ELEMENT_ARRAY_BUFFER, 0 )
        gl.glBindBuffer( gl.GL_ARRAY_BUFFER, 0 )
        gl.glPopClientAttrib( )
