# -*- coding: utf-8; -*-
import wx
from copy import copy
import src.edit_prop as edit_prop
import src.grab_object as grab_object
import src.select_clone as select_clone
#КОПИРОВАНИЕ СВОЙСТВ
class Copy_prop:
    def __init__(self, par):
        self.par = par
        self.copy_prop()
        
    def copy_prop(self):
        self.par.focus_cmd()
        if self.par.collection and len(self.par.collection)==1:
            self.par.rline = self.par.collection[0]
            self.par.kill()
            self.par.red_line_data, self.par.red_line_color = select_clone.select_clone(
                self.par,
                [self.par.rline,],
                [255, 0, 0],
                )            

            self.par.resFlag = True
            self.par.snap_flag = False
            
            self.par.info.SetValue('Copy properties - object 2:')
            self.par.info2.SetValue('Escape - stop')
            
            self.copy_prop3(self.par.rline)
            
            self.par.c.Unbind(wx.EVT_LEFT_DOWN)
            self.par.c.Bind(wx.EVT_LEFT_DOWN, self.copy_prop4)

        else:
            self.par.kill()
            self.par.snap_flag = False
            self.par.info.SetValue('Copy properties - object 1:')
            self.par.info2.SetValue('Escape - stop')

            self.par.c.Unbind(wx.EVT_LEFT_DOWN)
            self.par.c.Bind(wx.EVT_LEFT_DOWN, self.copy_prop2)


    def copy_prop2(self, event = None):
        self.par.focus_cmd()
        # Выбрать объект для копирования свойств
        el = self.par.current
        if el:
            self.par.rline = el
            self.par.info.SetValue('Copying properties - object 2:')
            self.par.c.Unbind(wx.EVT_LEFT_DOWN)
            self.par.c.Bind(wx.EVT_LEFT_DOWN, self.copy_prop4)
            self.copy_prop3(el)
            self.par.red_line_data, self.par.red_line_color = select_clone.select_clone(
                self.par,
                [self.par.rline,],
                [255, 0, 0],
                )
        
    def copy_prop3(self, col):
        self.par.focus_cmd()
        self.par.prop = {}
        for p in self.par.ALLOBJECT[col]:
            if p in self.par.properties.keys():                      
                self.par.prop[p] = copy(self.par.ALLOBJECT[col][p])

    def copy_prop4(self, event):
        self.par.focus_cmd()
        x = self.par.x_priv
        y = self.par.y_priv
        if self.par.rect:
            self.par.rect = None
            self.par.rect_data = []
            self.par.rect_color = []
            x1 = x
            y1 = y
            x2 = self.par.rectx
            y2 = self.par.recty
            objects = grab_object.select(self.par, [x1, y1, x2, y2], False)
            if objects:
                edit_prop.Edit_prop(self.par, self.par.prop, objects)
        else:
            el = self.par.current
            if el:
                edit_prop.Edit_prop(self.par, self.par.prop, [el,])
            else:
                self.par.rectx = x
                self.par.recty = y
                self.par.rect = True
        self.par.c.Refresh()
