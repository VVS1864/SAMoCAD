# -*- coding: utf-8 -*-
from src.base import Base
import src.select_clone as select_clone
import wx
class Edit_text(Base):
    def __init__(self, par, obj):
        self.obj = obj
        super(Edit_text, self).__init__(par)
        self.edit_textEvent()

    def edit_textEvent(self):
        self.par.kill()
        super(Edit_text, self).Y_N(self.edit_textEvent2, 'Edit ext:')
        self.par.red_line_data, self.par.red_line_color = select_clone.select_clone(
                self.par,
                [self.obj,],
                [255, 0, 0],
                )
        text = self.par.ALLOBJECT[self.obj]['text']
        if text:
            self.par.cmd.SetValue(text)
        
    def edit_textEvent2(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_RETURN:
            cd = self.par.ALLOBJECT[self.obj].copy()
            cd['text'] = self.par.cmd.GetValue()
            if cd['text'] == '':
                self.par.kill()
                return
            cd['in_mass'] = False
            cd['temp'] = False
            self.par.ALLOBJECT[self.obj]['class'].create_object(cd)
            self.par.delete_objects([self.obj,], False)
            self.par.change_pointdata()
            self.par.kill()
            return
            
        elif key == wx.WXK_ESCAPE:
            self.par.kill()
        
        else:
            event.Skip()
            return
        
        
    
