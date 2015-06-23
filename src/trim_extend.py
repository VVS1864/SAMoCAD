# -*- coding: utf-8; -*-
import src.calc as calc
import src.select_clone as select_clone
import src.grab_object as grab_object
import src.sectors_alg as sectors_alg
import wx
from base import Base

class Trim:
    def __init__(self, par):
        par.trim_extend = 'Trim'
        c = Object(par)

class Extend:
    def __init__(self, par):
        par.trim_extend = 'Extend'
        c = Object(par)

class Object(Base):
    def __init__(self, par):
        self.par = par
        self.trimEvent1()
        
    def trimEvent1(self):
        self.par.focus_cmd()
        if self.par.collection and len(self.par.collection)==1:
            self.par.rline = self.par.collection[0]
            
            self.par.kill()
            self.par.resFlag = True
            self.par.snap_flag = False

            self.par.red_line_data, self.par.red_line_color = select_clone.select_clone(
                self.par,
                [self.par.rline,],
                [255, 0, 0],
                )
            self.par.info.SetValue('%s - object 2:' %(self.par.trim_extend))
            self.par.info2.SetValue('Escape - stop')
            

            c = self.par.ALLOBJECT[self.par.rline]['coords'][0]
            self.par.ex = c[0]
            self.par.ey = c[1]
            self.par.ex2 = c[2]
            self.par.ey2 = c[3]
            self.par.c.Unbind(wx.EVT_LEFT_DOWN)
            self.par.c.Bind(wx.EVT_LEFT_DOWN, self.trimEvent3)

        else:
            self.par.kill()
            self.par.snap_flag = False
            self.par.info.SetValue('%s - object 1:' %(self.par.trim_extend))
            self.par.info2.SetValue('Escape - stop')
            
            self.par.c.Unbind(wx.EVT_LEFT_DOWN)
            self.par.c.Bind(wx.EVT_LEFT_DOWN, self.trimEvent2)

    def trimEvent2(self, event):
        self.par.focus_cmd()
        x = self.par.x_priv
        y = self.par.y_priv

        if self.par.current and self.par.ALLOBJECT[self.par.current]['object'] == 'line':
            self.par.info.SetValue('%s - Cuted objects:'%(self.par.trim_extend))
            self.par.c.Unbind(wx.EVT_LEFT_DOWN)
            self.par.c.Bind(wx.EVT_LEFT_DOWN, self.trimEvent3)

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
            

    def trimEvent3(self, event):
        self.par.focus_cmd()
        x = self.par.x_priv
        y = self.par.y_priv
        cNew = None
        if self.par.rect:

            self.par.rect = False
            self.par.rect_data = []
            self.par.rect_color = []
            x1 = x
            y1 = y
            x2 = self.par.rectx
            y2 = self.par.recty
            
            objects = grab_object.select(self.par, [x1, y1, x2, y2], False)
            x = (x1+x2)/2.0
            y = (y1+y2)/2.0
            
            if objects: 
                self.trim_extend(x, y, objects)
                        
        else:
            el = self.par.current
            if el:
                objects = [el,]
            
                self.trim_extend(x, y, objects)
                
            else:
                self.par.rectx = x
                self.par.recty = y
                self.par.rect = True
                
        #event.Skip()
        self.par.c.Refresh()
        
    def trim_extend(self, x, y, objects):
        del_objs = []
        start = self.par.total_N
        for el in objects:
            cNew = None
            if 'trim_extend' in dir(self.par.ALLOBJECT[el]['class']):
                cNew = self.par.ALLOBJECT[el]['class'].trim_extend(
                    x,
                    y,
                    self.par.ex,
                    self.par.ey,
                    self.par.ex2,
                    self.par.ey2,
                    self.par.trim_extend,
                    )
                if cNew:
                    del_objs.append(el)
        end = self.par.total_N
        new_objects = range(start+1, end+1)
        if del_objs:
            self.par.ALLOBJECT, self.par.sectors = sectors_alg.quadric_mass(
                self.par.ALLOBJECT,
                new_objects,
                self.par.sectors,
                self.par.q_scale
                )
            super(Object, self).add_history(objects = del_objs, mode = 'replace', objects_2 = new_objects)
            self.par.delete_objects(del_objs, False)
            
            self.par.change_pointdata()
            
