# -*- coding: utf-8; -*-
from math import sqrt, pi, degrees, radians

import src.sectors_alg as sectors_alg
from src.calc import calc_angle
from src.base import Base
#import line, dimension, text_line, circle, arc
#import get_conf
#from get_conf import get_arc_conf

#ИЗИЕНЕНИЕ УЗЛОВ
class Object(Base):
    def __init__(self, par):
        #self.par = par
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

        

        
        self.par.ex, self.par.ey = super(Object, self).func_2(
            self.editEvent2,
            'Etit node - %s objects:' %(len(self.par.collection)),
            True,
            )
        self.par.info2.SetValue('Escape - stop')                       
           
        '''
        if self.par.tip_p not in ('X', 'c'):
            self.par.standart_unbind()
            self.par.resFlag = True
            self.par.c.bind('<Button-1>', self.editEvent2)#Включить следующее действие
            self.par.edit_clone = True
            e = None#Пустая переменная
            self.par.find_privs2 = self.par.find_privs#Список приметивов, к которым в данный момент можно привязаться
            self.par.find_privs2.remove('t')#Убрать из списка разделитель
            self.par.ex = self.par.priv_coord[0]#Получить координаты из списка координат привязок (их рассчитывает gpriv)
            self.par.ey = self.par.priv_coord[1]
            if self.par.collection:#Если объекты выбраны, изменять их, если это возможно
                r = self.par.collection
                self.par.edit_c(r)
            if not self.par.collection:
                #Если объекты не выбраны - искать изменяемые в списке привязок
                e = self.par.edit_collektor(self.par.find_privs2)
            self.par.dialog.config(text = (u'Etit node - %s objects:') %(len(self.par.collection)))
            self.par.info.config(text = u'Escape - stop')
            self.par.set_coord()
            self.par.edit_clone = True
        '''
            

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
                self.par.delete_objects(del_objects, False)
                self.par.change_pointdata()
            #self.par.kill()
            
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
             


        """
        delete_list = []
        self.par.ex2=self.par.priv_coord[0]
        self.par.ey2=self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        self.par.set_coord()
        self.par.ex3 = None
        self.par.ey3 = None
        if self.par.ortoFlag == True and self.par.com == None:
            self.par.ex2,self.par.ey2 = self.par.orto(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
        for content in self.par.collection:
            if content[0] == 'L':
                delete_list.append(content)
                self.par.ALLOBJECT[content]['class'].edit(event)
            if content[0] == 'd':
                delete_list.append(content)
                self.par.ALLOBJECT[content]['class'].edit(event)
                '''
                text_prov = False
                fill = self.par.ALLOBJECT[content]['fill']
                sloy = self.par.ALLOBJECT[content]['sloy']
                text = self.par.ALLOBJECT[content]['text']
                line1 = self.par.get_snap_line(content)[0]
                line2 = self.par.get_snap_line(content)[1]
                line3 = self.par.get_snap_line(content)[2]
                ort = self.par.ALLOBJECT[content]['ort']
                size = self.par.ALLOBJECT[content]['size']
                s = self.par.ALLOBJECT[content]['s']
                vr_s = self.par.ALLOBJECT[content]['vr_s']
                vv_s = self.par.ALLOBJECT[content]['vv_s']
                arrow_s = self.par.ALLOBJECT[content]['arrow_s']
                type_arrow = self.par.ALLOBJECT[content]['type_arrow']
                s_s = self.par.ALLOBJECT[content]['s_s_dim']
                w_text = self.par.ALLOBJECT[content]['w_text_dim']
                font = self.par.ALLOBJECT[content]['font_dim']

                coord_list = map(lambda i: self.par.c.coords(i), [line1, line2, line3])

                if abs(coord_list[0][0] - self.par.ex) < self.par.min_e:
                    if abs(coord_list[0][1] - self.par.ey) < self.par.min_e:
                        coord_list[0] = [self.par.ex2, self.par.ey2]
                elif abs(coord_list[1][0] - self.par.ex) < self.par.min_e:
                    if abs(coord_list[1][1] - self.par.ey) < self.par.min_e:
                        coord_list[1] = [self.par.ex2, self.par.ey2]
                elif abs(coord_list[2][0] - self.par.ex) < self.par.min_e:
                    coord_list[2] = [self.par.ex2, self.par.ey2]
                    text_prov = True
                elif abs(coord_list[2][1] - self.par.ey) < self.par.min_e:
                    coord_list[2] = [self.par.ex2, self.par.ey2]
                    text_prov = True

                delete_list.append(content)
                if text_prov == True:
                    text_change = self.par.ALLOBJECT[content]['text_change']
                    text_lines, priv_line, text_place = self.par.dim_text_place(content)
                    if text_place[2] == 'hor':
                        text_place[1] = self.par.ey + (self.par.ey2-self.par.ey)

                    else:
                        text_place[0] = self.par.ex + (self.par.ex2-self.par.ex)

                else:
                    text_change = 'unchange'
                    text_place = None
                if event:
                    dimension.c_dim(self.par, coord_list[0][0], coord_list[0][1], coord_list[1][0], coord_list[1][1], coord_list[2][0], coord_list[2][1],
                                text = text,
                                sloy = sloy,
                                fill = fill,
                                size = size,
                                ort = ort,
                                text_change = text_change,
                                text_place = text_place,
                                s = s,
                                vr_s = vr_s,
                                vv_s = vv_s,
                                arrow_s = arrow_s,
                                type_arrow = type_arrow,
                                s_s = s_s,
                                w_text = w_text,
                                font = font)
                else:
                    dimension.c_dim(self.par, coord_list[0][0], coord_list[0][1], coord_list[1][0], coord_list[1][1], coord_list[2][0], coord_list[2][1],
                                text = text,
                                sloy = sloy,
                                fill = fill,
                                size = size,
                                ort = ort,
                                text_change = text_change,
                                text_place = text_place,
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
            if content[0] == 'r':
                xc, yc, x1, y1, size, fill, text, sloy, s, vr_s, arrow_s, type_arrow, s_s_dim, w_text_dim, font_dim, R = self.par.get_dimR_conf(content)
                x1 = self.par.ex2
                y1 = self.par.ey2
                delete_list.append(content)
                if event:
                    dimension.c_dimR(self.par, xc,yc,x1,y1,
                                Rn = R,
                                text = text,
                                sloy = sloy,
                                fill = fill,
                                size = size,
                                s = s,
                                vr_s = vr_s,
                                arrow_s = arrow_s,
                                type_arrow = type_arrow,
                                s_s = s_s_dim,
                                w_text = w_text_dim,
                                font = font_dim)

                else:
                    dimension.c_dimR(self.par, xc,yc,x1,y1,
                                Rn = R,
                                text = text,
                                sloy = sloy,
                                fill = fill,
                                size = size,
                                s = s,
                                vr_s = vr_s,
                                arrow_s = arrow_s,
                                type_arrow = type_arrow,
                                s_s = s_s_dim,
                                w_text = w_text_dim,
                                font = font_dim,
                                temp = 'Yes')

            if content[0] == 'c':
                delete_list.append(content)
                self.par.ALLOBJECT[content]['class'].edit(event)
                '''
                e = self.par.get_conf(content)
                x0 = e[1]
                y0 = e[2]
                R = sqrt((self.par.ex2-x0)**2 + (self.par.ey2-y0)**2)

                fill = e[4]
                width = e[5]
                sloy = e[6]
                delete_list.append(content)
                if event:
                    circle.c_circle(self.par, x0,y0,fill = fill, width = width, sloy = sloy, R = R)
                else:
                    circle.c_circle(self.par, x0,y0,fill = fill, width = width, sloy = sloy, R = R, temp = 'Yes')
                '''
            elif content[0] == 'a':
                delete_list.append(content)
                self.par.ALLOBJECT[content]['class'].edit(event)
                '''
                find = self.par.ALLOBJECT[content]['id']
                #for i in find:
                   # tag = self.par.ALLOBJECT[content]['id'][i]
                    #if 'a' in tag:
                     #   coord = self.par.c.coords(i)
                xc, yc, dx1, dy1, dx2, dy2, fill, width, sloy = get_arc_conf(content, self.par)
                
                e = self.par.get_arc_conf(content)
                xc = e[1]
                yc = e[2]
                dx1 = e[3]
                dy1 = e[4]
                dx2 = e[5]
                dy2 = e[6]
                fill = e[7]
                width = e[8]
                sloy = e[9]
                
                R = sqrt((dx1-xc)**2 + (dy1-yc)**2)
    
                if abs(self.par.ex-dx1)<self.par.min_e:
                    if abs(self.par.ey-dy1)<self.par.min_e:
                        dx1 = self.par.ex2
                        dy1 = self.par.ey2
                elif abs(self.par.ex-dx2)<self.par.min_e:
                    if abs(self.par.ey-dy2)<self.par.min_e:
                        dx2 = self.par.ex2
                        dy2 = self.par.ey2
                self.par.ex3 = xc
                self.par.ey3 = yc
                aa = degrees(calc_angle(xc, yc, coord[2], yc, dx1, dy1))
                bb = degrees(calc_angle(xc, yc, dx1, dy1, dx2, dy2))
                delete_list.append(content)
                if event:
                    arc.c_arc(self.par, xc, yc, R = R, start = aa, extent = bb, fill = fill, width = width, sloy = sloy)
                else:
                    arc.c_arc(self.par, xc, yc, R = R, start = aa, extent = bb, fill = fill, width = width, sloy = sloy, temp = 'Yes')
                '''
        if self.par.tracingFlag and  self.par.ex3 != None:
            self.par.trace_on = True
            self.par.trace_x1, self.par.trace_y1 = self.par.ex3,self.par.ey3
            self.par.trace_x2, self.par.trace_y2 = self.par.ex2,self.par.ey2
            
        if event:
            if delete_list:
                self.par.delete(elements = delete_list)
            self.par.edit_clone = False
            self.par.c.delete('temp')
            self.par.changeFlag = True
            self.par.enumerator_p()
            self.par.collection = []
            self.par.kill()
        """
