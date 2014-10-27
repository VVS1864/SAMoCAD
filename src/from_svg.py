# -*- coding: utf-8; -*-
from math import pi, sqrt, radians, ceil
import re
from calc import min_distanse, intersection_stright
class SVGopener:
    def __init__(self, _file, par):
        self.par = par
        self.command_list = []
        self.file = _file.split('\n')
        self.styles_dict = {}
        self.config_dict = {}
        if re.compile('<svg.*>').search(self.file[0]):
            self.svg_file()
        else:
            print ('No SVG file')

    def svg_file(self):
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
        
        if config['angle'] == pi/2:
            config['ort'] = 'horizontal'
            if 's_s' in config:
                config['y'] -= config['Ltext']/2.0
            else:
                config['s_s'] = 1.3
                
            if ym<config['y']<y:
                if config['y'] == abs(config['y1'] - config['y2']):
                    config['text_change'] = 'unchange'
                else:
                    config['text_change'] = 'online3_m_l'
            else:
                config['text_change'] = 'online3'
                
            config['s'] = abs(float(config['x']) - float(config['x3']))
            config['vv_s'] = abs(float(config['line_3_x1'])-float(config['line_1_x2']))

            config['text_place'] = [float(config['x']), float(config['y']), 'vert']
            try:
                if config['text'] == round(abs(float(config['line_1_y1'])-float(config['line_2_y1'])), 2):
                    config['text'] = None
            except ValueError:
                pass               
        else:               
            config['ort'] = 'vertical'
            if 's_s' in config:
                config['x'] += config['Ltext']/2.0
            else:
                config['s_s'] = 1.3
                
            if xm<config['x']<x:
                if config['x'] == abs(config['x1'] - config['x2']):
                    config['text_change'] = 'unchange'
                else:
                    config['text_change'] = 'online3_m_l'
            else:
                config['text_change'] = 'online3'
            
            config['s'] = abs(float(config['y']) - float(config['y3']))
            config['vv_s'] = abs(float(config['line_3_y1'])-float(config['line_1_y2']))
            
            config['text_place'] = [float(config['x']), float(config['y']), 'hor']
            try:
                if float(config['text']) == round(abs(float(config['line_1_x1'])-float(config['line_2_x1'])), 2):
                    config['text'] = None
            except ValueError:
                pass
        if 3 < line < 6:
            config['type_arrow'] = 'Arch'
            config['arrow_s'] = abs(float(config['line_4_x1'])-float(config['line_4_x2']))/2.0
        elif line == 7:
            if config['ort'] == 'horizontal':
                config['arrow_s'] = abs(float(config['line_4_y1'])-float(config['line_4_y2']))
            else:
                config['arrow_s'] = abs(float(config['line_4_x1'])-float(config['line_4_x2']))
          
        e = "self.dim(x1 = %(x1)s, y1 = %(y1)s, x2 = %(x2)s, y2 = %(y2)s, x3 = %(x3)s, y3 = %(y3)s, text = u'%(text)s', fill = '%(fill)s', ort = '%(ort)s', size = %(size)s, text_change = '%(text_change)s', text_place = %(text_place)s, sloy = 1, s = %(s)s, vr_s = %(vr_s)s, vv_s = %(vv_s)s, arrow_s = %(arrow_s)s, type_arrow = '%(type_arrow)s', s_s = %(s_s)s, w_text = %(w_text)s, font = 'Simumar TXT')"
        return (e % config)

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
                        
                        if opt == 'dash':
                            
                            e = re_o_dash.findall(self.styles_dict[o_style][opt])
                            e = [float(x) for x in e]
                            for line_type in self.par.stipples:
                                stipple = self.par.stipples[line_type]
                                
                                if stipple and len(stipple) == len(e):
                                    config['factor_stip'] = e[0]/stipple[0]
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
                            config['factor_stip'] = e[0]/stipple[0]
                            config[self.re_style_dict[opt][1]] = stipple
                                  
                    continue
                config[self.re_style_dict[opt][1]] = find.groups()[0]

        if 'fill' not in config or config['fill'] == 'black':
            config['fill'] = 'white'
        if 'width' not in config or not float(config['width']):
            config['width'] = 2
        if 'dash' not in config:
            config['dash'] = None
            config['factor_stip'] = 200.0
        return config

    
