#!/usr/bin/env python3
import sys
import random
import time

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

viewport_width = 1000
viewport_height = 1000
rand_seed = time.time()

def startup():
    update_viewport(None, viewport_width, viewport_height)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

def drawRectangle(x, y, a, b, d=0.0):
    color = [random.random(), random.random(), random.random()]
    color1 = [random.random(), random.random(), random.random()]
    color2 = [random.random(), random.random(), random.random()]
    color3 = [random.random(), random.random(), random.random()]

    glBegin(GL_TRIANGLES)
    glColor(color)
    glVertex2f(x-((a+d)/2), y-((b+d)/2))
    glColor(color2)
    glVertex2f(x-((a+d)/2), y+((b-d)/2))
    glColor(color1)
    glVertex2f(x+((a-d)/2), y+((b-d)/2))
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor(color)
    glVertex2f(x-((a+d)/2), y-((b+d)/2))
    glColor(color3)
    glVertex2f(x+((a-d)/2), y-((b+d)/2))
    glColor(color1)
    glVertex2f(x+((a-d)/2), y+((b-d)/2))
    glEnd()

def drawCarpet(x, y, a, b, level):
    random.seed((x+a+rand_seed)*(y+1)*level/b)
    level -= 1
    if(level == 0):
        drawRectangle(x, y, a, b, a*(random.random()/2))
        return
    new_a = a/3
    new_b = b/3
    drawCarpet(x-new_a, y, new_a, new_b, level)
    drawCarpet(x+new_a, y, new_a, new_b, level)

    drawCarpet(x-(new_a), y+new_b, new_a, new_b, level)
    drawCarpet(x, y+new_a, new_a, new_b, level)
    drawCarpet(x+new_a, y+new_b, new_a, new_b, level)

    drawCarpet(x-new_a, y-new_b, new_a, new_b, level)
    drawCarpet(x, y-new_b, new_a, new_b, level)
    drawCarpet(x+new_a, y-new_b, new_a, new_b, level)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    drawCarpet(0,0,100,100, int(sys.argv[1]))

    glFlush()


def update_viewport(window, width, height):

    global rand_seed
    rand_seed = time.time()

    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspectRatio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


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

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main() 
