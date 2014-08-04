# -*- coding: utf-8; -*-
from math import sin, cos, sqrt, degrees, radians
from calc import calc_angle

def tracer(par, x1, y1, x2, y2, snap_s, angle_s):
    angle = None
    x3 = x2
    y3 = y1
    i = 1
    j = 1
    if x2>x1:
        i = 1
    elif x2<x1:
        i = -1
    if y2>y1:
        j = 1
    elif y2<y1:
        j = -1
    if x1 == x2:
        angle = 90.0
    if y1 == y2:
        angle = 0.0
    if (x1, y1) == (x2, y2):
        return
    if angle == None:
        angle = abs(degrees(calc_angle(x1, y1, x3, y3, x2, y2)))
    a = 0
    d = sqrt((x2-x1)**2 + (y2-y1)**2)
    while angle_s*a <= 90.0:
        if abs(angle)-snap_s/6.0 <= abs(angle_s*a) <= abs(angle)+snap_s/6.0:
            xi = cos(radians(angle_s*a))*d*10000.0*i + x1
            yi = sin(radians(angle_s*a))*d*10000.0*j + y1
            if 'trace' in par.ALLOBJECT:
                par.c.delete('text')
                par.c.create_text(x2+snap_s*2, y2+snap_s*2, fill = 'yellow', text = str(angle_s*a), tags = ('obj', 'trace', 'text'))
                a = None
                break
            else:
                id = par.c.create_line(x1, y1, xi, yi, fill = 'yellow', width = 1, tags = ('obj', 'trace'))
                par.c.create_text(x2+snap_s*2, y2+snap_s*2, fill = 'yellow', text = str(angle_s*a), tags = ('obj', 'trace', 'text'))

                id_dict = {id:('line', 'priv')}
                par.ALLOBJECT['trace'] = {'id':id_dict}
                a = None
                break
        else:
            a += 1
    if a != None and 'trace' in par.ALLOBJECT:
        par.c.delete('trace')
        del par.ALLOBJECT['trace']
