# -*- coding: utf-8; -*-
from math import sqrt, copysign
import src.sectors_alg as sectors_alg
from base import Base
from os import path
import wx
import copy
import calc #import mirrorCalc, mirror_lines, mirror_points, calc_angle, offset_line
#from object_object import Root_object 
#from get_conf import get_line_conf
#ЛИНИЯ
list_prop = ('color', 'width', 'layer', 'stipple', 'factor_stipple')
#dp = {'fill':0, 'width', 'layer':0, 'stipple':0, 'factor_stipple':0}
### Действия создания линии ###
class Line(Base):
    def __init__(self, par):
        super(Line, self).__init__(par)
        self.risLine()
        
    def risLine(self):
        self.par.kill()
        super(Line, self).func_1(Line, self.line, 'Line - point 1:', 'Enter - stop')

    def line(self, e):
        super(Line, self).func_2(self.line2, 'Line - next point:')

    def line2(self, event = None):
        kwargs = {
            'par' : self.par,
            'x1' : self.par.ex,
            'y1' : self.par.ey,
            'x2' : self.par.ex2,
            'y2' : self.par.ey2,        
            'width' : self.par.width,
            'layer' : self.par.layer,
            'color' : self.par.color,
            'stipple' : self.par.stipple,
            'factor_stipple' : self.par.factor_stipple,
            'in_mass' : False,
            'temp' : False,
            }
        super(Line, self).func_3(event, c_line, kwargs)
        
        """
            #self.par.history_undo.append(('c_', self.par.Nline))
            ex = self.par.ex2
            ey = self.par.ey2
            event.Skip()
            #self.par.set_coord()
            #self.par.changeFlag = True
            #self.par.enumerator_p()
            #self.par.com = None
            #self.par.command.delete(0, 'end')
        """
        if event:
            self.par.ex = self.par.ex2
            self.par.ey = self.par.ey2
        

### Отрисовка линии ###
def c_line(
            par,
            x1,
            y1,
            x2,
            y2,
            width,
            layer,
            color,
            stipple,
            factor_stipple,
            in_mass,
            temp = False,
           ):
    
    if stipple:
        dash = [x*factor_stipple for x in stipple]
    else:
        dash = None
        
    if not temp:
        par.total_N+=1
        
        if not stipple:
            lines = ((x1,y1,x2,y2),)
            par.pointdata.extend([x1,y1,x2,y2])
            par.colordata.extend(color * 2)
            par.IDs.append(par.total_N)
                        
        else:
            lines, pointdata, colordata, IDs = stipple_line(par, x1,y1,x2,y2, dash, color, width)
            if not lines:
                return
            else:
                par.pointdata.extend(pointdata)
                par.colordata.extend(colordata)
                par.IDs.extend(IDs)
       
        object_line = Object_line(par, par.total_N)
        dict_prop = {}
        for k,v in locals().iteritems():
            if k in list_prop:
                dict_prop[k] = v
        #dict_prop = {k:v for k,v in locals().iteritems() if k in list_prop}        
        par.ALLOBJECT[par.total_N] = {
                                    'object':'line',
                                    'class':object_line,
                                    'sectors':[],
                                    'coords': ([x1,y1,x2,y2],),
                                    'lines': lines,
                                    }
        par.ALLOBJECT[par.total_N].update(dict_prop)
        if not in_mass:
            par.ALLOBJECT, par.sectors = sectors_alg.quadric_mass(par.ALLOBJECT, [par.total_N,], par.sectors, par.q_scale)
            par.change_pointdata()
            par.c.Refresh()              #Обновить картинку
            par.c.Update()
        
    else:
        if stipple == None:
            par.dynamic_data.extend([x1,y1,x2,y2])
            par.dynamic_color.extend(color * 2)            
        else:
            lines, pointdata, colordata, IDs = stipple_line(par, x1,y1,x2,y2, dash, color, width)
            par.dynamic_data.extend(pointdata)
            par.dynamic_color.extend(colordata)
            
### Отрисовка линии сложного типа ###    
def stipple_line(par, x1,y1,x2,y2, dash, color, width):
    lines = []
    pointdata = []
    colordata = []
    IDs = []
    xm = min(x1, x2)
    ym = min(y1, y2)
    xb = max(x1, x2)
    yb = max(y1, y2)
    dx = x1 - x2
    dy = y1 - y2
    d_dx = x1
    d_dy = y1
    len_dash = len(dash)
    try:
        den_x = sqrt((dx*dx)/(dy*dy + dx*dx))
        den_y = sqrt((dy*dy)/(dy*dy + dx*dx))
    except ZeroDivisionError:
        return [], [], [], []
    i = 1
    j = 1
    if x1 < x2:
        i =- 1
    if y1 < y2:
        j =- 1
    pos = 0
    one = 0
    while 1:
        pos+=1
        if pos == len_dash + 1:
            pos = 1
        d = dash[pos-1]
        dx0 = d * den_x
        dy0 = d * den_y
        
        xi1 = d_dx
        yi1 = d_dy
        xi2 = xi1 - i * dx0
        yi2 = yi1 - j * dy0
        d_dx = xi2
        d_dy = yi2
        cor = False
        
        if xm > xi2:
            xi2 = xm
            cor = True
        elif xi2 > xb:
            xi2 = xb
            cor = True
        if ym > yi2:
            yi2 = ym
            cor = True
        elif yi2 > yb:
            yi2 = yb
            cor = True

        if pos % 2 != 0:
            lines.append([xi1,yi1,xi2,yi2])
            pointdata.extend([xi1,yi1,xi2,yi2])
            colordata.extend(color * 2)
            if one:
                IDs.append(0)
            else:
                IDs.append(par.total_N)
                one = 1
        if cor:
            return lines, pointdata, colordata, IDs            

class Object_line:
    def __init__(self, par, obj):
        self.par = par
        self.obj = obj

    def create_object(self, cd):
        c_line(self.par, cd['coord'][0], cd['coord'][1], cd['coord'][2], cd['coord'][3],
               cd['width'],
               cd['layer'],
               cd['color'],
               cd['stipple'],
               cd['factor_stipple'],
               temp = cd['temp'],
                   )
        
    ### History_undo method ###
    def undo(self, cd, zoomOLDres, xynachres):
        cd['coord'][0], cd['coord'][1] = self.par.coordinator(cd['coord'][0], cd['coord'][1], zoomOLDres = zoomOLDres, xynachres = xynachres)
        cd['coord'][2], cd['coord'][3] = self.par.coordinator(cd['coord'][2], cd['coord'][3], zoomOLDres = zoomOLDres, xynachres = xynachres)
        cd['temp'] = False
        self.create_object(cd)
        
    ### Save method ###
    def save(self, file_format, layers, drawing_w, drawing_h):
        cd = self.par.ALLOBJECT[self.obj].copy()
        cd['x1'] = cd['coords'][0][0]
        cd['y1'] = drawing_h - cd['coords'][0][1]
        cd['x2'] = cd['coords'][0][2] 
        cd['y2'] = drawing_h - cd['coords'][0][3]

        if file_format == 'svg':
            try:
                dash_str = ', '.join([str(x*cd['factor_stipple']) for x in cd['stipple']])
            except:
                dash_str = None
            color_rgb_str = 'rgb(' + ', '.join([str(x) for x in cd['color']]) + ')'

                                               
            # Перебрать свойства слоя объекта
            SVG_prop = {
                # cd_name : (SVG_name, cd_value)
                'color' : ('stroke', color_rgb_str),
                'width' : ('stroke-width', cd['width']),
                'stipple' : ('stroke-dasharray', dash_str),
                'factor_stipple' : ('stroke-dasharray', dash_str),
                        }
            layer_prop = layers[cd['layer']]
            SVG_style_list = []
            en = ' '
            for prop in SVG_prop.keys():
                if cd[prop] != layer_prop[prop] and cd[prop]:   
                    SVG_style_list.append("%s: %s;" %(SVG_prop[prop][0], SVG_prop[prop][1]))

            if SVG_style_list:
                SVG_style_list.insert(0, '''style="''')
                SVG_style_list.append('''"''')
                en += ''.join(SVG_style_list)
                
            e = '''<line class="st0" x1="%(x1)s" y1="%(y1)s" x2="%(x2)s" y2="%(y2)s"''' + en + "/>"
            e = (e % cd)
            cd['svg_strings'] = [e,]
            
        return cd
            
    ### Edit_prop method ###
    def edit_prop(self, params):
        param_changed = False
        r_list = None
        cd = self.get_conf()
        for param in params:
            if param in cd:
                param_changed = True
                cd[param] = params[param]
        if param_changed == True:
            cd['temp'] = False
            self.create_object(cd)
            r_list = (self.obj, self.par.Nline)
        return r_list
                   
    ### Trim method ###
    def trim_extend(self, x, y, trim_extend):
        cd = self.get_conf()
        if trim_extend == 'Trim':
            self.par.c.delete('C'+self.obj)
            cNew = calc.trim_line(self.par.ex, self.par.ey, self.par.ex2, self.par.ey2, x, y, cd['coord'])
        else:
            cNew = calc.extend_line(self.par.ex, self.par.ey, self.par.ex2, self.par.ey2, cd['coord'])
            
        if cNew:
            self.par.delete(elements = (self.obj,))
            cd['temp'] = False
            self.create_object(cd)
            
        return cNew
    
    ### Edit method ###
    def edit(self, event):
        cd = self.get_conf()
        xn, yn, xf, yf = calc.near_far_point(cd['coord'], self.par.ex, self.par.ey)
        cd['coord'][0] = xn
        cd['coord'][1] = yn
        cd['coord'][2] = xf
        cd['coord'][3] = yf
        cd['coord'][0] = self.par.ex2
        cd['coord'][1] = self.par.ey2
        self.par.ex3 = xf
        self.par.ey3 = yf
        if event:
            cd['temp'] = False
        else:
            cd['temp'] = True
        self.create_object(cd)
    
    ### Rotate methods ###    
    def rotateN(self, x0, y0, msin, mcos, angle):
        cd = self.get_conf()
        cd['coord'] = calc.rotate_lines(x0, y0, [cd['coord'],], msin = msin, mcos = mcos)[0]
        cd['temp'] = True
        self.create_object(cd)
       

    #def rotateY(self, x0, y0, msin, mcos, angle):
        #find = self.par.ALLOBJECT[self.obj]['id']
        #for i in find:
            #coord = self.par.c.coords(i)
            #coord = tuple(calc.rotate_lines(x0,y0, [coord,], msin = msin, mcos = mcos)[0])
            #self.par.c.coords(i, coord)

    def rotate_temp(self, x0, y0, msin, mcos, angle):
        coord = self.get_coord()
        coord = calc.rotate_lines(x0,y0, [coord,], msin = msin, mcos = mcos)[0]
        c_line(self.par, coord[0], coord[1], coord[2], coord[3],
               width = 1,
               layer = 't',
               color = 'yellow',
               stipple = None,
               factor_stipple = None,
               temp = True,
               )
    
    ### Offset method ###
    def offset(self, pd, x3, y3):
        c = self.get_coord()
        x1i, y1i, x2i, y2i = calc.offset_line(c[0],c[1],c[2],c[3],pd, x3, y3)
        c_line(self.par, x1i, y1i, x2i, y2i)
        
    ### Mirror methods ###   
    def mirror(self, x1, y1, sin, cos):
        cd = self.par.ALLOBJECT[self.obj]
        coord = list(cd['coords'][0])
        coord = calc.mirror_lines(x1,y1, [coord,], sin, cos)[0]
        c_line(self.par, coord[0], coord[1], coord[2], coord[3],
               width = cd['width'],
               layer = cd['layer'],
               color = cd['color'],
               stipple = cd['stipple'],
               factor_stipple = cd['factor_stipple'],
               in_mass = True,
               temp = False,
               )

    def mirror_temp(self, x1, y1, sin, cos):
        coord = list(self.par.ALLOBJECT[self.obj]['coords'][0])
        coord = calc.mirror_lines(x1,y1, [coord,], sin, cos)[0]
        c_line(self.par, coord[0], coord[1], coord[2], coord[3],
               width = 1,
               layer = 't',
               color = [255, 255, 0],
               stipple = None,
               factor_stipple = None,
               in_mass = True,
               temp = True,
               )
        
    ### Copy method ###    
    def copy(self, d):
        cd = self.par.ALLOBJECT[self.obj]#self.get_conf()
        x1 = cd['coords'][0][0] + d[0]
        y1 = cd['coords'][0][1] + d[1]
        x2 = cd['coords'][0][2] + d[0]
        y2 = cd['coords'][0][3] + d[1]
        #cd['coord'] = [y+d[0] if ind%2 == 0 else y+d[1] for ind, y in enumerate(cd['coord'])]
        c_line(self.par, x1, y1, x2, y2,
               width = cd['width'],
               layer = cd['layer'],
               color = cd['color'],
               stipple = cd['stipple'],
               factor_stipple = cd['factor_stipple'],
               in_mass = True,
               temp = False,
               )
        
        
    def copy_temp(self, d):
        coord = list(self.par.ALLOBJECT[self.obj]['coords'][0])#self.get_coord()
        x1 = coord[0] + d[0]
        y1 = coord[1] + d[1]
        x2 = coord[2] + d[0]
        y2 = coord[3] + d[1]
        #cd['coord'] = [y+d[0] if ind%2 == 0 else y+d[1] for ind, y in enumerate(cd['coord'])]
        c_line(self.par, x1, y1, x2, y2,
               width = 1,
               layer = 't',
               color = [255, 255, 0],
               stipple = None,
               factor_stipple = None,
               in_mass = True,
               temp = True,
               )
    ### Get configure ###
    #Принимает объект - линию, возвращает все его свойства
    def get_conf(self):
        cd = {}
        for i in self.par.ALLOBJECT[self.obj]:
            if i in list_prop:
                cd[i] = self.par.ALLOBJECT[self.obj][i]
        cd['class'] = self.par.ALLOBJECT[self.obj]['class']
        cd['object'] = self.par.ALLOBJECT[self.obj]['object'] #Потом нужно будет удалить!!!
        #for i in self.par.ALLOBJECT[self.obj]['id']:
            #if 'line' in self.par.ALLOBJECT[self.obj]['id'][i] and 'priv' in self.par.ALLOBJECT[self.obj]['id'][i]:
                #cd['coord'] = self.par.c.coords(i)
        #points = list(self.par.ALLOBJECT[self.obj]['points'])
        cd['coords'] = self.par.ALLOBJECT[self.obj]['coords']#self.par.coordinator_to_local(points)
        #cd['coord'] = [cd['coord'][0][0], cd['coord'][0][1], cd['coord'][1][0], cd['coord'][1][1]]
        return cd

    #Принимает объект - линия, возвращает координаты
    def get_coord(self):
        points = list(self.par.ALLOBJECT[self.obj]['points'])
        coord = self.par.coordinator_to_local(points)
        #for i in self.par.ALLOBJECT[self.obj]['id']:
            #if 'line' in self.par.ALLOBJECT[self.obj]['id'][i] and 'priv' in self.par.ALLOBJECT[self.obj]['id'][i]:
                #coord = self.par.c.coords(i)
        return coord
