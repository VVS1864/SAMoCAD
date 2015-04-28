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
class Offset(Base):
    def __init__(self, par):
        super(Offset, self).__init__(par)
        self.offsetEvent()
        
    def offsetEvent(self, event=None):
        self.par.old_func = (self.par.action, Offset)
        if self.par.collection and len(self.par.collection)==1:
            self.par.rline = self.par.collection[0]
            
            self.par.kill()

            self.par.red_line_data, self.par.red_line_color = select_clone.select_clone(
                self.par,
                [self.par.rline,],
                [255, 0, 0],
                )
            
            self.par.snap_flag = True
            self.par.current_flag = False
            self.par.resFlag = True

            self.par.info.SetValue('Offset distanse:[%s]'%(str(self.par.old_offset)))
            self.par.info2.SetValue('Escape - stop. Enter - apply. Point 1')

            self.par.cmd.Unbind(wx.EVT_KEY_DOWN)
            self.par.cmd.Bind(wx.EVT_KEY_DOWN, self.offsetEvent3)
            self.par.c.Unbind(wx.EVT_LEFT_DOWN)
            self.par.c.Bind(wx.EVT_LEFT_DOWN, self.offsetDistanse1)
        else:
            self.par.kill()
            
            self.par.resFlag = True
            self.par.snap_flag = False
            self.par.current_flag = True
            self.par.info.SetValue('Offset - object:')
            self.par.info2.SetValue('Escape - stop')
            
            self.par.c.Unbind(wx.EVT_LEFT_DOWN)
            self.par.c.Bind(wx.EVT_LEFT_DOWN, self.offsetEvent2)

    def offsetEvent2(self, event):
        self.par.focus_cmd()
        if self.par.current and self.par.ALLOBJECT[self.par.current]['object'] in ('line', 'circle', 'arc'):
            self.par.collection.append(self.par.current)
            self.par.rline = self.par.current
            self.par.red_line_data, self.par.red_line_color = select_clone.select_clone(
                self.par,
                [self.par.rline,],
                [255, 0, 0],
                )
            self.par.info.SetValue('Offset distanse:[%s]'%(str(self.par.old_offset)))
            self.par.info2.SetValue('Escape - stop. Enter - apply. Point 1')
            
            self.par.cmd.Unbind(wx.EVT_KEY_DOWN)
            self.par.cmd.Bind(wx.EVT_KEY_DOWN, self.offsetEvent3)
            self.par.c.Unbind(wx.EVT_LEFT_DOWN)
            self.par.c.Bind(wx.EVT_LEFT_DOWN, self.offsetDistanse1)
            
            self.par.snap_flag = True
            self.par.current_flag = False
            
    '''
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
    '''

    def offsetDistanse1(self, event):
        self.par.info2.SetValue('Escape - stop. Ponit 2')
        self.par.ex = self.par.x_priv
        self.par.ey = self.par.y_priv
        self.par.c.Unbind(wx.EVT_LEFT_DOWN)
        self.par.c.Bind(wx.EVT_LEFT_DOWN, self.offsetDistanse2)

    def offsetDistanse2(self, event):
        self.par.ex2 = self.par.x_priv
        self.par.ey2 = self.par.y_priv
        pd = math.sqrt((-self.par.ex + self.par.ex2)**2 + (-self.par.ey + self.par.ey2)**2)

        #?self.par.c.unbind_class(self.par.c,"<1>")
        self.offsetEvent3(pd = pd)

    def offsetEvent3(self, event = None, pd = None):
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
            self.par.old_offset = R
        else:
            data = self.par.from_cmd(float)
            if data != None:
                R = data
                self.par.old_offset = R
            else:
                R = self.par.old_offset
        self.par.pd = R

        self.par.c.Unbind(wx.EVT_LEFT_DOWN)
        self.par.c.Bind(wx.EVT_LEFT_DOWN, self.offsetEvent4)
        self.par.info.SetValue('Offset - direction:')
        self.par.info2.SetValue('Escape - stop')
        self.par.snap_flag = False
        self.par.current_flag = False
        
        
    def offsetEvent4(self, event):
        x3 = self.par.x_priv
        y3 = self.par.y_priv
        
        e = self.par.ALLOBJECT[self.par.rline]['class'].offset(self.par.pd, x3, y3)
        self.par.kill()
        self.offsetEvent()

        '''
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
        '''
