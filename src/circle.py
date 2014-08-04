# -*- coding: utf-8 -*-
from math import sqrt
#КРУГ
#События
class Circle:
    def __init__(self, par):
        self.par = par
        self.risCircle()
        
    def risCircle(self):
        self.par.kill()
        self.par.standart_unbind()
        self.par.old_func = 'self.risCircle()'
        self.par.c.bind('<Button-1>', self.circle)
        self.par.dialog.config(text = 'Circle - center point:')
        self.par.info.config(text = 'Enter - stop')

    def circle(self, event):
        self.par.command.focus_set()
        self.par.set_coord()
        self.par.ex = self.par.priv_coord[0]
        self.par.ey = self.par.priv_coord[1]
        self.par.c.bind_class(self.par.c,"<1>", self.circle2)
        self.par.dialog.config(text = 'Circle - radius:')
        self.par.circle_clone = True

    def circle2(self, event=None):
        self.par.command.focus_set()
        self.par.ex2 = self.par.priv_coord[0]
        self.par.ey2 = self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        self.par.ex2,self.par.ey2 = self.par.commer(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
        if event:
            c_circle(self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
            self.par.history_undo.append(('c_', self.par.Ncircle))
            #self.par.com = None
            self.par.changeFlag = True
            self.par.circle_clone = False
            self.par.enumerator_p()
            self.par.risCircle()

        else:
            self.par.set_coord()
            c_circle(self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2, temp = 'Yes')
        
#Отрисовка
def c_circle(par, x0, y0, xr = None, yr = None, width = None, sloy = None, fill = None, R = None, ID = None, temp = None):
    if sloy == None:
        fill = par.color
        width = par.width
        sloy = par.sloy
    width = int(width)
    if not temp:
        if not ID:
            par.Ncircled+=1
            ID = par.Ncircle = 'c' + str(par.Ncircled)
            
        id_dict = {}
        if R == None:
            R = sqrt((xr-x0)*(xr-x0) + (yr-y0)*(yr-y0))
        x1=x0-R
        x2=x0+R
        y1=y0-R
        y2=y0+R
        s = R/20.0
        R = par.n_coordinator(R)
        id = par.c.create_oval(x1,y1,x2,y2,outline=fill, full=None,width=width,tags = ('obj', ID))
        id_dict[id] = ('cir', 'priv')
        id = par.c.create_line(x0-s,y0-s,x0+s,y0+s,fill=fill,tags = ('obj', ID, 'cir_centr'))
        id_dict[id] = ('line', 'priv', 'cir_centr')
        id = par.c.create_line(x0+s,y0-s,x0-s,y0+s,fill=fill,tags = ('obj', ID, 'cir_centr'))
        id_dict[id] = ('line', 'priv', 'cir_centr')
        par.ALLOBJECT[ID] = {'object':'circle', 'fill':fill, 'width':width, 'sloy':sloy, 'R':R, 'id':id_dict}

    else:
        if R == None:
            R = sqrt((xr-x0)*(xr-x0) + (yr-y0)*(yr-y0))
        x1=x0-R
        x2=x0+R
        y1=y0-R
        y2=y0+R
        s = R/20.0
        R = par.n_coordinator(R)
        par.c.create_oval(x1,y1,x2,y2,outline=fill, full=None,width=width,tags = ('obj', 'temp'))
        par.c.create_line(x0-s,y0-s,x0+s,y0+s,fill=fill,tags = ('obj', 'temp'))
        par.c.create_line(x0+s,y0-s,x0-s,y0+s,fill=fill,tags = ('obj', 'temp'))
        
        
