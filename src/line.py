# -*- coding: utf-8; -*-
from math import sqrt, copysign
from os import path
#ЛИНИЯ
class Line:
    def __init__(self, par):
        self.par = par
        self.risLine()
        
    def risLine(self):
        self.par.kill()
        self.par.standart_unbind()
        self.par.old_func = 'self.risLine()'
        self.par.c.bind('<Button-1>', self.line)
        self.par.dialog.config(text = u'Line - point 1:')
        self.par.info.config(text = u'Enter - stop')

    def line(self, event):
        self.par.command.focus_set()
        self.par.set_coord()
        self.par.ex = self.par.priv_coord[0]
        self.par.ey = self.par.priv_coord[1]
        self.par.c.bind_class(self.par.c,"<1>", self.line2)
        self.par.c.bind_class(self.par.c,"<Shift-1>", self.line2_shift)
        self.par.dialog.config(text = u'Line - next point:')
        self.par.line_clone = True

    def line2_shift(self, event):#Ести нажат Shift если не режим орто - чертится в режиме орто + ловит не точку привязки, а ее проекцию на ось, если режим орто - чертится как без орто
        self.par.command.focus_set()
        self.par.ex2 = self.par.priv_coord[0]
        self.par.ey2 = self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        if self.par.ortoFlag == False:
            self.par.ex2,self.par.ey2 = self.par.orto(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
        c_line(self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2,fill='white',width=3)
        self.par.ex=self.par.ex2
        self.par.ey=self.par.ey2
        self.par.set_coord()
        self.par.changeFlag = True
        self.par.enumerator_p()
        self.par.com = None
        self.par.command.delete(0, 'end')

    def line2(self, event=None):
        self.par.ex2 = self.par.priv_coord[0]
        self.par.ey2 = self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        self.par.ex2,self.par.ey2 = self.par.commer(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
        self.par.set_coord()
        if self.par.tracingFlag or self.par.tracing_obj_Flag:
            if self.par.tracingFlag:
                self.par.trace_on = True
            if self.par.tracing_obj_Flag:
                self.par.trace_obj_on = True
            self.par.trace_x1, self.par.trace_y1 = self.par.ex,self.par.ey
            self.par.trace_x2, self.par.trace_y2 = self.par.ex2,self.par.ey2
        if self.par.ortoFlag == True and self.par.com == None:
            if len(self.par.find_privs) == 1:
                self.par.ex2,self.par.ey2=self.par.orto(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
        if event:
            self.par.command.focus_set()
            c_line(self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
            self.par.history_undo.append(('c_', self.par.Nline))
            self.par.ex=self.par.ex2
            self.par.ey=self.par.ey2
            self.par.set_coord()
            self.par.changeFlag = True
            self.par.enumerator_p()
            self.par.com = None
            self.par.command.delete(0, 'end')
        else:
            c_line(self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2, temp = 'Yes')

def c_line(par, x1, y1, x2, y2, width = None, sloy = None, fill = None, stipple = None, tip = 'norm', temp = None):
    if sloy == None:
        fill = par.color
        width = par.width
        sloy = par.sloy
        stipple = par.stipple
    if not temp:
        width = int(width)
        par.Nlined+=1
        par.Nline = 'L' + str(par.Nlined)
        id_dict = {}
        if tip == 'norm':
            if stipple == None:
                id = par.c.create_line(x1,y1,x2,y2, fill=fill,width=width,tags = ('obj', par.Nline, 'sel'))
                id_dict[id] = ('line', 'priv', 'lin')
            else:
                id = d_line(par, x1,y1,x2,y2, dash = stipple, fill=fill,width=width,tags = ('obj', par.Nline, 'sel'))
                if id:
                    id_dict.update(id)
                    id = par.c.create_line(x1,y1,x2,y2, width=3, stipple = ('@'+path.join(par.appPath, 'res', '00.xbm')), tags = ('obj', par.Nline, 'sel'))
                    id_dict[id] = ('line', 'priv', 'lin')
                else:
                    return
        elif tip == 'temp':
            width = 1
            sloy = 'temp'
            fill = 'gray'
            id = par.c.create_line(x1,y1,x2,y2,fill=fill,width=width,tags = ('obj', par.Nline, 'sel'))
            id_dict = id_dict[id] = ('line', 'priv', 'temp')
        par.ALLOBJECT[par.Nline] = {'object':'line', 'fill':fill, 'width':width, 'sloy':sloy, 'stipple':stipple, 'factor_stip':par.stipple_size, 'id':id_dict}
    else:
        if stipple == None:
            par.c.create_line(x1,y1,x2,y2, fill=fill,width=width,tags = ('obj', 'temp'))
            
        else:
            d_line(par, x1,y1,x2,y2, dash = stipple, fill=fill,width=width,tags = ('obj', 'temp'))
            
            par.c.create_line(x1,y1,x2,y2, width=3, stipple = ('@'+path.join(par.appPath, 'res', '00.xbm')), tags = ('obj', 'temp'))
            
def d_line(par, x1,y1,x2,y2, dash, fill, width, tags):
    id_dict = {}
    dash = map(par.coordinator2, dash)
    xm = min(x1, x2)
    ym = min(y1, y2)
    xb = max(x1, x2)
    yb = max(y1, y2)
    dx = x1 - x2
    dy = y1 - y2
    d_dx = x1
    d_dy = y1
    pos = 0
    while 1:
        pos+=1
        if pos == len(dash)+1:
            pos = 1
        d = dash[pos-1]
        try:
            dx0 = sqrt((d*d * dx*dx)/(dy*dy + dx*dx))
        except ZeroDivisionError:
            return None
        if dy == 0:
            dy0 = 0
        elif dx == 0:
            dy0 = d * copysign(1, dy)
        else:
            dy0 = dx0 * dy / dx
        i = 1
        if x1 < x2:
            i =- 1
        xi1 = d_dx
        yi1 = d_dy
        xi2 = xi1 - i * dx0
        yi2 = yi1 - i * dy0
        d_dx = xi2
        d_dy = yi2
        ex = [xi1, xi2]
        ey = [yi1, yi2]
        cor = False
        for u in ex:
            if xm <= u <= xb:
                pass
            else:
                ind = ex.index(u)
                del ex[ind]
                if u < xm:
                    u = xm
                else:
                    u = xb
                ex.insert(ind, u)
                cor = True
        for u in ey:
            if ym <= u <= yb:
                pass
            else:
                ind = ey.index(u)
                del ey[ind]
                if u < ym:
                    u = ym
                else:
                    u = yb
                ey.insert(ind, u)
                cor = True

        if xm <= ex[1] <= xb and xm <= ex[0] <= xb and ym <= ey[1] <= yb and ym <= ey[0] <= yb:
            if pos % 2 != 0:
                id = par.c.create_line(ex[0],ey[0],ex[1],ey[1], fill=fill,width=width,tags=tags)
                id_dict[id] = ('line',)
            if cor == True:
                return id_dict 
                #break
        else:
            return id_dict 
            #break

