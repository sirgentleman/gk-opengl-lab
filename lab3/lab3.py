#!/usr/bin/env python3
import sys
import numpy as np
import math, random
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

# liczba punktow jajka
N = 20
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

def generate_egg_vertices(N, offset):
    
    distance = 1.0/(N-1)
    vertices = np.zeros((N, N, 3))

    for i in range(0, N):
        for j in range(0, N):
            u = distance*i
            v = distance*j
            vertices[i][j][0] = (-90*pow(u,5) + 225*pow(u,4) - 270*pow(u,3) + 180*pow(u,2) - 45*u) * math.cos(math.pi * v) + offset[0]
            vertices[i][j][1] = 160 * pow(u,4) - 320 * pow(u,3) + 160 * pow(u,2) + offset[1]
            vertices[i][j][2] = (-90*pow(u,5) + 225*pow(u,4) - 270*pow(u,3) + 180*pow(u,2) - 45*u) * math.sin(math.pi * v) + offset[2]
    
    return vertices

# FUNKCJA NA ZADANIE 3.0
def draw_egg_points(vertices, N):
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_POINTS)
    for i in range(0, N):
        for j in range(0, N):
            glVertex(vertices[i][j])
    glEnd()

# FUNKCJA NA ZADANIE 3.5
def draw_egg_lines(vertices, N):
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINES)
    for i in range(0, N-1):
        for j in range(0, N-1):
            glVertex(vertices[i][j])
            glVertex(vertices[i+1][j])
            glVertex(vertices[i][j])
            glVertex(vertices[i][j+1])
    glEnd()

# FUNKCJA NA ZADANIE 4.0
def draw_egg_triangles(vertices, N):
    colors = generate_colors(N)
    glBegin(GL_TRIANGLES)
    for i in range(0, N-1):
        for j in range(0, N-1):
            glColor3f(colors[i][j][0], colors[i][j][1], colors[i][j][2])
            glVertex(vertices[i][j])
            glColor3f(colors[i+1][j][0], colors[i+1][j][1], colors[i+1][j][2])
            glVertex(vertices[i+1][j])
            glColor3f(colors[i][j+1][0], colors[i][j+1][1], colors[i][j+1][2])
            glVertex(vertices[i][j+1])
            glColor3f(colors[i+1][j+1][0], colors[i+1][j+1][1], colors[i+1][j+1][2])
            glVertex(vertices[i+1][j+1])
            glColor3f(colors[i+1][j][0], colors[i+1][j][1], colors[i+1][j][2])
            glVertex(vertices[i+1][j])
            glColor3f(colors[i][j+1][0], colors[i][j+1][1], colors[i][j+1][2])
            glVertex(vertices[i][j+1])
    glEnd()

# FUNKCJA NA ZADANIE 4.5
def draw_egg_strip(vertices, N):
    colors = generate_colors(N)
    for i in range(0, N-1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(0, N):
            glColor3f(colors[i][j][0], colors[i][j][1], colors[i][j][2])
            glVertex(vertices[i][j])
            glColor3f(colors[i+1][j][0], colors[i+1][j][1], colors[i+1][j][2])
            glVertex(vertices[i+1][j])
        glEnd()
    
# generowanie kolorow, aby nie pojawial sie efekt migotania tylko ladne zlewanie
def generate_colors(N):
    np.random.seed(seed)
    colors = np.random.random((N, N, 3))
    for i in range(0, N):
        colors[i][0][0] = colors[N-i-1][N-1][0]
        colors[i][0][1] = colors[N-i-1][N-1][1]
        colors[i][0][2] = colors[N-i-1][N-1][2]
    return colors

def render(N, vertices, time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 180 / math.pi)

    axes()
    draw_egg_strip(vertices, N)
    #draw_egg_triangles(vertices, N)
    #draw_egg_lines(vertices, N)
    #draw_egg_points(vertices, N)
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
    vertices = generate_egg_vertices(N, [0, -4.5, 0])   # offset potrzebny aby ustawic jajko na srodku
    while not glfwWindowShouldClose(window):
        render(N, vertices, glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()