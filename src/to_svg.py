# -*- coding: utf-8; -*-
from save_file import saver
import os
from math import ceil, degrees

class Svger(saver):
    def __init__(self, parent):
        saver.__init__(self, parent)

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
        
        e = """<svg id="%(drawing_name)s" version="1.1" width="%(w)s" height="%(h)s" viewBox="0, 0, %(nx)s, %(ny)s" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">"""
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
  stroke-width: 1;
  }
]]></style>
</defs>"""
        self.write_list.append(e)

        for i in self.config_dict:
            if i[0] == 'L':
                self.config_dict[i]['x1']-=self.xmin
                self.config_dict[i]['y1']-=self.ymin
                self.config_dict[i]['x2']-=self.xmin
                self.config_dict[i]['y2']-=self.ymin
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
                en_list = self.opt_control(self.config_dict[i])
                en = ''
                if en_list:
                    for opt in en_list:
                        en += opt
                        
                ###здесь будет код если class!="st0"###
                
                e = '''<line class="st0" x1="%(x1)s" y1="%(y1)s" x2="%(x2)s" y2="%(y2)s"'''+" "+en+"/>"
                e = (e % self.config_dict[i])     
                self.write_list.append(e)

            if i[0] == 'c':
                self.config_dict[i]['x0']-=self.xmin
                self.config_dict[i]['y0']-=self.ymin
                e = """<circle class="st0" cx="%(x0)s" cy="%(y0)s" r="%(R)s"/>"""
                e = (e % self.config_dict[i])     
                self.write_list.append(e)

            if i[0] == 't':
                self.config_dict[i]['x']-=self.xmin
                self.config_dict[i]['y']-=self.ymin
                self.config_dict[i]['angle'] = degrees(float(self.config_dict[i]['angle']))
                text = self.config_dict[i]['text']
                self.config_dict[i]['text'] = text.encode("utf-8")
                size = self.config_dict[i]['size']
                self.config_dict[i]['size'] = str(-float(size))
                e = """<text class="st0" x="%(x)s" y="%(y)s" font-size="%(size)spx" transform="rotate(%(angle)s, %(x)s %(y)s)">%(text)s</text>"""
                e = (e % self.config_dict[i])     
                self.write_list.append(e)
        e = """</svg>"""
        self.write_list.append(e)

    def opt_control(self, config_dict_o):
        en_list = []
        for i in self.st0:
            if config_dict_o[i] != self.st0[i]:
                if i == "fill":
                    en = ("stroke: %(fill)s;") % config_dict_o
                elif i == "width":
                    en = ("stroke-width: %(width)s;") % config_dict_o
                elif i == "stipple":
                    d = [str(x/20.0) for x in config_dict_o['stipple']]
                    d = ', '.join(d)
                    dash = {'stipple':d}
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
                    en = ("stroke-dasharray: %(stipple)s;") % dash
                try:
                    en_list.append(en)
                except:
                    print "error", ' ', i
        if en_list:
            en_list.insert(0, '''style="''')
            en_list.append('''"''')   
        return en_list

        
        
            
            
        
        
