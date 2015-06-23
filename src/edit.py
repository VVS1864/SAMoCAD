# -*- coding: utf-8; -*-
from math import sqrt, pi, degrees, radians

import src.sectors_alg as sectors_alg
import src.select_clone as select_clone
from src.calc import calc_angle
from src.base import Base

#ИЗИЕНЕНИЕ УЗЛОВ
class Object(Base):
    def __init__(self, par):
        super(Object, self).__init__(par)
        self.editEvent()
        
    def editEvent(self):
        x = self.par.x_priv
        y = self.par.y_priv
        
        self.par.resFlag = True
        self.par.current_flag = False
        if self.par.collection:
            #Если объекты выбраны, изменять их, если это возможно
            self.par.collection = self.par.edit_collector(self.par.collection, x, y)
            if not self.par.collection:
                a = set(self.par.find_privs)
                self.par.collection = list(a)

        else:
            #Если объекты не выбраны - искать изменяемые в списке привязок
            a = set(self.par.find_privs)
            self.par.collection = list(a)

        self.par.rline = self.par.collection[0]
        self.par.red_line_data, self.par.red_line_color = select_clone.select_clone(
                self.par,
                self.par.collection,
                [255, 0, 0],
                )
        
        self.par.ex, self.par.ey = super(Object, self).func_2(
            self.editEvent2,
            'Etit node - %s objects:' %(len(self.par.collection)),
            True,
            )
        self.par.info2.SetValue('Escape - stop')
        self.par.c.Refresh()
            

    def editEvent2(self, event = None):
        self.par.ex2 = self.par.x_priv
        self.par.ey2 = self.par.y_priv
        if event:
            del_objects = []
            start = self.par.total_N
            for content in self.par.collection:
                cNew = None
                if 'edit' in dir(self.par.ALLOBJECT[content]['class']):
                    cNew = self.par.ALLOBJECT[content]['class'].edit(self.par.ex, self.par.ey, self.par.ex2, self.par.ey2)
                    if cNew:
                        del_objects.append(content)
            end = self.par.total_N
            new_objects = range(start+1, end+1)
            if del_objects:
                self.par.ALLOBJECT, self.par.sectors = sectors_alg.quadric_mass(self.par.ALLOBJECT, new_objects, self.par.sectors, self.par.q_scale)
                super(Object, self).add_history(objects = del_objects, mode = 'replace', objects_2 = new_objects)
                self.par.delete_objects(del_objects, False)
                self.par.change_pointdata()
            
            a = set(self.par.collection)
            b = set(new_objects)
            c = set(del_objects)
            a.difference_update(c)
            a.update(b)
            self.par.kill()
            self.par.collectionBack = list(b)
        else:
            for content in self.par.collection:
                if 'edit_temp' in dir(self.par.ALLOBJECT[content]['class']):
                    self.par.ALLOBJECT[content]['class'].edit_temp(self.par.ex, self.par.ey, self.par.ex2, self.par.ey2)
             
