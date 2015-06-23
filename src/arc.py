# -*- coding: utf-8; -*-
from math import pi, sqrt, degrees, radians, sin, cos, atan2
import src.calc as calc

import src.sectors_alg as sectors_alg
from src.base import Base
from src.base_object import Base_object
import src.save_file as save_file
#ДУГА
list_prop = (
    'color',
    'width',
    'layer',
    'start',
    'extent',
    #'stipple',
    #'factor_stipple',
    'R',
    'x1',
    'y1',
    'x3',
    'y3',
    'x2',
    'y2',
    )
temp_dict = {
    'width' : 1,
    'layer' : 't',
    'color' : [255, 255, 0],
    #'stipple' : None,
    #'factor_stipple' : None,
    'in_mass' : False,
    'temp' : True,
    }
#События
class Arc(Base):
    def __init__(self, par):
        super(Arc, self).__init__(par)
        self.risArc()
        
    def risArc(self):
        self.par.kill()
        super(Arc, self).func_1(Arc, self.arc, 'Arc - center point:', 'Enter - stop')
        
    def arc(self, event):
        self.par.ex, self.par.ey = super(Arc, self).func_2(
            self.arc2,
            'Arc - point 1:',
            True,
            )

    def arc2(self, event = None):
        if event:
            self.par.ex3, self.par.ey3 = super(Arc, self).func_2(
                self.arc3,
                'Arc - point 2:',
                True,
                )
        else:
            if self.par.trace_flag or self.par.trace_obj_flag:
                if self.par.trace_flag:
                    self.par.trace_on = True
                #if self.par.tracing_obj_Flag:
                    #self.par.trace_obj_on = True
                    
                self.par.trace_x1, self.par.trace_y1 = self.par.ex, self.par.ey
       

    def arc3(self, event = None):
        kwargs = {
            'par' : self.par,
            'x1' : self.par.ex,
            'y1' : self.par.ey,
            'x2' : self.par.ex2,
            'y2' : self.par.ey2,
            'x3' : self.par.ex3,
            'y3' : self.par.ey3,
            'width' : self.par.width,
            'layer' : self.par.layer,
            'color' : self.par.color,
            'R' : None,
            'start' : None,
            'extent' : None,
            'in_mass' : False,
            'temp' : False,
            }
        super(Arc, self).func_3(event, c_arc, kwargs)

        if event:
            super(Arc, self).add_history(objects = [self.par.total_N,], mode = 'create')
            self.risArc()
            

#Отрисовка
def c_arc(
    par,
    x1,
    y1,
    x2,
    y2,
    x3,
    y3,
    width,
    layer,
    color,
    R,
    start,
    extent,
    in_mass,
    temp = False,
    ):
    if not R:
        R = sqrt((x3-x1)*(x3-x1) + (y3-y1)*(y3-y1))
    xbox1 = x1 - R
    xbox2 = x1 + R
    ybox1 = y1 - R
    ybox2 = y1 + R

    if not (0 <= xbox1 <= par.drawing_w
            and 0 <= ybox1 <= par.drawing_h
            and 0 <= xbox2 <= par.drawing_w
            and 0 <= ybox2 <= par.drawing_h):
        
        return False

    if start == None:
        a = x3 - x1
        b = y3 - y1
        c = xbox2 - x1
        d = 0
        atanA = atan2(a, b)
        atanB = atan2(c, d)
        aa = (-degrees(atanA - atanB))%360

        a = x2 - x1
        b = y2 - y1
        c = x3 - x1
        d = y3 - y1
        atanA = atan2(a, b)
        atanB = atan2(c, d)
        bb = (-degrees(atanA - atanB))%360       
        
        start = aa
        extent = aa + bb
        xstart, ystart = calc.intersection_stright_circle(x1, y1, R, x1, y1, x3, y3, x3, y3)
        xend, yend = calc.intersection_stright_circle(x1, y1, R, x1, y1, x2, y2, x2, y2)
    else:
        r_start = radians(start)
        r_extent = radians(extent)
        mcos = cos(r_start)
        mcos2 = cos(r_extent)
        msin = sin(r_start)
        msin2 = sin(r_extent)
        xend = x1+R*mcos2
        yend = y1+R*msin2
        xstart = x1+R*mcos
        ystart = y1+R*msin
        
    s = R/20.0
    lines = [[x1,y1-s,x1,y1+s], [x1-s,y1,x1+s,y1]]
    pointdata = [x1,y1-s,x1,y1+s, x1-s,y1,x1+s,y1]
    lines_c, pointdata_c = calc.oval_lines(x1, y1, R, (start, extent), 180, xstart, ystart)

    if not lines_c:
        return False
    
    lines.extend(lines_c)
    pointdata.extend(pointdata_c)
    
    if not temp:
        par.total_N += 1

        colordata = color*2*len(lines)

        par.gl_wrap.update_pointdata(pointdata, colordata, width)
            
        object_arc = Object_arc(par, par.total_N)
        dict_prop = {}
        for k,v in locals().iteritems():
            if k in list_prop:
                dict_prop[k] = v
       
        par.ALLOBJECT[par.total_N] = {
                                    'object':'arc',
                                    'class':object_arc,
                                    'sectors':[],
                                    'coords': lines,
                                    'lines': lines,
                                    'pointdata': pointdata,
                                    'x1': x1,
                                    'y1': y1,
                                    'x3': xstart,
                                    'y3': ystart,
                                    'x2': xend,
                                    'y2': yend,
                                    'snap_type':'arc',
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
    
class Object_arc(Base_object):
    def __init__(self, par, obj):
        super(Object_arc, self).__init__(par, obj)
        self.temp_dict = temp_dict

    def create_object(self, cd):
        if cd['x2'] != None:
            cd['start'] = None
        cNew = c_arc(
            self.par,
            cd['x1'],
            cd['y1'],
            cd['x2'],
            cd['y2'],
            cd['x3'],
            cd['y3'],
            R = cd['R'],
            width = cd['width'],
            layer = cd['layer'],
            color = cd['color'],
            start = cd['start'],
            extent = cd['extent'],
            in_mass = cd['in_mass'],
            temp = cd['temp'],
            )
            
        return cNew

    ### History_undo method ###
    def undo(self, cd, zoomOLDres, xynachres):
        cd['xc'], cd['yc'] = self.par.coordinator(cd['xc'], cd['yc'], zoomOLDres = zoomOLDres, xynachres = xynachres)
        cd['dx1'], cd['dy1'] = self.par.coordinator(cd['dx1'], cd['dy1'], zoomOLDres = zoomOLDres, xynachres = xynachres)
        cd['dx2'], cd['dy2'] = self.par.coordinator(cd['dx2'], cd['dy2'], zoomOLDres = zoomOLDres, xynachres = xynachres)
        c_arc(self.par, cd['xc'], cd['yc'], cd['dx1'], cd['dy1'], cd['dx2'], cd['dy2'],
               cd['width'],
               cd['sloy'],
               cd['fill']
               )


    ### Save method ###
    def save(self, file_format, layers, drawing_w, drawing_h):
        cd = self.par.ALLOBJECT[self.obj].copy()
        cd['y2'] = drawing_h - cd['y2']
        cd['y3'] = drawing_h - cd['y3']
        

        if file_format == 'svg':
            cd['sf'] = 0
                
            if abs(cd['extent'] - cd['start']) < 180:
                cd['lf'] = 0
            else:
                cd['lf'] = 1
            
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
                
            e = '''<path class="st1" d="M%(x3)s,%(y3)s A%(R)s,%(R)s 0 %(lf)s %(sf)s %(x2)s,%(y2)s"'''+en+'/>'
            e = (e % cd)
            cd['svg_strings'] = [e,]
            
        return cd

    ### Edit method ###
    def edit_object(self, x1, y1, x2, y2, cd ):
        a = sqrt((cd['x2'] - x1)**2 + (cd['y2'] - y1)**2)
        b = sqrt((cd['x3'] - x1)**2 + (cd['y3'] - y1)**2)
        c = sqrt((cd['x1'] - x1)**2 + (cd['y1'] - y1)**2)
        
        if b < self.par.min_e:
            cd['x3'], cd['y3'] = x2, y2
        
        elif a < self.par.min_e:
            cd['x2'], cd['y2'] = x2, y2

        elif c < self.par.min_e:
            cd['x1'], cd['y1'] = x2, y2
            cd['x2'], cd['y2'], cd['x2'], cd['y2'] = None, None, None, None
        else:
            return False
        cNew = self.create_object(cd)
        return cNew

    ### Rotate methods ###
    def rotate(self, x0, y0, msin, mcos, angle):
        cd = self.par.ALLOBJECT[self.obj].copy()
        [[cd['x1'], cd['y1']],
         [cd['x2'], cd['y2']],
         [cd['x3'], cd['y3']]] = calc.rotate_points(x0, y0, [[cd['x1'], cd['y1']],
                                                             [cd['x2'], cd['y2']],
                                                             [cd['x3'], cd['y3']]], msin, mcos)
        
        cd['in_mass'] = True
        cd['temp'] = False
        cNew = self.create_object(cd)
        return cNew

    def rotate_temp(self, x0, y0, msin, mcos, angle):
        cd = self.par.ALLOBJECT[self.obj].copy()
        [[cd['x1'], cd['y1']],
         [cd['x2'], cd['y2']],
         [cd['x3'], cd['y3']]] = calc.rotate_points(x0, y0, [[cd['x1'], cd['y1']],
                                                             [cd['x2'], cd['y2']],
                                                             [cd['x3'], cd['y3']]], msin, mcos)
        
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
        cd['x2'], cd['y2'], cd['x2'], cd['y2'] = None, None, None, None
        cd['in_mass'] = False
        cd['temp'] = False
        cNew = self.create_object(cd)

    ### Mirror methods ###
    def mirror(self, x1, y1, msin, mcos):
        cd = self.par.ALLOBJECT[self.obj].copy()
        [[cd['x1'], cd['y1']],
         [cd['x3'], cd['y3']],
         [cd['x2'], cd['y2']]] = calc.mirror_points(x1, y1, [[cd['x1'], cd['y1']],
                                                             [cd['x2'], cd['y2']],
                                                             [cd['x3'], cd['y3']]], msin, mcos)
        cd['in_mass'] = True
        cd['temp'] = False
        cNew = self.create_object(cd)
        return cNew

    def mirror_temp(self, x1, y1, msin, mcos):
        cd = self.par.ALLOBJECT[self.obj].copy()
        [[cd['x1'], cd['y1']],
         [cd['x3'], cd['y3']],
         [cd['x2'], cd['y2']]] = calc.mirror_points(x1, y1, [[cd['x1'], cd['y1']],
                                                             [cd['x2'], cd['y2']],
                                                             [cd['x3'], cd['y3']]], msin, mcos)
        cd.update(temp_dict)
        self.create_object(cd)

    ### Copy method ###
    def copy(self, d):
        cd = self.par.ALLOBJECT[self.obj].copy()
        cd['x1'] += d[0]
        cd['y1'] += d[1]
        cd['x2'] = None
        
        cd['in_mass'] = True
        cd['temp'] = False
        cNew = self.create_object(cd)
        return cNew
        
    def copy_temp(self, d):
        cd = self.par.ALLOBJECT[self.obj].copy()
        cd.update(temp_dict)
        cd['x1'] += d[0]
        cd['y1'] += d[1]
        cd['x2'] = None
        cd['y2'] = None
        cd['x3'] = None
        cd['y3'] = None
        cNew = self.create_object(cd)

    ### Scale method ###    
    def scale(self, x, y, scale_factor):
        cd = self.par.ALLOBJECT[self.obj].copy()
        cd['x1'] = (cd['x1']-x)*scale_factor + x
        cd['y1'] = (cd['y1']-y)*scale_factor + y
        cd['R'] = cd['R']*scale_factor
        cd['x2'] = None
        
        cd['in_mass'] = True
        cd['temp'] = False
        cNew = self.create_object(cd)
        return cNew
