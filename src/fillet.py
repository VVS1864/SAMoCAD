# -*- coding: utf-8; -*-
import src.calc as calc

from src.line import c_line
from src.arc import c_arc

from src.base import Base

import src.select_clone as select_clone
import src.grab_object as grab_object
import src.sectors_alg as sectors_alg
import wx

import math

#СОПРЯЖЕНИЕ
class Fillet(Base):
    def __init__(self, par):
        super(Fillet, self).__init__(par)
        self.filletEvent()
    def filletEvent(self, event=None):
        self.par.kill()
        super(Fillet, self).func_1(
            Fillet,
            self.filletEvent2,
            'Fillet - line 1:',
            'Escape - stop',
            )
        self.par.resFlag = True
        self.par.snap_flag = False
        self.par.current_flag = True

    def filletEvent2(self, event):
        self.par.focus_cmd()
        if self.par.current and self.par.ALLOBJECT[self.par.current]['object'] == 'line':
            self.par.collection.append(self.par.current)
            self.par.rline = self.par.current
            self.par.red_line_data, self.par.red_line_color = select_clone.select_clone(
                self.par,
                [self.par.rline,],
                [255, 0, 0],
                )
            self.par.info.SetValue('Fillet - line 2:')
            
            self.par.c.Unbind(wx.EVT_LEFT_DOWN)
            self.par.c.Bind(wx.EVT_LEFT_DOWN, self.filletEvent3)

    def filletEvent3(self, event):
        self.par.focus_cmd()
        if (self.par.current
            and self.par.current not in self.par.collection
            and self.par.ALLOBJECT[self.par.current]['object'] == 'line'):
            
            self.par.collection.append(self.par.current)
            self.par.rline = self.par.current
            red_line_data, red_line_color = select_clone.select_clone(
                self.par,
                [self.par.rline,],
                [255, 0, 0],
                )
            self.par.red_line_data.extend(red_line_data)
            self.par.red_line_color.extend(red_line_color)
            self.par.info.SetValue('Fillet - radius: [%s]:'%(str(self.par.old_fillet_R)))
            self.par.info2.SetValue('Escape - stop. Ponit 1')
            
            self.par.cmd.Unbind(wx.EVT_KEY_DOWN)
            self.par.cmd.Bind(wx.EVT_KEY_DOWN, self.filletEvent4)
            self.par.c.Unbind(wx.EVT_LEFT_DOWN)
            self.par.c.Bind(wx.EVT_LEFT_DOWN, self.filletDistanse1)

    def filletDistanse1(self, event):
        self.par.info2.SetValue('Escape - stop. Ponit 2')
        self.par.ex = self.par.x_priv
        self.par.ey = self.par.y_priv
        self.par.c.Unbind(wx.EVT_LEFT_DOWN)
        self.par.c.Bind(wx.EVT_LEFT_DOWN, self.filletDistanse2)

    def filletDistanse2(self, event):
        self.par.ex2 = self.par.x_priv
        self.par.ey2 = self.par.y_priv
        pd = math.sqrt((-self.par.ex + self.par.ex2)**2 + (-self.par.ey + self.par.ey2)**2)

        #?self.par.c.unbind_class(self.par.c,"<1>")
        self.filletEvent4(pd = pd)

    def filletEvent4(self, event = None, pd = None):
        if event:
            key = event.GetKeyCode()
            if key == wx.WXK_RETURN:
                pass
                
            elif key == wx.WXK_ESCAPE:
                self.par.kill()
                return
            else:
                event.Skip()
                return
        
        if pd:
            R = pd
            self.par.old_fillet_R = R
        else:
            data = self.par.from_cmd(float)
            if data != None:
                R = data
                self.par.old_fillet_R = R
            else:
                R = self.par.old_fillet_R
        #fill1, width1, sloy1, stipple1, c1, factor_stip1 = get_line_conf(self.par.collection[0], self.par)
        #fill2, width2, sloy2, stipple2, c2, factor_stip2 = get_line_conf(self.par.collection[1], self.par)
        c1 = self.par.ALLOBJECT[self.par.collection[0]]['coords'][0]
        c2 = self.par.ALLOBJECT[self.par.collection[1]]['coords'][0]
        cd1 = self.par.ALLOBJECT[self.par.collection[0]].copy()
        cd2 = self.par.ALLOBJECT[self.par.collection[1]].copy()
        xc, yc, xe1, ye1, xe2, ye2, cord = calc.filet_point(c1[0], c1[1], c1[2], c1[3], c2[0], c2[1], c2[2], c2[3], R)
        cd1['x1'], cd1['y1'], cd1['x2'], cd1['y2'] = cord[0], cord[1], cord[2], cord[3]
        cd2['x1'], cd2['y1'], cd2['x2'], cd2['y2'] = cord[4], cord[5], cord[6], cord[7]
        cd1['in_mass'] = False
        cd2['in_mass'] = False
        cd1['temp'] = False
        cd2['temp'] = False
        if xc:
            #Если радиус != 0
            start, extent = calc.calc_angles_360(xc, yc, xe1, ye1, xe2, ye2)
            
            
            if abs(extent)>180:
                xa1 = xe2
                ya1 = ye2
                xa2 = xe1
                ya2 = ye1
            else:
                xa1 = xe1
                ya1 = ye1
                xa2 = xe2
                ya2 = ye2
            c_arc(
                self.par,
                xc,
                yc,
                xa1,
                ya1,
                xa2,
                ya2,
                width = self.par.width,
                layer = self.par.layer,
                color = self.par.color,
                R = None,
                start = None,
                extent = None,
                in_mass = False,
                temp = False,
                )
                
        self.par.ALLOBJECT[self.par.collection[0]]['class'].create_object(cd1)
        self.par.ALLOBJECT[self.par.collection[1]]['class'].create_object(cd2)
        self.par.delete_objects(self.par.collection, False)   
        self.par.change_pointdata()
        
        self.par.collection = []
        self.filletEvent()
