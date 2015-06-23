import src.sectors_alg as sectors_alg
import src.undo as undo
            
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
        undo.add_undo(par, objects = remove_list, mode = 'replace', objects_2 = new_objects)

        par.delete_objects(remove_list, False)
        
        par.change_pointdata()
    return new_objects        
