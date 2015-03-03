import src.sectors_alg as sectors_alg
#class Edit_prop:
'''
    def __init__(self, par, params, objects):
        self.par = par
        new_objects = self.param_edit(params, objects)
        return new_objects
'''
            
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
        
    #print remove_list
    if remove_list:
        new_objects = range(start+1, end+1)
        #del_list = [x[0] for x in remove_list]
        par.ALLOBJECT, par.sectors = sectors_alg.quadric_mass(
            par.ALLOBJECT,
            new_objects,
            par.sectors,
            par.q_scale
            )
    
        par.delete_objects(remove_list, False)
        
        par.change_pointdata()
    return new_objects
            #self.par.collection.remove(r[0])
            #self.par.collection.append(r[1])
        
