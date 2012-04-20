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
#ifndef __VEC234_H__
#define __VEC234_H__

#ifdef __cplusplus
extern "C" {
#endif


/** Tuple of 4 ints */
typedef union
{
	int data[4];
	struct { int x; int y; int z; int w; };
	struct { int r; int g; int b; int a; };
	struct { int vstart;  int vcount; int istart; int icount; };
} ivec4;


/** Tuple of 3 ints */
typedef union {
	int data[3];
	struct { int x; int y; int z; };
	struct { int r; int g; int b; };
} ivec3;


/** Tuple of 2 ints */
typedef union {
	int data[2];
	struct { int x;      int y;   };
	struct { int s;      int t;   };
	struct { int start;  int end; };
} ivec2;


/** Tuple of 4 floats */
typedef union
{
	float data[4];
	struct { float x; float y; float z; float w; };
	struct { float r; float g; float b; float a; };
} vec4;


/** Tuple of 3 floats */
typedef union {
	float data[3];
	struct { float x; float y; float z; };
	struct { float r; float g; float b; };
} vec3;


/** Tuple of 2 floats */
typedef union {
	float data[2];
	struct { float x; float y; };
	struct { float s; float t; };
} vec2;


#ifdef __cplusplus
}
#endif

#endif /* __VEC234_H__ */
