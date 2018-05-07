# -*- coding: utf-8 -*-
import time
import src.sectors_alg as sectors_alg

def add_undo(par, objects, mode, objects_2 = []):
    ALL = par.ALLOBJECT
    action = []
    #objects_to_history = []
    if mode == 'del':
        objects_to_history = mode_del(objects, ALL, par)
        
    elif mode == 'create':
        objects_to_history = dict(zip(objects, [None]*len(objects)))

    elif mode == 'replace':
        objects_to_history_1 = mode_del(objects, ALL, par)
        objects_to_history_2 = dict(zip(objects_2, [None]*len(objects_2)))
        
        objects_to_history = [objects_to_history_1, objects_to_history_2]
            
        
    par.history_undo.append([mode, objects_to_history])
    if len(par.history_undo) > 20:
        del par.history_undo[0]

def mode_del(objects, ALL, par):
    objects_to_history = {}
    for obj in objects:
        object_type = ALL[obj]['object']
        base_param_names = list(par.objects_base_parametrs[object_type])
        base_param_names.append('class')
        base_param_dict = {}
        for param in base_param_names:
            base_param_dict[param] = ALL[obj][param]        
                
        objects_to_history[obj] = base_param_dict
    return objects_to_history

def undo(par):
    if len(par.history_undo) < 1:
        print "History undo is clean!"
        return
    t1 = time.time()
    action = par.history_undo[-1]
    if action[0] == 'del':
        undo_del(par, action[1])
        num_objs = len(action[1])

        
    elif action[0] == 'create':
        undo_create(par, action[1])
        num_objs = len(action[1])

    elif action[0] == 'replace':
        undo_del(par, action[1][0])
        undo_create(par, action[1][1])
        num_objs = len(action[1][1])

    par.change_pointdata()
    par.c.Refresh()    
    print 'undo ', num_objs, ' objects', time.time() - t1, 'sec'   
    del par.history_undo[-1]


def undo_del(par, action_obsj):
    standart_cd = {
        'in_mass':True,
        'temp':False,
        }
    start = par.total_N                       
    for name, obj in action_obsj.items():
        cd = obj.copy()
        cd.update(standart_cd)
        del cd['class']
        obj['class'].create_object(cd)
        for undo_action in par.history_undo:
            if undo_action[0] == 'create':
                if name in undo_action[1]:
                    undo_action[1][par.total_N] = undo_action[1][name]
                    del undo_action[1][name]
                    
    end = par.total_N
    par.ALLOBJECT, par.sectors = sectors_alg.quadric_mass(par.ALLOBJECT, range(start+1, end+1), par.sectors, par.q_scale)

def undo_create(par, action_obsj):
    del_objects = []
    for obj in action_obsj.keys():
        if obj in par.ALLOBJECT:
            del_objects.append(obj)
    par.delete_objects(del_objects, add_history = False)
