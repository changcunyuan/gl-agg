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
varying float _length;
varying float _support;
varying float _thickness;
varying vec2 _cap;
void main()
{
    vec4 color = gl_Color;
    float t = _thickness/2.0-_support;
    vec2 uv = gl_TexCoord[0].xy;
    float d; 
    float dx = uv.x;
    float dy = abs(uv.y);

    // Cap at start
    if( dx < 0.0 )
    {
        dx = abs(dx);
        if      (_cap.x == 0.)  discard;               // None
        else if (_cap.x == 1.)  d = sqrt(dx*dx+dy*dy); // Round
        else if (_cap.x == 2.)  d = (dx+dy);           // Triangular
        else if (_cap.x == 3.)  d = max(dx,dy);        // Square
        else if (_cap.x == 4.)  d = max(dx+t,dy);      // Butt
    }
    // Cap at end
    else if ( dx > _length )
    {
        dx -= _length;
        if      (_cap.y == 0.)  discard;               // None
        else if (_cap.y == 1.)  d = sqrt(dx*dx+dy*dy); // Round
        else if (_cap.y == 2.)  d = (dx+dy);           // Triangular
        else if (_cap.y == 3.)  d = max(dx,dy);        // Square
        else if (_cap.y == 4.)  d = max(dx+t,dy);      // Butt
    }
    // Body
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
        float alpha = d/_support;
        alpha = exp(-alpha*alpha);
        gl_FragColor = vec4(color.xyz, alpha*color.a);
    }
}
