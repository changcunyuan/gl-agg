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
const float epsilon = -1e-10;

float
compute_alpha(float d, float thickness, float support)
{
    d -= thickness/2.0-support;
    if( d < 0.0 )
    {
        return 1.0;
    }
    else
    {
        float alpha = d/support;
        alpha = exp(-alpha*alpha);
        return alpha;
    }
}


uniform vec2  size, offset;
uniform vec3  major_lines, minor_lines;
uniform vec3  major_ticks, minor_ticks;
uniform vec4  major_lines_color, minor_lines_color;
uniform vec4  major_ticks_color, minor_ticks_color;
void main() 
{ 
    float x = gl_TexCoord[0].x;
    float y = gl_TexCoord[0].y;
    
    // Major lines
    float Mx = mod(x - offset.x, major_lines.x); Mx = min(Mx,major_lines.x-Mx);
    float My = mod(y - offset.y, major_lines.y); My = min(My,major_lines.y-My);
    float M = min(Mx,My);

    // Minor lines
    float mx = mod(x - offset.x, minor_lines.x);  mx = min(mx,minor_lines.x-mx);
    float my = mod(y - offset.y, minor_lines.y);  my = min(my,minor_lines.y-my);
    float m = min(mx,my);

    vec4 color = major_lines_color;
    float alpha1 = compute_alpha( M, major_lines.z, 0.55);
    float alpha2 = compute_alpha( m, minor_lines.z, 0.60);
    float alpha  = alpha1;

    if( (alpha2 - alpha1) > epsilon )
    {
        alpha = alpha2;
        color = minor_lines_color;
    }

    // Top major ticks
    if( y > (size.y-major_ticks.y) )
    {
        float a = compute_alpha(Mx, major_ticks.z, 0.5);
        if ( (a - alpha)  > epsilon )
        {
            alpha = a;
            color = major_ticks_color;
        }
    }

    // Bottom major ticks
    if( y < major_ticks.y )
    {
        float a = compute_alpha(Mx, major_ticks.z, 0.5);
        if ( (a - alpha)  > epsilon )
        {
            alpha = a;
            color = major_ticks_color;
        }
    }

    // Left major ticks
    if( x < major_ticks.x )
    {
        float a = compute_alpha(My, major_ticks.z, 0.5);
        if ( (a - alpha)  > epsilon )
        {
            alpha = a;
            color = major_ticks_color;
        }
    }
    
    // Right major ticks
    if( x > (size.x-major_ticks.x) )
    {
        float a = compute_alpha(My, major_ticks.z, 0.5);
        if ( (a - alpha)  > epsilon )
        {
            alpha = a;
            color = major_ticks_color;
        }
    }
    
    // Top minor ticks
    if( y > (size.y-minor_ticks.y) )
    {
        float a = compute_alpha(mx, minor_ticks.z, 0.5);
        if ( (a - alpha)  > epsilon )
        {
            alpha = a;
            color = minor_ticks_color;
        }
    }
    
    // Bottom minor ticks
    if( y < minor_ticks.y )
    {
        float a = compute_alpha(mx, minor_ticks.z, 0.5);
        if ( (a - alpha)  > epsilon )
        {
            alpha = a;
            color = minor_ticks_color;
        }
    }
    
    // Left minor ticks
    if( x < minor_ticks.x )
    {
        float a = compute_alpha(my, minor_ticks.z, 0.5);
        if ( (a - alpha)  > epsilon )
        {
            alpha = a;
            color = minor_ticks_color;
        }
    }
    
    // Right major ticks
    if( x > (size.x-minor_ticks.x) )
    {
        float a = compute_alpha(my, minor_ticks.z, 0.5);
        if ( (a - alpha)  > epsilon )
        {
            alpha = a;
            color = minor_ticks_color;
        }
    }

    gl_FragColor = vec4(color.xyz, alpha*color.a);
}
