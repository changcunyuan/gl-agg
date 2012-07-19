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
#include "gl-agg.h"


// --------------------------------------------------- typedefs and structs ---

enum line_cap_e
{
    square_cap = 0,
    butt_cap   = 1,
    round_cap  = 2
};

enum line_join_e
{
    bevel_join = 0,
    miter_join = 1,
    round_join = 2
};




// ------------------------------------------------------- global variables ---
vertex_buffer_t *buffer;
GLuint program;
matrix_t projection;
matrix_t modelview;


// --------------------------------------------------------------- reshape ---
void reshape(int width, int height)
{
    glViewport( 0, 0, width, height );

    matrix_load_identity( &projection );
    matrix_ortho( &projection, 0, width, 0, height, -1000, +1000 );
    matrix_load_identity( &modelview );

    glMatrixMode( GL_PROJECTION );
    glLoadMatrixf( projection.data );

    glMatrixMode( GL_MODELVIEW );
    glLoadMatrixf( modelview.data );

    glutPostRedisplay( );
}

// --------------------------------------------------------------- keyboard ---
void keyboard( unsigned char key, int x, int y )
{
    if ( key == 27 )
    {
        exit( EXIT_SUCCESS );
    }
}


// -------------------------------------------------------------- vec2_norm ---
double
vec2_norm( vec2 P )
{
    return sqrt( P.x*P.x + P.y*P.y );
}

// --------------------------------------------------------------- vec2_add ---
vec2
vec2_add( vec2 P1, vec2 P2 )
{
    return (vec2) {{P1.x+P2.x, P1.y+P2.y }};
}

// ---------------------------------------------------------------- tangent ---
vec2
vec2_tangent( vec2 P1, vec2 P2 )
{
    vec2 T = {{ P2.x - P1.x, P2.y - P1.y }};
    float norm = sqrt( T.x*T.x + T.y*T.y );
    if( norm > 0 )
    {
        T.x /= norm;
        T.y /= norm;
    }
    return T;
}

// ------------------------------------------------------------- vec2_ortho ---
vec2
vec2_ortho( vec2 P1, vec2 P2 )
{
    vec2 T = vec2_tangent( P1, P2 );
    return (vec2) {{ -T.y, T.x }};
}

// ----------------------------------------------------------- intersection ---
int
intersection( vec2 P1, vec2 P2, vec2 P3, vec2 P4, vec2 *I) 
{
    // Code by Paul Bourke
    // http://paulbourke.net/geometry/lineline2d/
    float epsilon = 1e-9;
    float mua,mub;
    float denom,numera,numerb;

    float x1 = P1.x, y1 = P1.y;
    float x2 = P2.x, y2 = P2.y;
    float x3 = P3.x, y3 = P3.y;
    float x4 = P4.x, y4 = P4.y;
    float *x = &(I->x), *y = &(I->y);

    denom  = (y4-y3) * (x2-x1) - (x4-x3) * (y2-y1);
    numera = (x4-x3) * (y1-y3) - (y4-y3) * (x1-x3);
    numerb = (x2-x1) * (y1-y3) - (y2-y1) * (x1-x3);

    /* Are the line coincident? */
    if( ( fabs( numera ) < epsilon ) &&
        ( fabs( numerb ) < epsilon ) &&
        ( fabs( denom )  < epsilon ) )
    {
        *x = (x1 + x2) / 2;
        *y = (y1 + y2) / 2;
        // Segments intersect
        return 2;
    }
    
    /* Are the line parallel */
    if( fabs(denom) < epsilon )
    {
        *x = 0;
        *y = 0;
        return 0;
    }
    
    /* Is the intersection along the the segments */
    mua = numera / denom;
    mub = numerb / denom;
    *x = x1 + mua * (x2 - x1);
    *y = y1 + mua * (y2 - y1);
    if (mua < 0 || mua > 1 || mub < 0 || mub > 1)
    {
        // Lines intersect but no segments
        return 1;
    }
    // Segments intersect
    return 2;
}



// --------------------------------------------- vertex_buffer_add_polyline ---
/*
 *      A1-------------------J---I
 *                               | 
 *      A--------------------B   K 
 *                           |   |
 *      A2---------------L   |   |
 *                       |   |   |
 *                       |   |   |
 *                       |   |   |
 *                      C2   C   C1
 */
void
vertex_buffer_add_polyline( vertex_buffer_t * self,
                            vec2 *points, size_t n_points,
                            vec4 color, double thickness,
                            int join, int cap )
{
    typedef struct { float x,y,z,r,g,b,a,s,t,u; } vertex_t;
    assert( self );
    assert( n_points > 2 );
    assert( strcmp( vertex_buffer_format( self ), "v3f:c4f:t3f" ) == 0 );

    float d,w;
    if (thickness < 1.0)
    {
        w = 2.0;
        color.a *= thickness;
        d = (w+2)/w;
    }
    else
    {
        d = (thickness+2.0)/thickness;
        w = thickness+2.0;
    }
    float r = color.r;
    float g = color.g;
    float b = color.b;
    float a = color.a;
    float t = thickness;

    size_t n_vertices = 0;
    size_t n_indices = 0;
    if( (join == bevel_join) )
    {
        n_vertices = 2 + (n_points-2) * 6 + 4;
        n_indices =  2*3  + (n_points-2) * 3 * 3 + 6;
    }
    else if( join == miter_join )
    {
        n_vertices = 2 + (n_points-2) * 6 + 4;
        n_indices =  2*3  + (n_points-2) * 4 * 3 + 6;
    }
    else
    {
        n_vertices = 2 + (n_points-2) * 10 + 4;
        n_indices =  2*3  + (n_points-2) * 6 * 3 + 6;
    }
    vertex_t * vertices = (vertex_t *) calloc( n_vertices, sizeof(vertex_t) );
    GLuint * indices = (GLuint *) calloc( n_indices, sizeof(GLuint) );

    vec2 A,B,C;
    vec2 A1,A2,C1,C2;
    vec2 T_ba,O_ab, T_bc, O_cb;
    vec2 I,J,K,L,T;
    size_t i;
    size_t v_index = 0;
    size_t v_count = 0;
    size_t i_index = 0;
    size_t i_count = 0;
    for( i=0; i< (n_points-2); ++i )
    {
        v_count = 0;
        i_count = 0;

        A = points[i+0];
        B = points[i+1];
        C = points[i+2];
        T_ba = (vec2) {{ B.x-A.x, B.y-A.y }};
        T_bc = (vec2) {{ B.x-C.x, B.y-C.y }};
        O_ab = vec2_ortho( A, B );
        O_cb = vec2_ortho( C, B );
        C1 = (vec2) {{ C.x - w/2*O_cb.x, C.y - w/2*O_cb.y }};
        C2 = (vec2) {{ C.x + w/2*O_cb.x, C.y + w/2*O_cb.y }};
        if( i == 0)
        {
            A1 = (vec2) {{ A.x + w/2*O_ab.x, A.y + w/2*O_ab.y }};
            A2 = (vec2) {{ A.x - w/2*O_ab.x, A.y - w/2*O_ab.y }};
        }
        intersection( A1, (vec2) {{ A1.x + T_ba.x, A1.y + T_ba.y }},
                      C1, (vec2) {{ C1.x + T_bc.x, C1.y + T_bc.y }}, &I);
        int cross = intersection( A2, (vec2) {{ A2.x + T_ba.x, A2.y + T_ba.y }},
                                  C2, (vec2) {{ C2.x + T_bc.x, C2.y + T_bc.y }}, &L);
        if( cross == 2)
        {
            J = (vec2) {{ B.x + w/2*O_ab.x, B.y + w/2*O_ab.y }};
            K = (vec2) {{ B.x - w/2*O_cb.x, B.y - w/2*O_cb.y }};        
        }
        else
        {
            T = I; I = L; L = T;
            T = A1; A1 = A2; A2 = T;
            T = C1; C1 = C2; C2 = T;
            J = (vec2) {{ B.x - w/2*O_ab.x, B.y - w/2*O_ab.y }};
            K = (vec2) {{ B.x + w/2*O_cb.x, B.y + w/2*O_cb.y }};        
        }

        // Cap start
        if( i == 0 )
        {
            vec2 T = vec2_tangent(B,A);
            vec2 cA1 = {{ A1.x + w/2*T.x, A1.y + w/2*T.y }};
            vec2 cA2 = {{ A2.x + w/2*T.x, A2.y + w/2*T.y }};

            float tt = t;
            if( (cap == square_cap) || (cap == butt_cap) )
            {
                tt = -t;
            }
            vertices[v_index+0] = (vertex_t) { cA1.x,cA1.y,0, r,g,b,a, -d,+d,tt }; // cA1
            vertices[v_index+1] = (vertex_t) { cA2.x,cA2.y,0, r,g,b,a, -d,-d,tt }; // cA2
            vertices[v_index+2] = (vertex_t) {  A1.x, A1.y,0, r,g,b,a,  0,+d,tt }; // A1
            vertices[v_index+3] = (vertex_t) {  A2.x, A2.y,0, r,g,b,a,  0,-d,tt }; // A2

            indices[i_index+0] = v_index+0; // cA1
            indices[i_index+1] = v_index+1; // cA2
            indices[i_index+2] = v_index+2; // A1
            i_index += 3; i_count += 3;

            indices[i_index+0] = v_index+1; // cA1
            indices[i_index+1] = v_index+2; // A1
            indices[i_index+2] = v_index+3; // A2
            i_index += 3; i_count += 3;

            v_index += 4;
        }

        vertices[v_index+0] = (vertex_t) { A1.x,A1.y,0, r,g,b,a, 0,+d,t }; // A1
        vertices[v_index+1] = (vertex_t) { A2.x,A2.y,0, r,g,b,a, 0,-d,t }; // A2
        vertices[v_index+2] = (vertex_t) {  I.x, I.y,0, r,g,b,a, 0,+d,t }; // I
        vertices[v_index+3] = (vertex_t) {  J.x, J.y,0, r,g,b,a, 0,+d,t }; // J
        vertices[v_index+4] = (vertex_t) {  K.x, K.y,0, r,g,b,a, 0,+d,t }; // K
        vertices[v_index+5] = (vertex_t) {  L.x, L.y,0, r,g,b,a, 0,-d,t }; // L
        v_count += 6;

        indices[i_index+0] = v_index+0; // A1
        indices[i_index+1] = v_index+1; // A2
        indices[i_index+2] = v_index+5; // L
        i_index += 3; i_count += 3;

        indices[i_index+0] = v_index+0; // A1
        indices[i_index+1] = v_index+3; // J
        indices[i_index+2] = v_index+5; // L
        i_index += 3; i_count += 3;

        /* Bevel joints */
        if( join == bevel_join )
        {
            indices[i_index+0] = v_index+3; // J
            indices[i_index+1] = v_index+4; // K
            indices[i_index+2] = v_index+5; // L
            i_index += 3; i_count += 3;
        }

        /* Miter joints */
        else if( join == miter_join )
        {
            indices[i_index+0] = v_index+2; // I
            indices[i_index+1] = v_index+3; // J
            indices[i_index+2] = v_index+5; // L
            i_index += 3; i_count += 3;

            indices[i_index+0] = v_index+2; // I
            indices[i_index+1] = v_index+4; // K
            indices[i_index+2] = v_index+5; // L
            i_index += 3; i_count += 3;
        }

        /* Round joints */
        else {
            float jk = vec2_norm( (vec2) {{ J.x-K.x, J.y-K.y }} );
            float jb = vec2_norm( (vec2) {{ J.x-B.x, J.y-B.y }} );
            float ib = vec2_norm( (vec2) {{ I.x-B.x, I.y-B.y }} );
            float jl = vec2_norm( (vec2) {{ J.x-L.x, J.y-L.y }} );
            float d1 = ib/jb;
            float d2 = 0.5*jk/jb;
            float d3 = sqrt(1-d2*d2);
            float c = w/jl;
            d1 *= d; d2 *= d; d3 *= d;

            vertices[v_index+6] = (vertex_t) {  I.x, I.y,0, r,g,b,a, -d1,  0,t };    // I'
            vertices[v_index+7] = (vertex_t) {  J.x, J.y,0, r,g,b,a, -d3,+d2,t };    // J'
            vertices[v_index+8] = (vertex_t) {  K.x, K.y,0, r,g,b,a, -d3,-d2,t };    // K'
            vertices[v_index+9] = (vertex_t) {  L.x, L.y,0, r,g,b,a, 2*c*d-d3,0,t }; // L'
            v_count += 4;

            indices[i_index+0] = v_index+6; // I'
            indices[i_index+1] = v_index+7; // J'
            indices[i_index+2] = v_index+8; // K'
            i_index += 3; i_count += 3;

            indices[i_index+0] = v_index+7; // J'
            indices[i_index+1] = v_index+8; // K'
            indices[i_index+2] = v_index+9; // L'
            i_index += 3; i_count += 3;
        }
  
      
        if( i == (n_points-3) )
        {
            vertices[v_index+v_count+0] = (vertex_t) {  C1.x, C1.y,0, r,g,b,a, 0,+d,t };    // C1
            vertices[v_index+v_count+1] = (vertex_t) {  C2.x, C2.y,0, r,g,b,a, 0,-d,t };    // C2
            v_count += 2;

            indices[i_index+0] = v_index+v_count-2+0; // C1
            indices[i_index+1] = v_index+v_count-2+1; // C2
            indices[i_index+2] = v_index+5;           // L
            i_index += 3; i_count += 3;

            indices[i_index+0] = v_index+v_count-2+0; // C1
            indices[i_index+1] = v_index+5;           // L
            indices[i_index+2] = v_index+4;           // K
            i_index += 3; i_count += 3;
        }
        v_index += v_count;
        if( cross == 2 )
        {
            A1 = K;
            A2 = L;
        }
        else
        {
            A1 = L;
            A2 = K;
        }
    }
    vertex_buffer_append( self, vertices, n_vertices, indices,  n_indices );
}




// ---------------------------------------------------------------- display ---
void
display( void )
{
    glClearColor( 1.0, 1.0, 1.0, 1.0 );
    glClear( GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT );
    glEnable( GL_BLEND );
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    // glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );
    glUseProgram( program );
    vertex_buffer_render( buffer, GL_TRIANGLES, "vtc" );
    glUseProgram( 0 );
    glutSwapBuffers();
}



// ------------------------------------------------------------------- main ---
int
main( int argc, char **argv )
{
    glutInit( &argc, argv );
    glutInitDisplayMode( GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH );
    glutInitWindowSize( 256, 256) ;
    glutCreateWindow( argv[0] );
    glutDisplayFunc( display );
    glutReshapeFunc( reshape );
    glutKeyboardFunc( keyboard );

    buffer = vertex_buffer_new( "v3f:c4f:t3f" ); 
    program = shader_load( "shaders/line-aa.vert",
                           "shaders/line-aa-round.frag" );

    vec4 color = {{0,0,0,1}};
    float thickness = 32;
    float x0 = 30;
    float y0 = 210;
    {
        vec2 points[] = { {{ x0+  0, y0+10 }},
                          {{ x0+ 40, y0-10 }},
                          {{ x0+ 80, y0+10 }},
                          {{ x0+120, y0-10 }},
                          {{ x0+160, y0+10 }},
                          {{ x0+200, y0-10 }} };
        vertex_buffer_add_polyline( buffer, points, 6, color, thickness, bevel_join, square_cap);
    }
    {
        y0 -= 80;
        vec2 points[] = { {{ x0+  0, y0+10 }},
                          {{ x0+ 40, y0-10 }},
                          {{ x0+ 80, y0+10 }},
                          {{ x0+120, y0-10 }},
                          {{ x0+160, y0+10 }},
                          {{ x0+200, y0-10 }} };
        vertex_buffer_add_polyline( buffer, points, 6, color, thickness, miter_join, square_cap);
    }
    {
        y0 -= 80;
        vec2 points[] = { {{ x0+  0, y0+10 }},
                          {{ x0+ 40, y0-10 }},
                          {{ x0+ 80, y0+10 }},
                          {{ x0+120, y0-10 }},
                          {{ x0+160, y0+10 }},
                          {{ x0+200, y0-10 }} };
        vertex_buffer_add_polyline( buffer, points, 6, color, thickness, round_join, round_cap);
    }

    glutMainLoop();
    return 0;
}
