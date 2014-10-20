# -*- coding: utf-8; -*-
from calc import filet_point
from line import c_line
from arc import c_arc
from get_conf import get_line_conf
from get_object import get_obj
import math

#СОПРЯЖЕНИЕ
class Fillet:
    def __init__(self, par):
        self.par = par
        self.filletEvent()
    def filletEvent(self, event=None):
        self.par.kill()
        self.par.info.config(text = u'Escape - stop')
        self.par.dialog.config(text = u'Fillet - line 1:')
        self.par.c.unbind('<Button-1>')
        self.par.c.bind('<Button-1>', self.filletEvent2)
        self.par.old_func = 'self.filletEvent()'
        #self.par.c.unbind_class(self.par.c,"<Motion>")
        self.par.unpriv = True
        self.par.c.unbind('<Shift-Button-1>')
        self.par.c.unbind_class(self.par.master1,"<Return>")

    def filletEvent2(self, event):
        el = get_obj(event.x, event.y, self.par, 'line')
        if el:
            self.par.mass_collektor([el,], 'select')
            self.par.resFlag = True
            self.par.dialog.config(text = u'Fillet - line 2:')
            self.par.c.bind('<Button-1>', self.filletEvent3)

    def filletEvent3(self, event):
        el = self.par.get_obj(event.x, event.y)
        if el:
            self.par.mass_collektor([el,], 'select')
            self.par.dialog.config(text = (u'Fillet - radius: [%s]') %(str(self.par.old_fillet_R)))
            self.par.info.config(text = u'Escape - stop. Ponit 1')
            self.par.c.bind_class(self.par.master1,"<Return>", self.filletEvent4)
            #self.par.c.bind_class(self.par.c,"<Motion>", self.par.gpriv)
            self.par.unpriv = False
            self.par.c.bind('<Button-1>', self.filletDistanse1)
            self.par.command.focus_set()

    def filletDistanse1(self, event):
        self.par.info.config(text = u'Escape - stop. Ponit 2')
        self.par.ex=self.par.priv_coord[0]
        self.par.ey=self.par.priv_coord[1]
        self.par.set_coord()
        self.par.c.bind_class(self.par.c,"<1>", self.filletDistanse2)

    def filletDistanse2(self, event):
        self.par.ex2=self.par.priv_coord[0]
        self.par.ey2=self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        pd = math.sqrt((-self.par.ex+self.par.ex2)**2 + (-self.par.ey+self.par.ey2)**2)
        self.par.c.unbind_class(self.par.c,"<1>")
        self.filletEvent4(pd = pd)

    def filletEvent4(self, event = None, pd = None):
        if pd:
            R = self.par.n_coordinator(pd)
            self.par.old_fillet_R = R
        else:
            self.par.comOrKill()
            if self.par.com != None:
                R = float(self.par.com)
                self.par.old_fillet_R = R
            else:
                R = self.par.old_fillet_R
        R = self.par.coordinator2(R)
        fill1, width1, sloy1, stipple1, c1, factor_stip1 = get_line_conf(self.par.collection[0], self.par)
        fill2, width2, sloy2, stipple2, c2, factor_stip2 = get_line_conf(self.par.collection[1], self.par)
        xc, yc, xe1, ye1, xe2, ye2, cord = filet_point(c1[0], c1[1], c1[2], c1[3], c2[0], c2[1], c2[2], c2[3], R)
        if xc:
            c_arc(self.par, xc, yc, xe1, ye1, xe2, ye2)

        c_line(self.par, cord[0], cord[1], cord[2], cord[3], fill=fill1, width=width1, sloy=sloy1, stipple=stipple1, factor_stip=factor_stip1)
        c_line(self.par, cord[4], cord[5], cord[6], cord[7], fill=fill2, width=width2, sloy=sloy2, stipple=stipple2, factor_stip=factor_stip2)
        self.par.delete(elements = self.par.collection)
        self.par.collection = []
        self.par.changeFlag = True
        self.par.enumerator_p()
        self.filletEvent()
