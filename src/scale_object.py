# -*- coding: utf-8; -*-
import time
import wx
import src.sectors_alg as sectors_alg
from base import Base

class Object(Base):
    def __init__(self, par):
        super(Object, self).__init__(par)
        self.scaleEvent()

    def scaleEvent(self):
        if self.par.collection:
            super(Object, self).func_1(
                Object,
                self.scaleEvent2,
                'Scale - base point:',
                'Selected %s objects. Escape - stop' %(len(self.par.collection))
                )
            self.par.amount_of_select()
            
        else:
            self.par.kill()
            self.par.info2.SetValue('Objects do not selected')


    def scaleEvent2(self, event):
        self.par.ex, self.par.ey = super(Object, self).func_3_r()
        super(Object, self).Y_N(
            self.scaleEvent3,
            'Scale - factor [%s]:' %(self.par.old_scale),
            )

    def scaleEvent3(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_RETURN:
            data = self.par.from_cmd(float)
            if data:
                self.par.old_scale = data
                scale_factor = data
            else:
                scale_factor = self.par.old_scale
            scale(self.par, self.par.ex, self.par.ey, scale_factor, self.par.collection)
            
        elif key == wx.WXK_ESCAPE:
            self.par.kill()
        
        else:
            event.Skip()
            return


def scale(par, x, y, scale_factor, objects):
    del_list = []
    t1 = time.time()
    start = par.total_N
    for content in par.collection:
        if 'scale' in dir(par.ALLOBJECT[content]['class']):
            cNew = par.ALLOBJECT[content]['class'].scale(x, y, scale_factor)
            if cNew:
                del_list.append(content)
            
    end = par.total_N
    if del_list:
        par.ALLOBJECT, par.sectors = sectors_alg.quadric_mass(
            par.ALLOBJECT,
            range(start+1, end+1),
            par.sectors,
            par.q_scale,
            )
    
        par.delete_objects(del_list, False)
        
        par.change_pointdata()
        
        print 'scale ', len(par.collection), ' objects', time.time() - t1, 'sec'
        par.kill()
