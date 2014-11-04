# -*- coding: utf-8; -*-
from calc import extend_line, trim_line
import select_clone
class Trim_extent:
    def __init__(self, par):
        self.par = par
        self.trimEvent1()
        
    def trimEvent1(self):
        self.par.red_line = True
        if self.par.collection and len(self.par.collection)==1:
            col = self.par.collection[0]
            self.par.resFlag = True
            self.par.kill()
            self.par.rline = col
            self.par.cord_cord = False
            select_clone.Select_clone([self.par.rline,], self.par, color = 'red')
            self.par.info.config(text = u'Escape - stop')
            self.par.dialog.config(text = (u'%s - object 2:') %(self.par.trim_extend))
            c = self.par.get_line_coord(self.par.rline)
            self.par.ex = c[0]
            self.par.ey = c[1]
            self.par.ex2 = c[2]
            self.par.ey2 = c[3]
            self.par.set_coord()
            self.par.c.bind('<Button-1>', self.trimEvent3)
            self.par.c.config(cursor = 'iron_cross')
        else:
            self.par.kill()
            self.par.info.config(text = u'Escape - stop')
            self.par.dialog.config(text = (u'%s - object 1:') %(self.par.trim_extend))
            self.par.c.bind('<Button-1>', self.trimEvent2)
        self.par.c.unbind_class(self.par.c,"<Motion>")
        self.par.c.unbind('<Shift-Button-1>')
        self.par.c.unbind_class(self.par.master1,"<Return>")

    def trimEvent2(self, event):
        el = self.par.get_obj(event.x, event.y)
        if el:
            self.par.dialog.config(text = (u'%s - object 2:') %(self.par.trim_extend))
            self.par.c.bind('<Button-1>', self.trimEvent3)
            c = self.par.get_line_coord(el)
            self.par.rline = el
            select_clone.Select_clone([self.par.rline,], self.par, color = 'red')
            self.par.ex = c[0]
            self.par.ey = c[1]
            self.par.ex2 = c[2]
            self.par.ey2 = c[3]
            self.par.set_coord()
            self.par.c.config(cursor = 'iron_cross')
            

    def trimEvent3(self, event):
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        self.par.ex2,self.par.ey2 = self.par.coordinator(self.par.ex2,self.par.ey2)
        self.par.set_coord()
        x = event.x
        y = event.y
        cNew = None
        if self.par.rect:
            self.par.c.delete(self.par.rect)#Удалить прямоугольник выделения
            self.par.rect = None
            self.par.c.unbind_class(self.par.c,"<Motion>")
            x1 = min(self.par.rectx, self.par.rectx2)
            x2 = max(self.par.rectx, self.par.rectx2)
            y1 = min(self.par.recty, self.par.recty2)
            y2 = max(self.par.recty, self.par.recty2)
            c = self.par.c.find_overlapping(x1,y1,x2,y2)
            x = (x1+x2)/2.0
            y = (y1+y2)/2.0
            self.par.mass_collektor(c, 'select')
            
            
            if self.par.collection:
                col = self.find_rline()
                for el in col:
                    if el[0] == 'L':
                        cNew = self.par.ALLOBJECT[el]['class'].trim_extend(x, y, self.par.trim_extend)
                if cNew:
                    self.par.changeFlag = True
                    self.par.enumerator_p()         
        else:
            el = self.par.get_obj(x, y)
            self.par.collection = [el,]
            col = self.find_rline()
            if col:
                cNew = self.par.ALLOBJECT[el]['class'].trim_extend(x, y, self.par.trim_extend)
                if cNew:
                    self.par.changeFlag = True
                    self.par.enumerator_p()
            else:
                self.par.rectx = x
                self.par.recty = y
                self.par.c.bind_class(self.par.c, "<Motion>", self.par.resRect)

    def find_rline(self):
        if self.par.collection:
            col = self.par.collection
            self.par.collection = []
            self.par.c.delete('clone')
            select_clone.Select_clone([self.par.rline,], self.par, color = 'red')
            if self.par.rline in col:
                col.remove(self.par.rline)
            if col == [None]:
                col = None
            return col
            
