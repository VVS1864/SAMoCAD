# -*- coding: utf-8 -*-
from math import sqrt, degrees, radians, sin, cos, pi
import calc

import src.sectors_alg as sectors_alg
from src.base import Base
from src.base_object import Base_object

#КРУГ
list_prop = (
    'color',
    'width',
    'layer',
    'stipple',
    'factor_stipple',
    'R'
    )

temp_dict = {
    'width' : 1,
    'layer' : 't',
    'color' : [255, 255, 0],
    'stipple' : None,
    'factor_stipple' : None,
    'in_mass' : False,
    'temp' : True,
    }

#События
class Circle(Base):
    def __init__(self, par):
        super(Circle, self).__init__(par)
        self.risCircle()
        
    def risCircle(self):
        self.par.kill()
        super(Circle, self).func_1(Circle, self.circle, 'Circle - center point:', 'Enter - stop')

        '''
        self.par.kill()
        self.par.standart_unbind()
        self.par.old_func = 'self.risCircle()'
        self.par.c.bind('<Button-1>', self.circle)
        self.par.dialog.config(text = 'Circle - center point:')
        self.par.info.config(text = 'Enter - stop')
        '''

    def circle(self, event):
        self.par.ex, self.par.ey = super(Circle, self).func_2(
            self.circle2,
            'Circle - radius:',
            True,
            )
        '''
        self.par.command.focus_set()
        self.par.set_coord()
        self.par.ex = self.par.priv_coord[0]
        self.par.ey = self.par.priv_coord[1]
        self.par.c.bind_class(self.par.c,"<1>", self.circle2)
        self.par.dialog.config(text = 'Circle - radius:')
        self.par.circle_clone = True
        '''

    def circle2(self, event=None):
        kwargs = {
            'par' : self.par,
            'x1' : self.par.ex,
            'y1' : self.par.ey,
            'x2' : self.par.ex2,
            'y2' : self.par.ey2,        
            'width' : self.par.width,
            'layer' : self.par.layer,
            'color' : self.par.color,
            'R' : False,
            'in_mass' : False,
            'temp' : False,
            }
        super(Circle, self).func_3(event, c_circle, kwargs)

        '''
        self.par.command.focus_set()
        self.par.ex2 = self.par.priv_coord[0]
        self.par.ey2 = self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        self.par.ex2,self.par.ey2 = self.par.commer(self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
        if event:
            c_circle(self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
            self.par.history_undo.append(('c_', self.par.Ncircle))
            #self.par.com = None
            self.par.changeFlag = True
            self.par.circle_clone = False
            self.par.enumerator_p()
            self.par.risCircle()

        else:
            self.par.set_coord()
            c_circle(self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2, temp = 'Yes')
        '''
        if event:
            self.risCircle()
        
#Отрисовка
def c_circle(
    par,
    x1,
    y1,
    x2,
    y2,
    width,
    layer,
    color,
    #stipple,
    #factor_stipple,
    R,
    in_mass,
    temp = False,
    ):
    if not R:
        R = sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
    xbox1=x1-R
    xbox2=x1+R
    ybox1=y1-R
    ybox2=y1+R
        
    if not (0 <= xbox1 <= par.drawing_w
            and 0 <= ybox1 <= par.drawing_h
            and 0 <= xbox2 <= par.drawing_w
            and 0 <= ybox2 <= par.drawing_h):
        return False

    s = R/20.0
    lines = [[x1,y1-s,x1,y1+s], [x1-s,y1,x1+s,y1]]
    pointdata = [x1,y1-s,x1,y1+s, x1-s,y1,x1+s,y1]
    lines_c, pointdata_c = oval_lines(x1, y1, R, (0, 360))
    lines.extend(lines_c)
    pointdata.extend(pointdata_c)
    if not temp:
        par.total_N+=1
        
        if not lines:
            return
        else:
            
            par.IDs.append(par.total_N)
            par.IDs.extend([0,]*(len(lines)-1))
            par.pointdata.extend(pointdata)
            par.colordata.extend(color*2*len(lines))
            


        object_circle = Object_circle(par, par.total_N)
        dict_prop = {}
        for k,v in locals().iteritems():
            if k in list_prop:
                dict_prop[k] = v
        #dict_prop = {k:v for k,v in locals().iteritems() if k in list_prop}        
        par.ALLOBJECT[par.total_N] = {
                                    'object':'circle',
                                    'class':object_circle,
                                    'sectors':[],
                                    'coords': lines,
                                    'lines': lines,
                                    'x1': x1,
                                    'y1': y1,
                                    'snap_type':'circle',
                                    }
        par.ALLOBJECT[par.total_N].update(dict_prop)
        if not in_mass:
            par.ALLOBJECT, par.sectors = sectors_alg.quadric_mass(par.ALLOBJECT, [par.total_N,], par.sectors, par.q_scale)
            par.change_pointdata()
            par.c.Refresh()              #Обновить картинку
            par.c.Update()
        return True
        
    else:
        par.dynamic_data.extend(pointdata)
        par.dynamic_color.extend(color*2*len(lines))

                
        '''    
        id_dict = {}
        if R == None:
            R = sqrt((xr-x0)*(xr-x0) + (yr-y0)*(yr-y0))
        x1=x0-R
        x2=x0+R
        y1=y0-R
        y2=y0+R
        s = R/20.0
        R = par.n_coordinator(R)
        id = par.c.create_oval(x1,y1,x2,y2,outline=fill, full=None,width=width,tags = ('obj', ID))
        id_dict[id] = ('cir', 'priv')
        id = par.c.create_line(x0-s,y0-s,x0+s,y0+s,fill=fill,tags = ('obj', ID, 'cir_centr'))
        id_dict[id] = ('line', 'priv', 'cir_centr')
        id = par.c.create_line(x0+s,y0-s,x0-s,y0+s,fill=fill,tags = ('obj', ID, 'cir_centr'))
        id_dict[id] = ('line', 'priv', 'cir_centr')

        object_circle = Object_circle(par, ID)
        dict_prop = {}
        for k,v in locals().iteritems():
            if k in list_prop:
                dict_prop[k] = v

        par.ALLOBJECT[ID] = {
                            'object':'circle',
                            'id':id_dict,
                            'class':object_circle,
                            }
        par.ALLOBJECT[ID].update(dict_prop)
    else:
        if R == None:
            R = sqrt((xr-x0)*(xr-x0) + (yr-y0)*(yr-y0))
        x1=x0-R
        x2=x0+R
        y1=y0-R
        y2=y0+R
        s = R/20.0
        R = par.n_coordinator(R)
        par.c.create_oval(x1,y1,x2,y2,outline=fill, full=None,width=width,tags = ('obj', 'temp'))
        par.c.create_line(x0-s,y0-s,x0+s,y0+s,fill=fill,tags = ('obj', 'temp'))
        par.c.create_line(x0+s,y0-s,x0-s,y0+s,fill=fill,tags = ('obj', 'temp'))
        '''

def oval_lines(x, y, R, sector_angle):
    w = h = 2.0*R
    angle_increment = pi*2 / 20
    theta = 0
    lines = []
    pointdata = []
    x1 = x+R
    y1 = y
    while theta < pi*2:
        theta += angle_increment
        x2 = w/2 * cos(theta) + x
        y2 = h/2 * sin(theta) + y
        lines.append([x1, y1, x2, y2])
        pointdata.extend([x1, y1, x2, y2])
        x1 = x2
        y1 = y2
    return lines, pointdata
    
class Object_circle(Base_object):
    def __init__(self, par, obj):
        super(Object_circle, self).__init__(par, obj)


    def create_object(self, cd):
        if 'R' in cd:
            cd['x2'], cd['y2'] = 0, 0
        cNew = c_circle(
            self.par,
            cd['x1'],
            cd['y1'],
            cd['x2'],
            cd['y2'],
            R = cd['R'],
            width = cd['width'],
            layer = cd['layer'],
            color = cd['color'],
            in_mass = cd['in_mass'],
            temp = cd['temp'],
            )
            
        return cNew


    ### Edit_prop method ###
    def save(self, dxf):
        cd = self.get_conf()
        e = "self.c_circle(x0 = %(xc)s, y0 = %(yc)s, R = %(R)s, width = %(width)s, fill = '%(fill)s', sloy = %(sloy)s)"
        e = (e % cd)
        if dxf:
            cd['fill'] = dxf_colorer(cd['fill'])
        return e, cd

    ### Edit method ###
    def edit(self, event):
        cd = self.get_conf()
        cd['R'] = sqrt((self.par.ex2-cd['xc'])**2 + (self.par.ey2-cd['yc'])**2)
        
        if event:
            temp = None
        else:
            temp = 'Yes'

        c_circle(self.par, cd['xc'], cd['yc'],
                width = cd['width'],
                sloy = cd['sloy'],
                fill = cd['fill'],
                R = cd['R'], 
                temp = temp)

    ### Rotate methods ###
    def rotate(self, x0, y0, msin, mcos, angle):
        cd = self.par.ALLOBJECT[self.obj].copy()
        [[cd['x1'], cd['y1']],] = calc.rotate_points(x0, y0, [[cd['x1'], cd['y1']],], msin, mcos)
        
        cd['in_mass'] = True
        cd['temp'] = False
        cNew = self.create_object(cd)
        return cNew

    def rotate_temp(self, x0, y0, msin, mcos, angle):
        cd = self.par.ALLOBJECT[self.obj].copy()
        [[cd['x1'], cd['y1']],] = calc.rotate_points(x0, y0, [[cd['x1'], cd['y1']],], msin, mcos)
        
        cd.update(temp_dict)
        self.create_object(cd)

    ### Offset method ###
    def offset(self, pd, x3, y3):
        cd = self.get_conf()
        r = sqrt((cd['xc']-x3)**2 + (cd['yc']-y3)**2)
        if cd['R']<r:
            cd['R'] += pd
        else:
            cd['R'] -= pd
        c_circle(self.par, cd['xc'],cd['yc'], R = cd['R'])

    ### Mirror methods ###
    def mirror(self, x1, y1, msin, mcos):
        cd = self.par.ALLOBJECT[self.obj].copy()
        [[cd['x1'], cd['y1']],] = calc.mirror_points(x1, y1, [[cd['x1'], cd['y1']],], msin, mcos)
        cd['in_mass'] = True
        cd['temp'] = False
        cNew = self.create_object(cd)
        return cNew

    def mirror_temp(self, x1, y1, msin, mcos):
        cd = self.par.ALLOBJECT[self.obj].copy()
        [[cd['x1'], cd['y1']],] = calc.mirror_points(x1, y1, [[cd['x1'], cd['y1']],], msin, mcos)
        cd.update(temp_dict)
        self.create_object(cd)

    ### Copy method ###
    def copy(self, d):
        cd = self.par.ALLOBJECT[self.obj].copy()
        cd['x1'] += d[0]
        cd['y1'] += d[1]
        cd['in_mass'] = True
        cd['temp'] = False
        cNew = self.create_object(cd)
        return cNew
        
    def copy_temp(self, d):
        cd = self.par.ALLOBJECT[self.obj].copy()
        cd.update(temp_dict)
        cd['x1'] += d[0]
        cd['y1'] += d[1]
        cNew = self.create_object(cd)
