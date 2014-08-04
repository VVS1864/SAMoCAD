# -*- coding: utf-8; -*-
import time
#ПЕРЕМЕЩЕНИЕ
class Move_object:
    def __init__(self, par):
        self.par = par
        self.moveEvent()
        
    def moveEvent(self):
        if self.par.collection:
            self.par.standart_unbind()
            self.par.old_func = 'self.moveEvent()'
            self.par.resFlag = True
            self.par.c.bind_class(self.par.master1,"<Return>", self.par.kill)
            self.par.info.config(text = (u'Selected %s objects. Enter - stop') %(len(self.par.collection)))
            self.par.dialog.config(text = u'Move  - base point:')
            self.par.c.bind('<Button-1>', self.moveEvent2)
            #self.par.c.unbind('<Shift-Button-1>')
        else:
            self.par.info.config(text = u'Objects do not selected')

    def moveEvent2(self, event = None):
        if event:
            self.par.ex=self.par.priv_coord[0]
            self.par.ey=self.par.priv_coord[1]
            self.par.ex3,self.par.ey3 = self.par.ex,self.par.ey
        self.par.dialog.config(text = u'Move - insertion point:')
        self.par.command.focus_set()
        self.par.set_coord()
        self.par.c.bind('<Button-1>', self.moveEvent3)
        self.par.move_clone = True

    def moveEvent3(self, event = None):
        self.par.ex2=self.par.priv_coord[0]
        self.par.ey2=self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        if event:
            t1 = time.time()
            self.par.ex2,self.par.ey2 = self.par.commer(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
            if self.par.ortoFlag == True and self.par.com == None: #Если режим орто - сделать координаты орто
                self.par.ex2,self.par.ey2 = self.par.orto(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
            mover(self.par.collection, self.par)
            t2 = time.time()
            print 'move', t2-t1
            self.par.changeFlag = True
            self.par.enumerator_p()
            self.par.kill()
        else:
            self.par.ex3, self.par.ey3 = self.par.coordinator(self.par.ex3, self.par.ey3)
            self.par.ex2,self.par.ey2 = self.par.commer(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
            if self.par.ortoFlag == True and self.par.com == None: #Если режим орто - сделать координаты орто
                self.par.ex2,self.par.ey2 = self.par.orto(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
            if self.par.tracingFlag:
                self.par.trace_on = True
                self.par.trace_x1, self.par.trace_y1 = self.par.ex,self.par.ey
                self.par.trace_x2, self.par.trace_y2 = self.par.ex2,self.par.ey2
            collection = ['C' + x for x in self.par.collection]

            mover(collection, self.par, dx = self.par.ex2-self.par.ex3, dy = self.par.ey2-self.par.ey3)
            self.par.ex3 = self.par.ex2
            self.par.ey3 = self.par.ey2
            self.par.set_coord()

def mover(collection, par, dx = None, dy = None):
    if dx == None:
        dx = par.ex2-par.ex
        dy = par.ey2-par.ey
    for i in collection:
        #par.c.addtag_withtag('copy', i)
        par.c.move(i, dx, dy)
    #par.c.dtag('copy', 'copy')

def move_lines(x1, y1, x2, y2, lines):
    dx = x2 - x1
    dy = y2 - y1
    for ind, line in enumerate(lines):
        lines[ind] = [y+dx if indd%2 == 0 else y+dy for indd, y in enumerate(line)]

    return lines
