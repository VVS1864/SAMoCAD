# -*- coding: utf-8; -*-
class Save_to_PB:
    def __init__(self, par, file_name, file_format, ALLOBJECT, drawing_w, drawing_h):
        self.par = par
        img_data = {
            'drawing_w':drawing_w,
            'drawing_h':drawing_h,
            }
        #Начало
        self.string_1 = '''  If OpenWindow(0, 0, 0, %(drawing_w)s, %(drawing_h)s, "2DDrawing Example", #PB_Window_SystemMenu | #PB_Window_ScreenCentered)
    If CreateImage(0, %(drawing_w)s, %(drawing_h)s) And StartDrawing(ImageOutput(0))''' % img_data

        #Конец
        self.string_2 = '''
      StopDrawing() 
      ImageGadget(0, 0, 0, %(drawing_w)s, %(drawing_h)s, ImageID(0))
    EndIf
    
    Repeat
      Event = WaitWindowEvent()
    Until Event = #PB_Event_CloseWindow
  EndIf''' % img_data

        #Середина
        self.content_string = ''

        #Перебрать словарь объектов
        for obj in ALLOBJECT.keys():
            if ALLOBJECT[obj]['object'] == 'line':
                #Словарь параметров линии
                opt = {}

                #Переворачиваем координаты (начало в нижнем левом -> верхнем левом)
                opt['y1'] = drawing_h - ALLOBJECT[obj]['y1']
                opt['y2'] = drawing_h - ALLOBJECT[obj]['y2']

                opt['x1'] = ALLOBJECT[obj]['x1']
                opt['x2'] = ALLOBJECT[obj]['x2']

                opt['R'] = ALLOBJECT[obj]['color'][0]
                opt['G'] = ALLOBJECT[obj]['color'][1]
                opt['B'] = ALLOBJECT[obj]['color'][2]

                #Строка линии
                line_string = '''
      LineXY(%(x1)s, %(y1)s, %(x2)s, %(y2)s, RGB(%(R)s, %(G)s, %(B)s))''' % opt
                #Прибавить к середине
                self.content_string += line_string
                
        #Сложить все строки
        self.rezultat = self.string_1 + self.content_string + self.string_2

        #Записать строку в файл
        f = open(file_name, 'w')
        f.write(self.rezultat)
        f.close()

                

                
                
        

        
