# -*- coding: utf-8; -*-
import dimension
import select_clone
from math import sqrt
import calc


#ПРОДЛЕНИЕ РАЗМЕРНОЙ ЛИНИИ
class Trim_dim:
    def __init__(self, par):
        self.par = par
        self.trim_dimEvent()

    def trim_dimEvent(self):
        self.par.kill()
        self.par.standart_unbind()
        self.par.info.config(text = u'Escape - stop')
        self.par.old_func = 'self.trim_dim()'
        self.par.c.unbind_class(self.par.c,"<Motion>")
        self.par.resFlag = True
        self.par.c.bind('<Button-1>', self.trim_dimEvent2)
        self.par.dialog.config(text = u'Chain dimension - dimension:')
        self.par.info.config(text = u'Enter - stop')

    def trim_dimEvent2(self, event):
        el = self.par.get_obj(event.x, event.y, 'all')
        if el and el[0] == 'd':
            self.par.col = el
            select_clone.Select_clone([self.par.col,], self.par, color = 'red')
            self.par.ex3 = self.par.priv_coord[0]
            self.par.ey3 = self.par.priv_coord[1]       
            self.par.set_coord()
            self.par.trim_dim_clone = True
            self.par.c.bind('<Button-1>', self.dim_conf)
            self.par.c.bind_class(self.par.c,"<Motion>", self.par.gpriv)
            self.par.dialog.config(text = u'Chain dimension - next point:')

    def dim_conf(self, event = None):
        self.par.ex2 = self.par.priv_coord[0]
        self.par.ey2 = self.par.priv_coord[1]
        self.par.ex3,self.par.ey3 = self.par.coordinator(self.par.ex3,self.par.ey3)
        x1, y1, x2, y2, x3, y3, ort, size, fill, text, sloy, text_change, text_place, s, vr_s, vv_s, arrow_s, type_arrow, s_s, w_text, font = self.par.get_dim_conf(self.par.col)
        if ort == 'horizontal':
            md1 = abs(y1-self.par.ey3)
            md2 = abs(y2-self.par.ey3)
        else:
            md1 = abs(x1-self.par.ex3)
            md2 = abs(x2-self.par.ex3)

        if md1<md2:
            self.par.ex = x1
            self.par.ey = y1
        else:
            self.par.ex = x2
            self.par.ey = y2
        
        self.par.set_coord()
        if event:
            dimension.c_dim(self.par, self.par.ex, self.par.ey, self.par.ex2, self.par.ey2, x3, y3,
                        #text = text,
                        sloy = sloy,
                        fill = fill,
                        size = size,
                        ort = ort,
                        #text_change = text_change,
                        #text_place = text_place,
                        s = s,
                        vr_s = vr_s,
                        vv_s = vv_s,
                        arrow_s = arrow_s,
                        type_arrow = type_arrow,
                        s_s = s_s,
                        w_text = w_text,
                        font = font)
            self.par.ex3 = self.par.priv_coord[0]
            self.par.ey3 = self.par.priv_coord[1]
            self.par.col = self.par.Ndim
            self.par.history_undo.append(('c_', self.par.Ndim))
            self.par.changeFlag = True
            self.par.enumerator_p()
            
        else:
            dimension.c_dim(self.par, self.par.ex, self.par.ey, self.par.ex2, self.par.ey2, x3, y3,
                        #text = text,
                        sloy = sloy,
                        fill = fill,
                        size = size,
                        ort = ort,
                        #text_change = text_change,
                        #text_place = text_place,
                        s = s,
                        vr_s = vr_s,
                        vv_s = vv_s,
                        arrow_s = arrow_s,
                        type_arrow = type_arrow,
                        s_s = s_s,
                        w_text = w_text,
                        font = font,
                        temp = 'Yes')
        
