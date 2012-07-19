// ----------------------------------------------------------------------------
// OpenGL Anti-Grain Geometry (GL-AGG) - Version 0.1
// A high quality OpenGL rendering engine for C
// Copyright (C) 2012 Nicolas P. Rougier. All rights reserved.
// Contact: Nicolas.Rougier@gmail.com
//          http:* code.google.com/p/gl-agg/
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
void main()
{
    float support = 1.0;

    vec2 uv = gl_TexCoord[0].xy;
    float thickness = gl_TexCoord[0].z;
    float length = gl_TexCoord[0].w;

    float t = thickness/2.0-support;
    vec4 color = gl_Color;
    float d; 
    float dx = uv.x;
    float dy = abs(uv.y); // - t;

    // cap at origin
    if( dx <= 0.0 )
    {
        dx = abs(dx);

        // Round cap   
        // d = sqrt(dx*dx+dy*dy) - t;

        // Triangular cap   
        d = (dx+dy) - t;
        
        // Square cap
        // d = max(dx,dy) - t;
    }
    // cap at end
    else if ( dx >= length )
    {
        dx -= length;

        // Round cap   
        // d = sqrt(dx*dx+dy*dy) - t;

        // Triangular cap   
        d = (dx+dy) - t;

        // Square cap
        // d = max(dx,dy) - t;
    }
    // line body
    else
    {
        d = dy - t;
    }

    if( d < 0.0 )
    {
        gl_FragColor = vec4(color.rgb, color.a);
    }
    else
    {
        float alpha = d/support;
        alpha = exp(-alpha*alpha);
        gl_FragColor = vec4(color.rgb, alpha*color.a);
    }
}
