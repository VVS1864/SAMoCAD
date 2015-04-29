# -*- coding: utf-8 -*-
from math import sqrt, degrees, radians, sin, cos, pi
import src.calc as calc

import src.sectors_alg as sectors_alg
from src.base import Base
from src.base_object import Base_object
import src.save_file as save_file

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

    def circle(self, event):
        self.par.ex, self.par.ey = super(Circle, self).func_2(
            self.circle2,
            'Circle - radius:',
            True,
            )

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
    xbox1 = x1 - R
    xbox2 = x1 + R
    ybox1 = y1 - R
    ybox2 = y1 + R  
    if not (0 <= xbox1 <= par.drawing_w
            and 0 <= ybox1 <= par.drawing_h
            and 0 <= xbox2 <= par.drawing_w
            and 0 <= ybox2 <= par.drawing_h):
        return False

    s = R/20.0
    lines = [[x1,y1-s,x1,y1+s], [x1-s,y1,x1+s,y1]]
    pointdata = [x1,y1-s,x1,y1+s, x1-s,y1,x1+s,y1]
    lines_c, pointdata_c = calc.circle_lines(x1, y1, R, 180)
    
    if not lines_c:
        return False
        
    lines.extend(lines_c)
    pointdata.extend(pointdata_c)
    if not temp:
        par.total_N += 1

        colordata = color*2*len(lines)
        
        par.gl_wrap.update_pointdata(pointdata, colordata, width)
        
        object_circle = Object_circle(par, par.total_N)
        dict_prop = {}
        for k,v in locals().iteritems():
            if k in list_prop:
                dict_prop[k] = v
                
        par.ALLOBJECT[par.total_N] = {
                                    'object':'circle',
                                    'class':object_circle,
                                    'sectors':[],
                                    'coords': lines,
                                    'lines': lines,
                                    'pointdata': pointdata,
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
    
class Object_circle(Base_object):
    def __init__(self, par, obj):
        super(Object_circle, self).__init__(par, obj)
        self.temp_dict = temp_dict


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


    ### Save method ###
    def save(self, file_format, layers, drawing_w, drawing_h):
        cd = self.par.ALLOBJECT[self.obj].copy()
        

        if file_format == 'svg':
            cd['y1'] = drawing_h - cd['y1']
            '''
            try:
                dash_str = ', '.join([str(x*cd['factor_stipple']) for x in cd['stipple']])
            except:
                dash_str = None
            '''
            color_rgb_str = 'rgb(' + ', '.join([str(x) for x in cd['color']]) + ')'

                                               
            # Перебрать свойства слоя объекта
            SVG_prop = {
                # cd_name : (SVG_name, cd_value)
                'color' : ('stroke', color_rgb_str),
                'width' : ('stroke-width', cd['width']),
                #'stipple' : ('stroke-dasharray', dash_str),
                #'factor_stipple' : ('stroke-dasharray', dash_str),
                        }
            
            en = save_file.prop_to_svg_style(layers, cd, SVG_prop)
                
            e = '''<circle class="st1" cx="%(x1)s" cy="%(y1)s" r="%(R)s"'''+en+"/>"
            e = (e % cd)
            cd['svg_strings'] = [e,]
            
        return cd

    ### Edit method ###
    def edit_object(self, x1, y1, x2, y2, cd ):
        a = sqrt((cd['x1'] - x1)**2 + (cd['y1'] - y1)**2)
        if abs(a - cd['R']) < self.par.min_e:
            cd['R'] = sqrt((x2-cd['x1'])**2 + (y2-cd['y1'])**2)
        elif a < self.par.min_e:
            cd['x1'], cd['y1'] = x2, y2
        cNew = self.create_object(cd)
        return cNew

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
        cd = self.par.ALLOBJECT[self.obj].copy()
        r = sqrt((cd['x1']-x3)**2 + (cd['y1']-y3)**2)
        if cd['R']<r:
            cd['R'] += pd
        else:
            cd['R'] -= pd
        cd['in_mass'] = False
        cd['temp'] = False
        cNew = self.create_object(cd)

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

    ### Scale method ###    
    def scale(self, x, y, scale_factor):
        cd = self.par.ALLOBJECT[self.obj].copy()
        cd['x1'] = (cd['x1']-x)*scale_factor + x
        cd['y1'] = (cd['y1']-y)*scale_factor + y
        cd['R'] = cd['R']*scale_factor
        
        cd['in_mass'] = True
        cd['temp'] = False
        cNew = self.create_object(cd)
        return cNew
