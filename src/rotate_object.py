# -*- coding: utf-8; -*-
import time
import wx
import src.sectors_alg as sectors_alg
from src.calc import calc_angle
import numpy

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
            elif event.GetKeyCode() == wx.WXK_ESCAPE:
                self.par.kill()
                return
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
        if angle != None:
            msin = sin(angle)
            mcos = cos(angle)
                
            if not temp:
                new_object = []
                del_list = []
                t1 = time.time()
                start = par.total_N
                for content in objects:
                    cNew = par.ALLOBJECT[content]['class'].rotate(x0, y0, msin, mcos, angle)
                    if cNew:
                        del_list.append(content)
                end = par.total_N
                new_objects = range(start+1, end+1)
                par.ALLOBJECT, par.sectors = sectors_alg.quadric_mass(par.ALLOBJECT, new_objects, par.sectors, par.q_scale)
                if del_old == 'Y':
                    print 'Y'
                    par.delete_objects(del_list, False)
                    
                par.change_pointdata()
                par.collection = new_objects    
                print 'rotate ', len(par.collection), ' objects', time.time() - t1, 'sec'
                par.kill()
            else:
                c = mcos
                s = -msin
                x = 0
                y = 0
                z = 1
                translate1Matrix = numpy.matrix(
                   [[1.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 0.0],
                    [-x0, -y0, 0.0, 1.0]], numpy.float32)
                
                rotateMatrix = numpy.matrix(
                   [[x*x*(1-c)+c,     y*x*(1-c)+z*s,  z*x*(1-c)+y*s, 0.0],
                    [y*x*(1-c)-z*s,   y*y*(1-c)+c,    y*z*(1-c)+x*s, 0.0],
                    [x*z*(1-c)+y*s,   y*z*(1-c)-x*s,  z*z*(1-c)+c,   0.0],
                    [0.0,             0.0,            0.0,           1.0]], numpy.float32)

                translate2Matrix = numpy.matrix(
                   [[1.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 0.0],
                    [x0, y0, 0.0, 1.0]], numpy.float32)
                   
                par.dynamic_matrix = translate1Matrix.dot(rotateMatrix)
                par.dynamic_matrix = par.dynamic_matrix.dot(translate2Matrix).flatten().tolist()
                #par.dynamic_matrix = rotateMatrix.dot(translateMatrix).flatten().tolist()
                '''
                par.dynamic_matrix = [
                    x*x*(1-c)+c,     y*x*(1-c)+z*s,  z*x*(1-c)+y*s, 0.0,
                    y*x*(1-c)-z*s,   y*y*(1-c)+c,    y*z*(1-c)+x*s, 0.0,
                    x*z*(1-c)+y*s,   y*z*(1-c)-x*s,  z*z*(1-c)+c,   0.0,
                    0.0,             0.0,            0.0,           1.0,
                    ]
                '''
                if par.first:
                    '''
                    for content in objects:
                        par.ALLOBJECT[content]['class'].rotate_temp(x0, y0, msin, mcos, angle)
                    '''
                    par.dynamic_data = par.collection_data
                    par.dynamic_color = []
                    par.gl_wrap.dinamic_vbo_on()
                    par.first = False

    else:
        if not temp:
            print 'Bad rotate coords!'
            par.kill()
