import src.sectors_alg as sectors_alg
            
def Edit_prop(par, params, objects):
    new_objects = []
    remove_list = []
    if objects:
        start = par.total_N
        for i in objects:
            cNew = par.ALLOBJECT[i]['class'].edit_prop(params)
            if cNew:
                remove_list.append(i)
        end = par.total_N
        

    if remove_list:
        new_objects = range(start+1, end+1)
        par.ALLOBJECT, par.sectors = sectors_alg.quadric_mass(
            par.ALLOBJECT,
            new_objects,
            par.sectors,
            par.q_scale
            )
    
        par.delete_objects(remove_list, False)
        
        par.change_pointdata()
    return new_objects        
