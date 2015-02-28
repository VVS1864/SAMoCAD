# -*- coding: utf-8; -*-
import time
import wx
import src.sectors_alg as sectors_alg

from base import Base
class Object(Base):
    def __init__(self, par):
        super(Object, self).__init__(par)
        self.copyEvent()
        
    def copyEvent(self):
        if self.par.collection:
            super(Object, self).func_1(
                Object,
                self.copyEvent2,
                'Copy - base point:',
                'Enter - stop'
                )
            self.par.amount_of_select()
            
        else:
            self.par.kill()
            
            self.par.info2.SetValue('Objects do not selected')

    def copyEvent2(self, event):
        self.par.ex, self.par.ey = super(Object, self).func_2(
                                self.copyEvent3,
                                'Copy - intersect point:',
                                True,
                                )
        

    def copyEvent3(self, event = None):
        
        kwargs = {
            'x1' : self.par.ex,
            'y1' : self.par.ey,
            'x2' : self.par.ex2,
            'y2' : self.par.ey2,
            'objects' : self.par.collection,
            'par' : self.par,
            'temp' : False,
            }
        
        super(Object, self).func_3(event, copyer, kwargs)
        
        
    #Копирует объекты
def copyer(x1, y1, x2, y2, objects, par, temp):
    d = (x2 - x1, y2 - y1)
    if not temp:
        t1 = time.time()
        start = par.total_N
        for content in objects:
            par.ALLOBJECT[content]['class'].copy(d)
        end = par.total_N
        par.ALLOBJECT, par.sectors = sectors_alg.quadric_mass(par.ALLOBJECT, range(start+1, end+1), par.sectors, par.q_scale)
        
        par.change_pointdata()
        par.c.Refresh()
        print 'copy ', len(par.collection), ' objects', time.time() - t1, 'sec'
    else:
        for content in objects:
            par.ALLOBJECT[content]['class'].copy_temp(d)
        
