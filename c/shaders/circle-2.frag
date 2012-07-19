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
varying float a;
varying float b;
varying vec2 radii;
varying float thickness;
void main()
{
    vec4 color = gl_Color;
    vec2 p = gl_TexCoord[0].xy;
    float x2 = p.x*p.x;
    float y2 = p.y*p.y;

    float dist1  = sqrt((x2+y2));
    float width1 = fwidth(dist1);

    if( radii.x < 0.5 )
    {
        width1 = dist1;
    }
    float alpha1  = smoothstep(1.0 - width1, 1.0 + width1, dist1);

    if( thickness == 0.0 )
    {
        //gl_FragColor = vec4(color.rgb, min(2.0*radius,1.0)*min((1.0-alpha)));
        gl_FragColor = vec4(color.rgb, (1.0-alpha1)*min(radii.y,1.0));
        return;
    }
    else
    {
        float dist2  = sqrt(a*a*x2 + b*b*y2);
        float width2 = fwidth(dist2);   
        float alpha2  = smoothstep(  1.0 + width2,  1.0 - width2, dist2);
        gl_FragColor = vec4(color.rgb, (1.0-max(alpha1,alpha2))*min(radii.y,1.0));
    }
}
