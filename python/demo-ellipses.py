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

from grid import Grid
from collection import EllipseCollection


def on_display( ):
    gl.glClearColor(1,1,1,1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glEnable(gl.GL_BLEND)
    grid.draw()
    collection.draw()
    glut.glutSwapBuffers()

    
def on_reshape( width, height ):
    gl.glViewport( 0, 0, width, height )
    gl.glMatrixMode( gl.GL_PROJECTION )
    gl.glLoadIdentity( )
    gl.glOrtho( 0, width, 0, height, -1000, 1000 )
    gl.glMatrixMode( gl.GL_MODELVIEW )
    gl.glLoadIdentity( )

    grid.update()


def on_keyboard( key, x, y ):
    if key == '\033':
        sys.exit( )


def on_motion( x, y ):
    global offset, mouse
    _,_,w,h = gl.glGetIntegerv(gl.GL_VIEWPORT)
    y = h-y
    dx,dy = x-mouse[0], y-mouse[1]
    offset += dx,dy
    mouse = x,y
    collection.set_offsets( offset )
    grid._transform = offset[0],offset[1],int(zoom),0
    glut.glutPostRedisplay()


def on_passive_motion( x, y ):
    global mouse
    _,_,w,h = gl.glGetIntegerv(gl.GL_VIEWPORT)
    mouse = x,h-y


def on_scroll(dx, dy):
    global offset, zoom, mouse
    x,y = mouse
    z = min(max(25.,zoom+0.001*dy*zoom), 1000.)
    offset[0] = x-int(z)*(x-offset[0])/int(zoom)
    offset[1] = y-int(z)*(y-offset[1])/int(zoom)
    zoom = z
    collection.set_offsets( offset )
    collection.set_scales( int(zoom) )
    grid._transform = offset[0],offset[1],int(zoom),0
    glut.glutPostRedisplay()

def on_wheel(wheel, direction, x, y):
    if wheel == 0:
        on_scroll(0,direction)
    elif wheel == 1:
        on_scroll(direction,0)


def on_idle():
    global t, t0, frames
    t = glut.glutGet( glut.GLUT_ELAPSED_TIME )
    frames = frames + 1
    if t-t0 > 2500:
        print "FPS : %.2f (%d frames in %.2f second)" % (frames*1000.0/(t-t0), frames, (t-t0)/1000.0)
        t0, frames = t,0
    glut.glutPostRedisplay()


if __name__ == '__main__':
    import sys

    # For OSX, see https://github.com/nanoant/osxglut
    # GLUT for Mac OS X fork with Core Profile and scroll wheel support
    try:
        from ctypes import c_float
        from OpenGL.GLUT.special import GLUTCallback
        glutScrollFunc = GLUTCallback(
            'Scroll', (c_float,c_float), ('delta_x','delta_y'),)
    except:
        glutScrollFunc = None

    glut.glutInit( sys.argv )
    glut.glutInitDisplayMode( glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH )
    glut.glutCreateWindow( sys.argv[0] )
    glut.glutReshapeWindow( 512, 512 )
    glut.glutDisplayFunc( on_display )
    glut.glutReshapeFunc( on_reshape )
    glut.glutKeyboardFunc( on_keyboard )
    glut.glutIdleFunc( on_idle )
    glut.glutMotionFunc( on_motion )
    glut.glutPassiveMotionFunc( on_passive_motion )
    if glutScrollFunc:
        glutScrollFunc( on_scroll)
    elif glut.glutMouseWheelFunc:
        glutMouseWheelFunc( on_wheel)


    t0, t, frames = glut.glutGet(glut.GLUT_ELAPSED_TIME), 0, 0

    zoom = 75.0
    offset = np.array([256.,256.])
    mouse = 0,0

    n = 2500
    centers = np.random.uniform( -5,5, (n,3) )
    centers[:,2] = 0
    radii = np.random.uniform( 0.05, 0.10, (n,2) )
    edgecolors = 0,0,0,.5
    facecolors = np.random.uniform(0,1, (n,4))
    facecolors[:,3] = .5
    transforms = np.zeros((n,4))
    transforms[:,3] = np.random.uniform( 0.0, 2*np.pi, n )
    collection = EllipseCollection( centers, radii, transforms = transforms,
                                    edgecolors=edgecolors, facecolors=facecolors )
    collection.set_offsets( (offset[0],offset[1]) )
    collection.set_scales( int(zoom) )

    grid = Grid()
    grid.set_transforms( (offset[0],offset[1],int(zoom),0) )

    glut.glutMainLoop( )


