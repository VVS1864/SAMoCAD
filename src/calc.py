# -*- coding: utf-8; -*-
from math import sqrt, acos, sin, cos
import copy
min_e = 0.00001
def intersection_l_l(x1,y1, x2,y2, x3, y3, x4, y4):#Пересечение векторов. Принимает координаты 2 линий, проверяет их на параллельность, если не параллельны - ищет точку пересечения, если такая есть - возвращает ее координаты, иначе вернет None, None
    ua1 = (x4 - x3)*(y1 - y3) - (y4 - y3)*(x1 - x3)
    ub1 = (x2 - x1)*(y1 - y3) - (y2 - y1)*(x1 - x3)
    u2 = (y4 - y3)*(x2 - x1) - (x4 - x3)*(y2 - y1)
    if u2 == 0:
        pir_inter = 'parallel'
        x = None
        y = None
    else: 
        ua = ua1 / u2 
        ub = ub1 / u2        
        x = x1 + ua*(x2-x1)
        y = y1 + ua*(y2-y1)
   
    return x, y
def intersection_l_c(xc,yc,R, x1,y1, x2,y2, x_c, y_c):
    xp1 = x1 - xc
    yp1 = y1 - yc
    xp2 = x2 - xc
    yp2 = y2 - yc
    x_pc = x_c - xc
    y_pc = y_c - yc
    A = yp1-yp2
    B = xp1-xp2
    C = xp2*(yp2-yp1) + yp2*(xp1-xp2)
    try:
        x0 = -A*C/(A*A+B*B)
        y0 = -B*C/(A*A+B*B)
    except ZeroDivisionError:
        return None, None
    if sqrt(x0*x0 + y0*y0)<=R:
        d = sqrt(R*R - C*C/(A*A + B*B))
        mult = sqrt(d*d/(A*A+B*B))
        ax = x0 + B*mult
        ay = -(y0 - A*mult)
        bx = x0 - B*mult
        by = -(y0 + A*mult)
        if abs(x_pc-ax)<abs(x_pc-bx):
            x = ax
        else:
            x = bx
        if abs(y_pc-ay)<abs(y_pc-by):
            y = ay
        else:
            y = by
    else:
        return None, None
    x += xc
    y += yc
    return x, y

def intersection_c_c(xc1,yc1,R1,xc2,yc2,R2, x_c, y_c):
    d = sqrt((xc2-xc1)**2.0+(yc2-yc1)**2.0)
    
    if d>(R1+R2) or (d == 0 and R1 == R2) or (d<abs(R1-R2)):
        x=None
        y=None
        return x, y
    else:
        a = (R1*R1 - R2*R2 + d*d)/(2*d)
        h = sqrt(R1*R1 - a*a)
        x2 = xc1+a*(xc2-xc1)/d
        y2 = yc1+a*(yc2-yc1)/d
        ax = x2 + h*(yc2 - yc1)/d
        ay = y2 - h*(xc2 - xc1)/d
        bx = x2 - h*(yc2 - yc1)/d
        by = y2 + h*(xc2 - xc1)/d
  
        if abs(x_c-ax)<=abs(x_c-bx):         
            if abs(y_c-ay)<=abs(y_c-by):
                x = ax
                y = ay
            else:
                x = None
                y = None
        elif abs(x_c-ax)>=abs(x_c-bx): 
            if abs(y_c-ay)>=abs(y_c-by):
                x = bx
                y = by
            else:
                x = None
                y = None
     
    return x, y

def min_distanse(x1,y1, x2,y2, x3, y3):
    a = (x2-x1)
    b = (y2-y1)
    numerator = (x3 - x1)*a + (y3 - y1)*b
    denumerator = a*a+b*b
    if denumerator != 0:
        u = numerator / denumerator
        x = x1 + u*a
        y = y1 + u*b
    else:
        x = None
        y = None

    return x, y

def intersection_stright(x1,y1, x2,y2, x3, y3, x4, y4):#По координатам 2 линий находит уравнения их прямых и определяет, есть ли у них общая точка - если есть возвращает ее.
    x = None
    y = None
    if x1 == x3 and y1 == y3:
        x = x1
        y = y1
        
    elif x2 == x4 and y2 == y4:
        x = x2
        y = y2
        
    else:
        dxa = x2-x1
        dxb = x4-x3
        dya = y2-y1
        dyb = y4-y3
        
        if dxa == 0:
            x = x1
        if dxb == 0:
            x = x3
        if dya == 0:
            y = y1
        if dyb == 0:
            y = y3
        
        if dxa != 0 and dya != 0 and (x or y):
            if y:
                x = (y*dxa - y1*dxa + dya*x1)/dya
            elif x:
                y = (x*dya - x1*dya + dxa*y1)/dxa
            
        elif dxb != 0 and dyb != 0 and (x or y):
            if y :
                x = (y*dxb - y3*dxb + dyb*x3)/dyb
            elif x:
                y = (x*dyb - x3*dyb + dxb*y3)/dxb

        if dxa != 0 and dya != 0 and dxb != 0 and dyb != 0:
            ka = dxa/dya
            kb = dxb/dyb
            ba = (-y1*dxa+x1*dya)/dya
            bb = (-y3*dxb+x3*dyb)/dyb
            yba = (-y1*dxa+x1*dya)/dxa
            ybb = (-y3*dxb+x3*dyb)/dxb
            y = (bb-ba)/(ka-kb)
            x = (y*dxa - y1*dxa + dya*x1)/dya
         
    return x,y

def offset_line(x1,y1, x2,y2, pd, x3, y3):
    xb = max(x2, x1)
    xm = min(x2, x1)
    yb = max(y2, y1)
    ym = min(y2, y1)
    dx2 = xb - xm
    dy2 = yb - ym
    c = sqrt (dx2**2.0 + dy2**2.0)
    mcos = dx2/c
    msin = dy2/c
 
    dxi = msin * pd
    dyi = mcos * pd
    
    D = (x3 - xm) * (yb - ym) - (y3 - ym) * (xb - xm)

    if D<0:
        dx = -dxi
        dy = dyi
    elif D>0:
        dx = dxi
        dy = -dyi
    box = [xm, ym, xb, yb]
    if [box[0], box[3]] == [x1, y1]:
        if y1 != y2 and x1 != x2:
            D = (x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)
            if D>0:
                dx = -dxi
                dy = -dyi
            else:
                dx = dxi
                dy = dyi
    if [box[0], box[3]] == [x2, y2]:
        if y1 != y2 and x1 != x2:
            D = (x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)
            if D>0:
                dx = dxi
                dy = dyi
            else:
                dx = -dxi
                dy = -dyi
        
    x1i = x1+dx
    y1i = y1+dy
    x2i = x2+dx
    y2i = y2+dy
    return x1i, y1i, x2i, y2i

def min_distanse_cir(xc, yc, R, x1, y1):
    d = sqrt((x1-xc)**2.0 + (y1-yc)**2.0) - R
    xp = x1 - xc
    yp = y1 - yc
    xpc = 0
    ypc = 0
    A = yp
    B = xp
    C = 0
    mult = sqrt(R**2.0/(A**2.0+B**2.0))
    ax = B*mult + xc
    ay = -A*mult + yc
    bx = -B*mult + xc
    by = A*mult + yc
    if abs(x1-ax)<abs(x1-bx):
        x = ax
    else:
        x = bx
    if abs(y1-ay)<abs(y1-by):
        y = ay
    else:
        y = by
    return x, y, d
def filet_point(xt1,yt1,xt2,yt2, xt3,yt3,xt4,yt4, R):
    x0,y0 = intersection_stright(xt1,yt1,xt2,yt2, xt3,yt3,xt4,yt4)
    a = sqrt((xt1-x0)**2 + (yt1-y0)**2)
    b = sqrt((xt2-x0)**2 + (yt2-y0)**2)
    c = sqrt((xt3-x0)**2 + (yt3-y0)**2)
    d = sqrt((xt4-x0)**2 + (yt4-y0)**2)
    rmin1 = min(a, b)
    rmin2 = min(c, d)
    x1 = xt1
    y1 = yt1
    x2 = xt2
    y2 = yt2
    x3 = xt3
    y3 = yt3
    x4 = xt4
    y4 = yt4
    if rmin1 == a and rmin2 == c:
       
        xr = (xt2+xt4)/2.0
        yr = (yt2+yt4)/2.0
        xd1 = x4
        xd2 = x2
        yd1 = y4
        yd2 = y2
        xm1 = x3
        xm2 = x1
        ym1 = y3
        ym2 = y1
    elif rmin1 == b and rmin2 == d:

        xr = (xt1+xt3)/2.0
        yr = (yt1+yt3)/2.0
        xd1 = x3
        xd2 = x1
        yd1 = y3
        yd2 = y1
        xm1 = x4
        xm2 = x2
        ym1 = y4
        ym2 = y2

    elif rmin1 == a and rmin2 == d:
    
        xr = (xt2+xt3)/2.0
        yr = (yt2+yt3)/2.0
        xd1 = x3
        xd2 = x2
        yd1 = y3
        yd2 = y2
        xm1 = x4
        xm2 = x2
        ym1 = y4
        ym2 = y2
        
    elif rmin1 == b and rmin2 == c:
 
        xr = (xt1+xt4)/2.0
        yr = (yt1+yt4)/2.0
        xd1 = x4
        xd2 = x1
        yd1 = y4
        yd2 = y1
        xm1 = x3
        xm2 = x2
        ym1 = y3
        ym2 = y2
            
    if R != 0:
        x1i, y1i, x2i, y2i = offset_line(x1,y1, x2,y2, R, xr, yr)
        x3i, y3i, x4i, y4i = offset_line(x3,y3, x4,y4, R, xr, yr)
        xc,yc = intersection_stright(x1i, y1i, x2i, y2i, x3i, y3i, x4i, y4i)
        xe1, ye1 = min_distanse(x1,y1, x2,y2, xc, yc)
        xe2, ye2 = min_distanse(x3,y3, x4,y4, xc, yc)
        D1 = (xe1 - x1) * (y2 - y1) - (ye1 - y1) * (x2 - x1)
        D2 = (xe1 - x3) * (y4 - y3) - (ye1 - y3) * (x4 - x3)
        D3 = (xe2 - x1) * (y2 - y1) - (ye2 - y1) * (x2 - x1)
        D4 = (xe2 - x3) * (y4 - y3) - (ye2 - y3) * (x4 - x3)
      
        if abs(D1) < 0.000001 or abs(D4) < 0.000001:
            aa = xd1
            bb = yd1
            xd1 = xd2
            yd1 = yd2
            xd2 = aa
            yd2 = bb
            
    else:
        xc = None
        yc = None
        xe1,ye1 = intersection_stright(x1, y1, x2, y2, x3, y3, x4, y4)
        xe2,ye2 = xe1,ye1
            
            
    cord = [xe1,ye1,xd1,yd1,xe2,ye2,xd2,yd2]


    return xc, yc, xe1, ye1, xe2, ye2, cord

def trim_line(x1, y1, x2, y2, x, y, c):
    xn, yn = intersection_stright(x1, y1, x2, y2, c[0], c[1], c[2], c[3])
    if  max(x1, x2) >= xn >= min(x1, x2) or max(y1, y2) >= yn >= min(y1, y2):
        pass
    else:
        return None
    cNew = None
    if xn:
        cNew = c
        D1 = (x2-x1)*(y-y1)-(y2-y1)*(x-x1)
        D2 = (x2-x1)*(c[1]-y1)-(y2-y1)*(c[0]-x1)
        D3 = (x2-x1)*(c[3]-y1)-(y2-y1)*(c[2]-x1)
        if abs(D1)<0.000001 or abs(D2)<0.000001 or abs(D3)<0.000001:
            return None
        elif D1<0:
            if D2<0:
                if D3<0:
                    return None
                cNew[0] = xn
                cNew[1] = yn
            elif D2>0:
                if D3>0:
                    return None
                cNew[2] = xn
                cNew[3] = yn
                
        elif D1>0:
            if D2>0:
                if D3>0:
                    return None
                cNew[0] = xn
                cNew[1] = yn
            elif D2<0:
                if D3<0:
                    return None
                cNew[2] = xn
                cNew[3] = yn
    return cNew

def extend_line(x1, y1, x2, y2, c):
    xn, yn = intersection_stright(x1, y1, x2, y2, c[0], c[1], c[2], c[3])
    r1 = sqrt((xn-c[0])**2+(yn-c[1])**2)
    r2 = sqrt((xn-c[2])**2+(yn-c[3])**2)
    if r1<r2:
        pass
    else:
        cc = copy.copy(c)
        c[2] = cc[0]
        c[0] = cc[2]
        c[3] = cc[1]
        c[1] = cc[3]
  
    if  max(x1, x2) >= xn >= min(x1, x2) or max(y1, y2) >= yn >= min(y1, y2):
        pass
    else:
        return None
    cNew = None
    if xn:
        cNew = c
        D2 = (x2-x1)*(c[1]-y1)-(y2-y1)*(c[0]-x1)
        D3 = (x2-x1)*(c[3]-y1)-(y2-y1)*(c[2]-x1)
        if abs(D2)<0.000001 or abs(D3)<0.000001:
            return None
        elif D2<0:
            if D3>0:
                return None
            cNew[0] = xn
            cNew[1] = yn
        elif D2>0:
            if D3<0:
                return None
            cNew[0] = xn
            cNew[1] = yn
        
    return cNew

def calc_angle(x0, y0, px1, py1, px2, py2):
    x1 = px1 - x0
    y1 = py1 - y0
    x2 = px2 - x0
    y2 = py2 - y0
    d1 = sqrt(x1*x1 + y1*y1)
    d2 = sqrt(x2*x2 + y2*y2)
    try:
        a = acos((x1 * x2 + y1 * y2) / (d1 * d2))
    except:
        print 'bad angle! ', '(',x1, '*', x2, '+', y1, '*', y2, ') / (', d1, '*', d2,')'
        return None
    if x1*y2 - x2*y1 <= 0:
        return a
    else:
        return -a
        

def rotateCalc(x0,y0,xold,yold,mcos,msin): #считает координаты поворота
    x=(xold-x0)*mcos+(yold-y0)*msin
    y=-(xold-x0)*msin+(yold-y0)*mcos
    x += x0
    y += y0
    return x,y

def rotate_lines(x, y, lines, msin, mcos):
    #if angle != None:
        #msin = sin(angle)
        #mcos = cos(angle)
    for i in lines:
        i[0],i[1] = rotateCalc(x,y,i[0],i[1],mcos,msin) #Пересчитать координаты певернутого
        i[2],i[3] = rotateCalc(x,y,i[2],i[3],mcos,msin)
    return lines

def rotate_points(x, y, points, angle = None, msin = None, mcos = None):
    if angle != None:
        msin = sin(angle)
        mcos = cos(angle)
    for i in points:
        i[0],i[1] = rotateCalc(x,y,i[0],i[1],mcos,msin) #Пересчитать координаты певернутого
    return points

def mirrorCalc(px1, py1, xold, yold,  mcos, msin):
    a = xold-px1
    b = yold-py1
    x2 = (mcos*(a*mcos+b*msin) + msin*(-a*msin+b*mcos))+px1
    y2 = (msin*(a*mcos+b*msin) + mcos*(a*msin-b*mcos)) +py1
    return x2,y2
    
def mirror_lines(x, y, lines, msin, mcos):
    for i in lines:
        i[0],i[1] = mirrorCalc(x,y,i[0],i[1],mcos,msin) #Пересчитать координаты певернутого
        i[2],i[3] = mirrorCalc(x,y,i[2],i[3],mcos,msin)
    return lines

def mirror_points(x, y, points, msin, mcos):
    for i in points:
        i[0],i[1] = mirrorCalc(x,y,i[0],i[1],mcos,msin) #Пересчитать координаты певернутого
    return points

def near_far_point(coord, ex, ey):
    d1 = sqrt((coord[0]-ex)**2 + (coord[1]-ey)**2)
    d2 = sqrt((coord[2]-ex)**2 + (coord[3]-ey)**2)
    if d1<d2:
        xn = coord[0]
        yn = coord[1]
        xf = coord[2]
        yf = coord[3]
    else:
        xn = coord[2]
        yn = coord[3]
        xf = coord[0]
        yf = coord[1]
    return xn, yn, xf, yf

def cmd_coorder(x1, y1, x2, y2, data, ortoFlag):
    #Принимает координаты линии и требуемую длинну, возвращает координаты второй точки линии с учетом заданной длинны
    #Если ortoFlag == True, линия будет нормализована
    dx = x1 - x2
    dy = y1 - y2
    if not ortoFlag and abs(dx) > min_e and  abs(dy) > min_e:#and x1 != x2 and y1 != y2:
        dx0 = sqrt((data*data * dx*dx)/(dy*dy + dx*dx))
        dy0 = dx0 * dy/dx
        i = 1
        if x1<x2:
            i=-1
        x2=x1 - i * dx0
        y2=y1 - i * dy0
    else:
        x2,y2 = ortho(x1, y1, x2, y2, data)
        
    return x2,y2

def ortho(x1, y1, x2, y2, data):
    i = 1
    dx = x1 - x2
    dy = y1 - y2            
    if abs(dx) > abs(dy):
        y2 = y1
        if x1 > x2:
            i =- 1
        x2 = x1 + i * data
    else:
        x2 = x1
        if y1 > y2:
            i =- 1
        y2 = y1 + i * data
    return x2, y2


