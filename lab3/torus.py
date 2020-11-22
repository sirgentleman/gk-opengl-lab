#!/usr/bin/env python3
import sys
import numpy as np
import math, random
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


torus = 40  # liczba generowanych torusow
N = 15      # liczba "punktow" w torusie (od 10 w dol zaczyna być coraz bardziej "kwadratowy")
R = 0.3     # zewnetrzny promien torusa
r = 0.1    # wewnetrzny promien torusa
seed = random.randint(0, 2**32-1)

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

# funkcja generujaca punkty dla torusa (blizniaca funkcja jak przy jajku)
def generate_torus_vertices():
    distance = 1.0/(N-1)
    vertices = np.zeros((N, N, 3))

    for i in range(0, N):
        for j in range(0, N):
            u = distance*i
            v = distance*j
            vertices[i][j][0] = (R + r*math.cos(2*math.pi*v))*math.cos(2*math.pi*u)
            vertices[i][j][1] = (R + r*math.cos(2*math.pi*v))*math.sin(2*math.pi*u)
            vertices[i][j][2] = r*math.sin(2*math.pi*v)
    return vertices
    
# funkcja rysujaca torusa za pomoca GL_TRIANGLE_STRIP (blizniacza do jajka)
def draw_torus(vertices, offset):
    for i in range(0, N-1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(0, N):
            glColor3f(j%2, 0, 1)
            glVertex(np.add(vertices[i][j], offset))
            glColor3f(j%2, 0, 1)
            glVertex(np.add(vertices[i+1][j], offset))
        glEnd()

# funkcja sluzaca do wygenerowania danych na temat krzywej, w tym waznego dla nas kąta (info[i][2])
def generate_curve_info(torusAmount):
    info = np.zeros((torusAmount,3))
    for i in range(0,torusAmount):
        # /4 aby toursy byly gesciej poukladane
        info[i][0] = i/4
        # funkcja wedlug ktorej torusy maja sie uklada (tutaj odpowiednio sparametryzowana sinusoida)
        info[i][1] = 4*math.sin(1.5*info[i][0])
        if i is not 0:
            # wyliczanie kata jaki przyjmie nastepny torus (arctan z x/y)
            info[i][2] = math.atan(info[i][1]/info[i][0])*(180/math.pi)
        else:
            info[i][2] = 0
    return info

def render(curveInfo, vertices, time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 180 / math.pi)
    axes()
    current_degree = 0
    for i in range(torus):
        glRotatef(curveInfo[i][2] - current_degree, 0, 1, 0)
        if i%2 == 0:
           glRotatef(90, 1, 0, 0)
        glTranslatef((5*R/4), 0, 0)
        draw_torus(vertices, [0,0,0])
        if i%2 == 0:
           glRotatef(-90, 1, 0, 0)
        current_degree = curveInfo[i][2]
    glFlush()

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    vertices = generate_torus_vertices()
    curveInfo = generate_curve_info(torus)
    while not glfwWindowShouldClose(window):
        render(curveInfo, vertices, glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()