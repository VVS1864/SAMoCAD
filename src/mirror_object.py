# -*- coding: utf-8; -*-
import time
import wx
import src.sectors_alg as sectors_alg

from math import sqrt
from base import Base
class Object(Base):
    def __init__(self, par):
        super(Object, self).__init__(par)
        self.mirrorEvent()
        
    def mirrorEvent(self):
        if self.par.collection:
            super(Object, self).func_1(
                Object,
                self.mirrorEvent2,
                'Mirror - point 1:',
                'Enter - stop'
                )
            self.par.amount_of_select()
            
        else:
            self.par.kill()
            self.par.info2.SetValue('Objects do not selected')

    def mirrorEvent2(self, event):
        self.par.ex, self.par.ey = super(Object, self).func_2(
                        self.mirrorEvent3,
                        'Mirror - point 2:',
                        True,
                        )

    def mirrorEvent3(self, event = None):
        self.par.ex2, self.par.ey2 = super(Object, self).func_3_r()
        
        
        if event:            
            if event.GetEventType() == wx.wxEVT_LEFT_DOWN:
                super(Object, self).Y_N(self.mirrorEvent4, 'Delete objects? (Y / N)[N]:')
            else:
                self.mirrorEvent4(event)
        else:
            self.mirrorEvent4(event)
    

    def mirrorEvent4(self, event = None):
        kwargs = {
            'x1' : self.par.ex,
            'y1' : self.par.ey,
            'x2' : self.par.ex2,
            'y2' : self.par.ey2,
            'del_old' : 'N',
            'objects' : self.par.collection,
            'par' : self.par,
            'temp' : False,
            }
        if event and event.GetEventType() == wx.wxEVT_KEY_DOWN:
            if event.GetKeyCode() == wx.WXK_RETURN:
                kwargs['del_old'] = super(Object, self).input_Y_N(default = 'N')
            elif event.GetKeyCode() == wx.WXK_ESCAPE:
                self.par.kill()
                return
            else:
                event.Skip()
                return
        
        super(Object, self).func_4_r(event, mirror, kwargs)
                
    #Отражаем объекты
def mirror(x1,y1,x2,y2, objects, par, del_old, temp):
    if (x1,y1) != (x2,y2):
        a = x2 - x1
        b = y2 - y1
        if a != 0 or b != 0:
            cos = a / sqrt(a*a + b*b)
            sin = b / sqrt(a*a + b*b)
        else:
            return
        
        if not temp:
            del_list = []
            new_object = []
            t1 = time.time()
            start = par.total_N
            for content in objects:
                cNew = par.ALLOBJECT[content]['class'].mirror(x1, y1, sin, cos)
                if cNew:
                    del_list.append(content)
            end = par.total_N
            new_objects = range(start+1, end+1)
            par.ALLOBJECT, par.sectors = sectors_alg.quadric_mass(par.ALLOBJECT, new_objects, par.sectors, par.q_scale)
            if del_old == 'Y':
                par.delete_objects(del_list, False)
                par.collection = new_objects
                
            par.change_pointdata()
            #par.collection = new_objects
            print 'mirror ', len(par.collection), ' objects', time.time() - t1, 'sec'
            par.kill()
        else:
            for content in objects:
                par.ALLOBJECT[content]['class'].mirror_temp(x1, y1, sin, cos)

    else:
        if not temp:
            print 'Bad mirror coords!'
            par.kill()
