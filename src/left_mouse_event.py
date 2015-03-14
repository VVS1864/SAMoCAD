# -*- coding: utf-8 -*-
import wx
import src.grab_object as grab_object
import src.edit as edit
def left_mouse_event(self):
    x = self.x_priv
    y = self.y_priv
    state = wx.GetMouseState()
    if self.resFlag:
        pass
    else:
        #добавить - убрать из коллекции
        if state.ShiftDown():
            select = 'deselect'
        else:
            select = 'select'
            
        if self.rect:
            self.rectx2 = x
            self.recty2 = y
            objects = grab_object.select(self, [self.rectx, self.recty, self.rectx2, self.recty2])
            self.mass_collector(objects, select)
            self.amount_of_select()
            self.rect = False
            self.rect_data = []
            self.rect_color = []
            self.c.Refresh()
            
        elif self.current_select:
            self.mass_collector([self.current,], select = select)
            self.amount_of_select()
            self.c.Refresh()
            
        elif not self.current_change:
            #Если объект под курсором нельзя изменить
            self.rect = True
            self.rectx = x
            self.recty = y
        elif self.current_change:
            edit.Object(self)
    if not self.current_change:        
        self.standart_state()
    #e.Skip()
    self.focus_cmd()
