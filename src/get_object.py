# -*- coding: utf-8; -*-
from calc import min_distanse, min_distanse_cir
from math import sqrt
#ДАТЬ ПРИМИТИВ БЛИЖАЙШИЙ К ТОЧКЕ
        
def get_obj(x, y, par, t_obj):
    find = par.c.find_overlapping(x-par.snap_s,y-par.snap_s,x+par.snap_s,y+par.snap_s)
    coords = []
    objs = []
    if find:
        for i in find:
            Num = par.c.gettags(i)[1]
            try:
                tag = par.ALLOBJECT[Num]['id'][i]
            except:
                continue
            if 'line' in t_obj:
                if 'lin' in tag:
                    c = par.c.coords(i)
                    xi, yi = min_distanse(c[0],c[1],c[2],c[3], x, y)
                    e = sqrt((xi-x)**2+(yi-y)**2)
                    coords.append(e)
                    objs.append(Num)
                    
            if 'dim' in t_obj:
                if Num[0] == 'd':
                    if 'dim_text' in tag:
                        print 'get'
                        c = par.c.coords(i)
                        xi, yi = min_distanse(c[0],c[1],c[2],c[3], x, y)
                        e = sqrt((xi-x)**2+(yi-y)**2)
                        coords.append(e)
                        objs.append(Num)

            if 'text' in t_obj:
                if Num[0] == 't':
                    #if 'dim_text' in tag:
                    print 'get'
                    c = par.c.coords(i)
                    xi, yi = min_distanse(c[0],c[1],c[2],c[3], x, y)
                    e = sqrt((xi-x)**2+(yi-y)**2)
                    coords.append(e)
                    objs.append(Num)
            
            if 'all' in t_obj:
                if 'a' in tag or 'cir' in tag:
                    c = par.c.coords(i)
                    x0 = (c[0]+c[2])/2.0
                    y0 = (c[1]+c[3])/2.0
                    R = (c[3]-c[1])/2.0
                    xi, yi, e = min_distanse_cir(x0, y0, R, x, y)
                    coords.append(e)
                    objs.append(Num)

                else:
                    c = par.c.coords(i)
                    xi, yi = min_distanse(c[0],c[1],c[2],c[3], x, y)
                    e = sqrt((xi-x)**2+(yi-y)**2)
                    coords.append(e)
                    objs.append(Num)

    if coords:
        emin = min(coords)
        el = objs[coords.index(emin)]
    else:
        el = None
    return el
