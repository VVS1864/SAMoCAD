# -*- coding: utf-8 -*-

def select_clone(par, objects, color):
    #Возвращает массив координат линий клонированных объектов + массив с указанным цветом
    clone_data = []
    clone_color = []
    
    for i in objects:
        clone_data.extend(par.ALLOBJECT[i]['pointdata'])
    clone_color.extend(color*(len(clone_data)//2))
        
    return clone_data, clone_color
