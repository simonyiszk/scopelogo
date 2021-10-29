import sys
from math import sqrt
from xml.dom import minidom
import regex as re
from svg.path import parse_path

def parse_poly(s):
  splitter = re.compile('''\s+''')
  points = list(map(float, splitter.split(s.replace(",", " ").strip())))
  return [(points[i], points[i+1]) for i in range(0,len(points), 2)]
        
def parse_svg(fn):
    doc = minidom.parse(fn)  # parseString also exists
    path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
    polygon_strings = [p.getAttribute('points') for p in doc.getElementsByTagName('polygon')]
    doc.unlink()
    return [parse_poly(s) for s in polygon_strings], [parse_path(s) for s in path_strings]

def loop(data):
    bindata = [int(255*x) for x in data]
    bindata = [max(0, min(255, x)) for x in bindata]
    while True:
        arr = bytearray(bindata)
        sys.stdout.buffer.write(arr)

def interlace(data1, data2):
    return [v for pair in zip(data1, data2) for v in pair]

def loop_interlace(data1, data2):
    loop(interlace(data1, data2))

line_speed = 300000
samp_rate = 192000
def line(x1, y1, x2, y2):
    step = line_speed / samp_rate
    l = sqrt((x1-x2)**2 + (y1-y2)**2)
    if l < step:
        return [(x1, y1), (x2, y2)]
    step_x = (x2-x1)/(l/step)
    step_y = (y2-y1)/(l/step)
    points = [(x1+i*step_x, y1+i*step_y) for i in range(int(l/step))]
    return zip(*points)

def poly(points):
    xs = []
    ys = []
    for tpl in zip(points, points[1:]):
        line_x, line_y = line(tpl[0][0], tpl[0][1], tpl[1][0], tpl[1][1])
        xs += line_x
        ys += line_y
    line_x, line_y = line(points[-1][0], points[-1][1], points[0][0], points[0][1])
    xs += line_x
    ys += line_y
    return xs, ys

def path(p):
    step = line_speed / samp_rate
    points = []
    for elem in p:
        l = elem.length()
        if l < step:
            points += [(elem.start.real, elem.start.imag), (elem.end.real, elem.end.imag)]
        else:
            n_steps = int(l/step)
            for i in range(n_steps):
                p = elem.point(float(i)/n_steps)
                points.append((p.real, p.imag))
    return zip(*points)

def rescale(coords, scale):
    return [x/scale for x in coords]

def scopelogo(filepath):
    polys, paths = parse_svg(filepath)
    all_shapes = [(p, 'poly') for p in polys] + [(p, 'path') for p in paths]
    x = []
    y = []
    for shape, type in all_shapes:
        px, py = {"poly":poly, "path":path}[type](shape)
        x += px
        y += py

    x = rescale(x, 1500)
    y = rescale(y, 1000)
    loop_interlace(x, y)

if __name__=="__main__":
    import sys
    scopelogo(sys.argv[1])
