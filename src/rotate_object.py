# -*- coding: utf-8; -*-
import time
import wx
import src.sectors_alg as sectors_alg
from src.calc import calc_angle

from math import sqrt, sin, cos
from base import Base
class Object(Base):
    def __init__(self, par):
        super(Object, self).__init__(par)
        self.rotateEvent()
        
    def rotateEvent(self):
        if self.par.collection:
            super(Object, self).func_1(
                Object,
                self.rotateEvent2,
                'Rotate - base point:',
                'Enter - stop'
                )
            self.par.amount_of_select()
            
        else:
            self.par.kill()
            self.par.info2.SetValue('Objects do not selected')

    def rotateEvent2(self, event):
        self.par.ex, self.par.ey = super(Object, self).func_2(
                        self.rotateEvent3,
                        'Rotate - point 2:',
                        False,
                        )

    def rotateEvent3(self, event):
        self.par.ex2, self.par.ey2 = super(Object, self).func_2(
                        self.rotateEvent4,
                        'Rotate - point 2:',
                        True,
                        )
    
    def rotateEvent4(self, event = None):
        self.par.ex3, self.par.ey3 = super(Object, self).func_3_r()
        
        if event:            
            if event.GetEventType() == wx.wxEVT_LEFT_DOWN:
                super(Object, self).Y_N(self.rotateEvent5, 'Delete objects? (Y / N)[Y]:')
            else:
                self.rotateEvent5(event)
        else:
            self.rotateEvent5(event)
            
    def rotateEvent5(self, event = None):
        kwargs = {
            'x0' : self.par.ex,
            'y0' : self.par.ey,
            'x1' : self.par.ex2,
            'y1' : self.par.ey2,
            'x2' : self.par.ex3,
            'y2' : self.par.ey3,
            'angle' : None,
            'del_old' : 'Y',
            'objects' : self.par.collection,
            'par' : self.par,
            'temp' : False,
            }
        if event and event.GetEventType() == wx.wxEVT_KEY_DOWN:
            if event.GetKeyCode() == wx.WXK_RETURN:
                kwargs['del_old'] = super(Object, self).input_Y_N(default = 'Y')
            else:
                event.Skip()
                return
        
        super(Object, self).func_4_r(event, rotate, kwargs)
                
    #Отражаем объекты
def rotate(x0, y0, x1, y1, x2, y2, angle, objects, par, del_old, temp):
    if (x0, y0) != (x1, y1) != (x2, y2):
        #Если угол поворота не указан - считать по координатам
        if angle == None:
            #Если угол указан - считать сразу
            angle = calc_angle(x0, y0, x1, y1, x2, y2)
        if angle:
            msin = sin(angle)
            mcos = cos(angle)
                
            if not temp:
                del_list = []
                t1 = time.time()
                start = par.total_N
                for content in objects:
                    cNew = par.ALLOBJECT[content]['class'].rotate(x0, y0, msin, mcos, angle)
                    if cNew:
                        del_list.append(content)
                end = par.total_N
                par.ALLOBJECT, par.sectors = sectors_alg.quadric_mass(par.ALLOBJECT, range(start+1, end+1), par.sectors, par.q_scale)
                if del_old == 'Y':
                    print 'Y'
                    par.delete_objects(del_list, False)
                    
                par.change_pointdata()
                    
                print 'rotate ', len(par.collection), ' objects', time.time() - t1, 'sec'
                par.kill()
            else:
                for content in objects:
                    par.ALLOBJECT[content]['class'].rotate_temp(x0, y0, msin, mcos, angle)

    else:
        if not temp:
            print 'Bad rotate coords!'
            par.kill()
