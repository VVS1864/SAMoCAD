# -*- coding: utf-8; -*-
def tracer_obj(par, x2, y2, snap_s):
    a = False
    c = None
    w = par.c.winfo_width()
    h = par.c.winfo_height()
    find = list(par.c.find_overlapping(0,0,w,h))
    if len(find) > 10000:
        return
    for i in find:#Перебрать список приметивов
        obj_tags = par.c.gettags(i)
        try:
            t = obj_tags[1]
        except IndexError:
            continue
        if t[0] != 'L':
            continue
        tags = par.ALLOBJECT[t]['id'][i]
        if 'trace_o' in par.ALLOBJECT:
            c = par.c.coords('trace_o')
        if 'priv' in tags and 'line' in tags:
            xy = par.c.coords(i)
            if abs(xy[0]-xy[2])<par.min_e or abs(xy[1]-xy[3]) < par.min_e:
                if abs(x2-xy[0]) <= snap_s:
                    coords = [xy[0], xy[1]-10000.0, xy[0], xy[1]+10000.0]
                    
                elif abs(y2-xy[1]) <= snap_s:
                    coords = [xy[0]-10000.0, xy[1], xy[0]+10000.0, xy[1]]

                elif abs(x2-xy[2]) <= snap_s:
                    coords = [xy[2], xy[3]-10000.0, xy[2], xy[3]+10000.0]

                elif abs(y2-xy[3]) <= snap_s:
                    coords = [xy[2]-10000.0, xy[3], xy[2]+10000.0, xy[3]]
                else:
                    continue
                if c:
                    if c == coords:
                        a = True
                        break
                    par.c.delete('trace_o')
                    del par.ALLOBJECT['trace_o']                 
                id = par.c.create_line(coords, fill = 'yellow', width = 1, tags = ('obj', 'trace_o'))
                id_dict = {id:('line', 'priv')}
                par.ALLOBJECT['trace_o'] = {'id':id_dict}
                a = True
                break
    if a == False and 'trace_o' in par.ALLOBJECT:
        par.c.delete('trace_o')
        del par.ALLOBJECT['trace_o']
            
