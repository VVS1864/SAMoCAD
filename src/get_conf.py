# -*- coding: utf-8 -*-
from math import sin, cos, degrees, radians
#Дать все параметры:     
def get_conf(obj, par):
    o = obj[0]
    if o == 'L':
        fill, width, sloy, stipple, coord = get_line_conf(obj, par)
        e = ['line', fill, width, sloy, stipple, coord]
    elif o == 'r':
        xc, yc, x1, y1, size, fill, text, sloy, s, vr_s, arrow_s, type_arrow, s_s_dim, w_text_dim, font_dim, R = get_dimR_conf(obj, par)
        e = ['dimr', xc, yc, x1, y1, size, fill, text, sloy, s, vr_s, arrow_s, type_arrow, s_s_dim, w_text_dim, font_dim, R]
    elif o == 'd':
        x1, y1, x2, y2, x3, y3, ort, size, fill, text, sloy, text_change, text_place, s, vr_s, vv_s, arrow_s, type_arrow, s_s_dim, w_text_dim, font_dim = get_dim_conf(obj, par)
        e = ['dim', x1, y1, x2, y2, x3, y3, ort, size, fill, text, sloy, text_change, text_place, s, vr_s, vv_s, arrow_s, type_arrow, s_s_dim, w_text_dim, font_dim]
    elif o == 'c':
        x0, y0, R, fill, width, sloy = get_circle_conf(obj, par)
        e = ['circle', x0, y0, R, fill, width, sloy]
    elif o == 'a':
        xc, yc, dx1, dy1, dx2, dy2, fill, width, sloy = get_arc_conf(obj, par)
        e = ['arc', xc, yc, dx1, dy1, dx2, dy2, fill, width, sloy]
    elif o == 't':
        fill, text, sloy, angle, anchor, size, line, coord, s_s, w_text, font = get_text_conf(obj, par)
        e = ['text', fill, text, sloy, angle, anchor, size, line, coord, s_s, w_text, font]
    return e

def get_circle_conf(obj, par):#Принимает объект - круг, возвращает все его свойства
    fill = par.ALLOBJECT[obj]['fill']
    width = par.ALLOBJECT[obj]['width']
    sloy = par.ALLOBJECT[obj]['sloy']
    find = par.ALLOBJECT[obj]['id']#par.c.find_withtag(obj)
    for i in find:
        tag = par.ALLOBJECT[obj]['id'][i]#par.c.gettags(i)
        if 'cir' in tag:
            coord = par.c.coords(i)
    x0 = (coord[0]+coord[2])/2.0
    y0 = (coord[1]+coord[3])/2.0
    R = (coord[3]-coord[1])/2.0
    return x0, y0, R, fill, width, sloy

def get_arc_conf(obj, par, _start = None,):#Принимает объект - дуга, возвращает все его свойства
    fill = par.ALLOBJECT[obj]['fill']
    width = par.ALLOBJECT[obj]['width']
    sloy = par.ALLOBJECT[obj]['sloy']
    for i in par.ALLOBJECT[obj]['id']:#par.c.find_withtag(obj):
        if 'a' in par.ALLOBJECT[obj]['id'][i]:#par.c.gettags(i):
            coord = par.c.coords(i)
            start = float(par.c.itemcget(i, 'start'))
            extent = float(par.c.itemcget(i, 'extent'))
            xc, yc, dx1, dy1, dx2, dy2 = get_arc_coord(coord[0], coord[1], coord[2], coord[3], start, extent)
    if _start:
        R = (coord[2]-coord[0])/2.0
        return xc, yc, dx1, dy1, dx2, dy2, start, extent, R, fill, width, sloy
    else:
        return xc, yc, dx1, dy1, dx2, dy2, fill, width, sloy
    
def get_arc_coord(x1, y1, x2, y2, start, extent):
    R = (x2-x1)/2.0
    xc = (x1+x2)/2.0
    yc = (y1+y2)/2.0
    mcos = cos(radians(start))#*math.pi/180.0)
    mcos2 = cos(radians(extent+start))#*math.pi/180.0)
    msin = sin(radians(start))#*math.pi/180.0)
    msin2 = sin(radians(extent+start))#*math.pi/180.0)
    dx1 = xc+R*mcos
    dy1 = yc-R*msin
    dx2 = xc+R*mcos2
    dy2 = yc-R*msin2
    return xc, yc, dx1, dy1, dx2, dy2


def get_line_conf(obj, par):#Принимает объект - линия, возвращает все его свойства
    fill = par.ALLOBJECT[obj]['fill']
    width = par.ALLOBJECT[obj]['width']
    sloy = par.ALLOBJECT[obj]['sloy']
    stipple = par.ALLOBJECT[obj]['stipple']
    for i in par.ALLOBJECT[obj]['id']: #par.c.find_withtag(obj):
        if 'lin' in par.ALLOBJECT[obj]['id'][i]:#all(x in par.ALLOBJECT[obj]['id'][i] for x in ('line', 'priv')):#par.c.gettags(i):
            coord = par.c.coords(i)
    return fill, width, sloy, stipple, coord

def get_line_coord(obj, par):#Принимает объект - линия, возвращает все его свойства
    for i in par.ALLOBJECT[obj]['id']:#par.c.find_withtag(obj):
        if all(x in par.ALLOBJECT[obj]['id'][i] for x in ('line', 'priv')):#par.c.gettags(i):
            coord = par.c.coords(i)
    return coord

def get_text_conf(obj, par):#Принимает объект - текст, возвращает все его свойства
    fill = par.ALLOBJECT[obj]['fill']
    text = par.ALLOBJECT[obj]['text']
    sloy = par.ALLOBJECT[obj]['sloy']
    angle = par.ALLOBJECT[obj]['angle']
    anchor = par.ALLOBJECT[obj]['anchor']
    size = par.ALLOBJECT[obj]['size']
    s_s = par.ALLOBJECT[obj]['s_s']
    w_text = par.ALLOBJECT[obj]['w_text']
    font = par.ALLOBJECT[obj]['font']
    line = par.get_snap_line(obj)[0]
    coord = par.c.coords(line)
    return fill, text, sloy, angle, anchor, size, line, coord, s_s, w_text, font

def get_dim_conf(obj, par):#Принимает объект - размер, возвращает все его свойства
    snap_line = par.get_snap_line(obj)
    line1 = snap_line[0]
    line2 = snap_line[1]
    line3 = snap_line[2]
    coord_list = map(lambda i: par.c.coords(i), [line1, line2, line3])
    x1 = coord_list[0][0]
    y1 = coord_list[0][1]
    x2 = coord_list[1][0]
    y2 = coord_list[1][1]
    x3 = coord_list[2][0]
    y3 = coord_list[2][1]
    ort = par.ALLOBJECT[obj]['ort']
    size = par.ALLOBJECT[obj]['size']
    fill = par.ALLOBJECT[obj]['fill']
    text = par.ALLOBJECT[obj]['text']
    sloy = par.ALLOBJECT[obj]['sloy']
    text_change = par.ALLOBJECT[obj]['text_change']
    s = par.ALLOBJECT[obj]['s']
    vr_s = par.ALLOBJECT[obj]['vr_s']
    vv_s = par.ALLOBJECT[obj]['vv_s']
    arrow_s = par.ALLOBJECT[obj]['arrow_s']
    type_arrow = par.ALLOBJECT[obj]['type_arrow']
    s_s_dim = par.ALLOBJECT[obj]['s_s_dim']
    w_text_dim = par.ALLOBJECT[obj]['w_text_dim']
    font_dim = par.ALLOBJECT[obj]['font_dim']

    if text_change in ['online3', 'changed', 'online3_m_l']:
        text_lines, priv_line, text_place = par.dim_text_place(obj)
    else:
        text_change = 'unchange'
        text_place = None
    #print 'xxxx', x1, y1, x2, y2, x3, y3, text_change, text_place,
    return x1, y1, x2, y2, x3, y3, ort, size, fill, text, sloy, text_change, text_place, s, vr_s, vv_s, arrow_s, type_arrow, s_s_dim, w_text_dim, font_dim

def get_dimR_conf(obj, par):#Принимает объект - размер, возвращает все его свойства
    
    line1 = par.get_snap_line(obj)[0]
    c = par.c.coords(line1)
    xc = c[0]
    yc = c[1]
    x1 = c[2]
    y1 = c[3]
    size = par.ALLOBJECT[obj]['size']
    fill = par.ALLOBJECT[obj]['fill']
    text = par.ALLOBJECT[obj]['text']
    sloy = par.ALLOBJECT[obj]['sloy']
    s = par.ALLOBJECT[obj]['s']
    vr_s = par.ALLOBJECT[obj]['vr_s']
    arrow_s = par.ALLOBJECT[obj]['arrow_s']
    type_arrow = par.ALLOBJECT[obj]['type_arrow']
    s_s_dim = par.ALLOBJECT[obj]['s_s_dim']
    w_text_dim = par.ALLOBJECT[obj]['w_text_dim']
    font_dim = par.ALLOBJECT[obj]['font_dim']
    R = par.ALLOBJECT[obj]['R']
    #print s, vr_s, arrow_s, type_arrow
    return xc, yc, x1, y1, size, fill, text, sloy, s, vr_s, arrow_s, type_arrow, s_s_dim, w_text_dim, font_dim, R
