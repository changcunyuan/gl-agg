#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut

def save(display_func, filename="screenshot.png"):
    """
    """

    try:
        import OpenGL.GL.EXT.framebuffer_object as fbo
    except ImportError:
        print 'You do not have the framebuffer extension on your video card'
        print 'Cannot save figure'
        return

    x,y,w,h = gl.glGetIntegerv(gl.GL_VIEWPORT)

    # Setup framebuffer
    framebuffer = fbo.glGenFramebuffersEXT(1)
    fbo.glBindFramebufferEXT( fbo.GL_FRAMEBUFFER_EXT, framebuffer)

    # Setup depthbuffer
    depthbuffer = fbo.glGenRenderbuffersEXT( 1 )
    fbo.glBindRenderbufferEXT( fbo.GL_RENDERBUFFER_EXT, depthbuffer )
    fbo.glRenderbufferStorageEXT( fbo.GL_RENDERBUFFER_EXT, gl.GL_DEPTH_COMPONENT, w, h)
    
    # Create texture to render to
    data = np.zeros((w,h,4), dtype=np.ubyte)
    texture = gl.glGenTextures(1)
    gl.glBindTexture( gl.GL_TEXTURE_2D, texture)
    gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexImage2D( gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, w, h, 0,
                     gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, data)
    fbo.glFramebufferTexture2DEXT( gl.GL_FRAMEBUFFER_EXT, gl.GL_COLOR_ATTACHMENT0_EXT,
                                   gl.GL_TEXTURE_2D, texture, 0)
    fbo.glFramebufferRenderbufferEXT( gl.GL_FRAMEBUFFER_EXT, gl.GL_DEPTH_ATTACHMENT_EXT, 
                                      gl.GL_RENDERBUFFER_EXT, depthbuffer)
    status = fbo.glCheckFramebufferStatusEXT( fbo.GL_FRAMEBUFFER_EXT )

    if status != fbo.GL_FRAMEBUFFER_COMPLETE_EXT:
        raise(RuntimeError, 'Error in framebuffer activation')

    display_func()
    glut.glutSwapBuffers()
    data = gl.glReadPixels (x,y,w,h, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE)

    from PIL import Image
    image = Image.fromstring('RGBA', (w,h), data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save (filename)

    # Cleanup
    fbo.glBindRenderbufferEXT( fbo.GL_RENDERBUFFER_EXT, 0 )
    fbo.glBindFramebufferEXT( fbo.GL_FRAMEBUFFER_EXT, 0 )
    gl.glDeleteTextures( texture )
    fbo.glDeleteFramebuffersEXT( [framebuffer,] )
