# -*- coding: utf-8 -*-
import re
import math

import src.line as line
import src.arc as arc
import src.circle as circle
import src.text_line as text_line
import src.dimension as dimension
#import src.dxf_library.color_acad_rgb as color_acad_rgb

import src.sectors_alg as sectors_alg
class Load_from_DXF:
    def __init__(self, par, _file):
        self.par = par
        
        self.DXF_my_ltypes = {
            'CENTER':(4,1,1,1),
            'DASHED':(1,1),
            'PHANTOM':(4,1,1,1,1,1),
            'Continuous':None,
            }
                    
        
        self.par.delete_objects(self.par.ALLOBJECT.keys())
        self.par.collection = []
        
        self.dxf, comment = self.dxf_parse(_file)
        if not self.dxf:
            print 'DXF fatal error:'
            print comment
            print 'Invalid or incomplete DXF input -- drawing discarded.'
            return

        w = 0.0
        h = 0.0
        x_mov = 0
        y_mov = 0
        for obj in self.excavated_dxf['entities']:
            for x in obj['xx']:
                if x<0 and x < x_mov:
                    x_mov = x
            for y in obj['yy']:
                if y<0 and y < y_mov:
                    y_mov = y
        if x_mov or y_mov:
            for obj in self.excavated_dxf['entities']:
                for x in ('x1', 'x2', 'x3', 'text_place'):
                    if x in obj:
                        if x == 'text_place' and obj[x][0] != None:
                            obj[x][0] -= x_mov-1
                        else:
                            obj[x] -= x_mov-1

                for y in ('y1', 'y2', 'y3', 'text_place'):
                    if y in obj:
                        if y == 'text_place' and obj[y][0] != None:
                            obj[y][1] -= y_mov-1
                        else:
                            obj[y] -= y_mov-1
                    
        for obj in self.excavated_dxf['entities']:
            for x in ('x1', 'x2', 'x3'):
                if x in obj:
                    if obj[x] > w:
                        w = obj[x]
            for y in ('y1', 'y2', 'y3'):
                if y in obj:
                    if obj[y] > h:
                        h = obj[y]
        print w, h
        new_h = math.ceil((h)/self.par.q_scale)*(self.par.q_scale)+self.par.q_scale#*1000
        new_w = math.ceil((w)/self.par.q_scale)*(self.par.q_scale)+self.par.q_scale#*1000
        print new_w, new_h
        if new_h > self.par.drawing_h:
            self.par.drawing_h = new_h
        if new_w > self.par.drawing_w:
            self.par.drawing_w = new_w
        
        self.par.create_sectors()
        print 'read', len(self.excavated_dxf['entities']), 'dxf entities'
        for obj in self.excavated_dxf['entities']:
            
            obj['color'] = self.DXF_colorer(obj['color'])
            if 'width' in obj:
                obj['width'] = self.DXF_widther(obj['width'])
            obj['layer'] = '1' #Временно
            if obj['obj'] == 'LINE':
                obj['stipple'] = self.DXF_ltyper(obj['ltype'])
                line.c_line(
                    self.par, obj['x1'], obj['y1'], obj['x2'], obj['y2'],
                    width = obj['width'],
                    layer = obj['layer'],
                    color = obj['color'],
                    stipple = obj['stipple'],
                    factor_stipple = obj['factor_stipple'],
                    in_mass = True,
                    )
            elif obj['obj'] == 'ARC':
                obj['x2'], obj['y2'] = 0, 0
                obj['x3'], obj['y3'] = 0, 0
                arc.c_arc(
                    self.par,
                    obj['x1'],
                    obj['y1'],
                    obj['x2'],
                    obj['y2'],
                    obj['x3'],
                    obj['y3'],
                    R = obj['R'],
                    width = obj['width'],
                    layer = obj['layer'],
                    color = obj['color'],
                    start = obj['start'],
                    extent = obj['extent'],
                    in_mass = True,
                    temp = False,  
                )
            elif obj['obj'] == 'CIRCLE':
                obj['x2'], obj['y2'] = 0, 0
                circle.c_circle(
                    self.par,
                    obj['x1'],
                    obj['y1'],
                    obj['x2'],
                    obj['y2'],
                    R = obj['R'],
                    width = obj['width'],
                    layer = obj['layer'],
                    color = obj['color'],
                    in_mass = True,
                    temp = False
                )

            elif obj['obj'] == 'TEXT':
                obj['text_w'] = obj['text_s_s']*1.4
                obj['anchor'] = 'sw'
                obj['text_font'] = 'txt'
                text_line.c_text(
                    self.par,
                    obj['x1'],
                    obj['y1'],
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

            elif obj['obj'] == 'DIMENSION':
                obj['dim_text_w'] = obj['dim_text_s_s']*1.4
                obj['dim_text_font'] = 'txt'
                cNew =  dimension.c_dim(
                    self.par,
                    obj['x1'],
                    obj['y1'],
                    obj['x2'],
                    obj['y2'],
                    obj['x3'],
                    obj['y3'],
                    text = obj['text'],
                    layer = obj['layer'],
                    color = obj['color'],
                    dim_text_size = obj['dim_text_size'],
                    ort = obj['ort'],
                    text_change = obj['text_change'],
                    text_place = obj['text_place'],
                    s = obj['s'],
                    vv_s = obj['vv_s'],
                    vr_s = obj['vr_s'],
                    arrow_s = obj['arrow_s'],
                    type_arrow = obj['type_arrow'],
                    dim_text_s_s = obj['dim_text_s_s'],
                    dim_text_w = obj['dim_text_w'],
                    dim_text_font = obj['dim_text_font'],
                    in_mass = True,
                    temp = False,
                    )
        print 'redraw...'
        
        
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
        print comment
        

    def dxf_parse(self, dxf_file):
        '''
        dxf_file = open(dxf_file)
        dxf_string = dxf_file.read()
        dxf_file.close()
        '''
        with open(dxf_file, 'r') as f:
            dxf_string = f.read()
        f.closed

        self.dxf_sections = {}
        self.excavated_dxf = {}
        for section_name in (
            'HEADER',
            'CLASSES',
            'TABLES',
            'BLOCKS',
            'ENTITIES',
            'OBJECTS',
            ):
            #DXF SECTIONS
            try:
                self.dxf_sections[section_name] = re.findall(r'0\r?\nSECTION\r?\n[ ]*2\r?\n%s([\w\W]*?0\r?\nENDSEC)'%section_name, dxf_string, re.DOTALL)[0]
            except:
            #if not self.dxf_sections[section_name]:
                if section_name in ('ENTITIES', 'TABLES'):
                    return None, 'Not section %s'%section_name
                else:
                    print 'DXF read warning: not section %s'%section_name
        #DXF LTYPES
        self.dxf_ltypes()

        #DXF BLOCK_RECORD
        self.dxf_block_records()

        #DXF STYLES
        self.dxf_styles()

        #DXF LAYERS
        self.dxf_layers()

        #DXF STYLES
        self.dxf_dimstyles()

        #DXF ENTITIES
        self.dxf_entities()
        #print 'excavar', self.excavated_dxf['dimstyles']
        #print len(self.excavated_dxf['entities'])
         
        return self.excavated_dxf, 'Opening an AutoCAD 2000 DXF file'

    def dxf_ltypes(self):
        dxf_TABLE_LTYPE = re.findall(r'0\r?\nTABLE\r?\n[ ]*2\r?\nLTYPE([\w\W]*?\r?\nENDTAB)', self.dxf_sections['TABLES'], re.DOTALL)[0]
        dxf_LTYPES = re.findall(r'LTYPE\r?\n[ ]*5([\w\W]*?)\n\r?(?=[ ]*0\r?\n[A-Z]+)', dxf_TABLE_LTYPE)
        dxf_LTYPES_names = []
        for LTYPE in dxf_LTYPES:
            LTYPE_name = re.findall(r'AcDbLinetypeTableRecord\r?\n[ ]*2\r?\n[ ]*(\w*)\r?\n', LTYPE)
            try:
                LTYPE_name = LTYPE_name[0]
            except IndexError:
                #print LTYPE
                continue
            if LTYPE_name in ('CENTER', 'DASHED', 'PHANTOM'):
                dxf_LTYPES_names.append(LTYPE_name)
        self.excavated_dxf['ltypes'] = dxf_LTYPES_names

    def dxf_block_records(self):
        dxf_TABLE_BLOCK_RECORD = re.findall(r'0\r?\nTABLE\r?\n[ ]*2\r?\nBLOCK_RECORD([\w\W]*?\r?\nENDTAB)', self.dxf_sections['TABLES'], re.DOTALL)[0]
        dxf_BLOCK_RECORDS = re.findall(r'(BLOCK_RECORD\r?\n[ ]*5[\w\W]*?)\n\r?(?=[ ]*0\r?\n[A-Z]+)', dxf_TABLE_BLOCK_RECORD)
        dxf_BLOCK_RECORD_handle_name = {}
        for BLOCK_RECORD in dxf_BLOCK_RECORDS:
            BLOCK_RECORD_name = re.findall(r'AcDbBlockTableRecord\r?\n[ ]*2\r?\n[ ]*([\w_*-]*)\r?\n', BLOCK_RECORD)
            try:
                BLOCK_RECORD_name = BLOCK_RECORD_name[0]
            except IndexError:
                #print BLOCK_RECORD
                continue
            BLOCK_RECORD_handle = re.findall(r'BLOCK_RECORD\r?\n[ ]*5\r?\n[ ]*(\w*)\r?\n', BLOCK_RECORD)[0]
            dxf_BLOCK_RECORD_handle_name[BLOCK_RECORD_handle] = BLOCK_RECORD_name
        self.excavated_dxf['block_records'] = dxf_BLOCK_RECORD_handle_name

    def dxf_styles(self):
        dxf_TABLE_STYLE = re.findall(r'0\r?\nTABLE\r?\n[ ]*2\r?\nSTYLE([\w\W]*?\r?\nENDTAB)', self.dxf_sections['TABLES'], re.DOTALL)[0]
        dxf_STYLES = re.findall(r'STYLE\r?\n[ ]*5\r?\n[ ]*(\w*)\r?\n[ ]*([\w\W]*?)\r?\n(?=[ ]*0\r?\n[A-Z]+)', dxf_TABLE_STYLE)
        dxf_STYLE_names = {}
        for STYLE_groups in dxf_STYLES:
            STYLE_handle = STYLE_groups[0]
            STYLE = STYLE_groups[1]
            STYLE = unicode(STYLE, "cp1251")
            STYLE_name = re.findall(r'AcDbTextStyleTableRecord\r?\n[ ]*2\r?\n[ ]*([\w ]*)', STYLE, re.U)[0]
            STYLE_width = re.findall(r'\r?\n[ ]*41\r?\n[ ]*([\d.]*)\r?\n', STYLE, re.U)
            STYLE_width = self.get_val(STYLE_width, 1.0)
            STYLE_size = re.findall(r'\r?\n[ ]*42\r?\n[ ]*([\d.]*)\r?\n', STYLE, re.U)
            STYLE_size = self.get_val(STYLE_size, 350.0)
            #LAYER_ltype = re.findall(r'\r?\n[ ]*6\r?\n[ ]*([\w]*)', LAYER)[0]
            #LAYER_width = re.findall(r'\r?\n[ ]*370\r?\n[ ]*([-\d]*)', LAYER)[0]
            dxf_STYLE_names[STYLE_name] = {
                'handle':STYLE_handle,
                'text_s_s':STYLE_width,
                'text_size':STYLE_size,
                }
        self.excavated_dxf['styles'] = dxf_STYLE_names

    def dxf_layers(self):
        dxf_TABLE_LAYER = re.findall(r'0\r?\nTABLE\r?\n[ ]*2\r?\nLAYER([\w\W]*?\r?\nENDTAB)', self.dxf_sections['TABLES'], re.DOTALL)[0]
        dxf_LAYERS = re.findall(r'LAYER\r?\n[ ]*5([\w\W]*?)\r?\n(?=[ ]*0\r?\n[A-Z]+)', dxf_TABLE_LAYER)
        dxf_LAYER_names = {'0':{
                'color':7,
                'ltype':'Continuous',
                'width':20,
                }}
        for LAYER in dxf_LAYERS:
            LAYER = unicode(LAYER, "cp1251")
            LAYER_name = re.findall(r'AcDbLayerTableRecord\r?\n[ ]*2\r?\n[ ]*([-\w .]*)\r?\n', LAYER, re.U)
            try:
                LAYER_name = LAYER_name[0]
            except:
                print LAYER
                print '_______________'
                continue
            LAYER_color = re.findall(r'\r?\n[ ]*62\r?\n[ ]*([-\d]*)\r?\n', LAYER, re.U)[0]
            LAYER_ltype = re.findall(r'\r?\n[ ]*6\r?\n[ ]*([\w]*)\r?\n', LAYER, re.U)[0]
            LAYER_width = re.findall(r'\r?\n[ ]*370\r?\n[ ]*([-\d]*)\r?\n', LAYER, re.U)[0]
            dxf_LAYER_names[LAYER_name] = {
                'color':LAYER_color,
                'ltype':LAYER_ltype,
                'width':LAYER_width,
                }
        self.excavated_dxf['layers'] = dxf_LAYER_names

    def dxf_dimstyles(self):
        dxf_TABLE_DIMSTYLE = re.findall(r'0\r?\nTABLE\r?\n[ ]*2\r?\nDIMSTYLE([\w\W]*?\r?\nENDTAB)', self.dxf_sections['TABLES'], re.DOTALL)[0]
        dxf_DIMSTYLES = re.findall(r'DIMSTYLE\r?\n[ ]*105([\w\W]*?)\r?\n(?=[ ]*0\r?\n[A-Z]+)', dxf_TABLE_DIMSTYLE)
        dxf_DIMSTYLE_names = {}
        
        for DIMSTYLE in dxf_DIMSTYLES:
            DIMSTYLE = unicode(DIMSTYLE, "cp1251")
            DIMSTYLE_name = re.findall(r'AcDbDimStyleTableRecord\r?\n[ ]*2\r?\n[ ]*([\w -]*)', DIMSTYLE, re.U)
            try:
                DIMSTYLE_name = DIMSTYLE_name[0]
            except IndexError:
                print DIMSTYLE
                continue
            DIMSTYLE_arrow_s = re.findall(r'\r?\n[ ]*41\r?\n[ ]*([\d.]*)\r?\n', DIMSTYLE, re.U)
            DIMSTYLE_arrow_s = self.get_val(DIMSTYLE_arrow_s, 200.0)
            DIMSTYLE_vv_s = re.findall(r'\r?\n[ ]*44\r?\n[ ]*([\d.]*)\r?\n', DIMSTYLE, re.U)
            DIMSTYLE_vv_s = self.get_val(DIMSTYLE_vv_s, 150.0)
            DIMSTYLE_s = re.findall(r'\r?\n[ ]*147\r?\n[ ]*([\d.]*)\r?\n', DIMSTYLE, re.U)
            DIMSTYLE_s = self.get_val(DIMSTYLE_s, 50.0)
            DIMSTYLE_dim_text_size = re.findall(r'\r?\n[ ]*140\r?\n[ ]*([\d.]*)\r?\n', DIMSTYLE, re.U)
            DIMSTYLE_dim_text_size = self.get_val(DIMSTYLE_dim_text_size, 350.0)
            DIMSTYLE_dim_text_style_handle = re.findall(r'100\r?\n[ ]*AcDbDimStyleTableRecord\r?\n[ ]*[\w\W]*340\r?\n[ ]*([\w]*)', DIMSTYLE, re.U)[0]

            DIMSTYLE_dim_arrowhead_handle = re.findall(r'100\r?\n[ ]*AcDbDimStyleTableRecord\r?\n[ ]*[\w\W]*342\r?\n[ ]*([\w]*)', DIMSTYLE, re.U)
            DIMSTYLE_dim_arrowhead_handle = self.get_val(DIMSTYLE_dim_arrowhead_handle, None)
            DIMSTYLE_dim_arrowhead_type = None
            if DIMSTYLE_dim_arrowhead_handle:
                for block_record_handle in self.excavated_dxf['block_records'].keys():
                    if block_record_handle == DIMSTYLE_dim_arrowhead_handle:
                        DIMSTYLE_dim_arrowhead_type = self.excavated_dxf['block_records'][block_record_handle]
            
            for style in self.excavated_dxf['styles'].keys():
                if self.excavated_dxf['styles'][style]['handle'] == DIMSTYLE_dim_text_style_handle:
                    DIMSTYLE_dim_text_style = style
                    
            #LAYER_ltype = re.findall(r'\r?\n[ ]*6\r?\n[ ]*([\w]*)', LAYER)[0]
            #LAYER_width = re.findall(r'\r?\n[ ]*370\r?\n[ ]*([-\d]*)', LAYER)[0]
            dxf_DIMSTYLE_names[DIMSTYLE_name] = {
                'dim_text_s_s':self.excavated_dxf['styles'][DIMSTYLE_dim_text_style]['text_s_s'],
                'dim_text_size':DIMSTYLE_dim_text_size,
                'arrow_s':DIMSTYLE_arrow_s,
                's':DIMSTYLE_s,
                'vv_s':DIMSTYLE_vv_s,
                'type_arrow' : DIMSTYLE_dim_arrowhead_type,
                'text_style':{DIMSTYLE_dim_text_style:self.excavated_dxf['styles'][DIMSTYLE_dim_text_style]},
                }
        self.excavated_dxf['dimstyles'] = dxf_DIMSTYLE_names

    def dxf_entities(self):
        dxf_ENTITIES = re.findall(r'0\r?\n([A-Z]+)\r?\n[ ]*5\r?\n([\w\W]*?)\r?\n(?=[ ]*0\r?\n[A-Z]+)', self.dxf_sections['ENTITIES'])
        dxf_ENTITIES_names = []
        for i in dxf_ENTITIES:
            i = list(i)
            i[1] = unicode(i[1], "cp1251")
            obj = i[0]
            layer = re.findall(r'\r?\n[ ]*8\r?\n[ ]*([-\w .]*)\r?\n', i[1], re.U)
            try:
                layer = layer[0]
            except IndexError:
                #layer = '0'
                print i[1]
                #for e in self.excavated_dxf['layers']:
                    #print e
                continue              
            color = re.findall(r'\r?\n[ ]*62\r?\n[ ]*([-\d]*)\r?\n', i[1], re.U)
            try:
                color = self.get_val(color, self.excavated_dxf['layers'][layer]['color'])
            except:
                print i[1]
            if obj == 'LINE': 
                ltype = re.findall(r'\r?\n[ ]*6\r?\n[ ]*([\w]*)\r?\n', i[1], re.U)
                try:
                    ltype = self.get_val(ltype, self.excavated_dxf['layers'][layer]['ltype'])
                except:
                    print i[1]
                    for e in self.excavated_dxf['layers']:
                        print e
                    print layer
      
                width = re.findall(r'\r?\n[ ]*370\r?\n[ ]*([-\d]*)\r?\n', i[1], re.U)
                width = self.get_val(width, self.excavated_dxf['layers'][layer]['width'])
               
                stipple_factor = re.findall(r'\r?\n[ ]*48\r?\n[ ]*([\d.]*)\r?\n', i[1], re.U)
                stipple_factor = self.get_val(stipple_factor, 1.0)

                xy = re.findall(r'\r?\n[ ]*10\r?\n[ ]*([\d.-]*)\r?\n[ ]*20\r?\n[ ]*([\d.-]*)\r?\n[ ]*30\r?\n[ ]*(?:[\d.-]*)\r?\n[ ]*11\r?\n[ ]*([\d.-]*)\r?\n[ ]*21\r?\n[ ]*([\d.-]*)\r?\n[ ]*31\r?\n[ ]*(?:[\d.-]*)', i[1], re.U)
                if not xy:
                    xy = re.findall(r'\r?\n[ ]*10\r?\n[ ]*([\d.-]*)\r?\n[ ]*20\r?\n[ ]*([\d.-]*)\r?\n[ ]*11\r?\n[ ]*([\d.-]*)\r?\n[ ]*21\r?\n[ ]*([\d.-]*)', i[1], re.U)
                    
                    
                x1 = float(xy[0][0])
                y1 = float(xy[0][1])
                x2 = float(xy[0][2])
                y2 = float(xy[0][3])

                dxf_ENTITIES_names.append({
                    'obj':obj,
                    'color':color,
                    'ltype':ltype,
                    'width':width,
                    'x1':x1,
                    'y1':y1,
                    'x2':x2,
                    'y2':y2,
                    'xx':(x1, x2),
                    'yy':(y1, y2),
                    'factor_stipple':float(stipple_factor)*8.0,
                    })

            elif obj == 'ARC':
                ltype = re.findall(r'\r?\n[ ]*6\r?\n[ ]*([\w]*)\r?\n', i[1], re.U)
                ltype = self.get_val(ltype, self.excavated_dxf['layers'][layer]['ltype'])
      
                width = re.findall(r'\r?\n[ ]*370\r?\n[ ]*([-\d]*)\r?\n', i[1], re.U)
                width = self.get_val(width, self.excavated_dxf['layers'][layer]['width'])                    

                xy = re.findall(r'\r?\n[ ]*10\r?\n[ ]*([\d.-]*)\r?\n[ ]*20\r?\n[ ]*([\d.-]*)\r?\n[ ]*30\r?\n[ ]*(?:[\d.-]*)\r?\n[ ]*40\r?\n[ ]*([\d.-]*)[\w\W]*?\r?\n[ ]*100\r?\n[ ]*AcDbArc\r?\n[ ]*50\r?\n[ ]*([\d.-]*)\r?\n[ ]*51\r?\n[ ]*([\d.-]*)', i[1], re.U)
                if not xy:
                    xy = re.findall(r'\r?\n[ ]*10\r?\n[ ]*([\d.-]*)\r?\n[ ]*20\r?\n[ ]*([\d.-]*)\r?\n[ ]*40\r?\n[ ]*([\d.-]*)[\w\W]*?\r?\n[ ]*100\r?\n[ ]*AcDbArc\r?\n[ ]*50\r?\n[ ]*([\d.-]*)\r?\n[ ]*51\r?\n[ ]*([\d.-]*)', i[1], re.U)
                try:
                    x1 = float(xy[0][0])
                except:
                    print i[1]
                    return
                y1 = float(xy[0][1])
                R = float(xy[0][2])
                start = float(xy[0][3])
                extent = float(xy[0][4])
                
                if start > extent:
                    extent += 360
                

                dxf_ENTITIES_names.append({
                'obj':obj,
                'color':color,
                'width':width,
                'x1':x1,
                'y1':y1,
                'R':R,
                'start':start,
                'extent':extent,
                'xx':(x1-R, x1+R),
                'yy':(y1-R, y1+R),
                })

            elif obj == 'CIRCLE':
                ltype = re.findall(r'\r?\n[ ]*6\r?\n[ ]*([\w]*)\r?\n', i[1], re.U)
                ltype = self.get_val(ltype, self.excavated_dxf['layers'][layer]['ltype'])
      
                width = re.findall(r'\r?\n[ ]*370\r?\n[ ]*([-\d]*)\r?\n', i[1], re.U)
                width = self.get_val(width, self.excavated_dxf['layers'][layer]['width'])

                xy = re.findall(r'\r?\n[ ]*10\r?\n[ ]*([\d.-]*)\r?\n[ ]*20\r?\n[ ]*([\d.-]*)\r?\n[ ]*30\r?\n[ ]*(?:[\d.-]*)\r?\n[ ]*40\r?\n[ ]*([\d.-]*)', i[1], re.U)
                if not xy:
                    xy = re.findall(r'\r?\n[ ]*10\r?\n[ ]*([\d.-]*)\r?\n[ ]*20\r?\n[ ]*([\d.-]*)\r?\n[ ]*40\r?\n[ ]*([\d.-]*)', i[1], re.U)
                x1 = float(xy[0][0])
                y1 = float(xy[0][1])
                R = float(xy[0][2])
               
                dxf_ENTITIES_names.append({
                'obj':obj,
                'color':color,
                #'ltype':ltype,
                'width':width,
                'x1':x1,
                'y1':y1,
                'R':R,
                'xx':(x1-R, x1+R),
                'yy':(y1-R, y1+R),
                #'factor_stipple':float(stipple_factor)*8.0,
                })

            elif obj == 'TEXT':
                style = re.findall(r'100\r?\n[ ]*AcDbText\r?\n[ ]*7\r?\n[ ]*7\r?\n[ ]*([\w ]*)\r?\n', i[1], re.U)
                style = self.get_val(style, 'Standard')
                
                width = re.findall(r'\r?\n[ ]*41\r?\n[ ]*([\d.-]*)\r?\n', i[1], re.U)
                width = self.get_val(width, self.excavated_dxf['styles'][style]['text_s_s'])

                size = re.findall(r'\r?\n[ ]*40\r?\n[ ]*([-\d.]*)\r?\n', i[1], re.U)
                size = self.get_val(size, self.excavated_dxf['styles'][style]['text_size'])

                angle = re.findall(r'\r?\n[ ]*50\r?\n[ ]*([\d.-]*)\r?\n', i[1], re.U)
                angle = self.get_val(angle, 0.0)

                text = re.findall(r'(?:AcDbText\r?\n[ ]*[\w\W]*?)\r?\n[ ]*1\r?\n[ ]*([\w. -]*?)\r?\n', i[1], re.U)#unicode(i[1], "cp1251"), re.U)
                text = self.get_val(text, 'None')
               
                xy = re.findall(r'\r?\n[ ]*10\r?\n[ ]*([\d.-]*)\r?\n[ ]*20\r?\n[ ]*([\d.-]*)\r?\n[ ]*30\r?\n[ ]*([\d.-]*)\r?\n', i[1], re.U)
                if not xy:
                    xy = re.findall(r'\r?\n[ ]*10\r?\n[ ]*([\d.-]*)\r?\n[ ]*20\r?\n[ ]*([\d.-]*)', i[1], re.U)
                x1 = float(xy[0][0])
                y1 = float(xy[0][1])

                dxf_ENTITIES_names.append({
                    'obj':obj,
                    'color':color,
                    'text_s_s':float(width)/0.57,
                    'angle':-math.radians(float(angle)),
                    'text_size':abs(float(size)),
                    'text':text,
                    'x1':x1,
                    'y1':y1,
                    'xx':(x1,),
                    'yy':(y1,),
                    })

            elif obj == 'DIMENSION':
                dimstyle = re.findall(r'AcDbDimension\r?\n[\W\w]*\r?\n[ ]*3\r?\n[ ]*([\S ]*)[\W\w]*100\r?\n[ ]*AcDbAlignedDimension', i[1], re.U)
                try:
                    dimstyle = dimstyle[0]
                except:
                    continue
                dimstyle_dict = self.excavated_dxf['dimstyles'][dimstyle]

                text = re.findall(r'AcDbDimension\r?\n[\W\w]*\r?\n[ ]*1\r?\n[ ]*([\S ]*)[\W\w]*100\r?\n[ ]*AcDbAlignedDimension', i[1], re.U)#unicode(i[1], "cp1251"), re.U)
                
		#if text:
                #	text = text[0]
                text = self.get_val(text, None)
                
                dimstyle_dict = self.excavated_dxf['dimstyles'][dimstyle]

                text_change_2 = re.findall(r'AcDbDimension\r?\n[\W\w]*\r?\n[ ]*70\r?\n[ ]*([\d]*)[\W\w]*100\r?\n[ ]*AcDbAlignedDimension', i[1], re.U)
                text_change_2 = self.get_val(text_change_2, 32)

                DIMSCALE = re.findall(r'1001\r?\n[ ]*ACAD\r?\n[ ]*1000\r?\n[ ]*DSTYLE[\w\W]*\r?\n[ ]*1070\r?\n[ ]*40\r?\n[ ]*1040\r?\n[ ]*([\d.]*)\r?\n[ ]*', i[1], re.U)
                DIMSCALE = self.get_val(DIMSCALE, 1.0)
                DIMSCALE = float(DIMSCALE)
                
                vv_s = re.findall(r'1001\r?\n[ ]*ACAD\r?\n[ ]*1000\r?\n[ ]*DSTYLE[\w\W]*\r?\n[ ]*1070\r?\n[ ]*44\r?\n[ ]*1040\r?\n[ ]*([\d.]*)\r?\n[ ]*', i[1], re.U)
                vv_s = self.get_val(vv_s, dimstyle_dict['vv_s'])

                vr_s = re.findall(r'1001\r?\n[ ]*ACAD\r?\n[ ]*1000\r?\n[ ]*DSTYLE[\w\W]*\r?\n[ ]*1070\r?\n[ ]*46\r?\n[ ]*1040\r?\n[ ]*([\d.]*)\r?\n[ ]*', i[1], re.U)
                vr_s = self.get_val(vr_s, 0.0)

                arrow_s = re.findall(r'1001\r?\n[ ]*ACAD\r?\n[ ]*1000\r?\n[ ]*DSTYLE[\w\W]*\r?\n[ ]*1070\r?\n[ ]*41\r?\n[ ]*1040\r?\n[ ]*([\d.]*)\r?\n[ ]*', i[1], re.U)
                #try:
                    #arrow_s = arrow_s[0]
                #except:
                    #print i[1]
                    #return
                arrow_s = self.get_val(arrow_s, dimstyle_dict['arrow_s'])
                
                s = re.findall(r'1001\r?\n[ ]*ACAD\r?\n[ ]*1000\r?\n[ ]*DSTYLE[\w\W]*\r?\n[ ]*1070\r?\n[ ]*147\r?\n[ ]*1040\r?\n[ ]*([\d.]*)\r?\n[ ]*', i[1], re.U)
                s = self.get_val(s, dimstyle_dict['s'])

                
                if dimstyle_dict['type_arrow']:
                    default_type_arrow = dimstyle_dict['type_arrow']
                else:
                    default_type_arrow = 'Arrow'
                arrowhead_handle = re.findall(r'1001\r?\n[ ]*ACAD\r?\n[ ]*1000\r?\n[ ]*DSTYLE[\w\W]*\r?\n[ ]*1070\r?\n[ ]*343\r?\n[ ]*1005\r?\n[ ]*(\w*)\r?\n[ ]*', i[1], re.U)
                if arrowhead_handle:
                    arrowhead_handle = arrowhead_handle[0]
                    try:
                        type_arrow = self.excavated_dxf['block_records'][arrowhead_handle]
                    except:
                        #print 'Unknow arowhead'
                        type_arrow = default_type_arrow
                    if type_arrow in ('_Oblique', '_OBLIQUE', '_ArchTick'):
                        type_arrow = 'Arch'
                    else:
                        type_arrow = 'Arrow'
                else:
                    type_arrow = default_type_arrow

                if type_arrow == 'Arch':
                    arrow_s = float(arrow_s)/2.0

                dim_text_size = re.findall(r'1001\r?\n[ ]*ACAD\r?\n[ ]*1000\r?\n[ ]*DSTYLE[\w\W]*\r?\n[ ]*1070\r?\n[ ]*140\r?\n[ ]*1040\r?\n[ ]*([\d.]*)\r?\n[ ]*', i[1], re.U)
                dim_text_size = self.get_val(dim_text_size, dimstyle_dict['dim_text_size'])
                dim_text_size = abs(float(dim_text_size))
                
                angle = re.findall(r'AcDbAlignedDimension\r?\n[\W\w]*\r?\n[ ]*50\r?\n[ ]*([\d.-]*)[\W\w]*100\r?\n[ ]*AcDbRotatedDimension', i[1], re.U)
                angle = float(self.get_val(angle, 0.0))

                if angle == 0.0:
                    ort = 'vertical'
                else:
                    ort = 'horizontal'

                text_change = re.findall(r'1001\r?\n[ ]*ACAD\r?\n[ ]*1000\r?\n[ ]*DSTYLE[\w\W]*\r?\n[ ]*1070\r?\n[ ]*279\r?\n[ ]*1070\r?\n[ ]*([\d]*)\r?\n[ ]*', i[1], re.U)
                text_change = self.get_val(text_change, 0)
                text_change = int(text_change)
                text_change_2 = int(text_change_2)
                if text_change == 0 and text_change_2 == 32:
                    text_change = 1
                elif text_change == 0 and text_change_2 == 160:
                    text_change = 2
                elif text_change == 2 and text_change_2 == 160:
                    text_change = 3
                else:
                    text_change = 1
                    

                dim_text_s_s = dimstyle_dict['dim_text_s_s']

                
               
                xy12 = re.findall(r'13\r?\n[ ]*([-\d.]*)\r?\n[ ]*23\r?\n[ ]*([-\d.]*)\r?\n[ ]*33\r?\n[ ]*[-\d.]*\r?\n[ ]*14\r?\n[ ]*([-\d.]*)\r?\n[ ]*24\r?\n[ ]*([-\d.]*)\r?\n[ ]*34\r?\n[ ]*[-\d.]*\r?\n[ ]*', i[1], re.U)
                if not xy12:
                    xy12 = re.findall(r'13\r?\n[ ]*([-\d.]*)\r?\n[ ]*23\r?\n[ ]*([-\d.]*)\r?\n[ ]*14\r?\n[ ]*([-\d.]*)\r?\n[ ]*24\r?\n[ ]*([-\d.]*)\r?\n[ ]*', i[1], re.U)

                xy3text = re.findall(r'10\r?\n[ ]*([-\d.]*)\r?\n[ ]*20\r?\n[ ]*([-\d.]*)\r?\n[ ]*30\r?\n[ ]*[-\d.]*\r?\n[ ]*11\r?\n[ ]*([-\d.]*)\r?\n[ ]*21\r?\n[ ]*([-\d.]*)\r?\n[ ]*31\r?\n[ ]*[-\d.]*\r?\n[ ]*', i[1], re.U)
                if not xy3text:
                    xy3text = re.findall(r'10\r?\n[ ]*([-\d.]*)\r?\n[ ]*20\r?\n[ ]*([-\d.]*)\r?\n[ ]*11\r?\n[ ]*([-\d.]*)\r?\n[ ]*21\r?\n[ ]*([-\d.]*)\r?\n[ ]*', i[1], re.U)
                try:
                    x1 = float(xy12[0][0])
                except IndexError:
                    print i[1]
                    continue
                x1 = float(xy12[0][0])
                y1 = float(xy12[0][1])
                x2 = float(xy12[0][2])
                y2 = float(xy12[0][3])

                x3 = float(xy3text[0][0])
                y3 = float(xy3text[0][1])
                text_x = float(xy3text[0][2])
                text_y = float(xy3text[0][3])
                if text_change == 3:
                    if ort == 'horizontal':
                        text_x += dim_text_size/2.0
                    else:
                        text_y -= dim_text_size/2.0
                    

                dxf_ENTITIES_names.append({
                    'obj':obj,
                    'color':color,
                    'dim_text_s_s':float(dim_text_s_s)/0.57,# * DIMSCALE,
                    'angle':math.radians(abs(angle)),
                    'dim_text_size':dim_text_size * DIMSCALE,
                    'text_place':[text_x, text_y],
                    'text_change':text_change,
                    'ort':ort,
                    'text':text,
                    's':float(s)* DIMSCALE,
                    'vv_s':float(vv_s),#* DIMSCALE,
                    'vr_s':float(vr_s),#* DIMSCALE,
                    'arrow_s':float(arrow_s)* DIMSCALE,
                    'type_arrow':type_arrow,
                    'x1':x1,
                    'y1':y1,
                    'x2':x2,
                    'y2':y2,
                    'x3':x3,
                    'y3':y3,
                    'xx':(x1,x2,x3,text_x),
                    'yy':(y1,y2,y3,text_y),
                    })
                
        self.excavated_dxf['entities'] = dxf_ENTITIES_names
        #print self.excavated_dxf['entities']

    def DXF_widther(self, DXF_width):
        DXF_width = int(DXF_width)
        if 0 < DXF_width <= 20:
            w = 1
        elif 20 < DXF_width <= 30:
            w = 2
        elif 30 < DXF_width <= 80:
            w = 3
        elif 80 < DXF_width:
            w = 4
        else:
            w = 2
        return w

    def DXF_colorer(self, DXF_color):
        try:
            c = self.par.DXF_RGB_colores[int(DXF_color)]
        except:
            c = self.par.DXF_RGB_colores[7]
        return list(c)

    def DXF_ltyper(self, DXF_ltype):
        try:
            c = self.DXF_my_ltypes[DXF_ltype]
        except:
            c = self.DXF_my_ltypes['Continuous']
        return c

    def get_val(self, input_v, default):
        if input_v:
            output_v = input_v[0]
        else:
            output_v = default
            
        return output_v
        
            
        
                
        
