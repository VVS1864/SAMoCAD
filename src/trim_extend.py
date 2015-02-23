# -*- coding: utf-8; -*-
import src.calc as calc#import extend_line, trim_line
import src.select_clone as select_clone
import src.grab_object as grab_object
import src.sectors_alg as sectors_alg
import wx

class Trim:
    def __init__(self, par):
        par.trim_extend = 'Trim'
        c = Object(par)

class Extend:
    def __init__(self, par):
        par.trim_extend = 'Extend'
        c = Object(par)

class Object:
    def __init__(self, par):
        self.par = par
        self.trimEvent1()
        
    def trimEvent1(self):
        #self.par.red_line = True
        print 111
        self.par.focus_cmd()
        if self.par.collection and len(self.par.collection)==1:
            self.par.rline = self.par.collection[0]
            
            self.par.kill()
            self.par.resFlag = True
            self.par.snap_flag = False

            #self.par.cord_cord = False
            self.par.red_line_data, self.par.red_line_color = select_clone.select_clone(
                self.par,
                [self.par.rline,],
                [255, 0, 0],
                )
            #self.par.red_line_data.extend(clone_data)
            #self.par.red_line_color.extend(clone_color)
            self.par.info.SetValue('%s - object 2:' %(self.par.trim_extend))
            self.par.info2.SetValue('Escape - stop')
            

            c = self.par.ALLOBJECT[self.par.rline]['coords'][0]
            self.par.ex = c[0]
            self.par.ey = c[1]
            self.par.ex2 = c[2]
            self.par.ey2 = c[3]
            #print self.par.ex, self.par.ey, self.par.ex2, self.par.ey2
            self.par.c.Unbind(wx.EVT_LEFT_DOWN)
            self.par.c.Bind(wx.EVT_LEFT_DOWN, self.trimEvent3)

            #self.par.c.bind('<Button-1>', self.trimEvent3)
            #self.par.c.config(cursor = 'iron_cross')
        else:
            self.par.kill()
            self.par.info.SetValue('%s - object 1:' %(self.par.trim_extend))
            self.par.info2.SetValue('Escape - stop')
            
            #self.par.c.bind('<Button-1>', self.trimEvent2)
            self.par.c.Unbind(wx.EVT_LEFT_DOWN)
            self.par.c.Bind(wx.EVT_LEFT_DOWN, self.trimEvent2)

        #self.par.c.Unbind(wx.EVT_MOTION)
        #self.par.c.unbind_class(self.par.c,"<Motion>")
        #self.par.c.unbind('<Shift-Button-1>')
        #self.par.c.unbind_class(self.par.master1,"<Return>")

    def trimEvent2(self, event):
        self.par.focus_cmd()
        x = self.par.x_priv
        y = self.par.y_priv
        #object = #self.par.get_current_objects(rect)
        #el = self.par.get_obj(event.x, event.y)
        if self.par.current:
            self.par.info.SetValue('%s - Cuted objects:'%(self.par.trim_extend))
            self.par.c.Unbind(wx.EVT_LEFT_DOWN)
            self.par.c.Bind(wx.EVT_LEFT_DOWN, self.trimEvent3)
            #self.par.get_line_coord(el)
            self.par.rline = self.par.current
            self.par.red_line_data, self.par.red_line_color = select_clone.select_clone(
                self.par,
                [self.par.rline,],
                [255, 0, 0],
                )
            c = self.par.ALLOBJECT[self.par.current]['coords'][0]
            self.par.ex = c[0]
            self.par.ey = c[1]
            self.par.ex2 = c[2]
            self.par.ey2 = c[3]
            #print self.par.ex, self.par.ey, self.par.ex2, self.par.ey2
            #self.par.c.config(cursor = 'iron_cross')
            

    def trimEvent3(self, event):
        self.par.focus_cmd()
        #self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        #self.par.ex2,self.par.ey2 = self.par.coordinator(self.par.ex2,self.par.ey2)
        #self.par.set_coord()
        #x = event.x
        #y = event.y
        x = self.par.x_priv
        y = self.par.y_priv
        cNew = None
        if self.par.rect:
            #self.par.c.delete(self.par.rect)#Удалить прямоугольник выделения
            self.par.rect = False
            self.par.rect_data = []
            self.par.rect_color = []
            #self.par.c.unbind_class(self.par.c,"<Motion>")
            #x1 = min(self.par.rectx, x)
            #x2 = max(self.par.rectx, x)
            #y1 = min(self.par.recty, y)
            #y2 = max(self.par.recty, y)
            x1 = x
            y1 = y
            x2 = self.par.rectx
            y2 = self.par.recty
            
            objects = grab_object.select(self.par, [x1, y1, x2, y2], False)
            #c = self.par.c.find_overlapping(x1,y1,x2,y2)
            x = (x1+x2)/2.0
            y = (y1+y2)/2.0
            #self.par.mass_collektor(c, 'select')
            print '111', objects
            print [x1, y1, x2, y2]
            
            if objects: #self.par.collection:
                self.trim_extend(x, y, objects)
                #col = self.find_rline()
                #self.par.changeFlag = True
                #self.par.enumerator_p() 
                        
        else:
            el = self.par.current#self.par.get_obj(x, y)
            print '111', self.par.current
            if el:
                objects = [el,]
            #col = self.find_rline()
            #if col:
                self.trim_extend(x, y, objects)
                #cNew = self.par.ALLOBJECT[el]['class'].trim_extend(x, y, self.par.trim_extend)
                #if cNew:
                    #pass
                    #self.par.changeFlag = True
                    #self.par.enumerator_p()
            else:
                self.par.rectx = x
                self.par.recty = y
                self.par.rect = True
                #self.par.c.bind_class(self.par.c, "<Motion>", self.par.resRect)
        #event.Skip()
        self.par.c.Refresh()
        
    def trim_extend(self, x, y, objects):
        print objects
        del_objs = []
        start = self.par.total_N
        for el in objects:
            #if el[0] == 'L':
            cNew = self.par.ALLOBJECT[el]['class'].trim_extend(x, y, self.par.ex, self.par.ey, self.par.ex2, self.par.ey2, self.par.trim_extend)
            if cNew:
                del_objs.append(el)
        end = self.par.total_N
        #if range(start+1, end+1):
        if cNew:
            self.par.ALLOBJECT, self.par.sectors = sectors_alg.quadric_mass(
                self.par.ALLOBJECT,
                range(start+1, end+1),
                self.par.sectors,
                self.par.q_scale
                )
        if del_objs:
            self.par.delete_objects(del_objs, False)
            
        self.par.change_pointdata()
            
            
            
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
            
