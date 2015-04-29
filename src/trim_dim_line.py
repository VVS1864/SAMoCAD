# -*- coding: utf-8; -*-
import dimension
import select_clone
from src.base import Base
from math import sqrt
import calc


#ПРОДЛЕНИЕ РАЗМЕРНОЙ ЛИНИИ
class Object(Base):
    def __init__(self, par):
        super(Object, self).__init__(par)
        self.trim_dimEvent()

    def trim_dimEvent(self):
        
        super(Object, self).func_1(
                Object,
                self.trim_dimEvent2,
                'Chain dim - dimension:',
                'Escape - stop'
                )
        #self.par.resFlag = True
        self.par.snap_flag = False
        self.par.current_flag = True


    def trim_dimEvent2(self, event):
        self.el = self.par.current
        if self.el and self.par.ALLOBJECT[self.el]['object'] == 'dim':
            self.par.ex, self.par.ey = super(Object, self).func_2(
                self.trim_dimEvent3,
                'Chain dim - next point:',
                True,
                )

            self.par.red_line_data, self.par.red_line_color = select_clone.select_clone(
                self.par,
                [self.el,],
                color = [255, 0, 0],
                )
            self.par.snap_flag = True
            self.par.current_flag = False

    def trim_dimEvent3(self, event = None):
        self.par.ex2 = self.par.x_priv
        self.par.ey2 = self.par.y_priv
        cd = self.par.ALLOBJECT[self.el].copy()
       
        if cd['ort'] == 'horizontal':
            md1 = abs(cd['y1'] - self.par.ey2)
            md2 = abs(cd['y2'] - self.par.ey2)
        else:
            md1 = abs(cd['x1'] - self.par.ex2)
            md2 = abs(cd['x2'] - self.par.ex2)
            
        if md1<md2:
            self.par.ex = cd['x1']
            self.par.ey = cd['y1']
        else:
            self.par.ex = cd['x2']
            self.par.ey = cd['y2']
            
        cd['in_mass'] = False
        cd['x1'] = self.par.ex
        cd['y1'] = self.par.ey
        cd['x2'] = self.par.ex2
        cd['y2'] = self.par.ey2
        cd['text_change'] = 1
        cd['text_place'] = None
        if event:
            cd['temp'] = False
            cNew = self.par.ALLOBJECT[self.el]['class'].create_object(cd)
            if cNew:
                self.par.ex = self.par.ex2
                self.par.ey = self.par.ey2
                self.el = self.par.total_N
            
        else:
            cd['temp'] = True
            self.par.ALLOBJECT[self.el]['class'].create_object(cd)
        
        
