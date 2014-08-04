# -*- coding: utf-8; -*-
import symbols
from os import path
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
        par.ALLOBJECT[par.Ntext]={
                                'anchor':anchor,
                                'text':text,
                                'object':'text',
                                'fill':fill,
                                'Ltext':tt.Ltext,
                                'angle':angle,
                                'size':size,
                                'sloy':sloy,
                                's_s':s_s,
                                'w_text':w_text,
                                'font':font,
                                'id':id_dict}
        return id_dict

    else:
        x = float(x)
        y = float(y)
        size = float(size)
        tt = symbols.font(x, y, text, size, par.zoomOLD, s_s, w_text, anchor, font, angle)
        # Не брать первую линию - это привязка
        id_dict = {}
        for i in tt.nabor[1:]: #Перебрать координаты линий текста, нарисовать линии
            try:
                par.c.create_line(i[0],i[1],i[2],i[3],fill=fill, tags = ('obj', 'temp'))#['ltext', par.Ntext, 'line', 'obj',  sloy])
                
            except:
                pass
        #Линия привязки
        par.c.create_line(tt.nabor[0][0],tt.nabor[0][1],tt.nabor[0][2],tt.nabor[0][3], width=8, fill = fill, stipple = ('@'+path.join(par.appPath, 'res', '00.xbm')), tags = ('obj', 'temp'))#'ltext', par.Ntext, 'line', 'obj', 'priv', par.Ntext+'xy'#, sloy])
        
