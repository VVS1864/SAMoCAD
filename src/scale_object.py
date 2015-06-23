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
            t1 = time.time()
            new_objects = scale(self.par, self.par.ex, self.par.ey, scale_factor, self.par.collection)
            super(Object, self).add_history(objects = new_objects[0], mode = 'replace', objects_2 = new_objects[1])
            self.par.delete_objects(new_objects[0], False)
        
            self.par.change_pointdata()
            
            print 'scale ', len(new_objects[1]), ' objects', time.time() - t1, 'sec'
            self.par.kill()
            
        elif key == wx.WXK_ESCAPE:
            self.par.kill()
        
        else:
            event.Skip()
            return


def scale(par, x, y, scale_factor, objects):
    del_list = []
    
    start = par.total_N
    for content in par.collection:
        cNew = par.ALLOBJECT[content]['class'].scale(x, y, scale_factor)
        if cNew:
            del_list.append(content)
            
    end = par.total_N
    new_objects = range(start+1, end+1)
    if del_list:
        par.ALLOBJECT, par.sectors = sectors_alg.quadric_mass(
            par.ALLOBJECT,
            new_objects,
            par.sectors,
            par.q_scale,
            )
        replace_objects = [del_list, new_objects]
        return replace_objects
        
        
