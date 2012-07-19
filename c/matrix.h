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
#ifndef __MATRIX_H__
#define __MATRIX_H__

/**
 * 4x4 float matrix
 */
typedef struct
{
    float data[4*4];
} matrix_t;


/**
 * Replace the current matrix with the identity matrix.
 *
 * @param self   current transformation matrix
 */
  matrix_t *
  matrix_load_identity( matrix_t *self );


/**
 * Multiply the current matrix with the specified matrix.
 *
 * @param self   current matrix
 * @param self   another matrix
 */
  matrix_t *
  matrix_multiply( matrix_t *self,
                   const matrix_t *other );


/**
 * Multiply the given matrix with a perspective matrix.
 *
 * @param self   current matrix
 * @param left   coordinate of the left vertical clipping plane
 * @param right  coordinate of the right vertical clipping plane
 * @param bottom coordinate of the bottom horizontal clipping plane
 * @param top    coordinate of the top horizontal clipping plane
 * @param z_near distance of the near clipping plane
 * @param z_far  distance of the far clipping plane
 */
  matrix_t *
  matrix_frustum( matrix_t *self, 
                  float left,   float right,
                  float bottom, float top,
                  float z_near, float z_far );


/**
 * Multiply the current matrix with an orthographic matrix.
 *
 * @param self   current matrix
 * @param left   coordinate of the left vertical clipping plane
 * @param right  coordinate of the right vertical clipping plane
 * @param bottom coordinate of the bottom horizontal clipping plane
 * @param top    coordinate of the top horizontal clipping plane
 * @param z_near distance of the near clipping plane
 * @param z_far  distance of the far clipping plane
 */
  matrix_t *
  matrix_ortho( matrix_t *self, 
                float left,   float right,
                float bottom, float top,
                float z_near, float z_far );

/**
 * Multiply the current with a perpective matrix.
 *
 * @param self   current matrix
 * @param fovy   specifies the field of view angle, in degrees, in the y direction.
 * @param aspect aspect ratio that determines the field of view in the x direction.
 * @param z_near distance to the near clipping plane
 * @param z_far  distance to the far clipping plane
 */
  matrix_t *
  matrix_perspective( matrix_t *self, 
                      float fovy,   float aspect,
                      float z_near, float z_far );

/**
 * Multiply current matrix by a rotation matrix.
 *
 * @param self   current matrix
 * @param angle  angle of rotation in degrees
 * @param x      x coordinate of a vector
 * @param y      y coordinate of a vector
 * @param z      z coordinate of a vector
 */
  matrix_t *
  matrix_rotate( matrix_t *self, 
                 float angle,
                 float x, float y, float z );

/**
 * Multiply current matrix by a translation matrix.
 *
 * @param self   current matrix
 * @param x      x coordinate of a vector
 * @param y      y coordinate of a vector
 * @param z      z coordinate of a vector
 */
  matrix_t *
  matrix_translate( matrix_t *self, 
                    float x, float y, float z );

/**
 * Multiply currentmatrix by a general scaling matrix.
 *
 * @param self   current matrix
 * @param x      x scaling factor
 * @param y      y scaling factor
 * @param z      z scaling factor
 */
  matrix_t *
  matrix_scale( matrix_t *self, 
                float x, float y, float z );


#endif /* __MATRIX_H__ */
