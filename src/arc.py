# -*- coding: utf-8; -*-
from math import pi, sqrt, degrees, radians
from calc import calc_angle
from Tkinter import ARC
#ДУГА
class Arc:
    def __init__(self, par):
        self.par = par
        self.risArc()
        
    def risArc(self):
        self.par.kill()
        self.par.standart_unbind()
        self.par.old_func = 'self.risArc()'
        self.par.c.bind('<Button-1>', self.arc)
        self.par.dialog.config(text = 'Arc - center point:')
        self.par.info.config(text = 'Enter - stop')

    def arc(self, event):
        self.par.command.focus_set()
        self.par.set_coord()
        self.par.ex = self.par.priv_coord[0]
        self.par.ey = self.par.priv_coord[1]
        self.par.c.bind_class(self.par.c,"<1>", self.arc2)
        self.par.dialog.config(text = 'Arc - point 1:')

    def arc2(self, event):
        self.par.command.focus_set()
        self.par.ex2 = self.par.priv_coord[0]
        self.par.ey2 = self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        self.par.ex2,self.par.ey2 = self.par.commer(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
        self.par.c.bind_class(self.par.c,"<1>", self.arc3)
        self.par.set_coord()
        self.par.arc_clone = True
        self.par.dialog.config(text = 'Arc - point 2:')

    def arc3(self, event = None):
        self.par.command.focus_set()
        self.par.ex3 = self.par.priv_coord[0]
        self.par.ey3 = self.par.priv_coord[1]
        self.par.ex2,self.par.ey2 = self.par.coordinator(self.par.ex2,self.par.ey2)
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        self.par.ex3,self.par.ey3 = self.par.commer(self.par.ex,self.par.ey,self.par.ex3,self.par.ey3)
        if self.par.tracingFlag:
            self.par.trace_on = True
            self.par.trace_x1, self.par.trace_y1 = self.par.ex,self.par.ey
            self.par.trace_x2, self.par.trace_y2 = self.par.ex3,self.par.ey3
        if (self.par.ex,self.par.ey) != (self.par.ex2,self.par.ey2) and (self.par.ex,self.par.ey) != (self.par.ex3,self.par.ey3) and (self.par.ex2,self.par.ey2) != (self.par.ex3,self.par.ey3):
            if event:
                c_arc(self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2,self.par.ex3,self.par.ey3)
                self.par.history_undo.append(('c_', self.par.Narc))
                
                self.par.changeFlag = True
                self.par.arc_clone = False
                self.par.enumerator_p()
                self.par.risArc()
            else:
                self.par.set_coord()
                c_arc(self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2,self.par.ex3,self.par.ey3, temp = 'yes')
#Отрисовка
def c_arc(par,x0,y0,xr1=None, yr1=None, xr2=None, yr2=None, width = None, sloy = None, fill = None, R = None, start = None, extent = None, ID = None, temp = None):
    if sloy == None:
        fill = par.color
        width = par.width
        sloy = par.sloy
    width = int(width)
    if not temp:
        if not ID:
            par.Narcd+=1
            ID = par.Narc = 'a' + str(par.Narcd)
        
        if R == None:
            R = sqrt((xr1-x0)*(xr1-x0) + (yr1-y0)*(yr1-y0))
        x1=x0-R
        x2=x0+R
        y1=y0-R
        y2=y0+R
        s = R/20.0
        R = par.n_coordinator(R)
        id_dict = {}
        if start == None:
            aa = degrees(calc_angle(x0, y0, x2, y0, xr1, yr1))
            bb = degrees(calc_angle(x0, y0, xr1, yr1, xr2, yr2))
        else:
            aa = start
            bb = extent
        id = par.c.create_arc(x1,y1,x2,y2, start = aa, extent = bb, outline=fill, full=None,width=width,style = 'arc', tags = ('obj', ID))#['arc', par.Narc, 'a', 'obj', 'priv', sloy])
        id_dict[id] = ('a', 'priv')
        id = par.c.create_line(x0-s,y0-s,x0+s,y0+s,fill=fill,tags = ('obj', ID, 'a_centr'))#['arc', par.Narc, 'line', 'a_centr', 'obj', 'priv',  sloy])
        id_dict[id] = ('line', 'priv', 'a_centr')
        id = par.c.create_line(x0+s,y0-s,x0-s,y0+s,fill=fill,tags = ('obj', ID, 'a_centr'))#['arc', par.Narc, 'line', 'a_centr', 'obj', 'priv',  sloy])
        id_dict[id] = ('line', 'priv', 'a_centr')
        par.ALLOBJECT[ID]={'object':'arc', 'fill':fill, 'width':width, 'sloy':sloy, 'start':aa, 'extent':bb, 'R':R, 'id':id_dict}
    else:
        if R == None:
            R = sqrt((xr1-x0)*(xr1-x0) + (yr1-y0)*(yr1-y0))
        x1=x0-R
        x2=x0+R
        y1=y0-R
        y2=y0+R
        s = R/20.0
        R = par.n_coordinator(R)
        if start == None:
            aa = degrees(calc_angle(x0, y0, x2, y0, xr1, yr1))
            bb = degrees(calc_angle(x0, y0, xr1, yr1, xr2, yr2))
        else:
            aa = start
            bb = extent
        par.c.create_arc(x1,y1,x2,y2, start = aa, extent = bb, outline=fill, full=None,width=width,style = 'arc', tags = ('obj', 'temp'))#['arc', par.Narc, 'a', 'obj', 'priv', sloy])
        
        par.c.create_line(x0-s,y0-s,x0+s,y0+s,fill=fill,tags = ('obj', 'temp'))#['arc', par.Narc, 'line', 'a_centr', 'obj', 'priv',  sloy])
        
        par.c.create_line(x0+s,y0-s,x0-s,y0+s,fill=fill,tags = ('obj', 'temp'))#['arc', par.Narc, 'line', 'a_centr', 'obj', 'priv',  sloy])
      
