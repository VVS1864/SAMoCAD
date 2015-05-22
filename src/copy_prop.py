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
        #self.par.standart_unbind()
        self.par.focus_cmd()
        if self.par.collection and len(self.par.collection)==1:
            self.par.rline = self.par.collection[0]
            self.par.kill()
            self.par.red_line_data, self.par.red_line_color = select_clone.select_clone(
                self.par,
                [self.par.rline,],
                [255, 0, 0],
                )
            
            #col = self.par.collection[0]
            

            self.par.resFlag = True
            self.par.snap_flag = False
            #self.par.current_flag = False
            
            self.par.info.SetValue('Copy properties - object 2:')
            self.par.info2.SetValue('Escape - stop')
            
            self.copy_prop3(self.par.rline)
            
            self.par.c.Unbind(wx.EVT_LEFT_DOWN)
            self.par.c.Bind(wx.EVT_LEFT_DOWN, self.copy_prop4)

            #self.par.c.config(cursor = 'iron_cross')
        else:
            self.par.kill()
            self.par.snap_flag = False
            self.par.info.SetValue('Copy properties - object 1:')
            self.par.info2.SetValue('Escape - stop')

            self.par.c.Unbind(wx.EVT_LEFT_DOWN)
            self.par.c.Bind(wx.EVT_LEFT_DOWN, self.copy_prop2)
            
            #self.par.c.bind('<Button-1>', self.copy_prop2)
        
        #self.par.resFlag = True    
        #self.par.c.unbind_class(self.par.c,"<Motion>")
        #self.par.unpriv = True
        #self.par.c.unbind_class(self.par.master1,"<Return>")

    def copy_prop2(self, event = None):
        self.par.focus_cmd()
        # Выбрать объект для копирования свойств
        #el = self.par.get_obj(event.x, event.y, 'all')
        el = self.par.current
        if el:
            self.par.rline = el
            self.par.info.SetValue('Copying properties - object 2:')
            #self.par.c.bind('<Button-1>', self.copy_prop4)
            self.par.c.Unbind(wx.EVT_LEFT_DOWN)
            self.par.c.Bind(wx.EVT_LEFT_DOWN, self.copy_prop4)
            self.copy_prop3(el)
            self.par.red_line_data, self.par.red_line_color = select_clone.select_clone(
                self.par,
                [self.par.rline,],
                [255, 0, 0],
                )
            #self.par.c.config(cursor = 'iron_cross')
        
    def copy_prop3(self, col):
        self.par.focus_cmd()
        self.par.prop = {}
        for p in self.par.ALLOBJECT[col]:
            if p in self.par.properties.keys():#('color', 'width', 'stipple', 'factor_stipple', 'text_size', 'layer', 's', 'vr_s', 'vv_s', 'arrow_s', 'type_arrow', 'text_s_s', 'text_w', 'text_font', 'dim_text_size', 'dim_text_s_s', 'dim_text_w', 'dim_text_font'):                       
                self.par.prop[p] = copy(self.par.ALLOBJECT[col][p])

    def copy_prop4(self, event):
        #self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        #self.par.ex2,self.par.ey2 = self.par.coordinator(self.par.ex2,self.par.ey2)
        #self.par.set_coord()
        #x = event.x
        #y = event.y
        self.par.focus_cmd()
        x = self.par.x_priv
        y = self.par.y_priv
        print self.par.prop
        if self.par.rect:
            #self.par.c.delete(self.par.rect)#Удалить прямоугольник выделения
            self.par.rect = None
            self.par.rect_data = []
            self.par.rect_color = []
            #self.par.unpriv = True
            #self.par.c.bind_class(self.par.c,"<Motion>", self.par.gpriv)
            #x1 = min(self.par.rectx, self.par.rectx2)
            #x2 = max(self.par.rectx, self.par.rectx2)
            #y1 = min(self.par.recty, self.par.recty2)
            #y2 = max(self.par.recty, self.par.recty2)
            #c = self.par.c.find_overlapping(x1,y1,x2,y2)
            #self.par.mass_collektor(c, 'select')
            x1 = x
            y1 = y
            x2 = self.par.rectx
            y2 = self.par.recty
            objects = grab_object.select(self.par, [x1, y1, x2, y2], False)
            if objects:
                edit_prop.Edit_prop(self.par, self.par.prop, objects)
                #self.par.sbros()
                #self.par.changeFlag = True
                #self.par.enumerator_p()
        else:
            el = self.par.current
            #el = self.par.get_obj(event.x, event.y, 'all')
            if el:
                
                #self.par.collection = [el,]
                edit_prop.Edit_prop(self.par, self.par.prop, [el,])
                #self.par.sbros()
                #self.par.changeFlag = True
                #self.par.enumerator_p()
            else:
                self.par.rectx = x
                self.par.recty = y
                self.par.rect = True
                #self.par.unpriv = False
                #self.par.c.bind_class(self.par.c, "<Motion>", self.par.resRect)
        self.par.c.Refresh()
