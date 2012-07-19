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
#ifndef __CURVES_H__
#define __CURVES_H__
#include <stddef.h>

#include <math.h>
#include "vec234.h"
#include "vector.h"
#include "vertex-buffer.h"


/**
 *  Add a cubic bezier curve to a vertex_buffer
 *
 *  @param  self  A vertex buffer with format "v3f:c4f:t3f"
 *  @param  x1,y1 Control point 1
 *  @param  x2,y2 Control point 2
 *  @param  x3,y3 Control point 3
 */
  void
  vertex_buffer_add_curve3( vertex_buffer_t * self,
                            double x1, double y1, 
                            double x2, double y2, 
                            double x3, double y3,
                            vec4 color, double thickness );

/**
 *  Add a cubic bezier curve to a vertex_buffer
 *
 *  @param  self   A collection with format "v3f:c4f:t3f"
 *  @param  x1,y1  Control point 1
 *  @param  x2,y2  Control point 2
 *  @param  x3,y3  Control point 3
 *  @param  x4,y4  Control point 4
 */
  void
  vertex_buffer_add_curve4( vertex_buffer_t * self,
                            double x1, double y1, 
                            double x2, double y2, 
                            double x3, double y3,
                            double x4, double y4,
                            vec4 color, double thickness );

/**
 *  Returns a vector of points for the given bezier curve
 *
 *  @param  x1,y1 Control point 1
 *  @param  x2,y2 Control point 2
 *  @param  x3,y3 Control point 3
 *  @return       A vector of points describing the bezier curve
 */
vector_t *
curve3_bezier( double x1, double y1, 
               double x2, double y2, 
               double x3, double y3 );

/**
 *  Returns a vector of points for the given bezier curve
 *
 *  @param  x1,y1 Control point 1
 *  @param  x2,y2 Control point 2
 *  @param  x3,y3 Control point 3
 *  @param  x4,y4 Control point 4
 *  @return       A vector of points describing the bezier curve
 */
vector_t *
curve4_bezier( double x1, double y1, 
               double x2, double y2, 
               double x3, double y3,
               double x4, double y4 );


#endif /* __CURVES_H__ */
