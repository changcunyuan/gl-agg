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
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include "matrix.h"


// --------------------------------------------------- matrix_load_identity ---
matrix_t *
matrix_load_identity( matrix_t *self )
{
    assert( self );

    memset( self, 0, sizeof( matrix_t ) );
    self->data[0*4+0] = 1.0;
    self->data[1*4+1] = 1.0;
    self->data[2*4+2] = 1.0;
    self->data[3*4+3] = 1.0;

    return self;
}


// -------------------------------------------------------- matrix_multiply ---
matrix_t *
matrix_multiply( matrix_t *self,
                 const matrix_t *other )
{
    assert( self );
    assert( other );

    matrix_t result;
    float *A = self->data;
    const float *B = other->data;
    size_t i;
    for( i = 0; i < 4; ++i )
    {
        result.data[i*4+0] =
            (A[i*4+0] * B[0*4+0]) +
            (A[i*4+1] * B[1*4+0]) +
            (A[i*4+2] * B[2*4+0]) +
            (A[i*4+3] * B[3*4+0]) ;
        result.data[i*4+1] =
            (A[i*4+0] * B[0*4+1]) +
            (A[i*4+1] * B[1*4+1]) +
            (A[i*4+2] * B[2*4+1]) +
            (A[i*4+3] * B[3*4+1]) ;
        result.data[i*4+2] =
            (A[i*4+0] * B[0*4+2]) +
            (A[i*4+1] * B[1*4+2]) +
            (A[i*4+2] * B[2*4+2]) +
            (A[i*4+3] * B[3*4+2]) ;
        result.data[i*4+3] =
            (A[i*4+0] * B[0*4+3]) +
            (A[i*4+1] * B[1*4+3]) +
            (A[i*4+2] * B[2*4+3]) +
            (A[i*4+3] * B[3*4+3]) ;
    }

    memcpy( self, &result, sizeof( matrix_t ) );
    return self;
}


// --------------------------------------------------------- matrix_frustum ---
matrix_t *
matrix_frustum( matrix_t *self, 
                float left,   float right,
                float bottom, float top,
                float z_near, float z_far )
{
  assert( self );

  float dx = right - left;
  float dy = top   - bottom;
  float dz = z_far - z_near;

  if ( (z_near <= 0.0) || (z_far <= 0.0)  ||
       (dx <= 0.0) || (dy <= 0.0) || (dz <= 0.0) )
  {
      return self;
  }

  matrix_t frustum;
  matrix_load_identity( &frustum );
  float *data = frustum.data;

  data[0*4+0] = 2.0 * z_near / dx;
  data[1*4+1] = 2.0 * z_near / dy;
  data[2*4+0] = +(right  + left)   / dx;
  data[2*4+1] = +(top    + bottom) / dy;
  data[2*4+2] = -(z_near + z_far)  / dz;
  data[2*4+3] = -1.0;
  data[3*4+2] = -2.0 * z_near * z_far / dz;

  matrix_multiply( &frustum, self );
  memcpy( self, &frustum, sizeof( matrix_t ) );
  return self;
}


// ----------------------------------------------------------- matrix_ortho ---
matrix_t *
matrix_ortho( matrix_t *self, 
            float left,   float right,
            float bottom, float top,
            float z_near, float z_far )
{
    assert( self );

    float dx = right - left;
    float dy = top   - bottom;
    float dz = z_far - z_near;

    if ( (dx == 0.0) || (dy == 0.0) || (dz == 0.0) )
    {
        return self;
    }

    matrix_t ortho;
    matrix_load_identity( &ortho );
    float *data = ortho.data;

    data[0*4+0] = 2.0 / dx;
    data[3*4+0] = -(right + left) / dx;
    data[1*4+1] = 2.0 / dy;
    data[3*4+1] = -(top + bottom) / dy;
    data[2*4+2] = -2.0 / dz;
    data[3*4+2] = -(z_near + z_far) / dz;
    data[3*4+3] = 1.0;
    
    matrix_multiply( &ortho, self );
    memcpy( self, &ortho, sizeof( matrix_t ) );
    return self;
}


// ----------------------------------------------------- matrix_perspective ---
matrix_t *
matrix_perspective( matrix_t *self, 
                    float fovy,   float aspect,
                    float z_near, float z_far )
{
    assert( self );

    float h = tan( fovy / 360.0 * M_PI ) * z_near;
    float w = h * aspect;
    return matrix_frustum( self, -w, w, -h, h, z_near, z_far);
}


// ---------------------------------------------------------- matrix_rotate ---
matrix_t *
matrix_rotate( matrix_t *self, 
               float angle,
               float x, float y, float z )
{
    assert( self );

    float mag = sqrt(x*x + y*y + z*z);

    if( mag <= 0 )
    {
        return self;
    }

    float sin_angle = sin( angle * M_PI / 180.0 );
    float cos_angle = cos( angle * M_PI / 180.0 );
    float one_minus_cos= 1.0 - cos_angle;
    float xx, yy, zz, xy, yz, zx, xs, ys, zs;

    matrix_t rotation;
    matrix_load_identity( &rotation );
    float *data = rotation.data;

    x /= mag;
    y /= mag;
    z /= mag;
    xx = x * x;
    yy = y * y;
    zz = z * z;
    xy = x * y;
    yz = y * z;
    zx = z * x;
    xs = x * sin_angle;
    ys = y * sin_angle;
    zs = z * sin_angle;

    data[0*4+0] = (one_minus_cos * xx) + cos_angle;
    data[0*4+1] = (one_minus_cos * xy) - zs;
    data[0*4+2] = (one_minus_cos * zx) + ys;
    
    data[1*4+0] = (one_minus_cos * xy) + zs;
    data[1*4+1] = (one_minus_cos * yy) + cos_angle;
    data[1*4+2] = (one_minus_cos * yz) - xs;

    data[2*4+0] = (one_minus_cos * zx) - ys;
    data[2*4+1] = (one_minus_cos * yz) + xs;
    data[2*4+2] = (one_minus_cos * zz) + cos_angle;

    data[3*4+3] = 1.0;

    matrix_multiply( &rotation, self );
    memcpy( self, &rotation, sizeof( matrix_t ) );
    return self;
  
}

// ------------------------------------------------------- matrix_translate ---
matrix_t *
matrix_translate( matrix_t *self, 
                  float x, float y, float z )
{
    assert( self );

    float *data = self->data;
    data[3*4+0] += data[0*4+0] * x + data[1*4+0] * y + data[2*4+0] * z;
    data[3*4+1] += data[0*4+1] * x + data[1*4+1] * y + data[2*4+1] * z;
    data[3*4+2] += data[0*4+2] * x + data[1*4+2] * y + data[2*4+2] * z;
    data[3*4+3] += data[0*4+3] * x + data[1*4+3] * y + data[2*4+3] * z;

    return self;
}


// ----------------------------------------------------------- matrix_scale ---
matrix_t *
matrix_scale( matrix_t *self, 
              float x, float y, float z )
{
    assert( self );

    float *data = self->data;

    data[0*4+0] *= x;
    data[0*4+1] *= x;
    data[0*4+2] *= x;
    data[0*4+3] *= x;
    
    data[1*4+0] *= y;
    data[1*4+1] *= y;
    data[1*4+2] *= y;
    data[1*4+3] *= y;

    data[2*4+0] *= z;
    data[2*4+1] *= z;
    data[2*4+2] *= z;
    data[2*4+3] *= z;

    return self;
}
