# -*- coding: utf-8; -*-
#import rotate_object
import fonts
import src.calc as calc
from math import sin, cos
font_arch = fonts.Font_Arch()
font_txt = fonts.Font_TXT()

def font(x, y, text, size, s_s, w_text, anchor, font, angle, temp):
    if font == 'Architectural':
        tt = Text_arch(x, y, text, size, s_s, w_text, anchor, angle, temp)
    else:
        tt = Text_TXT(x, y, text, size, s_s, w_text, anchor, angle, temp)

    return tt

class Text:
    #Общий класс шрифта
    def __init__(self, x, y, text, size, s_s, w_text, anchor, angle):
        self.sy = -size
        self.w_text = w_text #Ширина символа
        self.s_s = s_s#смещение символов в строке
        self.anchor = anchor#Привязка надписи к базовой точке
        
        self.sx = -self.sy/4.0#Ширина символа = четверть высоты
        self.liter = -self.s_s#Позиция первого символа
        self.Ltext = len(text) * (self.s_s * 2.0 * self.sx)  #- self.sx#Длина готовой строки
        axy = tuple(anchor)
        if axy[0] == 's':
            self.nachTextY = y
        else:# axy[0] == 'n':
            self.nachTextY = y + self.sy
        if axy[1] == 'w':
            self.nachTextX = x
        elif axy[1] == 'e':
            self.nachTextX = x-self.Ltext
        else:# axy[1] == 'c':
            self.nachTextX = x-self.Ltext/2.0
        self.nabor = []#Список координат символов текста
        self.snapLine = [self.nachTextX,self.nachTextY, self.nachTextX+self.Ltext,self.nachTextY]#Координаты линии привязки текста
        self.nabor.append(self.snapLine)#Добавить координаты в список
        sl = self.snapLine
        self.box = [[sl[0], sl[1], sl[2], sl[3]],
                    [sl[0], sl[1]+size, sl[2], sl[3]+size],
                    [sl[0], sl[1], sl[0], sl[1]+size],
                    [sl[2], sl[3]+size, sl[2], sl[3]]]
                          
                          
        #Дальше работает конкретный шрифт

class Text_arch(Text):#Ахитектурный шрифт

    def __init__(self, x, y, text, size, s_s, w_text, anchor, angle, temp = False):
        Text.__init__(self, x, y, text, size, s_s, w_text, anchor, angle)
        if not temp:
            font_arch.w_text = self.w_text
            font_arch.nachTextX = self.nachTextX
            font_arch.sx = self.sx
            font_arch.sy = self.sy
            font_arch.liter = self.liter
            font_arch.nachTextY = self.nachTextY
            for i in text:#Перебрать символы строки
                font_arch.liter += self.s_s #Передвинуть позицию на один символ
                try:
                    r = font_arch.liter_dict[i]()
                except KeyError:
                    r = font_arch.qmark()
                self.nabor.extend(r)#Добавить в список координаты символа

        if angle:
            msin = sin(angle)
            mcos = cos(angle)
            self.nabor = calc.rotate_lines(x, y, self.nabor, msin, mcos)
            self.box = calc.rotate_lines(x, y, self.box, msin, mcos)
        '''
        else:
            if angle:
                msin = sin(angle)
                mcos = cos(angle)
                self.nabor = calc.rotate_lines(x, y, self.nabor, msin, mcos)
                self.box = calc.rotate_lines(x, y, self.box, msin, mcos)
        '''


class Text_TXT(Text):
    def __init__(self, x, y, text, size, s_s, w_text, anchor, angle, temp):
        Text.__init__(self, x, y, text, size, s_s, w_text, anchor, angle)
        if not temp:
            font_txt.w_text = self.w_text
            font_txt.nachTextX = self.nachTextX
            font_txt.sx = self.sx
            font_txt.sy = self.sy
            font_txt.liter = self.liter
            font_txt.nachTextY = self.nachTextY
            for i in text:
                font_txt.liter+=self.s_s
                try:
                    r = font_txt.liter_dict[i]()
                except KeyError:
                    r = font_txt.qmark()
                self.nabor.extend(r)
        
        if angle:
            msin = sin(angle)
            mcos = cos(angle)
            self.nabor = calc.rotate_lines(x, y, self.nabor, msin, mcos)
            self.box = calc.rotate_lines(x, y, self.box, msin, mcos)
    


