# -*- coding: utf-8; -*-
import symbols
import src.sectors_alg as sectors_alg
import src.save_file as save_file
from math import sqrt, degrees#, sin, cos
from os import path
import wx
import calc
from base import Base
#from object_object import Root_object
list_prop = ('color', 'text', 'layer', 'angle', 'anchor', 'text_size', 'text_s_s', 'text_w', 'text_font')
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
        
        if event:            
            if event.GetEventType() == wx.wxEVT_LEFT_DOWN:
                super(Object, self).Y_N(self.textEvent3, 'Text [%s]:' %(self.par.old_text))
            else:
                self.textEvent3(event)
        else:
            self.textEvent3(event)
        '''
        self.par.ex=self.par.priv_coord[0]
        self.par.ey=self.par.priv_coord[1]
        self.par.set_coord()
        self.par.dialog.config(text = (u'Text [%s]:') %(self.par.old_text))
        self.par.info.config(text = u'//a - Snap text. Escape - stop')
        self.par.command.focus_set()
        self.par.c.bind_class(self.par.master1,"<Return>",self.risText3)
        '''

    def textEvent3(self, event=None):
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
        if event and event.GetEventType() == wx.wxEVT_KEY_DOWN:
            key = event.GetKeyCode()
            if key == wx.WXK_RETURN:
                kwargs['text'] = self.par.cmd.GetValue()
                if kwargs['text'] == '':
                    kwargs['text'] = self.par.old_text
                else:
                    self.par.old_text = kwargs['text']
                super(Object, self).func_4_r(event, c_text, kwargs)
                self.par.kill()
                
            elif key == wx.WXK_ESCAPE:
                self.par.kill()
            
            else:
                event.Skip()
                return
            
            
            




        '''
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        self.par.com=self.par.command.get()
        if self.par.anchorFlag == False:
            if self.par.com == '//a':
                self.par.anchorFlag = True
                self.par.dialog.config(text = 'Snap text point (s/n | w/e/c):')
                self.par.info.config(text = 'Escape - stop')
                self.par.command.delete(0,END)
            else:
                if self.par.com != '':
                    text = self.par.com
                    self.par.old_text = self.par.com
                else:
                    text = self.par.old_text
                c_text(self.par, self.par.ex, self.par.ey, text, self.par.anchor)
                self.par.changeFlag = True
                self.par.enumerator_p()
                self.par.history_undo.append(('c_', self.par.Ntext))
                self.par.kill()

        else:
            if self.par.com == 'sw' or self.par.com == 'se' or self.par.com == 'sc' or self.par.com == 'nw' or self.par.com == 'ne' or self.par.com == 'nc':
                self.par.anchor = self.par.com
                self.par.anchorFlag = False
                self.par.dialog.config(text = 'Text:')
                self.par.info.config(text = '//a - Snap text. Escape - stop')
                self.par.command.delete(0,END)
            else:
                self.par.info.config(text = ("Unknow command '%s'. Escape - stop") %(self.par.com))
                self.par.command.delete(0,END)
        '''

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
        for i in tt.nabor[1:]:
            par.pointdata.extend(i)
            par.colordata.extend(color * 2)
            if one:
                par.IDs.append(0)
            else:
                par.IDs.append(par.total_N)
                one = 1

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
                                        }
        par.ALLOBJECT[par.total_N].update(dict_prop)
        if not in_mass:
            par.ALLOBJECT, par.sectors = sectors_alg.quadric_mass(par.ALLOBJECT, [par.total_N,], par.sectors, par.q_scale)
            par.change_pointdata()
            par.c.Refresh()
    else:
        box = tt.box
        for i in box:
            par.dynamic_data.extend(i)
            par.dynamic_color.extend(color * 2)
    '''
    if sloy == None:
        sloy = par.sloy
        fill = par.color
        size = par.size_t
        s_s = par.s_s
        w_text = par.w_text
        font = par.font
    if not temp:
        par.Ntextd += 1
        par.Ntext = 't' + str(par.Ntextd)
        x = float(x)
        y = float(y)
        size = float(size)
        tt = symbols.font(x, y, text, size, par.zoomOLD, s_s, w_text, anchor, font, angle)
        # Не брать первую линию - это привязка
        id_dict = {}
        for i in tt.nabor[1:]: #Перебрать координаты линий текста, нарисовать линии
            try:
                id = par.c.create_line(i[0],i[1],i[2],i[3],fill=fill, tags = ('obj', par.Ntext, 't_LOD', 'sel'))#['ltext', par.Ntext, 'line', 'obj',  sloy])
                id_dict[id] = ('line',)
            except:
                pass
        #Линия привязки
        id = par.c.create_line(tt.nabor[0][0],tt.nabor[0][1],tt.nabor[0][2],tt.nabor[0][3], width=8, fill = fill, stipple = ('@'+path.join(par.appPath, 'res', '00.xbm')), tags = ('obj', par.Ntext, 'snap_text', 'sel'))#'ltext', par.Ntext, 'line', 'obj', 'priv', par.Ntext+'xy'#, sloy])
        id_dict[id] = ('line', 'priv')
        
        object_text = Object_text(par, par.Ntext)
        #dict_prop = {k:v for k,v in locals().iteritems() if k in list_prop}
        dict_prop = {}
        for k,v in locals().iteritems():
            if k in list_prop:
                dict_prop[k] = v
        par.ALLOBJECT[par.Ntext]={
                                'object':'text',
                                'Ltext':tt.Ltext,
                                'id':id_dict,
                                'class':object_text,
                                }
        par.ALLOBJECT[par.Ntext].update(dict_prop)
        return id_dict

    else:
        x = float(x)
        y = float(y)
        size = float(size)
        tt = symbols.font(x, y, text, size, par.zoomOLD, s_s, w_text, anchor, font, angle)
        # Не брать первую линию - это привязка
        id_dict = {}
        #Перебрать координаты линий текста, нарисовать линии
        for i in tt.nabor[1:]: 
            try:
                par.c.create_line(i[0],i[1],i[2],i[3],fill=fill, tags = ('obj', 'temp'))
            except:
                pass
        #Линия привязки
        par.c.create_line(tt.nabor[0][0],tt.nabor[0][1],tt.nabor[0][2],tt.nabor[0][3], width=8, fill = fill, stipple = ('@'+path.join(par.appPath, 'res', '00.xbm')), tags = ('obj', 'temp'))
        '''
class Object_text:
    def __init__(self, par, obj):
        self.par = par
        self.obj = obj

    ### History_undo method ###
    def undo(self, cd, zoomOLDres, xynachres):
        cd['x1'], cd['y1'] = self.par.coordinator(cd['coord'][0], cd['coord'][1], zoomOLDres = zoomOLDres, xynachres = xynachres)
        c_text(self.par, cd['x1'], cd['y1'],
               cd['text'],
               cd['anchor'],
               cd['sloy'],
               cd['fill'],
               cd['angle'],
               cd['size'],
               cd['s_s'],
               cd['w_text'],
               cd['font'],
               )

    ### Edit_prop method ###
    def save(self, file_format, layers, drawing_w, drawing_h):
        cd = self.par.ALLOBJECT[self.obj].copy()
        cd['x1'] = cd['coords'][0][0]
        cd['y1'] = drawing_h - cd['coords'][0][1]
        cd['Ltext'] = sqrt((cd['coords'][0][0]-cd['coords'][0][2])**2+(cd['coords'][0][1]-cd['coords'][0][3])**2)

        if file_format == 'svg':
            SVG_style_list = []
            en = ' '
            
            color_rgb_str = 'rgb(' + ', '.join([str(x) for x in cd['color']]) + ')'
            cd['angle'] = degrees(-float(cd['angle']))
            text = cd['text']
            cd['text'] = text.encode("utf-8")
            cd['text_size'] = str(cd['text_size'])
            if cd['angle']:
                en += '''transform="rotate(%(angle)s, %(x1)s %(y1)s)" '''
            # Перебрать свойства слоя объекта
            SVG_prop = {
                # cd_name : (SVG_name, cd_value)
                'color' : ('fill', color_rgb_str),
                #'width' : ('stroke-width', cd['width']),
                #'stipple' : ('stroke-dasharray', dash_str),
                #'factor_stipple' : ('stroke-dasharray', dash_str),
                        }
            
            en = save_file.prop_to_svg_style(layers, cd, SVG_prop)
            e = '''<text class="st1" x="%(x1)s" y="%(y1)s" font-size="%(text_size)spx" textLength="%(Ltext)s" lengthAdjust="spacingAndGlyphs"'''+en+'>%(text)s</text>'
            e = (e % cd)
            cd['svg_strings'] = [e,]
            
        return cd

        
    
    ### Edit_prop method ###
    def edit_prop(self, params):
        param_changed = False
        r_list = None
        cd = self.get_conf()
        for param in params:
            if param in cd:
                param_changed = True
                cd[param] = params[param]
        if param_changed == True:
            c_text(self.par, cd['coord'][0], cd['coord'][1],
               cd['text'],
               cd['anchor'],
               cd['sloy'],
               cd['fill'],
               cd['angle'],
               cd['size'],
               cd['s_s'],
               cd['w_text'],
               cd['font'],
               )
            
            r_list = (self.obj, self.par.Ntext)
        return r_list

    ### Edit method ###
    def edit(self, event):
        pass

    ### Rotate methods ###
    def rotate(self, x0, y0, msin, mcos, angle):
        cd = self.par.ALLOBJECT[self.obj]
        coord = list(cd['coords'][0])
        coord = calc.rotate_lines(x0, y0, [coord,], msin, mcos)[0]
        angle += cd['angle']
        c_text(self.par, coord[0], coord[1],
               text = cd['text'],
               anchor = cd['anchor'],
               layer = cd['layer'],
               color = cd['color'],
               angle = angle,
               text_size = cd['text_size'],
               text_s_s = cd['text_s_s'],
               text_w = cd['text_w'],
               text_font = cd['text_font'],
               in_mass = True,
               temp = False,
               )

    def rotate_temp(self, x0, y0, msin, mcos, angle):
        cd = self.par.ALLOBJECT[self.obj]
        coord = list(cd['coords'][0])
        coord = calc.rotate_lines(x0, y0, [coord,], msin, mcos)[0]
        angle += cd['angle']
        c_text(self.par, coord[0], coord[1],
               text = cd['text'],
               anchor = cd['anchor'],
               layer = cd['layer'],
               color = [255, 255, 0],
               angle = angle,
               text_size = cd['text_size'],
               text_s_s = cd['text_s_s'],
               text_w = cd['text_w'],
               text_font = cd['text_font'],
               in_mass = True,
               temp = True,
               )

    ### Offset method ###
    def offset(self, pd, x3, y3):
        pass

    ### Rotate methods ###    
    def mirror(self, x0, y0, msin, mcos):
        pass

    def mirror_temp(self, x0, y0, msin, mcos):
        pass

    ### Copy method ###    
    def copy(self, d):
        cd = self.par.ALLOBJECT[self.obj]
        x = cd['coords'][0][0] + d[0]
        y = cd['coords'][0][1] + d[1]
        c_text(self.par, x, y,
               text = cd['text'],
               anchor = cd['anchor'],
               layer = cd['layer'],
               color = cd['color'],
               angle = cd['angle'],
               text_size = cd['text_size'],
               text_s_s = cd['text_s_s'],
               text_w = cd['text_w'],
               text_font = cd['text_font'],
               in_mass = True,
               temp = False,
               )

    def copy_temp(self, d):
        cd = self.par.ALLOBJECT[self.obj]
        coord = list(self.par.ALLOBJECT[self.obj]['coords'][0])
        x = coord[0] + d[0]
        y = coord[1] + d[1]
        c_text(self.par, x, y,
               text = cd['text'],
               anchor = cd['anchor'],
               layer = 't',
               color = [255, 255, 0],
               angle = cd['angle'],
               text_size = cd['text_size'],
               text_s_s = cd['text_s_s'],
               text_w = cd['text_w'],
               text_font = cd['text_font'],
               in_mass = True,
               temp = True,
               )
        
