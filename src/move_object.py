# -*- coding: utf-8; -*-
import time
import wx
import src.sectors_alg as sectors_alg

from base import Base
class Object(Base):
    def __init__(self, par):
        super(Object, self).__init__(par)
        self.moveEvent()
        
    def moveEvent(self):
        if self.par.collection:
            super(Object, self).func_1(
                Object,
                self.moveEvent2,
                'Move - base point:',
                'Enter - stop'
                )
            self.par.amount_of_select()
            
        else:
            self.par.kill()
            
            self.par.info2.SetValue('Objects do not selected')

    def moveEvent2(self, event):
        self.par.ex, self.par.ey = super(Object, self).func_2(
                                self.moveEvent3,
                                'Move - intersect point:',
                                True,
                                )
        

    def moveEvent3(self, event = None):
        
        kwargs = {
            'x1' : self.par.ex,
            'y1' : self.par.ey,
            'x2' : self.par.ex2,
            'y2' : self.par.ey2,
            'objects' : self.par.collection,
            'par' : self.par,
            'temp' : False,
            }
        
        super(Object, self).func_3(event, mover, kwargs)
        
        
    #Копирует объекты
def mover(x1, y1, x2, y2, objects, par, temp):
    d = (x2 - x1, y2 - y1)
    if not temp:
        t1 = time.time()
        start = par.total_N
        for content in objects:
            par.ALLOBJECT[content]['class'].copy(d)
        end = par.total_N
        new_objects = range(start+1, end+1)
        par.ALLOBJECT, par.sectors = sectors_alg.quadric_mass(par.ALLOBJECT, new_objects, par.sectors, par.q_scale)

        par.delete_objects(objects, False)
        par.change_pointdata()
        print 'move ', len(par.collection), ' objects', time.time() - t1, 'sec'
        par.kill()
        par.collectionBack = new_objects
        
    else:
        par.dynamic_matrix = [
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            float(d[0]), float(d[1]), 0.0, 1.0,
            ]
        if par.first:
            '''
            for content in objects:
                par.ALLOBJECT[content]['class'].copy_temp(d)
            '''
            par.dynamic_data = par.collection_data
            par.dynamic_color = []

            par.gl_wrap.dinamic_vbo_on()
            par.first = False
        
