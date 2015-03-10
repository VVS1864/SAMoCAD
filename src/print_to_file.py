# -*- coding: utf-8 -*-
from __future__ import division
import wx
from PIL import Image, ImageDraw


import reportlab
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas

import src.grab_object as grab_object
import src.calc as calc

def print_to(par, rect, ALLOBJECT, scale, f_format, f_name):
    #Печать выделенной области чертежа в растр. или вектор. файл
    objects = grab_object.select(par, rect, master_enclose = False)
    '''
    width_dict = {
        1:1,
        2:2,
        3:4,
        4:6,
        }
    '''
    width_dict = {
        1:0.25,
        2:0.5,
        3:0.8,
        4:1.5,
        }
    rect2 = [
        min(rect[0], rect[2]),
        min(rect[1], rect[3]),
        max(rect[0], rect[2]),
        max(rect[1], rect[3]),
        ]

    

    if f_format == 'PDF':
        
        w = (abs(rect2[0] - rect2[2])/scale)
        h = (abs(rect2[1] - rect2[3])/scale)
        im = canvas.Canvas(f_name, pagesize = (w*mm, h*mm))
        for i in objects:
            if ALLOBJECT[i]['color'] == [255, 255, 255]:
                color = (0, 0, 0)
            else:
                color = tuple(x*1.0/255.0 for x in ALLOBJECT[i]['color'])
            if 'width' in ALLOBJECT[i]:
                width = width_dict[ALLOBJECT[i]['width']]*mm
            else:
                width = width_dict[1]*mm

            if ALLOBJECT[i]['object'] == 'circle':
                x1 = ((ALLOBJECT[i]['x1'] - rect2[0])/scale)*mm
                y1 = ((ALLOBJECT[i]['y1'] - rect2[1])/scale)*mm
                R = (ALLOBJECT[i]['R'] / scale) * mm
                im.setLineWidth(width)
                im.setStrokeColorRGB(*color)
                im.circle(x1, y1, R)

            elif ALLOBJECT[i]['object'] == 'arc':
                
                x1 = ((ALLOBJECT[i]['x1']-ALLOBJECT[i]['R'] - rect2[0])/scale)*mm
                y1 = ((ALLOBJECT[i]['y1']-ALLOBJECT[i]['R'] - rect2[1])/scale)*mm
                x2 = ((ALLOBJECT[i]['x1']+ALLOBJECT[i]['R'] - rect2[0])/scale)*mm
                y2 = ((ALLOBJECT[i]['y1']+ALLOBJECT[i]['R'] - rect2[1])/scale)*mm
                R = (ALLOBJECT[i]['R'] / scale) * mm
                im.setLineWidth(width)
                im.setStrokeColorRGB(*color)
                im.arc(x1, y1, x2, y2, startAng=ALLOBJECT[i]['start'], extent=abs(ALLOBJECT[i]['extent'] - ALLOBJECT[i]['start']))

            else:
                for line in ALLOBJECT[i]['lines']:
                    x1 = ((line[0] - rect2[0])/scale)*mm
                    y1 = ((line[1] - rect2[1])/scale)*mm
                    x2 = ((line[2] - rect2[0])/scale)*mm
                    y2 = ((line[3] - rect2[1])/scale)*mm
                    im.setLineWidth(width)
                    im.setStrokeColorRGB(*color)
                    im.line(x1, y1, x2, y2)

        im.save()

    else:
        scale *= 0.5
        w = int((abs(rect2[0] - rect2[2])/scale)*mm)
        h = int((abs(rect2[1] - rect2[3])/scale)*mm)
        #w = int(abs(rect2[0] - rect2[2])*mm
        #h = int(abs(rect2[1] - rect2[3])//scale)
        im = Image.new("RGB", (w, h), (255,255,255))
        draw = ImageDraw.Draw(im)
        for i in objects:
            color = tuple(ALLOBJECT[i]['color'])
            if color == (255, 255, 255):
                color = (0, 0, 0)

            if 'width' in ALLOBJECT[i]:
                width = int(width_dict[ALLOBJECT[i]['width']]*mm)
            else:
                width = int(width_dict[1]*mm)
            '''
            if 'width' in ALLOBJECT[i]:
                width = int(width_dict[ALLOBJECT[i]['width']]//scale)
            else:
                width = 1
            '''
            if ALLOBJECT[i]['object'] == 'circle':
                lines, p = calc.circle_lines(ALLOBJECT[i]['x1'], ALLOBJECT[i]['y1'], ALLOBJECT[i]['R'], 90)

            elif ALLOBJECT[i]['object'] == 'arc':
                lines, p = calc.oval_lines(
                    ALLOBJECT[i]['x1'],
                    ALLOBJECT[i]['y1'],
                    ALLOBJECT[i]['R'],
                    (ALLOBJECT[i]['start'], ALLOBJECT[i]['extent']),
                    360,
                    ALLOBJECT[i]['x3'],
                    ALLOBJECT[i]['y3'],
                    )
                
            else:
                lines = ALLOBJECT[i]['lines']
            for line in lines:
                x1 = int( ((line[0] - rect2[0])/scale)*mm )
                y1 = int( ((rect2[3] - line[1])/scale)*mm )
                x2 = int( ((line[2] - rect2[0])/scale)*mm )
                y2 = int( ((rect2[3] - line[3])/scale)*mm )

                draw.line((x1, y1, x2, y2), fill = color, width = width)

        del draw
        im.save(f_name, f_format)
        
    print 'Print successfull! File', f_format, f_name 
    

class Select_area:
    def __init__(self, par):
        self.par = par
        self.select_area()
        par.interface.print_dialog.Hide()
        
    def select_area(self):
        self.par.kill()
        self.par.info.SetValue('Print area - point 1:')
        self.par.info2.SetValue('Escape - stop')
        self.par.c.Unbind(wx.EVT_LEFT_DOWN)
        self.par.c.Bind(wx.EVT_LEFT_DOWN, self.select_area_1)
        self.par.current_flag = False

    def select_area_1(self, e):
        self.par.info.SetValue('Print area - point 2:')
        self.par.c.Unbind(wx.EVT_LEFT_DOWN)
        self.par.c.Bind(wx.EVT_LEFT_DOWN, self.select_area_2)
        self.par.rect = True
        self.par.print_flag = True
        self.par.rectx = self.par.x_priv
        self.par.recty = self.par.y_priv
        e.Skip()

    def select_area_2(self, e):
        self.par.rectx2 = self.par.x_priv
        self.par.recty2 = self.par.y_priv
        #self.par.rect = False
        self.par.rect_data = []
        self.par.rect_color = []
        self.par.interface.print_dialog.Show()
        #e.Skip()
        self.par.kill()
        self.par.print_rect = [self.par.rectx, self.par.recty, self.par.rectx2, self.par.recty2]
        
