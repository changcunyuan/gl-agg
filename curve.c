// ----------------------------------------------------------------------------
// Anti-Grain Geometry (AGG) - Version 2.5
// A high quality rendering engine for C++
// Copyright (C) 2002-2006 Maxim Shemanarev
// Contact: mcseem@antigrain.com
//          mcseemagg@yahoo.com
//          http://antigrain.com
// ----------------------------------------------------------------------------
// OpenGL Anti-Grain Geometry (GL-AGG) - Version 0.1
// A high quality OpenGL rendering engine for C
// Copyright (C) 2012 Nicolas P. Rougier. All rights reserved.
// Contact: Nicolas.Rougier@gmail.com
//          http://code.google.com/p/gl-agg/
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
//  1. Redistributions of source code must retain the above copyright notice,
//     this list of conditions and the following disclaimer.
//
//  2. Redistributions in binary form must reproduce the above copyright
//     notice, this list of conditions and the following disclaimer in the
//     documentation and/or other materials provided with the distribution.
//
// THIS SOFTWARE IS PROVIDED BY NICOLAS P. ROUGIER ''AS IS'' AND ANY EXPRESS OR
// IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
// MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
// EVENT SHALL NICOLAS P. ROUGIER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
// INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
// LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
// ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
// THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
// The views and conclusions contained in the software and documentation are
// those of the authors and should not be interpreted as representing official
// policies, either expressed or implied, of Nicolas P. Rougier.
// ----------------------------------------------------------------------------
#include <assert.h>
#include <string.h>
#include <stdlib.h>
#include "curve.h"


const double curve_distance_epsilon                  = 1e-30;
const double curve_collinearity_epsilon              = 1e-30;
const double curve_angle_tolerance_epsilon           = 0.01;
enum curve_recursion_limit_e { curve_recursion_limit = 32 };

double m_distance_tolerance_square;
double m_cusp_limit = 0.0;
double m_angle_tolerance = 15*M_PI/180.0;
double m_approximation_scale = 1.0;
double pi = M_PI;


// ------------------------------------------------------- calc_sq_distance ---
double
calc_sq_distance( double x1, double y1,
                  double x2, double y2 )
{
    double dx = x2-x1;
    double dy = y2-y1;
    return dx * dx + dy * dy;
}


// -------------------------------------------------------- curve_add_point ---
void
curve_add_point( vector_t * points, double x, double y )
{
    vec2 p = {{x,y}};
    vector_push_back( points, &p );
}


// ------------------------------------------------ curve3_recursive_bezier ---
void
curve3_recursive_bezier( vector_t * points,
                         double x1, double y1, 
                         double x2, double y2, 
                         double x3, double y3,
                         unsigned level )
{
    if(level > curve_recursion_limit) 
    {
        return;
    }

    // Calculate all the mid-points of the line segments
    //----------------------
    double x12   = (x1 + x2) / 2;                
    double y12   = (y1 + y2) / 2;
    double x23   = (x2 + x3) / 2;
    double y23   = (y2 + y3) / 2;
    double x123  = (x12 + x23) / 2;
    double y123  = (y12 + y23) / 2;

    double dx = x3-x1;
    double dy = y3-y1;
    double d = fabs(((x2 - x3) * dy - (y2 - y3) * dx));
    double da;

    if(d > curve_collinearity_epsilon)
    { 
        // Regular case
        //-----------------
        if(d * d <= m_distance_tolerance_square * (dx*dx + dy*dy))
        {
            // If the curvature doesn't exceed the distance_tolerance value
            // we tend to finish subdivisions.
            //----------------------
            if(m_angle_tolerance < curve_angle_tolerance_epsilon)
            {
                curve_add_point( points, x123, y123 );
                return;
            }

            // Angle & Cusp Condition
            //----------------------
            da = fabs(atan2(y3 - y2, x3 - x2) - atan2(y2 - y1, x2 - x1));
            if(da >= pi) da = 2*pi - da;

            if(da < m_angle_tolerance)
            {
                // Finally we can stop the recursion
                //----------------------
                curve_add_point( points, x123, y123 );
                return;                 
            }
        }
    }
    else
    {
        // Collinear case
        //------------------
        da = dx*dx + dy*dy;
        if(da == 0)
        {
            d = calc_sq_distance(x1, y1, x2, y2);
        }
        else
        {
            d = ((x2 - x1)*dx + (y2 - y1)*dy) / da;
            if(d > 0 && d < 1)
            {
                // Simple collinear case, 1---2---3
                // We can leave just two endpoints
                return;
            }
                 if(d <= 0) d = calc_sq_distance(x2, y2, x1, y1);
            else if(d >= 1) d = calc_sq_distance(x2, y2, x3, y3);
            else            d = calc_sq_distance(x2, y2, x1 + d*dx, y1 + d*dy);
        }
        if(d < m_distance_tolerance_square)
        {
            curve_add_point( points, x2, y2 );
            return;
        }
    }

    // Continue subdivision
    //----------------------
    curve3_recursive_bezier( points, x1, y1, x12, y12, x123, y123, level + 1 ); 
    curve3_recursive_bezier( points, x123, y123, x23, y23, x3, y3, level + 1 ); 
}


//------------------------------------------------------------------------
void curve4_recursive_bezier( vector_t *points,
                              double x1, double y1, 
                              double x2, double y2, 
                              double x3, double y3, 
                              double x4, double y4,
                              unsigned level)
{
    if(level > curve_recursion_limit) 
    {
        return;
    }

    // Calculate all the mid-points of the line segments
    //----------------------
    double x12   = (x1 + x2) / 2;
    double y12   = (y1 + y2) / 2;
    double x23   = (x2 + x3) / 2;
    double y23   = (y2 + y3) / 2;
    double x34   = (x3 + x4) / 2;
    double y34   = (y3 + y4) / 2;
    double x123  = (x12 + x23) / 2;
    double y123  = (y12 + y23) / 2;
    double x234  = (x23 + x34) / 2;
    double y234  = (y23 + y34) / 2;
    double x1234 = (x123 + x234) / 2;
    double y1234 = (y123 + y234) / 2;


    // Try to approximate the full cubic curve by a single straight line
    //------------------
    double dx = x4-x1;
    double dy = y4-y1;

    double d2 = fabs(((x2 - x4) * dy - (y2 - y4) * dx));
    double d3 = fabs(((x3 - x4) * dy - (y3 - y4) * dx));
    double da1, da2, k;

    switch(((int)(d2 > curve_collinearity_epsilon) << 1) +
           (int)(d3 > curve_collinearity_epsilon))
    {
    case 0:
        // All collinear OR p1==p4
        //----------------------
        k = dx*dx + dy*dy;
        if(k == 0)
        {
            d2 = calc_sq_distance(x1, y1, x2, y2);
            d3 = calc_sq_distance(x4, y4, x3, y3);
        }
        else
        {
            k   = 1 / k;
            da1 = x2 - x1;
            da2 = y2 - y1;
            d2  = k * (da1*dx + da2*dy);
            da1 = x3 - x1;
            da2 = y3 - y1;
            d3  = k * (da1*dx + da2*dy);
            if(d2 > 0 && d2 < 1 && d3 > 0 && d3 < 1)
            {
                // Simple collinear case, 1---2---3---4
                // We can leave just two endpoints
                return;
            }
                 if(d2 <= 0) d2 = calc_sq_distance(x2, y2, x1, y1);
            else if(d2 >= 1) d2 = calc_sq_distance(x2, y2, x4, y4);
            else             d2 = calc_sq_distance(x2, y2, x1 + d2*dx, y1 + d2*dy);

                 if(d3 <= 0) d3 = calc_sq_distance(x3, y3, x1, y1);
            else if(d3 >= 1) d3 = calc_sq_distance(x3, y3, x4, y4);
            else             d3 = calc_sq_distance(x3, y3, x1 + d3*dx, y1 + d3*dy);
        }
        if(d2 > d3)
        {
            if(d2 < m_distance_tolerance_square)
            {
                curve_add_point( points, x2, y2);
                return;
            }
        }
        else
        {
            if(d3 < m_distance_tolerance_square)
            {
                curve_add_point( points, x3, y3);
                return;
            }
        }
        break;

    case 1:
        // p1,p2,p4 are collinear, p3 is significant
        //----------------------
        if(d3 * d3 <= m_distance_tolerance_square * (dx*dx + dy*dy))
        {
            if(m_angle_tolerance < curve_angle_tolerance_epsilon)
            {
                curve_add_point( points, x23, y23 );
                return;
            }
            
            // Angle Condition
            //----------------------
            da1 = fabs(atan2(y4 - y3, x4 - x3) - atan2(y3 - y2, x3 - x2));
            if(da1 >= pi) da1 = 2*pi - da1;
            
            if(da1 < m_angle_tolerance)
            {
                curve_add_point( points, x2, y2 );
                curve_add_point( points, x3, y3 );
                return;
            }

            if(m_cusp_limit != 0.0)
            {
                if(da1 > m_cusp_limit)
                {
                    curve_add_point( points, x3, y3 );
                    return;
                }
            }
        }
        break;

    case 2:
        // p1,p3,p4 are collinear, p2 is significant
        //----------------------
        if(d2 * d2 <= m_distance_tolerance_square * (dx*dx + dy*dy))
        {
            if(m_angle_tolerance < curve_angle_tolerance_epsilon)
            {
                curve_add_point( points, x23, y23 );
                return;
            }
            
            // Angle Condition
            //----------------------
            da1 = fabs(atan2(y3 - y2, x3 - x2) - atan2(y2 - y1, x2 - x1));
            if(da1 >= pi) da1 = 2*pi - da1;
            
            if(da1 < m_angle_tolerance)
            {
                curve_add_point( points, x2, y2 );
                curve_add_point( points, x3, y3 );
                return;
            }
            
            if(m_cusp_limit != 0.0)
            {
                if(da1 > m_cusp_limit)
                {
                    curve_add_point( points, x2, y2 );
                    return;
                }
            }
        }
        break;
        
    case 3: 
        // Regular case
        //-----------------
        if((d2 + d3)*(d2 + d3) <= m_distance_tolerance_square * (dx*dx + dy*dy))
        {
            // If the curvature doesn't exceed the distance_tolerance value
            // we tend to finish subdivisions.
            //----------------------
            if(m_angle_tolerance < curve_angle_tolerance_epsilon)
            {
                curve_add_point( points, x23, y23 );
                return;
            }
            
            // Angle & Cusp Condition
            //----------------------
            k   = atan2(y3 - y2, x3 - x2);
            da1 = fabs(k - atan2(y2 - y1, x2 - x1));
            da2 = fabs(atan2(y4 - y3, x4 - x3) - k);
            if(da1 >= pi) da1 = 2*pi - da1;
            if(da2 >= pi) da2 = 2*pi - da2;

            if(da1 + da2 < m_angle_tolerance)
            {
                // Finally we can stop the recursion
                //----------------------
                curve_add_point( points, x23, y23 );
                return;
            }
            
            if(m_cusp_limit != 0.0)
            {
                if(da1 > m_cusp_limit)
                {
                    curve_add_point( points, x2, y2 );
                    return;
                }
                
                if(da2 > m_cusp_limit)
                {
                    curve_add_point( points, x3, y3 );
                    return;
                }
            }
        }
        break;
    }
    
    // Continue subdivision
    //----------------------
    curve4_recursive_bezier( points,
                             x1, y1, x12, y12, x123, y123, x1234, y1234, level + 1 ); 
    curve4_recursive_bezier( points,
                             x1234, y1234, x234, y234, x34, y34, x4, y4, level + 1 ); 
}


// ---------------------------------------------------------- curve3_bezier ---
vector_t *
curve3_bezier( double x1, double y1, 
               double x2, double y2, 
               double x3, double y3 )
{
    m_distance_tolerance_square = 0.5 / m_approximation_scale;
    m_distance_tolerance_square *= m_distance_tolerance_square;

    vector_t * points = vector_new( sizeof(vec2) );
    curve_add_point( points, x1, y1);
    curve3_recursive_bezier( points, x1, y1, x2, y2, x3, y3, 0 );
    curve_add_point( points, x3, y3);

    return points;
}


// ---------------------------------------------------------- curve4_bezier ---
vector_t *
curve4_bezier( double x1, double y1, 
               double x2, double y2, 
               double x3, double y3,
               double x4, double y4 )
{
    m_distance_tolerance_square = 0.5 / m_approximation_scale;
    m_distance_tolerance_square *= m_distance_tolerance_square;

    vector_t * points = vector_new( sizeof(vec2) );
    curve_add_point( points, x1, y1);
    curve4_recursive_bezier(points, x1, y1, x2, y2, x3, y3, x4, y4, 0);
    curve_add_point( points, x4, y4);

    return points;
}



// ----------------------------------------------- vertex_buffer_add_curve3 ---
void
vertex_buffer_add_curve3( vertex_buffer_t * self,
                          double x1, double y1, 
                          double x2, double y2, 
                          double x3, double y3,
                          vec4 color, double thickness )
{
    assert( self );
    assert( strcmp( vertex_buffer_format( self ), "v3f:c4f:t3f" ) == 0 );

}


// -------------------------------------------------- vertex_buffer_add_curve4 ---
void
vertex_buffer_add_curve4( vertex_buffer_t * self,
                          double x1, double y1, 
                          double x2, double y2, 
                          double x3, double y3,
                          double x4, double y4,
                          vec4 color, double thickness )
{
    assert( self );
    assert( strcmp( vertex_buffer_format( self ), "v3f:c4f:t3f" ) == 0 );

    typedef struct {
        vec3 vertex;      
        vec4 color;
        vec3 tex_coord;
    } vertex_t;


    vector_t *points = curve4_bezier( x1, y1, x2, y2, x3, y3, x4, y4 );
    size_t n = vector_size(points);

    int n_vertices = 2*n+2+2;
    vertex_t * vertices = (vertex_t *) calloc( n_vertices, sizeof(vertex_t) );

    int n_indices  = 6*(n+1);
    GLuint * indices = (GLuint *) calloc( n_indices, sizeof(GLuint) );

    float d,w;
    if (thickness < 1.0)
    {
        w = 2.5;
        color.a = thickness*thickness;
        d = (w+2.5)/w;
    }
    else
    {
        d = (thickness+2.0)/thickness;
        w = thickness+2.0;
    }

    vertex_t vertex = { {{0.0, 0.0, 0.0}}, color, {{0.0, 0.0, thickness}} };
    double x_, y_, x, y;

    int i=0, index=0;
    for(i=0; i<n; ++i)
    {
        vec2 *p = (vec2 *)vector_get( points, i );
        x = p->x;
        y = p->y;

        // Extract tangent/ortho vector
        vec2 tangent = {{x-x_, y-y_}};
        double norm = sqrt(tangent.x*tangent.x+tangent.y*tangent.y);
        if( norm > 0 )
        {
            tangent.x /= norm;
            tangent.y /= norm;
        }
        vec2 ortho = {{-tangent.y, tangent.x}};

        if (i==1)
        {
            // Cap
            memcpy(&vertices[index], &vertex, sizeof(vertex_t));
            vertices[index].vertex.x = x_ + (-ortho.x-tangent.x)*w/2;
            vertices[index].vertex.y = y_ + (-ortho.y-tangent.y)*w/2;
            vertices[index].tex_coord.x = -d;
            vertices[index].tex_coord.y = -d;
            index++;

            memcpy(&vertices[index], &vertex, sizeof(vertex_t));
            vertices[index].vertex.x = x_ + (ortho.x-tangent.x)*w/2;
            vertices[index].vertex.y = y_ + (ortho.y-tangent.y)*w/2;
            vertices[index].tex_coord.x = -d;
            vertices[index].tex_coord.y = +d;
            index++;

            memcpy(&vertices[index], &vertex, sizeof(vertex_t));
            vertices[index].vertex.x = x_ - ortho.x*w/2;
            vertices[index].vertex.y = y_ - ortho.y*w/2;
            vertices[index].tex_coord.x = 0;
            vertices[index].tex_coord.y = -d;
            index++;

            memcpy(&vertices[index], &vertex, sizeof(vertex_t));
            vertices[index].vertex.x = x_ + ortho.x*w/2;
            vertices[index].vertex.y = y_ + ortho.y*w/2;
            vertices[index].tex_coord.x = 0;
            vertices[index].tex_coord.y = +d;
            index++;
        }
        if( i > 0 )
        {
            memcpy(&vertices[index], &vertex, sizeof(vertex_t));
            vertices[index].vertex.x = x - ortho.x*w/2;
            vertices[index].vertex.y = y - ortho.y*w/2;
            vertices[index].tex_coord.x = i/(float)n;
            vertices[index].tex_coord.y = -d;
            index++;

            memcpy(&vertices[index], &vertex, sizeof(vertex_t));
            vertices[index].vertex.x = x + ortho.x*w/2;
            vertices[index].vertex.y = y + ortho.y*w/2;
            vertices[index].tex_coord.x = i/(float)n;
            vertices[index].tex_coord.y = +d;
            index++;
        }

        // Cap
        if( i == (n-1) )
        {
            memcpy(&vertices[index], &vertex, sizeof(vertex_t));
            vertices[index].vertex.x = x + (-ortho.x+tangent.x)*w/2;
            vertices[index].vertex.y = y + (-ortho.y+tangent.y)*w/2;
            vertices[index].tex_coord.x = 1+d;
            vertices[index].tex_coord.y = -d;
            index++;

            memcpy(&vertices[index], &vertex, sizeof(vertex_t));
            vertices[index].vertex.x = x + (ortho.x+tangent.x)*w/2;
            vertices[index].vertex.y = y + (ortho.y+tangent.y)*w/2;
            vertices[index].tex_coord.x = 1+d;
            vertices[index].tex_coord.y = +d;
            index++;
        }
        x_ = x;
        y_ = y;
    }
    vector_delete( points );

    for(i=0; i<=n; ++i)
    {
        indices[6*i+0] = 2*i+0;
        indices[6*i+1] = 2*i+1;
        indices[6*i+2] = 2*i+2;
        indices[6*i+3] = 2*i+1;
        indices[6*i+4] = 2*i+2;
        indices[6*i+5] = 2*i+3;
    }
    vertex_buffer_append( self, vertices, n_vertices, indices, n_indices );
    free( indices );
    free( vertices );
}
