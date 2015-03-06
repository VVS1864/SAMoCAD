# -*- coding: utf-8; -*-
import calc
from math import sqrt
#ДАТЬ ТЕКУЩУЮ ПРИВЯЗКУ К ОБЪЕКТУ

def get_snap(x, y, snap_s, find, par):
    par.find_privs = []
    tip_p = None
    stopFlag = False
    #Приравнять возвращаемые координаты к тем, которые пришли
    xi=x 
    yi=y
    priv_coord_list = [] #Список координат приметивов с тегом привязки
    for ind, i in enumerate(find):#Перебрать список объектов
        if par.ALLOBJECT[i]['snap_type'] == 'line':
            for xy in par.ALLOBJECT[i]['coords']:
                a = sqrt((x-xy[0])**2 + (y-xy[1])**2)
                b = sqrt((x-xy[2])**2 + (y-xy[3])**2)
                y0 = xy[1]-((xy[1]-xy[3])/2.0)
                x0 = xy[0]-((xy[0]-xy[2])/2.0)
                c = sqrt((x-x0)**2 + (y-y0)**2)
                xn, yn = calc.min_distanse(xy[0],xy[1],xy[2],xy[3], x,y)
                if xn:
                    d = sqrt((x-xn)**2 + (y-yn)**2)
                else:
                    d = None
                cath = False
                
                if a <= snap_s:
                    yt=xy[1]#Текущимь координатами взять координаты первой точки приметива
                    xt=xy[0]
                    cath = True
                    tip_p = 'r'#Тип привязки - к конточке
                    
                elif b <= snap_s:
                    yt=xy[3]#Текущимь координатами взять координаты первой точки приметива
                    xt=xy[2]
                    cath = True
                    tip_p = 'r'#Тип привязки - к конточке
                    
                elif c <= snap_s:
                    yt=y0#Текущимь координатами взять координаты первой точки приметива
                    xt=x0
                    cath = True
                    tip_p = 'c'#Тип привязки - к середине

                elif len(find) > 1:
                    # Если привязка к 2 приметивам возможна
                    xt, yt, p = intersect_2_objects(par, x, y, find, ind, i, snap_s)
                    
                    if p == 'X':
                        xi = xt
                        yi = yt
                        tip_p = p
                        break
                    
                elif d and d <= snap_s and par.snap_near == True and par.resFlag == True:
                    xi = xn
                    yi = yn
                    #cath = True
                    tip_p = 'N'
                    break

                                     
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
            if a <= snap_s:
                yt = yc #Текущимь координатами взять координаты первой точки приметива
                xt = xc
                cath = True
                tip_p = 'r'#Тип привязки - к конточке
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

            elif len(find) > 1:
                    # Если привязка к 2 приметивам возможна
                    xt, yt, p = intersect_2_objects(par, x, y, find, ind, i, snap_s)
                    if p == 'X':
                        xi = xt
                        yi = yt
                        tip_p = p
                        break

            elif N_dist <= snap_s and par.snap_near == True and par.resFlag == True:
                xi = xn#Назначить координаты выхода полученным координатам
                yi = yn
                tip_p = 'N'
                break

            if cath:
                #priv_coord_list.append((xy,'line'))
                par.find_privs.append(i)#Добавить приметив в список привязок
                if stopFlag == False:#Если точка привязки не была найдена ранее
                    xi = xt#Назначить возвращаемые координаты равными координатам точки
                    yi = yt
                    stopFlag = True#Остановить назначение возвращаемых координат
                break

        '''
        if 'priv' in tags and 'line' in tags:#Если у приметива есть тег привязки
            xy = self.c.coords(i)#Взять координаты приметива
            priv_coord_list.append((xy,'line'))#Добавить координаты приметива в список
            ay1 = abs(y-xy[1])#Получить разность координат приметива и пришедших в метод координат (коорд. курсора)
            ay2 = abs(y-xy[3])
            ax1 = abs(x-xy[0])
            ax2 = abs(x-xy[2])
            if ax1<=ax2 and ax1<=self.snap_s and ay1<=self.snap_s: #or ay2<=self.snap_s):#Если разность координат х по первой точке меньше, чем по второй и эта разность меньше self.snap_s
                if ay1<=ay2 and ay1<self.snap_s:#Если разность по у первой точки меньше, чем по второй и эта разность меньше self.snap_s
                    yt=xy[1]#Текущимь координатами взять координаты первой точки приметива
                    xt=xy[0]
                    tip_p = 'r'#Тип привязки - к конточке
                    self.find_privs.append(i)#Добавить приметив в список привязок
                    if stopFlag == False:#Если точка привязки не была найдена ранее
                        xi = xt#Назначить возвращаемые координаты равными координатам точки
                        yi = yt
                        stopFlag = True#Остановить назначение возвращаемых координат

            elif ax1>=ax2 and ax2<=self.snap_s and ay2<=self.snap_s:#(ay1<=self.snap_s or ay2<=self.snap_s):#Если разность координат х по второй точке меньше, чем по первой и эта разность меньше self.snap_s
                if ay1>=ay2 and ay2<=self.snap_s:
                    yt=xy[3]
                    xt=xy[2]
                    tip_p = 'r'
                    self.find_privs.append(i)
                    if stopFlag == False:
                        xi = xt
                        yi = yt
                        stopFlag = True
        '''
        '''
            else:#Если не подошел не один из вариантов - привязка к середине
                y0=xy[1]-((xy[1]-xy[3])/2.0)
                x0=xy[0]-((xy[0]-xy[2])/2.0)

                if abs(x-x0)<=self.snap_s and abs(y-y0)<=self.snap_s:
                    yt=y0
                    xt=x0
                    tip_p = 'c'
                    self.find_privs.append(i)
                    if stopFlag == False:
                        xi = xt
                        yi = yt
                        stopFlag = True
           
            if 'temp' in tags or 'cir_centr' in tags or 'a_centr' in tags:
                tip_p = None
                stopFlag = False
                xi=x
                yi=y

        elif 'priv' in tags and 'cir' in tags:
            xy = self.c.coords(i)
            priv_coord_list.append((xy,'cir'))
            xc,yc,R = self.coord_circle(xy[0],xy[1],xy[2],xy[3])
            if abs(x - xc)<=self.snap_s:
                if abs(yc-R - y) <= self.snap_s:
                    xi = xc
                    yi = yc-R
                    tip_p = 'r'
                    stopFlag = True
                    self.find_privs.append(i)
                elif abs(yc+R - y) <= self.snap_s:
                    xi = xc
                    yi = yc+R
                    tip_p = 'r'
                    stopFlag = True
                    self.find_privs.append(i)

            elif abs(y - yc)<=self.snap_s:
                if abs(xc-R - x) <= self.snap_s:
                    xi = xc-R
                    yi = yc
                    tip_p = 'r'
                    stopFlag = True
                    self.find_privs.append(i)
                elif abs(xc+R - x) <= self.snap_s:
                    xi = xc+R
                    yi = yc
                    tip_p = 'r'
                    stopFlag = True
                    self.find_privs.append(i)


        elif 'priv' in tags and 'a' in tags:
            xy = self.c.coords(i)
            start = float(self.c.itemcget(i, 'start'))
            extent = float(self.c.itemcget(i, 'extent'))
            priv_coord_list.append((xy,'a'))
            xc, yc, dx1, dy1, dx2, dy2 = get_conf.get_arc_coord(xy[0],xy[1],xy[2],xy[3], start, extent)
            R = (xy[2]-xy[0])/2.0
            if abs(x - dx1)<=self.snap_s:
                if abs(y - dy1)<=self.snap_s:
                    xi = dx1
                    yi = dy1
                    tip_p = 'r'
                    stopFlag = True
                    self.find_privs.append(i)
            elif abs(x - dx2)<=self.snap_s:
                if abs(y - dy2)<=self.snap_s:
                    xi = dx2
                    yi = dy2
                    tip_p = 'r'
                    stopFlag = True
                    self.find_privs.append(i)
        '''
        '''
    #Привязка к ближайшей точке на линии - Если неподошел не один предыдущий вариант
    
    if stopFlag == False and par.snap_near == True and par.resFlag == True and priv_coord_list:
        for j, i in enumerate(priv_coord_list):
            xy = priv_coord_list[j][0]
            if i[1] == 'line':
                xt, yt = calc.min_distanse(xy[0],xy[1],xy[2],xy[3], x,y)
                if xt:
                    xi = xt
                    yi = yt
                    tip_p = 'N'
                    break
        '''
        '''
            else:
                xc,yc,R = self.coord_circle(xy[0],xy[1],xy[2],xy[3])
                if i[1] == 'a':
                    xt,yt, d = calc.min_distanse_cir(xc, yc, R, x, y)
                    if d<=self.snap_s:
                        xi = xt#Назначить координаты выхода полученным координатам
                        yi = yt
                        tip_p = 'N'
                        break

                elif i[1] == 'cir':
                    xt,yt, d = calc.min_distanse_cir(xc, yc, R, x, y)
                    if d<=self.snap_s:
                        xi = xt#Назначить координаты выхода полученным координатам
                        yi = yt
                        tip_p = 'N'
                        break

        '''
        '''
    ### Привязка к двум приметивам ###
    if len(find) > 1 and stopFlag == False:#Привязка к пересечению
        print 'X'
        for ind, i in enumerate(priv_coord_list):#Перебрать список координат
            #ind = priv_coord_list.index(i)#Взять индекс текущего элемента
            if ind == 0:#Если элемент первый - приверять пересечение с последующим
                ii = 1
            else:#Иначе с предыдущим
                ii = -1
            r = priv_coord_list[ind+ii]
            if i[1] == 'line' and r[1] == 'line':
                xt,yt = calc.intersection_l_l(i[0][0],i[0][1],i[0][2],i[0][3],r[0][0],r[0][1],r[0][2],r[0][3])#Проверить есть ли точка пересечения, если да - вычислить
                if xt != None:#Если точка есть
                    if (abs(y-yt)<=snap_s) and (abs(x-xt)<=snap_s):#Если разность координат не превышает self.snap_s
                        if (xt != i[0][0] or yt != i[0][1]) and (xt != i[0][2] or yt != i[0][3]):#Если эта точка не равна одной из точек
                            if (xt != r[0][0] or yt != r[0][1]) and (xt != r[0][2] or yt != r[0][3]):
                                xi = xt#Назначить координаты выхода полученным координатам
                                yi = yt
                                tip_p = 'X'#Тип привязки - пересечение
                                break
        '''
        '''
            elif (i[1] == 'line' and r[1] in ['cir', 'a']) or (i[1] in ['cir', 'a'] and r[1] == 'line'):
                if i[1] == 'line':
                    line = i
                    circle = r
                else:
                    line = r
                    circle = i
                xc,yc,R = self.coord_circle(circle[0][0],circle[0][1],circle[0][2],circle[0][3])
                xt,yt = calc.intersection_l_c(xc, yc, R, line[0][0], line[0][1], line[0][2], line[0][3], x, y)
                if xt != None:#Если точка есть
                    if (abs(y-yt)<=self.snap_s) and (abs(x-xt)<=self.snap_s):#Если разность координат не превышает self.snap_s
                        xi = xt#Назначить координаты выхода полученным координатам
                        yi = yt
                        tip_p = 'X'#Тип привязки - пересечение
                        break
            elif i[1] in ['cir', 'a'] and r[1] in ['cir', 'a']:
                xc1,yc1,R1 = self.coord_circle(i[0][0],i[0][1],i[0][2],i[0][3])
                xc2,yc2,R2 = self.coord_circle(r[0][0],r[0][1],r[0][2],r[0][3])
                xt, yt = calc.intersection_c_c(xc1, yc1, R1, xc2, yc2, R2, x, y)
                if xt != None:#Если точка есть
                    if (abs(y-yt)<=self.snap_s) and (abs(x-xt)<=self.snap_s):#Если разность координат не превышает self.snap_s
                        xi = xt#Назначить координаты выхода полученным координатам
                        yi = yt
                        tip_p = 'X'#Тип привязки - пересечение
                        break
        '''
    #if f == None: #Если список приметивов не был назначен - включить функцию перебора привязки
        #self.perebor_priv()
    return xi,yi,tip_p #Вернуть координаты привязки, и ее тип

def intersect_2_objects(par, x, y, find, ind, i, snap_s):
    try:
        r = find[ind+1]
    except:
        return None, None, None
    line = True
    circle = False
    if par.ALLOBJECT[r]['snap_type'] == 'line':
        obj1 = r
        obj2 = i
    elif par.ALLOBJECT[i]['snap_type'] == 'line':
        obj1 = i
        obj2 = r
        circle = True
    else:
        obj1 = i
        obj2 = r
        circle = True
        line = False
        
    #if par.ALLOBJECT[r]['object'] in ('line', 'text_line', 'dim'):
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
    
