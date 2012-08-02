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
varying vec2 _radius;
varying float _support;
varying float _thickness;
varying vec4 _facecolor;
void main()
{
    float t = _thickness/2.0-_support;
    vec4 color = gl_Color;
    vec2 uv = gl_TexCoord[0].xy;
    float x2 = uv.x * uv.x;
    float y2 = uv.y * uv.y;

    float a2 = _radius.x+_thickness/2.;
    a2 *= a2;
    float b2 = _radius.y+_thickness/2.;
    b2 *= b2;

    float d1 = sqrt(x2/a2 + y2/b2);
    float width1 = fwidth(d1)*_support/1.25;
    float alpha1  = smoothstep(1.0 - width1, 1.0 + width1, d1);

    a2 = _radius.x - _thickness/2.;
    a2 *= a2;
    b2 = _radius.y - _thickness/2.;
    b2 *= b2;
    float d2 = sqrt(x2/a2 + y2/b2);
    float width2 = fwidth(d2)*_support/1.25;
    float alpha2  = smoothstep(1.0 + width2, 1.0 - width2, d2);

    if( alpha1 < alpha2)
    {
        gl_FragColor = mix(_facecolor, color, 1.0-alpha2);
    }
    else
    {
        gl_FragColor = vec4(color.rgb, (1.0-alpha1)*color.a);
    }
}
