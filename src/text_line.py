# -*- coding: utf-8; -*-
import src.symbols as symbols
import src.sectors_alg as sectors_alg
import src.save_file as save_file
from math import sqrt, degrees
from os import path
import wx
import calc
from src.base import Base
from src.base_object import Base_object
list_prop = (
    'color',
    'text',
    'layer',
    'angle',
    'anchor',
    'text_size',
    'text_s_s',
    'text_w',
    'text_font',
    'x',
    'y',
    )
temp_dict = {
    'layer' : 't',
    'color' : [255, 255, 0],
    'in_mass' : False,
    'temp' : True,
    }
#ТЕКСТ
#События
class Object(Base):
    def __init__(self, par):
        super(Object, self).__init__(par)
        self.textEvent()
        
    def textEvent(self):
        self.par.kill()
        super(Object, self).func_1(Object, self.textEvent2, 'Text - base point:', 'Escape - stop')

    def textEvent2(self, event = None):
        self.par.ex, self.par.ey = super(Object, self).func_3_r()
        super(Object, self).Y_N(self.textEvent3, 'Text [%s]:' %(self.par.old_text))
        

    def textEvent3(self, event):
        kwargs = {
            'par' : self.par,
            'x' : self.par.ex,
            'y' : self.par.ey,
            'text' : '',
            'anchor' : 'sw',
            'layer' : self.par.layer,
            'color' : self.par.color,
            'angle' : 0,
            'text_size' : self.par.text_size,
            'text_s_s' : self.par.text_s_s,
            'text_w' : self.par.text_w,
            'text_font' : self.par.text_font,
            'in_mass' : False,
            'temp' : False,
            }
        key = event.GetKeyCode()
        if key == wx.WXK_RETURN:
            kwargs['text'] = self.par.cmd.GetValue()
            if kwargs['text'] == '':
                kwargs['text'] = self.par.old_text
            else:
                self.par.old_text = kwargs['text']
            super(Object, self).func_4_r(event, c_text, kwargs)
            self.par.kill()
            return
            
        elif key == wx.WXK_ESCAPE:
            self.par.kill()
        
        else:
            event.Skip()
            return

#Отрисовка
def c_text(
            par,
            x,
            y,
            text,
            anchor,
            layer,
            color,
            angle,
            text_size,
            text_s_s,
            text_w,
            text_font,
            in_mass,
            temp
            ):
    tt = symbols.font(x, y, text, text_size, text_s_s, text_w, anchor, text_font, angle, temp)
    sl = tt.nabor[0]
    if not (0 < sl[0] < par.drawing_w and 0 < sl[1] < par.drawing_h and 0 < sl[2] < par.drawing_w and 0 < sl[3] < par.drawing_h):
        return
    if not temp:
        par.total_N+=1        
        lines = (tt.nabor[1:])
        one = 0
        pointdata = []
        
        for i in tt.nabor[1:]:
            pointdata.extend(i)

        colordata = color*(len(pointdata)/2)
        
        par.gl_wrap.update_pointdata(pointdata, colordata)
        
        object_text = Object_text(par, par.total_N)
        dict_prop = {}
        for k,v in locals().iteritems():
            if k in list_prop:
                dict_prop[k] = v

        par.ALLOBJECT[par.total_N] = {
                                        'object':'text_line',
                                        'class':object_text,
                                        'sectors':[],
                                        'coords': (sl,),
                                        'lines': lines,
                                        'width': 1,
                                        'pointdata': pointdata,
                                        #'x' : x,
                                        #'y' : y,
                                        'snap_type':'line',
                                        }
        par.ALLOBJECT[par.total_N].update(dict_prop)
        if not in_mass:
            par.ALLOBJECT, par.sectors = sectors_alg.quadric_mass(par.ALLOBJECT, [par.total_N,], par.sectors, par.q_scale)
            par.change_pointdata()
            par.c.Refresh()
        return True
    else:
        box = tt.box
        for i in box:
            par.dynamic_data.extend(i)
            par.dynamic_color.extend(color * 2)
    
class Object_text(Base_object):
    def __init__(self, par, obj):
        super(Object_text, self).__init__(par, obj)
        self.text_changeble = True

    def create_object(self, cd):
        cNew = c_text(
            self.par,
            cd['x'],
            cd['y'],
            text = cd['text'],
            anchor = cd['anchor'],
            layer = cd['layer'],
            color = cd['color'],
            angle = cd['angle'],
            text_size = cd['text_size'],
            text_s_s = cd['text_s_s'],
            text_w = cd['text_w'],
            text_font = cd['text_font'],
            in_mass = cd['in_mass'],
            temp = cd['temp'],
            )
        return cNew


    ### Edit_prop method ###
    def save(self, file_format, layers, drawing_w, drawing_h):
        cd = self.par.ALLOBJECT[self.obj].copy()
        cd['x1'] = cd['coords'][0][0]
        cd['y1'] = cd['coords'][0][1]
        cd['Ltext'] = sqrt((cd['coords'][0][0]-cd['coords'][0][2])**2+(cd['coords'][0][1]-cd['coords'][0][3])**2)

        if file_format == 'svg':
            cd['y1'] = drawing_h - cd['coords'][0][1]
            SVG_style_list = []
            en = ' '
            
            color_rgb_str = 'rgb(' + ', '.join([str(x) for x in cd['color']]) + ')'
            cd['angle'] = degrees(float(cd['angle']))
            text = cd['text']
            cd['text'] = text.encode("utf-8")
            cd['text_size'] = str(cd['text_size'])
            if cd['angle']:
                en += '''transform="rotate(%(angle)s, %(x1)s %(y1)s)" '''
            # Перебрать свойства слоя объекта
            SVG_prop = {
                # cd_name : (SVG_name, cd_value)
                'color' : ('fill', color_rgb_str),
                        }
            
            en += save_file.prop_to_svg_style(layers, cd, SVG_prop)
            e = '''<text class="st1" x="%(x1)s" y="%(y1)s" font-size="%(text_size)spx" textLength="%(Ltext)s" lengthAdjust="spacingAndGlyphs"'''+en+'>%(text)s</text>'
            e = (e % cd)
            cd['svg_strings'] = [e,]
            
        return cd

    ### Edit method ###
    def edit(self, x1, y1, x2, y2):
        pass

    def edit_temp(self, x1, y1, x2, y2):
        pass

    ### Rotate methods ###
    def rotate(self, x0, y0, msin, mcos, angle):
        cd = self.par.ALLOBJECT[self.obj].copy()
        coord = list(cd['coords'][0])
        [cd['x'], cd['y'], cd['x2'], cd['y2']] = calc.rotate_lines(x0, y0, [coord,], msin, mcos)[0]
        cd['angle'] += angle
        cd['in_mass'] = True
        cd['temp'] = False
        cNew = self.create_object(cd)
        return cNew

    def rotate_temp(self, x0, y0, msin, mcos, angle):
        cd = self.par.ALLOBJECT[self.obj].copy()
        coord = list(cd['coords'][0])
        [cd['x'], cd['y'], cd['x2'], cd['y2']] = calc.rotate_lines(x0, y0, [coord,], msin, mcos)[0]
        cd['angle'] += angle
        cd.update(temp_dict)
        self.create_object(cd)

    ### Copy method ###    
    def copy(self, d):
        cd = self.par.ALLOBJECT[self.obj].copy()
        cd['x'] += d[0]
        cd['y'] += d[1]
        cd['in_mass'] = True
        cd['temp'] = False
        cNew = self.create_object(cd)
        return cNew

    def copy_temp(self, d):
        cd = self.par.ALLOBJECT[self.obj].copy()
        cd.update(temp_dict)
        cd['x'] += d[0]
        cd['y'] += d[1]
        cNew = self.create_object(cd)        
