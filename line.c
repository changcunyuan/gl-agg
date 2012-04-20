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
#include "lines.h"

// ----------------------------------------------------------------------------
void
vertex_buffer_add_line( vertex_buffer_t * self,
                        double x1, double y1, 
                        double x2, double y2,
                        vec4 color, double thickness )
{
    typedef struct {
        vec3 vertex;      
        vec4 color;
        vec3 tex_coord;
    } vertex_t;

    assert( self );
    assert( strcmp( vertex_buffer_format( self ), "v3f:c4f:t3f" ) == 0 );

    size_t n = 2;
    int n_vertices = 2*n+2+2;
    vertex_t * vertices = (vertex_t *) calloc( n_vertices, sizeof(vertex_t) );
    int n_indices  = 6*(n+1);
    GLuint * indices = (GLuint *) calloc( n_indices, sizeof(GLuint) );

    float d,w;
    if (thickness < 1.0)
    {
        w = 2.0;
        color.a *= thickness; //*thickness;
        d = (w+2)/w;
    }
    else
    {
        d = (thickness+2.0)/thickness;
        w = thickness+2.0;
    }

    x1 = round(x1) + 0.315;
    y1 = round(y1) + 0.315;
    x2 = round(x2) + 0.315;
    y2 = round(y2) + 0.315;
    vertex_t vertex = { {{0.0, 0.0, 0.0}}, color, {{0.0, 0.0, thickness}} };

    // Extract tangent/ortho vector
    vec2 tangent = {{x2-x1, y2-y1}};
    double norm = sqrt(tangent.x*tangent.x+tangent.y*tangent.y);
    if( norm > 0 )
    {
        tangent.x /= norm;
        tangent.y /= norm;
    }
    vec2 ortho = {{-tangent.y, tangent.x}};
    size_t index=0;

    // Start cap
    memcpy(&vertices[index], &vertex, sizeof(vertex_t));
    vertices[index].vertex.x = x1 + (-ortho.x-tangent.x)*w/2;
    vertices[index].vertex.y = y1 + (-ortho.y-tangent.y)*w/2;
    vertices[index].tex_coord.x = -d;
    vertices[index].tex_coord.y = -d;
    index++;
    memcpy(&vertices[index], &vertex, sizeof(vertex_t));
    vertices[index].vertex.x = x1 + (ortho.x-tangent.x)*w/2;
    vertices[index].vertex.y = y1 + (ortho.y-tangent.y)*w/2;
    vertices[index].tex_coord.x = -d;
    vertices[index].tex_coord.y = +d;
    index++;

    // Actual line segment
    memcpy(&vertices[index], &vertex, sizeof(vertex_t));
    vertices[index].vertex.x = x1 - ortho.x*w/2;
    vertices[index].vertex.y = y1 - ortho.y*w/2;
    vertices[index].tex_coord.x = 0;
    vertices[index].tex_coord.y = -d;
    index++;
    memcpy(&vertices[index], &vertex, sizeof(vertex_t));
    vertices[index].vertex.x = x1 + ortho.x*w/2;
    vertices[index].vertex.y = y1 + ortho.y*w/2;
    vertices[index].tex_coord.x = 0;
    vertices[index].tex_coord.y = +d;
    index++;

    memcpy(&vertices[index], &vertex, sizeof(vertex_t));
    vertices[index].vertex.x = x2 - ortho.x*w/2;
    vertices[index].vertex.y = y2 - ortho.y*w/2;
    vertices[index].tex_coord.x = 1;
    vertices[index].tex_coord.y = -d;
    index++;
    memcpy(&vertices[index], &vertex, sizeof(vertex_t));
    vertices[index].vertex.x = x2 + ortho.x*w/2;
    vertices[index].vertex.y = y2 + ortho.y*w/2;
    vertices[index].tex_coord.x = 1;
    vertices[index].tex_coord.y = +d;
    index++;


    // End cap
    memcpy(&vertices[index], &vertex, sizeof(vertex_t));
    vertices[index].vertex.x = x2 + (-ortho.x+tangent.x)*w/2;
    vertices[index].vertex.y = y2 + (-ortho.y+tangent.y)*w/2;
    vertices[index].tex_coord.x = 1+d;
    vertices[index].tex_coord.y = -d;
    index++;
    memcpy(&vertices[index], &vertex, sizeof(vertex_t));
    vertices[index].vertex.x = x2 + (ortho.x+tangent.x)*w/2;
    vertices[index].vertex.y = y2 + (ortho.y+tangent.y)*w/2;
    vertices[index].tex_coord.x = 1+d;
    vertices[index].tex_coord.y = +d;
    index++;

    size_t i;
    for(i=0; i<=n; ++i)
    {
        indices[6*i+0] = 2*i+0;
        indices[6*i+1] = 2*i+1;
        indices[6*i+2] = 2*i+2;
        indices[6*i+3] = 2*i+1;
        indices[6*i+4] = 2*i+2;
        indices[6*i+5] = 2*i+3;
    }

    vertex_buffer_append( self, vertices, n_vertices, indices,  n_indices );
    free( indices );
    free( vertices );

/*


    vec2 points[2] = { {{x1,y1}}, {{x2,y2}} };
    size_t n = 2;

    int n_vertices = 2*n; //+2+2;
    vertex_t * vertices = (vertex_t *) calloc( n_vertices, sizeof(vertex_t) );

    int n_indices  = 6*(n+1);
    GLuint * indices = (GLuint *) calloc( n_indices, sizeof(GLuint) );

    float d,w;
    if (thickness < 1.0)
    {
        w = 2.0;
        color.a = thickness;
        d = (w+2)/w;
    }
    else
    {
        d = (thickness+2.0)/thickness;
        w = thickness+2.0;
    }

    vertex_t vertex = { {{0.0, 0.0, 0.0}}, color, {{0.0, 0.0}} };

    // Extract tangent/ortho vector
    vec2 tangent = {{x2-x1, y2-y1}};
    double norm = sqrt(tangent.x*tangent.x+tangent.y*tangent.y);
    if( norm > 0 )
    {
        tangent.x /= norm;
        tangent.y /= norm;
    }
    vec2 ortho = {{-tangent.y, tangent.x}};
    size_t index=0;

    // Start cap
    memcpy(&vertices[index], &vertex, sizeof(vertex_t));
    vertices[index].vertex.x = x1 + (-ortho.x-tangent.x)*w/2;
    vertices[index].vertex.y = y1 + (-ortho.y-tangent.y)*w/2;
    vertices[index].tex_coord.s = -d;
    vertices[index].tex_coord.t = -d;
    index++;
    memcpy(&vertices[index], &vertex, sizeof(vertex_t));
    vertices[index].vertex.x = x1 + (ortho.x-tangent.x)*w/2;
    vertices[index].vertex.y = y1 + (ortho.y-tangent.y)*w/2;
    vertices[index].tex_coord.s = -d;
    vertices[index].tex_coord.t = +d;
    index++;
*/
    // Actual line segment
/*
    memcpy(&vertices[index], &vertex, sizeof(vertex_t));
    vertices[index].vertex.x = x1 - ortho.x*w/2;
    vertices[index].vertex.y = y1 - ortho.y*w/2;
    vertices[index].tex_coord.s = 0;
    vertices[index].tex_coord.t = -d;
    index++;
    memcpy(&vertices[index], &vertex, sizeof(vertex_t));
    vertices[index].vertex.x = x1 + ortho.x*w/2;
    vertices[index].vertex.y = y1 + ortho.y*w/2;
    vertices[index].tex_coord.s = 0;
    vertices[index].tex_coord.t = +d;
    index++;

    memcpy(&vertices[index], &vertex, sizeof(vertex_t));
    vertices[index].vertex.x = x2 - ortho.x*w/2;
    vertices[index].vertex.y = y2 - ortho.y*w/2;
    vertices[index].tex_coord.s = 0;
    vertices[index].tex_coord.t = -d;
    index++;
    memcpy(&vertices[index], &vertex, sizeof(vertex_t));
    vertices[index].vertex.x = x2 + ortho.x*w/2;
    vertices[index].vertex.y = y2 + ortho.y*w/2;
    vertices[index].tex_coord.s = 0;
    vertices[index].tex_coord.t = +d;
    index++;
*/
/*
    // End cap
    memcpy(&vertices[index], &vertex, sizeof(vertex_t));
    vertices[index].vertex.x = x2 + (-ortho.x+tangent.x)*w/2;
    vertices[index].vertex.y = y2 + (-ortho.y+tangent.y)*w/2;
    vertices[index].tex_coord.s = 1+d;
    vertices[index].tex_coord.t = -d;
    index++;
    memcpy(&vertices[index], &vertex, sizeof(vertex_t));
    vertices[index].vertex.x = x2 + (ortho.x+tangent.x)*w/2;
    vertices[index].vertex.y = y2 + (ortho.y+tangent.y)*w/2;
    vertices[index].tex_coord.s = 1+d;
    vertices[index].tex_coord.t = +d;
    index++;

    size_t i;
    for(i=0; i<=n; ++i)
    {
        indices[6*i+0] = 2*i+0;
        indices[6*i+1] = 2*i+1;
        indices[6*i+2] = 2*i+2;
        indices[6*i+3] = 2*i+1;
        indices[6*i+4] = 2*i+2;
        indices[6*i+5] = 2*i+3;
    }
    collection_append( self, vertices, n_vertices, indices, n_indices );
    free( indices );
    free( vertices );
*/
}
