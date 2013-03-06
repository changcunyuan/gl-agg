// ----------------------------------------------------------------------------
// OpenGL Anti-Grain Geometry (GL-AGG) - Version 0.1
// A high quality OpenGL rendering engine
// Copyright (C) 2012 Nicolas P. Rougier. All rights reserved.
// Contact: Nicolas.Rougier@gmail.com
//         http://code.google.com/p/gl-agg/
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
// 1. Redistributions of source code must retain the above copyright notice,
//    this list of conditions and the following disclaimer.
//
// 2. Redistributions in binary form must reproduce the above copyright
//    notice, this list of conditions and the following disclaimer in the
//    documentation and/or other materials provided with the distribution.
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

// Global transform to be applied as (x0,y0,scale,rotation)
uniform vec4 Transform;
// Local transform to be applied as (x0,y0,scale,rotation)
attribute vec4 transform;
// Tangent to the line segment
attribute vec2 tangent;
// Line thickness
attribute float thickness;
// Line antialias support radius
attribute float support;
// Line length
attribute float length;
// Start/End caps
attribute vec2 cap;

varying float _length;
varying float _support;
varying float _thickness;
varying vec2  _cap;
void main()
{
    vec2  translation = transform.xy + Transform.xy;
    float scale       = transform.z * Transform.z;
    float rotation    = transform.w;

    _cap = cap;
    _support = support;
    _length = length * scale;

    // Thickness below 1 pixel are represented using a 1 pixel thickness
    // and a modified alpha
    float alpha = min(thickness, 1.0);
    _thickness = max(thickness, 1.0);

    // This is the actual half) width of the line
    float w = ceil(2.5*_support+_thickness)/2.0;

    vec2 t = normalize(tangent)*w;
    float u = gl_MultiTexCoord0.x;
    float v = gl_MultiTexCoord0.y;

    vec4 vertex = gl_Vertex;
    vertex.xy *= scale;

    vertex.xy += vec2( +t.y, -t.x) * v;
    gl_TexCoord[0].xy = vec2( u*scale, +w*v);

    // Cap at start
    if (u < 0.0)
    {
        vertex.xy -= vec2(t.x,t.y);
        gl_TexCoord[0].xy = vec2( -w, +w*v);
    }

    // Cap at end
    if (u > length)
    {
        vertex.xy += vec2(t.x,t.y);
        gl_TexCoord[0].xy = vec2( _length + w, +w*v);
    }

    mat2 rot= mat2( cos( rotation ), -sin( rotation ),
                    sin( rotation ),  cos( rotation ));
    vertex.xy *= rot;
    vertex.xy += transform.xy * scale;
    vertex.xy += Transform.xy;


    gl_Position = gl_ModelViewProjectionMatrix * vertex;
    gl_FrontColor = vec4(gl_Color.rgb, gl_Color.a*alpha);
}
