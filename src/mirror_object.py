# -*- coding: utf-8; -*-
from calc import mirrorCalc, mirror_lines, mirror_points, calc_angle
#from get_conf import get_circle_conf, get_arc_conf, get_line_conf, get_text_conf, get_dim_conf, get_dimR_conf
from math import sqrt, pi
#import text_line, dimension, circle, arc
import line as _line
import time
#ЗЕРКАЛО (не применятеся к сложным объектам, содержащим текст)
class Mirror_object:
    def __init__(self, par):
        self.par = par
        self.mirrorEvent()
    def mirrorEvent(self):
        if self.par.collection:
            #self.par.standart_unbind()
            self.par.old_func = (self.par.action, Mirror_object)
            #self.par.info.config(text = (u'Selected %s objects. Escape - stop') %(len(self.par.collection)))
            #self.par.dialog.config(text = u'Mirror - point 1:')
            #self.par.c.bind('<Button-1>', self.mirrorEvent2)
            self.par.c.Unbind(wx.EVT_LEFT_DOWN)
            self.par.c.Bind(wx.EVT_LEFT_DOWN, self.mirrorEvent2)            
        else:
            pass
            #self.par.info.config(text = u'Objects do not selected')
    def mirrorEvent2(self, event):
        #self.par.dialog.config(text = u'Mirror - point 2:')
        #self.par.ex=self.par.priv_coord[0]
        #self.par.ey=self.par.priv_coord[1]
        self.par.ex = self.par.x_priv
        self.par.ey = self.par.y_priv
        self.par.c.Unbind(wx.EVT_LEFT_DOWN)
        self.par.c.Unbind(wx.EVT_MOTION)
        self.par.c.Bind(wx.EVT_LEFT_DOWN, self.mirrorEvent3)
        self.par.c.Bind(wx.EVT_MOTION, self.dynamic)
        #self.par.set_coord()
        #self.par.c.bind('<Button-1>', self.mirrorEvent3)
        #self.par.mirror_clone = True

    def dynamic(self, e):
        if not self.par.motion_flag:
            self.par.dynamic_data = []
            self.par.dynamic_color = []
            self.mirrorEvent3()
        self.par.motion(e)
        e.Skip()
    #??????????????? __ ?????????????????
    def mirrorEvent3(self, event):
        self.par.ex2=self.par.priv_coord[0]
        self.par.ey2=self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        self.par.set_coord()
        self.par.mirror_clone = False
        self.mirDelorNo()

    def mirDelorNo(self):
        self.par.dialog.config(text = u'Delete objects? (Y / N)-[N]:')
        self.par.command.focus_set()
        self.par.c.bind_class(self.par.master1,"<Return>",self.mirrorEvent4)

    def mirrorEvent4(self, event = None):
        if event:
            d = self.par.comY_N('N')#Проверить, что было набрано в командную строку - если значение недопустимое - ничего не делать
            if d == 'unknow':
                pass
            else:
                t1 = time.time()
                self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
                self.par.ex2,self.par.ey2 = self.par.coordinator(self.par.ex2,self.par.ey2)
                if self.par.ortoFlag == True and self.par.com == None:
                    self.par.ex2,self.par.ey2 = self.par.orto(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
                c = self.par.collection
                col = [x for x in c if x[0] not in ('t', 'd', 'r')]
                        
                if [self.par.ex,self.par.ey] != [self.par.ex2,self.par.ey2]:
                    if d == 'N':
                        mirror(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2, self.par, delOld='No', content = col)
                    elif d == 'Y':
                        mirror(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2, self.par, delOld='Yes', content = col)
                t2 = time.time()
                print ('mirror', t2-t1)
                self.par.changeFlag = True
                self.par.enumerator_p()
                self.par.kill()
        else:
            self.par.ex2=self.par.priv_coord[0]
            self.par.ey2=self.par.priv_coord[1]
            self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
            self.par.ex2,self.par.ey2 = self.par.coordinator(self.par.ex2,self.par.ey2)
            self.par.set_coord()
            if self.par.tracingFlag:
                self.par.trace_on = True
                self.par.trace_x1, self.par.trace_y1 = self.par.ex,self.par.ey
                self.par.trace_x2, self.par.trace_y2 = self.par.ex2,self.par.ey2
            
            if self.par.ortoFlag == True and self.par.com == None:
                self.par.ex2,self.par.ey2 = self.par.orto(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
            c = self.par.collection
            col = [x for x in c if x[0] not in ('t', 'd', 'r')] 
            if [self.par.ex,self.par.ey] != [self.par.ex2,self.par.ey2]:
                #if d == 'N':
                mirror(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2, self.par, delOld='No', content = col, temp = 'Yes')
                #elif d == 'Y':
                    #mirror(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2, self.par, delOld='Yes', content = col)

def mirror(px1,py1,px2,py2, par, delOld='No', content = None, temp = None):
    a = px2 - px1
    b = py2 - py1
    cos=a/sqrt(a*a+b*b)
    sin=b/sqrt(a*a+b*b)
    
    if not temp:
        if delOld == 'No':
            """
            for c in content:
                if c[0] == 'L':
                    par.ALLOBJECT[c]['class'].mirrorN(px1,py1, sin, cos)
                    '''
                    fill, width, sloy, stipple, coord, factor_stip = get_line_conf(c, par)
                    coord = mirror_lines(px1,py1, [coord,], sin, cos)[0]
                    _line.c_line(par, coord[0], coord[1], coord[2], coord[3], width, sloy, fill, stipple, factor_stip)
                    '''
                elif c[0] == 'c':
                    par.ALLOBJECT[c]['class'].mirrorN(px1,py1, sin, cos)
                    '''
                    xc, yc, R, fill, width, sloy = get_circle_conf(c, par)
                    coord = mirror_points(px1,py1, [[xc, yc],], sin, cos)[0]
                    circle.c_circle(par, coord[0], coord[1], width = width, sloy = sloy, fill = fill, R = R)
                    '''
                elif c[0] == 'a':
                    par.ALLOBJECT[c]['class'].mirrorN(px1,py1, sin, cos)
                    '''
                    xc, yc, dx1, dy1, dx2, dy2, fill, width, sloy = get_arc_conf(c, par)
                    coord = mirror_points(px1,py1, [[xc, yc], [dx1, dy1], [dx2, dy2]], sin, cos)
                    arc.c_arc(par, coord[0][0], coord[0][1], coord[1][0], coord[1][1], coord[2][0], coord[2][1], width = width, sloy = sloy, fill = fill)
                    '''
            """
        else:
            """
            for c in content:
                if c[0] == 'L':
                    par.ALLOBJECT[c]['class'].mirrorY(px1,py1, sin, cos)
                    '''
                    find = par.ALLOBJECT[c]['id']
                    for i in find:
                        coord = par.c.coords(i)
                        coord = tuple(mirror_lines(px1,py1, [coord,], sin, cos)[0])
                        par.c.coords(i, coord)
                    '''

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
                    
                    par.ALLOBJECT[c]['class'].mirrorN(px1,py1, sin, cos)
                    par.c.delete(c)
                    '''
                    xc, yc, R, fill, width, sloy = get_circle_conf(c, par)
                    par.c.delete(c)
                    coord = mirror_points(px1,py1, [[xc, yc],], sin, cos)[0]
                    circle.c_circle(par, coord[0], coord[1], width = width, sloy = sloy, fill = fill, R = R, ID = c)
                    '''
                    
                elif c[0] == 'a':
                    
                    par.ALLOBJECT[c]['class'].mirrorN(px1,py1, sin, cos)
                    par.c.delete(c)
                    '''
                    xc, yc, dx1, dy1, dx2, dy2, fill, width, sloy = get_arc_conf(c, par)
                    par.c.delete(c)
                    coord = mirror_points(px1,py1, [[xc, yc], [dx1, dy1], [dx2, dy2]], sin, cos)
                    arc.c_arc(par, coord[0][0], coord[0][1], coord[1][0], coord[1][1], coord[2][0], coord[2][1], width = width, sloy = sloy, fill = fill, ID = c)
                    '''
            """
    else:
        _line.c_line(par, px1,py1,px2,py2, width = 2, sloy = 't', fill = 'red', temp = temp)
        """
        for c in content:
            if c[0] == 'L':
                par.ALLOBJECT[c]['class'].mirror_temp(px1,py1, sin, cos)
                '''
                fill, width, sloy, stipple, coord, factor_stip = get_line_conf(c, par)
                coord = mirror_lines(px1,py1, [coord,], sin, cos)[0]
                _line.c_line(par, coord[0], coord[1], coord[2], coord[3], width, sloy, fill, stipple, factor_stip, temp = temp)
                '''
            elif c[0] == 'c':
                par.ALLOBJECT[c]['class'].mirror_temp(px1,py1, sin, cos)
                '''
                xc, yc, R, fill, width, sloy = get_circle_conf(c, par)
                coord = mirror_points(px1,py1, [[xc, yc],], sin, cos)[0]
                circle.c_circle(par, coord[0], coord[1], width = width, sloy = sloy, fill = fill, R = R, temp = temp)
                '''
            elif c[0] == 'a':
                par.ALLOBJECT[c]['class'].mirror_temp(px1,py1, sin, cos)
                '''
                xc, yc, dx1, dy1, dx2, dy2, fill, width, sloy = get_arc_conf(c, par)
                coord = mirror_points(px1,py1, [[xc, yc], [dx1, dy1], [dx2, dy2]], sin, cos)
                arc.c_arc(par, coord[0][0], coord[0][1], coord[1][0], coord[1][1], coord[2][0], coord[2][1], width = width, sloy = sloy, fill = fill, temp = temp)
                '''
        """
                
