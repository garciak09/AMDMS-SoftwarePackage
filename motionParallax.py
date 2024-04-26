from graphics import graphics
import random

#Kevin Garcia
# CSC110
# This program creates a parallax where there is some landscape drawn using
# gui drawings and a canvas as well as motion parallax to make the
# drawings move according to the mouse position making it look like the camera
# angle is changing. There is also a line of birds that repeatedly fly across
# the screen.

def landscape(gui):
    '''This function creates the grass along with the grass blades, the tree,
    and the sun along with the parallax to make them move according to the positiion
    of the mouse. It takes one argument and thats the gui canvas.'''
    x_grass = (gui.mouse_x//100)
    y_grass= (gui.mouse_y//5)
    gui.rectangle(x_grass + -100, y_grass + 450, 750, 250, 'spring green')

    #blades of grass
    i = -50
    while i < 750:
        gui.line(x_grass + i, y_grass + 425, i, 800, 'spring green', 2)
        i += 5
    #tree
    x_tree = gui.mouse_x// 5
    y_tree = gui.mouse_y// 5
    gui.rectangle(x_tree + 400, y_tree + 480, 20, 50, 'brown4')
    gui.ellipse(x_tree + 410, y_tree + 450, 60, 95, 'forest green')

    x_sun = gui.mouse_x//50
    y_sun = gui.mouse_y//50
    #sun
    gui.ellipse(x_sun + 475, y_sun + 65, 100, 100, 'yellow')

def bird(gui, x):
    '''this function is a block of code used to lines to reate the birds.
    It takes two arguments, one of them being the gui canvas and the other
    is 'x' which is an int. X is used to make the birds transition from
    left to right in order to make it look like they are flying.'''

    gui.line(75 + x, 90, 100 + x, 105, 'black')
    gui.line(100 + x, 105, 120 + x, 90, 'black')
    gui.line(150 + x, 110, 175 + x, 125, 'black')
    gui.line(175 + x, 125, 195 + x, 110, 'black')
    gui.line(225 + x, 130, 250 + x, 145, 'black')
    gui.line(250 + x, 145, 270 + x, 130, 'black')
    gui.line(300 + x, 150, 325 + x, 165, 'black')
    gui.line(325 + x, 165, 345 + x, 150, 'black')
    gui.line(375 + x, 170, 400 + x, 185, 'black')
    gui.line(400 + x, 185, 420 + x, 170, 'black')





def main():
    '''This function is where I run most of the past functions except I
    decided to make it so the mountains and their color are created on
    here. I also made it so the birds will repeatedly go across the screen rather
    than only once. My gui canvas was created on here as well.'''

    gui = graphics(650, 650, 'Landscape')
    color_string1 = gui.get_color_string(random.randint(0,255),random.randint(0,255), random.randint(0,255))
    color_string2 = gui.get_color_string(random.randint(0,255), random.randint(0,255), random.randint(0,255))
    color_string3 = gui.get_color_string(random.randint(0,255), random.randint(0,255), random.randint(0,255))
    i = -50
    x = 0

    while True:
        x_mountains1 = gui.mouse_x//15
        y_mountains1 = gui.mouse_y//15
        x_mountains2 = gui.mouse_x//11
        y_mountains2 = gui.mouse_y//11
        gui.clear()
        gui.rectangle(-100,-100, 750, 750, 'light sky blue')
        gui.triangle(x_mountains2 + 325, y_mountains2 + 150, x_mountains2 + 25,
                     y_mountains2 + 700, x_mountains2 + 625, y_mountains2 + 700, color_string3)

        gui.triangle(x_mountains1 + 150, y_mountains1 + 200, x_mountains1 + -200,
                     y_mountains1 + 700, x_mountains1 + 500, y_mountains1 + 700, color_string1)

        gui.triangle(x_mountains1 + 500, y_mountains1 + 200, x_mountains1 +  150,
                     y_mountains1 + 700, x_mountains1 +  850, y_mountains1 + 700, color_string2)

        landscape(gui)
        bird(gui, x)

        if x >= 600:
            x = -500
        x += 5
        gui.update_frame(60)


main()