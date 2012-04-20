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

typedef struct {
    vec3 vertex;      
    vec4 color;
    vec3 tex_coord;
} vertex_t;
vertex_buffer_t * buffer;


// ------------------------------------------------------- global variables ---
GLuint program = 0;
matrix_t projection;
matrix_t modelview;


// --------------------------------------------------------------- reshape ---
void reshape(int width, int height)
{
    glViewport( 0, 0, width, height );
    matrix_load_identity( &projection );
    matrix_ortho( &projection, 0, width, 0, height, -1, +1 );
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

// ---------------------------------------------------------------- display ---
void
display( void )
{
    glClearColor( 1.0, 1.0, 1.0, 1.0 );
    glClear( GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT );

    glEnable( GL_BLEND );
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);  
    glDisable( GL_TEXTURE_2D );
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
    glutInitWindowSize( 256, 256 ) ;
    glutCreateWindow( argv[0] );
    glutDisplayFunc( display );
    glutReshapeFunc( reshape );
    glutKeyboardFunc( keyboard );

    buffer = vertex_buffer_new( "v3f:c4f:t3f" ); 
    size_t n = 20, i;
    float x0 =  25, y0 = 240;
    float x1 =  75, y1 = 290;
    float x2 = 175, y2 = 190;
    float x3 = 225, y3 = 240;
    vec4 color = {{0,0,0,1}};
    for (i = 0; i < n; ++i)
    {
        y0 -= 10; y1 -= 10;
        y2 -= 10; y3 -= 10;
        float w = (i+1)/10.0;
        vertex_buffer_add_curve4( buffer, x0, y0, x1, y1, x2, y2, x3, y3, color, w );
    }
    program = shader_load( "shaders/line-aa.vert",
                           "shaders/line-aa-round.frag" ); 
    glutMainLoop();
    return 0;
}
