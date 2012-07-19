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
    gl_TexCoord[0].xyz = gl_MultiTexCoord0.xyz;
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
'''

frag = '''
uniform float support;
uniform float thickness;
void main()
{
    float t = (thickness+2.5*support)/2.0;
    vec3 dist = gl_TexCoord[0].xyz;
    vec4 color = gl_Color;

    float d = abs(min(dist[0],min(dist[1],dist[2]))-t);
    //float d = abs(min(dist[0],min(dist[1],dist[2])));

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

    det = P0[0]*P1[1]+P1[0]*P2[1]+P2[0]*P0[1]-P1[1]*P2[0]-P2[1]*P0[0]-P0[1]*P1[0]
    if det < 0:
        P1,P2 = P2,P1
    

    P0 = np.array( P0 )
    P1 = np.array( P1 )
    P2 = np.array( P2 )

    O0 = ortho(P0-P1)
    O1 = ortho(P1-P2)
    O2 = ortho(P2-P0)

    P00,P10 = P0 + O0*w, P1 + O0*w
    P11,P21 = P1 + O1*w, P2 + O1*w
    P02,P22 = P0 + O2*w, P2 + O2*w

    PP0 = intersection( P00,P10, P02,P22)
    PP1 = intersection( P11,P21, P00,P10)
    PP2 = intersection( P02,P22, P11,P21)

    V0 = PP2 - PP1
    V1 = PP2 - PP0
    V2 = PP1 - PP0
    A = abs(np.cross(V1,V2))

    D0 = A/np.sqrt(np.vdot(V0,V0)), 0, 0
    D1 = 0, A/np.sqrt(np.vdot(V1,V1)), 0
    D2 = 0, 0, A/np.sqrt(np.vdot(V2,V2))


    shader.bind()
    shader.uniformf('support', support)
    shader.uniformf('thickness', thickness)
    gl.glColor( 0,0,0, alpha)
    gl.glBegin( gl.GL_TRIANGLES )

    gl.glTexCoord3f( D0[0], D0[1], D0[2] )
    gl.glVertex( PP0[0], PP0[1], 0 )

    gl.glTexCoord3f( D1[0], D1[1], D1[2] )
    gl.glVertex( PP1[0], PP1[1], 0 )

    gl.glTexCoord3f( D2[0], D2[1], D2[2] )
    gl.glVertex( PP2[0], PP2[1], 0 )

    gl.glEnd( )
    shader.unbind()


def on_display( ):
    global shader

    gl.glClearColor(1,1,1,1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glActiveTexture(gl.GL_TEXTURE0)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glEnable(gl.GL_BLEND)
    gl.glColor(0,0,0,1)

    radius = 255.0
    theta, dtheta = 0, 5.5/180.0*math.pi
    thickness = 1.0
    support = .75

    for i in range(500):
        xc,yc = 256, 256+32
        r = 10.1-i*0.02

        x0 = xc + np.cos(theta+dtheta/3)*radius*.925
        y0 = yc + np.sin(theta+dtheta/3)*radius*.925
        x1 = xc + np.cos(theta-dtheta/3)*radius*.925
        y1 = yc + np.sin(theta-dtheta/3)*radius*.925
        x2 = xc + np.cos(theta)*radius*1.00
        y2 = yc + np.sin(theta)*radius*1.00
        triangle( (x0,y0), (x1,y1), (x2,y2), thickness, support )

        radius -= 0.45
        theta += dtheta


    for i in range(0,39):
        thickness = (i+1)/20.0
        xc,yc = 20 + i*12.5, 16
        x0,y0 = xc-5, yc-5
        x1,y1 = xc+5, yc-5
        x2,y2 = xc,   yc+5
        triangle( (x0,y0), (x1,y1), (x2,y2), thickness, support )

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
        fbo.save(on_display, "gl-triangle.png")


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


