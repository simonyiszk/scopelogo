
import sys
from math import sqrt, sin, cos
import numpy as np
import time
import pdb

def display(points):
    data = points.reshape(points.shape[0]*points.shape[1])
    data = data + 1
    data *= 128
    data = data.astype(int)
    data = np.maximum(0, np.minimum(255, data))
    binary = bytearray(list(data))
    sys.stdout.buffer.write(binary)

line_speed = 300
samp_rate = 48000
def line(p1, p2):
    step = line_speed / samp_rate
    l = np.linalg.norm(p1-p2)
    if l < step:
        return np.stack((p1, p2))
    space = np.linspace(0, 1, num=l//step)
    space = space.reshape(space.shape[0], 1)
    points = np.dot(space, p1.reshape(1,p1.shape[0])) + np.dot(1-space, p2.reshape(1, p2.shape[0]))
    #pdb.set_trace()
    return points

lines3d = [
        (np.array((0, 0, 0, 1)), np.array((1, 0, 0, 1))),
        (np.array((1, 0, 0, 1)), np.array((1, 1, 0, 1))),
        (np.array((1, 1, 0, 1)), np.array((0, 1, 0, 1))),
        (np.array((0, 1, 0, 1)), np.array((0, 0, 0, 1))),

        (np.array((0, 0, 1, 1)), np.array((1, 0, 1, 1))),
        (np.array((1, 0, 1, 1)), np.array((1, 1, 1, 1))),
        (np.array((1, 1, 1, 1)), np.array((0, 1, 1, 1))),
        (np.array((0, 1, 1, 1)), np.array((0, 0, 1, 1))),

        (np.array((0, 0, 0, 1)), np.array((0, 0, 1, 1))),
        (np.array((1, 1, 0, 1)), np.array((1, 1, 1, 1))),
        (np.array((1, 0, 0, 1)), np.array((1, 0, 1, 1))),
        (np.array((0, 1, 0, 1)), np.array((0, 1, 1, 1))),
]

pers_mat = 0.2*np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
    ])

rot_mat = np.array([
    [1, 0, 0, 0],
    [0, cos(0.75), -sin(0.75), 0],
    [0, sin(0.75), cos(0.75), 0],
    [0, 0, 0, 1]
    ])
rot_mat2 = np.array([
    [cos(0.2), 0, sin(0.2), 0],
    [0, 1, 0, 0],
    [-sin(0.2), 0, cos(0.2), 0],
    [0, 0, 0, 1]
    ])


while True:
    t = time.monotonic()
    rotx = t
    roty = 0.5* t
    rot_mat = np.array([
        [1, 0, 0, 0],
        [0, cos(rotx), -sin(rotx), 0],
        [0, sin(rotx), cos(rotx), 0],
        [0, 0, 0, 1]
        ])
    rot_mat2 = np.array([
        [cos(roty), 0, sin(roty), 0],
        [0, 1, 0, 0],
        [-sin(roty), 0, cos(roty), 0],
        [0, 0, 0, 1]
        ])
    trf = np.dot(np.dot(rot_mat, rot_mat2), pers_mat)
    lines2d = [(np.dot(s, trf), np.dot(e, trf)) for s, e in lines3d]
    for s, e in lines2d:
        display(line(s[:2],e[:2]))
