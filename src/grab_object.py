# -*- coding: utf-8; -*-

def select(par, rect, master_enclose = None):
    #Выделение/снятие выделения рамкой
    x2 = max(rect[0], rect[2])
    x1 = min(rect[0], rect[2])
    y2 = max(rect[1], rect[3])
    y1 = min(rect[1], rect[3])
    if master_enclose == None:
        if rect[0] > rect[2]:
            enclose = False
        else:
            enclose = True
    else:
        enclose = master_enclose
    
    objects = par.get_current_objects([x1, y1, x2, y2], enclose)
    return objects
    
