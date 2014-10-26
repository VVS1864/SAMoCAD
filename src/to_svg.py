# -*- coding: utf-8; -*-
from save_file import saver
import os
import re
from math import ceil, degrees

class Svger(saver):
    def __init__(self, parent):
        saver.__init__(self, parent)
        self.m = 1.0

        #Определение максимальных координат
        all_o = parent.c.find('all')
        all_el = [x for x in all_o if x != parent.nachCoordy]
        xmax = None
        ymax = None
        xmin = None
        ymin = None
        for i in all_el:
            xy = parent.c.coords(i)
            xm = min(xy[0],xy[2])
            ym = min(xy[1],xy[3])
            xb = max(xy[0],xy[2])
            yb = max(xy[1],xy[3])
            if xmax == None:
                xmin = xm
                ymin = ym
                xmax = xb
                ymax = yb
            if xm<xmin:
                xmin = xm
            if ym<ymin:
                ymin = ym
            if xb>xmax:
                xmax = xb
            if yb>ymax:
                ymax = yb
        self.xmin = xmin
        self.ymin = ymin
        self.w = ceil(abs(xmax-xmin))
        self.h = ceil(abs(ymax-ymin))
        if self.w < 1024:
            self.nx = self.w
            self.ny =  self.h
            self.h *= 1024/self.w
            self.w = 1024
        else:
            mx = 1024/self.w
            self.nx = ceil(self.w/mx)
            self.ny =  ceil(self.h/mx)
        self.drawing_data = {
                            'h':self.h,
                            'w':self.w,
                            'nx':self.nx,
                            'ny':self.ny,
                            'drawing_name':os.path.basename(parent.current_file),
                            }
        self.write_list = []
        self.st0 = {
                    "fill": "white",
                    "width": 2,
                    "stipple":None,
                    }
        
        e = """<svg id="%(drawing_name)s" version="1.1" width="%(w)s" height="%(h)s" viewBox="0 0 %(nx)s %(ny)s" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" type="1">"""
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
.st0 {
  fill: none;
  stroke: black;
  stroke-width: 2;
  }
  
text {
  fill: black;
  font-family: GOST type A, OpenGOST Type A;
  text-decoration: none;
}

.stt0 {}
]]></style>
</defs>"""
        self.write_list.append(e)

        for i in self.config_dict:
            if i[0] == 'L':
                self.config_dict[i]['x1'] = self.scaler(self.config_dict[i]['x1'], 'x')
                self.config_dict[i]['y1'] = self.scaler(self.config_dict[i]['y1'], 'y')
                self.config_dict[i]['x2'] = self.scaler(self.config_dict[i]['x2'], 'x')
                self.config_dict[i]['y2'] = self.scaler(self.config_dict[i]['y2'], 'y')
                """
                self.stipples = {'_____________':None,
                     '_ _ _ _ _ _ _':(1,1),
                     '____ _ ____ _':(4,1,1,1),
                     '____ _ _ ____':(4,1,1,1,1,1)}
                if self.config_dict[i]['stipple']:
                    for j in self.stipples:
                        if self.stipples[j]:
                            t = map(lambda x: x*float(self.AL[i]['factor_stip']), self.stipples[j])
                            if t == self.AL[i]['stipple']:
                                stip = j
                                break
                    if stip == '____ _ ____ _':
                        self.config_dict[i]['dash'] = 'lt3'
                    elif stip == '_ _ _ _ _ _ _':
                        self.config_dict[i]['dash'] = 'lt4'
                    elif stip == '____ _ _ ____':
                        self.config_dict[i]['dash'] = 'lt8'
                
                else:
                    self.config_dict[i]['dash'] = 'lt2'
                """
                en_list = self.opt_control(self.config_dict[i], 'line')
                en = ' '
                if en_list:
                    en += ''.join(en_list)
                        
                ###здесь будет код если class!="st0"###
                
                e = '''<line class="st0" x1="%(x1)s" y1="%(y1)s" x2="%(x2)s" y2="%(y2)s"'''+en+"/>"
                e = (e % self.config_dict[i])     
                self.write_list.append(e)

            elif i[0] == 'c':
                self.config_dict[i]['x0'] = self.scaler(self.config_dict[i]['x0'], 'x')
                self.config_dict[i]['y0'] = self.scaler(self.config_dict[i]['y0'], 'y')
                self.config_dict[i]['R'] /= self.m
                en_list = self.opt_control(self.config_dict[i], 'circle')
                en = ' '
                if en_list:
                    en += ''.join(en_list)
                e = '''<circle class="st0" cx="%(x0)s" cy="%(y0)s" r="%(R)s"'''+en+"/>"
                e = (e % self.config_dict[i])     
                self.write_list.append(e)

            elif i[0] == 't':
                self.config_dict[i]['x'] = self.scaler(self.config_dict[i]['x'], 'x')
                self.config_dict[i]['y'] = self.scaler(self.config_dict[i]['y'], 'y')
                self.config_dict[i]['angle'] = degrees(-float(self.config_dict[i]['angle']))
                text = self.config_dict[i]['text']
                self.config_dict[i]['text'] = text.encode("utf-8")
                size = self.config_dict[i]['size']
                self.config_dict[i]['size'] = str(-float(size)/self.m)
                en = ' '
                if float(self.config_dict[i]['angle']):
                    en += '''transform="rotate(%(angle)s, %(x)s %(y)s)" '''
                en_list = self.opt_control(self.config_dict[i], 'text')
                if en_list:
                    en += ''.join(en_list)
                    
                e = '''<text class="stt0" x="%(x)s" y="%(y)s" font-size="%(size)spx" textLength="%(Ltext)s" lengthAdjust="spacingAndGlyphs"'''+en+'>%(text)s</text>'
                e = (e % self.config_dict[i])     
                self.write_list.append(e)

            elif i[0] == 'd':
                self.config_dict[i]['line_1_x1'] = self.scaler(self.config_dict[i]['line_1_x1'], 'x')
                self.config_dict[i]['line_1_x2'] = self.scaler(self.config_dict[i]['line_1_x2'], 'x')
                self.config_dict[i]['line_1_y1'] = self.scaler(self.config_dict[i]['line_1_y1'], 'y')
                self.config_dict[i]['line_1_y2'] = self.scaler(self.config_dict[i]['line_1_y2'], 'y')

                self.config_dict[i]['line_2_x1'] = self.scaler(self.config_dict[i]['line_2_x1'], 'x')
                self.config_dict[i]['line_2_x2'] = self.scaler(self.config_dict[i]['line_2_x2'], 'x')
                self.config_dict[i]['line_2_y1'] = self.scaler(self.config_dict[i]['line_2_y1'], 'y')
                self.config_dict[i]['line_2_y2'] = self.scaler(self.config_dict[i]['line_2_y2'], 'y')

                self.config_dict[i]['line_3_x1'] = self.scaler(self.config_dict[i]['line_3_x1'], 'x')
                self.config_dict[i]['line_3_x2'] = self.scaler(self.config_dict[i]['line_3_x2'], 'x')
                self.config_dict[i]['line_3_y1'] = self.scaler(self.config_dict[i]['line_3_y1'], 'y')
                self.config_dict[i]['line_3_y2'] = self.scaler(self.config_dict[i]['line_3_y2'], 'y')

                self.config_dict[i]['text_x'] = self.scaler(self.config_dict[i]['text_x'], 'x')
                self.config_dict[i]['text_y'] = self.scaler(self.config_dict[i]['text_y'], 'y')

                self.config_dict[i]['arrow_1_x1'] = self.scaler(self.config_dict[i]['arrow_1_x1'], 'x')
                self.config_dict[i]['arrow_1_x2'] = self.scaler(self.config_dict[i]['arrow_1_x2'], 'x')
                self.config_dict[i]['arrow_1_y1'] = self.scaler(self.config_dict[i]['arrow_1_y1'], 'y')
                self.config_dict[i]['arrow_1_y2'] = self.scaler(self.config_dict[i]['arrow_1_y2'], 'y')

                self.config_dict[i]['arrow_2_x1'] = self.scaler(self.config_dict[i]['arrow_2_x1'], 'x')
                self.config_dict[i]['arrow_2_x2'] = self.scaler(self.config_dict[i]['arrow_2_x2'], 'x')
                self.config_dict[i]['arrow_2_y1'] = self.scaler(self.config_dict[i]['arrow_2_y1'], 'y')
                self.config_dict[i]['arrow_2_y2'] = self.scaler(self.config_dict[i]['arrow_2_y2'], 'y')

                self.config_dict[i]['angle'] = -float(self.config_dict[i]['angle'])
                self.config_dict[i]['size'] = str(-float(self.config_dict[i]['size'])/self.m)
                
                en_list1 = self.opt_control(self.config_dict[i], 'line')
                en_list2 = self.opt_control(self.config_dict[i], 'text')
                en1 = ''
                en2 = ''
                if en_list1:
                    en1 = ' ' + ''.join(en_list1)
                if en_list2:
                    en2 = ' ' + ''.join(en_list2)
                e0 = '''<g class="DimL">'''
                e1 = '''<line class="st0" x1="%(line_1_x1)s" y1="%(line_1_y1)s" x2="%(line_1_x2)s" y2="%(line_1_y2)s"'''+en1+"/>"
                e2 = '''<line class="st0" x1="%(line_2_x1)s" y1="%(line_2_y1)s" x2="%(line_2_x2)s" y2="%(line_2_y2)s"'''+en1+"/>"
                e3 = '''<line class="st0" x1="%(line_3_x1)s" y1="%(line_3_y1)s" x2="%(line_3_x2)s" y2="%(line_3_y2)s"'''+en1+"/>"
                if self.config_dict[i]['angle'] not in ('0.0', '0'):
                    e4 = '''<text class="stt0" x="%(text_x)s" y="%(text_y)s" font-size="%(size)spx"   textLength="%(Ltext)s" lengthAdjust="spacingAndGlyphs" transform="rotate(%(angle)s, %(text_x)s %(text_y)s)" '''+en2+'>%(dim_distanse)s</text>'
                else:
                    e4 = '''<text class="stt0" x="%(text_x)s" y="%(text_y)s" font-size="%(size)spx" textLength="%(Ltext)s" lengthAdjust="spacingAndGlyphs"'''+en2+'>%(text)s</text>'
                if self.config_dict[i]['type_arrow'] != 'Arch':
                    self.config_dict[i]['arrow_3_x1'] = self.scaler(self.config_dict[i]['arrow_3_x1'], 'x')
                    self.config_dict[i]['arrow_3_x2'] = self.scaler(self.config_dict[i]['arrow_3_x2'], 'x')
                    self.config_dict[i]['arrow_3_y1'] = self.scaler(self.config_dict[i]['arrow_3_y1'], 'y')
                    self.config_dict[i]['arrow_3_y2'] = self.scaler(self.config_dict[i]['arrow_3_y2'], 'y')
                    
                    self.config_dict[i]['arrow_4_x1'] = self.scaler(self.config_dict[i]['arrow_4_x1'], 'x')
                    self.config_dict[i]['arrow_4_x2'] = self.scaler(self.config_dict[i]['arrow_4_x2'], 'x')
                    self.config_dict[i]['arrow_4_y1'] = self.scaler(self.config_dict[i]['arrow_4_y1'], 'y')
                    self.config_dict[i]['arrow_4_y2'] = self.scaler(self.config_dict[i]['arrow_4_y2'], 'y')
                    
                    a1 = '''<line class="st0" x1="%(arrow_1_x1)s" y1="%(arrow_1_y1)s" x2="%(arrow_1_x2)s" y2="%(arrow_1_y2)s"'''+en1+"/>"
                    a2 = '''<line class="st0" x1="%(arrow_2_x1)s" y1="%(arrow_2_y1)s" x2="%(arrow_2_x2)s" y2="%(arrow_2_y2)s"'''+en1+"/>"
                    a3 = '''<line class="st0" x1="%(arrow_3_x1)s" y1="%(arrow_3_y1)s" x2="%(arrow_3_x2)s" y2="%(arrow_3_y2)s"'''+en1+"/>"
                    a4 = '''<line class="st0" x1="%(arrow_4_x1)s" y1="%(arrow_4_y1)s" x2="%(arrow_4_x2)s" y2="%(arrow_4_y2)s"'''+en1+"/>"
                else:
                    a1 = '''<line class="st0" x1="%(arrow_1_x1)s" y1="%(arrow_1_y1)s" x2="%(arrow_1_x2)s" y2="%(arrow_1_y2)s"'''+en1+"/>"
                    a2 = '''<line class="st0" x1="%(arrow_2_x1)s" y1="%(arrow_2_y1)s" x2="%(arrow_2_x2)s" y2="%(arrow_2_y2)s"'''+en1+"/>"
                    a3 = ''
                    a4 = ''

                
                e5 = '</g>'
                e = [x % self.config_dict[i] for x in (e0, e1, e2, e3, e4, a1, a2, a3, a4, e5) if x]
                self.write_list.extend(e)

            elif i[0] == 'r':
                self.config_dict[i]['line_1_x1'] = self.scaler(self.config_dict[i]['line_1_x1'], 'x')
                self.config_dict[i]['line_1_x2'] = self.scaler(self.config_dict[i]['line_1_x2'], 'x')
                self.config_dict[i]['line_1_y1'] = self.scaler(self.config_dict[i]['line_1_y1'], 'y')
                self.config_dict[i]['line_1_y2'] = self.scaler(self.config_dict[i]['line_1_y2'], 'y')
                
                self.config_dict[i]['text_x'] = self.scaler(self.config_dict[i]['text_x'], 'x')
                self.config_dict[i]['text_y'] = self.scaler(self.config_dict[i]['text_y'], 'y')
                self.config_dict[i]['angle'] = degrees(-float(self.config_dict[i]['angle']))
                self.config_dict[i]['size'] = str(-float(self.config_dict[i]['size'])/self.m)
                
                en_list1 = self.opt_control(self.config_dict[i], 'line')
                en_list2 = self.opt_control(self.config_dict[i], 'text')
                en1 = ''
                en2 = ''
                if en_list1:
                    en1 = ' ' + ''.join(en_list1)
                if en_list2:
                    en2 = ' ' + ''.join(en_list2)
                e0 = '''<g class="DimR">'''
                e1 = '''<line class="st0" x1="%(line_1_x1)s" y1="%(line_1_y1)s" x2="%(line_1_x2)s" y2="%(line_1_y2)s"'''+en1+"/>"
                e2 = '''<text class="stt0" x="%(text_x)s" y="%(text_y)s" font-size="%(size)spx" transform="rotate(%(angle)s, %(text_x)s %(text_y)s)" textLength="%(Ltext)s" lengthAdjust="spacingAndGlyphs"'''+en2+'>%(text)s</text>'

                self.config_dict[i]['arrow_1_x1'] = self.scaler(self.config_dict[i]['arrow_1_x1'], 'x')
                self.config_dict[i]['arrow_1_x2'] = self.scaler(self.config_dict[i]['arrow_1_x2'], 'x')
                self.config_dict[i]['arrow_1_y1'] = self.scaler(self.config_dict[i]['arrow_1_y1'], 'y')
                self.config_dict[i]['arrow_1_y2'] = self.scaler(self.config_dict[i]['arrow_1_y2'], 'y')

                if self.config_dict[i]['type_arrow'] != 'Arch':
                    self.config_dict[i]['arrow_2_x1'] = self.scaler(self.config_dict[i]['arrow_2_x1'], 'x')
                    self.config_dict[i]['arrow_2_x2'] = self.scaler(self.config_dict[i]['arrow_2_x2'], 'x')
                    self.config_dict[i]['arrow_2_y1'] = self.scaler(self.config_dict[i]['arrow_2_y1'], 'y')
                    self.config_dict[i]['arrow_2_y2'] = self.scaler(self.config_dict[i]['arrow_2_y2'], 'y')
                                        
                    a1 = '''<line class="st0" x1="%(arrow_1_x1)s" y1="%(arrow_1_y1)s" x2="%(arrow_1_x2)s" y2="%(arrow_1_y2)s"'''+en1+"/>"
                    a2 = '''<line class="st0" x1="%(arrow_2_x1)s" y1="%(arrow_2_y1)s" x2="%(arrow_2_x2)s" y2="%(arrow_2_y2)s"'''+en1+"/>"
                else:
                    a1 = '''<line class="st0" x1="%(arrow_1_x1)s" y1="%(arrow_1_y1)s" x2="%(arrow_1_x2)s" y2="%(arrow_1_y2)s"'''+en1+"/>"
                    a2 = ''
                    
                e3 = '</g>'
                e = [x % self.config_dict[i] for x in (e0, e1, e2, a1, a2, e3) if x]
                self.write_list.extend(e)

            elif i[0] == 'a':
                self.config_dict[i]['xr1'] = self.scaler(self.config_dict[i]['xr1'], 'x')
                self.config_dict[i]['yr1'] = self.scaler(self.config_dict[i]['yr1'], 'y')
                self.config_dict[i]['xr2'] = self.scaler(self.config_dict[i]['xr2'], 'x')
                self.config_dict[i]['yr2'] = self.scaler(self.config_dict[i]['yr2'], 'y')
                en_list = self.opt_control(self.config_dict[i], 'arc')
                en = ' '
                if en_list:
                    en += ''.join(en_list)

                if self.config_dict[i]['extent']<0:
                    self.config_dict[i]['sf'] = 0
                else:
                    self.config_dict[i]['sf'] = 1
                
                        
                e = '''<path class="st0" d="M%(xr2)s,%(yr2)s A%(R)s,%(R)s 0 0 %(sf)s %(xr1)s,%(yr1)s"'''+en+'/>'
                e = (e % self.config_dict[i])     
                self.write_list.append(e)




                
        e = """</svg>"""
        self.write_list.append(e)

    def scaler(self, coord, xy):
        if xy == 'x':
            coord -= self.xmin
        else:
            coord -= self.ymin
        return coord/self.m

    def opt_control(self, config_dict_o, type_o):
        en_list = []
        for i in self.st0:
            try:
                config_dict_o[i]
            except:
                continue
            if config_dict_o[i] != self.st0[i]:
                if i == "fill":
                    re_two_words = re.compile('([\w]+) ([\w]+)')
                    find = re_two_words.search(config_dict_o[i])
                    if find:
                        config_dict_o[i] = ''.join(find.groups())
                        
                    if type_o in ('circle', 'line', 'arc'):
                        en = ("stroke: %(fill)s;") % config_dict_o
                    elif type_o == 'text':
                        en = ("fill: %(fill)s;") % config_dict_o
                elif i == "width":
                    en = ("stroke-width: %(width)s;") % config_dict_o
                elif i == "stipple":
                    d = [str(x*config_dict_o['factor_stip']/self.m) for x in config_dict_o['stipple']]
                    d = ', '.join(d)
                    dash = {'stipple':d}
                    en = ("stroke-dasharray: %(stipple)s;") % dash
                try:
                    en_list.append(en)
                except:
                    print ("error", ' ', i)
        if en_list:
            en_list.insert(0, '''style="''')
            en_list.append('''"''')   
        return en_list

        
        
            
            
        
        
