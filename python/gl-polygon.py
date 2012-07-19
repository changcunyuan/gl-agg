#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import ctypes
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut

from shader import Shader
import fbo


from numpy import *
def ortho( P ) :
    O = empty_like(P)
    O[0] = -P[1]
    O[1] = P[0]
    return O/sqrt(P[0]*P[0] + P[1]*P[1])

def intersection(a1,a2,b1,b2):
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = ortho(da)
    denom = dot( dap, db)
    num = dot( dap, dp )
    return (num / denom)*db + b1


vert = '''
void main()
{
    gl_FrontColor = gl_Color;    
    gl_TexCoord[0].xy = gl_MultiTexCoord0.xy;
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
'''

frag = '''
uniform float support;
uniform float thickness;
void main()
{
    float t = (thickness+2.5*support)/2.0;
    float dist = gl_TexCoord[0].x;
    vec4 color = gl_Color;

    float d = abs(dist-t);
    t = thickness/2.0-support;
    d = d-t;
    if( d < 0.0 )
    {
        gl_FragColor = color;
    }
    else
    {
        float alpha = d/support;
        alpha = exp(-alpha*alpha);
        gl_FragColor = vec4(color.xyz, alpha*color.a);
    }
}
'''

def triangle(P0, P1, P2, thickness=1.0, support=0.75):
     
    alpha = min(thickness, 1.0)
    thickness = max(thickness, 1.0)
    w = math.ceil(2.5*support+thickness)/2.0
    V0 = P2-P1
    V1 = P2-P0
    V2 = P1-P0

    d = abs(np.cross(V1,V2))/np.sqrt(np.vdot(V0,V0))
    gl.glColor( 0,0,0, alpha)
    gl.glBegin( gl.GL_TRIANGLES )
    gl.glTexCoord2f( d, 0 ), gl.glVertex( P0[0], P0[1], 0 )
    gl.glTexCoord2f( 0, 0 ), gl.glVertex( P1[0], P1[1], 0 )
    gl.glTexCoord2f( 0, 0 ), gl.glVertex( P2[0], P2[1], 0 )
    gl.glEnd( )


def polygon(P, thickness=1.0, support=0.75):

    C = P.sum(axis=0)/len(P)
    for i in range(len(P)):
        P0 = P[i]
        P1 = P[(i+1)%len(P)]
        triangle( C, P0, P1, thickness=thickness, support=support )


def on_display( ):
    global shader

    gl.glClearColor(1,1,1,1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glEnable(gl.GL_BLEND)

    radius = 255.0
    theta, dtheta = 0, 5.5/180.0*math.pi
    support = 0.75
    thickness = 1.0
    shader.bind()
    shader.uniformf('support', support)
    shader.uniformf('thickness', thickness)

    for i in range(500):
        xc =    256+radius*math.cos(theta);
        yc = 32+256+radius*math.sin(theta);
        r = 10.1 + thickness/2.0 + 1.25*support - i*0.02
        P = [(xc+cos(t+theta)*r, yc+sin(t+theta)*r)
                       for t in np.linspace(0,2*np.pi,6,endpoint=False)]
        polygon(np.array(P).reshape(6,2), thickness, support)

        radius -= 0.45
        theta += dtheta

    for i in range(0,39):
        thickness = (i+1)/10.0
        shader.uniformf('thickness', thickness)
        r = 4 + max(thickness,1.0)/2 + 1.25*support
        xc = 20+i*12.5 - r
        yc = 16
        P = [(xc+cos(t)*r, yc+sin(t)*r)
             for t in np.linspace(0,2*np.pi,6,endpoint=False)]
        polygon(np.array(P).reshape(6,2), thickness, support)
    shader.unbind()

    glut.glutSwapBuffers()

    
def on_reshape( width, height ):
    gl.glViewport( 0, 0, width, height )
    gl.glMatrixMode( gl.GL_PROJECTION )
    gl.glLoadIdentity( )
    gl.glOrtho( 0, width, 0, height, -1, 1 )
    gl.glMatrixMode( gl.GL_MODELVIEW )
    gl.glLoadIdentity( )


def on_keyboard( key, x, y ):
    if key == '\033':
        sys.exit( )
    if key == ' ':
        fbo.save(on_display, "gl-polygon.png")


if __name__ == '__main__':
    import sys
    glut.glutInit( sys.argv )
    glut.glutInitDisplayMode( glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH )
    glut.glutCreateWindow( sys.argv[0] )
    glut.glutReshapeWindow( 512, 512+32 )
    glut.glutDisplayFunc( on_display )
    glut.glutReshapeFunc( on_reshape )
    glut.glutKeyboardFunc( on_keyboard )
    shader = Shader(vert,frag)

    glut.glutMainLoop( )


