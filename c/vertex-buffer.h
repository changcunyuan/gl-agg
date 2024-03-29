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
#ifndef __VERTEX_BUFFER_H__
#define __VERTEX_BUFFER_H__

#if defined(__APPLE__)
    #include <OpenGL/gl.h>
#else
    #include <GL/gl.h>
#endif
#include "vector.h"

#define MAX_VERTEX_ATTRIBUTE 16


/**
 * @file   vertex-buffer.h
 * @author Nicolas Rougier (Nicolas.Rougier@inria.fr)
 * @date   April, 2012
 *
 * @defgroup vertex-buffer Vertex buffer
 *
 * @{
 */


/**
 *  Generic vertex attribute.
 */
typedef struct 
{
    /**
     *  a client-side capability.
     */
    GLenum target;

    /**
     *  a translated client-side capability.
     */
    GLchar ctarget;

    /**
     * index of the generic vertex attribute to be modified.
     */
    GLuint index;

    /**
     * Number of components per generic vertex attribute. Must be 1, 2, 3, or
     * 4. The initial value is 4.
     */
    GLint size;

    /** 
     *  Data type of each component in the array. Symbolic constants GL_BYTE,
     *  GL_UNSIGNED_BYTE, GL_SHORT, GL_UNSIGNED_SHORT, GL_INT, GL_UNSIGNED_INT,
     *  GL_FLOAT, or GL_DOUBLE are accepted. The initial value is GL_FLOAT.
     */
    GLenum type;

    /**
     *  Whether fixed-point data values should be normalized (GL_TRUE) or
     *  converted directly as fixed-point values (GL_FALSE) when they are
     *  accessed.
     */
    GLboolean normalized;

    /**
     *  Byte offset between consecutive generic vertex attributes. If stride is
     *  0, the generic vertex attributes are understood to be tightly packed in
     *  the array. The initial value is 0.
     */
    GLsizei stride;

    /**
     *  Pointer to the first component of the first attribute element in the
     *  array.
     */
    GLvoid * pointer;

    /** Pointer to the function that enable this attribute. */
    void ( * enable )(void *);

} vertex_attribute_t;



/**
 * Generic vertex buffer.
 */
typedef struct
{
    /** Format of the vertex buffer. */
    char * format;

    /** Vector of vertices. */
    vector_t * vertices;

    /** GL identity of the vertices buffer. */
    GLuint vertices_id;

    /** Vector of indices. */
    vector_t * indices;

    /** GL identity of the indices buffer. */
    GLuint indices_id;

    /** GL primitives to render. */
    GLenum mode;

    /** Whether the vertex buffer needs to be uploaded to GPU memory. */
    char dirty;

    /** Individual items */
    vector_t * items;

    /** Array of attributes. */
    vertex_attribute_t *attributes[MAX_VERTEX_ATTRIBUTE];
} vertex_buffer_t;


/**
 * Creates an empty vertex buffer.
 *
 * @param  format a string describing vertex format.
 * @return        an empty vertex buffer.
 */
  vertex_buffer_t *
  vertex_buffer_new( const char *format );


/**
 * Creates a vertex buffer from data.
 *
 * @param  format   a string describing vertex format.
 * @param  vcount   number of vertices
 * @param  vertices raw vertices data
 * @param  icount   number of vertices
 * @param  indices  raw indices data
 * @return          an empty vertex buffer.
 */
  vertex_buffer_t *
  vertex_buffer_new_from_data( const char *format,
                               size_t vcount,
                               void * vertices,
                               size_t icount,
                               GLuint * indices );


/**
 * Deletes vertex buffer and releases GPU memory.
 *
 * @param  self  a vertex buffer
 */
  void
  vertex_buffer_delete( vertex_buffer_t * self );


/**
 *  Returns the number of items in the vertex buffer
 *
 *  @param  self  a vertex buffer
 *  @return       number of items
 */
  size_t
  vertex_buffer_size( const vertex_buffer_t *self );

/**
 *  Returns vertex format
 *
 *  @param  self  a vertex buffer
 *  @return       vertex format
 */
  const char *
  vertex_buffer_format( const vertex_buffer_t *self );

/**
 * Print information about a vertex buffer
 *
 * @param  self  a vertex buffer
 */
  void
  vertex_buffer_print( vertex_buffer_t * self );


/**
 * Immediate draw
 *
 * @param  self  a vertex buffer
 * @param  mode  render mode
 * @param  what  attributes to be rendered
 */
  void
  vertex_buffer_draw ( const char * format,
                       const GLenum mode,
                       const void * vertices,
                       const size_t count );


/**
 * Immediate draw with indexed vertices
 *
 * @param  self  a vertex buffer
 * @param  mode  render mode
 * @param  what  attributes to be rendered
 */
  void
  vertex_buffer_draw_indexed ( const char * format,
                               const GLenum mode,
                               const void * vertices,
                               const size_t vcount,
                               const GLuint * indices,
                               const size_t icount );


/**
 * Prepare vertex buffer for render.
 *
 * @param  self  a vertex buffer
 * @param  mode  render mode
 * @param  what  attributes to be rendered
 */
  void
  vertex_buffer_render_setup ( vertex_buffer_t *self,
                               GLenum mode, const char *what );

/**
 * Finish rendering by setting back modified states
 *
 * @param  self  a vertex buffer
 */
  void
  vertex_buffer_render_finish ( vertex_buffer_t *self );


/**
 * Render vertex buffer.
 *
 * @param  self  a vertex buffer
 * @param  mode  render mode
 * @param  what  attributes to be rendered
 */
  void
  vertex_buffer_render ( vertex_buffer_t *self,
                         GLenum mode, const char *what );


/**
 * Render a specified item from the vertex buffer.
 *
 * @param  self   a vertex buffer
 * @param  index index of the item to be rendered 
 */
  void
  vertex_buffer_render_item ( vertex_buffer_t *self,
                              size_t index );

/**
 * Upload buffer to GPU memory.
 *
 * @param  self  a vertex buffer
 */
  void
  vertex_buffer_upload( vertex_buffer_t *self );


/**
 * Clear all vertices and indices
 *
 * @param  self  a vertex buffer
 */
  void
  vertex_buffer_clear( vertex_buffer_t *self );



/**
 * Appends indices at the end of the buffer.
 *
 * @param  self     a vertex buffer
 * @param  indices  indices to be appended
 * @param  icount   number of indices to be appended
 */
  void
  vertex_buffer_push_back_indices ( vertex_buffer_t *self,
                                    GLuint * indices,
                                    size_t icount );


/**
 * Appends vertices at the end of the buffer.
 *
 * @param  self     a vertex buffer
 * @param  vertices vertices to be appended
 * @param  vcount   number of vertices to be appended
 */
  void
  vertex_buffer_push_back_vertices ( vertex_buffer_t *self,
                                     void * vertices,
                                     size_t vcount );

/**
 * Appends vertices at the end of the buffer.
 *
 * @param  self     a vertex buffer
 * @param  vertices vertices to be appended
 * @param  vcount   number of vertices to be appended
 * @param  indices  indices to be appended
 * @param  icount   number of indices to be appended
 */
  void
  vertex_buffer_push_back_data ( vertex_buffer_t *self,
                                 void * vertices,
                                 size_t vcount,
                                 GLuint * indices,
                                 size_t icount );


/**
 * Insert indices in the buffer.
 *
 * @param  self    a vertex buffer
 * @param  index   location before which to insert indices
 * @param  indices indices to be appended
 * @param  count   number of indices to be appended
 */
  void
  vertex_buffer_insert_indices ( vertex_buffer_t *self,
                                 size_t index,
                                 GLuint *indices,
                                 size_t count );


/**
 * Insert vertices in the buffer.
 *
 * @param  self     a vertex buffer
 * @param  index    location before which to insert vertices
 * @param  vertices vertices to be appended
 * @param  count    number of vertices to be appended
 *
 * @note
 * Indices after index will be increased by count. 
 */
  void
  vertex_buffer_insert_vertices ( vertex_buffer_t *self,
                                  size_t index,
                                  void *vertices,
                                  size_t vcount );

/**
 * Erase indices in the buffer.
 *
 * @param  self   a vertex buffer
 * @param  first  the index of the first index to be erased
 * @param  last   the index of the last index to be erased
 */
  void
  vertex_buffer_erase_indices ( vertex_buffer_t *self,
                                size_t first,
                                size_t last );

/**
 * Erase vertices in the buffer.
 *
 * @param  self   a vertex buffer
 * @param  first  the index of the first vertex to be erased
 * @param  last   the index of the last vertex to be erased
 */
  void
  vertex_buffer_erase_vertices ( vertex_buffer_t *self,
                                 size_t first,
                                 size_t last );


/**
 * Append a new item to the collection.
 *
 * @param  index    location before which to insert item
 * @param  vcount   number of vertices
 * @param  vertices raw vertices data
 * @param  icount   number of indices
 * @param  indices  raw indices data
 */
  void
  vertex_buffer_append( vertex_buffer_t * self,
                        void * vertices, size_t vcount,  
                        GLuint * indices, size_t icount );


/**
 * Insert a new item into the collection.
 *
 * @param  self      a collection
 * @param  index     location before which to insert item
 * @param  vertices  raw vertices data
 * @param  vcount    number of vertices
 * @param  indices   raw indices data
 * @param  icount    number of indices
 */
  void
  vertex_buffer_insert( vertex_buffer_t * self,
                        size_t index,
                        void * vertices, size_t vcount,  
                        GLuint * indices, size_t icount );
/** @} */


/**
 * Create an attribute from the given parameters.
 *
 * @param target     client-side capability
 * @param index      index of the generic vertex attribute to be modified.
 * @param size       number of component
 * @param type       data type
 * @param normalized Whether fixed-point data values should be normalized
                     (GL_TRUE) or converted directly as fixed-point values
                     (GL_FALSE) when they are  accessed.
 * @param stride     byte offset between consecutive attributes.
 * @param pointer    pointer to the first component of the first attribute
 *                   element in the array.
 * @return           a new initialized vertex attribute.
 */
vertex_attribute_t *
vertex_attribute_new( GLenum target,
                      GLuint index,
                      GLint size,
                      GLenum type,
                      GLboolean normalized,
                      GLsizei stride,
                      GLvoid *pointer );


/**
 * Create an attribute from the given description.
 *
 * @param  format Format string specifies the format of a vertex attribute.
 * @return        an initialized vertex attribute
 *
 */
  vertex_attribute_t *
  vertex_attribute_parse( char *format );


/**
 * Enable the position vertex attribute.
 *
 * @param  attr a vertex attribute
 */
  void
  vertex_attribute_position_enable( vertex_attribute_t *attr );


/**
 * Enable the normal vertex attribute.
 *
 * @param  attr a vertex attribute
 */
  void
  vertex_attribute_normal_enable( vertex_attribute_t *attr );


/**
 * Enable the color vertex attribute.
 *
 * @param attr  a vertex attribute
 */
  void
  vertex_attribute_color_enable( vertex_attribute_t *attr );


/**
 * Enable the texture vertex attribute.
 *
 * @param attr  a vertex attribute
 */
  void
  vertex_attribute_tex_coord_enable( vertex_attribute_t *attr );


/**
 * Enable the fog vertex attribute.
 *
 * @param attr  a vertex attribute
 */
  void
  vertex_attribute_fog_coord_enable( vertex_attribute_t *attr );


/**
 * Enable the edge flag vertex attribute.
 *
 * @param attr  a vertex attribute
 */
  void
  vertex_attribute_edge_flag_enable( vertex_attribute_t *attr );


/**
 * Enable the secondary color vertex attribute.
 *
 * @param attr  a vertex attribute
 */
  void
  vertex_attribute_secondary_color_enable( vertex_attribute_t *attr );

/**
 * Enable a generic vertex attribute.
 *
 * @param attr  a vertex attribute
 */
  void
  vertex_attribute_generic_attribute_enable( vertex_attribute_t *attr );


/**
 * Returns the GL enum type correspond to given character.
 *
 * @param ctype  character type
 * @return       GL enum type
 */
  GLenum
  GL_TYPE( char ctype );


/**
 * Get the GL name of the given target.
 *
 * @param  ctarget  a char describing target ( one of v,c,e,f,n,s,t)
 * @return          the associated GL target
 */
  GLenum
  GL_VERTEX_ATTRIBUTE_TARGET( char ctarget );


/**
 * Returns the size of a given GL enum type.
 *
 * @param  gtype a GL enum type
 * @return       the size of the given type
 */
  GLuint
  GL_TYPE_SIZE( GLenum gtype );


/**
 * Returns the literal string of given GL enum type.
 *
 * @param  gtype a GL enum type
 * @return       the literal string describing the type
 */
  const char *
  GL_TYPE_STRING( GLenum gtype );

/** @} */

#endif /* __VERTEX_BUFFER_H__ */
