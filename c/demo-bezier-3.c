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
    vec2 tex_coord;
} vertex_t;


// ------------------------------------------------------- global variables ---
GLuint all;
GLuint body;
GLuint envelope;
vertex_buffer_t * buffer;
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

// ---------------------------------------------------------------- display ---
void
display( void )
{
    static int frame = 0;
    static int timebase = 0;
	frame++;
	int time = glutGet( GLUT_ELAPSED_TIME );
    if( (time-timebase) > (2500) )
    {
        printf( "FPS : %.2f (%d frames in %.2f second)\n",
                frame*1000.0/(time-timebase), frame, (time-timebase)/1000.0);
        timebase = time;
        frame = 0;
    }

    glClearColor( 1.0, 1.0, 1.0, 1.0 );
    glClear( GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT );
    glEnable( GL_BLEND );
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);  

    // Render at once (no stencil test)
    if( 0 )
    {
        glDisable( GL_STENCIL_TEST );
        glUseProgram( all );
        vertex_buffer_render( buffer, GL_TRIANGLES, "vtc" );
    }
    // Render each curve, controling overdrawing
    else {
        glEnable( GL_STENCIL_TEST );
        glStencilOp( GL_KEEP, GL_KEEP, GL_REPLACE );
        glClear( GL_STENCIL_BUFFER_BIT );

        vertex_buffer_render_setup( buffer, GL_TRIANGLES, "vtc" );
        size_t i;
        for( i=0; i<vertex_buffer_size( buffer ); ++i)
        {
            glStencilFunc( GL_GREATER, i+1, 0xffffffff ); 
            glUseProgram( body );
            vertex_buffer_render_item( buffer, i );
            glUseProgram( envelope );
            vertex_buffer_render_item( buffer, i );
        }
        vertex_buffer_render_finish( buffer );
    }
    glUseProgram( 0 );

    glutSwapBuffers();
}


// --------------------------------------------------------- random_uniform ---
float
random_uniform( float lower,
                float upper)
{
    return lower + random()/(float)(RAND_MAX)*(upper-lower);
}


// ------------------------------------------------------------------- main ---
int
main( int argc, char **argv )
{
    glutInit( &argc, argv );
    glutInitDisplayMode( GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_STENCIL );
    glutInitWindowSize( 512, 512);
    glutCreateWindow( argv[0] );
    glutIdleFunc( display );
    glutDisplayFunc( display );
    glutReshapeFunc( reshape );
    glutKeyboardFunc( keyboard );

    buffer = vertex_buffer_new( "v3f:c4f:t3f" ); 

    size_t n = 100;
    float xmin=0, xmax = 512;
    float ymin=0, ymax = 512;
    size_t i;
    for (i = 0; i < n; ++i)
    {
        float x1 = random_uniform( xmin, xmax );
        float x2 = random_uniform( xmin, xmax );
        float x3 = random_uniform( xmin, xmax );
        float x4 = random_uniform( xmin, xmax );
        float y1 = random_uniform( ymin, ymax );
        float y2 = random_uniform( ymin, ymax );
        float y3 = random_uniform( ymin, ymax );
        float y4 = random_uniform( ymin, ymax );
        float r = random_uniform (0, 1);
        float g = random_uniform (0, 1);
        float b = random_uniform (0, 1);
        float a = random_uniform (0, 1);
        float w = random_uniform (2,10);
        vec4 color = {{r,g,b,a}};
        vertex_buffer_add_curve4( buffer, x1, y1, x2, y2, x3, y3, x4, y4, color, w );
    }

    all  = shader_load( "shaders/line-aa.vert",
                        "shaders/line-aa-round.frag" );
    body = shader_load( "shaders/line-aa.vert",
                        "shaders/line-aa-round-body.frag" );
    envelope = shader_load( "shaders/line-aa.vert",
                            "shaders/line-aa-round-envelope.frag" );
    glutMainLoop();
    return 0;
}
