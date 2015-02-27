# -*- coding: utf-8; -*-
from math import pi, sqrt, radians, ceil
import re
from calc import min_distanse, intersection_stright
import src.line as line
import src.dimension as dimension

import src.text_line as text_line
import src.sectors_alg as sectors_alg
import xml.etree.ElementTree as etree

class Open_from_SVG:
    def __init__(self, par, _file, file_format):
        self.par = par
        
        self.par.delete_objects(self.par.ALLOBJECT.keys())
        self.par.collection = []

        self.file = etree.parse(_file)#_file.split('\n')
        self.styles_dict = {}
        self.config_list = []
        

        self.prop_dict = {
                    'stroke' : ('color', self.color),
                    'fill' : ('color', self.color),
                    'stroke-width' : ('width', lambda x: int(x)),
                    'stroke-dasharray' : ('stipple', self.stipple),
                    }
        self.color_dict = {
                        "white" : [0, 0, 0],
                        "light blue" : [0, 255, 255],
                        "blue" : [0, 0, 255],
                        "green" : [0, 255, 0],
                        "gray" : [110, 110, 110] ,
                        "black" : [255, 255, 255],
                        "yellow" : [255, 255, 0],
                        "orange" : [255, 127, 0] ,
                        "red" : [255, 0, 0],
                            }

        self.svg_file()
        
        for obj in self.config_list:
            if obj['object'] == 'line':
                line.c_line(
                            self.par, obj['x1'], obj['y1'], obj['x2'], obj['y2'],
                            width = obj['width'],
                            layer = obj['layer'],
                            color = obj['color'],
                            stipple = obj['stipple'],
                            factor_stipple = obj['factor_stipple'],
                            in_mass = True,
                        )

            elif obj['object'] == 'text_line':
                text_line.c_text(self.par, obj['x'], obj['y'],
                    text = obj['text'],
                    anchor = obj['anchor'],
                    layer = obj['layer'],
                    color = obj['color'],
                    angle = obj['angle'],
                    text_size = obj['text_size'],
                    text_s_s = obj['text_s_s'],
                    text_w = obj['text_w'],
                    text_font = obj['text_font'],
                    in_mass = True,
                    temp = False,
                    )

            elif obj['object'] == 'dimL':
                cNew =  dimension.c_dim(
                    self.par,
                    float(obj['x1']),
                    float(obj['y1']),
                    float(obj['x2']),
                    float(obj['y2']),
                    float(obj['x3']),
                    float(obj['y3']),
                    text = obj['text'],
                    layer = obj['layer'],
                    color = obj['color'],
                    dim_text_size = float(obj['dim_text_size']),
                    ort = obj['ort'],
                    text_change = int(obj['text_change']),
                    text_place = obj['text_place'],
                    s = float(obj['s']),
                    vv_s = float(obj['vv_s']),
                    vr_s = float(obj['vr_s']),
                    arrow_s = float(obj['arrow_s']),
                    type_arrow = obj['type_arrow'],
                    dim_text_s_s = float(obj['dim_text_s_s']),
                    dim_text_w = float(obj['dim_text_w']),
                    dim_text_font = obj['dim_text_font'],
                    in_mass = True,
                    temp = False,
                    )
                

        self.par.change_pointdata()
        self.par.ALLOBJECT, self.par.sectors = sectors_alg.quadric_mass(
                                        self.par.ALLOBJECT,
                                        self.par.ALLOBJECT.keys(),
                                        self.par.sectors,
                                        self.par.q_scale
                                        )

        self.par.drawing_rect_data = [
            0.0, 0.0, self.par.drawing_w, 0.0,
            0.0, 0.0, 0.0, self.par.drawing_h,
            self.par.drawing_w, self.par.drawing_h, self.par.drawing_w, 0.0,
            self.par.drawing_w, self.par.drawing_h, 0.0, self.par.drawing_h
                                  ]
    
        #Список индексов ID
        #self.par.inds_vals = dict((y,x) for x,y in enumerate(self.par.IDs))
        

    def svg_file(self):
        re_layer = re.compile('\.st([^{}]*) {([^{}]*)}')
        re_style_prop = re.compile('([^=:; ]+): ([^=;]+);')
        re_class = re.compile('([\w-]+) ?: ?([\w., ()]+)')
        
        level_1 = self.file.getroot()
        level_2 = level_1.getchildren()
        level_3 = level_2[0].getchildren()
        text_styles = level_3[0].text

        self.par.drawing_w = float(level_1.attrib['width'])
        self.par.drawing_h = float(level_1.attrib['height'])
        self.par.create_sectors()

        re_styles = re_layer.findall(text_styles)

        for layer, props in re_styles:

            self.styles_dict[layer] = {}
            #Перебрать по строчкам свойства стиля
            for prop_str in props.split('\n'):

                #Взять пару (имя параметра, значение
                prop_n_v = re_style_prop.findall(prop_str)
                #if prop_n_v:
                    #prop_n_v = prop_n_v.groups()
                if prop_n_v:
                    
                    #Отправить на обработку
                    name, value = self.proper(prop_n_v[0])
                    self.styles_dict[layer][name] = value
                    
            # Проверить все ли параметры есть в слое
            for i in self.par.default_layer.keys():
                if i not in self.styles_dict[layer]:
                    #Если параметра нет - добавить поумолчанию
                    self.styles_dict[layer][i] = self.par.default_layer[i]
                    
        self.par.layers = self.styles_dict
        for i in level_2:
            config = {}
            tag = i.tag
            if tag == '{http://www.w3.org/2000/svg}line':
                attrib = i.attrib
                config['object'] = 'line'
                config['x1'] = float(attrib['x1'])
                config['y1'] = self.par.drawing_h - float(attrib['y1'])
                config['x2'] = float(attrib['x2'])
                config['y2'] = self.par.drawing_h - float(attrib['y2'])
                config['layer'] = attrib['class'][2:]

                from_style = self.styles_dict[config['layer']]
                config.update(from_style)

                if 'style' in attrib:
                    style_attrib = re_class.findall(attrib['style'])
                    if style_attrib:
                        for prop_n_v in style_attrib:
                            name, value = self.proper(prop_n_v)
                            config[name] = value

                self.config_list.append(config)

            elif tag == '{http://www.w3.org/2000/svg}text':
                attrib = i.attrib
                config['object'] = 'text_line'
                ###
                config['x'] = float(attrib['x'])
                config['y'] = self.par.drawing_h - float(attrib['y'])
                
                config['layer'] = attrib['class'][2:]

                #from_style = self.styles_dict[config['layer']]
                #config.update(from_style)
                config['text'] = i.text
                config['text_s_s'] = 1.3
                config['text_size'] = attrib['font-size']
                if 'px' in config['text_size']:
                    config['text_size'] = float(config['text_size'][0:-2])
                elif 'mm' in config['text_size']:
                    config['text_size'] = float(config['text_size'][0:-2])
                else:
                    config['text_size'] = float(config['text_size'])

                if 'transform' in attrib:
                    re_rotate = re.compile('rotate\(([^",]+)[, ]+([^",]+)[, ]+([^",]+)\)')
                    find_rotate = re_rotate.search(attrib['transform'])
                    config['angle'] = radians(-float(find_rotate.groups()[0]))
                else:
                    config['angle'] = 0.0

                config['anchor'] = 'sw'
                config['text_w'] = 1
                config['color'] = [255, 255, 255]
                config['text_font'] = 'TXT'
                self.config_list.append(config)
                ###
            elif tag == '{http://www.w3.org/2000/svg}g':
                attrib = i.attrib
                config['object'] = 'dimL'
                
                if attrib['class'] == 'DimL':
                    elements = i.getchildren()
                    for el in elements:
                        if el.tag == '{http://www.w3.org/2000/svg}desc':
                            re_desc = re.compile('''([\w][^=, ]*) = "([^=]*)"''')
                            props = re_desc.findall(el.text)#.groups()
                            confs = dict((key, val) for key, val in props)
                            config.update(confs)
                            config['color'] = self.color(config['color'], svg = False)
                            re_list = re.compile('([.\d]+), ?([.\d]+)')
                            text_place = re_list.search(config['text_place'])
                            
                            if text_place:
                                list_str = text_place.groups()
                                config['text_place'] = [float(x) for x in list_str]
                            else:
                                config['text_place'] = None
                                config['text_change'] = None
                                
                            if config['text'] == 'None':
                                config['text'] = None

                            self.config_list.append(config)

                    
                
                
        for i in self.config_list:
            if 'stipple' in i and i['stipple']:
                stipple = i['stipple'][0]
                factor_stipple = i['stipple'][1]
                i['stipple'] = stipple
                i['factor_stipple'] = factor_stipple
                
            else:
                i['stipple'] = None
                i['factor_stipple'] = 10

            if 'dash' in i:
                del i['dash']
                    
                    
    def proper(self, name_value):
        name = name_value[0]
        value = name_value[1]
        
        ist_name = self.prop_dict[name][0]
        ist_value = self.prop_dict[name][1](value)
                    
        return ist_name, ist_value

    def color(self, value, svg = True):
        if svg:
            re_color = re.compile('rgb[a]?\(([.\d]+), ?([.\d]+), ?([.\d]+)[,. \d]*\)')
            factor = 255
        else:
            re_color = re.compile('\(([.\d]+), ?([.\d]+), ?([.\d]+)\)')
            factor = 1
        rgb = re_color.search(value)
        ist_value = [255, 255, 255]
        if rgb:
            rgb = rgb.groups()
            ivalue = []
            for color in rgb:
                i = int(color)*factor
                if i > 255:
                    return ist_value
                ivalue.append(i)
            if ivalue == [0, 0, 0]:
                ivalue = [255, 255, 255]
            ist_value = ivalue
            
        elif value in self.color_dict:
            ist_value = self.color_dict[value]
       
            

        return ist_value

    def stipple(self, value):
        re_stipple = re.compile('[-+]?([0-9]*\.[0-9]+|[0-9]+)[, ]?')
        value = re_stipple.findall(value)
        ist_value = None
        if value:
            value = [int(float(x)) for x in value]
            for line_type in self.par.stipples:
                stipple = self.par.stipples[line_type]
                
                if stipple and len(stipple) == len(value):
                    factor_stipple = value[0]/stipple[0]
                    ist_value = (stipple, factor_stipple)
        return ist_value

    
                


              
    def svg_file1111(self):
        self.re_dict = {
                'styles' : (re.compile('<style.*>'), self.styles),
                #'defs': (re.compile('<defs>'),self.defs),
                'line' : (re.compile('<line.*/>'),self.line),
                'circle' : (re.compile('<circle.*/>'),self.circle),
                'text' : (re.compile('<text.*>.*</text>'),self.text),
                'arc': (re.compile('<path.*/>'),self.arc),
                'dimL' : (re.compile('<g class="DimL".*>'),self.dim),
                'dimR' : (re.compile('<g class="DimR".*>'),self.dim),
                'rect' : (re.compile('<rect.*/>'),self.rect),
                }
        self.re_style_dict = {
                        're_fill' : (re.compile('stroke: ([^=;]+);'),'fill'),
                        're_fill_text' : (re.compile('fill: ([^=;]+);'),'fill'),
                        're_width' : (re.compile('stroke-width: ([^= ]+);'),'width'),
                        're_dash' : (re.compile('stroke-dasharray: ([^=;]+);'),'dash'),
                        }
        
                
        g_flag = False
        for ind, s in enumerate(self.file):
            
            if g_flag:
                if '</g>' in s:
                    g_flag = False
                continue
            for i in self.re_dict:
                if self.re_dict[i][0].search(s):
                    self.re_dict[i][1](s, ind)
                    if i in ('dimL', 'dimR'):
                        g_flag = True
                

    def styles(self, s, ind):
        re_style = re.compile('\.([^ ]*)[ ]?{')
        
        
        ind0 = ind - 1
        style_flag = 0
        for i in self.file[ind:]:
            
            ind0 += 1
            if style_flag == 0:
                if '</style>' in i:
                    break
                if re_style.search(i):
                    
                    if '}' not in i:
                        style_flag = 1
                        style_name = re_style.search(i).groups()[0]
                        self.styles_dict[style_name] = {}
                    else:
                        style_name = re_style.search(i).groups()[0]
                        if re.compile('font-size: ([^;]+)(;|\})?').search(i):
                            font_size = re.compile('font-size: ([^;]+)(;|\})?').search(i).groups()[0]
                        else:
                            continue
                        self.styles_dict[style_name] = {}
                        self.styles_dict[style_name]['font-size'] = font_size
                    
                    continue
            else:
                for opt in self.re_style_dict:
                    find = self.re_style_dict[opt][0].search(i)
                    if find:
                        self.styles_dict[style_name][self.re_style_dict[opt][1]] = find.groups()[0]
                    elif '}' in i:
                        style_flag = 0
                        break
        #for x in self.styles_dict:
            #print '____________________________'
            #print repr(x), self.styles_dict[x]

    def line(self, s, ind):
        config = {}
        re_o = re.compile('x1="([^= ]+)" y1="([^= ]+)" x2="([^= ]+)" y2="([^= ]+)"')
        config = self.prop_from_style(s, config)
        coord = re_o.search(s).groups()
        config['x1'] = coord[0]
        config['y1'] = coord[1]
        config['x2'] = coord[2]
        config['y2'] = coord[3]
        e = "self.c_line(x1 = %(x1)s, y1 = %(y1)s, x2 = %(x2)s, y2 = %(y2)s, width = %(width)s, stipple = %(dash)s, factor_stip = %(factor_stip)s, fill = '%(fill)s', sloy = 1)"
        e = (e % config)

        self.command_list.append(e)

    def rect(self, s, ind):
        config = {}
        re_o = re.compile('x="([^= ]+)" y="([^= ]+)" width="([^= ]+)" height="([^= ]+)"')
        config = self.prop_from_style(s, config)
        coord = [float(x) for x in re_o.search(s).groups()]
        config['x1'] = coord[0]
        config['y1'] = coord[1]
        config['x2'] = coord[0]+coord[2]
        config['y2'] = coord[1]+coord[3]
        
        e1 = "self.c_line(x1 = %(x1)s, y1 = %(y1)s, x2 = %(x2)s, y2 = %(y1)s, width = %(width)s, stipple = %(dash)s, factor_stip = %(factor_stip)s, fill = '%(fill)s', sloy = 1)"
        e2 = "self.c_line(x1 = %(x1)s, y1 = %(y1)s, x2 = %(x1)s, y2 = %(y2)s, width = %(width)s, stipple = %(dash)s, factor_stip = %(factor_stip)s, fill = '%(fill)s', sloy = 1)"
        e3 = "self.c_line(x1 = %(x1)s, y1 = %(y2)s, x2 = %(x2)s, y2 = %(y2)s, width = %(width)s, stipple = %(dash)s, factor_stip = %(factor_stip)s, fill = '%(fill)s', sloy = 1)"
        e4 = "self.c_line(x1 = %(x2)s, y1 = %(y1)s, x2 = %(x2)s, y2 = %(y2)s, width = %(width)s, stipple = %(dash)s, factor_stip = %(factor_stip)s, fill = '%(fill)s', sloy = 1)"
        ee = [e %config for e in [e1, e2, e3, e4]]
        self.command_list.extend(ee)
        

    def circle(self, s, ind):
        config = {}
        re_o = re.compile('cx="([^= ]+)" cy="([^= ]+)" r="([^= ]+)"')
        config = self.prop_from_style(s, config)
        
        coord = re_o.search(s).groups()
        config['cx'] = coord[0]
        config['cy'] = coord[1]
        config['r'] = coord[2]
        e = "self.c_circle(x0 = %(cx)s, y0 = %(cy)s, R = %(r)s, width = %(width)s, fill = '%(fill)s', sloy = 1)"
        e = (e % config)

        self.command_list.append(e)    


    def arc(self, s, ind):
        config = {}
        re_o = re.compile('d="M([^," ]+)[, ]?([^," ]+)[, ]?A([^," ]+)[, ?]([^," ]+) 0 0[, ]?([^," ]+)[, ]?([^," ]+)[, ]?([^," ]+)')
        config = self.prop_from_style(s, config)
        
        try:
            coord = re_o.search(s).groups()
        except:
            print (s)
            return
        config['xr2'] = coord[0]
        config['yr2'] = coord[1]
        config['r'] = coord[2]
        config['sf'] = float(coord[4])
        config['xr1'] = coord[5]
        config['yr1'] = coord[6]
        if coord[2] != coord[3]:
            return
        
        if config['sf'] == 1:
            sf = -1
        else:
            sf = 1
        xr1 = float(config['xr1'])
        yr1 = float(config['yr1'])
        xr2 = float(config['xr2'])
        yr2 = float(config['yr2'])
        r = float(config['r'])
        d1 = sqrt((xr1-xr2)**2 + (yr1-yr2)**2)/2.0
        p0x = (xr1+xr2)/2.0
        p0y = (yr1+yr2)/2.0
        sin = (p0x-xr1)/d1
        cos = (p0y-yr1)/d1
        try:
            d2 = sqrt(r*r-d1*d1)
        except:
            print ('error, bad arc!', r, d1)
            return
        x0 = p0x - d2*cos*sf
        y0 = p0y + d2*sin*sf
        config['x0'] = x0
        config['y0'] = y0
        e = "self.c_arc(x0 = %(x0)s, y0 = %(y0)s, xr1 = %(xr1)s, yr1 = %(yr1)s, xr2 = %(xr2)s, yr2 = %(yr2)s, R = %(r)s, width = %(width)s, fill = '%(fill)s', sloy = 1)"
        e = (e % config)
        self.command_list.append(e)

    def text(self, s, ind):
        config = {}
        re_o = re.compile('x="([^," ]+)" y="([^," ]+)"')
        config = self.prop_from_style(s, config)
        coord = re_o.search(s).groups()
        config['x'] = coord[0]
        config['y'] = coord[1]
        re_font_size = re.compile('font-size="([^="]+)"')
        re_rotate = re.compile('transform="rotate\(([^",]+)[, ]+([^",]+)[, ]+([^",]+)\)"')
        re_Ltext = re.compile('textLength="([^",]+)" lengthAdjust="spacingAndGlyphs"')
        re_text = re.compile('<text.*>(.*)</text>')
        find_size = re_font_size.search(s)
        find_rotate = re_rotate.search(s)
        find_text = re_text.search(s)
        find_Ltext = re_Ltext.search(s)
        config['text'] = find_text.groups()[0].decode('utf-8')
        config['s_s'] = 1.3
        if find_size:
            config['size'] = find_size.groups()[0]
            if 'px' in config['size']:
                config['size'] = -float(config['size'][0:-2])
            elif 'mm' in config['size']:
                ###
                config['size'] = -float(config['size'][0:-2])
            else:
                config['size'] = -float(config['size'])
        if find_rotate:
            config['angle'] = radians(-float(find_rotate.groups()[0]))
        else:
            config['angle'] = 0.0
        if find_Ltext:
            Ltext = float(find_Ltext.groups()[0])
            print config['size']
            print len(config['text'])
            if len(config['text']) == 0:
                return
            config['s_s'] = (Ltext + -float(config['size'])/4.0)/(len(config['text'])*2.0*-float(config['size'])/4.0)                                                                     
                                                                
            
        if config['angle'] == -0.0:
            config['angle'] = 0.0
        ### Надо будет доделать
        #config['s_s'] = 1.2
        config['w_text'] = 1
        ###
        
        e = "self.c_text(x = %(x)s, y = %(y)s, text = u'%(text)s', fill = '%(fill)s', angle = %(angle)s, size = %(size)s, anchor = 'sw', sloy = 1, s_s = %(s_s)s, w_text = %(w_text)s, font = 'Simular TXT')"
        e = (e % config)

        self.command_list.append(e)

    def dim(self, s, ind):
        config = {}
        re_line = re.compile('x1="([^= ]+)" y1="([^= ]+)" x2="([^= ]+)" y2="([^= ]+)"')
        re_text_xy = re.compile('x="([^," ]+)" y="([^," ]+)"')
        re_font_size = re.compile('font-size="([^="]+)"')
        re_rotate = re.compile('transform="rotate\(([^",]+)[, ]+([^",]+)[, ]+([^",]+)\)"')
        re_text = re.compile('<text.*>(.*)</text>')
        re_Ltext = re.compile('textLength="([^",]+)" lengthAdjust="spacingAndGlyphs"')
        line = 0
        ind+=1
        for ss in self.file[ind:]:
            ind += 1
            if '</g>' in ss:
                break
            for x in self.re_dict:
                if self.re_dict[x][0].search(ss):
                    if x == 'line':
                        line += 1
                        config = self.prop_from_style(ss, config)
                        coord = re_line.search(ss).groups()
                        config[('line_'+str(line)+'_x1')] = coord[0]
                        config[('line_'+str(line)+'_y1')] = coord[1]
                        config[('line_'+str(line)+'_x2')] = coord[2]
                        config[('line_'+str(line)+'_y2')] = coord[3]
                    elif x == 'text':
                        config = self.prop_from_style(ss, config)
                        coord = re_text_xy.search(ss).groups()
                        config['x'] = float(coord[0])
                        config['y'] = float(coord[1])
                        find_size = re_font_size.search(ss)
                        find_rotate = re_rotate.search(ss)
                        find_text = re_text.search(ss)
                        find_Ltext = re_Ltext.search(ss)
                        config['text'] = find_text.groups()[0].decode('utf-8')
                        
                        if find_size:
                            config['size'] = find_size.groups()[0]
                            if 'px' in config['size']:
                                config['size'] = -float(config['size'][0:-2])
                            elif 'mm' in config['size']:
                                ### Разобраться с mm!
                                config['size'] = -float(config['size'][0:-2])
                            else:
                                config['size'] = -float(config['size'])
                        if find_rotate:
                            config['angle'] = radians(-float(find_rotate.groups()[0]))
                        else:
                            config['angle'] = 0.0
                        if find_Ltext:
                            config['Ltext'] = float(find_Ltext.groups()[0])           
                            config['s_s'] = (config['Ltext'] + -float(config['size'])/4.0)/(len(config['text'])*2.0*-float(config['size'])/4.0)  
                        
        
        config['text_place'] = None
               
        config['vr_s'] = 0.0
        config['vv_s'] = 2.0
        config['arrow_s'] = 4.0
        config['type_arrow'] = 'Arrow'
        
        config['w_text'] = 1.0
        config['x1'] = float(config['line_1_x1'])
        config['y1'] = float(config['line_1_y1'])
        config['x2'] = float(config['line_2_x1'])
        config['y2'] = float(config['line_2_y1'])    
        
            
        if re.compile('<g class="DimL".*>').search(s):
            e = self.dimL(line, config)
        else:
            e = self.dimR(line, config)
        if e:
            self.command_list.append(e)

    def dimL(self, line, config):
        
        config['x3'] = float(config['line_3_x1'])
        config['y3'] = float(config['line_3_y1'])
        x = max(config['x1'], config['x2'])
        xm = min(config['x1'], config['x2'])
        y = max(config['y1'], config['y2'])
        ym = min(config['y1'], config['y2'])
        
        if 3 < line < 6:
            config['type_arrow'] = 'Arch'
            config['arrow_s'] = abs(float(config['arrow_1_x1'])-float(config['arrow_1_x2']))/2.0
        elif line == 7:
            if config['ort'] == 'horizontal':
                config['arrow_s'] = abs(float(config['arrow_1_y1'])-float(config['arrow_1_y1']))
            else:
                config['arrow_s'] = abs(float(config['arrow_1_x1'])-float(config['arrow_1_x1']))
                
        
        if config['angle'] == pi/2:
            config['ort'] = 'horizontal'
            config['y'] += config['Ltext']/2.0
            if 's_s' in config:
                pass
                #config['y'] += config['Ltext']/2.0
            else:
                config['s_s'] = 1.3
                
            if ym<config['y']<y:
                #if config['y'] == abs(config['y1'] - config['y2']):
                if abs(config['y'] - abs(config['y1'] + config['y2'])/2) < self.par.min_e:
                    config['text_change'] = 1
                else:
                    config['text_change'] = 3
            elif abs(config['y'] - (ym - config['arrow_s'] - config['Ltext']/2.0)) < self.par.min_e:
                config['text_change'] = 1
            else:
                config['text_change'] = 2
                
            config['s'] = abs(float(config['x']) - float(config['x3']))
            config['vv_s'] = abs(float(config['line_3_x1'])-float(config['line_1_x2']))
            #config['vr_s'] = abs(float(config['line_3_y1'])-float(config['line_1_y2']))
            vr_s1 = abs(config['line_3_y2']-config['line_1_y2'])
            vr_s2 = abs(config['line_3_y1']-config['line_2_y2'])
            config['vr_s'] = min(vr_s1, vr_s2)

            config['text_place'] = [float(config['x']), float(config['y']), 'vert']
            try:
                if config['text'] == round(abs(float(config['line_1_y1'])-float(config['line_2_y1'])), 2):
                    config['text'] = None
            except ValueError:
                pass               
        else:
            
            config['ort'] = 'vertical'
            config['x'] += config['Ltext']/2.0
            if 's_s' in config:
                pass
                #config['x'] += config['Ltext']/2.0
            else:
                config['s_s'] = 1.3
                
            if xm<config['x']<x:
                #if config['x'] == abs(config['x1'] - config['x2']):
                if abs(config['x'] - abs(config['x1'] + config['x2'])/2) < self.par.min_e:
                    config['text_change'] = 1
                else:
                    config['text_change'] = 3
            elif abs(config['x'] - (xm - config['arrow_s'] - config['Ltext']/2.0)) < self.par.min_e:
                config['text_change'] = 1
            else:
                config['text_change'] = 2
            
            config['s'] = abs(float(config['y']) - float(config['y3']))
            config['vv_s'] = abs(float(config['line_3_y1'])-float(config['line_1_y2']))
            vr_s1 = abs(config['line_3_x2']-config['line_1_x2'])
            vr_s2 = abs(config['line_3_x1']-config['line_2_x2'])
            vr_s3 = abs(config['line_3_x1']-config['line_1_x2'])
            vr_s4 = abs(config['line_3_x2']-config['line_2_x2'])
            config['vr_s'] = min(vr_s1, vr_s2, vr_s3, vr_s4)#abs(float(config['line_3_x1'])-float(config['line_1_x2']))
            
            config['text_place'] = [float(config['x']), float(config['y']), 'hor']
            try:
                if float(config['text']) == round(abs(float(config['line_1_x1'])-float(config['line_2_x1'])), 2):
                    config['text'] = None
            except ValueError:
                pass
        
          
        #e = "self.dim(x1 = %(x1)s, y1 = %(y1)s, x2 = %(x2)s, y2 = %(y2)s, x3 = %(x3)s, y3 = %(y3)s, text = u'%(text)s', fill = '%(fill)s', ort = '%(ort)s', size = %(size)s, text_change = '%(text_change)s', text_place = %(text_place)s, sloy = 1, s = %(s)s, vr_s = %(vr_s)s, vv_s = %(vv_s)s, arrow_s = %(arrow_s)s, type_arrow = '%(type_arrow)s', s_s = %(s_s)s, w_text = %(w_text)s, font = 'Simumar TXT')"
        return config

    def dimR(self, line, config):
        if line > 2:
            config['x3'] = float(config['line_3_x1'])
            config['y3'] = float(config['line_3_y1'])
        config['x2'], config['y2'] = intersection_stright(float(config['line_1_x1']),float(config['line_1_y1']), float(config['line_1_x2']),float(config['line_1_y2']), float(config['line_2_x1']),float(config['line_2_y1']), float(config['line_2_x2']),float(config['line_2_y2']))
        config['s_s'] = 1.3
        config['s'] = 1.3
        e = "self.dimR(x1 = %(x1)s, y1 = %(y1)s, x2 = %(x2)s, y2 = %(y2)s, text = u'%(text)s', fill = '%(fill)s', size = %(size)s, sloy = 1, s = %(s)s, vr_s = %(vr_s)s, arrow_s = %(arrow_s)s, type_arrow = '%(type_arrow)s', s_s = %(s_s)s, w_text = %(w_text)s, font = 'Simumar TXT')"
        return (e % config)
            
    def prop_from_style(self, s, config):
        re_o_class = re.compile('class="([^= ]+)" ')
        re_o_dash = re.compile('[-+]?([0-9]*\.[0-9]+|[0-9]+)[, ]?')
        o_class = re_o_class.search(s)
        if o_class:
            
            o_style = o_class.groups()[0]
            if o_style in self.styles_dict:
                
                for opt in self.styles_dict[o_style]:
                    if opt in ('fill', 'width', 'dash'):

                        if opt == 'fill':
                            config['color'] = self.styles_dict[o_style][opt]
                            continue
                            
                        if opt == 'dash':
                            
                            e = re_o_dash.findall(self.styles_dict[o_style][opt])
                            e = [float(x) for x in e]
                            for line_type in self.par.stipples:
                                stipple = self.par.stipples[line_type]
                                
                                if stipple and len(stipple) == len(e):
                                    config['factor_stipple'] = e[0]/stipple[0]
                                    config[opt] = stipple
                                                                
                            continue
                        config[opt] = self.styles_dict[o_style][opt]
                    
        for opt in self.re_style_dict:
            
                
            find = self.re_style_dict[opt][0].search(s)
            if find:
                if self.re_style_dict[opt][1] == 'dash':
                    
                    e = re_o_dash.findall(find.groups()[0])
                    e = [float(x) for x in e]
                    
                    
                    for line_type in self.par.stipples:
                        stipple = self.par.stipples[line_type]
                        
                        if stipple and len(stipple) == len(e):
                            config['factor_stipple'] = e[0]/stipple[0]
                            config[self.re_style_dict[opt][1]] = stipple
                                  
                    continue
                config[self.re_style_dict[opt][1]] = find.groups()[0]

        if 'color' not in config or config['color'] == 'black':
            config['color'] = 'white'
        if 'width' not in config or not float(config['width']):
            config['width'] = 2
        if 'dash' not in config:
            config['dash'] = None
            config['factor_stip'] = 200.0
        return config

def get_object_elements(g, drawing_h):
    dict_prop = {}
    elements = g.getchildren()
    line_num = 0
    arrow_num = 0
    for el in elements:
        el_attrib = el.attrib
        if el.tag == '{http://www.w3.org/2000/svg}line':

            if line_num < 3:
                line_num += 1
                dict_prop.update({
                    'line_'+str(line_num)+'_x1' : float(el_attrib['x1']),
                    'line_'+str(line_num)+'_y1' : drawing_h - float(el_attrib['y1']),
                    'line_'+str(line_num)+'_x2' : float(el_attrib['x2']),
                    'line_'+str(line_num)+'_y2' : drawing_h - float(el_attrib['y2']),
                    })
            else:
                arrow_num += 1
                dict_prop.update({
                    'arrow_'+str(arrow_num)+'_x1' : float(el_attrib['x1']),
                    'arrow_'+str(arrow_num)+'_y1' : drawing_h - float(el_attrib['y1']),
                    'arrow_'+str(arrow_num)+'_x2' : float(el_attrib['x2']),
                    'arrow_'+str(arrow_num)+'_y2' : drawing_h - float(el_attrib['y2']),
                    })
                
        elif el.tag == '{http://www.w3.org/2000/svg}text':

            dict_prop['x'] = float(el_attrib['x'])
            dict_prop['y'] = drawing_h - float(el_attrib['y'])
            
            dict_prop['layer'] = el_attrib['class'][2:]

            #from_style = self.styles_dict[config['layer']]
            #config.update(from_style)
            dict_prop['text'] = el.text.decode('utf-8')
            dict_prop['text_s_s'] = 1.3
            dict_prop['text_size'] = el_attrib['font-size']
            if 'px' in dict_prop['text_size']:
                dict_prop['text_size'] = float(dict_prop['text_size'][0:-2])
            elif 'mm' in dict_prop['text_size']:
                dict_prop['text_size'] = float(dict_prop['text_size'][0:-2])
            else:
                dict_prop['text_size'] = float(dict_prop['text_size'])

            if 'transform' in el_attrib:
                re_rotate = re.compile('rotate\(([^",]+)[, ]+([^",]+)[, ]+([^",]+)\)')
                find_rotate = re_rotate.search(el_attrib['transform'])
                dict_prop['angle'] = radians(-float(find_rotate.groups()[0]))
            else:
                dict_prop['angle'] = 0.0

            dict_prop['anchor'] = 'sw'
            dict_prop['text_w'] = 1
            dict_prop['color'] = [255, 255, 255]
            dict_prop['text_font'] = 'TXT'
            dict_prop['Ltext'] = float(el_attrib['textLength'])
    dict_prop['num_arrows'] = arrow_num+line_num
    return dict_prop
            
                

    
