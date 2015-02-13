# -*- coding: utf-8 -*-
from __future__ import division
import wx
import Image, ImageDraw

import reportlab
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas

import src.grab_object as grab_object

def print_to(par, rect, ALLOBJECT, scale, f_format, f_name):
    #Печать выделенной области чертежа в растр. или вектор. файл
    objects = grab_object.select(par, rect, master_enclose = False)
    width_dict = {
        1:1,
        2:2,
        3:4,
        4:6,
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
                        
            width = ALLOBJECT[i]['width']/scale*mm
            for line in ALLOBJECT[i]['lines']:
                x1 = ((line[0] - rect2[0])/scale)*mm
                y1 = ((line[1] - rect2[1])/scale)*mm
                x2 =( (line[2] - rect2[0])/scale)*mm
                y2 = ((line[3] - rect2[1])/scale)*mm
                im.setLineWidth(width)
                im.setStrokeColorRGB(*color)
                im.line(x1, y1, x2, y2)

        im.save()

    else:
        scale *= 0.1 
        w = int(abs(rect2[0] - rect2[2])//scale)
        h = int(abs(rect2[1] - rect2[3])//scale)
        im = Image.new("RGB", (w, h), (255,255,255))
        draw = ImageDraw.Draw(im)
        for i in objects:
            color = tuple(ALLOBJECT[i]['color'])
            if color == (255, 255, 255):
                color = (0, 0, 0)
            if 'width' in ALLOBJECT[i]:
                width = int(width_dict[ALLOBJECT[i]['width']]//scale)
            else:
                width = 1
                
            for line in ALLOBJECT[i]['lines']:
                x1 = int((line[0] - rect2[0])//scale)
                y1 = int((rect2[3] - line[1])//scale)
                x2 = int((line[2] - rect2[0])//scale)
                y2 = int((rect2[3] - line[3])//scale)

                draw.line((x1, y1, x2, y2), fill = color, width = width)

        del draw
        im.info['dpi'] = (100, 100)
        im.save(f_name, f_format)
    

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
        
