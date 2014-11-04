# -*- coding: utf-8; -*-
from get_conf import get_line_coord, get_arc_coord, get_dimR_conf
from math import sqrt
class saver:
    def __init__(self, parent):
        self.parent = parent
        self.AL = self.parent.ALLOBJECT.copy()
        self.write_list = []
        self.config_dict = {}
        dxf = self.parent.s_dxf
        def dxf_colorer(color):
            color_tab = {"white":7,
                         "light blue":4,
                         "blue":5,
                         "green":96,
                         "gray":8,
                         "black":7,
                         "yellow":2,
                         "orange":30,
                         "red":10}
            return color_tab[color]
        
        for obj in self.AL:
            if obj == 'trace':
                continue
            if obj == 'trace_o':
                continue
            if obj[0] == 'L':
                e, config = self.parent.ALLOBJECT[obj]['class'].save(dxf)
                '''
                coord = get_line_coord(obj, self.parent)
                config = {'x1' : coord[0],#Взять свойства из канваса
                          'y1' : coord[1],
                          'x2' : coord[2],
                          'y2' : coord[3],
                          'fill' : self.AL[obj]['fill'],#Взять свойства из ALLOBJECT
                          'width' : self.AL[obj]['width'],
                          'sloy' : self.AL[obj]['sloy'],
                          'stipple' : self.AL[obj]['stipple'],
                          'factor_stip' : self.AL[obj]['factor_stip']}
                e = "self.c_line(x1 = %(x1)s, y1 = %(y1)s, x2 = %(x2)s, y2 = %(y2)s, width = %(width)s, stipple = %(stipple)s, fill = '%(fill)s', sloy = %(sloy)s)"
                e = (e % config)
                if dxf:
                    config['fill'] = dxf_colorer(config['fill'])
                '''
            elif obj[0] == 'c':
                find = self.AL[obj]['id']
                for i in find:
                    tag = self.AL[obj]['id'][i]
                    if 'cir' in tag:
                        coord = self.parent.c.coords(i)
                xc = (coord[0]+coord[2])/2.0
                yc = (coord[1]+coord[3])/2.0
                
                config = {'x0' : xc,#Взять свойства из канваса
                          'y0' : yc,
                          'fill' : self.AL[obj]['fill'],#Взять свойства из ALLOBJECT
                          'width' : self.AL[obj]['width'],
                          'sloy' : self.AL[obj]['sloy'],
                          'R':self.AL[obj]['R']}
                e = "self.c_circle(x0 = %(x0)s, y0 = %(y0)s, R = %(R)s, width = %(width)s, fill = '%(fill)s', sloy = %(sloy)s)"
                e = (e % config)
                if dxf:
                    config['fill'] = dxf_colorer(config['fill'])
                

            elif obj[0] == 'a':
                find = self.AL[obj]['id']
                for i in find:
                    tag = self.AL[obj]['id'][i]
                    if 'a' in tag:
                        coord = self.parent.c.coords(i)
                        start = float(self.parent.c.itemcget(i, 'start'))
                        extent = float(self.parent.c.itemcget(i, 'extent'))
                x0, y0, xr1, yr1, xr2, yr2 = get_arc_coord(coord[0], coord[1], coord[2], coord[3], start, extent)
                
                config = {'x0' : x0,#Взять свойства из канваса
                          'y0' : y0,
                          'xr1' : xr1,
                          'yr1' : yr1,
                          'xr2' : xr2,
                          'yr2' : yr2,
                          'fill' : self.AL[obj]['fill'],#Взять свойства из ALLOBJECT
                          'width' : self.AL[obj]['width'],
                          'start' : self.AL[obj]['start'],
                          'extent' : self.AL[obj]['extent'],
                          'sloy' : self.AL[obj]['sloy'],
                          'R':self.AL[obj]['R']}
                e = "self.c_arc(x0 = %(x0)s, y0 = %(y0)s, xr1 = %(xr1)s, yr1 = %(yr1)s, xr2 = %(xr2)s, yr2 = %(yr2)s, width = %(width)s, fill = '%(fill)s', sloy = %(sloy)s)"
                e = (e % config)
                if dxf:
                    config['fill'] = dxf_colorer(config['fill'])
                
            elif obj[0] == 'r':
                x1, y1, x2, y2, size, fill, text, sloy, s, vr_s, arrow_s, type_arrow, s_s_dim, w_text_dim, font_dim, R = get_dimR_conf(obj, self.parent)
                config = {'x1' : x1,
                          'y1' : y1,
                          'x2' : x2,
                          'y2' : y2,                          
                          'size' : size,
                          'fill' : fill,
                          'text' : text,
                          'sloy' : sloy,                          
                          's' : s,
                          'vr_s' : vr_s,
                          'arrow_s' : arrow_s,
                          'type_arrow' : type_arrow,
                          's_s_dim' : s_s_dim,
                          'w_text_dim' : w_text_dim,
                          'font_dim' : font_dim,
                          'R':R,
                          'angle':self.AL[obj]['angle']}

                lines_coord = self.coord_dim_lines(obj, config, dxf, 1)
                config.update(lines_coord)
                if config['text'] in ('None', None):
                    config['dim_distanse'] = int(format(R, '.0f'))
                else:
                    config['dim_distanse'] = config['text']
                e = "self.dimR(x1 = %(x1)s, y1 = %(y1)s, x2 = %(x2)s, y2 = %(y2)s, text = u'%(text)s', Rn = %(R)s, fill = '%(fill)s', size = %(size)s, sloy = %(sloy)s, s = %(s)s, vr_s = %(vr_s)s, arrow_s = %(arrow_s)s, type_arrow = '%(type_arrow)s', s_s = %(s_s_dim)s, w_text = %(w_text_dim)s, font = '%(font_dim)s')"
                e = (e % config)
                
            elif obj[0] == 'd':
              
                line1 = self.parent.get_snap_line(obj)[0]
                line2 = self.parent.get_snap_line(obj)[1]
                line3 = self.parent.get_snap_line(obj)[2]
                coord_list = map(lambda i: self.parent.c.coords(i), [line1, line2, line3])
                config = {'x1' : coord_list[0][0],
                          'y1' : coord_list[0][1],
                          'x2' : coord_list[1][0],
                          'y2' : coord_list[1][1],
                          'x3' : coord_list[2][0],
                          'y3' : coord_list[2][1],
                          'ort' : self.AL[obj]['ort'],
                          'size' : self.AL[obj]['size'],
                          'fill' : self.AL[obj]['fill'],
                          'text' : self.AL[obj]['text'],
                          'sloy' : self.AL[obj]['sloy'],
                          'text_change' : self.AL[obj]['text_change'],
                          's' : self.AL[obj]['s'],
                          'vr_s' : self.AL[obj]['vr_s'],
                          'vv_s' : self.AL[obj]['vv_s'],
                          'arrow_s' : self.AL[obj]['arrow_s'],
                          'type_arrow' : self.AL[obj]['type_arrow'],
                          's_s_dim' : self.AL[obj]['s_s_dim'],
                          'w_text_dim' : self.AL[obj]['w_text_dim'],
                          'font_dim' : self.AL[obj]['font_dim']}
                
                if config['text_change'] in ('online3', 'changed', 'online3_m_l'):
                    text_lines, priv_line, text_place = self.parent.dim_text_place(obj)
                else:
                    text_change = 'unchange'
                    text_place = None
                ###if dxf:
                if dxf:
                    config['fill'] = dxf_colorer(config['fill'])
                    yf = -1
                else:
                    yf = 1
                lines_coord = self.coord_dim_lines(obj, config, dxf, yf)
                config.update(lines_coord)
                if config['text'] in ('None', None):
                    if config['ort'] == "horizontal":
                        config['dim_distanse'] = int(format(abs(config['y1'] - config['y2']), '.0f'))                            
                    else:
                        config['dim_distanse'] = int(format(abs(config['x1'] - config['x2']), '.0f'))
                else:
                    config['dim_distanse'] = config['text']
                '''
                lines = self.AL[obj]['id']#self.parent.c.find_withtag(obj)
                num_lines = 0
                num_arrows = 0                   
                for i in lines:
                    tag = self.AL[obj]['id'][i]#self.parent.c.gettags(i)
                    if ('priv' in tag) and ('dim_text' not in tag):
                        num_lines += 1
                        coord = self.parent.c.coords(i)
                        lines_coord.update({'line_'+str(num_lines)+'_x1': coord[0],
                                            'line_'+str(num_lines)+'_y1': yf*coord[1],
                                            'line_'+str(num_lines)+'_x2': coord[2],
                                            'line_'+str(num_lines)+'_y2': yf*coord[3]})
                        
                    elif tag == ('line',):
                        num_arrows += 1
                        
                        coord = self.parent.c.coords(i)
                        lines_coord.update({'arrow_'+str(num_arrows)+'_x1': coord[0],
                                            'arrow_'+str(num_arrows)+'_y1': yf*coord[1],
                                            'arrow_'+str(num_arrows)+'_x2': coord[2],
                                            'arrow_'+str(num_arrows)+'_y2': yf*coord[3]})
                        
                    elif ('dim_text_priv' in tag):
                        coord = self.parent.c.coords(i)
                        x1 = coord[0]
                        y1 = coord[1]
                        x2 = coord[2]
                        y2 = coord[3]
                        if dxf:
                            if config['ort'] == "horizontal":
                                y = (y1+y2)/2.0
                                yy = y
                                x = coord_list[2][0]
                                xx = x1 + config['size']/2.0
                            else:
                                x = (x1+x2)/2.0
                                xx = x
                                y = coord_list[2][1]
                                yy = y1 + config['size']/2.0
                        else:
                            x = x1
                            xx = x2
                            y = y1
                            yy = y2
                            
                        lines_coord.update({'text_x': x,
                                            'text_y': yf*y,
                                            'text_xx': xx,
                                            'text_yy': yf*yy})
                '''        
                if config['ort'] == "horizontal":
                    config.update({'arrow_point1_x': coord_list[2][0],
                                    'arrow_point1_y': yf*coord_list[0][1],
                                    'arrow_point2_x': coord_list[2][0],
                                    'arrow_point2_y': yf*coord_list[1][1]})
                    
                    
                    config.update({'angle': 90.0,
                                    'angle_arrow1': 90.0,
                                    'angle_arrow2': 270.0})
                    if config['type_arrow'] == 'Arrow':
                        config.update({'arrow_5_x': coord_list[2][0],
                                    'arrow_5_y': lines_coord['arrow_1_y1'],
                                    'arrow_6_x': coord_list[2][0],
                                    'arrow_6_y': lines_coord['arrow_3_y1']})
                else:
                    config.update({'arrow_point1_x': coord_list[0][0],
                                    'arrow_point1_y': yf*coord_list[2][1],
                                    'arrow_point2_x': coord_list[1][0],
                                    'arrow_point2_y': yf*coord_list[2][1],
                                    'angle': 0.0,
                                    'angle_arrow1': 180.0,
                                    'angle_arrow2': 0.0})
                    if config['type_arrow'] == 'Arrow':
                        config.update({'arrow_5_y': yf*coord_list[2][1],   
                                    'arrow_5_x': lines_coord['arrow_1_x1'],
                                    'arrow_6_y': yf*coord_list[2][1],
                                    'arrow_6_x': lines_coord['arrow_3_x1']})
                if config['text_change'] != 'online3':
                    config.update({'line_3_x1': config['arrow_point1_x'],
                                    'line_3_x2': config['arrow_point2_x'],
                                    'line_3_y1': config['arrow_point1_y'],
                                    'line_3_y2': config['arrow_point2_y']})
                        
                config['text_place'] = text_place
                if lines_coord:
                    config.update(lines_coord)
                e = "self.dim(x1 = %(x1)s, y1 = %(y1)s, x2 = %(x2)s, y2 = %(y2)s, x3 = %(x3)s, y3 = %(y3)s, text = u'%(text)s', fill = '%(fill)s', ort = '%(ort)s', size = %(size)s, text_change = '%(text_change)s', text_place = %(text_place)s, sloy = %(sloy)s, s = %(s)s, vr_s = %(vr_s)s, vv_s = %(vv_s)s, arrow_s = %(arrow_s)s, type_arrow = '%(type_arrow)s', s_s = %(s_s_dim)s, w_text = %(w_text_dim)s, font = '%(font_dim)s')"
                e = (e % config)
                
            elif obj[0] == 't':
            
                line = self.parent.get_snap_line(obj)[0]
                
                coord = self.parent.c.coords(line)
                Ltext = sqrt((coord[0]-coord[2])**2+(coord[1]-coord[3])**2)
                config = {'x' : coord[0],
                          'y' : coord[1],
                          'size' : self.AL[obj]['size'],
                          'fill' : self.AL[obj]['fill'],
                          'sloy' : self.AL[obj]['sloy'],
                          'text' : self.AL[obj]['text'],
                          'angle' : self.AL[obj]['angle'],
                          'anchor' : self.AL[obj]['anchor'],
                          's_s' : self.AL[obj]['s_s'],
                          'w_text' : self.AL[obj]['w_text'],
                          'Ltext' : Ltext,
                          'font' : self.AL[obj]['font']}
                
                e = """self.c_text(x = %(x)s, y = %(y)s, text = u"%(text)s", fill = '%(fill)s', angle = %(angle)s, size = %(size)s, anchor = '%(anchor)s', sloy = %(sloy)s, s_s = %(s_s)s, w_text = %(w_text)s, font = '%(font)s')"""
                e = (e % config)
                if dxf:
                    config['fill'] = dxf_colorer(config['fill'])
                
                
            if dxf:
                self.config_dict[obj] = config
            else:
                self.config_dict[obj] = config
                self.write_list.append(e)
                
    def coord_dim_lines(self, obj, config, dxf, yf):
        lines_coord = {}
        lines = self.AL[obj]['id']
        num_lines = 0
        num_arrows = 0
        for i in lines:
            tag = self.AL[obj]['id'][i]
            if ('priv' in tag) and ('dim_text' not in tag):
                num_lines += 1
                coord = self.parent.c.coords(i)
                lines_coord.update({'line_'+str(num_lines)+'_x1': coord[0],
                                    'line_'+str(num_lines)+'_y1': yf*coord[1],
                                    'line_'+str(num_lines)+'_x2': coord[2],
                                    'line_'+str(num_lines)+'_y2': yf*coord[3]})
                
            elif tag == ('line',):
                num_arrows += 1
                
                coord = self.parent.c.coords(i)
                lines_coord.update({'arrow_'+str(num_arrows)+'_x1': coord[0],
                                    'arrow_'+str(num_arrows)+'_y1': yf*coord[1],
                                    'arrow_'+str(num_arrows)+'_x2': coord[2],
                                    'arrow_'+str(num_arrows)+'_y2': yf*coord[3]})
                
            elif ('dim_text_priv' in tag):
                coord = self.parent.c.coords(i)
                x1 = coord[0]
                y1 = coord[1]
                x2 = coord[2]
                y2 = coord[3]
                Ltext = sqrt((x1-x2)**2+(y1-y2)**2)
                ### Этот параметр не относится к координатам - это длина линии привязки текста!
                lines_coord['Ltext'] = Ltext
                if dxf:
                    if config['ort'] == "horizontal":
                        y = (y1+y2)/2.0
                        yy = y
                        x = coord_list[2][0]
                        xx = x1 + config['size']/2.0
                    else:
                        x = (x1+x2)/2.0
                        xx = x
                        y = coord_list[2][1]
                        yy = y1 + config['size']/2.0
                else:
                    x = x1
                    xx = x2
                    y = y1
                    yy = y2
                    
                lines_coord.update({'text_x': x,
                                    'text_y': yf*y,
                                    'text_xx': xx,
                                    'text_yy': yf*yy})
        return lines_coord
