# -*- coding: utf-8; -*-
from math import pi
class DXFopener:
    def __init__(self, _file):
        self.command_list = []
        self.file = _file.split('\n')
        self.config_dict = {}
        entities_flag = 0
        blocks_flag = 0
        tables_flag = 0
        self.entities_start = None
        self.entities_end = None
        self.blocks_start = None
        self.blocks_end = None
        self.tables_start = None
        self.tables_end = None
        ind = -1
        for i in self.file:
            ind += 1
            s = i
            
            if "ENTITIES" in s:
                self.entities_start = ind
                entities_flag = 1
                
            elif "BLOCKS" in s:
                self.blocks_start = ind
                blocks_flag = 1

            elif "TABLES" in s and 'STYLE' not in s:
                self.tables_start = ind
                tables_flag = 1

            elif "ENDSEC" in s:
                if entities_flag == 1:
                    self.entities_end = ind
                    entities_flag = 0
                    
                elif blocks_flag == 1:
                    self.blocks_end = ind
                    blocks_flag = 0
                    
                elif tables_flag == 1:
                    self.tables_end = ind
                    tables_flag = 0
        if None not in (self.entities_start, self.entities_end, self.blocks_start, self.blocks_end, self.tables_start, self.tables_end):
            
            self.entities = self.file[self.entities_start : (self.entities_end+1)]
            self.blocks = self.file[self.blocks_start : (self.blocks_end+1)]
            self.tables = self.file[self.tables_start : (self.tables_end+1)]
            
            ind = -1
            
            line_flag = 0
            circle_flag = 0
            arc_flag = 0
            text_flag = 0
            dim_flag = 0
            break_flag = 0
            def dxf_colorer(color):
                color_tab = {'256':"white",
                             '7':"white",
                             '4':"light blue",
                             '5':"blue",
                             '96':"green",
                             '8':"gray",
                             '2':"yellow",
                             '30':"orange",
                             '1':"red",
                             '10':"red"}
                if color in color_tab:
                    return color_tab[color]
                else:
                    return "white"

            def widther(width):
                try:
                    int(width)
                except:
                    width = 1
                if width == -1 or (0 < int(width) <= 20):
                    w = 1
                elif 20 < int(width) <= 40:
                    w = 2
                elif 40 < int(width) <= 100:
                    w = 3
                elif 100 < int(width) <= 211:
                    w = 4
                else:
                    w = 1
                return w
            def dasher(dash):
                dash = dash.split()[0]
                dash_flag = 0
                stipples = {'SOLID':None,
                         'DASHED':(1,1),
                         'CENTER':(4,1,1,1),
                         'PHANTOM':(4,1,1,1,1,1)}
                ind = -1
                for t in self.tables:
                    ind +=1
                    i = t.split()
                    if i:
                        i = i[0]
                        if i == dash:
                            dash_flag = 1
                        if dash_flag == 1:
                            if i == '3':
                                d = self.tables[ind+1].upper()
                                for ii in stipples:
                                    if ii in d:
                                        if ii != 'SOLID':
                                            return map(lambda x: x*200,stipples[ii])
                                        else:
                                            return 'None'
                                        
                return None
            def angler(start, extent):
                start = float(start)
                extent = float(extent)
                
                if extent > start:
                    eextent = start 
                    estart = extent
                    eextent -= estart
                else:
                    estart = start - 360.0
                    eextent = -estart + extent
                
                return estart, eextent

            def dim_texter(values):
                dim_block = 0
                t_flag = 0
                a_flag = 0
                val = {'size': None,
                    'type_arrow': 'Arch',
                    'arrow_s': None,
                    's': None,
                    'vv_s': None,
                    'vr_s': '0',
                    's_s_dim': '1.3',
                    'w_text_dim': '1',
                    'font_dim': 'Simular TXT',
                    'text': 'None',
                    'sloy': '1'}
                del_list = []
                for v in val:
                    if v in values:
                        del_list.append(v)
                for d in del_list:
                    del val[d]
                        
                values.update(val)
                
                ind = -1
                dim_style_flag = 0
                reactors = 0
                var_flag = 0
                for s in self.tables:
                    ind += 1
                    i = s.split()
                    if i:
                        i = i[0]
                    else:
                        continue
                    if i == 'DIMSTYLE' and self.tables[ind-1].split()[0] == '0':
                        if dim_style_flag == 1:
                            dim_style_flag = 0
                            reactors = 0
                            var_flag = 0
                            
                        dim_style_flag = 1
                        continue
                    if dim_style_flag == 1:
                        if i == '{ACAD_REACTORS' and self.tables[ind-1].split()[0] == '102':
                            reactors = 1
                            continue
                        if reactors == 1:
                            if i == values['dim_handle'] and self.tables[ind-1].split()[0] == '330':
                                var_flag = 1
                                continue
                            if var_flag == 1:
                                if i == '41':
                                    if values['arrow_s'] == None:
                                        values['arrow_s'] = self.tables[ind+1].split()[0]
                                        
                                elif i == '42':
                                    if values['s'] == None:
                                        values['s'] = self.tables[ind+1].split()[0]
                                    
                                elif i == '44':
                                    if values['vv_s'] == None:
                                        values['vv_s'] = self.tables[ind+1].split()[0]
                                    
                                elif i == '140':
                                    if values['size'] == None:
                                        values['size'] = str(-float(self.tables[ind+1].split()[0]))
                                        
                                    
                                if None not in values.values():
                                    break
                        
                ind = -1
                for s in self.blocks:
                    ind += 1
                    
                    i = s.split()
                    if i:
                        i = i[0]
                    else:
                        continue
                    
                    if i == values['dim_ind'] and self.blocks[ind-1].split()[0] == '2':
                       
                        dim_block = 1
                        continue
                    if dim_block == 1:
                        if i in ('MTEXT', 'TEXT') and self.blocks[ind-1].split()[0] == '0':
                            
                            t_flag = 1
                            continue
                        elif i in ('INSERT', 'SOLID') and self.blocks[ind-1].split()[0] == '0':
                            a_flag = 1
                            if i == 'SOLID':
                                a = 'SOLID'
                                values['type_arrow'] = 'Arrow'
                            else:
                                a = 'INSERT'
                                values['type_arrow'] = 'Arch'
                                
                        elif i == 'ENDBLK' and self.blocks[ind-1].split()[0] == '0':
                            break
                            
                    if a_flag == 1:
                        if a == 'INSERT':
                            if i == '41':
                                values['arrow_s'] = self.blocks[ind+1].split()[0]
                                a_flag = 0
                                continue
                        else:
                            pass
                            '''
                            if values['ort'] == "horizontal":
                                if i == '20':
                                    y1 = -float(self.blocks[ind+1].split()[0])
                                    y2 = values['y2']
                                    y3 = values['y1']
                                    values['arrow_s'] = str(format(min(abs(y1-y2), abs(y1-y3)), '.2f'))
                                    print values['arrow_s']
                                    a_flag = 0
                                    continue
                            else:
                                if i == '10':
                                    x1 = float(self.blocks[ind+1].split()[0])
                                    x2 = values['x2']
                                    x3 = values['x1']
                                    values['arrow_s'] = str(format(min(abs(x1-x2), abs(x1-x3)), '.2f'))
                                    print values['arrow_s']
                                    a_flag = 0
                                    continue
                            '''
                            
                    if t_flag == 1:
                        if i == '40':
                            values['size'] = str(-float(self.blocks[ind+1].split()[0]))
                            t_flag = 0
                            continue
                
                if values['ort'] == "horizontal":
                    if (values['y2']<values['text_y']<values['y1']) or (values['y2']>values['text_y']>values['y1']):
                        values['text_change'] = 'online3_m_l'
                    else:
                        values['text_change'] = 'online3'
                    values['text_x'] = float(values['text_x']) + float(values['size'])/2.0
                    
                else:
                    if (values['x2']<values['text_x']<values['x1']) or (values['x2']>values['text_x']>values['x1']):
                        values['text_change'] = 'online3_m_l'
                    else:
                        values['text_change'] = 'online3'
                    values['text_y'] = values['text_y'] - float(values['size'])/2.0
                values['text_place'] = [values['text_x'], values['text_y']]
                for i in values:
                    if values[i] == None:
                        if i not in ('x1', 'y1', 'x2', 'y2', 'x3', 'y3'):
                            values[i] = str(-float(values['size'])/4.0)
                                
                return values
                         
            
            for s in self.entities:
                ind += 1
                i = s.split()
                if i:
                    i = i[0]
                else:
                    continue
                '''
                if break_flag == 1:
                    line_flag = 0
                    circle_flag = 0
                    arc_flag = 0
                    text_flag = 0
                    dim_flag = 0
                    break_flag = 0
                '''
                    
                if i == "LINE" or (line_flag == 1 and self.entities[ind+1].split() and self.entities[ind+1].split()[0].isupper() and i == '0'):
                    if line_flag == 0:
                        line_flag = 1
                        values = {'fill':None,
                                  'width':None,
                                  'stipple':None,
                                  'x1':None,
                                  'y1':None,
                                  'x2':None,
                                  'y2':None}
                    else:
                        for j in values:
                            if values[j] == None:
                                if j == 'fill':
                                    values[j] = 'white'
                                elif j == 'stipple':
                                    values[j] = 'None'
                                elif j == 'width':
                                    values[j] = '1'
                        if None not in values.values():
                            config = "self.c_line(x1 = %(x1)s, y1 = %(y1)s, x2 = %(x2)s, y2 = %(y2)s, width = %(width)s, stipple = %(stipple)s, fill = '%(fill)s', sloy = 1)"
                            try:
                                config = (config % values)
                            except KeyError:
                                print i
                            else:
                                self.command_list.append(config)
                        line_flag = 0
                        
                            

                if line_flag == 1:
                    
                    if i == '62':
                        values['fill'] = dxf_colorer(self.entities[ind+1])
                    elif i == '370':
                        values['width'] = widther(self.entities[ind+1])
                    elif i == '6':
                        values['stipple'] = dasher(self.entities[ind+1])
                    elif i == '10':
                        values['x1'] = str(float(self.entities[ind+1]))
                    elif i == '20':
                        values['y1'] = str(-float(self.entities[ind+1]))
                    elif i == '11':
                        values['x2'] = str(float(self.entities[ind+1]))
                    elif i == '21':
                        values['y2'] = str(-float(self.entities[ind+1]))

                    '''if None not in values.values():
                        config = "self.c_line(x1 = %(x1)s, y1 = %(y1)s, x2 = %(x2)s, y2 = %(y2)s, width = %(width)s, stipple = %(stipple)s, fill = '%(fill)s', sloy = 1)"
                        config = (config % values)
                        self.command_list.append(config)
                        line_flag = 0
'''
                if i == "CIRCLE" or (circle_flag == 1 and self.entities[ind+1].split() and self.entities[ind+1].split()[0].isupper() and i == '0'):
                    if circle_flag == 0:
                        circle_flag = 1
                        values = {'fill':None,
                                  'width':None,
                                  'x0':None,
                                  'y0':None,
                                  'R':None}
                    else:
                        for j in values:
                            if values[j] == None:
                                if j == 'fill':
                                    values[j] = 'white'
                                elif j == 'width':
                                    values[j] = '1'
                        if None not in values.values():
                            config = "self.c_circle(x0 = %(x0)s, y0 = %(y0)s, R = %(R)s, width = %(width)s, fill = '%(fill)s', sloy = 1)"
                            config = (config % values)
                            self.command_list.append(config)
                        circle_flag = 0

                if circle_flag == 1:
                    if i == '62':
                        values['fill'] = dxf_colorer(self.entities[ind+1])
                    elif i == '370':
                        values['width'] = widther(self.entities[ind+1])
                    elif i == '10':
                        values['x0'] = str(float(self.entities[ind+1]))
                    elif i == '20':
                        values['y0'] = str(-float(self.entities[ind+1]))
                    elif i == '40':
                        values['R'] = str(float(self.entities[ind+1]))
                    '''
                    if None not in values.values():
                        config = "self.c_circle(x0 = %(x0)s, y0 = %(y0)s, R = %(R)s, width = %(width)s, fill = '%(fill)s', sloy = 1)"
                        config = (config % values)
                        self.command_list.append(config)
                        circle_flag = 0
'''
                if i == "ARC" or (arc_flag == 1 and self.entities[ind+1].split() and self.entities[ind+1].split()[0].isupper() and i == '0'):
                    if arc_flag == 0:
                        arc_flag = 1
                        values = {'fill':None,
                                  'width':None,
                                  'x0':None,
                                  'y0':None,
                                  'R':None,
                                  'start':None,
                                  'extent':None}
                    else:
                        for j in values:
                            if values[j] == None:
                                if j == 'fill':
                                    values[j] = 'white'
                                elif j == 'width':
                                    values[j] = '1'
                        if None not in values.values():
                            values['start'], values['extent'] = angler(values['start'], values['extent'])
                            config = "self.c_arc(x0 = %(x0)s, y0 = %(y0)s, R = %(R)s, start = %(start)s, extent = %(extent)s, width = %(width)s, fill = '%(fill)s', sloy = 1)"
                            config = (config % values)
                            self.command_list.append(config)
                        arc_flag = 0

                if arc_flag == 1:
                    if i == '62':
                        values['fill'] = dxf_colorer(self.entities[ind+1])
                    elif i == '370':
                        values['width'] = widther(self.entities[ind+1])
                    elif i == '10':
                        values['x0'] = str(float(self.entities[ind+1]))
                    elif i == '20':
                        values['y0'] = str(-float(self.entities[ind+1]))
                    elif i == '40':
                        values['R'] = str(float(self.entities[ind+1]))
                    elif i == '50':
                        values['start'] = self.entities[ind+1]
                    elif i == '51':
                        values['extent'] = self.entities[ind+1]
                    '''
                    if None not in values.values():
                        values['start'], values['extent'] = angler(values['start'], values['extent'])
                        config = "self.c_arc(x0 = %(x0)s, y0 = %(y0)s, R = %(R)s, start = %(start)s, extent = %(extent)s, width = %(width)s, fill = '%(fill)s', sloy = 1)"
                        config = (config % values)
                        self.command_list.append(config)
                        arc_flag = 0
'''
                if i == "TEXT" or (text_flag == 1 and self.entities[ind+1].split() and self.entities[ind+1].split()[0].isupper() and i == '0'):
                    if text_flag == 0:
                        text_flag = 1
                        values = {'fill':None,
                                  'x':None,
                                  'y':None,
                                  'size':None,
                                  'w_text':None,
                                  's_s':None,
                                  'text':None,
                                  'angle':None}
                    else:
                        for j in values:
                            if values[j] == None:
                                if j == 'fill':
                                    values[j] = 'white'
                                elif j == 'w_text':
                                    values[j] = '3.0'
                                elif j == 's_s':
                                    values[j] = '2.8'
                                elif j == 'angle':
                                    values[j] = '0'
                        if None not in values.values():
                            config = "self.c_text(x = %(x)s, y = %(y)s, text = u'%(text)s', fill = '%(fill)s', angle = %(angle)s, size = %(size)s, anchor = 'sw', sloy = 1, s_s = %(s_s)s, w_text = %(w_text)s, font = 'Simular TXT')"
                            config = (config % values)
                            self.command_list.append(config)
                        text_flag = 0

                if text_flag == 1:
                    if i == '62':
                        values['fill'] = dxf_colorer(self.entities[ind+1])
                    elif i == '10':
                        values['x'] = str(float(self.entities[ind+1]))
                    elif i == '20':
                        values['y'] = str(-float(self.entities[ind+1]))
                    elif i == '40':
                        values['size'] = str(-float(self.entities[ind+1]))
                    elif i == '1' and values['text'] == None:
                        text = self.entities[ind+1].decode("cp1251")
                        if text[-1] == '\r':
                            text = text[0:-1]
                        values['text'] = text
                    elif i == '50':
                        values['angle'] = float(self.entities[ind+1])*pi/180.0
                    elif i == '41':
                        values['w_text'] = float(self.entities[ind+1])*3.0
                        if values['w_text'] >= 1:
                            values['s_s'] = values['w_text']
                        else:
                            values['s_s'] = '1'
                    
                    
                    '''if None not in values.values():
                        config = "self.c_text(x = %(x)s, y = %(y)s, text = u'%(text)s', fill = '%(fill)s', angle = %(angle)s, size = %(size)s, anchor = 'sw', sloy = 1, s_s = %(s_s)s, w_text = %(w_text)s, font = 'Simular TXT')"
                        config = (config % values)
                        self.command_list.append(config)
                        text_flag = 0
'''
                if i == "DIMENSION" or (dim_flag == 1 and self.entities[ind+1].split() and self.entities[ind+1].split()[0].isupper() and i == '0'):
                    if dim_flag == 0:
                        dim_flag = 1
                        dimstyle_flag = 0
                        values = {'fill':None,
                                  'ort':None,
                                  'dim_handle':None, 
                                  'x1':None,
                                  'y1':None,
                                  'x2':None,
                                  'y2':None,
                                  'x3':None,
                                  'y3':None}
                    else:
                        for j in values:
                            if values[j] == None:
                                if j == 'fill':
                                    values[j] = 'white'
                                elif j == 'ort':
                                    values[j] = "vertical"
                                
                        if None not in values.values():
                            values = dim_texter(values)
                            config = "self.dim(x1 = %(x1)s, y1 = %(y1)s, x2 = %(x2)s, y2 = %(y2)s, x3 = %(x3)s, y3 = %(y3)s, text = u'%(text)s', fill = '%(fill)s', ort = '%(ort)s', size = %(size)s, text_change = '%(text_change)s', text_place = %(text_place)s, sloy = %(sloy)s, s = %(s)s, vr_s = %(vr_s)s, vv_s = %(vv_s)s, arrow_s = %(arrow_s)s, type_arrow = '%(type_arrow)s', s_s = %(s_s_dim)s, w_text = %(w_text_dim)s, font = '%(font_dim)s')"
                            config = (config % values)
                            self.command_list.append(config)
                        dim_flag = 0

                if dim_flag == 1:
                    if i == '5' and values['dim_handle'] == None:
                        values['dim_handle'] = self.entities[ind+1].split()[0]
                    elif i == '62':
                        values['fill'] = dxf_colorer(self.entities[ind+1])
                    elif i == '10':
                        values['x3'] = float(self.entities[ind+1])
                    elif i == '20':
                        values['y3'] = -float(self.entities[ind+1])
                    elif i == '13':
                        values['x1'] = float(self.entities[ind+1])
                    elif i == '23':
                        values['y1'] = -float(self.entities[ind+1])
                    elif i == '14':
                        values['x2'] = float(self.entities[ind+1])
                    elif i == '24':
                        values['y2'] = -float(self.entities[ind+1])
                    elif i == '11':
                        values['text_x'] = float(self.entities[ind+1])
                    elif i == '21':
                        values['text_y'] = -float(self.entities[ind+1])
                    
                    elif i == '2':
                        text = self.entities[ind+1]
                        if text[-1] == '\r':
                            text = text[0:-1]
                        values['dim_ind'] = text
                    elif i == '50':
                        a = float(self.entities[ind+1])
                        if a == 90.0:
                            values['ort'] = "horizontal"
                        elif a == 0.0:
                            values['ort'] = "vertical"
                    elif i == 'DSTYLE':
                        dimstyle_flag = 1
                        continue
                   
                    if dimstyle_flag == 1:
                        if i == '1040' and (self.entities[ind-2].split()[0],self.entities[ind-1].split()[0]) == ('1070', '147'):
                            values['s'] = float(self.entities[ind+1])
                        elif i == '1040' and (self.entities[ind-2].split()[0],self.entities[ind-1].split()[0]) == ('1070', '44'):
                            values['vv_s'] = float(self.entities[ind+1])
                        elif i == '1040' and (self.entities[ind-2].split()[0],self.entities[ind-1].split()[0]) == ('1070', '41'):
                            values['size_arrow'] = float(self.entities[ind+1])

                        
                    #if None not in values.values():
                        #continue
                    '''
                        print 'exit2'
                        values = dim_texter(values)
                        config = "self.dim(x1 = %(x1)s, y1 = %(y1)s, x2 = %(x2)s, y2 = %(y2)s, x3 = %(x3)s, y3 = %(y3)s, text = u'%(text)s', fill = '%(fill)s', ort = '%(ort)s', size = %(size)s, text_change = '%(text_change)s', text_place = %(text_place)s, sloy = %(sloy)s, s = %(s)s, vr_s = %(vr_s)s, vv_s = %(vv_s)s, arrow_s = %(arrow_s)s, type_arrow = '%(type_arrow)s', s_s = %(s_s_dim)s, w_text = %(w_text_dim)s, font = '%(font_dim)s')"
                        config = (config % values)
                        self.command_list.append(config)
                        dim_flag = 0
                    '''
            
