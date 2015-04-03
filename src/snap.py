# -*- coding: utf-8; -*-
import calc
from math import sqrt
#ДАТЬ ТЕКУЩУЮ ПРИВЯЗКУ К ОБЪЕКТУ

def get_snap(x, y, snap_s, find, par):
    par.find_privs = []
    tip_p = None
    N_dist = None
    stopFlag = False
    #Приравнять возвращаемые координаты к тем, которые пришли
    xi=x 
    yi=y
    priv_coord_list = [] #Список координат приметивов с тегом привязки
    for ind, i in enumerate(find):#Перебрать список объектов
        tip_p = None
        if par.ALLOBJECT[i]['snap_type'] == 'line':
            for xy in par.ALLOBJECT[i]['coords']:
                
                a = sqrt((x-xy[0])**2 + (y-xy[1])**2)
                b = sqrt((x-xy[2])**2 + (y-xy[3])**2)
                y0 = xy[1]-((xy[1]-xy[3])/2.0)
                x0 = xy[0]-((xy[0]-xy[2])/2.0)
                c = sqrt((x-x0)**2 + (y-y0)**2)
                xn, yn = calc.min_distanse(xy[0],xy[1],xy[2],xy[3], x,y)
                if xn:
                    N_dist = sqrt((x-xn)**2 + (y-yn)**2)
                else:
                    N_dist = None
                cath = False

                if c <= snap_s and tip_p != 'r':
                    yt=y0#Текущимь координатами взять координаты первой точки приметива
                    xt=x0
                    cath = True
                    tip_p = 'c'#Тип привязки - к середине
                
                elif a <= snap_s:
                    yt=xy[1]#Текущимь координатами взять координаты первой точки приметива
                    xt=xy[0]
                    cath = True
                    tip_p = 'r'#Тип привязки - к конточке
                    
                elif b <= snap_s:
                    yt=xy[3]#Текущимь координатами взять координаты первой точки приметива
                    xt=xy[2]
                    cath = True
                    tip_p = 'r'#Тип привязки - к конточке
                                     
                if cath:
                    priv_coord_list.append((xy,'line'))
                    par.find_privs.append(i)#Добавить приметив в список привязок
                    if stopFlag == False:#Если точка привязки не была найдена ранее
                        xi = xt#Назначить возвращаемые координаты равными координатам точки
                        yi = yt
                        stopFlag = True#Остановить назначение возвращаемых координат
                    break
                

        elif par.ALLOBJECT[i]['snap_type'] == 'circle':
            R = par.ALLOBJECT[i]['R']
            xc = par.ALLOBJECT[i]['x1']
            yc = par.ALLOBJECT[i]['y1']
            a = sqrt((x-xc)**2 + (y-yc)**2)
            b = sqrt((x-(xc-R))**2 + (y-yc)**2)
            c = sqrt((x-(xc+R))**2 + (y-yc)**2)
            d = sqrt((x-xc)**2 + (y-(yc-R))**2)
            e = sqrt((x-xc)**2 + (y-(yc+R))**2)
            xn, yn, N_dist = calc.min_distanse_cir(xc, yc, R, x, y)
            
            cath = False
            if a <= snap_s and tip_p != 'r':
                yt = yc #Текущимь координатами взять координаты первой точки приметива
                xt = xc
                cath = True
                tip_p = 'c'#Тип привязки - к середине
                
            elif b <= snap_s:
                yt = yc #Текущимь координатами взять координаты первой точки приметива
                xt = xc-R
                cath = True
                tip_p = 'r'#Тип привязки - к конточке

            elif c <= snap_s:
                yt = yc #Текущимь координатами взять координаты первой точки приметива
                xt = xc+R
                cath = True
                tip_p = 'r'#Тип привязки - к конточке

            elif d <= snap_s:
                yt = yc-R #Текущимь координатами взять координаты первой точки приметива
                xt = xc
                cath = True
                tip_p = 'r'#Тип привязки - к конточке
                
            elif e <= snap_s:
                yt = yc+R #Текущимь координатами взять координаты первой точки приметива
                xt = xc
                cath = True
                tip_p = 'r'#Тип привязки - к конточке

            if cath:
                par.find_privs.append(i)#Добавить приметив в список привязок
                if stopFlag == False:#Если точка привязки не была найдена ранее
                    xi = xt#Назначить возвращаемые координаты равными координатам точки
                    yi = yt
                    stopFlag = True#Остановить назначение возвращаемых координат
            
        elif par.ALLOBJECT[i]['snap_type'] == 'arc':
            R = par.ALLOBJECT[i]['R']
            xc = par.ALLOBJECT[i]['x1']
            yc = par.ALLOBJECT[i]['y1']
            x1 = par.ALLOBJECT[i]['x2']
            y1 = par.ALLOBJECT[i]['y2']
            x2 = par.ALLOBJECT[i]['x3']
            y2 = par.ALLOBJECT[i]['y3']
            
            a = sqrt((x-xc)**2 + (y-yc)**2)
            b = sqrt((x-x1)**2 + (y-y1)**2)
            c = sqrt((x-x2)**2 + (y-y2)**2)
            xn, yn, N_dist = calc.min_distanse_cir(xc, yc, R, x, y)
            cath = False
            if a <= snap_s and tip_p != 'r':
                yt = yc #Текущимь координатами взять координаты первой точки приметива
                xt = xc
                cath = True
                tip_p = 'c'#Тип привязки - к середине
                
            elif b <= snap_s:
                
                yt = y1 #Текущимь координатами взять координаты первой точки приметива
                xt = x1
                cath = True
                tip_p = 'r'#Тип привязки - к конточке

            elif c <= snap_s:
                
                yt = y2 #Текущимь координатами взять координаты первой точки приметива
                xt = x2
                cath = True
                tip_p = 'r'#Тип привязки - к конточке

            if cath:
                par.find_privs.append(i)#Добавить приметив в список привязок
                if stopFlag == False:#Если точка привязки не была найдена ранее
                    xi = xt#Назначить возвращаемые координаты равными координатам точки
                    yi = yt
                    stopFlag = True#Остановить назначение возвращаемых координат
                break

    if len(find) > 1:
        # Если привязка к 2 приметивам возможна
        xt, yt, p = intersect_2_objects(par, x, y, find, snap_s)
        if p == 'X':
            xi = xt
            yi = yt
            tip_p = p

    if not tip_p and N_dist and N_dist <= snap_s and par.snap_near == True and par.resFlag == True:
        xi = xn
        yi = yn
        tip_p = 'N'

    return xi,yi,tip_p #Вернуть координаты привязки, и ее тип

def intersect_2_objects(par, x, y, find, snap_s):
    for ind, i in enumerate(find):
        try:
            r = find[ind+1]
        except:
            return None, None, None
        
        if par.ALLOBJECT[i]['snap_type'] != 'line' and par.ALLOBJECT[r]['snap_type'] != 'line':
            obj1 = r
            obj2 = i
            circle = True
            line = False
        elif par.ALLOBJECT[i]['snap_type'] != 'line':
            obj1 = r
            obj2 = i
            circle = True
            line = True
        elif par.ALLOBJECT[r]['snap_type'] != 'line':
            obj1 = i
            obj2 = r
            circle = True
            line = True
        else:
            obj1 = i
            obj2 = r
            circle = False
            line = True
            
        if line and not circle:
            for xy in par.ALLOBJECT[obj1]['coords']:
                for rxy in par.ALLOBJECT[obj2]['coords']:
                    #Проверить есть ли точка пересечения, если да - вычислить
                    xt, yt = calc.intersection_l_l(rxy[0],rxy[1],rxy[2],rxy[3],
                                                  xy[0],xy[1],xy[2],xy[3])
                    if xt != None:
                        #Если точка есть
                        a = sqrt((x-xt)**2 + (y-yt)**2)
                        if a < snap_s and par.resFlag == True: 
                            #Если разность координат не превышает self.snap_s                        
                            xi = xt#Назначить координаты выхода полученным координатам
                            yi = yt
                            tip_p = 'X'#Тип привязки - пересечение
                            
                            return xi, yi, tip_p
                        
        elif line and circle:
            xc = par.ALLOBJECT[obj2]['x1']
            yc = par.ALLOBJECT[obj2]['y1']
            R = par.ALLOBJECT[obj2]['R']
            for xy in par.ALLOBJECT[obj1]['coords']:
                
                xt,yt = calc.intersection_l_c(xc, yc, R, xy[0], xy[1], xy[2], xy[3], x, y)
                if xt != None:#Если точка есть
                    a = sqrt((x-xt)**2 + (y-yt)**2)
                    if a < snap_s and par.resFlag == True:#Если разность координат не превышает self.snap_s
                        xi = xt#Назначить координаты выхода полученным координатам
                        yi = yt
                        tip_p = 'X'#Тип привязки - пересечение
                        return xi, yi, tip_p

        elif not line and circle:
            xc1 = par.ALLOBJECT[obj1]['x1']
            yc1 = par.ALLOBJECT[obj1]['y1']
            R1 = par.ALLOBJECT[obj1]['R']
            
            xc2 = par.ALLOBJECT[obj2]['x1']
            yc2 = par.ALLOBJECT[obj2]['y1']
            R2 = par.ALLOBJECT[obj2]['R']

            xt, yt = calc.intersection_c_c(xc1, yc1, R1, xc2, yc2, R2, x, y)
            if xt != None:#Если точка есть
                a = sqrt((x-xt)**2 + (y-yt)**2)
                if a < snap_s and par.resFlag == True:#Если разность координат не превышает self.snap_s
                    xi = xt#Назначить координаты выхода полученным координатам
                    yi = yt
                    tip_p = 'X'#Тип привязки - пересечение
                    return xi, yi, tip_p
                
    return None, None, None
    
