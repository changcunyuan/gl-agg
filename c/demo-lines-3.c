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
typedef struct {
    vec3 vertex;      
    vec4 color;
    vec3 tex_coord;
} vertex_t;

// ------------------------------------------------------- global variables ---
GLuint program[3];
vertex_buffer_t * buffer;
matrix_t projection;
matrix_t modelview;

// --------------------------------------------------------------- reshape ---
void reshape( int width, int height )
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

// ---------------------------------------------------------------- display ---
void
display( void )
{
    glClearColor( 1.0, 1.0, 1.0, 1.0 );
    glClear( GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT );

    glEnable( GL_BLEND );
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    vertex_buffer_render_setup( buffer, GL_TRIANGLES, "vtc" );
    glUseProgram( program[0] );
    vertex_buffer_render_item( buffer, 0 );
    glUseProgram( program[1] );
    vertex_buffer_render_item( buffer, 1 );
    glUseProgram( program[2] );
    vertex_buffer_render_item( buffer, 2 );
    vertex_buffer_render_finish( buffer );
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
    glutIdleFunc( display );
    glutDisplayFunc( display );
    glutReshapeFunc( reshape );
    glutKeyboardFunc( keyboard );

    buffer = vertex_buffer_new( "v3f:c4f:t3f" ); 
    program[0] = shader_load( "shaders/line-aa.vert",
                              "shaders/line-aa-round.frag" );
    program[1] = shader_load( "shaders/line-aa.vert",
                              "shaders/line-aa-butt.frag" );
    program[2] = shader_load( "shaders/line-aa.vert",
                              "shaders/line-aa-square.frag" );

    vec4 color = {{0,0,0,1}};
    vertex_buffer_add_line( buffer, 50,  50, 200,  50+20, color, 32 );
    vertex_buffer_add_line( buffer, 50, 122, 200, 122+20, color, 32 );
    vertex_buffer_add_line( buffer, 50, 194, 200, 194+20, color, 32 );

    glutMainLoop();
    return 0;
}
