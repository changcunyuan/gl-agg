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
#include "circle.h"

// ----------------------------------------------------------------------------
void
vertex_buffer_add_circle( vertex_buffer_t * self,
                          double cx, double cy, double radius,
                          vec4 color, double thickness )
{
    typedef struct { vec3 vertex; vec4 color; vec4 tex_coord; } vertex_t;

    assert( self );
    assert( strcmp( vertex_buffer_format( self ), "v3f:c4f:t4f" ) == 0 );

    float wx  = radius + 1;
    //float tx1 = -wx/(wx-1.0)+1.0;
    //float tx2 = +wx/(wx-1.0);
    float tx1 = +(wx)/(wx-1);
    float tx2 = -(wx)/(wx-1);

    float wy  = radius + 1;
    //float ty1 = -wy/(wy-1.0)+1.0;
    //float ty2 = +wy/(wy-1.0);
    float ty1 = +(wy)/(wy-1);
    float ty2 = -(wy)/(wy-1);

    vertex_t vertices[4] = {
        { {{cx-wx, cy-wy, 0}}, color, {{tx1, ty1, radius, thickness}} },
        { {{cx+wx, cy-wy, 0}}, color, {{tx2, ty1, radius, thickness}} },
        { {{cx+wx, cy+wy, 0}}, color, {{tx2, ty2, radius, thickness}} },
        { {{cx-wx, cy+wy, 0}}, color, {{tx1, ty2, radius, thickness}} } };
    GLuint indices[6] = { 0,1,2, 0,2,3 };

    vertex_buffer_append( self, vertices, 4, indices,  6 );
}
