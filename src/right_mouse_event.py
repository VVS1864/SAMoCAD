# -*- coding: utf-8 -*-
import src.edit_text as edit_text
import wx

def right_mouse_event(par):
    state = wx.GetMouseState()
    if state.ControlDown():
        par.back_collection()
    else:
        for i in par.current_objects:
            if par.ALLOBJECT[i]['class'].text_changeble:
                edit_text.Edit_text(par, i)
                break



        
    par.focus_cmd()
    
    
    
