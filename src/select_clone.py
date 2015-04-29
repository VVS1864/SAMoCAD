# -*- coding: utf-8 -*-

def select_clone(par, objects, color):
    #Возвращает массив координат линий клонированных объектов + массив с указанным цветом
    clone_data = []
    clone_color = []
    '''
    begin_list, end_list = par.get_indexes(objects)
    for i in xrange(len(objects)):
        clone_data.extend(par.pointdata[begin_list[i]:end_list[i]])
    
    clone_color.extend(color*(len(clone_data)//2))
    '''
    for i in objects:
        clone_data.extend(par.ALLOBJECT[i]['pointdata'])
    clone_color.extend(color*(len(clone_data)//2))
        
    return clone_data, clone_color
