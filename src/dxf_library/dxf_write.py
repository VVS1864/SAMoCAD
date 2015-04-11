# -*- coding: utf-8 -*-

import src.save_file as save_file
import os
from math import degrees
appPath = os.getcwd()


class Save_to_DXF(save_file.Base_save):
    def __init__(self, par, file_name, file_format, ALLOBJECT, layers, stipples, drawing_w, drawing_h):
        super(Save_to_DXF, self).__init__(par, file_format, ALLOBJECT, layers, drawing_w, drawing_h)
        self.handle = 'BA'
        self._OBLIQUE = False
        self.dim_list = {}
        dim_ind = 0

        self.dxf_line = """LINE
  5
%(handle)s
330
%(handle2)s
100
AcDbEntity
  8
0
  6
%(dash)s
 62
  %(color)s
 48
%(factor_stipple)s
370
   %(width)s
100
AcDbLine
 10
%(x1)s
 20
%(y1)s
 30
0.0
 11
%(x2)s
 21
%(y2)s
 31
0.0
 0"""
        self.dxf_arc = """ARC
5
%(handle)s
330
1F
100
AcDbEntity
8
0
6
ByLayer
62
%(color)s
370
%(width)s
100
AcDbCircle
10
%(x1)s
20
%(y1)s
30
0.0
40
%(R)s
100
AcDbArc
50
%(start)s
51
%(extent)s
0"""

        self.dxf_circle = """CIRCLE
5
%(handle)s
330
1F
100
AcDbEntity
  8
0
 62
  %(color)s
370
   %(width)s
100
AcDbCircle
 10
%(x1)s
 20
%(y1)s
 30
0.0
 40
%(R)s
  0"""
        self.dxf_text = """TEXT
5
%(handle)s
330
1F
100
AcDbEntity
8
0
62
%(color)s
100
AcDbText
10
%(x1)s
20
%(y1)s
30
0.0
40
%(text_size)s
50
%(angle)s
1
%(text)s
41
%(text_s_s)s
100
AcDbText
0"""
        
###        DIMENSION   ###
        self.dxf_dim = """DIMENSION
  5
%(handle)s
330
1F
100
AcDbEntity
  8
0
62
%(color)s
100
AcDbDimension
  2
*%(dim_ind)s
 10
%(arrow_point2_x)s
 20
%(arrow_point2_y)s
 30
0.0
 11
%(text_xx)s
 21
%(text_yy)s
 31
0.0
 70
    %(text_change_2)s
1
%(text)s
 71
     5
 42
%(dim_distanse)s
  3
ISO-25
100
AcDbAlignedDimension
 13
%(x1)s
 23
%(y1)s
 33
0.0
 14
%(x2)s
 24
%(y2)s
 34
0.0
 50
%(angle)s
100
AcDbRotatedDimension
1001
ACAD
1000
DSTYLE
1002
{
1070
   271
1070
     0
1070
   173
1070
     1
1070
   343
1005
%(handle_block_record_dim_oblique)s
1070
   344
1005
%(handle_block_record_dim_oblique)s
1070
    44
1040
%(vv_s)s
1070
    46
1040
%(vr_s)s
1070
    41
1040
%(arrow_s)s
1070
    42
1040
0.0
1070
   147
1040
%(s)s
1070
   140
1040
%(dim_text_size)s
1070
   279
1070
     %(text_change)s
1002
}
0"""
        self.dxf_block_record_dim = """BLOCK_RECORD
  5
%(handle_block_records_dim)s
330
1
100
AcDbSymbolTableRecord
100
AcDbBlockTableRecord
  2
*%(dim_ind)s
340
0
  0"""
        self.dxf_block_dim = """BLOCK
  5
%(handle_block_dim)s
330
%(handle_block_records_dim)s
100
AcDbEntity
  8
0
100
AcDbBlockBegin
  2
*%(dim_ind)s
 70
     1
 10
0.0
 20
0.0
 30
0.0
  3
*%(dim_ind)s
  1
*%(dim_ind)s
  0"""
        self.dxf_block_dim_line = """LINE
  5
%(handle_block_dim_line)s
330
%(handle_block_records_dim)s
100
AcDbEntity
  8
0
 62
     0
370
    -2
100
AcDbLine
 10
%(line_x1)s
 20
%(line_y1)s
 30
0.0
 11
%(line_x2)s
 21
%(line_y2)s
 31
0.0
  0"""
        self.dxf_block_dim_insert = """INSERT
  5
%(handle_block_dim_insert)s
330
%(handle_block_records_dim)s
100
AcDbEntity
  8
0
 62
     0
370
    -2
100
AcDbBlockReference
  2
_OBLIQUE
 10
%(arrow_x)s
 20
%(arrow_y)s
 30
0.0
 41
%(arrow_s)s
 42
%(arrow_s)s
 43
%(arrow_s)s
 50
%(angle_arrow)s
  0"""

        self.dxf_block_dim_mtext = """MTEXT
  5
%(handle_block_dim_mtext)s
330
%(handle_block_records_dim)s
100
AcDbEntity
  8
0
 62
     0
100
AcDbMText
 10
%(text_xx)s
 20
%(text_yy)s
 30
0.0
 40
%(dim_text_size)s
 41
0.0
 71
     5
 72
     1
  1
%(dim_distanse)s
MY_TEXT_ROTATE
 73
     1
 44
1.0
  0"""

        self.dxf_block_dim_point = """POINT
  5
%(handle_block_dim_point)s
330
%(handle_block_records_dim)s
100
AcDbEntity
  8
Defpoints
 62
     0
100
AcDbPoint
 10
%(point_x)s
 20
%(point_y)s
 30
0.0
  0"""
        self.dxf_endblock_dim = """ENDBLK
  5
%(handle_endblock_dim)s
330
%(handle_block_records_dim)s
100
AcDbEntity
  8
0
100
AcDbBlockEnd
  0"""

        ### BLOCK_OBLIQUE ###

        self.dxf_block_record_dim_oblique = """BLOCK_RECORD
  5
%(handle_block_record_dim_oblique)s
330
1
100
AcDbSymbolTableRecord
100
AcDbBlockTableRecord
  2
_OBLIQUE
340
0
102
{BLKREFS
MY_BLKREFS
102
}
  0"""

        self.dxf_block_dim_oblique = """BLOCK
  5
%(handle_block_dim_oblique)s
330
%(handle_block_record_dim_oblique)s
100
AcDbEntity
  8
0
100
AcDbBlockBegin
  2
_OBLIQUE
 70
     0
 10
0.0
 20
0.0
 30
0.0
  3
_OBLIQUE
  1
_OBLIQUE
  0
LINE
  5
%(handle_oblique_line)s
330
%(handle_block_record_dim_oblique)s
100
AcDbEntity
  8
0
  6
ByBlock
 62
     0
370
    -2
100
AcDbLine
 10
-0.5
 20
-0.5
 30
0.0
 11
0.5
 21
0.5
 31
0.0
  0
ENDBLK
  5
%(handle_endblock_dim_oblique)s
330
%(handle_block_record_dim_oblique)s
100
AcDbEntity
  8
0
100
AcDbBlockEnd
0"""

###        /DIMENSION   ###

        

        
        def hand():
            self.handle = format(int(self.handle,16) + 1, '02x').upper()
            if self.handle in ('BD', '105'):
                self.handle = format(int(self.handle,16) + 1, '02x').upper()

        def widther(w):
            #w = str(i['width'])
            if w in ('1', '1.0'):
                w = '20'
            elif w in ('2', '2.0'):
                w = '30'
            elif w in ('3', '3.0'):
                w = '80'
            elif w in ('4', '4.0'):
                w = '158'
            else:
                w = '20'
            return w

        def formater(i, z=1):
            e = str(format(z*float(i), '.5f'))
            while 1:
                if e[-1] == 0 and e[-2] != '.':
                    e = e[0:-1]
                else:
                    break
            return e

        SECTION_HEADER = open(os.path.join(appPath, 'src', 'dxf_library', 'SECTION_HEADER.txt')).read()
        SECTION_CLASSES = open(os.path.join(appPath, 'src', 'dxf_library', 'SECTION_CLASSES.txt')).read()
        SECTION_TABLES = open(os.path.join(appPath, 'src', 'dxf_library', 'SECTION_TABLES.txt')).read()
        SECTION_BLOCKS = open(os.path.join(appPath, 'src', 'dxf_library', 'SECTION_BLOCKS.txt')).read()
        SECTION_ENTITIES = open(os.path.join(appPath, 'src', 'dxf_library', 'SECTION_ENTITIES.txt')).read()
        SECTION_OBJECTS = open(os.path.join(appPath, 'src', 'dxf_library', 'SECTION_OBJECTS.txt')).read()

        MY_BLOCK_RECORDS = ''
        MY_BLOCKS = ''
        MY_ACAD_REACTORS = ''
        MY_ENTITIES = ''
        MY_ACAD_REACTORS = ''
        MY_BLKREFS = ''
        

        for ind, i in enumerate(self.config_list):
            support = False
            if i['object'] == 'line':
                hand()
                i['handle'] = self.handle
                i['handle2'] = '1F'
                i['width'] = widther(i['width'])
                y1 = i['y1']
                i['y1'] = formater(y1)
                y2 = i['y2']
                i['y2'] = formater(y2)
                x1 = i['x1']
                i['x1'] = formater(x1)
                x2 = i['x2']
                i['x2'] = formater(x2)
                i['factor_stipple'] /= 8.0
                if i['stipple']:
                    
                    if i['stipple'] == (4,1,1,1):
                        i['dash'] = 'CENTER'
                    elif i['stipple'] == (1,1):
                        i['dash'] = 'DASHED'
                    elif i['stipple'] == (4,1,1,1,1,1):
                        i['dash'] = 'PHANTOM'
                else:
                    i['dash'] = 'Continuous'

                support = self.dxf_line

                

            elif i['object'] == 'arc':
                hand()
                i['handle'] = self.handle
                i['width'] = widther(i['width'])
                y1 = i['y1']
                i['y1'] = formater(y1)
                x1 = i['x1']
                i['x1'] = formater(x1)
                support = self.dxf_arc


            elif i['object'] == 'circle':
                hand()
                i['handle'] = self.handle
                i['width'] = widther(i['width'])
                y1 = i['y1']
                i['y1'] = formater(y1)
                x1 = i['x1']
                i['x1'] = formater(x1)
                support = self.dxf_circle

            elif i['object'] == 'text_line':
                hand()
                i['handle'] = self.handle
                y1 = i['y1']
                i['y1'] = formater(y1)
                x1 = i['x1']
                i['x1'] = formater(x1)

                size = i['text_size']
                i['text_size'] = str(size)
                angle = i['angle']
                i['angle'] = str(degrees(-angle))
                text_s_s = i['text_s_s']
                i['text_s_s'] = str(text_s_s*0.57)
                text = i['text']
                i['text'] = text.encode("cp1251")
                
                support = self.dxf_text

            elif i['object'] == 'dim':
                hand()
                i['handle'] = self.handle               
                hand()
                i['handle_block_records_dim'] = self.handle
                hand()
                i['handle_block_dim'] = self.handle
                hand()
                i['handle_endblock_dim'] = self.handle
                hand()
                i['handle_block_dim_line_1'] = self.handle
                hand()
                i['handle_block_dim_line_2'] = self.handle
                hand()
                i['handle_block_dim_line_3'] = self.handle
                hand()
                i['handle_block_dim_insert_1'] = self.handle
                i['handle_block_dim_blkrefs_insert_1'] = self.handle
                hand()
                i['handle_block_dim_insert_2'] = self.handle
                i['handle_block_dim_blkrefs_insert_2'] = self.handle
                hand()
                i['handle_block_dim_mtext'] = self.handle
                hand()
                i['handle_block_dim_point_1'] = self.handle
                hand()
                i['handle_block_dim_point_2'] = self.handle
                hand()
                i['handle_block_dim_point_3'] = self.handle


                dim_ind += 1
                i['dim_ind'] = 'D' + str(dim_ind)
                y1 = i['y1']
                i['y1'] = formater(y1)
                y2 = i['y2']
                i['y2'] = formater(y2)
                y3 = i['y3']
                i['y3'] = formater(y3)
                x1 = i['x1']
                i['x1'] = formater(x1)
                x2 = i['x2']
                i['x2'] = formater(x2)
                x3 = i['x3']
                i['x3'] = formater(x3)

                vr_s = i['vr_s']
                i['vr_s'] = formater(vr_s)
                s = i['arrow_s']
                i['arrow_s'] = s*2.0
                vv_s = i['vv_s']
                i['vv_s'] = formater(vv_s)
                #size = i['dim_text_size']
                #i['dim_text_size'] = str(-float(size))
                w_text = i['dim_text_w']
                i['dim_text_w'] = str(w_text)
                #self.dim_list[i['dim_ind']] = copy(i)
                if i['text']:
                    text = i['text']
                else:
                    text = ''
                i['text'] = text.encode("cp1251")

                if i['text_change'] == 1:
                    i['text_change'] = 0
                    i['text_change_2'] = 32
                    
                elif i['text_change'] == 2:
                    i['text_change'] = 0
                    i['text_change_2'] = 160
                
                elif i['text_change'] == 3:
                    i['text_change'] = 2
                    #Х.З, но без этого при редактировании текст перемещается в середину размера
                    i['text_change_2'] = 160

                e = """330
%(handle)s"""
                e = (e % i)
                MY_ACAD_REACTORS += (e + '\n')

                #BLOCK_RECORDS
                block_record_dim = self.dxf_block_record_dim % i
                MY_BLOCK_RECORDS += (block_record_dim + '\n')
                #BLOCK
                block_dim = (self.dxf_block_dim % i)
                MY_BLOCKS += (block_dim + '\n')
                #LINE x 3
                i['handle_block_dim_line'] = i['handle_block_dim_line_1']
                i['line_x1'] = i['line_1_x1']
                i['line_x2'] = i['line_1_x2']
                i['line_y1'] = i['line_1_y1']
                i['line_y2'] = i['line_1_y2']
                block_dim_line_1 = (self.dxf_block_dim_line % i)
                MY_BLOCKS += (block_dim_line_1 + '\n')
                i['handle_block_dim_line'] = i['handle_block_dim_line_2']
                i['line_x1'] = i['line_2_x1']
                i['line_x2'] = i['line_2_x2']
                i['line_y1'] = i['line_2_y1']
                i['line_y2'] = i['line_2_y2']
                block_dim_line_2 = (self.dxf_block_dim_line % i)
                MY_BLOCKS += (block_dim_line_2 + '\n')
                i['handle_block_dim_line'] = i['handle_block_dim_line_3']
                i['line_x1'] = i['line_3_x1']
                i['line_x2'] = i['line_3_x2']
                i['line_y1'] = i['line_3_y1']
                i['line_y2'] = i['line_3_y2']
                block_dim_line_3 = (self.dxf_block_dim_line % i)
                MY_BLOCKS += (block_dim_line_3 + '\n')
                #INSERT x 2
                i['handle_block_dim_insert'] = i['handle_block_dim_insert_1']
                i['arrow_x'] = i['arrow_point1_x']
                i['arrow_y'] = i['arrow_point1_y']
                i['angle_arrow'] = i['angle_arrow1']
                block_dim_insert_1 = (self.dxf_block_dim_insert % i)
                MY_BLOCKS += (block_dim_insert_1 + '\n')
                i['handle_block_dim_insert'] = i['handle_block_dim_insert_2']
                i['arrow_x'] = i['arrow_point2_x']
                i['arrow_y'] = i['arrow_point2_y']
                i['angle_arrow'] = i['angle_arrow2']
                block_dim_insert_2 = (self.dxf_block_dim_insert % i)
                MY_BLOCKS += (block_dim_insert_2 + '\n')
                #MTEXT
                if i['ort'] == 'horizontal':
                    MY_TEXT_ROTATE = """
 11
0.0
 21
1.0
 31
0.0"""
                else:
                    MY_TEXT_ROTATE = ''
                block_dim_mtext = (self.dxf_block_dim_mtext % i)
                block_dim_mtext = block_dim_mtext.replace('\nMY_TEXT_ROTATE', MY_TEXT_ROTATE)
                MY_BLOCKS += (block_dim_mtext + '\n')
                #POINT x 3
                i['handle_block_dim_point'] = i['handle_block_dim_point_1']
                i['point_x'] = i['line_1_x1']
                i['point_y'] = i['line_1_y1']
                block_dim_point_1 = (self.dxf_block_dim_point % i)
                MY_BLOCKS += (block_dim_point_1 + '\n')
                i['handle_block_dim_point'] = i['handle_block_dim_point_2']
                i['point_x'] = i['line_2_x1']
                i['point_y'] = i['line_2_y1']
                block_dim_point_2 = (self.dxf_block_dim_point % i)
                MY_BLOCKS += (block_dim_point_2 + '\n')
                i['handle_block_dim_point'] = i['handle_block_dim_point_3']
                i['point_x'] = i['arrow_point2_x']
                i['point_y'] = i['arrow_point2_y']
                block_dim_point_3 = (self.dxf_block_dim_point % i)
                MY_BLOCKS += (block_dim_point_3 + '\n')
                #ENDBLOCK
                endblock_dim = (self.dxf_endblock_dim % i)
                MY_BLOCKS += (endblock_dim + '\n')
                if not self._OBLIQUE:
                    hand()
                    i['handle_block_record_dim_oblique'] = self.handle
                    self.handle_block_record_dim_oblique = self.handle
                    hand()
                    i['handle_block_dim_oblique'] = self.handle
                    hand()
                    i['handle_endblock_dim_oblique'] = self.handle
                    hand()
                    i['handle_oblique_line'] = self.handle
                    block_record_dim_oblique = (self.dxf_block_record_dim_oblique % i)
                    MY_BLOCK_RECORDS += (block_record_dim_oblique + '\n')
                    block_dim_oblique = (self.dxf_block_dim_oblique % i)
                    MY_BLOCKS += (block_dim_oblique + '\n')
                    self._OBLIQUE = True
                else: 
                    i['handle_block_record_dim_oblique'] = self.handle_block_record_dim_oblique

                e = """331
%(handle_block_dim_blkrefs_insert_1)s\n"""
                MY_BLKREFS += (e % i)
                e = """331
%(handle_block_dim_blkrefs_insert_2)s\n"""
                MY_BLKREFS += (e % i)
                
                support = self.dxf_dim
                
            if support:
                MY_ENTITIES += (support % i)
                if ind != len(self.config_list)-1:
                    MY_ENTITIES += '\n'
                                

        hand()
        MY_LAST_HANDLE = self.handle
        MY_HANDSEED = 110000

        SECTION_HEADER = SECTION_HEADER.replace('MY_HANDSEED', format(MY_HANDSEED, '02x').upper())
        SECTION_TABLES = SECTION_TABLES.replace('MY_BLOCK_RECORDS\n', MY_BLOCK_RECORDS)
        SECTION_TABLES = SECTION_TABLES.replace('MY_BLKREFS\n', MY_BLKREFS)
        SECTION_BLOCKS = SECTION_BLOCKS.replace('MY_BLOCKS\n', MY_BLOCKS)
        SECTION_ENTITIES = SECTION_ENTITIES.replace('MY_ENTITIES', MY_ENTITIES)
        SECTION_OBJECTS = SECTION_OBJECTS.replace('MY_LAST_HANDLE', MY_LAST_HANDLE)
        SECTION_TABLES = SECTION_TABLES.replace('MY_ACAD_REACTORS', MY_ACAD_REACTORS)
        f = open(file_name, 'w')
        for section in (SECTION_HEADER, SECTION_CLASSES, SECTION_TABLES, SECTION_BLOCKS, SECTION_ENTITIES, SECTION_OBJECTS):
        
            f.writelines("%s\n" % section)

        f.close()
                        
        
