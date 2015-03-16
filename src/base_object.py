class Base_object(object):
    def __init__(self, par, obj):
        self.par = par
        self.obj = obj
        self.text_changeble = False

    ### History_undo method ###
    def undo(self, cd, zoomOLDres, xynachres):
        pass      
    
    ### Edit_prop method ###
    def edit_prop(self, params):
        cd = self.par.ALLOBJECT[self.obj]
        for param in params:
            if param in cd:
                cd[param] = params[param]
        cd['temp'] = False
        cd['in_mass'] = True
        cNew = self.create_object(cd)
        return cNew

    ### Edit method ###
    def edit(self, x1, y1, x2, y2):
        cd = self.par.ALLOBJECT[self.obj].copy()
        cd['in_mass'] = True
        cd['temp'] = False
        cNew = self.edit_object(x1, y1, x2, y2, cd)
        return cNew

    def edit_temp(self, x1, y1, x2, y2):
        cd = self.par.ALLOBJECT[self.obj].copy()
        cd.update(self.temp_dict)
        cd['in_mass'] = False
        self.edit_object(x1, y1, x2, y2, cd)

    ### Rotate methods ###
    def rotate(self, x0, y0, msin, mcos, angle):
        pass

    def rotate_temp(self, x0, y0, msin, mcos, angle):
        pass

    ### Offset method ###
    def offset(self, pd, x3, y3):
        pass

    ### Rotate methods ###    
    def mirror(self, x0, y0, msin, mcos):
        pass

    def mirror_temp(self, x0, y0, msin, mcos):
        pass

    ### Copy method ###    
    def copy(self, d):
        pass

    def copy_temp(self, d):
        pass

    ### Scale method ###    
    def scale(self, x, y, scale_factor):
        pass
