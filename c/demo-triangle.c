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


// ------------------------------------------------------- global variables ---
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






// ---------------------------------------------------------------- tangent ---
vec2
tangent( vec2 P1, vec2 P2 )
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

// ------------------------------------------------------------------- norm ---
vec2
ortho( vec2 P1, vec2 P2 )
{
    vec2 T = tangent( P1, P2 );
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
    if( (abs(numera) < epsilon) && (abs(numerb) < epsilon) && (abs(denom) < epsilon) )
    {
        *x = (x1 + x2) / 2;
        *y = (y1 + y2) / 2;
        // Segments intersect
        return 2;
    }
    
    /* Are the line parallel */
    if( abs(denom) < epsilon )
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


// ----------------------------------------------------------------------------
void
triangle( vec2 A, vec2 B, vec2 C )
{
    vec2 Oab = ortho( A, B );
    vec2 Aa = {{ A.x + Oab.x, A.y + Oab.y }};

    vec2 Obc = ortho( B, C );
    vec2 Cc = {{ C.x + Obc.x, C.y + Obc.y }};

    vec2 O;
    intersection( A, Aa, C, Cc, &O );

    glColor4f(0,0,0,1);
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );
    glBegin( GL_TRIANGLES );
    glVertex2f( A.x, A.y );
    glVertex2f( B.x, B.y );
    glVertex2f( C.x, C.y );
    glEnd();
    
    printf("%f\n", O.x);
    printf("%f\n", O.y);

    glPolygonMode( GL_FRONT_AND_BACK, GL_FILL );
    glPointSize( 5 );
    glBegin( GL_POINTS );
    glVertex2f( O.x, O.y );
    glEnd();

}

// ---------------------------------------------------------------- display ---
void
display( void )
{
    glClearColor( 1.0, 1.0, 1.0, 1.0 );
    glClear( GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT );

    glEnable( GL_BLEND );
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    glPolygonMode( GL_FRONT_AND_BACK, GL_FILL );
    //glUseProgram( program );
    triangle( (vec2) {{ 100, 300 }},
              (vec2) {{ 200, 400 }},
              (vec2) {{ 300, 300 }} );


    glutSwapBuffers();
}



// ------------------------------------------------------------------- main ---
int
main( int argc, char **argv )
{
    glutInit( &argc, argv );
    glutInitDisplayMode( GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH );
    glutInitWindowSize( 512, 512) ;
    glutCreateWindow( argv[0] );
    glutDisplayFunc( display );
    glutReshapeFunc( reshape );
    glutKeyboardFunc( keyboard );

    program = shader_load( "shaders/line-aa.vert",
                           "shaders/line-aa-round.frag" );

    glutMainLoop();
    return 0;
}
