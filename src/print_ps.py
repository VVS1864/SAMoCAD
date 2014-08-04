# -*- coding: utf-8 -*-
import tkFileDialog
import os
zoomm = 0.8
zoomp = 1.0/0.8

#Печать картинки в постскрипт
class Print_PS:
    def __init__(self, par):
        self.par = par
        self.print_postScript()
        
    def print_postScript(self):
        self.par.kill()
        self.par.standart_unbind()
        self.par.dialog.config(text = (u'Print scale [%s]:') %(self.par.old_print_scale))
        self.par.info.config(text = u'Escape - stop')
        self.par.old_func = 'self.print_postScript()'
        self.par.c.unbind_class(self.par.c,"<Motion>")
        self.par.c.unbind_class(self.par.c,"<1>")
        self.par.c.bind_class(self.par.master1,"<Return>", self.print_postScript0)

    def print_postScript0(self, event = None):
        self.par.comOrKill()
        if self.par.com:
            self.par.pd = float(self.par.com)
            self.par.old_print_scale = self.par.pd
        else:
            self.par.pd = self.par.old_print_scale
        self.par.kill()
        self.par.dialog.config(text = u'Print rectangle - point 1:')
        self.par.info.config(text = u'Escape - stop')
        self.par.old_func = 'self.print_postScript()'
        self.par.resFlag = True
        self.par.c.unbind('<Shift-Button-1>')
        self.par.c.unbind_class(self.par.master1,"<Return>")
        self.par.c.bind_class(self.par.c,"<1>", self.print_postScript2)

    def printRect(self, event):
        if self.par.rect != None:#Если прямоугольник есть - удалить его
            self.par.c.delete(self.par.rect)
        self.par.ex2=self.par.priv_coord[0]
        self.par.ey2=self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        self.par.set_coord()
        self.par.rect=self.par.c.create_rectangle(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2,fill=None,outline='red', tags = 'rect')#Нарисовать заново по новым координатам

    def print_postScript2(self, event):
        self.par.dialog.config(text = u'Print rectangle - point 2:')
        self.par.ex = self.par.priv_coord[0]
        self.par.ey = self.par.priv_coord[1]
        self.par.c.bind_class(self.par.master1, "<Motion>", self.printRect)
        self.par.c.bind_class(self.par.c,"<1>", self.print_postScript3)
        self.par.set_coord()

    def print_postScript3(self, event):
        self.par.ex2 = self.par.priv_coord[0]
        self.par.ey2 = self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        self.par.c.delete(self.par.rect)#Удалить прялиугольник выделения
        x = max(self.par.ex, self.par.ex2)
        xm = min(self.par.ex, self.par.ex2)
        y = max(self.par.ey, self.par.ey2)
        ym = min(self.par.ey, self.par.ey2)

        t=self.par.c.find_withtag('c1')#Найти значек привязки
        if t:#Если таковой имеется
            self.par.c.delete('c1')#Удалить значек
        c = self.par.c.find_overlapping(xm,ym,x,y)
        self.par.mass_collektor(c, 'select')
        self.print_p(xm,ym,x,y)
        self.par.c.unbind_class(self.par.c, "<Motion>")#Вернуть события в исходное состояние
        self.par.c.bind_class(self.par.c,"<Motion>", self.par.gpriv)
        self.par.c.bind_class(self.par.master1,"<Return>", self.par.old_function)
        self.par.dialog.config(text = u'Command:')
        self.par.kill()

    def print_p(self, x1, y1, x2, y2):
        opt = options = {}
        options['defaultextension'] = '.ps'
        options['filetypes'] = [('postscript', '.ps'),
                                ('all files', '.*')]
        options['initialdir'] = self.par.appPath
        options['initialfile'] = 'draft_1'
        options['parent'] = self.par.master1
        options['title'] = 'Save to PostScript'
        f = tkFileDialog.asksaveasfilename(**opt)
        if f:
            self.par.width_list = []
            self.par.c.delete('clone')
            for i in self.par.collection:
                fill = self.par.ALLOBJECT[i]['fill']
                if fill == 'white':
                    self.par.back_color('black', i)
            if self.par.zoomOLD <= -19:
                self.par.c.itemconfig('t_LOD', state = 'normal')
                self.par.c.itemconfig('snap_text', stipple = ('@'+os.path.join(self.par.appPath, 'res', '00.xbm')))
            height = y2-y1
            width = x2-x1
            if self.par.zoomOLD != 0:
                if self.par.zoomOLD>0:
                    self.par.c.scale('obj',x1,y1,zoomm**self.par.zoomOLD,zoomm**self.par.zoomOLD)
                    x2 *= zoomm**self.par.zoomOLD
                    y2 *= zoomm**self.par.zoomOLD
                else:
                    zoomOLDx=self.par.zoomOLD*(-1)
                    self.par.c.scale('obj',x1,y1,zoomp**zoomOLDx,zoomp**zoomOLDx)
                    height *= zoomp**zoomOLDx
                    width *= zoomp**zoomOLDx
            t=self.par.c.find_withtag('c1')#Найти значек привязки
            if t:#Если таковой имеется
                self.par.c.delete('c1')#Удалить значек
            for i in ('cir_centr', 'a_centr'):
                self.par.c.itemconfig(i, state = 'hidden')
            if 'trace' in self.par.ALLOBJECT:
                del self.par.ALLOBJECT['trace']
                self.par.c.delete('trace')
            self.widther('up')
            heightt = str(height/self.par.pd)+'m'
            widtht = str(width/self.par.pd)+'m'
            self.par.c.postscript(file=f,x=x1,y=y1,colormode="color", height=height, width=width, pageheight = heightt, pagewidth = widtht)
            if self.par.zoomOLD != 0:
                if self.par.zoomOLD>0:
                    self.par.c.scale('obj',x1,y1,zoomp**self.par.zoomOLD,zoomp**self.par.zoomOLD)

                else:
                    zoomOLDx=self.par.zoomOLD*(-1)
                    self.par.c.scale('obj',x1,y1,zoomm**zoomOLDx,zoomm**zoomOLDx)

            for i in ('cir_centr', 'a_centr'):
                self.par.c.itemconfig(i, state = 'normal')
            self.widther('down')
            for i in self.par.collection:
                fill = self.par.ALLOBJECT[i]['fill']
                if fill == 'white':
                    self.par.back_color('white', i)
            if self.par.zoomOLD <= -19:
                self.par.c.itemconfig('t_LOD', state = 'hidden')
                self.par.c.itemconfig('snap_text', stipple = '')

    def widther(self, e):
        if e == 'up':
            for j in self.par.collection:
                for i in self.par.ALLOBJECT[j]['id']:
                    w = self.par.c.itemcget(i, 'width')
                    self.par.width_list.append((i, w))
                    self.par.c.itemconfig(i, width = float(w)*self.par.pd/5.0)
        else:
            if self.par.width_list:
                for j in self.par.width_list:
                    self.par.c.itemconfig(j[0], width = j[1])
                del self.par.width_list
