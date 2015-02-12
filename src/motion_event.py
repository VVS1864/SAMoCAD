# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *

import src.snap as snap
import src.trace as trace
import src.select_clone as select_clone

def motion(self, e):
# Обработчик события движения курсора
    x = e.GetX()
    y = e.GetY()
    size = glGetIntegerv(GL_VIEWPORT)
    y = size[3]-y
    xy = gluUnProject(x, y, 0)
    
    x_w = xy[0]
    y_w = xy[1]
    
    
    rect = [x-self.snap_s, y-self.snap_s, x+self.snap_s, y+self.snap_s]
    r1 = gluUnProject(rect[0], rect[1], 0)
    r2 = gluUnProject(rect[2], rect[3], 0)
    rect[0], rect[1] = r1[0], r1[1]
    rect[2], rect[3] = r2[0], r2[1]
    
    if self.motion_flag:
        # Навигвция по плану
        self.motion_plane(e)
    else:
        if self.rect:
            #Если рисуется прямоугольник выделения
            self.draw_rect(x_w, y_w)
        
        if (not self.rect) or self.print_flag:
            if self.trace_on:
                self.trace_x2 = x_w
                self.trace_y2 = y_w
                
                trace.tracer(self, self.trace_x1, self.trace_y1, self.trace_x2, self.trace_y2, self.angle_s)
            #if self.trace_obj_on:
                #trace_object.tracer_obj(graf, self.priv_coord[0], self.priv_coord[1], self.snap_s)

            #Если просто перемещается курсор
            self.snap_data = []
            self.snap_color = []
            self.current_data = []
            self.current_color = []
            self.snap = False
            self.current_select = False
            self.current_change = False 
            objects = self.get_current_objects(rect)
        
            if self.snap_flag:
                # Если включена привязка
                r1 = gluUnProject(self.size_simbol_p/2, 0, 0)
                r2 = gluUnProject(self.size_simbol_p, 0, 0)
                r = r2[0] - r1[0]
                
                self.x_priv, self.y_priv, self.tip_p = snap.get_snap(x_w, y_w, r, objects, self)
                x1 = self.x_priv
                y1 = self.y_priv
                
                if self.tip_p == 'r':#Если тип привязки - к конечной точке
                    #Нарисовать знак привязки - квадрат
                    self.snap_data.extend([
                        x1-r,y1-r,x1-r,y1+r,
                        x1-r,y1-r,x1+r,y1-r,
                        x1+r,y1-r,x1+r,y1+r,
                        x1+r,y1+r,x1-r,y1+r,
                        ])
                    self.snap = True
                    #Объект можно изменять
                    self.current_change = True 
                    self.snap_color.extend(self.priv_color * (len(self.snap_data)//2))

                elif self.tip_p == 'c':#Если привязка к середине нарисовать знак привязки - треугольник
                    lines = 3
                    self.snap_data.extend([
                        x1-r,y1-r,x1+r,y1-r,
                        x1-r,y1-r,x1,y1+r,
                        x1,y1+r,x1+r,y1-r,
                        ])
                    self.snap = True
                    self.snap_color.extend(self.priv_color * (len(self.snap_data)//2))

                elif self.tip_p == 'X': #Если привязка к пересечению - нарисовать знак Х
                    
                    self.snap_data.extend([
                        x1-r,y1-r,x1+r,y1+r,
                        x1+r,y1-r,x1-r,y1+r,
                        ])
                    self.snap = True
                    self.snap_color.extend(self.priv_color * (len(self.snap_data)//2))
                    
                elif self.tip_p == 'N': #Если привязка к ближайшей - нарисовать знак N
                    
                    self.snap_data.extend([
                        x1-r,y1-r,x1+r,y1+r,
                        x1+r,y1-r,x1-r,y1+r,
                        x1-r,y1-r,x1-r,y1+r,
                        x1+r,y1-r,x1+r,y1+r,
                        ])
                    self.snap = True
                    self.snap_color.extend(self.priv_color * (len(self.snap_data)//2))
                else:
                    self.snap = False
                
                    
            if not self.snap:
                #Если привязка не поймана
                if self.current_flag:
                    #Если включен выбор текущего
                    if objects:
                        # Если есть набор объектов
                        if objects[0] == 'trace':
                            self.c.Refresh()
                            return
                        clone_data, clone_color = select_clone.select_clone(
                                                        self,
                                                        [objects[0],],
                                                        self.select_color,
                                                        )
                        self.current_data.extend(clone_data)
                        self.current_color.extend(clone_color)
                        self.current_select = True
                        self.current = objects[0]

                    else:
                        # Если ничего в области курсора
                        self.current = None           
    self.c.Refresh()              #Обновить картинку
    #self.c.Update()
    e.Skip()
