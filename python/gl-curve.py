# ----------------------------------------------------------------------------
#  Anti-Grain Geometry (AGG) - Version 2.5
#  A high quality rendering engine for C++
#  Copyright (C) 2002-2006 Maxim Shemanarev
#  Contact: mcseem@antigrain.com
#           mcseemagg@yahoo.com
#           http://antigrain.com
#  
#  AGG is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#  
#  AGG is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with AGG; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, 
#  MA 02110-1301, USA.
# ----------------------------------------------------------------------------
#
# OpenGL/Python translation by Nicolas P. Rougier
#
# ----------------------------------------------------------------------------
import math
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
from shader import Shader
import fbo

curve_distance_epsilon        = 1e-30
curve_collinearity_epsilon    = 1e-30
curve_angle_tolerance_epsilon = 0.01
curve_recursion_limit         = 32
m_cusp_limit                  = 0.0
m_angle_tolerance             = 15*math.pi/180.0
m_approximation_scale         = 1.0
m_distance_tolerance_square   = (0.5 / m_approximation_scale)**2


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

def calc_sq_distance( x1,y1, x2,y2 ):
    """
    """
    dx = x2-x1
    dy = y2-y1
    return dx * dx + dy * dy


def curve3_recursive_bezier( points, x1, y1, x2, y2, x3, y3, level = 0 ):
    """
    """
    if level > curve_recursion_limit:
        return

    # Calculate all the mid-points of the line segments
    # -------------------------------------------------
    x12  = (x1 + x2) / 2.
    y12  = (y1 + y2) / 2.
    x23  = (x2 + x3) / 2.
    y23  = (y2 + y3) / 2.
    x123 = (x12 + x23) / 2.
    y123 = (y12 + y23) / 2.

    dx = x3 - x1
    dy = y3 - y1
    d = math.fabs((x2-x3)*dy - (y2-y3)*dx)

    if d > curve_collinearity_epsilon:
        # Regular case
        # ------------
        if d*d <= m_distance_tolerance_square * (dx*dx + dy*dy):
            # If the curvature doesn't exceed the distance_tolerance value
            # we tend to finish subdivisions.
            if m_angle_tolerance < curve_angle_tolerance_epsilon:
                points.append( (x123,y123) )
                return

            # Angle & Cusp Condition
            da = math.fabs(math.atan2(y3 - y2, x3 - x2) - math.atan2(y2 - y1, x2 - x1))
            if da >= math.pi:
                da = 2*math.pi - da

            if da < m_angle_tolerance:
                # Finally we can stop the recursion
                points.append( (x123,y123) )
                return
    else:
        # Collinear case
        # --------------
        da = dx*dx + dy*dy
        if da == 0:
            d = calc_sq_distance(x1, y1, x2, y2)
        else:
            d = ((x2 - x1)*dx + (y2 - y1)*dy) / da
            if d > 0 and d < 1:
                # Simple collinear case, 1---2---3, we can leave just two endpoints
                return
            if(d <= 0):
                d = calc_sq_distance(x2, y2, x1, y1)
            elif d >= 1:
                d = calc_sq_distance(x2, y2, x3, y3)
            else:
               d = calc_sq_distance(x2, y2, x1 + d*dx, y1 + d*dy)

        if d < m_distance_tolerance_square:
            points.append( (x2,y2) )
            return

    # Continue subdivision
    # --------------------
    curve3_recursive_bezier( points, x1, y1, x12, y12, x123, y123, level + 1 )
    curve3_recursive_bezier( points, x123, y123, x23, y23, x3, y3, level + 1 )



def curve4_recursive_bezier( points, x1, y1, x2, y2, x3, y3, x4, y4, level=0):
    """
    """

    if level > curve_recursion_limit: 
        return

    # Calculate all the mid-points of the line segments
    # -------------------------------------------------
    x12   = (x1 + x2) / 2.
    y12   = (y1 + y2) / 2.
    x23   = (x2 + x3) / 2.
    y23   = (y2 + y3) / 2.
    x34   = (x3 + x4) / 2.
    y34   = (y3 + y4) / 2.
    x123  = (x12 + x23) / 2.
    y123  = (y12 + y23) / 2.
    x234  = (x23 + x34) / 2.
    y234  = (y23 + y34) / 2.
    x1234 = (x123 + x234) / 2.
    y1234 = (y123 + y234) / 2.


    # Try to approximate the full cubic curve by a single straight line
    # -----------------------------------------------------------------
    dx = x4 - x1
    dy = y4 - y1
    d2 = math.fabs(((x2 - x4) * dy - (y2 - y4) * dx))
    d3 = math.fabs(((x3 - x4) * dy - (y3 - y4) * dx))

    s =  int((d2 > curve_collinearity_epsilon) << 1) + int(d3 > curve_collinearity_epsilon)

    if s == 0:
        # All collinear OR p1==p4
        # ----------------------
        k = dx*dx + dy*dy
        if k == 0:
            d2 = calc_sq_distance(x1, y1, x2, y2)
            d3 = calc_sq_distance(x4, y4, x3, y3)

        else:
            k   = 1. / k
            da1 = x2 - x1
            da2 = y2 - y1
            d2  = k * (da1*dx + da2*dy)
            da1 = x3 - x1
            da2 = y3 - y1
            d3  = k * (da1*dx + da2*dy)
            if d2 > 0 and d2 < 1 and d3 > 0 and d3 < 1:
                # Simple collinear case, 1---2---3---4
                # We can leave just two endpoints
                return
             
            if d2 <= 0:
                d2 = calc_sq_distance(x2, y2, x1, y1)
            elif d2 >= 1:
                d2 = calc_sq_distance(x2, y2, x4, y4)
            else:
                d2 = calc_sq_distance(x2, y2, x1 + d2*dx, y1 + d2*dy)

            if d3 <= 0:
                d3 = calc_sq_distance(x3, y3, x1, y1)
            elif d3 >= 1:
                d3 = calc_sq_distance(x3, y3, x4, y4)
            else:
                d3 = calc_sq_distance(x3, y3, x1 + d3*dx, y1 + d3*dy)

        if d2 > d3:
            if d2 < m_distance_tolerance_square:
                points.append( (x2, y2) )
                return
        else:
            if d3 < m_distance_tolerance_square:
                points.append( (x3, y3) )
                return

    elif s == 1:
        # p1,p2,p4 are collinear, p3 is significant
        # -----------------------------------------
        if d3 * d3 <= m_distance_tolerance_square * (dx*dx + dy*dy):
            if m_angle_tolerance < curve_angle_tolerance_epsilon:
                points.append((x23, y23) )
                return
            
            # Angle Condition
            # ---------------
            da1 = math.fabs(math.atan2(y4 - y3, x4 - x3) - math.atan2(y3 - y2, x3 - x2))
            if da1 >= math.pi:
                da1 = 2*math.pi - da1
            
            if da1 < m_angle_tolerance:
                points.extend( [(x2, y2),(x3, y3)] )
                return

            if m_cusp_limit != 0.0:
                if da1 > m_cusp_limit:
                    points.append( (x3, y3) )
                    return

    elif s == 2:
        # p1,p3,p4 are collinear, p2 is significant
        # -----------------------------------------
        if d2 * d2 <= m_distance_tolerance_square * (dx*dx + dy*dy):
            if m_angle_tolerance < curve_angle_tolerance_epsilon:
                points.append( (x23, y23) )
                return
            
            # Angle Condition
            # ---------------
            da1 = math.fabs(math.atan2(y3 - y2, x3 - x2) - math.atan2(y2 - y1, x2 - x1))
            if da1 >= math.pi:
                da1 = 2*math.pi - da1
            
            if da1 < m_angle_tolerance:
                points.extend( [(x2, y2),(x3, y3)] )
                return
            
            if m_cusp_limit != 0.0:
                if da1 > m_cusp_limit:
                    points.append( (x2, y2) )
                    return
        
    elif s == 3:
        # Regular case
        # ------------
        if (d2 + d3)*(d2 + d3) <= m_distance_tolerance_square * (dx*dx + dy*dy):
            # If the curvature doesn't exceed the distance_tolerance value
            # we tend to finish subdivisions.

            if m_angle_tolerance < curve_angle_tolerance_epsilon:
                points.append( (x23, y23) )
                return
            
            # Angle & Cusp Condition
            # ----------------------
            k   = math.atan2(y3 - y2, x3 - x2)
            da1 = math.fabs(k - math.atan2(y2 - y1, x2 - x1))
            da2 = math.fabs(math.atan2(y4 - y3, x4 - x3) - k)
            if da1 >= math.pi:
                da1 = 2*math.pi - da1
            if da2 >= math.pi:
                da2 = 2*math.pi - da2

            if da1 + da2 < m_angle_tolerance:
                # Finally we can stop the recursion
                # ---------------------------------
                points.append( (x23, y23) )
                return
            
            if m_cusp_limit != 0.0:
                if da1 > m_cusp_limit:
                    points.append( (x2, y2) )
                    return
                
                if da2 > m_cusp_limit:
                    points.append( (x3, y3) )
                    return
    
    # Continue subdivision
    # --------------------
    curve4_recursive_bezier( points, x1, y1, x12, y12, x123, y123, x1234, y1234, level + 1 )
    curve4_recursive_bezier( points, x1234, y1234, x234, y234, x34, y34, x4, y4, level + 1 )


def curve3_bezier( P1, P2, P3 ):
    """
    """

    x1,y1 = float(P1[0]), float(P1[1])
    x2,y2 = float(P2[0]), float(P2[1])
    x3,y3 = float(P3[0]), float(P3[1])
    points = []
    curve3_recursive_bezier( points, x1,y1, x2,y2, x3,y3 )
    points.insert( 0, (x1,y1) )
    points.append( (x3,y3) )
    return points


def curve4_bezier( P1, P2, P3, P4 ):
    """
    """

    x1,y1 = float(P1[0]), float(P1[1])
    x2,y2 = float(P2[0]), float(P2[1])
    x3,y3 = float(P3[0]), float(P3[1])
    x4,y4 = float(P4[0]), float(P4[1])
    points = []
    curve4_recursive_bezier( points, x1,y1, x2,y2, x3,y3, x4,y4 )
    points.insert( 0, (x1,y1) )
    points.append( (x4,y4) )
    return points


def curve_thicken( points, thickness=1.0, support=0.75 ):
    """
    """

    alpha = min(thickness, 1.0)
    thickness = max(thickness, 1.0)
    w = math.ceil(2.5*support+thickness)

    # Points
    P = np.array( points ).reshape(len(points),2)

    # Tangent vectors 
    T = np.zeros_like(P)
    T[:-1] = P[1:] - P[:-1]
    T[-1] = T[-2] # repeating last tangent for last point

    # Normalization and scaling
    L = np.sqrt(T[:,0]**2 + T[:,1]**2)
    T *= (w/2) / L.reshape(len(P),1)

    # Total length of curve
    L = np.cumsum(L)
    # Last cumulative sum is wrong because of the repeat of the last point
    L[1:] = L[:-1]
    L[0] = 0
    length = L[-1]

    X,Y = P[:,0], P[:,1]
    dX, dY = T[:,0], T[:,1]
    n = (len(P))*2 + 4
    V = np.zeros( n, [ ('vertex', [('x','f4'), ('y','f4'), ('z','f4')]),
                       ('texture',[('x','f4'), ('y','f4'), ('z','f4')]),
                       ('color',  [('r','f4'), ('g','f4'), ('b','f4'), ('a','f4')]) ] )

    V['color'] = 0,0,0,alpha

    # Main body
    V['vertex']['x'][2:-3:2] = X-dY
    V['vertex']['y'][2:-3:2] = Y+dX
    V['texture']['x'][2:-3:2] = L
    V['texture']['y'][2:-3:2] = -w/2

    V['vertex']['x'][3:-2:2] = X+dY
    V['vertex']['y'][3:-2:2] = Y-dX
    V['texture']['x'][3:-2:2] = L
    V['texture']['y'][3:-2:2] = +w/2

    # Cap at start
    V['vertex']['x'][0] = X[0]-dX[0]-dY[0]
    V['vertex']['y'][0] = Y[0]-dY[0]+dX[0]
    V['texture']['x'][0] = -w/2
    V['texture']['y'][0] = -w/2

    V['vertex']['x'][1] = X[0]-dX[0]+dY[0]
    V['vertex']['y'][1] = Y[0]-dY[0]-dX[0]
    V['texture']['x'][1] = -w/2
    V['texture']['y'][1] = +w/2

    # Cap at end
    V['vertex']['x'][-2] = X[-1]+dX[-1]-dY[-1]
    V['vertex']['y'][-2] = Y[-1]+dY[-1]+dX[-1]
    V['texture']['x'][-2] = length+w/2
    V['texture']['y'][-2] = -w/2

    V['vertex']['x'][-1] = X[-1]+dX[-1]+dY[-1]
    V['vertex']['y'][-1] = Y[-1]+dY[-1]-dX[-1]
    V['texture']['x'][-1] = length+w/2
    V['texture']['y'][-1] = +w/2


    shader.bind()
    shader.uniformf('support', support)
    shader.uniformf('length', length)
    shader.uniformf('thickness', thickness)
    gl.glColor(0,0,0,alpha)

    gl.glBegin(gl.GL_TRIANGLES)
    for i in range(0,len(V)-3,2):
        gl.glTexCoord2f( V['texture']['x'][i+0], V['texture']['y'][i+0] )
        gl.glVertex( V['vertex'][i+0] )
        gl.glTexCoord2f( V['texture']['x'][i+1], V['texture']['y'][i+1] )
        gl.glVertex( V['vertex'][i+1] )
        gl.glTexCoord2f( V['texture']['x'][i+2], V['texture']['y'][i+2] )
        gl.glVertex( V['vertex'][i+2] )

        gl.glTexCoord2f( V['texture']['x'][i+1], V['texture']['y'][i+1] )
        gl.glVertex( V['vertex'][i+1] )
        gl.glTexCoord2f( V['texture']['x'][i+2], V['texture']['y'][i+2] )
        gl.glVertex( V['vertex'][i+2] )
        gl.glTexCoord2f( V['texture']['x'][i+3], V['texture']['y'][i+3] )
        gl.glVertex( V['vertex'][i+3] )
    gl.glEnd()
    shader.unbind()


def on_display( ):
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
        thickness = 1.0
        x0 = xc + np.cos(theta)*radius*0.925
        y0 = yc + np.sin(theta)*radius*0.925
        x1 = xc + np.cos(theta+dtheta/2)*radius*0.950
        y1 = yc + np.sin(theta+dtheta/2)*radius*0.950
        x2 = xc + np.cos(theta-dtheta/2)*radius*0.975
        y2 = yc + np.sin(theta-dtheta/2)*radius*0.975
        x3 = xc + np.cos(theta)*radius*1.000
        y3 = yc + np.sin(theta)*radius*1.000

        P = curve4_bezier( (x0,y0), (x1,y1), (x2,y2), (x3,y3) )
        curve_thicken(P, thickness, support)
        radius -= 0.45
        theta += dtheta

    for i in range(0,49):
        thickness = (i+1)/10.0
        x0 = 20+i*10
        y0 = 10
        x1 = 15+i*10
        y1 = 14
        x2 = 25+i*10
        y2 = 18
        x3 = 20+i*10
        y3 = 22
        P = curve4_bezier( (x0,y0), (x1,y1), (x2,y2), (x3,y3) )
        curve_thicken(P, thickness, support)
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
        fbo.save(on_display, "gl-curve.png")

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


