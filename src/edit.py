# -*- coding: utf-8; -*-
from math import sqrt, pi, degrees, radians
from calc import calc_angle
import line, dimension, text_line, circle, arc
import get_conf
from get_conf import get_arc_conf
#ИЗИЕНЕНИЕ УЗЛОВ
class Edit_node:
    def __init__(self, par):
        self.par = par
        self.editEvent()
        
    def editEvent(self):
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
            if not self.par.collection:#Если объекты не выбраны - искать изменяемые в списке привязок
                e = self.par.edit_collektor(self.par.find_privs2)
            self.par.dialog.config(text = (u'Etit node - %s objects:') %(len(self.par.collection)))
            self.par.info.config(text = u'Escape - stop')
            self.par.set_coord()
            self.par.edit_clone = True
            

    def editEvent2(self, event = None):
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
                self.par.ALLOBJECT[content]['class'].edit(self.par, content, event)
            if content[0] == 'd':
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
            elif content[0] == 'a':
                find = self.par.ALLOBJECT[content]['id']
                for i in find:
                    tag = self.par.ALLOBJECT[content]['id'][i]
                    if 'a' in tag:
                        coord = self.par.c.coords(i)
                xc, yc, dx1, dy1, dx2, dy2, fill, width, sloy = get_arc_conf(content, self.par)
                '''
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
                '''
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
