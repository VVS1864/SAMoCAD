# -*- coding: utf-8; -*-
from math import sqrt
from calc import offset_line
from get_conf import get_circle_conf, get_arc_conf, get_line_coord
#СМЕЩЕНИЕ
class Offset:
    def __init__(self, par):
        self.par = par
        self.offsetEvent()
        
    def offsetEvent(self):
        if self.par.collection and len(self.par.collection)==1:
            col = self.par.collection[0]
            self.par.kill()
            self.par.mass_collektor([col,], 'select')
            self.par.info.config(text = u'Escape - stop. Enter - apply. Point 1')
            self.par.dialog.config(text = (u'Offset distanse:[%s]') %(str(self.par.old_offset)))
            self.par.c.bind('<Button-1>', self.offsetDistanse1)
            self.par.c.bind_class(self.par.master1,"<Return>", self.offsetEvent3)
            self.par.command.focus_set()
            self.par.c.bind_class(self.par.c,"<Motion>", self.par.gpriv)
            self.par.resFlag = True

        else:
            self.par.kill()
            self.par.info.config(text = u'Escape - stop')
            self.par.dialog.config(text = u'Offset - object:')
            self.par.c.unbind('<Button-1>')
            self.par.c.bind('<Button-1>', self.offsetEvent2)
            self.par.c.unbind_class(self.par.c,"<Motion>")
            self.par.c.unbind_class(self.par.master1,"<Return>")

        self.par.old_func = 'self.offsetEvent()'
        #self.par.c.tag_unbind('sel', '<Button-1>')
        #self.par.c.tag_unbind('sel', "<Leave>")
        #self.par.c.tag_unbind('sel', "<Enter>")
        self.par.c.unbind('<Shift-Button-1>')


    def offsetEvent2(self, event):
        el = self.par.get_obj(event.x, event.y, 'all')
        if el:
            self.par.mass_collektor([el,], 'select')
            self.par.resFlag = True
            self.par.c.bind('<Button-1>', self.offsetDistanse1)
            self.par.c.bind_class(self.par.master1,"<Return>", self.offsetEvent3)
            self.par.dialog.config(text = (u'Offset distanse:[%s]') %(str(self.par.old_offset)))
            self.par.info.config(text = u'Escape - stop. Enter - apply. Point 1')
            self.par.c.bind_class(self.par.c,"<Motion>", self.par.gpriv)
            self.par.command.focus_set()

    def offsetDistanse1(self, event):
        self.par.info.config(text = u'Escape - stop. Enter - apply. Point 2')
        self.par.ex=self.par.priv_coord[0]
        self.par.ey=self.par.priv_coord[1]
        self.par.set_coord()
        self.par.c.bind_class(self.par.c,"<1>", self.offsetDistanse2)

    def offsetDistanse2(self, event):
        self.par.ex2=self.par.priv_coord[0]
        self.par.ey2=self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        pd = sqrt((-self.par.ex+self.par.ex2)**2 + (-self.par.ey+self.par.ey2)**2)
        self.par.c.unbind_class(self.par.c,"<1>")
        self.offsetEvent3(pd = pd)

    def offsetEvent3(self, event = None, pd = None):
        self.par.info.config(text = u'Escape - stop')
        self.par.dialog.config(text = u'Offset direction:')
        if pd:
            self.par.pd = self.par.n_coordinator(pd)
            self.par.old_offset = self.par.pd
        else:
            self.par.comOrKill()
            if self.par.com:
                self.par.pd = float(self.par.com)
                self.par.old_offset = self.par.pd
            else:
                self.par.pd = self.par.old_offset
        self.par.c.bind('<Button-1>', self.offsetEvent4)

    def offsetEvent4(self, event):
        pd = self.par.coordinator2(self.par.pd)
        x3 = event.x
        y3 = event.y
        i = self.par.collection[0]
        if i[0] == 'L':
            c = get_line_coord(i, self.par)
            x1i, y1i, x2i, y2i = offset_line(c[0],c[1],c[2],c[3],pd, x3, y3)
            self.par.c_line(x1i, y1i, x2i, y2i)
        elif i[0] == 'c':
            x0, y0, R, fill, width, sloy = get_circle_conf(i, self.par)
            r = sqrt((x0-x3)**2 + (y0-y3)**2)
            if R<r:
                R += pd
            else:
                R -= pd
            self.par.c_circle(x0, y0, R = R)
        elif i[0] == 'a':
            x0, y0, dx1, dy1, dx2, dy2, start, extent, R, fill, width, sloy = get_arc_conf(i, self.par, _start = 1)
            r = sqrt((x0-x3)**2 + (y0-y3)**2)
            if R<r:
                R += pd
            else:
                R -= pd
            self.par.c_arc(x0,y0, R = R, start = start, extent = extent)

        self.par.changeFlag = True
        self.par.enumerator_p()
        self.par.kill()
        self.par.offsetEvent()
