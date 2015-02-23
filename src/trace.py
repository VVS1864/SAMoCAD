# -*- coding: utf-8; -*-
from math import sin, cos, sqrt, degrees, radians
from calc import calc_angle
import sectors_alg
import src.symbols as symbols
import clip

def tracer(par, x1, y1, x2, y2, angle_s, rect):
    if not (0 < x1 < par.drawing_w and 0 < y1 < par.drawing_h and 0 < x2 < par.drawing_w and 0 < y2 < par.drawing_h):
        return
    if 'trace' in par.ALLOBJECT:
        par.trace_data = []
        par.trace_color = []
        par.ALLOBJECT, par.sectors = sectors_alg.delete(par.ALLOBJECT, par.sectors, ['trace',])
        
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
        
    if j > 0 and i < 0:
        angle_360 = 180.0 - angle
    elif j < 0 and i < 0:
        angle_360 = 180.0 + angle
    elif j < 0 and i > 0:
        angle_360 = 360.0 - angle
    else:
        angle_360 = angle
            
    a = 0
    d = sqrt((x2-x1)**2 + (y2-y1)**2)
    while angle_s*a <= 360.0:#90.0:
        if abs(angle_360)-3 <= abs(angle_s*a) <= abs(angle_360)+3:
            xi = cos(radians(angle_s*a))*d*10000.0 + x1#*i + x1
            yi = sin(radians(angle_s*a))*d*10000.0 + y1#*j + y1
            xr1, yr1, xr2, yr2 = clip.cohensutherland(0, par.drawing_h - 1, par.drawing_w - 1, 0, x1, y1, xi, yi)
            if not xr1:
                xr1, yr1, xr2, yr2 = x1, y1, xi, yi
            #if 'trace' in par.ALLOBJECT:
               # par.c.delete('text')
               # par.c.create_text(x2+snap_s*2, y2+snap_s*2, fill = 'yellow', text = str(angle_s*a), tags = ('obj', 'trace', 'text'))
                #a = None
                #break
            #else:
                #id = par.c.create_line(x1, y1, xi, yi, fill = 'yellow', width = 1, tags = ('obj', 'trace'))
                #par.c.create_text(x2+snap_s*2, y2+snap_s*2, fill = 'yellow', text = str(angle_s*a), tags = ('obj', 'trace', 'text'))
            lines = [(xr1,yr1,xr2,yr2),]
            par.trace_data.extend([xr1,yr1,xr2,yr2])
            par.trace_color.extend([255, 255, 0]*2)
            size = abs(rect[0]-rect[2])
            tt = symbols.font(x2 + size, y2 - size, str(angle_s*a), size, 1, 1, 'sw', 'TXT', 0, False)
            #lines.extend(tt.nabor[1:])
            for i in tt.nabor[1:]:
                par.trace_data.extend(i)
                par.trace_color.extend([255, 255, 0]*2)

            par.ALLOBJECT['trace'] =  {
                                'object':'line',
                                #'tags':id_dict,
                                #'class':object_line,
                                'sectors':[],
                                'coords': ((xr1,yr1,xr2,yr2),),
                                'lines': lines,
                                }
            par.ALLOBJECT, par.sectors = sectors_alg.quadric_mass(par.ALLOBJECT, ['trace',], par.sectors, par.q_scale)
            #id_dict = {id:('line', 'priv')}
            #par.ALLOBJECT['trace'] = {'id':id_dict}
            a = None
            
            break
        else:
            a += 1
    if a != None and 'trace' in par.ALLOBJECT:
        par.trace_data = []
        par.trace_color = []
        par.ALLOBJECT, par.sectors = sectors_alg.delete(par.ALLOBJECT, par.sectors, ['trace',])
       
