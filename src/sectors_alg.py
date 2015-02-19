# -*- coding: utf-8 -*-
from math import sqrt, floor
def quadric(ALL, sectors, q_scale):
    for i in ALL:
        
        for line in ALL[i]['coords']:
            ex1 = line[0]/q_scale
            ex2 = line[2]/q_scale
            ey1 = line[1]/q_scale
            ey2 = line[3]/q_scale
            dx = abs(ex1 - ex2)
            dy = abs(ey1 - ey2)
            x = int(floor(ex1))
            y = int(floor(ey1))
            n = 1
            if dx == 0:
                x_inc = 0
                dt_dx = 0
                t_next_horizontal = float("inf")
            elif ex2>ex1:
                x_inc = 1
                dt_dx = 1.0 / dx
                n += int(floor(ex2)) - x
                t_next_horizontal = (floor(ex1) + 1 - ex1) * dt_dx
            else:
                x_inc = -1
                dt_dx = 1.0 / dx
                n += x - int(floor(ex2))
                t_next_horizontal = (ex1 - floor(ex1)) * dt_dx

            if dy == 0:
                y_inc = 0
                dt_dy = 0
                t_next_vertical = float("inf")
            elif ey2>ey1:
                y_inc = 1
                dt_dy = 1.0 / dy
                n += int(floor(ey2)) - y
                t_next_vertical = (floor(ey1) + 1 - ey1) * dt_dy
            else:
                y_inc = -1
                dt_dy = 1.0 / dy
                n += y - int(floor(ey2))
                t_next_vertical = (ey1 - floor(ey1)) * dt_dy

            while True:
                sector = str(int(x)) + ' ' + str(int(y))
                sectors[sector].append(i)
                ALL[i]['sectors'].append(sector)
                n -= 1
                if n == 0:
                    break
                if t_next_vertical < t_next_horizontal:
                    y += y_inc
                    t_next_vertical += dt_dy
                else:
                    x += x_inc
                    t_next_horizontal += dt_dx
    return ALL, sectors

def quadric_mass(ALL, mass, sectors, q_scale):
    for ind, i in enumerate(mass):
        try:
            ALL[i]
        except KeyError:
            print 'KeyError!!!'
            print len(mass)
            print ind
        for line in ALL[i]['coords']:
            ex1 = line[0]/q_scale
            ex2 = line[2]/q_scale
            ey1 = line[1]/q_scale
            ey2 = line[3]/q_scale
            dx = abs(ex1 - ex2)
            dy = abs(ey1 - ey2)
            x = int(floor(ex1))
            y = int(floor(ey1))
            n = 1
            if dx == 0:
                x_inc = 0
                dt_dx = 0
                t_next_horizontal = float("inf")
            elif ex2>ex1:
                x_inc = 1
                dt_dx = 1.0 / dx
                n += int(floor(ex2)) - x
                t_next_horizontal = (floor(ex1) + 1 - ex1) * dt_dx
            else:
                x_inc = -1
                dt_dx = 1.0 / dx
                n += x - int(floor(ex2))
                t_next_horizontal = (ex1 - floor(ex1)) * dt_dx

            if dy == 0:
                y_inc = 0
                dt_dy = 0
                t_next_vertical = float("inf")
            elif ey2>ey1:
                y_inc = 1
                dt_dy = 1.0 / dy
                n += int(floor(ey2)) - y
                t_next_vertical = (floor(ey1) + 1 - ey1) * dt_dy
            else:
                y_inc = -1
                dt_dy = 1.0 / dy
                n += y - int(floor(ey2))
                t_next_vertical = (ey1 - floor(ey1)) * dt_dy

            while True:
                sector = str(int(x)) + ' ' + str(int(y))
                #try:
                sectors[sector].append(i)
                #except:
                    #print line
                ALL[i]['sectors'].append(sector)
                n -= 1
                if n == 0:
                    break
                if t_next_vertical < t_next_horizontal:
                    y += y_inc
                    t_next_vertical += dt_dy
                else:
                    x += x_inc
                    t_next_horizontal += dt_dx
    return ALL, sectors

def delete(ALL, sectors, del_ids):
    #Удаляет [del_ids] из sectors и ALLOBJECT
    
    for x in del_ids:
        object_sectors = ALL[x]['sectors']
        for sector in object_sectors:
            sectors[sector].remove(x)
            
        del ALL[x]
    return ALL, sectors
