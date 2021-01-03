#!/usr/bin/env python3
import sys, math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0
R_param = 5

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

light1_ambient = [0.0, 0.0, 0.2, 1.0]
light1_diffuse = [0.0, 0.0, 0.8, 1.0]
light1_specular = [0.0, 0.0, 1.0, 1.0]
light1_position = [5.0, 5.0, 5.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

# NOWE ZMIENNE

change_mode = 0 # 0 - mat_ambient | 1 - mat_diffuse | 2 - mat_specular | 3 - light_ambient | 4 - light_diffuse | 5 - light_specular

cur_mat_ambient = mat_ambient
cur_mat_diffuse = mat_diffuse
cur_mat_specular = mat_specular

cur_light_ambient = light_ambient
cur_light_diffuse = light_diffuse
cur_light_specular = light_specular
#cur_light_position = [0.0, 0.0, 10.0, 1.0]

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    # Second light source
    
    #glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
    #glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
    #glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)
    #glLightfv(GL_LIGHT1, GL_POSITION, light1_position)

    #glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    #glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    #glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)


    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)


def shutdown():
    pass


def render(time):
    global theta, phi

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    theta = abs(theta%360)
    phi = abs(phi%360)

    #glRotatef(theta, 0.0, 1.0, 0.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    x = R_param*math.cos(math.radians(theta))*math.cos(math.radians(phi))
    y = R_param*math.sin(math.radians(phi))
    z = R_param*math.sin(math.radians(theta))*math.cos(math.radians(phi))

    glTranslate(x,y,z)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)
    glLightfv(GL_LIGHT0, GL_POSITION, [x,y,z,1.0])
    glTranslate(-x,-y,-z)

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def change_color(color, isUp):
    global cur_light_ambient, cur_light_diffuse, cur_light_specular, cur_mat_ambient, cur_mat_diffuse, cur_mat_specular

    light_type = {0: GL_AMBIENT, 1: GL_DIFFUSE, 2: GL_SPECULAR}
    cur_value = {0: cur_mat_ambient, 1: cur_mat_diffuse, 2: cur_mat_specular, 3: cur_light_ambient, 4: cur_light_diffuse, 5: cur_light_specular}
    
    if isUp == True:
        cur_value[change_mode][color] = cur_value[change_mode][color]+0.1 if cur_value[change_mode][color]+0.1 <= 1.0 else 1.0
    else:
        cur_value[change_mode][color] = cur_value[change_mode][color]-0.1 if cur_value[change_mode][color]-0.1 >= 0.0 else 0

    if change_mode < 3:
        glMaterialfv(GL_FRONT, light_type[change_mode], cur_value[change_mode])
    else:
        glLightfv(GL_LIGHT0, light_type[change_mode-3], cur_value[change_mode])

    print(cur_value[change_mode])

# TODO: Change it to dictionary??
def keyboard_key_callback(window, key, scancode, action, mods):
    global change_mode
    
    if action == GLFW_PRESS:
        if key == GLFW_KEY_ESCAPE:
            glfwSetWindowShouldClose(window, GLFW_TRUE)
        elif key == GLFW_KEY_1:
            change_mode = 0
        elif key == GLFW_KEY_2:
            change_mode = 1
        elif key == GLFW_KEY_3:
            change_mode = 2
        elif key == GLFW_KEY_4:
            change_mode = 3
        elif key == GLFW_KEY_5:
            change_mode = 4
        elif key == GLFW_KEY_6: 
            change_mode = 5
        elif key == GLFW_KEY_Q:
            change_color(0, True)
        elif key == GLFW_KEY_A:
            change_color(0, False)
        elif key == GLFW_KEY_W:
            change_color(1, True)
        elif key == GLFW_KEY_S:
            change_color(1, False)
        elif key == GLFW_KEY_E:
            change_color(2, True)
        elif key == GLFW_KEY_D:
            change_color(2, False)



def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global delta_y
    global mouse_x_pos_old
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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
