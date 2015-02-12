# -*- coding: utf-8 -*-
 
def simple(xBL, yBL, xTR, yTR, activIDs, ALL):#, x1, y1, x2, y2):
    #Дает все объекты которые как-нибудь попадают в рамку (пересекают или полностью внутри)
    objects = []
    for e in activIDs:
        lines = ALL[e]['coords']
        for ind, line  in enumerate(lines):
            x1 = line[0]
            y1 = line[1]
            x2 = line[2]
            y2 = line[3]
            
            if x1 > xTR and x2 > xTR:
                break
            if x1 < xBL and x2< xBL:
                break
            if y1 > yTR and y2 > yTR:
                break
            if y1 < yBL and y2< yBL:
                break

            if xBL < x1 < xTR and xBL < x2 < xTR and yBL < y1 < yTR and yBL < y2 < yTR:
                objects.append(e)
                break
            
            c = x2*y1-x1*y2
            b = x1-x2
            a = y2-y1
            
            
            r1 = a * xBL + b * yTR + c
            if not r1:
                objects.append(e)
                break
            r2 = a * xBL + b * yBL+ c
            if not r2:
                objects.append(e)
                break
            r3 = a * xTR + b * yTR+ c
            if not r3:
                objects.append(e)
                break
            r4 = a * xTR + b * yBL + c
            if not r4:
                objects.append(e)
                break
                
               
            if (r1 < 0 and r2 < 0 and r3 < 0 and r4 < 0) or (r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0):
                break
            else:
                objects.append(e)
                break

    return objects

def enclosing(xBL, yBL, xTR, yTR, activIDs, ALL):
    #Дает объекты, которые находятся полностью внутри рамки
    objects = []
    for e in activIDs:
        r = 0
        lines = ALL[e]['coords']
        for ind, line  in enumerate(lines):
            x1 = line[0]
            y1 = line[1]
            x2 = line[2]
            y2 = line[3]
            
            if xBL < x1 < xTR and xBL < x2 < xTR and yBL < y1 < yTR and yBL < y2 < yTR:
                #objects.append(e)
                #r = 1
                #break
                pass
            else:
                r = 1
                break
        if not r:
            objects.append(e)
    return objects


def cohensutherland(xmin, ymax, xmax, ymin, x1, y1, x2, y2):
    """Clips a line to a rectangular area.

    This implements the Cohen-Sutherland line clipping algorithm.  xmin,
    ymax, xmax and ymin denote the clipping area, into which the line
    defined by x1, y1 (start point) and x2, y2 (end point) will be
    clipped.

    If the line does not intersect with the rectangular clipping area,
    four None values will be returned as tuple. Otherwise a tuple of the
    clipped line points will be returned in the form (cx1, cy1, cx2, cy2).
    """
    INSIDE,LEFT, RIGHT, LOWER, UPPER = 0,1, 2, 4, 8

    def _getclip(xa, ya):
        #if dbglvl>1: print('point: '),; print(xa,ya)
        p = INSIDE  #default is inside

        # consider x
        if xa < xmin:
            p |= LEFT
        elif xa > xmax:
            p |= RIGHT

        # consider y
        if ya < ymin:
            p |= LOWER # bitwise OR
        elif ya > ymax:
            p |= UPPER #bitwise OR
        return p

# check for trivially outside lines
    k1 = _getclip(x1, y1)
    k2 = _getclip(x2, y2)

# examine non-trivially outside points
    while (k1 | k2) != 0: # if both points are inside box (0000) , ACCEPT trivial whole line in box

        # if line trivially outside window, REJECT
        if (k1 & k2) != 0:
            #if dbglvl>1: print('  REJECT trivially outside box')
            return None, None, None, None

        #non-trivial case, at least one point outside window
        opt = k1 or k2 # take first non-zero point, short circuit logic
        if opt & UPPER:
            x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
            y = ymax
        elif opt & LOWER:
            x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
            y = ymin
        elif opt & RIGHT:
            y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
            x = xmax
        elif opt & LEFT:
            y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
            x = xmin
        else: raise RuntimeError('Undefined clipping state')

        if opt == k1:
            x1, y1 = x, y
            k1 = _getclip(x1, y1)
            #if dbglvl>1: print('checking k1: ' + str(x) + ',' + str(y) + '    ' + str(k1))
        elif opt == k2:
            #if dbglvl>1: print('checking k2: ' + str(x) + ',' + str(y) + '    ' + str(k2))
            x2, y2 = x, y
            k2 = _getclip(x2, y2)
    return x1, y1, x2, y2
