# -*- coding: utf-8; -*-
import symbols
from os import path
from object_object import Root_object
list_prop = ('fill', 'text', 'sloy', 'angle', 'anchor', 'size', 's_s', 'w_text', 'font')
#ТЕКСТ
#События
class Text:
    def __init__(self, par):
        self.par = par
        self.risText()
        
    def risText(self):
        self.par.kill()
        self.par.standart_unbind()
        self.par.old_func = 'self.risText()'
        self.par.c.bind('<Button-1>', self.risText2)
        self.par.dialog.config(text = u'Text - base point:')
        self.par.info.config(text = u'Escape - stop')

    def risText2(self, event = None):
        self.par.ex=self.par.priv_coord[0]
        self.par.ey=self.par.priv_coord[1]
        self.par.set_coord()
        self.par.dialog.config(text = (u'Text [%s]:') %(self.par.old_text))
        self.par.info.config(text = u'//a - Snap text. Escape - stop')
        self.par.command.focus_set()
        self.par.c.bind_class(self.par.master1,"<Return>",self.risText3)

    def risText3(self, event=None):
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

#Отрисовка
def c_text(par, x, y, text, anchor = 'sw', sloy = None, fill = None, angle = 0, size = None, s_s = None, w_text = None, font = None, temp = None): 
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
        object_text = Object_text()
        '''
        'anchor':anchor,
        'text':text,
        
        'fill':fill,
        
        'angle':angle,
        'size':size,
        'sloy':sloy,
        's_s':s_s,
        'w_text':w_text,
        'font':font,
        '''
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
        
class Object_text(Root_object):
    def copy(self, par, content, d):
        cd = self.get_conf(content, par)
        cd['coord'] = [y+d[0] if ind%2 == 0 else y+d[1] for ind, y in enumerate(cd['coord'][0:2])]
        c_text(par, cd['coord'][0], cd['coord'][1],
               cd['text'],
               cd['anchor'],
               cd['sloy'],
               cd['fill'],
               cd['angle'],
               cd['size'],
               cd['s_s'],
               cd['w_text'],
               cd['font'])

    def get_conf(self, obj, par):#Принимает объект - текст, возвращает все его свойства
         
        Root_object.from_AL(self, par.ALLOBJECT, obj, list_prop)
        '''
        fill = par.ALLOBJECT[obj]['fill']
        text = par.ALLOBJECT[obj]['text']
        sloy = par.ALLOBJECT[obj]['sloy']
        angle = par.ALLOBJECT[obj]['angle']
        anchor = par.ALLOBJECT[obj]['anchor']
        size = par.ALLOBJECT[obj]['size']
        s_s = par.ALLOBJECT[obj]['s_s']
        w_text = par.ALLOBJECT[obj]['w_text']
        font = par.ALLOBJECT[obj]['font']
        '''
        line = par.get_snap_line(obj)[0]
        self.conf_dict['coord'] = par.c.coords(line)
        return self.conf_dict
