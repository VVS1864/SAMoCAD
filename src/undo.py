# -*- coding: utf-8 -*-
import time
import src.sectors_alg as sectors_alg

def add_undo(par, objects, mode):
    ALL = par.ALLOBJECT
    action = []
    objects_to_history = []
    if mode == 'del':
        
        for obj in objects:
            
            object_type = ALL[obj]['object']
            base_param_names = list(par.objects_base_parametrs[object_type])
            base_param_names.append('class')
            base_param_dict = {}
            for param in base_param_names:
                base_param_dict[param] = ALL[obj][param]

            objects_to_history.append(base_param_dict)
        par.history_undo.append([mode, objects_to_history])

def undo(par):
    if len(par.history_undo) < 1:
        print "History undo is clean!"
        return
    t1 = time.time()
    standart_cd = {
        'in_mass':True,
        'temp':False,
        }
    start = par.total_N                       
    for obj in par.history_undo[-1][1]:
        cd = obj.copy()
        cd.update(standart_cd)
        del cd['class']
        obj['class'].create_object(cd)
    end = par.total_N
    par.ALLOBJECT, par.sectors = sectors_alg.quadric_mass(par.ALLOBJECT, range(start+1, end+1), par.sectors, par.q_scale)
    par.change_pointdata()
    par.c.Refresh()
    print 'undo ', len(par.history_undo[-1][1]), ' objects', time.time() - t1, 'sec'
        
    del par.history_undo[-1]
    
    

        
                    
                    
                
