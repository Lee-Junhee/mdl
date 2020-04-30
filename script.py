import mdl
import math
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1]
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    print(symbols)
    for command in commands:
        print(command)
        args = command['args']
        if command['op'] == 'sphere':
            polygons = []
            add_sphere(polygons, args[0], args[1], args[2],
                       args[3], step_3d)
            matrix_mult(stack[-1], polygons)
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, command['constants'])
        elif command['op'] == 'torus':
            polygons = []
            add_torus(polygons, args[0], args[1], args[2],
                      args[3], args[4], step_3d)
            matrix_mult(stack[-1], polygons)
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, command['constants'])
        elif command['op'] == 'box':
            polygons = []
            add_box(polygons,
                    args[0], args[1], args[2],
                    args[3], args[4], args[5])
            matrix_mult(stack[-1], polygons)
            draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, command['constants'])
        elif command['op'] == 'circle':
            edges = []
            add_circle(edges,
                       args[0], args[1], args[2],
                       args[3], step_3d)
            matrix_mult(stack[-1], edges)
            draw_lines(edges, screen, zbuffer, color)
        elif command['op'] in ['hermite', 'bezier']:
            edges = []
            add_curve(edges,
                      args[0], args[1],
                      args[2], args[3],
                      args[4], args[5],
                      args[6], args[7],
                      step, command['op'])
            matrix_mult(stack[-1], edges)
            draw_lines(edges, screen, zbuffer, color)
        elif command['op'] == 'line':
            edges = []
            add_edge(edges,
                     args[0], args[1], args[2],
                     args[3], args[4], args[5])
            matrix_mult(stack[-1], edges)
            draw_lines(edges, screen, zbuffer, color)
        elif command['op'] == 'scale':
            t = make_scale(args[0], args[1], args[2])
            matrix_mult(stack[-1], t)
            stack[-1] = [x[:] for x in t]
        elif command['op'] == 'move':
            t = make_translate(args[0], args[1], args[2])
            matrix_mult(stack[-1], t)
            stack[-1] = [x[:] for x in t]
        elif command['op'] == 'rotate':
            theta = args[1] * (math.pi / 180)
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult(stack[-1], t)
            stack[-1] = [x[:] for x in t]
        elif command['op'] == 'push':
            systems.append([x[:] for x in stack[-1]])
        elif command['op'] == 'pop':
            stack.pop()
        elif command['op'] in ['display', 'save']:
            if command['op'] == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])