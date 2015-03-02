import src.sectors_alg as sectors_alg
class Edit_prop:
    def __init__(self, par, params, objects):
        self.par = par
        self.param_edit(params, objects)
            
    def param_edit(self, params, objects):
        
        remove_list = []
        if objects:
            start = self.par.total_N
            for i in objects:
                cNew = self.par.ALLOBJECT[i]['class'].edit_prop(params)
                if cNew:
                    remove_list.append(i)
            end = self.par.total_N
            
        #print remove_list
        if remove_list:
            
            #del_list = [x[0] for x in remove_list]
            self.par.ALLOBJECT, self.par.sectors = sectors_alg.quadric_mass(
                self.par.ALLOBJECT,
                range(start+1, end+1),
                self.par.sectors,
                self.par.q_scale
                )
        
            self.par.delete_objects(remove_list, False)
            
            self.par.change_pointdata()
                #self.par.collection.remove(r[0])
                #self.par.collection.append(r[1])
        
