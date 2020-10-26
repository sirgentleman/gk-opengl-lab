#!/usr/bin/env python3
import sys
import numpy as np
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

viewport_width = 500
viewport_height = 500
max_iterations = 200
offset_x = -0.7
offset_y = 0
scale = 0.8
mouse_x = 0
mouse_y = 0

def startup():
    update_viewport(None, viewport_width, viewport_height)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

def np_mandelbrot(np_input):
    prev_z = np.zeros([viewport_width*2,viewport_height*2], dtype=complex)
    return_array = np.zeros([viewport_width*2,viewport_height*2], dtype=int)
    for i in range(1, max_iterations):
        prev_z = np.add(np.square(prev_z), np_input)
        temp = np.absolute(prev_z)
        return_array[np.less(temp,2)] = i
    return return_array

def drawSet(offset_x, offset_y, scale):
    glBegin(GL_POINTS)
    vertices = np.empty([viewport_width*2, viewport_height*2], dtype=complex)
    for x in range(-viewport_width,viewport_width):
        for y in range(-viewport_height, viewport_height):
            vertices[x,y] = np.complex(offset_x+(x/(scale*viewport_width)), offset_y+(y/(scale*viewport_height)))
    colors = np_mandelbrot(vertices)
    for x in range(-viewport_width,viewport_width):
        for y in range(-viewport_height, viewport_height):
            glColor3f((colors[x,y]/max_iterations), (colors[x,y]/max_iterations)-0.1, 0.1)
            glVertex2f(x,y)
    glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    drawSet(offset_x, offset_y, scale)
    glFlush()


def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    glOrtho(-viewport_width, viewport_width, -viewport_height, viewport_height,-1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    render(glfwGetTime())

def mouse_position_callback(window, x, y):
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = y

def zoom_in():
    print(mouse_x, mouse_y)
    global offset_x, offset_y, scale
    offset_x -= 2*(viewport_width/2-mouse_x)/scale/viewport_width
    offset_y += 2*(viewport_height/2-mouse_y)/scale/viewport_height
    scale *= 4

def zoom_out():
    print(mouse_x, mouse_y)
    global offset_x, offset_y, scale
    scale /= 6

def mouse_button_callback(window, button, action, mods):
    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        zoom_in()
    elif button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        zoom_out()
    render(glfwGetTime())


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(viewport_width, viewport_height, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSetCursorPosCallback(window, mouse_position_callback)

    startup()
    while not glfwWindowShouldClose(window):
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main() 
