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
    vec4 p          = gl_TexCoord[0];
    float radius    = p.z;
    float thickness = p.w;

    vec4 color   = gl_Color;
    float dist   = sqrt(((p.x-0.5)*(p.x-0.5)+(p.y-0.5)*(p.y-0.5)));
    float width  = fwidth(dist);
    if( radius < 0.5 )
    {
        width = dist;
    }
    if( thickness == 0.0 )
    {
        float alpha  = smoothstep(0.5-width,0.5+width, dist);
        gl_FragColor = vec4(color.rgb,
                min(2.0*radius,1.0)*min((1.0-alpha), min(pow(radius,2.2),1.0)) );
    }
    else {
        float r = .5*(radius-0.5*thickness)/radius;
        float alpha1  = smoothstep(0.5-width,0.5+width, dist);
        float alpha2  = smoothstep(r+width,r-width, dist);
        gl_FragColor = vec4(color.rgb,
                (1.0-max(alpha1,alpha2)) * min(pow(thickness,1.0/2.2),1.0));
    }
}
