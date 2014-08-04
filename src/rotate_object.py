# -*- coding: utf-8; -*-
from calc import calc_angle, rotateCalc, rotate_lines, rotate_points
from math import sin, cos, pi, degrees, radians
from get_conf import get_circle_conf, get_arc_conf, get_line_conf, get_text_conf, get_dim_conf, get_dimR_conf
import time
import text_line, dimension, circle, arc
import line as _line
#ВРАЩЕНИЕ
class Rotate_object:
    def __init__(self, par):
        self.par = par
        self.rotateEvent()
    def rotateEvent(self):
        if self.par.collection: #Если есть выбранные объекты
            self.par.standart_unbind()
            self.par.old_func = 'self.rotateEvent()'
            self.par.resFlag = True
            self.par.info.config(text = (u'Selected %s objects. Escape - stop') %(len(self.par.collection)))
            self.par.dialog.config(text = u'Rotate - base point:')
            self.par.c.bind('<Button-1>', self.rotateEvent2)
        else:
            self.par.info.config(text = u'Objects do not selected')
    def rotateEvent2(self, event):
        self.par.dialog.config(text = u'Rotate - point 1:')
        self.par.ex=self.par.priv_coord[0]
        self.par.ey=self.par.priv_coord[1]
        self.par.set_coord()
        self.par.c.bind('<Button-1>', self.rotateEvent3)

    def rotateEvent3(self, event):
        self.par.dialog.config(text = u'Rotate - point 2:')
        self.par.ex2=self.par.priv_coord[0]
        self.par.ey2=self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        self.par.set_coord()
        self.par.c.bind('<Button-1>', self.rotateEvent4)
        self.par.rotate_clone = True

    def rotateEvent4(self, event):
        self.par.ex3=self.par.priv_coord[0]
        self.par.ey3=self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        self.par.ex2,self.par.ey2 = self.par.coordinator(self.par.ex2,self.par.ey2)
        self.par.set_coord()
        self.par.rotate_clone = False
        self.rotateDelorNo()
        
    def rotateDelorNo(self):
        self.par.dialog.config(text = u'Delete objects? (Y / N)-[Y]:')
        self.par.command.focus_set()
        self.par.c.bind_class(self.par.master1,"<Return>",self.rotateEvent5)
        
    def rotateEvent5(self, event = None):
        if event:
            d = self.par.comY_N('Y')#Проверить, что было набрано в комндную строку - если значение недопустимое - ничего не делать
            if d == 'unknow':
                pass
            else:
                self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
                self.par.ex2,self.par.ey2 = self.par.coordinator(self.par.ex2,self.par.ey2)
                self.par.ex3,self.par.ey3 = self.par.coordinator(self.par.ex3,self.par.ey3)
                if self.par.ortoFlag == True and self.par.com == None:
                    self.par.ex3,self.par.ey3 = self.par.orto(self.par.ex,self.par.ey,self.par.ex3,self.par.ey3)
                if d == 'N':
                    de = 'No'
                elif d == 'Y':
                    de = 'Yes'
                if [self.par.ex,self.par.ey] != [self.par.ex3,self.par.ey3] and [self.par.ex,self.par.ey] != [self.par.ex2,self.par.ey2] and [self.par.ex3,self.par.ey3] != [self.par.ex2,self.par.ey2]: #Защита от деления на ноль
                    t1 = time.time()
                    rotate(self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2,self.par.ex3,self.par.ey3,delOld=de, content = self.par.collection)
                    t2 = time.time()
                    print 'rotate', t2-t1
                self.par.changeFlag = True
                self.par.enumerator_p()
                self.par.kill()
        else:
            self.par.ex3=self.par.priv_coord[0]
            self.par.ey3=self.par.priv_coord[1]
            self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
            self.par.ex2,self.par.ey2 = self.par.coordinator(self.par.ex2,self.par.ey2)
            self.par.ex3,self.par.ey3 = self.par.coordinator(self.par.ex3,self.par.ey3)
            self.par.set_coord()
            if self.par.tracingFlag:
                self.par.trace_on = True
                self.par.trace_x1, self.par.trace_y1 = self.par.ex,self.par.ey
                self.par.trace_x2, self.par.trace_y2 = self.par.ex3,self.par.ey3
            if self.par.ortoFlag == True and self.par.com == None:
                self.par.ex3,self.par.ey3 = self.par.orto(self.par.ex,self.par.ey,self.par.ex3,self.par.ey3)
            if [self.par.ex,self.par.ey] != [self.par.ex3,self.par.ey3] and [self.par.ex,self.par.ey] != [self.par.ex2,self.par.ey2] and [self.par.ex3,self.par.ey3] != [self.par.ex2,self.par.ey2]: #Защита от деления на ноль
                rotate(self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2,self.par.ex3,self.par.ey3,delOld='No', content = self.par.collection, temp = 'Yes')
            


def rotate(par, x0 = None, y0 = None, px1 = None, py1 = None, px2 = None, py2 = None, delOld = 'Yes', content = None, angle = None, temp = None):
    if angle == None: #Если угол поворота не указан - считать по координатам
        angle = calc_angle(x0, y0, px1, py1, px2, py2) #Если угол указан - считать сразу
    msin = sin(angle)
    mcos = cos(angle)
    
    if not temp:
        if delOld == 'No':
            for c in content:
                if c[0] == 'L':
                    fill, width, sloy, stipple, coord = get_line_conf(c, par)
                    coord = rotate_lines(x0, y0, [coord,], msin = msin, mcos = mcos)[0]
                    _line.c_line(par, coord[0], coord[1], coord[2], coord[3], width, sloy, fill, stipple)

                elif c[0] == 't':
                    fill, text, sloy, _angle, anchor, size, line, coord, s_s, w_text, font = get_text_conf(c, par)
                    coord = rotate_lines(x0, y0, [coord,], msin = msin, mcos = mcos)[0]
                    text_line.c_text(par, coord[0], coord[1], text, anchor, sloy, fill, angle+_angle, size, s_s, w_text, font)

                elif c[0] == 'd':
                    pass
                    '''
                    x1, y1, x2, y2, x3, y3, ort, size, fill, text, sloy, text_change, text_place, s, vr_s, vv_s, arrow_s, type_arrow, s_s_dim, w_text_dim, font_dim = get_dim_conf(c, par)
                    #coord = [y+d[0] if ind%2 == 0 else y+d[1] for ind, y in enumerate((x1, y1, x2, y2, x3, y3))]
                    if text_change == None:
                        text_change = [0, 0]
                    coord = rotate_lines(x0, y0, [x1, y1, x2, y2, x3, y3, text_change[0], text_change[1]], msin = msin, mcos = mcos)
                    dimension.c_dim(par, coord[0],coord[1],coord[2],coord[3],coord[4],coord[5],text, sloy,
                                                    fill,
                                                    size,
                                                    ort,
                                                    text_change,
                                                    [coord[6], coord[7]],
                                                    s,
                                                    vv_s,
                                                    vr_s,
                                                    arrow_s,
                                                    type_arrow,
                                                    s_s_dim,
                                                    w_text_dim,
                                                    font_dim)
                    '''
                elif c[0] == 'r':
                    pass
                    '''
                    xc, yc, x1, y1, size, fill, text, sloy, s, vr_s, arrow_s, type_arrow, s_s, w_text, font, R = get_dimR_conf(c, par)
                    coord = [y+d[0] if ind%2 == 0 else y+d[1] for ind, y in enumerate((xc, yc, x1, y1))]
                    dimension.c_dimR(par,coord[0],coord[1],coord[2],coord[3], text, sloy,
                                                    fill,
                                                    size,
                                                    s,
                                                    vr_s,
                                                    arrow_s,
                                                    type_arrow,
                                                    s_s,
                                                    w_text,
                                                    font,
                                                    R)
                    '''

                elif c[0] == 'c':
                    xc, yc, R, fill, width, sloy = get_circle_conf(c, par)
                    coord = rotate_points(x0, y0, [[xc, yc],], msin = msin, mcos = mcos)[0]
                    circle.c_circle(par, coord[0], coord[1], width = width, sloy = sloy, fill = fill, R = R)

                elif c[0] == 'a':
                    xc, yc, dx1, dy1, dx2, dy2, fill, width, sloy = get_arc_conf(c, par)
                    coord = rotate_points(x0, y0, [[xc, yc], [dx1, dy1], [dx2, dy2]], msin = msin, mcos = mcos)
                    arc.c_arc(par, coord[0][0], coord[0][1], coord[1][0], coord[1][1], coord[2][0], coord[2][1], width = width, sloy = sloy, fill = fill)

        else:
            for c in content:
                if c[0] in ('L', 't'):
                    if c[0] == 't':
                        par.ALLOBJECT[c]['angle'] += angle 
                    find = par.ALLOBJECT[c]['id']
                    for i in find:
                        coord = par.c.coords(i)
                        coord = tuple(rotate_lines(x0, y0, [coord,], msin = msin, mcos = mcos)[0])
                        par.c.coords(i, coord)

                elif c[0] == 'd':
                    pass
                    '''
                    x1, y1, x2, y2, x3, y3, ort, size, fill, text, sloy, text_change, text_place, s, vr_s, vv_s, arrow_s, type_arrow, s_s_dim, w_text_dim, font_dim = get_dim_conf(c, par)
                    #coord = [y+d[0] if ind%2 == 0 else y+d[1] for ind, y in enumerate((x1, y1, x2, y2, x3, y3))]
                    if text_change == None:
                        text_change = [0, 0]
                    coord = rotate_lines(x0, y0, [x1, y1, x2, y2, x3, y3, text_change[0], text_change[1]], msin = msin, mcos = mcos)
                    dimension.c_dim(par, coord[0],coord[1],coord[2],coord[3],coord[4],coord[5],text, sloy,
                                                    fill,
                                                    size,
                                                    ort,
                                                    text_change,
                                                    [coord[6], coord[7]],
                                                    s,
                                                    vv_s,
                                                    vr_s,
                                                    arrow_s,
                                                    type_arrow,
                                                    s_s_dim,
                                                    w_text_dim,
                                                    font_dim)
                    '''
                elif c[0] == 'r':
                    pass
                    '''
                    xc, yc, x1, y1, size, fill, text, sloy, s, vr_s, arrow_s, type_arrow, s_s, w_text, font, R = get_dimR_conf(c, par)
                    coord = [y+d[0] if ind%2 == 0 else y+d[1] for ind, y in enumerate((xc, yc, x1, y1))]
                    dimension.c_dimR(par,coord[0],coord[1],coord[2],coord[3], text, sloy,
                                                    fill,
                                                    size,
                                                    s,
                                                    vr_s,
                                                    arrow_s,
                                                    type_arrow,
                                                    s_s,
                                                    w_text,
                                                    font,
                                                    R)
                    '''

                elif c[0] == 'c':
                    xc, yc, R, fill, width, sloy = get_circle_conf(c, par)
                    par.c.delete(c)
                    coord = rotate_points(x0, y0, [[xc, yc],], msin = msin, mcos = mcos)[0]
                    circle.c_circle(par, coord[0], coord[1], width = width, sloy = sloy, fill = fill, R = R, ID = c)
                
                elif c[0] == 'a':
                    xc, yc, dx1, dy1, dx2, dy2, fill, width, sloy = get_arc_conf(c, par)
                    par.c.delete(c)
                    coord = rotate_points(x0, y0, [[xc, yc], [dx1, dy1], [dx2, dy2]], msin = msin, mcos = mcos)
                    arc.c_arc(par, coord[0][0], coord[0][1], coord[1][0], coord[1][1], coord[2][0], coord[2][1], width = width, sloy = sloy, fill = fill, ID = c)
    else:
        for c in content:
            if c[0] == 'L':
                fill, width, sloy, stipple, coord = get_line_conf(c, par)
                coord = rotate_lines(x0, y0, [coord,], msin = msin, mcos = mcos)[0]
                _line.c_line(par, coord[0], coord[1], coord[2], coord[3], width, sloy, fill, stipple, temp = temp)

            elif c[0] == 't':
                fill, text, sloy, _angle, anchor, size, line, coord, s_s, w_text, font = get_text_conf(c, par)
                coord = rotate_lines(x0, y0, [coord,], msin = msin, mcos = mcos)[0]
                text_line.c_text(par, coord[0], coord[1], text, anchor, sloy, fill, angle+_angle, size, s_s, w_text, font, temp = temp)

            elif c[0] == 'c':
                xc, yc, R, fill, width, sloy = get_circle_conf(c, par)
                coord = rotate_points(x0, y0, [[xc, yc],], msin = msin, mcos = mcos)[0]
                circle.c_circle(par, coord[0], coord[1], width = width, sloy = sloy, fill = fill, R = R, temp = temp)

            elif c[0] == 'a':
                xc, yc, dx1, dy1, dx2, dy2, fill, width, sloy = get_arc_conf(c, par)
                coord = rotate_points(x0, y0, [[xc, yc], [dx1, dy1], [dx2, dy2]], msin = msin, mcos = mcos)
                arc.c_arc(par, coord[0][0], coord[0][1], coord[1][0], coord[1][1], coord[2][0], coord[2][1], width = width, sloy = sloy, fill = fill, temp = temp)
