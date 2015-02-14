# -*- coding: utf-8; -*-
import wx
import calc
class Base(object):
    def __init__(self, par):
        self.par = par
        
    def func_1(self, target_class, target_func_2, info, info2):
        self.par.resFlag = True
        self.par.old_func = (self.par.action, target_class)
        self.par.c.Unbind(wx.EVT_LEFT_DOWN)
        self.par.c.Bind(wx.EVT_LEFT_DOWN, target_func_2)

        self.par.info.SetValue(info)
        self.par.info2.SetValue(info2)

    def func_2(self, target_func_2):
        self.par.c.Unbind(wx.EVT_LEFT_DOWN)
        self.par.c.Unbind(wx.EVT_MOTION)
        self.par.c.Bind(wx.EVT_LEFT_DOWN, target_func_2)
        self.par.c.Bind(wx.EVT_MOTION, self.dynamic)

        self.par.ex = self.par.x_priv
        self.par.ey = self.par.y_priv

        self.par.info.SetValue('Line - next point:')
        self.target_func_2 = target_func_2

    def dynamic(self, e):
        if not self.par.motion_flag:
            self.par.dynamic_data = []
            self.par.dynamic_color = []
            self.target_func_2()
        self.par.motion(e)
        e.Skip()

    def func_3(self, event, target_c_func, target_kwargs):
        self.par.ex2 = self.par.x_priv
        self.par.ey2 = self.par.y_priv
        data = self.par.from_cmd(float)
        if data:
            self.par.ex2, self.par.ey2 = calc.cmd_coorder(
                self.par.ex,
                self.par.ey,
                self.par.ex2,
                self.par.ey2,
                data,
                self.par.ortoFlag,
                )        
        if self.par.trace_flag or self.par.trace_obj_flag:
            if self.par.trace_flag:
                self.par.trace_on = True
            #if self.par.tracing_obj_Flag:
                #self.par.trace_obj_on = True
            self.par.trace_x1, self.par.trace_y1 = self.par.ex, self.par.ey
            self.par.trace_x2, self.par.trace_y2 = self.par.ex2, self.par.ey2
        if event:
            target_kwargs['temp'] = False
            self.par.dynamic_data = []
            self.par.dynamic_color = []
            #self.par.history_undo.append(('c_', self.par.Nline))
            #ex = self.par.ex2
            #ey = self.par.ey2
            event.Skip()
            #self.par.set_coord()
            #self.par.changeFlag = True
            #self.par.enumerator_p()
            #self.par.com = None
            #self.par.command.delete(0, 'end')
        else:
            target_kwargs['temp'] = True
        target_kwargs['x2'] = self.par.ex2
        target_kwargs['y2'] = self.par.ey2
        target_c_func(**target_kwargs)
