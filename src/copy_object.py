# -*- coding: utf-8; -*-
import time
import cProfile as profile
from get_conf import get_circle_conf, get_arc_conf, get_line_conf, get_text_conf, get_dim_conf, get_dimR_conf
import line as _line
import text_line, dimension, circle, arc
from move_object import mover
class Copy_object:
    def __init__(self, par):
        self.par = par
        self.copyEvent()
        
    def copyEvent(self):
        if self.par.collection:
            self.par.standart_unbind()
            self.par.old_func = 'self.copyEvent()'
            self.par.resFlag = True
            self.par.info.config(text = (u'Selected %s objects. Enter - stop') %(len(self.par.collection)))
            self.par.dialog.config(text = u'Copy - base point:')
            self.par.c.bind('<Button-1>', self.copyEvent2)
            self.par.c.unbind('<Shift-Button-1>')
            self.par.c.bind_class(self.par.master1,"<Return>", self.par.kill)
        else:
            self.par.info.config(text = u'Objects do not selected')

    def copyEvent2(self, event):
        self.par.dialog.config(text = u'Copy - insertion point:')
        self.par.command.focus_set()
        self.par.ex=self.par.priv_coord[0]
        self.par.ey=self.par.priv_coord[1]
        self.par.set_coord()
        self.par.c.bind('<Button-1>', self.copyEvent3)
        self.par.ex3,self.par.ey3 = self.par.ex,self.par.ey
        self.par.copy_clone = True

    def copyEvent3(self, event=None):
        t1 = time.time()
        self.par.ex2=self.par.priv_coord[0]
        self.par.ey2=self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        if self.par.tracingFlag:
            self.par.trace_on = True
            self.par.trace_x1, self.par.trace_y1 = self.par.ex,self.par.ey
            self.par.trace_x2, self.par.trace_y2 = self.par.ex2,self.par.ey2
        if event:
            if self.par.ortoFlag == True and self.par.com == None:
                self.par.ex2,self.par.ey2=self.par.orto(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
            self.par.ex2,self.par.ey2 = self.par.commer(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
            dx = self.par.ex2-self.par.ex
            dy = self.par.ey2-self.par.ey
            #profile.runctx('self.copyer(self.par.collection, self.par, (dx, dy))', None, locals())
            copyer(self.par.collection, self.par, (dx, dy))
            t2 = time.time()
            print ('copy', t2-t1)
            self.par.set_coord()
            self.par.com = None
            self.par.changeFlag = True
            self.par.enumerator_p()
        else:
            self.par.ex3, self.par.ey3 = self.par.coordinator(self.par.ex3, self.par.ey3)
            self.par.ex2,self.par.ey2 = self.par.commer(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
            if self.par.ortoFlag == True and self.par.com == None: #Если режим орто - сделать координаты орто
                self.par.ex2,self.par.ey2 = self.par.orto(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
            
            collection = ['C' + x for x in self.par.collection]
            
            mover(collection, self.par, dx = self.par.ex2-self.par.ex3, dy = self.par.ey2-self.par.ey3)
            self.par.ex3 = self.par.ex2
            self.par.ey3 = self.par.ey2
            self.par.set_coord()
       
    #Копирует объекты
def copyer(collection, par, d): 
    for content in collection:
        if content[0] in ['L', 't']:
            par.ALLOBJECT[content]['class'].copy(d)
            '''
            fill, width, sloy, stipple, coord, factor_stip = get_line_conf(content, par)
            coord = [y+d[0] if ind%2 == 0 else y+d[1] for ind, y in enumerate(coord)]
            _line.c_line(par, coord[0], coord[1], coord[2], coord[3], width, sloy, fill, stipple, factor_stip)
            
        elif content[0] == 't':
            fill, text, sloy, angle, anchor, size, line, coord, s_s, w_text, font = get_text_conf(content, par)
            coord = [y+d[0] if ind%2 == 0 else y+d[1] for ind, y in enumerate(coord[0:2])]
            text_line.c_text(par, coord[0], coord[1], text, anchor, sloy, fill, angle, size, s_s, w_text, font)
            '''
        elif content[0] == 'd':
            x1, y1, x2, y2, x3, y3, ort, size, fill, text, sloy, text_change, text_place, s, vr_s, vv_s, arrow_s, type_arrow, s_s_dim, w_text_dim, font_dim = get_dim_conf(content, par)
            coord = [y+d[0] if ind%2 == 0 else y+d[1] for ind, y in enumerate((x1, y1, x2, y2, x3, y3))]
            if text_place:
                text_place[0] += d[0]
                text_place[1] += d[1]
            dimension.c_dim(par, coord[0],coord[1],coord[2],coord[3],coord[4],coord[5],text, sloy,
                                            fill,
                                            size,
                                            ort,
                                            text_change,
                                            text_place,
                                            s,
                                            vv_s,
                                            vr_s,
                                            arrow_s,
                                            type_arrow,
                                            s_s_dim,
                                            w_text_dim,
                                            font_dim)

        elif content[0] == 'r':
            xc, yc, x1, y1, size, fill, text, sloy, s, vr_s, arrow_s, type_arrow, s_s, w_text, font, R = get_dimR_conf(content, par)
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

        elif content[0] == 'c':
            x0, y0, R, fill, width, sloy = get_circle_conf(content, par)
            x0 += d[0]
            y0 += d[1]
            circle.c_circle(par, x0, y0, width = width, sloy = sloy, fill = fill, R = R)

        elif content[0] == 'a':
            xc, yc, dx1, dy1, dx2, dy2, start, extent, R, fill, width, sloy = get_arc_conf(content, par, 1)
            xc += d[0]
            yc += d[1]
            arc.c_arc(par,xc,yc, width = width, sloy = sloy, fill = fill, R = R, start = start, extent = extent)
            
