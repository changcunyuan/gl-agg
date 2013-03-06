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
import fbo

# For OSX, see https://github.com/nanoant/osxglut
# GLUT for Mac OS X fork with Core Profile and scroll wheel support
from ctypes import c_float
from OpenGL.GLUT.special import GLUTCallback
try:
    glutScrollFunc = GLUTCallback(
        'Scroll', (c_float,c_float), ('delta_x','delta_y'),)
except:
    glutScrollFunc = None


vert = """
    void main()
    {
        gl_FrontColor = gl_Color;    
        gl_TexCoord[0].xyz = gl_MultiTexCoord0.xyz;
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    }
"""

frag = """
    float
    compute_alpha(float d, float thickness, float support)
    {
        d -= thickness/2.0-support;
        if( d < 0.0 )
        {
            return 1.0;
        }
        else
        {
            float alpha = d/support;
            alpha = exp(-alpha*alpha);
            return alpha;
        }
    }

    uniform vec2  size;
    uniform float major_grid_width, minor_grid_width;
    uniform vec4  major_grid_color, minor_grid_color;
    uniform vec2  major_tick_size,  minor_tick_size;
    uniform float major_tick_width, minor_tick_width;
    uniform vec4  major_tick_color, minor_tick_color;
    uniform sampler1D texture;
    void main() 
    { 
        // Major grid
        float Mx = texture1D(texture, gl_TexCoord[0].x+.001).x;
        float My = texture1D(texture, gl_TexCoord[0].y+.001).y;
        float M = min(Mx,My);

        // Minor grid
        float mx = texture1D(texture, gl_TexCoord[0].x+.001).z;
        float my = texture1D(texture, gl_TexCoord[0].y+.001).w;
        float m = min(mx,my);

        vec4 color = major_grid_color;
        float alpha1 = compute_alpha( M, major_grid_width, 0.55);
        float alpha2 = compute_alpha( m, minor_grid_width, 0.60);
        float alpha  = alpha1;
        if( alpha2 > alpha1 )
        {
            alpha = alpha2;
            color = minor_grid_color;
        }

        float x = gl_TexCoord[0].x * size.x;
        float y = gl_TexCoord[0].y * size.y;

        // Top major ticks
        if( y > (size.y-major_tick_size.y) )
        {
            float a = compute_alpha(Mx, major_tick_width, 0.5);
            if (a > alpha)
            {
                alpha = a;
                color = major_tick_color;
            }
        }

        // Bottom major ticks
        if( y < major_tick_size.y )
        {
            float a = compute_alpha(Mx, major_tick_width, 0.5);
            if (a > alpha)
            {
                alpha = a;
                color = major_tick_color;
            }
        }

        // Left major ticks
        if( x < major_tick_size.x )
        {
            float a = compute_alpha(My, major_tick_width, 0.5);
            if (a > alpha )
            {
                alpha = a;
                color = major_tick_color;
            }
        }

        // Right major ticks
        if( x > (size.x-major_tick_size.x) )
        {
            float a = compute_alpha(My, major_tick_width, 0.5);
            if (a > alpha )
            {
                alpha = a;
                color = major_tick_color;
            }
        }

        // Top minor ticks
        if( y > (size.y-minor_tick_size.y) )
        {
            float a = compute_alpha(mx, minor_tick_width, 0.5);
            if (a > alpha)
            {
                alpha = a;
                color = minor_tick_color;
            }
        }

        // Bottom minor ticks
        if( y < minor_tick_size.y )
        {
            float a = compute_alpha(mx, minor_tick_width, 0.5);
            if (a > alpha)
            {
                alpha = a;
                color = minor_tick_color;
            }
        }

        // Left minor ticks
        if( x < minor_tick_size.x )
        {
            float a = compute_alpha(my, minor_tick_width, 0.5);
            if (a > alpha )
            {
                alpha = a;
                color = minor_tick_color;
            }
        }

        // Right major ticks
        if( x > (size.x-minor_tick_size.x) )
        {
            float a = compute_alpha(my, minor_tick_width, 0.5);
            if (a > alpha )
            {
                alpha = a;
                color = minor_tick_color;
            }
        }

        gl_FragColor = vec4(color.xyz, alpha*color.a);
    }"""


def on_display( ):
    gl.glClearColor(1,1,1,1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glEnable(gl.GL_BLEND)

    global t, t0, frames
    t = glut.glutGet( glut.GLUT_ELAPSED_TIME )
    frames = frames + 1
    if t-t0 > 2500:
        print "FPS : %.2f (%d frames in %.2f second)" % (frames*1000.0/(t-t0), frames, (t-t0)/1000.0)
        t0, frames = t,0

    shader.bind()
    shader.uniformi( 'texture',           0)
    shader.uniformf( 'size',              w,h)
    shader.uniformf( 'major_grid_width',   major_grid_width )
    shader.uniformf( 'minor_grid_width',   minor_grid_width )
    shader.uniformf( 'major_grid_color',  *major_grid_color )
    shader.uniformf( 'minor_grid_color',  *minor_grid_color )
    shader.uniformf( 'major_tick_size',   *major_tick_size )
    shader.uniformf( 'minor_tick_size',   *minor_tick_size )
    shader.uniformf( 'major_tick_width',   major_tick_width )
    shader.uniformf( 'minor_tick_width',   minor_tick_width )
    shader.uniformf( 'major_tick_color',  *major_tick_color )
    shader.uniformf( 'minor_tick_color',  *minor_tick_color )
    axis.draw( gl.GL_TRIANGLES )
    shader.unbind()

    glut.glutSwapBuffers()


def on_motion( x, y ):
    global offset, mouse
    _,_,w,h = gl.glGetIntegerv(gl.GL_VIEWPORT)
    y = h-y
    dx,dy = x-mouse[0], y-mouse[1]
    offset += dx,dy
    mouse = x,y
    update()

    glut.glutPostRedisplay()

def on_passive_motion( x, y ):
    global mouse
    _,_,w,h = gl.glGetIntegerv(gl.GL_VIEWPORT)
    mouse = x,h-y

def on_scroll(dx, dy):
    global offset, zoom, mouse
    x,y = mouse
    z = min(max(0.5,zoom+.001*dy*zoom), 10)
    offset[0] = x-z*(x-offset[0])/zoom 
    offset[1] = y-z*(y-offset[1])/zoom 
    zoom = z
    update()

    glut.glutPostRedisplay()

def on_reshape( width, height ):
    gl.glViewport( 0, 0, width, height )
    gl.glMatrixMode( gl.GL_PROJECTION )
    gl.glLoadIdentity( )
    gl.glOrtho( 0, width, 0, height, -1, 1 )
    gl.glMatrixMode( gl.GL_MODELVIEW )
    gl.glLoadIdentity( )
    update()


def update():
    _,_,w,h = gl.glGetIntegerv(gl.GL_VIEWPORT)
    aspect = float(h)/float(w)
    axis.vertices['position'][0] = 0, 0
    axis.vertices['position'][1] = w, 0
    axis.vertices['position'][2] = w, h
    axis.vertices['position'][3] = 0, h
    axis.upload()

    n = len(Z)
    L = np.linspace(0,w,n)

    t = major_grid[0]*zoom
    #I = np.arange(np.fmod(offset[0],t), np.fmod(offset[0],t)+w+t,t)
    I = np.logspace(np.log10(1), np.log10(2*w), 5)*zoom
    Z[:,0] = abs(L-I.reshape(len(I),1)).min(axis=0)

    t = minor_grid[0]*zoom
    #I = np.arange(np.fmod(offset[0],t), np.fmod(offset[0],t)+w+t,t)
    I = np.logspace(np.log10(1), np.log10(2*w), 50)*zoom
    Z[:,2] = abs(L-I.reshape(len(I),1)).min(axis=0)

    L = np.linspace(0,h,n)

    t = major_grid[1]*zoom
    #I = np.arange(np.fmod(offset[1],t), np.fmod(offset[1],t)+h+t,t)
    I = np.logspace(np.log10(1), np.log10(2*h), 5)*zoom
    Z[:,1] = abs(L-I.reshape(len(I),1)).min(axis=0)

    t = minor_grid[1]*zoom
    #I = np.arange(np.fmod(offset[1],t), np.fmod(offset[1],t)+h+t,t)
    I = np.logspace(np.log10(1), np.log10(2*h), 50)*zoom
    Z[:,3] = abs(L-I.reshape(len(I),1)).min(axis=0)

    gl.glBindTexture( gl.GL_TEXTURE_1D, texid )
    gl.glTexImage1D (gl.GL_TEXTURE_1D, 0, gl.GL_RGBA32F, len(Z), 0, gl.GL_RGBA, gl.GL_FLOAT, Z)


def on_keyboard( key, x, y ):
    if key == '\033':
        sys.exit( )
    if key == ' ':
        fbo.save(on_display, "gl-grid.png")


def on_idle():
    glut.glutPostRedisplay()

if __name__ == '__main__':
    import sys
    glut.glutInit( sys.argv )
    glut.glutInitDisplayMode( glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH )
    glut.glutCreateWindow( sys.argv[0] )
    glut.glutReshapeWindow( 512, 512 )
    glut.glutDisplayFunc( on_display )
    glut.glutReshapeFunc( on_reshape )
    glut.glutKeyboardFunc( on_keyboard )
    glut.glutMotionFunc( on_motion )
    glut.glutPassiveMotionFunc( on_passive_motion )

    glutScrollFunc( on_scroll)
    glut.glutIdleFunc( on_idle )

    shader = Shader(vert,frag)
    t0, frames, t = 0,0,0
    t0 = glut.glutGet(glut.GLUT_ELAPSED_TIME)
    offset = np.zeros(2)
    zoom = 1.0
    mouse = 0,0

    Z = np.zeros((2*1024,4),dtype=np.float32)
    gl.glEnable (gl.GL_TEXTURE_1D)
    texid = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_1D, texid)
    gl.glPixelStorei (gl.GL_UNPACK_ALIGNMENT, 1)
    gl.glPixelStorei (gl.GL_PACK_ALIGNMENT, 1)
    gl.glTexParameterf (gl.GL_TEXTURE_1D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameterf (gl.GL_TEXTURE_1D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameterf (gl.GL_TEXTURE_1D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameterf (gl.GL_TEXTURE_1D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
    gl.glPixelTransferf(gl.GL_ALPHA_SCALE, 1)
    gl.glPixelTransferf(gl.GL_ALPHA_BIAS, 0)

    w,h = 512,512
    V = np.array( [ ((0, 0), (0,0)),
                    ((w, 0), (1,0)),
                    ((w, h), (1,1)),
                    ((0, h), (0,1)) ],
                  dtype = [('position','f4',2), ('tex_coord','f4',2)] )
    I = np.array( [0,1,2, 0,2,3 ], dtype=np.uint32 )
    axis = VertexBuffer(V,I)

    major_grid = np.array([64.0,64.0])
    minor_grid = np.array([64.0,64.0])/5.0
    major_grid_color = np.array([0.75, 0.75, 0.75, 1.0*0.75])
    minor_grid_color = np.array([0.75, 0.75, 0.75, 1.0*0.25])
    major_tick_color = np.array([0.0, 0.0, 0.0, 1.00])
    minor_tick_color = np.array([0.0, 0.0, 0.0, 1.00*0.75])
    major_grid_width = 1.0 #0.75
    minor_grid_width = 1.0 #0.25
    major_tick_size = np.array([5.0,5.0]) #*zoom
    minor_tick_size = np.array([3.5,3.5]) #*zoom
    major_tick_width = 1.50
    minor_tick_width = 1.00 #0.75


    glut.glutMainLoop( )

