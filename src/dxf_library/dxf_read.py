# -*- coding: utf-8 -*-
import re
import math

import src.line as line

import src.sectors_alg as sectors_alg
class Load_from_DXF:
    def __init__(self, par, _file):
        self.par = par
        self.DXF_RGB_colores = {
            7:(255, 255, 255),
            5:(0, 0, 255),
            96:(0, 255, 0),
            3:(0, 255, 0),
            10:(255, 0, 0),
            1:(255, 0, 0),
            2:(255, 255, 0),
            }
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
        for obj in self.excavated_dxf['entities']:
            for x in obj['xx']:
                if x > w:
                    w = x

            for y in obj['yy']:
                if y > h:
                    h = y
        new_h = math.ceil((h)/self.par.q_scale)*(self.par.q_scale)#+self.par.q_scale*1000
        new_w = math.ceil((w)/self.par.q_scale)*(self.par.q_scale)#+self.par.q_scale*1000
        #print new_h, new_w
        if new_h > self.par.drawing_h:
            self.par.drawing_h = new_h
        if new_w > self.par.drawing_w:
            self.par.drawing_w = new_w
        #print int(self.par.drawing_w)
        #print int(self.par.drawing_h)
        self.par.create_sectors()
        print 'read', len(self.excavated_dxf['entities']), 'dxf entities'
        for obj in self.excavated_dxf['entities']:
            
            obj['color'] = self.DXF_colorer(obj['color'])
            if obj['obj'] == 'LINE':
                obj['width'] = self.DXF_widther(obj['width'])
                obj['stipple'] = self.DXF_ltyper(obj['ltype'])
                obj['layer'] = '1' #Временно
                line.c_line(
                    self.par, obj['x1'], obj['y1'], obj['x2'], obj['y2'],
                    width = obj['width'],
                    layer = obj['layer'],
                    color = obj['color'],
                    stipple = obj['stipple'],
                    factor_stipple = obj['factor_stipple'],
                    in_mass = True,
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
            self.dxf_sections[section_name] = re.findall('0\r?\nSECTION\r?\n[ ]*2\r?\n%s([\w\W]*?0\r?\nENDSEC)'%section_name, dxf_string, re.DOTALL)[0]
            if not self.dxf_sections[section_name]:
                if section_name in ('ENTITIES', 'TABLES'):
                    return None, 'Not section %s'%section_name
                else:
                    print 'DXF read warning: not section %s'%section_name
        #DXF LTYPES
        self.dxf_ltypes()

        #DXF LAYERS
        self.dxf_layers()

        #DXF ENTITIES
        self.dxf_entities()
        #print 'excavar', self.excavated_dxf
        #print len(self.excavated_dxf['entities'])
         
        return self.excavated_dxf, 'Opening an AutoCAD 2000 DXF file'

    def dxf_ltypes(self):
        dxf_TABLE_LTYPE = re.findall('0\r?\nTABLE\r?\n[ ]*2\r?\nLTYPE([\w\W]*?\r?\nENDTAB)', self.dxf_sections['TABLES'], re.DOTALL)[0]
        #dxf_TABLE_LTYPE += '0'
        dxf_LTYPES = re.findall('LTYPE\r?\n[ ]*5([\w\W]*?)\n\r?(?=[ ]*0\r?\n[A-Z]+)', dxf_TABLE_LTYPE)
        dxf_LTYPES_names = []
        for LTYPE in dxf_LTYPES:
            LTYPE_name = re.findall('AcDbLinetypeTableRecord\r?\n[ ]*2\r?\n[ ]*(\w*)', LTYPE)[0]
            if LTYPE_name in ('CENTER', 'DASHED', 'PHANTOM'):
                dxf_LTYPES_names.append(LTYPE_name)
        self.excavated_dxf['ltypes'] = dxf_LTYPES_names

    def dxf_layers(self):
        dxf_TABLE_LAYER = re.findall('0\r?\nTABLE\r?\n[ ]*2\r?\nLAYER([\w\W]*?\r?\nENDTAB)', self.dxf_sections['TABLES'], re.DOTALL)[0]
        dxf_LAYERS = re.findall('LAYER\r?\n[ ]*5([\w\W]*?)\r?\n(?=[ ]*0\r?\n[A-Z]+)', dxf_TABLE_LAYER)
        dxf_LAYER_names = {}
        for LAYER in dxf_LAYERS:
            LAYER_name = re.findall('AcDbLayerTableRecord\r?\n[ ]*2\r?\n[ ]*([\w ]*)', LAYER)[0]
            LAYER_color = re.findall('\r?\n[ ]*62\r?\n[ ]*([-\d]*)', LAYER)[0]
            LAYER_ltype = re.findall('\r?\n[ ]*6\r?\n[ ]*([\w]*)', LAYER)[0]
            LAYER_width = re.findall('\r?\n[ ]*370\r?\n[ ]*([-\d]*)', LAYER)[0]
            dxf_LAYER_names[LAYER_name] = {
                'color':LAYER_color,
                'ltype':LAYER_ltype,
                'width':LAYER_width,
                }
        self.excavated_dxf['layers'] = dxf_LAYER_names

    def dxf_entities(self):
        #print self.dxf_sections['ENTITIES']
        dxf_ENTITIES = re.findall('0\r?\n([A-Z]+)\r?\n[ ]*5\r?\n([\w\W]*?)\r?\n(?=[ ]*0\r?\n[A-Z]+)', self.dxf_sections['ENTITIES'])
        dxf_ENTITIES_names = []
        #r = 0
        for i in dxf_ENTITIES:
            '''
            r+=1
            
            if r == 100:
                break
            '''
            
            obj = i[0]
            if obj == 'LINE':
                
                layer = re.findall('\r?\n[ ]*8\r?\n[ ]*([\w]*)', i[1])[0]                
                color = re.findall('\r?\n[ ]*62\r?\n[ ]*([-\d]*)', i[1])
                if not color:
                    color = self.excavated_dxf['layers'][layer]['color']
                else:
                    color = color[0]
                    
                ltype = re.findall('\r?\n[ ]*6\r?\n[ ]*([\w]*)', i[1])
                if not ltype:
                    ltype = self.excavated_dxf['layers'][layer]['ltype']
                else:
                    ltype = ltype[0]
                    
                width = re.findall('\r?\n[ ]*370\r?\n[ ]*([-\d]*)', i[1])
                if not width:
                    width = self.excavated_dxf['layers'][layer]['width']
                else:
                    width = width[0]
                    
                stipple_factor = re.findall('\r?\n[ ]*48\r?\n[ ]*([\d]*)', i[1])
                if not stipple_factor:
                    stipple_factor = 1.0
                else:
                    stipple_factor = stipple_factor[0]
                    

                xy = re.findall('\r?\n[ ]*10\r?\n[ ]*([\d.]*)\r?\n[ ]*20\r?\n[ ]*([\d.]*)\r?\n[ ]*30\r?\n[ ]*([\d.]*)\r?\n[ ]*11\r?\n[ ]*([\d.]*)\r?\n[ ]*21\r?\n[ ]*([\d.]*)\r?\n[ ]*31\r?\n[ ]*([\d.]*)', i[1])[0]
                
                x1 = xy[0]
                y1 = xy[1]
                x2 = xy[3]
                y2 = xy[4]

                #x2y2 = re.findall('\r?\n[ ]*11\r?\n[ ]*([\d.]*)\r?\n[ ]*21\r?\n[ ]*([\d.]*)', i[1])[0]
                #x2 = x2y2[0]
                #y2 = x2y2[1]
               
                try:
                    dxf_ENTITIES_names.append({
                    'obj':obj,
                    'color':color,
                    'ltype':ltype,
                    'width':float(width),
                    'x1':float(x1),
                    'y1':float(y1),
                    'x2':float(x2),
                    'y2':float(y2),
                    'xx':(float(x1), float(x2)),
                    'yy':(float(y1), float(y2)),
                    'factor_stipple':float(stipple_factor)*8.0,
                    })
                except:
                    print x1, x2, y1, y2
                    return
        self.excavated_dxf['entities'] = dxf_ENTITIES_names

    def DXF_widther(self, DXF_width):
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
            c = self.DXF_RGB_colores[int(DXF_color)]
        except:
            #print 'unknow DXF color:', DXF_color
            c = self.DXF_RGB_colores[7]
        return list(c)

    def DXF_ltyper(self, DXF_ltype):
        try:
            c = self.DXF_my_ltypes[DXF_ltype]
        except:
            #print 'unknow DXF ltype:', DXF_ltype
            c = self.DXF_my_ltypes['Continuous']
        return c
        
            
        
                
        
