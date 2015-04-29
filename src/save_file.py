# -*- coding: utf-8; -*-
from math import ceil, degrees, sqrt

import src.dxf_library.color_acad_rgb as color_acad_rgb
import os
class Base_save(object):
    # Базовый класс сохранения
    def __init__(self, par, file_format, ALLOBJECT, layers, drawing_w, drawing_h):
        self.par = par
        self.AL = ALLOBJECT 
        self.config_list = []           
        
        for obj in self.AL:
            if obj == 'trace':
                continue
            if obj == 'trace_o':
                continue
            config = self.AL[obj]['class'].save(file_format, layers, drawing_w, drawing_h)
            self.config_list.append(config)
        if file_format == '.dxf':
            for i in self.config_list:
                i['color'] = self.dxf_colorer(tuple(i['color']))

    def dxf_colorer(self, color):
        return self.par.RGB_DXF_colores[color]
                
class Save_to_SVG(Base_save):
    def __init__(self, par, file_name, file_format, ALLOBJECT, layers, drawing_w, drawing_h):
        self.par = par
        self.w = ceil(drawing_w)
        self.h = ceil(drawing_h)
        
        self.drawing_data = {
                            'h':self.h,
                            'w':self.w,
                                                        
                            'drawing_name':os.path.basename(file_name),
                            }
        
        self.write_list = []
        self.st0 = {
                    "fill": "white",
                    "width": 2,
                    "stipple":None,
                    }
        
        e = """<svg id="%(drawing_name)s" version="1.1" width="%(w)s" height="%(h)s" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" type="1">"""
        e = (e % self.drawing_data)
        self.write_list.append(e)

        e = """<defs>
<style type="text/css"><![CDATA[
line,
rect,
circle,
ellipse,
path,
text {
  vector-effect: non-scaling-stroke;
}
.st1 {
  fill: none;
  stroke: black;
  stroke-width: 2;
  stroke-dasharray: none
  }
}
]]></style>
</defs>"""
        self.write_list.append(e)
        super(Save_to_SVG, self).__init__(file_format, ALLOBJECT, layers, drawing_w, drawing_h)
        for i in self.config_list:
            strings = i['svg_strings']
            self.write_list.extend(strings)

        e = """</svg>"""
        self.write_list.append(e)

        f = open(file_name, 'w')
        for i in self.write_list:
            try:
                f.writelines("%s\n" % i)
            except:
                print i, type(i)
        f.close()

def get_object_lines(cd, drawing_h, file_format):
    lines_coord = {}        
    for ind, i in enumerate(cd['coords']):
        lines_coord.update({
            'line_'+str(ind+1)+'_x1': i[0],
            'line_'+str(ind+1)+'_y1': i[1],
            'line_'+str(ind+1)+'_x2': i[2],
            'line_'+str(ind+1)+'_y2': i[3]
            })
    for ind, i in enumerate(cd['arrow_lines']):
        lines_coord.update({
            'arrow_'+str(ind+1)+'_x1': i[0],
            'arrow_'+str(ind+1)+'_y1': i[1],
            'arrow_'+str(ind+1)+'_x2': i[2],
            'arrow_'+str(ind+1)+'_y2': i[3]
            })

    x1 = cd['coords'][3][0]
    y1 = cd['coords'][3][1]
    x2 = cd['coords'][3][2]
    y2 = cd['coords'][3][3]
    # Длинна текста
    lines_coord['Ltext'] = sqrt((x1-x2)**2+(y1-y2)**2)
    if file_format == '.dxf':
        # Если DXF - берется центральная точка текста
        #!!!
        
        if cd['ort'] == "horizontal":
            y = (y1+y2)/2.0
            yy = y
            x = cd['x3']#coord_list[2][0]
            xx = x1 - cd['dim_text_size']/2.0
        else:
            x = (x1+x2)/2.0
            xx = x
            y = cd['y3']#coord_list[2][1]
            yy = y1 + cd['dim_text_size']/2.0
        #!!!
    else:
        # Иначе - нижняя  левая
        x = x1
        xx = x2
        y = y1
        yy = y2
        
    lines_coord.update({
        'text_x': x,
        'text_y': y,
        'text_xx': xx,
        'text_yy': yy
        })
    cd.update(lines_coord)

    if cd['ort'] == "horizontal":
        cd.update({
            'arrow_point1_x': cd['x3'],
            'arrow_point1_y': cd['y1'],
            'arrow_point2_x': cd['x3'],
            'arrow_point2_y': cd['y2'],
            #'angle': 90.0,
            'angle_arrow1': 90.0,
            'angle_arrow2': 270.0,
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
            #'angle': 0.0,
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
    return cd

def prop_to_svg_style(layers, cd, SVG_prop):
    #Принимает словарь слоев из SVG, свойства объекта, словарь вида
    # cd_name : (SVG_name, cd_value)
    #Возвращает строку style="..." для вставки в SVG
    try:
        layer_prop = layers[cd['layer']]
    except:
        print layers
        print cd['layer']
    SVG_style_list = []
    style_string = ' '
    for prop in SVG_prop.keys():
        if cd[prop] != layer_prop[prop] and cd[prop]:   
            SVG_style_list.append("%s: %s;" %(SVG_prop[prop][0], SVG_prop[prop][1]))

    if SVG_style_list:
        SVG_style_list.insert(0, '''style="''')
        SVG_style_list.append('''"''')
        style_string += ''.join(SVG_style_list)
    return style_string
        
        
