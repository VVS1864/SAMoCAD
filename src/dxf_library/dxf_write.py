
import src.save_file as save_file
import os
appPath = os.getcwd()

class Save_to_DXF(save_file.Base_save):
    def __init__(self, file_name, file_format, ALLOBJECT, layers, stipples, drawing_w, drawing_h):
        super(Save_to_DXF, self).__init__(file_format, ALLOBJECT, layers, drawing_w, drawing_h)
        self.handle = 'BA'
        self._OBLIQUE = False

        self.dxf_line = """LINE
  5
%(handle)s
330
1F
100
AcDbEntity
  8
0
  6
%(dash)s
 62
  %(color)s
 48
30.0
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
        

        for ind, i in enumerate(self.config_list):
            support = False
            if i['object'] == 'line':
                hand()
                i['handle'] = self.handle
                i['width'] = widther(i['width'])
                y1 = i['y1']
                i['y1'] = formater(y1)
                y2 = i['y2']
                i['y2'] = formater(y2)
                x1 = i['x1']
                i['x1'] = formater(x1)
                x2 = i['x2']
                i['x2'] = formater(x2)
                
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
                
            if support:
                MY_ENTITIES += ((support % i))
                if ind != len(self.config_list)-1:
                    MY_ENTITIES += '\n'
                                

        hand()
        MY_LAST_HANDLE = self.handle
        MY_HANDSEED = 110000

        SECTION_HEADER = SECTION_HEADER.replace('MY_HANDSEED', format(MY_HANDSEED, '02x').upper())
        SECTION_TABLES = SECTION_TABLES.replace('MY_BLOCK_RECORDS', MY_BLOCK_RECORDS)
        SECTION_BLOCKS = SECTION_BLOCKS.replace('MY_BLOCKS', MY_BLOCKS)
        SECTION_ENTITIES = SECTION_ENTITIES.replace('MY_ENTITIES', MY_ENTITIES)
        SECTION_OBJECTS = SECTION_OBJECTS.replace('MY_LAST_HANDLE', MY_LAST_HANDLE)
        SECTION_TABLES = SECTION_TABLES.replace('MY_ACAD_REACTORS', MY_ACAD_REACTORS)
        f = open(file_name, 'w')
        for section in (SECTION_HEADER, SECTION_TABLES, SECTION_BLOCKS, SECTION_ENTITIES, SECTION_OBJECTS):
        
            f.writelines("%s\n" % section)

        f.close()
                        
        
