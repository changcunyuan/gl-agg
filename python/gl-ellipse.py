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
uniform float radius_x;
uniform float radius_y;
uniform float thickness;
uniform float support;
void main()
{
    float t = thickness/2.0-support;

    vec4 color = gl_Color;
    vec2 uv = gl_TexCoord[0].xy;
    float x = uv.x;
    float y = uv.y;

    float a = radius_x+thickness/2.;
    float b = radius_y+thickness/2.;
    float d1 = sqrt(x*x/(a*a) + y*y/(b*b));
    float width1 = fwidth(d1)*support/1.25;
    float alpha1  = smoothstep(1.0 - width1, 1.0 + width1, d1);

    a = radius_x - thickness/2.;
    b = radius_y - thickness/2.;
    float d2 = sqrt(x*x/(a*a) + y*y/(b*b));
    float width2 = fwidth(d2)*support/1.25;
    float alpha2  = smoothstep(1.0 + width2, 1.0 - width2, d2);

    float alpha = (1.0-max(alpha1,alpha2));
    gl_FragColor = vec4(color.rgb, alpha*color.a);
}
'''


def ellipse( (x,y,rx,ry), angle, thickness=1.0, support=0.75):
    alpha = min(thickness, 1.0)
    thickness = max(thickness, 1.0)
    dx = math.ceil(rx + thickness/2.0 + 2.5*support)
    dy = math.ceil(ry + thickness/2.0 + 2.5*support)
    body = ( (0-dx, 0-dy, 0),
             (0+dx, 0-dy, 0),
             (0+dx, 0+dy, 0),
             (0-dx, 0+dy, 0) )

    shader.bind()
    shader.uniformf('radius_x', rx)
    shader.uniformf('radius_y', ry)
    shader.uniformf('support', support);
    shader.uniformf('thickness', thickness)

    gl.glColor(0,0,0, alpha)
    gl.glPushMatrix()
    gl.glTranslate(x,y,0)
    gl.glRotatef(angle,0,0,1)

    gl.glBegin(gl.GL_TRIANGLES)
    gl.glTexCoord2f(-dx, -dy), gl.glVertex(body[0] )
    gl.glTexCoord2f(+dx, -dy), gl.glVertex(body[1] )
    gl.glTexCoord2f(+dx, +dy), gl.glVertex(body[2] )

    gl.glTexCoord2f(-dx, -dy), gl.glVertex(body[0] )
    gl.glTexCoord2f(+dx, +dy), gl.glVertex(body[2] )
    gl.glTexCoord2f(-dx, +dy), gl.glVertex(body[3] )
    gl.glEnd()
    gl.glPopMatrix()

    shader.unbind()


def on_display( ):
    gl.glClearColor(1,1,1,1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glEnable(gl.GL_BLEND)

    thickness = 1.0
    support = 0.75

    radius = 255.0
    theta, dtheta = 0, 5.5/180.0*math.pi
    for i in range(500):
        x = 256+radius*math.cos(theta)
        y = 32+256+radius*math.sin(theta)
        rx = 10.1-i*0.02
        ry = 1.5*rx
        ellipse( (x,y,rx,ry), 90+180*theta/math.pi, thickness, support)

        theta += dtheta
        radius -= 0.45

    for i in range(0,39):
        thickness = (i+1)/10.0
        rx, ry = 4, 8
        x = 20 - rx +i*12.5
        y = 16 
        ellipse( (x,y,rx,ry), 0.0, thickness, support)

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
        fbo.save(on_display, "gl-ellipse.png")

    

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

