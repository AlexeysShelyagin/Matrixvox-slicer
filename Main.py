import random
import numpy as np
from Fonts import font

f = open('Rain.txt', 'w')

f.write('[\n')

frames = 240
h = 16

def print_frame(frame):
    f.write('   [\n')
    for i in range(h):
        f.write('       [\n')
        for j in range(8):
            f.write('           ')
            f.write(bin(frame[i][j]))
            f.write(',\n')

        f.write('       ],\n')
    f.write('    ],\n')

cube = []
def clear_cube():
    cube = []
    for i in range(h):
        cube.append([])
        for j in range(8):
            cube[i].append(0b00000000)
    return cube

layer = []

def rain():
    cube = clear_cube()
    for k in range(frames):
        cube.pop()
        layer = [0]*8
        for i in range(8):
            for j in range(8):
                layer[i] = (layer[i] << 1) | int(random.randint(0, 12) == 1)
        cube.insert(0, layer)
        print_frame(cube)

def plane():
    for k in range(frames):
        layer = [0]*8
        for i in range(8):
            layer[i] = (1 << (k % 8))
        for i in range(h):
            cube.insert(i, layer)
        print_frame(cube)

def sinusoid():
    for k in range(frames):
        cube = clear_cube()
        for i in range(8):
            sin_h = round(np.sin(np.pi*(i + k)/4)*3 + 5)
            cube[sin_h][i] = 0b00011000
            #cube[sin_h][(i + 4) % 8] = 0b00000110
        print_frame(cube)

def walking_cube():
    vec_x = random.randint(5, 10) / 5
    vec_y = random.randint(5, 10) / 5
    vec_z = random.randint(10, 20) / 5
    if random.randint(0, 1) == 1:
        vec_x = -vec_x
    if random.randint(0, 1) == 1:
        vec_y = -vec_y
    if random.randint(0, 1) == 1:
        vec_z = -vec_z
    
    cube_x = 4
    cube_y = 4
    cube_z = 8

    for k in range(frames):
        cube = clear_cube()
        cube[round(cube_z)][round(cube_x)] = (1 << round(cube_y))
        if round(cube_z) != 0:
            cube[round(cube_z) - 1][round(cube_x)] = (1 << round(cube_y))
        print_frame(cube)

        cube_x += vec_x
        cube_y += vec_y
        cube_z += vec_z

        if round(cube_x) >= 7 or round(cube_x) <= 0:
            vec_x = -vec_x
            if cube_x < 0:
                cube_x = 0
            if cube_x > 7:
                cube_x = 7
        if round(cube_y) >= 7 or round(cube_y) <= 0:
            vec_y = -vec_y
            if cube_y < 0:
                cube_y = 0
            if cube_y > 7:
                cube_y = 7
        if round(cube_z) >= h-1 or round(cube_z) <= 0:
            vec_z = -vec_z
            if cube_z < 0:
                cube_z = 0
            if cube_z > h-1:
                cube_z = h-1

def circlesoid():
    for k in range(frames):
        cube = clear_cube()
        for i in range(8):
            for j in range(8):
                l = np.sqrt((i-3)**2 + (j-3)**2)
                sin_h = round(np.sin(np.pi*(l + k // 2)/4)*3 + 6)
                cube[sin_h][i] = (1 << j) | (1 << (7 - j))
        print_frame(cube)

def text(txt):
    for k in range(frames):
        cube = clear_cube()
        letter = txt[min(k // 8, len(txt) - 1)]
        for i in range(h):
            for j in range(8):
                cube[i][7 - j] = cube[i][7 - j] | (font[letter][i][j] << (k % 8))
        print_frame(cube)

#text('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
#walking_cube()
rain()

f.write(']')