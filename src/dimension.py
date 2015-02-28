# -*- coding: utf-8; -*-
from math import pi, sqrt, degrees, radians, sin, cos

import src.calc as calc
import src.sectors_alg as sectors_alg
from src.base import Base
import src.save_file as save_file

import symbols
import copy

from collections import OrderedDict


#РАЗМЕР
list_prop = (
    'x1',
    'y1',
    'x2',
    'y2',
    'x3',
    'y3',
    'color',
    'text',
    'layer',
    'angle',
    'anchor',
    'dim_text_size',
    'dim_text_s_s',
    'dim_text_w',
    'dim_text_font',
    'ort',
    'text_change',
    'text_place',
    's',
    'vr_s',
    'vv_s',
    'arrow_s',
    'type_arrow',
    )

temp_dict = {
    'text' : None,
    'layer' : 't',
    'color' : [255, 255, 0],
    'in_mass' : False,
    'temp' : True,
    }

class Dimension(Base):
    def __init__(self, par):
        super(Dimension, self).__init__(par)
        #self.par = par
        self.risDim()
        
    def risDim(self):
        self.par.kill()
        super(Dimension, self).func_1(Dimension, self.dim, 'Dimension - point 1:', 'Enter - stop')

    def dim(self, event):
        self.par.ex, self.par.ey = super(Dimension, self).func_2(
            self.dim2,
            'Dimension - point 2:',
            False,
            )

    def dim2(self, event):
        self.par.ex2, self.par.ey2 = super(Dimension, self).func_2(
            self.dim3,
            'Dimension - dim line:',
            True,
            )
        
    def dim3(self, event = None):
        kwargs = {
        'par' : self.par,
        'x1' : self.par.ex,
        'y1' : self.par.ey,
        'x2' : self.par.ex2,
        'y2' : self.par.ey2,
        'x3' : self.par.ex3,
        'y3' : self.par.ey3,
        'text' : None,
        'layer' : self.par.layer,
        'color' : self.par.color,
        'ort' : None,
        'text_change' : 1,
        'text_place' : None,
        's' : self.par.s,
        'vv_s' : self.par.vv_s,
        'vr_s' : self.par.vr_s,
        'arrow_s' : self.par.arrow_s,
        'type_arrow' : self.par.type_arrow,
        'dim_text_size' : self.par.dim_text_size,
        'dim_text_s_s' : self.par.dim_text_s_s,
        'dim_text_w' : self.par.dim_text_w,
        'dim_text_font' : self.par.dim_text_font,
        'in_mass' : False,
        'temp' : False,
        }
        
        self.par.ex3 = self.par.x_priv
        self.par.ey3 = self.par.y_priv
        data = self.par.from_cmd(float)
        if data:
            kwargs['ort'], derect = calc.get_dim_direction(
                self.par.ex,
                self.par.ey,
                self.par.ex2,
                self.par.ey2,
                self.par.ex3,
                self.par.ey3,
                )
            if kwargs['ort'] == "vertical":  
                self.par.ey3 = self.par.ey2 + data * derect
            else:
                self.par.ex3 = self.par.ex2 + data * derect
            '''
            x = max(self.par.ex, self.par.ex2)
            xm = min(self.par.ex, self.par.ex2)
            y = max(self.par.ey, self.par.ey2)
            ym = min(self.par.ey, self.par.ey2)
            xe_max = max(self.par.ex3, x)
            xe_min = min(self.par.ex3, x)
            ye_max = max(self.par.ey3, y)
            ye_min = min(self.par.ey3, y)
            if xe_max - xe_min > ye_max - ye_min:
                kwargs['ort'] = "horizontal"
            else:
                kwargs['ort'] = "vertical"
            if ym <= self.par.ey3 <= y:
                kwargs['ort'] = "horizontal"
            if xm <= self.par.ex3 <= x:
                kwargs['ort'] = "vertical"
            if kwargs['ort'] == "vertical":
                if self.par.ey3 < self.par.ey2:
                    data = -data  
                self.par.ey3 = self.par.ey2 + data
            else:
                if self.par.ex3 < self.par.ex2:
                    data = -data  
                self.par.ex3 = self.par.ex2 + data
            '''
                
            '''
            if self.par.ex3 > self.par.ex2 and self.par.ex3 > self.par.ex:
                self.par.ex3 = self.par.ex2 + data
            else:
                self.par.ex3 = self.par.ex2 - data
                
            if self.par.ey3 > self.par.ey2 and self.par.ey3 > self.par.ey:
                self.par.ey3 = self.par.ey2 + data
            else:
                self.par.ey3 = self.par.ey2 - data
            '''
            '''
            self.par.ex3, self.par.ey3 = calc.cmd_coorder(
                self.par.ex2,
                self.par.ey2,
                self.par.ex3,
                self.par.ey3,
                data,
                self.par.ortoFlag,
                )
            '''
        '''
        if event:
            c_dim(
                self.par,
                self.par.ex,
                self.par.ey,
                self.par.ex2,
                self.par.ey2,
                self.par.ex3,
                self.par.ey3)
        '''

        
        #self.par.ex3 = self.par.priv_coord[0]
        #self.par.ey3 = self.par.priv_coord[1]
        '''
        self.par.comOrKill()
        if self.par.com:
            self.par.com = self.par.coordinator2(self.par.com)
            if self.par.ex3>self.par.ex2 and self.par.ex3>self.par.ex:
                self.par.ex3=self.par.ex2+self.par.com
            else:
                self.par.ex3=self.par.ex2-self.par.com
            if self.par.ey3>self.par.ey2 and self.par.ey3>self.par.ey:
                self.par.ey3=self.par.ey2+self.par.com
            else:
                self.par.ey3=self.par.ey2-self.par.com
        '''
        
        if event:
            '''
            self.par.history_undo.append(('c_', self.par.Ndim))
            self.par.changeFlag = True
            self.par.enumerator_p()
            '''
            c_dim(**kwargs)
            self.risDim()
        else:
            kwargs['temp'] = True
            
            c_dim(**kwargs)
            

def c_dim(
    par,
    x1,
    y1,
    x2,
    y2,
    x3,
    y3,
    text,
    layer,
    color,
    ort,
    text_change,
    text_place,
    s,
    vv_s,
    vr_s,
    arrow_s,
    type_arrow,
    dim_text_size,
    dim_text_s_s,
    dim_text_w,
    dim_text_font,
    in_mass,
    temp,
    #ID = None
    ):
    if not (0 <= x1 <= par.drawing_w and
            0 <= y1 <= par.drawing_h and
            0 <= x2 <= par.drawing_w and
            0 <= y2 <= par.drawing_h and
            0 <= x3 <= par.drawing_w and
            0 <= y3 <= par.drawing_h):
        return False
    #kwargs = locals().iteritems()
    kwargs = {k:v for k,v in locals().iteritems()}
    pointdata = []
    colordata = []
    IDs = []
    snap_lines, lines, list_arrow, ort, text_place, text_change, line3 = get_dim_lines(**kwargs)
    if not (0 <= snap_lines[3][0] <= par.drawing_w and
            0 <= snap_lines[3][1] <= par.drawing_h and
            0 <= snap_lines[3][2] <= par.drawing_w and
            0 <= snap_lines[3][3] <= par.drawing_h):
        return False
    
    if not temp:
        par.total_N+=1                
        one = 0
        for i in lines:
            pointdata.extend(i)
            colordata.extend(color * 2)
            if one:
                IDs.append(0)
            else:
                IDs.append(par.total_N)
                one = 1
        par.pointdata.extend(pointdata)
        par.colordata.extend(colordata)
        par.IDs.extend(IDs)
        object_dim = Object_dim(par, par.total_N)
        #Записать в ALLOBJECT параметры размера
        dict_prop = {}
        for k,v in locals().iteritems():
            if k in list_prop:
                dict_prop[k] = v
        par.ALLOBJECT[par.total_N] = {
                                'object':'dim',
                                'class':object_dim,
                                'sectors': [],
                                'coords': snap_lines,
                                'lines': lines,
                                'arrow_lines' : list_arrow,
                                'line3' : line3,
                                }
        par.ALLOBJECT[par.total_N].update(dict_prop)
        
        if not in_mass:
            par.ALLOBJECT, par.sectors = sectors_alg.quadric_mass(par.ALLOBJECT, [par.total_N,], par.sectors, par.q_scale)
            par.change_pointdata()
            par.c.Refresh()              #Обновить картинку
            par.c.Update()

        return True

    else:
        #snap_lines, lines, ort = get_dim_lines(**kwargs)
        for i in lines:
            par.dynamic_data.extend(i)
            par.dynamic_color.extend(color * 2)

    
         
        
def get_dim_lines(
    par,
    x1,
    y1,
    x2,
    y2,
    x3,
    y3,
    text,
    layer,
    color,
    ort,
    text_change,
    text_place,
    s,
    vv_s,
    vr_s,
    arrow_s,
    type_arrow,
    dim_text_size,
    dim_text_s_s,
    dim_text_w,
    dim_text_font,
    in_mass,
    temp,
    ):
    

    list_arrow = []
    list_lines = []
    list_text_lines = []
    list_snap_lines = []

        
    x = max(x1, x2)
    xm = min(x1, x2)
    y = max(y1, y2)
    ym = min(y1, y2)
    
    if ort == None:
        xe_max = max(x3, x)
        xe_min = min(x3, x)
        ye_max = max(y3, y)
        ye_min = min(y3, y)
        if xe_max - xe_min > ye_max - ye_min:
            ort = "horizontal"
        else:
            ort = "vertical"
        if ym <= y3 <= y:
            ort = "horizontal"
        elif xm <= x3 <= x:
            ort = "vertical"
    #elif ort == 'rotated':
        #pass
    
            
    if ort == "horizontal":
        if text_place == None:
            text_place = [0, 0]
                    
        angle = radians(90)
        msin = sin(angle)
        mcos = cos(angle)
        if y1 < y2:
            xm = x1
            ym = y1
            x = x2
            y = y2
            
        else:
            xm = x2
            ym = y2
            x = x1
            y = y1
        [ [x,y], [x3,y3], [ text_place[0], text_place[1] ] ]  = calc.rotate_points(xm, ym, [[x,y], [x3,y3], [text_place[0], text_place[1]]], msin, mcos)
        #text_place[0], text_place[1] = a, b        

    else:
        

        if x1 < x2:
            xm = x1
            ym = y1
            x = x2
            y = y2
            
        else:
            xm = x2
            ym = y2
            x = x1
            y = y1

    dx = abs(xm - x)
    ddx = format(dx, '.0f')

    if text:
        textt = text
    else:
        textt = ddx


    #Выносные линии
    zvv_s = 1
    if y3 < y:
        zvv_s = -1


    list_lines.extend([[xm, ym, xm, y3+vv_s*zvv_s], [x, y, x, y3+vv_s*zvv_s]])

    #Размерная линия + текст(если задан, если нет - вкличина размера)
    # text_change :
    # 1 = 'unchange' - auto
    # 2 = 'online3'
    # 3 = 'online3_m_l'
   
    if text_change == 1:
        text_place = [xm+dx/2.0, y3+s] 
    elif text_change == 2  or text_change == 3:
        text_place[1] = y3+s
        
    
    if in_mass and temp:
        temp = True
    else:
        temp = False
    
        
    list_text_lines = symbols.font(text_place[0], text_place[1], textt, dim_text_size, dim_text_s_s, dim_text_w, 'sc', dim_text_font, 0, temp)


    i = 1
    if text_change == 2:
        e2 = list_text_lines.nabor[0][0]
        e3 = list_text_lines.nabor[0][2]
        if x < e3:
            line3 = [xm-vr_s, y3, e3, y3]
        else:
            line3 = [e2, y3, x+vr_s, y3]
    elif text_change == 1:
        line3 = [xm-vr_s, y3, x+vr_s, y3]
        
        #Если текст не вмещается между выносными линиями - нарисовать сбоку
        if list_text_lines.Ltext > dx - arrow_s:

            list_text_lines.nabor = calc.move_lines(text_place[0], text_place[1], xm-arrow_s-list_text_lines.Ltext/2.0, y3+s, list_text_lines.nabor)
            e = list_text_lines.nabor[0][0]
            line3 = [x+vr_s, y3, e, y3]
            i = -1
            #text_change = 2
            text_place = [xm-arrow_s - list_text_lines.Ltext / 2.0, y3 + s]
    '''
    if text_change == 1:

        e = list_text_lines.Ltext
        #Если текст не вмещается между выносными линиями - нарисовать сбоку
        if e>dx-arrow_s:

            list_text_lines.nabor = calc.move_lines(text_place[0], text_place[1], xm-arrow_s-list_text_lines.Ltext/2.0, y3+s, list_text_lines.nabor)
            e = list_text_lines.nabor[0][0]
            line3 = [x+vr_s, y3, e, y3]
            i = -1
            #text_change = 2
            text_place = [xm-arrow_s - list_text_lines.Ltext / 2.0, y3 + s]
        '''
    list_lines.append(line3)       
    #Засечки
    if type_arrow == 'Arch':
        L1 = [x - arrow_s, y3 + arrow_s, x + arrow_s, y3 - arrow_s]
        L2 = [xm - arrow_s, y3 + arrow_s, xm + arrow_s, y3 - arrow_s]
        list_arrow.extend([L1, L2])
    elif type_arrow == 'Arrow':
        if dx < arrow_s*3.0:
            i = -1
        L1 = [xm, y3, xm + arrow_s*i, y3 - arrow_s/10.0]
        L2 = [xm, y3, xm + arrow_s*i, y3 + arrow_s/10.0]
        L3 = [x, y3, x - arrow_s*i, y3 - arrow_s/10.0]
        L4 = [x, y3, x - arrow_s*i, y3 + arrow_s/10.0]
        list_arrow.extend([L1, L2, L3, L4])

    snap_text = list_text_lines.nabor[0]
    list_snap_lines = [[xm, ym, xm, y3],
                       [x, y, x, y3],
                       [xm, y3, x, y3],
                       snap_text]
    del list_text_lines.nabor[0]
    list_lines.extend(list_text_lines.nabor)
    

    if ort == 'horizontal':
        msin = -msin  
        list_arrow = calc.rotate_lines(xm, ym, list_arrow, msin, mcos)
        list_lines = calc.rotate_lines(xm, ym, list_lines, msin, mcos)
        list_snap_lines = calc.rotate_lines(xm, ym, list_snap_lines, msin, mcos)
        #[line3,] = calc.rotate_lines(xm, ym, [line3,], msin, mcos)
        (text_place,) = calc.rotate_points(xm, ym, [text_place,], msin, mcos)
    list_lines.extend(list_arrow)
    
    
    
    return list_snap_lines, list_lines, list_arrow, ort, text_place, text_change, line3
        

class Object_dim:
    def __init__(self, par, obj):
        self.par = par
        self.obj = obj
    
    def create_object(self, cd):
        cNew =  c_dim(
            self.par,
            cd['x1'],
            cd['y1'],
            cd['x2'],
            cd['y2'],
            cd['x3'],
            cd['y3'],
            text = cd['text'],
            layer = cd['layer'],
            color = cd['color'],
            dim_text_size = cd['dim_text_size'],
            ort = cd['ort'],
            text_change = cd['text_change'],
            text_place = cd['text_place'],
            s = cd['s'],
            vv_s = cd['vv_s'],
            vr_s = cd['vr_s'],
            arrow_s = cd['arrow_s'],
            type_arrow = cd['type_arrow'],
            dim_text_s_s = cd['dim_text_s_s'],
            dim_text_w = cd['dim_text_w'],
            dim_text_font = cd['dim_text_font'],
            in_mass = cd['in_mass'],
            temp = cd['temp'],
            )
        return cNew

    ### History_undo method ###
    def undo(self, cd, zoomOLDres, xynachres):
        cd['x1'], cd['y1'] = self.par.coordinator(cd['x1'], cd['y1'], zoomOLDres = zoomOLDres, xynachres = xynachres)
        cd['x2'], cd['y2'] = self.par.coordinator(cd['x2'], cd['y2'], zoomOLDres = zoomOLDres, xynachres = xynachres)
        cd['x3'], cd['y3'] = self.par.coordinator(cd['x3'], cd['y3'], zoomOLDres = zoomOLDres, xynachres = xynachres)
        cd['temp'] = None
        self.create_object(cd)
               

    ### Edit_prop method ###
    def save(self, file_format, layers, drawing_w, drawing_h):
        cd = self.par.ALLOBJECT[self.obj].copy()
        if cd['text'] == None:
            if cd['ort'] == "horizontal":
                cd['dim_distanse'] = int(format(abs(cd['y1'] - cd['y2']), '.0f'))                            
            else:
                cd['dim_distanse'] = int(format(abs(cd['x1'] - cd['x2']), '.0f'))
        else:
            cd['dim_distanse'] = cd['text']
        ort, derect = calc.get_dim_direction(
            cd['x1'],
            cd['y1'],
            cd['x2'],
            cd['y2'],
            cd['x3'],
            cd['y3'],
            )
        cd['ist_y1'] = cd['y1']
        cd['ist_y2'] = cd['y2']
        cd['ist_y3'] = cd['y3']
        
        cd['y1'] = drawing_h - cd['y1']
        cd['y2'] = drawing_h - cd['y2']
        cd['y3'] = drawing_h - cd['y3']

        '''
        lines_coord = {}        
        for ind, i in enumerate(cd['coords']):
            lines_coord.update({
                'line_'+str(ind)+'_x1': i[0],
                'line_'+str(ind)+'_y1': drawing_h - i[1],
                'line_'+str(ind)+'_x2': i[2],
                'line_'+str(ind)+'_y2': drawing_h - i[3]
                })
            
        for ind, i in enumerate(cd['arrow_lines']):
            lines_coord.update({
                'arrow_'+str(ind)+'_x1': coord[0],
                'arrow_'+str(ind)+'_y1': drawing_h - coord[1],
                'arrow_'+str(ind)+'_x2': coord[2],
                'arrow_'+str(ind)+'_y2': drawing_h - coord[3]
                })

        x1 = cd['snap_lines'][3][0]
        y1 = cd['snap_lines'][3][1]
        x2 = cd['snap_lines'][3][2]
        y2 = cd['snap_lines'][3][3]
        # Длинна текста
        lines_coord['Ltext'] = sqrt((x1-x2)**2+(y1-y2)**2)
        if file_format == 'dxf':
            # Если DXF - берется центральная точка текста
            #!!!
            if config['ort'] == "horizontal":
                y = (y1+y2)/2.0
                yy = y
                x = cd['x3']#coord_list[2][0]
                xx = x1 - config['size']/2.0
            else:
                x = (x1+x2)/2.0
                xx = x
                y = cd['y3']#coord_list[2][1]
                yy = y1 - config['size']/2.0
            #!!!
        else:
            # Иначе - нижняя  левая
            x = x1
            xx = x2
            y = y1
            yy = y2
            
        lines_coord.update({
            'text_x': x,
            'text_y': yf*y,
            'text_xx': xx,
            'text_yy': yf*yy
            })
        cd.update(lines_coord)

        if cd['ort'] == "horizontal":
            cd.update({
                'arrow_point1_x': cd['x3'],
                'arrow_point1_y': cd['y1'],
                'arrow_point2_x': cd['x3'],
                'arrow_point2_y': cd['y2']
                })
            cd.update({
                'angle': 90.0,
                'angle_arrow1': 90.0,
                'angle_arrow2': 270.0
                })
            
            if cd['type_arrow'] == 'Arrow':
                cd.update({
                    'arrow_5_x': cd['x3'],
                    'arrow_5_y': lines_coord['arrow_1_y1'],
                    'arrow_6_x': cd['x3'],
                    'arrow_6_y': lines_coord['arrow_3_y1']
                    })
        else:
            cd.update({
                'arrow_point1_x': cd['x1'],
                'arrow_point1_y': cd['y3'],
                'arrow_point2_x': cd['x2'],
                'arrow_point2_y': cd['y3'],
                'angle': 0.0,
                'angle_arrow1': 180.0,
                'angle_arrow2': 0.0
                })
            
            if cd['type_arrow'] == 'Arrow':
                cd.update({
                    'arrow_5_y': cd['y3'],   
                    'arrow_5_x': lines_coord['arrow_1_x1'],
                    'arrow_6_y': cd['y3'],
                    'arrow_6_x': lines_coord['arrow_3_x1']
                    })
        '''
        cd = save_file.get_object_lines(cd, drawing_h, file_format)
        
        if ort == "vertical":
            cd['line_2_y2'] -= cd['vv_s']*derect
            cd['line_1_y2'] -= cd['vv_s']*derect
            
            #cd['line_3_x1'] -= cd['vr_s']
            #cd['line_3_x2'] += cd['vr_s']
        else:
            cd['line_2_x2'] += cd['vv_s']*derect
            cd['line_1_x2'] += cd['vv_s']*derect
            
            #cd['line_3_y1'] += cd['vr_s']
            #cd['line_3_y2'] -= cd['vr_s']
        
        cd['line_3_x1'] = cd['line3'][0]
        cd['line_3_y1'] = drawing_h - cd['line3'][1]
        cd['line_3_x2'] = cd['line3'][2]
        cd['line_3_y2'] = drawing_h - cd['line3'][3]
        cd['angle'] = -cd['angle']
        if not cd['text']:
            text = str(cd['dim_distanse'])
        else:
            text = cd['text']
        cd['svg_text'] = text.encode("utf-8")
        cd['dim_text_size'] = str(cd['dim_text_size'])

        en = ' '
        en_text = ' '
        if cd['angle']:
            en_text += '''transform="rotate(%(angle)s, %(text_x)s %(text_y)s)" '''

        if file_format == 'svg':
            color_rgb_str = 'rgb(' + ', '.join([str(x) for x in cd['color']]) + ')'
            # Перебрать свойства слоя объекта
            SVG_prop = {
                # cd_name : (SVG_name, cd_value)
                'color' : ('stroke', color_rgb_str),
                        }
            SVG_prop_text = {
                # cd_name : (SVG_name, cd_value)
                'color' : ('fill', color_rgb_str),
                        }
            en += save_file.prop_to_svg_style(layers, cd, SVG_prop)
            en_text += save_file.prop_to_svg_style(layers, cd, SVG_prop_text)
        
            e0 = '''<g class="DimL">'''
            e_desc = '''<desc>x1 = "%(x1)s", y1 = "%(ist_y1)s", x2 = "%(x2)s", y2 = "%(ist_y2)s", x3 = "%(x3)s", y3 = "%(ist_y3)s", text = "%(text)s", color = "%(color)s", ort = "%(ort)s", dim_text_size = "%(dim_text_size)s", text_change = "%(text_change)s", text_place = "%(text_place)s", layer = "%(layer)s", s = "%(s)s", vr_s = "%(vr_s)s", vv_s = "%(vv_s)s", arrow_s = "%(arrow_s)s", type_arrow = "%(type_arrow)s", dim_text_s_s = "%(dim_text_s_s)s", dim_text_w = "%(dim_text_w)s", dim_text_font = "%(dim_text_font)s"</desc>'''
            e1 = '''<line class="st1" x1="%(line_1_x1)s" y1="%(line_1_y1)s" x2="%(line_1_x2)s" y2="%(line_1_y2)s"'''+en+"/>"
            e2 = '''<line class="st1" x1="%(line_2_x1)s" y1="%(line_2_y1)s" x2="%(line_2_x2)s" y2="%(line_2_y2)s"'''+en+"/>"
            e3 = '''<line class="st1" x1="%(line_3_x1)s" y1="%(line_3_y1)s" x2="%(line_3_x2)s" y2="%(line_3_y2)s"'''+en+"/>"
            e4 = '''<text class="st1" x="%(text_x)s" y="%(text_y)s" font-size="%(dim_text_size)spx" textLength="%(Ltext)s" lengthAdjust="spacingAndGlyphs"'''+en_text+'>%(svg_text)s</text>'

            if cd['type_arrow'] != 'Arch':                
                a1 = '''<line class="st1" x1="%(arrow_1_x1)s" y1="%(arrow_1_y1)s" x2="%(arrow_1_x2)s" y2="%(arrow_1_y2)s"'''+en+"/>"
                a2 = '''<line class="st1" x1="%(arrow_2_x1)s" y1="%(arrow_2_y1)s" x2="%(arrow_2_x2)s" y2="%(arrow_2_y2)s"'''+en+"/>"
                a3 = '''<line class="st1" x1="%(arrow_3_x1)s" y1="%(arrow_3_y1)s" x2="%(arrow_3_x2)s" y2="%(arrow_3_y2)s"'''+en+"/>"
                a4 = '''<line class="st1" x1="%(arrow_4_x1)s" y1="%(arrow_4_y1)s" x2="%(arrow_4_x2)s" y2="%(arrow_4_y2)s"'''+en+"/>"
            else:
                a1 = '''<line class="st1" x1="%(arrow_1_x1)s" y1="%(arrow_1_y1)s" x2="%(arrow_1_x2)s" y2="%(arrow_1_y2)s"'''+en+"/>"
                a2 = '''<line class="st1" x1="%(arrow_2_x1)s" y1="%(arrow_2_y1)s" x2="%(arrow_2_x2)s" y2="%(arrow_2_y2)s"'''+en+"/>"
                a3 = ''
                a4 = ''
            e5 = '</g>'
            e = [x % cd for x in (e0, e_desc, e1, e2, e3, e4, a1, a2, a3, a4, e5) if x]
            cd['svg_strings'] = e
            
        return cd
            
        '''
        cd = self.get_conf()
        if dxf:
            cd['fill'] = dxf_colorer(cd['fill'])
            yf = -1
        else:
            yf = 1
        lines_coord = get_conf.coord_dim_lines(self.par, self.obj, cd, dxf, yf)
        cd.update(lines_coord)
        if cd['text'] in ('None', None):
            if cd['ort'] == "horizontal":
                cd['dim_distanse'] = int(format(abs(cd['y1'] - cd['y2']), '.0f'))                            
            else:
                cd['dim_distanse'] = int(format(abs(cd['x1'] - cd['x2']), '.0f'))
        else:
            cd['dim_distanse'] = cd['text']

        if cd['ort'] == "horizontal":
            cd.update({'arrow_point1_x': cd['x3'],
                    'arrow_point1_y': yf*cd['y1'],
                    'arrow_point2_x': cd['x3'],
                    'arrow_point2_y': yf*cd['y2']})
            cd.update({'angle': 90.0,
                    'angle_arrow1': 90.0,
                    'angle_arrow2': 270.0})
            
            if cd['type_arrow'] == 'Arrow':
                cd.update({'arrow_5_x': cd['x3'],
                    'arrow_5_y': lines_coord['arrow_1_y1'],
                    'arrow_6_x': cd['x3'],
                    'arrow_6_y': lines_coord['arrow_3_y1']})
        else:
            cd.update({'arrow_point1_x': cd['x1'],
                    'arrow_point1_y': yf*cd['y3'],
                    'arrow_point2_x': cd['x2'],
                    'arrow_point2_y': yf*cd['y3'],
                    'angle': 0.0,
                    'angle_arrow1': 180.0,
                    'angle_arrow2': 0.0})
            if cd['type_arrow'] == 'Arrow':
                cd.update({'arrow_5_y': yf*cd['y3'],   
                    'arrow_5_x': lines_coord['arrow_1_x1'],
                    'arrow_6_y': yf*cd['y3'],
                    'arrow_6_x': lines_coord['arrow_3_x1']})
        if cd['text_change'] != 'online3':
            cd.update({'line_3_x1': cd['arrow_point1_x'],
                    'line_3_x2': cd['arrow_point2_x'],
                    'line_3_y1': cd['arrow_point1_y'],
                    'line_3_y2': cd['arrow_point2_y']})
                
        cd['text_place'] = text_place
        if lines_coord:
            cd.update(lines_coord)
        e = "self.dim(x1 = %(x1)s, y1 = %(y1)s, x2 = %(x2)s, y2 = %(y2)s, x3 = %(x3)s, y3 = %(y3)s, text = u'%(text)s', fill = '%(fill)s', ort = '%(ort)s', size = %(size)s, text_change = '%(text_change)s', text_place = %(text_place)s, sloy = %(sloy)s, s = %(s)s, vr_s = %(vr_s)s, vv_s = %(vv_s)s, arrow_s = %(arrow_s)s, type_arrow = '%(type_arrow)s', s_s = %(s_s_dim)s, w_text = %(w_text_dim)s, font = '%(font_dim)s')"
        e = (e % cd)
        return e, cd
        '''
    
    ### Edit_prop method ###
    def edit_prop(self, params):
        #param_changed = False
        #r_list = None
        cd = self.par.ALLOBJECT[self.obj]#self.get_conf()
        for param in params:
            if param in cd:
                param_changed = True
                cd[param] = params[param]
        #if param_changed == True:
        cd['temp'] = False
        cd['in_mass'] = True
        cNew = self.create_object(cd)
            #r_list = (self.obj, self.par.Nline)
        return cNew

    ### Edit method ###
    def edit(self, x1, y1, x2, y2):
        cd = self.par.ALLOBJECT[self.obj].copy()
        cd['in_mass'] = True
        cd['temp'] = False
        cNew = self.edit_object(x1, y1, x2, y2, cd)
        return cNew
        #text_change = 'unchange'
        #text_place = None
        '''
        cd['x3'] = cd['coords'][2][0]
        cd['y3'] = cd['coords'][2][1]
        
        cd['x4'] = cd['coords'][2][2]
        cd['y4'] = cd['coords'][2][3]
        
        
        a = sqrt((cd['x1'] - x1)**2 + (cd['y1'] - y1)**2)
        b = sqrt((cd['x2'] - x1)**2 + (cd['y2'] - y1)**2)
        c = sqrt((cd['x3'] - x1)**2 + (cd['y3'] - y1)**2)
        d = sqrt((cd['x4'] - x1)**2 + (cd['y4'] - y1)**2)

        if a < self.par.min_e:
            cd['x1'], cd['y1'] = x2, y2
        elif b < self.par.min_e:
            cd['x2'], cd['y2'] = x2, y2
        elif c < self.par.min_e or d < self.par.min_e:
            cd['x3'], cd['y3'] = x2, y2
        elif abs(cd['x3'] - x1) < self.par.min_e or abs(cd['y3'] - y1) < self.par.min_e:
            cd['x3'], cd['y3'] = x2, y2
            #text_change = cd['text_change']
            #text_lines, priv_line, text_place =
            #text_lines, priv_line, text_place = get_conf.dim_text_place(content)
            #if cd['ort'] == 'vertical':#text_place[2] == 'hor':
            #    text_place[1] = y1 + (y2-y1)
            #else:
             #   text_place[0] = x1 + (x2-x1)
        cd['in_mass'] = True
        cd['temp'] = False

        cNew = self.create_object(cd)
                    
        return cNew
        '''

    def edit_temp(self, x1, y1, x2, y2):
        cd = self.par.ALLOBJECT[self.obj].copy()
        cd.update(temp_dict)
        cd['in_mass'] = False
        self.edit_object(x1, y1, x2, y2, cd)
        #text_change = 'unchange'
        #text_place = None
        #cd = self.grt_coords(cd)
        '''
        cd['x3'] = cd['coords'][2][0]
        cd['y3'] = cd['coords'][2][1]
        
        cd['x4'] = cd['coords'][2][2]
        cd['y4'] = cd['coords'][2][3]
        
        
        a = sqrt((cd['x1'] - x1)**2 + (cd['y1'] - y1)**2)
        b = sqrt((cd['x2'] - x1)**2 + (cd['y2'] - y1)**2)
        c = sqrt((cd['x3'] - x1)**2 + (cd['y3'] - y1)**2)
        d = sqrt((cd['x4'] - x1)**2 + (cd['y4'] - y1)**2)

        if a < self.par.min_e:
            cd['x1'], cd['y1'] = x2, y2
        elif b < self.par.min_e:
            cd['x2'], cd['y2'] = x2, y2
        elif c < self.par.min_e or d < self.par.min_e:
            cd['x3'], cd['y3'] = x2, y2
        elif abs(cd['x3'] - x1) < self.par.min_e or abs(cd['y3'] - y1) < self.par.min_e:
            cd['x3'], cd['y3'] = x2, y2
            #text_change = cd['text_change']
            #text_lines, priv_line, text_place =
            #text_lines, priv_line, text_place = get_conf.dim_text_place(content)
            #if cd['ort'] == 'vertical':#text_place[2] == 'hor':
            #    text_place[1] = y1 + (y2-y1)
            #else:
             #   text_place[0] = x1 + (x2-x1)
        cd['in_mass'] = False
        #if event:
            #cd['temp'] = False
        #else:
        #cd['temp'] = True
            
        self.create_object(cd)
        '''
        
    def edit_object(self, x1, y1, x2, y2, cd):
        cd['x3'] = cd['coords'][2][0]
        cd['y3'] = cd['coords'][2][1]
        
        cd['x4'] = cd['coords'][2][2]
        cd['y4'] = cd['coords'][2][3]
        
        
        a = sqrt((cd['x1'] - x1)**2 + (cd['y1'] - y1)**2)
        b = sqrt((cd['x2'] - x1)**2 + (cd['y2'] - y1)**2)
        c = sqrt((cd['x3'] - x1)**2 + (cd['y3'] - y1)**2)
        d = sqrt((cd['x4'] - x1)**2 + (cd['y4'] - y1)**2)

        if a < self.par.min_e:
            cd['x1'], cd['y1'] = x2, y2
        elif b < self.par.min_e:
            cd['x2'], cd['y2'] = x2, y2
        elif c < self.par.min_e or d < self.par.min_e:
            cd['x3'], cd['y3'] = x2, y2
        elif abs(cd['x3'] - x1) < self.par.min_e or abs(cd['y3'] - y1) < self.par.min_e:
            cd['x3'], cd['y3'] = x2, y2
        else:
            return False
            #text_change = cd['text_change']
            #text_lines, priv_line, text_place =
            #text_lines, priv_line, text_place = get_conf.dim_text_place(content)
            #if cd['ort'] == 'vertical':#text_place[2] == 'hor':
            #    text_place[1] = y1 + (y2-y1)
            #else:
             #   text_place[0] = x1 + (x2-x1)
        #cd['in_mass'] = False
        #if event:
            #cd['temp'] = False
        #else:
        #cd['temp'] = True
        cNew = self.create_object(cd)
        return cNew
    
        
    ### Rotate methods ###    
    def rotate(self, x0, y0, msin, mcos, angle):
        pass

    def rotate_temp(self, x0, y0, msin, mcos, angle):
        pass

    ### Rotate methods ###    
    def mirror(self, x0, y0, msin, mcos):
        pass

    def mirror_temp(self, x0, y0, msin, mcos):
        pass

    ### Copy method ###    
    def copy(self, d):
        cd = self.par.ALLOBJECT[self.obj].copy() #self.get_conf()
        cd['x1'] += d[0]
        cd['y1'] += d[1]
        cd['x2'] += d[0]
        cd['y2'] += d[1]
        cd['x3'] += d[0]
        cd['y3'] += d[1]
        
        if cd['text_place']:
            cd['text_place'][0] += d[0]
            cd['text_place'][1] += d[1]
        cd['in_mass'] = True    
        cd['temp'] = False
        self.create_object(cd)
        

    def copy_temp(self, d):
        cd = self.par.ALLOBJECT[self.obj].copy()
        cd.update(temp_dict)
        
        #coord = list(self.par.ALLOBJECT[self.obj]['coords'])#self.par.ALLOBJECT[self.obj].copy() #self.get_conf()
        cd['x1'] += d[0]
        cd['y1'] += d[1]
        cd['x2'] += d[0]
        cd['y2'] += d[1]
        cd['x3'] += d[0]
        cd['y3'] += d[1]
    
        #coord = [y+d[0] if ind%2 == 0 else y+d[1] for ind, y in enumerate(]
        if cd['text_place']:
            cd['text_place'][0] += d[0]
            cd['text_place'][1] += d[1]
        #cd['temp'] = False
        cd['in_mass'] = True
        self.create_object(cd)
        
    
    

#РАЗМЕР РАДИУСНЫЙ
class Dimension_R:
    def __init__(self, par):
        self.par = par
        self.risDimR()

    def risDimR(self, event = None):
        self.par.kill()
        self.par.standart_unbind()
        self.par.old_func = 'self.risDimR()'
        self.par.c.bind('<Button-1>', self.risDimR2)
        self.par.dialog.config(text = u'Radius dimension - point 1:')
        self.par.info.config(text = u'Enter - stop')

    def risDimR2(self, event):
        self.par.ex = self.par.priv_coord[0]
        self.par.ey = self.par.priv_coord[1]
        self.par.set_coord()
        self.par.c.bind_class(self.par.c,"<1>", self.risDimR3)
        self.par.dialog.config(text = u'Radius dimension - point 2:')
        self.par.command.focus_set()
        self.par.dimR_clone = True    

    def risDimR3(self, event=None):
        self.par.ex2 = self.par.priv_coord[0]
        self.par.ey2 = self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        self.par.set_coord()
        self.par.trace_on = True
        self.par.trace_x1, self.par.trace_y1 = self.par.ex,self.par.ey
        self.par.trace_x2, self.par.trace_y2 = self.par.ex2,self.par.ey2
        if (self.par.ex2, self.par.ey2) != (self.par.ex, self.par.ey):
            if event:
                c_dimR(self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
                self.par.history_undo.append(('c_', self.par.Ndimr))
                self.par.changeFlag = True
                self.par.enumerator_p()
                self.par.risDimR()
            else:
                self.par.set_coord()
                c_dimR(self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2, temp = 'Yes')

def c_dimR(par,x1,y1,x2,y2, text=None, sloy = None,
                                            fill = None,
                                            size = None,
                                            s=None,
                                            vr_s = None,
                                            arrow_s = None,
                                            type_arrow = None,
                                            s_s = None,
                                            w_text = None,
                                            font = None,
                                            Rn = None,
                                            temp = None):
    if sloy == None:
        sloy = par.sloy
        fill = par.color
        size = par.size_f
        s = old_s = par.s
        vr_s = old_vr_s = par.vr_s
        arrow_s = old_arrow_s = par.arrow_s
        type_arrow = par.type_arrow
        s_s = par.s_s_dim
        w_text = par.w_text_dim
        font = par.font_dim
    else:
        old_s = s
        old_vr_s = vr_s
        old_arrow_s = arrow_s
    if text == 'None':
        text = None
    if not temp:
        par.Ndimrd+=1
        par.Ndimr = 'r' + str(par.Ndimrd)
        dx=x2-x1
        dy=y2-y1
        R = sqrt(dx*dx + dy*dy)
        
        id_dict = {}
        list_arrow = []
        list_lines = []
        list_text_lines = []
        
        if par.zoomOLD==0:
            Rr = R
        else:
            if par.zoomOLD>0:
                s*=(zoomp**par.zoomOLD)
                arrow_s*=(zoomp**par.zoomOLD)
                vr_s*=(zoomp**par.zoomOLD)
                Rr=R*zoomm**par.zoomOLD
            else:
                zoomOLDx=par.zoomOLD*(-1)
                s/=(zoomp**zoomOLDx)
                arrow_s/=(zoomp**zoomOLDx)
                vr_s/=(zoomp**zoomOLDx)
                Rr=R*zoomp**zoomOLDx
        if Rn != None:
            Rr = Rn
            R = par.coordinator2(Rn)
        Rrr=format(Rr, '.0f')

        angle = abs(calc_angle(x1, y1, x2, y2, x1+R, y1))
        i = 1
        anchor = 'sw'
        if y2>y1:
            angle = -angle
        if x2<x1:
            i = -1
            angle = angle-pi
            anchor = 'se'
        if text:
            textt = text
        else:
            textt = 'R ' + Rrr
        x1t = x1 + i*(R + arrow_s*2.0)
        y1t = y1 - s
        list_text_lines = symbols.font(x1t, y1t, textt, size, par.zoomOLD, s_s, w_text, anchor, font, 0)
        e = list_text_lines.nabor[0]
        if i > 0:
            list_lines.extend([[x1, y1, e[2], y1]])
        else:
            list_lines.extend([[x1, y1, e[0], y1]])
            
        if type_arrow == 'Arch':
            L1 = [x1+i*(R-arrow_s), y1+arrow_s, x1+i*(R+arrow_s), y1-arrow_s]
            list_arrow.extend([L1,])
                                  
        elif type_arrow == 'Arrow':
            L1 = [x1+i*R,y1,x1+i*(R-arrow_s),y1-arrow_s/10.0]
            L2 = [x1+i*R,y1,x1+i*(R-arrow_s),y1+arrow_s/10.0]
            list_arrow.extend([L1, L2])
        list_text_lines.nabor = rotate_lines(x1, y1, list_text_lines.nabor, angle)
        list_arrow = rotate_lines(x1, y1, list_arrow, angle)
        list_lines = rotate_lines(x1, y1, list_lines, angle)
            
        for i in list_arrow:
            id = par.c.create_line(i, fill=fill, tags = ('obj', par.Ndimr, 'sel'))
            id_dict[id] = ('line',)
        for i in list_lines:
            id = par.c.create_line(i, fill=fill, tags = ('obj', par.Ndimr, 'sel'))
            id_dict[id] = ('line', 'priv')
            
        for i in list_text_lines.nabor[1:]: 
            try:
                id = par.c.create_line(i[0],i[1],i[2],i[3],fill=fill, tags = ('obj', par.Ndimr, 't_LOD', 'sel'))
                id_dict[id] = ('line', 'dim_text')
            except:
                pass
        snap_text = list_text_lines.nabor[0]
        id = par.c.create_line(snap_text[0],snap_text[1],snap_text[2],snap_text[3], width=8, fill = fill, stipple = ('@'+path.join(par.appPath, 'res', '00.xbm')), tags = ('obj', par.Ndimr, 'snap_text', 'sel'))        
        id_dict[id] = ('line', 'priv', 'dim_text', 'dim_text_priv')
        par.ALLOBJECT[par.Ndimr]={'text':text,#Записать в ALLOBJECT параметры размера
                                    'angle':angle,
                                    'object':'dimr',
                                    'fill':fill,
                                    'size':size,
                                    'sloy':sloy,
                                    's' : old_s,
                                    'R' : Rr,
                                    'vr_s': old_vr_s,
                                    'arrow_s': old_arrow_s,
                                    'type_arrow':type_arrow,
                                    's_s_dim':s_s,
                                    'w_text_dim':w_text,
                                    'font_dim':font,
                                    'id':id_dict}
    else:
        dx=x2-x1
        dy=y2-y1
        R = sqrt(dx*dx + dy*dy)
        list_arrow = []
        list_lines = []
        list_text_lines = []   
        if par.zoomOLD==0:
            Rr = R
        else:
            if par.zoomOLD>0:
                s*=(zoomp**par.zoomOLD)
                arrow_s*=(zoomp**par.zoomOLD)
                vr_s*=(zoomp**par.zoomOLD)
                Rr=R*zoomm**par.zoomOLD
            else:
                zoomOLDx=par.zoomOLD*(-1)
                s/=(zoomp**zoomOLDx)
                arrow_s/=(zoomp**zoomOLDx)
                vr_s/=(zoomp**zoomOLDx)
                Rr=R*zoomp**zoomOLDx
        if Rn != None:
            Rr = Rn
            R = par.coordinator2(Rn)
        Rrr=format(Rr, '.0f')

        angle = abs(calc_angle(x1, y1, x2, y2, x1+R, y1))
        i = 1
        anchor = 'sw'
        if y2>y1:
            angle = -angle
        if x2<x1:
            i = -1
            angle = angle-pi
            anchor = 'se'
        if text:
            textt = text
        else:
            textt = 'R ' + Rrr
        x1t = x1 + i*(R + arrow_s*2.0)
        y1t = y1 - s
        list_text_lines = symbols.font(x1t, y1t, textt, size, par.zoomOLD, s_s, w_text, anchor, font, 0)
        e = list_text_lines.nabor[0]
        if i > 0:
            list_lines.extend([[x1, y1, e[2], y1]])
        else:
            list_lines.extend([[x1, y1, e[0], y1]])
            
        if type_arrow == 'Arch':
            L1 = [x1+i*(R-arrow_s), y1+arrow_s, x1+i*(R+arrow_s), y1-arrow_s]
            list_arrow.extend([L1,])
                                  
        elif type_arrow == 'Arrow':
            L1 = [x1+i*R,y1,x1+i*(R-arrow_s),y1-arrow_s/10.0]
            L2 = [x1+i*R,y1,x1+i*(R-arrow_s),y1+arrow_s/10.0]
            list_arrow.extend([L1, L2])

        list_text_lines.nabor = rotate_lines(x1, y1, list_text_lines.nabor, angle)
        list_arrow = rotate_lines(x1, y1, list_arrow, angle)
        list_lines = rotate_lines(x1, y1, list_lines, angle)
            
        for i in list_arrow:
            par.c.create_line(i, fill=fill, tags = ('obj', 'temp'))
        for i in list_lines:
            par.c.create_line(i, fill=fill, tags = ('obj', 'temp'))
        for i in list_text_lines.nabor[1:]: 
            try:
                par.c.create_line(i[0],i[1],i[2],i[3],fill=fill, tags = ('obj', 'temp'))
            except:
                pass
        snap_text = list_text_lines.nabor[0]
        par.c.create_line(snap_text[0],snap_text[1],snap_text[2],snap_text[3], width=8, fill = fill, stipple = ('@'+path.join(par.appPath, 'res', '00.xbm')), tags = ('obj', 'temp'))
        
      
