# -*- coding: utf-8; -*-
from math import ceil, degrees
import os
class Base_save(object):
    # Базовый класс сохранения
    def __init__(self, file_format, ALLOBJECT, layers, drawing_w, drawing_h):
        self.AL = ALLOBJECT 
        self.config_list = []
        
        def dxf_colorer(color):
            color_tab = {
                        "white":7,
                        "light blue":4,
                        "blue":5,
                        "green":96,
                        "gray":8,
                        "black":7,
                        "yellow":2,
                        "orange":30,
                        "red":10
                        }
            return color_tab[color]
        
        for obj in self.AL:
            if obj == 'trace':
                continue
            if obj == 'trace_o':
                continue
            config = self.AL[obj]['class'].save(file_format, layers, drawing_w, drawing_h)
            self.config_list.append(config)
        if file_format == 'dxf':
            for i in self.config_list:
                i['color'] = dxf_colorer(i['color'])
                
class Save_to_SVG(Base_save):
    def __init__(self, file_name, file_format, ALLOBJECT, layers, drawing_w, drawing_h):
        self.w = ceil(drawing_w)
        self.h = ceil(drawing_h)
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
                            'drawing_name':os.path.basename(file_name),
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
.st1 {
  fill: none;
  stroke: black;
  stroke-width: 2;
  }
}
]]></style>
</defs>"""
        self.write_list.append(e)
        super(Save_to_SVG, self).__init__(file_format, ALLOBJECT, layers, drawing_w, drawing_h)
        for i in self.config_list:
            strings = i['svg_strings']
            self.write_list.extend(strings)

        e = """</svg>"""
        self.write_list.append(e)

        f = open(file_name, 'w')
        for i in self.write_list:                                        
            f.writelines("%s\n" % i)
        f.close()
        
        
