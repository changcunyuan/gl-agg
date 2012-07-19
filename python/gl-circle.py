#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
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
uniform float radius;
uniform float support;
uniform float thickness;
void main()
{
    float t = thickness/2.0-support;
    vec4 color = gl_Color;
    vec2 uv = gl_TexCoord[0].xy;
    float dx = uv.x;
    float dy = uv.y;
    float d = abs(sqrt(dx*dx+dy*dy) - radius) - t;

    if( d < 0.0 )
    {
        gl_FragColor = color;
    }
    else
    {
        float alpha = d/support;
        alpha = exp(-alpha*alpha);
        gl_FragColor = vec4(color.rgb, alpha*color.a);
    }
}
'''



def circle( (x,y,radius), thickness=1.0, support=0.75):

    alpha = min(thickness, 1.0)
    thickness = max(thickness, 1.0)
    w = math.ceil(2.5*support+2*radius+thickness)
    dx = w/2
    dy = w/2
    body = ( (x-dx, y-dy, 0),
             (x+dx, y-dy, 0),
             (x+dx, y+dy, 0),
             (x-dx, y+dy, 0) )
    
    shader.bind()
    shader.uniformf('radius', radius)
    shader.uniformf('support', support)
    shader.uniformf('thickness', thickness)

    gl.glColor(0,0,0, alpha)
    gl.glBegin(gl.GL_TRIANGLES)

    gl.glTexCoord2f(-w/2, -w/2), gl.glVertex(body[0] )
    gl.glTexCoord2f(-w/2, +w/2), gl.glVertex(body[1] )
    gl.glTexCoord2f(+w/2, +w/2), gl.glVertex(body[2] )

    gl.glTexCoord2f(-w/2, -w/2), gl.glVertex(body[0] )
    gl.glTexCoord2f(+w/2, +w/2), gl.glVertex(body[2] )
    gl.glTexCoord2f(+w/2, -w/2), gl.glVertex(body[3] )
    gl.glEnd()

    shader.unbind()        



def on_display( ):
    global shader

    gl.glClearColor(1,1,1,1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glActiveTexture(gl.GL_TEXTURE0)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glEnable(gl.GL_BLEND)

    gl.glColor(0,0,0,1)
    shader.bind()


    radius = 255.0
    theta, dtheta = 0, 5.5/180.0*math.pi
    support = 0.75
    thickness = 1.0
    for i in range(500):
        x =    256+radius*math.cos(theta);
        y = 32+256+radius*math.sin(theta);
        r = 10.1-i*0.02
        circle( (x,y,r), thickness=thickness, support=support )
        radius -= 0.45
        theta += dtheta

    for i in range(0,39):
        r = 4
        thickness = (i+1)/10.0
        x = 20+i*12.5 - r
        y = 16
        circle( (x,y,r), thickness=thickness, support=support )
 
    glut.glutSwapBuffers( )

    
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
        fbo.save(on_display, "gl-circle.png")


if __name__ == '__main__':
    import sys
    glut.glutInit( sys.argv )
    glut.glutInitDisplayMode( glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH )
    glut.glutCreateWindow( "Antiliased line using OpenGL shaders" )
    glut.glutReshapeWindow( 512, 512+32 )
    glut.glutDisplayFunc( on_display )
    glut.glutReshapeFunc( on_reshape )
    glut.glutKeyboardFunc( on_keyboard )

    shader = Shader(vert,frag)
    glut.glutMainLoop( )
