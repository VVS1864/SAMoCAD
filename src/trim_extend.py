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
            self.par.col = col
            self.par.cord_cord = False
            select_clone.Select_clone([self.par.col,], self.par, color = 'red')
            self.par.info.config(text = u'Escape - stop')
            self.par.dialog.config(text = (u'%s - object 2:') %(self.par.trim_extend))
            c = self.par.get_line_coord(self.par.col)
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
            self.par.col = el
            select_clone.Select_clone([self.par.col,], self.par, color = 'red')
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
                col = self.par.collection
                self.par.sbros()
                if self.par.col in col:
                    col.remove(self.par.col)
                if self.par.trim_extend == 'Trim':
                    for el in col:
                        if el[0] == 'L':
                            self.par.c.delete('C'+el)
                            fill, width, sloy, stipple, c, factor_stip = self.par.get_line_conf(el)
                            cNew = trim_line(self.par.ex, self.par.ey, self.par.ex2, self.par.ey2, x, y, c)
                            if cNew:
                                self.par.delete(elements = (el,))
                                
                                self.par.c_line(cNew[0], cNew[1], cNew[2], cNew[3], fill=fill, width=width, sloy=sloy, stipple=stipple, factor_stip=factor_stip)
                else:
                    for el in col:
                        if el[0] == 'L':
                            fill, width, sloy, stipple, c = self.par.get_line_conf(el)
                            cNew = extend_line(self.par.ex, self.par.ey, self.par.ex2, self.par.ey2, c)
                            if cNew:
                                self.par.delete(elements = (el,))
                                self.par.c_line(cNew[0], cNew[1], cNew[2], cNew[3], fill=fill, width=width, sloy=sloy, stipple=stipple, factor_stip=factor_stip)
                if cNew:
                    self.par.changeFlag = True
                    self.par.enumerator_p()
        else:
            el = self.par.get_obj(x, y)
            if el:
                fill, width, sloy, stipple, c = self.par.get_line_conf(el)
                if self.par.trim_extend == 'Trim':
                    cNew = trim_line(self.par.ex, self.par.ey, self.par.ex2, self.par.ey2, x, y, c)
                else:
                    cNew = extend_line(self.par.ex, self.par.ey, self.par.ex2, self.par.ey2, c)
                if cNew:
                    self.par.delete(elements = (el,))
                    self.par.c_line(cNew[0], cNew[1], cNew[2], cNew[3], fill=fill, width=width, sloy=sloy, stipple=stipple)
                    self.par.changeFlag = True
                    self.par.enumerator_p()
            else:
                self.par.rectx = x
                self.par.recty = y
                self.par.c.bind_class(self.par.c, "<Motion>", self.par.resRect)

            
            
