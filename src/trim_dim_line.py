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
        self.el = self.par.current#self.par.get_obj(event.x, event.y, 'all')
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
        #self.par.ex2 = self.par.priv_coord[0]
        #self.par.ey2 = self.par.priv_coord[1]
        self.par.ex2 = self.par.x_priv
        self.par.ey2 = self.par.y_priv
        cd = self.par.ALLOBJECT[self.el].copy()
       # self.par.ex3,self.par.ey3 = self.par.coordinator(self.par.ex3,self.par.ey3)
        #x1, y1, x2, y2, x3, y3, ort, size, fill, text, sloy, text_change, text_place, s, vr_s, vv_s, arrow_s, type_arrow, s_s, w_text, font = self.par.get_dim_conf(self.par.col)
        '''
        if cd['ort'] == 'horizontal':
            md1 = abs(cd['y1']-self.par.ey3)
            md2 = abs(cd['y2']-self.par.ey3)
        else:
            md1 = abs(cd['x1']-self.par.ex3)
            md2 = abs(cd['x2']-self.par.ex3)

        if md1<md2:
            self.par.ex = cd['x1']
            self.par.ey = cd['y1']
        else:
            self.par.ex = cd['x2']
            self.par.ey = cd['y2']
        
        x1 = cd['x1']
        x2 = cd['x2']
        y1 = cd['y1']
        y2 = cd['y2']
        x3 = cd['x3']
        y3 = cd['y3']
        '''
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
            
        '''
        if cd['ort'] == 'horizontal':
            #print 111
            x12 = x3
            y12 = y1
            x22 = x3
            y22 = y2
        else:
            #print 222
            x12 = x1
            y12 = y3
            x22 = x2
            y22 = y3
        mdx1,mdy1 = calc.min_distanse(x1, y1, x12, y12,self.par.ex3,self.par.ey3)
        mdx2,mdy2 = calc.min_distanse(x2, y2, x22, y22,self.par.ex3,self.par.ey3)
        try:
            md1 = sqrt((self.par.ex3-mdx1)**2 + (self.par.ey3-mdy1)**2)
        except:
            md1 = 0
        try:
            md2 = sqrt((self.par.ex3-mdx2)**2 + (self.par.ey3-mdy2)**2)
        except:
            md2 = 0
            
        if md1<md2:
            #print 333
            self.par.ex = x12
            self.par.ey = y12
        else:
            #print 444
            self.par.ex = x22
            self.par.ey = y22
        '''
            
        cd['in_mass'] = False
        cd['x1'] = self.par.ex
        cd['y1'] = self.par.ey
        cd['x2'] = self.par.ex2
        cd['y2'] = self.par.ey2
        cd['text_change'] = 1
        cd['text_place'] = None
        #self.par.set_coord()
        if event:
            cd['temp'] = False
            cNew = self.par.ALLOBJECT[self.el]['class'].create_object(cd)
            if cNew:
                self.par.ex = self.par.ex2
                self.par.ey = self.par.ey2
                self.el = self.par.total_N
                
            '''
            dimension.c_dim(self.par, self.par.ex, self.par.ey, self.par.ex2, self.par.ey2, x3, y3,
                        #text = text,
                        sloy = sloy,
                        fill = fill,
                        size = size,
                        ort = ort,
                        #text_change = text_change,
                        #text_place = text_place,
                        s = s,
                        vr_s = vr_s,
                        vv_s = vv_s,
                        arrow_s = arrow_s,
                        type_arrow = type_arrow,
                        s_s = s_s,
                        w_text = w_text,
                        font = font)
            self.par.ex3 = self.par.priv_coord[0]
            self.par.ey3 = self.par.priv_coord[1]
            self.par.col = self.par.Ndim
            self.par.history_undo.append(('c_', self.par.Ndim))
            self.par.changeFlag = True
            self.par.enumerator_p()
            '''
            
        else:
            cd['temp'] = True
            self.par.ALLOBJECT[self.el]['class'].create_object(cd)

            '''
            dimension.c_dim(self.par, self.par.ex, self.par.ey, self.par.ex2, self.par.ey2, x3, y3,
                        #text = text,
                        sloy = sloy,
                        fill = fill,
                        size = size,
                        ort = ort,
                        #text_change = text_change,
                        #text_place = text_place,
                        s = s,
                        vr_s = vr_s,
                        vv_s = vv_s,
                        arrow_s = arrow_s,
                        type_arrow = type_arrow,
                        s_s = s_s,
                        w_text = w_text,
                        font = font,
                        temp = 'Yes')
            '''
        
        
