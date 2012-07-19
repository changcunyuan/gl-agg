#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import ctypes
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import matplotlib.image as mpimg

from shader import Shader
import fbo


vert = '''
void main()
{
    gl_FrontColor = gl_Color;    
    gl_TexCoord[0].xy = gl_MultiTexCoord0.xy;
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
'''

frag = '''
uniform float length;
uniform float support;
uniform float thickness;
void main()
{
    float t = thickness/2.0-support;

    vec4 color = gl_Color;
    vec2 uv = gl_TexCoord[0].xy;
    float d; 
    float dx = uv.x;
    float dy = abs(uv.y); // - t;

    // cap at origin
    if( dx < 0.0 )
    {
        dx = abs(dx);

        // Round cap   
        d = sqrt(dx*dx+dy*dy);

        // Triangular cap   
        // d = (dx+dy);

        // Square cap
        // d = max(dx,dy);
    }
    // cap at end
    else if ( dx > length )
    {
        dx -= length;

        // Round cap   
        d = sqrt(dx*dx+dy*dy); 

        // Triangular cap   
        // d = (dx+dy);

        // Square cap
        // d = max(dx,dy);
    }
    // line body
    else
    {
        d = dy;
    }

    d = d - t;
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


def line((x0,y0), (x1,y1), thickness=1.0, support=0.75):

    alpha = min(thickness, 1.0)
    thickness = max(thickness, 1.0)
    w = math.ceil(2.5*support+thickness)
    length = math.sqrt((x1-x0)**2+(y1-y0)**2)

    dx = (x1-x0)/length * w/2
    dy = (y1-y0)/length * w/2
    body = ( (x0+dy-dx, y0-dx-dy, 0),
             (x0-dy-dx, y0+dx-dy, 0),
             (x1-dy+dx, y1+dx+dy, 0),
             (x1+dy+dx, y1-dx+dy, 0) )

    shader.bind()
    shader.uniformf('support', support)
    shader.uniformf('length', length)
    shader.uniformf('thickness', thickness)

    gl.glColor(0,0,0, alpha)
    gl.glBegin(gl.GL_TRIANGLES)
    gl.glTexCoord2f(0-w/2, -w/2), gl.glVertex(body[0] )
    gl.glTexCoord2f(0-w/2, +w/2), gl.glVertex(body[1] )
    gl.glTexCoord2f(length+w/2, +w/2), gl.glVertex(body[2] )
    
    gl.glTexCoord2f(0-w/2, -w/2), gl.glVertex(body[0] )
    gl.glTexCoord2f(length+w/2, +w/2), gl.glVertex(body[2] )
    gl.glTexCoord2f(length+w/2, -w/2), gl.glVertex(body[3] )
    gl.glEnd()
    shader.unbind()



def on_display( ):
    global shader

    gl.glClearColor(1,1,1,1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glEnable(gl.GL_BLEND)

    radius = 255.0
    theta, dtheta = 0, 5.5/180.0*math.pi
    thickness = 1.0
    support = .75
    for i in range(500):
        xc, yc = 256, 256+32
        r = 10.1-i*0.02
        thickness = 1.0 #0.1 + (1.0-i/500.0)*4

        x0 = xc + np.cos(theta)*radius*.925
        y0 = yc + np.sin(theta)*radius*.925
        x1 = xc + np.cos(theta)*radius*1.00
        y1 = yc + np.sin(theta)*radius*1.00
        line( (x0,y0), (x1,y1), thickness, support)

        radius -= 0.45
        theta += dtheta

    for i in range(0,49):
        thickness = (i+1)/10.0
        x = 20+i*10 + .315
        y = 16+.315
        line( (x,y+6), (x,y-6), thickness, support )


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
        fbo.save(on_display, "gl-line.png")



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


