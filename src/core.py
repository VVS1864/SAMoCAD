# -*- coding: utf-8; -*-
import symbols

import draft_gui
import calc
import get_conf
import get_object
import param_edit
import select_clone
import trace

import save_file
import undo_redo
import to_dxf
import from_dxf
import copy_prop
import trim_extend
import trim_dim
import fillet
import edit
import offset
import scale_object
import rotate_object
import mirror_object
import move_object
import copy_object
import grab_object
import print_ps

import line
import dimension
import text_line
import circle
import arc

from Tkinter import*
import math
import os
import time
import tkFileDialog
import tkMessageBox
from random import randint
import codecs
import copy

from shutil import copyfile


#font = 'Arial'

zoomm = 0.8
zoomp = 1.0/0.8

class Graphics:
    def __init__(self):
        self.appPath = os.getcwd()
        
        #переменные для рисования
        self.zoomOLDres = 0

        self.ex = 0.0
        self.ey = 0.0
        self.ex2 = 0.0
        self.ey2 = 0.0
        self.ex3 = 0.0
        self.ey3 = 0.0

        self.min_e = 0.00001 #Минимальная величина чертежа

        #переменные для отображениия
        self.zoomOLD = 0
        self.sloy = '1' #Текущий слой
        self.color = 'white' #Текущий цвет
        self.width = 2 #Текущая толщина
        self.stipple = None
        self.stipple_size = 200 #размер типа линий
        self.select_color = 'green' #Цвет выделяемых объектов
        self.priv_color = 'red' #Цвет привязки
        self.fon_color = 'black'
        self.left_color = 'light blue'
        self.right_color = 'red'
        self.size_t=-500 #Текущий размер шрифта текста (5 мм)
        self.size_f=-350 #Текущий размер шрифта размеров (3.5 мм)
        self.size_simbol_p = 10 #Размер значка привязки
        self.anchor = 'sw' #Текущая привязка текста
        self.font = 'Architectural'
        self.s_s = 1.2 #Межбуквенное расстояние
        self.w_text = 1 #Ширина буквы
        self.s = 50 #Переменная, определяющая пропорции в размерах
        self.arrow_s = 200
        self.vr_s = 200
        self.vv_s = 200
        self.type_arrow = 'Arch'
        self.s_s_dim = 1.3
        self.w_text_dim = 1
        self.font_dim = 'Architectural'
        self.snap_s = 10 #Определяет дальнобойность привязки (расстояние в точках на экране)
        self.angle_s = 15.0
        
        self.old_func = 'self.copyEvent()'
        self.prog_version = 'SAMoCAD - v0.0.8.2 alpha'
        self.old_text = self.prog_version
        self.old_offset = 0
        self.old_fillet_R = 0
        self.old_scale = 1
        self.old_print_scale = 100.0

        self.Old_sel = None

        self.ortoFlag=False #Если True - значит орто вкл
        self.trace_on = False
        self.tracingFlag = True
        self.snap_near = True
        self.lappingFlag = False #Если True - значит активен квадрат выделения
        self.resFlag = False #Если True - значит рисуем
        self.anchorFlag = False #Если True - режим выбора привязки текста
        self.saveFlag = False
        self.changeFlag = False
        self.current_file = 'New draft'
        self.s_dxf = False
        self.curent_class = None
        self.unpriv = False

        self.edit_clone = False
        self.move_clone = False
        self.mirror_clone = False
        self.rotate_clone = False
        self.edit_dim_clone = False
        self.copy_clone = False
        self.line_clone = False
        self.circle_clone = False
        self.arc_clone = False
        self.dim_clone = False
        self.dimR_clone = False
        self.edit_dim_text_clone = False
        self.trim_dim_clone = False

        self.enumerator = 0

        self.com=None #переменная команды
        self.colorC = None #Запоминает цвет объекта, когда на него наезжает курсор
        self.rect = None #Прямоугольник выделения
        self.priv_coord = (0,0) #Текущая точка привязки
        self.x_priv = 0 #Координаты привязок
        self.y_priv = 0
        self.tip_p = '' #тип привязки

        self.Ndimd = 0 #Количество размеров
        self.Nlined = 0 #Количество линий
        self.Ncircled = 2 #Количество кругов
        self.Ntextd = 0 #Количество текстовых строк
        self.Narcd = 0 #Количество дуг
        self.Ncloned = 0
        self.Ndimrd = 0
        self.Ndim = ''
        self.Nline = ''
        self.Ntext = ''
        self.Ncircle = ''
        self.Narc = ''
        self.Ndimr = ''

        self.Nclone = ''

        self.func_collection = [] #Объекты из коллекции, над которыми уже было проведено действие
        self.collection = [] #Выделенные объекты
        self.find_privs = [] #Набор объектов-привязок
        self.collectionBack = [] #Сброшенный набор объектов
        self.temp_collection = []
        self.temp_lines_list = []
        self.ALLOBJECT = {} #ВСЕ объекты (Объект : {параметр : значение}}
        self.all_clone = {}
        self.history_undo = [] #Список событий
        #self.history_redo = [] #Список событий

    def initial(self, master1):#Создает GUI
        draft_gui.gui = draft_gui.Gui(master1, graf)
        self.master1 = draft_gui.gui.master1
        self.dialog = draft_gui.gui.dialog
        self.command = draft_gui.gui.command
        self.info = draft_gui.gui.info
        self.button_orto = draft_gui.gui.button_orto
        self.button_trace = draft_gui.gui.button_trace
        self.button_snap_N = draft_gui.gui.button_snap_N
        self.frame1 = draft_gui.gui.frame1
        self.c = draft_gui.gui.canvas

#Начало коорданат
        self.nachCoordy = self.c.create_line(10,10,100,10,fill='white',width=3,tags=['line', 'obj'], state = HIDDEN)
        self.c.create_line(100,10,80,5,fill='white',width=3,tags=['line', 'obj'], state = HIDDEN)
        self.c.create_line(100,10,80,15,fill='white',width=3,tags=['line', 'obj'], state = HIDDEN)
        self.nachCoordx = self.c.create_line(10,10,10,100,fill='white',width=3,tags=['line', 'obj'], state = HIDDEN)
        self.c.create_line(10,100,5,80,fill='white',width=3,tags=['line', 'obj'], state = HIDDEN)
        self.c.create_line(10,100,15,80,fill='white',width=3,tags=['line', 'obj'], state = HIDDEN)
    
#Перехват закрытия окна
        self.col = 0
        self.master1.protocol('WM_DELETE_WINDOW', self.exitMethod)
#События
        self.master1.bind_class(self.c,"<MouseWheel>", self.Mzoommer)#Windows OS
        self.master1.bind_class(self.c,'<Button-4>', self.Mzoommer)#Linux OS
        self.master1.bind_class(self.c,'<Button-5>', self.Mzoommer)#Linux OS
        self.c.bind_class(self.master1,"<B2-Motion>", self.mouseMove)
        self.c.bind_class(self.master1,"<2>", self.OnMouseMove)
        self.c.bind_class(self.c,"<Motion>", self.gpriv)
        #self.c.tag_bind('t_LOD', '<Button-3>', self.editText)
        #self.c.tag_bind('dim_text_priv', '<Button-3>', self.editDimTextPlace)
        self.c.bind_class(self.master1, "<Control-Button-3>", self.BackCol)
        self.c.bind('<Button-3>', self.edit_butt_3)
        self.c.bind('<Button-1>', self.lapping_sel)
        self.c.bind('<Shift-Button-1>', self.lapping_desel)
        self.c.bind_class(self.master1, "<Delete>", self.delete)
        self.c.bind_class(self.master1, "<Escape>", self.kill)
        self.c.bind_class(self.master1, "<Return>", self.old_function)

#Горячие клавиши
        self.c.bind_class(self.master1, "<Control-KeyPress-x>", self.mirrorEvent)
        self.c.bind_class(self.master1, "<Control-KeyPress-z>", self.copyEvent)
        self.c.bind_class(self.master1, "<Control-KeyPress-a>", self.moveEvent)
        self.c.bind_class(self.master1, "<Control-KeyPress-s>", self.rotateEvent)
        self.c.bind_class(self.master1, "<Control-KeyPress-l>", self.ort)
        self.c.bind_class(self.master1, "<Control-KeyPress-e>", self.tt)
        self.c.bind_class(self.master1, "<Control-KeyPress-d>", self.copy_prop)
        self.c.bind_class(self.master1, "<Control-KeyPress-q>", self.trimEvent)
        self.c.bind_class(self.master1, "<Control-KeyPress-w>", self.extendEvent)
        self.c.bind_class(self.master1, "<Control-KeyPress-r>", self.scaleEvent)
        self.c.bind_class(self.master1, "<Control-KeyPress-p>", self.print_postScript)
        self.c.bind_class(self.master1, "<Control-KeyPress-o>", self.fileOpen)
        self.c.bind_class(self.master1, "<Control-KeyPress-n>", self.new)
        self.c.bind_class(self.master1, "<Control-KeyPress-m>", self.trim_dim)
        self.c.bind_class(self.master1, "<F1>", draft_gui.gui.obj_prop)
        self.set_coord()
        j = 0 #Сделать масштаб нормальным (-20х)
        while j < 20:
            self.zoommerM()
            j+=1

    def tt(self, event):
        print self.ALLOBJECT.keys()
        print self.collection
        #print self.ALLOBJECT
        #print self.ALLOBJECT[self.collection[0]]['text_change']

        #print self.temp_lines_list
        #print '_______'
        #print 'undo', self.history_undo
        #print 'redo', self.history_redo


    def undo(self, event = None):
        self.kill()
        if self.history_undo:
            undo_redo.undo(self.history_undo[-1], graf)
    '''
    def redo(self, event = None):
        self.kill()
        if self.history_redo:
            undo_redo.redo(self.history_redo[-1], graf)
    '''


#РЕДАКТИРОВАНИЕ ОБЪЕКТОВ
    def old_function(self, event):#При нажатии Enter вне режима рисования - вызывает последнюю вызванную функцию
        exec(self.old_func)

    #ПРОДОЛЖЕНИЕ РАЗМЕРНОЙ ЛИНИИ
    def trim_dim(self, event = None):
        self.curent_class = trim_dim.Trim_dim(graf)

    #КОПИРОВАНИЕ СВОЙСТВ
    def copy_prop(self, event = None):
        self.curent_class = copy_prop.Copy_prop(graf)

    #ОБРЕЗКА/УДЛИНЕНИЕ ЛИНИЙ
    def trimEvent(self, event = None):
        self.trim_extend = 'Trim'
        self.curent_class = trim_extend.Trim_extent(graf)
        self.old_func = 'self.trimEvent()'

    def extendEvent(self, event = None):
        self.trim_extend = 'Extend'
        self.curent_class = trim_extend.Trim_extent(graf)
        self.old_func = 'self.extendEvent()'

    

    #ИЗМЕНЕНИЕ ПАРАМЕТРОВ ВЫДЕЛЕННЫХ ОБЪЕКТОВ ПРИ СМЕНЕ ЗНАЧЕНИЯ В НАСТРОЙКАХ
    def param_edit(self, params):
        param_edit.Param_edit(graf, params)

        
#СОБЫТИЯ 3 КН МЫШИ
    def edit_butt_3(self, event):
        el = get_object.get_obj(event.x, event.y, graf, ('dim', 'text'))
        if el:
            self.kill()
            #Получить координаты из списка координат привязок (их рассчитывает gpriv)
            self.ex = self.priv_coord[0]
            self.ey = self.priv_coord[1]
            if el[0] == 'd':
                self.editDimTextPlace(el)
            elif el[0] == 't':
                self.editText(el)
                

    #РЕДАКТИРОВАНИЕ МЕСТОПОЛОЖЕНИЯ ТЕКСТА РАЗМЕРОВ
    def editDimTextPlace(self, el):
        if self.tip_p == 'c':
            self.ex = self.priv_coord[0]#Получить координаты из списка координат привязок (их рассчитывает gpriv)
            self.ey = self.priv_coord[1]
            self.ex3,self.ey3 = self.ex,self.ey
            self.dialog.config(text = u'Move dim text - new point:')
            self.info.config(text = u'Escape - stop')
            self.resFlag = True
            self.c.bind_class(self.master1,"<Return>", self.kill)
            self.c.bind('<Button-1>', self.editDimTextPlace2)
            self.c.unbind('<Button-3>')
            self.c.unbind('<Shift-Button-1>')
            self.set_coord()
            self.collection.append(el,)
            select_clone.Select_clone([el,], graf)
            self.Old_sel = None
            self.edit_dim_text_clone = True

    def editDimTextPlace2(self, event = None):
        x1, y1, x2, y2, x3, y3, ort, size, fill, text, sloy, text_change, text_place, s, vr_s, vv_s, arrow_s, type_arrow, s_s_dim, w_text_dim, font_dim = get_conf.get_dim_conf(self.collection[0], graf)
        self.ex2 = self.priv_coord[0]#Получить координаты из списка координат привязок (их рассчитывает gpriv)
        self.ey2 = self.priv_coord[1]
        self.ex,self.ey = self.coordinator(self.ex,self.ey)
        s2 = self.coordinator2(s)
        line3 = self.c.coords(self.get_snap_line(self.collection[0])[2])
        if ort == 'vertical' and abs(self.ey2-y3) <= s2*2.0:
            self.ey2 = y3-s
            text_change = 'online3'
            if x1<self.ex2<x2 or x2<self.ex2<x1:
                text_change = 'online3_m_l'
        elif ort == 'horizontal' and abs(self.ex2-x3) <= s2*2.0:
            self.ex2 = x3+s
            text_change = 'online3'
            if y1<self.ey2<y2 or y2<self.ey2<y1:
                text_change = 'online3_m_l'
        else:
            text_change = 'changed'
        text_place = [self.ex2, self.ey2]
        if event:
            self.c.delete(self.collection[0])
            dimension.c_dim(graf, x1, y1, x2, y2, x3, y3, text, sloy,
                                            fill,
                                            size,
                                            ort,
                                            text_change,
                                            text_place,
                                            s,
                                            vv_s,
                                            vr_s,
                                            arrow_s,
                                            type_arrow,
                                            s_s_dim,
                                            w_text_dim,
                                            font_dim,
                                            ID = self.collection[0])
            self.changeFlag = True
            self.kill()
        else:
            self.set_coord()
            dimension.c_dim(graf, x1, y1, x2, y2, x3, y3, text, sloy,
                                            fill,
                                            size,
                                            ort,
                                            text_change,
                                            text_place,
                                            s,
                                            vv_s,
                                            vr_s,
                                            arrow_s,
                                            type_arrow,
                                            s_s_dim,
                                            w_text_dim,
                                            font_dim,
                                            temp = 'Yes')
            
            self.ex3 = self.ex2
            self.ey3 = self.ey2
        
    def dim_text_place(self, Num):#Принимает объект - размер, возвращает кортеж приметивов его текста, линию привязки текста, координату привязки
        objs = self.ALLOBJECT[Num]['id']
        text_lines = []
        for i in objs:
            tag = self.ALLOBJECT[Num]['id'][i]
            if 'dim_text' in tag:
                text_lines.append(i)
                if 'dim_text_priv' in tag:
                    priv_line = i
        text_p = self.c.coords(priv_line)
        text_place = []
        text_place1 = (text_p[0] + text_p[2]) / 2.0
        text_place2 = (text_p[1] + text_p[3]) / 2.0
        if text_place1 == text_p[0]:
            text_place.append(text_p[0])
            text_place.append(text_place2)
            text_place.append('vert')
        else:
            text_place.append(text_place1)
            text_place.append(text_p[1])
            text_place.append('hor')

        return text_lines, priv_line, text_place


    #РЕДАКТИРОВАНИЕ ТЕКСТА
    def editText(self, Num):
        self.dialog.config(text = u'Edit text:')
        self.info.config(text = u'Enter - apply. Escape - stop')
        self.command.delete(0, END)
        self.collection.append(Num)
        select_clone.Select_clone([Num,], graf)
        text = self.ALLOBJECT[self.collection[0]]['text']
        self.command.insert(0, text)
        self.c.bind_class(self.master1, "<Return>", self.editText2)
        self.command.focus_set()
        self.Old_sel = None

    def editText2(self, event):
        fill, text, sloy, angle, anchor, size, line, coord, s_s, w_text, font = self.get_text_conf(self.collection[0])
        text = self.command.get()
        self.delete(elements = (self.collection[0],))
        text_line.c_text(graf, coord[0], coord[1], text = text, size = size, anchor = anchor, sloy = sloy, fill = fill, angle = angle, s_s = s_s, w_text = w_text, font = font)
        self.collection = []
        self.changeFlag = True
        self.enumerator_p()
        self.kill()

    #ДАТЬ ПАРАМЕТРЫ ОБЪЕКТА
    def get_conf(self, obj):
        return get_conf.get_conf(obj, graf)

    def get_circle_conf(self, obj):
        return get_conf.get_circle_conf(obj, graf)
    
    def get_arc_conf(self, obj):
        return get_conf.get_arc_conf(obj, graf)
    
    def get_line_conf(self, obj):
        return get_conf.get_line_conf(obj, graf)

    def get_line_coord(self, obj):
        return get_conf.get_line_coord(obj, graf)

    def get_text_conf(self, obj):
        return get_conf.get_text_conf(obj, graf)

    def get_dim_conf(self, obj):
        return get_conf.get_dim_conf(obj, graf)

    def get_dimR_conf(self, obj):
        return get_conf.get_dimR_conf(obj, graf)
        
    #ИЗИЕНЕНИЕ УЗЛОВ
    def editEvent(self, event):
        self.curent_class = edit.Edit_node(graf)

    #СОПРЯЖЕНИЕ
    def filletEvent(self, event=None):
        self.curent_class = fillet.Fillet(graf)

    #ДАТЬ ПРИМИТИВ БЛИЖАЙШИЙ К ТОЧКЕ
    def get_obj(self, x, y, t_obj = 'line'):
        return get_object.get_obj(x, y, graf, t_obj)
    
    #СМЕЩЕНИЕ
    def offsetEvent(self, event=None):
        self.curent_class = offset.Offset(graf)
        
    #МАСШТАБИРОВАНИЕ ОБЪЕКТОВ
    def scaleEvent(self, event=None):
        self.curent_class = scale_object.Scale_object(graf)

    #ВРАЩЕНИЕ
    def rotateEvent(self, event=None):
        self.curent_class = rotate_object.Rotate_object(graf)
    
    #ЗЕРКАЛО (не применятеся к сложным объектам, содержащим текст)
    def mirrorEvent(self, event=None):
        self.curent_class = mirror_object.Mirror_object(graf)

    #ПЕРЕМЕЩЕНИЕ
    def moveEvent(self, event=None):
        self.curent_class = move_object.Move_object(graf)

    #КОПИРОВАНИЕ
    def copyEvent(self,event=None):
        self.curent_class = copy_object.Copy_object(graf)
        
    #ВЫДЕЛЕНИЕ
    def lapping_sel(self,event):
        grab_object.lapping2(graf, select = 'select')
        
    #СНЯТИЕ ВЫДЕЛЕНИЯ
    def lapping_desel(self, event):
        grab_object.lapping2(graf, select = 'deselect')

    def resRect(self, event):
        self.rectx2=event.x
        self.recty2=event.y
        self.priv_coord = (self.rectx2, self.recty2)
        self.rectx,self.recty = self.coordinator(self.rectx,self.recty)
        self.set_coord()
        if self.rectx2<self.rectx:#Цвет зависит от координат x
            color = self.left_color
        else:
            color = self.right_color
        if self.rect:
            self.c.coords(self.rect, self.rectx, self.recty, self.rectx2, self.recty2)
            self.c.itemconfig(self.rect, outline = color)
        else:
            self.rect=self.c.create_rectangle(self.rectx, self.recty, self.rectx2, self.recty2, fill=None,outline=color, tags=['line', 'obj', 'rect'])#Нарисовать заново по новым координатам

    def set_coord(self):
        self.xynachres=self.c.coords(self.nachCoordy)
        self.zoomOLDres = self.zoomOLD

    def delete(self, event=None, elements = None, add_history = None): #Уделение объектов
        
        def dele(i, h = None):#Удаляет пришедший объект с канваса и из ALLOBJECT
            if h:
                e = self.get_conf(i)
                self.e_list.append(e)
            self.c.delete(i)
            del self.ALLOBJECT[i]
            if ('c_', i) in self.history_undo:
                self.history_undo.remove(('c_', i))
        
        t1 = time.time()
        if elements == None:#Если не заданы элементы для удаления
            self.set_coord()
            self.e_list = []
            map(lambda x: dele(x, h = 'add'), self.collection)#Перебрать коллекцию
            self.collection = []
            self.history_undo.append(('delete', (self.e_list, self.xynachres, self.zoomOLDres)))
            self.changeFlag = True
            self.enumerator_p()
            self.kill()
        else:#Если заданы элементы для удаления
            map(dele, elements)
        t2 = time.time()
        print 'delete', t2-t1

    def sbros(self):#Сбрасывает коллекцию - переводит список веделенных объектов в collectionBack.
        t1 = time.time()
        self.collectionBack = self.collection
        self.c.delete('clone')
        self.collection = []
        t2 = time.time()
        print 'sbros', t2-t1

    def BackCol(self, event):#core-feature!!! - Возвращает в коллекцию предыдущий набор
        if self.resFlag == False and (not self.collection):#Если начего не рисуется и коллекция не пуста
            def BC(i):
                if i in self.ALLOBJECT:#Если объект есть в обхем списке (не был удален)
                    self.collection.append(i)#Добавить в коллекцию
            print 111
            map(BC, self.collectionBack)#Перебрать старую коллекцию
            select_clone.Select_clone(self.collection, graf)
            self.colObj()#Посчитать колличество выделенных объектов
            draft_gui.gui.update_prop()

    def colObj(self):#Пишет информацию о количестве выбранных объектов
        if self.collection:
            self.info.config(text = (u'Selected %s objects') %(len(self.collection)))
        else:
            self.info.config(text ='')

    def back_color(self, color, obj):
        if obj[0] in ['c', 'a']:
            for i in self.ALLOBJECT[obj]['id']:
                tag = self.ALLOBJECT[obj]['id'][i]
                if 'line' in tag:
                    self.c.itemconfig(i, fill = color)
                if 'cir' in tag or 'a' in tag:
                    self.c.itemconfig(i, outline = color)
        else:
            self.c.itemconfig(obj, fill = color)

    def collektor_sel(self, event):
        x = event.x
        y = event.y
        self.collektor(x, y, select = 'select')

    def collektor_desel(self, event):
        x = event.x
        y = event.y
        self.collektor(x, y, select = 'deselect')

    def collektor(self, x, y, select):#Добавляет в коллекцию объект, приметивы которого в активном состоянии (находятся под курсором)
        #Получить номер объекта по текущему активному приметиву
        Num = get_object.get_obj(x, y, graf, 'all')
        #Если не нажат Shift
        if select == 'select':
            #Если объект отсутствует в коллекции - добавить, сменить цвет
            if Num not in self.collection and Num in self.ALLOBJECT:
                self.collection.append(Num)
                select_clone.Select_clone((Num,), graf)
                self.Old_sel = None
        #Если нажат Shift
        else:
            #Если объект в коллекции - вырвать, вернуть цвет
            if Num in self.collection: 
                self.collection.remove(Num)
                self.c.delete('C'+Num)
        draft_gui.gui.update_prop()
        #Сосчитать колличество выделенных объектов
        self.colObj()

    def mass_collektor(self, mass, select):#Добавляет в коллекцию объекты из массы приметивов
        t1 = time.time()
        old_col = self.collection
        if select == 'select':#Если дабавить
            append_list = []#Заместо коллекции
            gettags = self.c.gettags
            append = append_list.append
            for content in mass:
                Num = gettags(content)[1]#Получить номер объекта по приметиву
                if Num not in self.collection and Num not in append_list and Num[0] != 'C':#Если объект отсутствует в коллекции - добавить, сменить цвет
                    append(Num)
            select_clone.Select_clone(append_list, graf)
            self.collection.extend(append_list)
        else: #Если вырвать
            delete_list = []
            for content in mass:
                Num = self.c.gettags(content)[1]#Получить номер объекта по приметиву
                if Num in self.collection and Num not in delete_list and Num[0] != 'C':#Если объект в коллекции - вырвать из нее, вернуть цвет
                    #Если объекта нет в списке удаления
                    delete_list.append(Num)
            #перебрать delete_list, удалить все его объекты из коллекции
            for i in delete_list:
                self.collection.remove(i)
                self.c.delete('C'+i)
        if old_col != self.collection:
            draft_gui.gui.update_prop()
        t2 = time.time()
        print 'mass_collektor', t2-t1

    def edit_collektor(self, edit_mass): #Добавляет в коллекцию объекты из массы приметивов, если в массе есть размеры - то остальные объекты не попадут в коллекцию
        prov = True #True, пока не попался размер
        append_list = []
        for content in edit_mass:
            non_ap = False
            Num = self.c.gettags(content)[1]#Получить номер объекта по приметиву
            if Num not in append_list and Num[0] != 'C':
                if  Num[0] in ('d', 'r'):
                    prov = False
                    if Num[0] == 'r':
                        line1 = self.get_snap_line(Num)[0]
                        c = self.c.coords(line1) #get_conf.get_line_coord(line1, graf)#
                        xc = c[0]
                        yc = c[1]
                        if (xc, yc) == (self.ex, self.ey):
                            non_ap = True
                elif Num[0] == 'c':
                    x0, y0, R, fill, width, sloy = get_conf.get_circle_conf(Num, graf)
                    if (x0, y0) == (self.ex, self.ey):
                        non_ap = True

                elif Num[0] == 'a':
                    xc, yc, dx1, dy1, dx2, dy2, fill, width, sloy = get_conf.get_arc_conf(Num, graf)
                    if (xc, yc) == (self.ex, self.ey):
                        non_ap = True

                if non_ap == False:
                    append_list.append(Num)
        select_clone.Select_clone(append_list, graf)
        if self.Old_sel in append_list:
            self.Old_sel = None
        self.collection.extend(append_list)
        if self.tip_p == 'c' and prov == True and len(self.collection)==1:#Если объект 1, это линия и привязка к середине
            return 'line_c'#Включит режим Move
        else:
            return 'another'#Включит режим Edit

    def edit_c(self, edit_mass): #Проверяет, какие объекты находятся в коллекции - если только размеры по линии - оставляет коллекцию неизменной, если есть другие объекты - оставляет в кол. только те, к которым есть привязка в данный момент
        delete_list = []#Список объектов из коллекции, к которым привязка нет
        dim_list = []#Список размеров из коллекции
        line_dim_edit = True#Будет True - пока не попался НЕразмер
        for content in edit_mass:#Перебрать пришедшую коллекцию
            if content[0] == 'd':#Если объект == размер
                dim_list.append(content)#Добавить в список размеров
            else:
                line_dim_edit = False#Иначе неразмер попался
            undel_obj = False#Если False - убрать объект из коллекции
            find  = self.ALLOBJECT[content]['id']#self.c.find_withtag(content)#Получить приметивы объекта
            for i in find:#Перебрать их
                if i in self.find_privs2:#Если приметив в списке приметивов - привязок
                    undel_obj = True#Оставить объект в коллекции
            if undel_obj == False:#Если не удалять - False
                delete_list.append(content)#Добавить объект в список удаления
                self.c.delete('C'+content)
        map(lambda i: self.collection.remove(i), delete_list)#перебрать delete_list, удалить все его объекты из коллекции

#core-feature!!! - определяет, по одной линии все размеры или нет. Если да - можно перенести всю размерную цепочку
        if line_dim_edit == True:#Если ни одного неразмера не попалось
            if len(dim_list) > 1:#Если количество размеров > 1
                line3_list = []#Список первых координат размерных линий размеров
                ort1 = None#ориентация первого размера
                ort2 = None#То же второго
                bFlag = False#Если False - то все размерные линии имеют одну общую координату (x или y) и лежат по одной линии
                for i in dim_list:# Перебрать список размеров
                    if dim_list.index(i) == 0:  #Если размер первый в списке
                        ort1 = self.ALLOBJECT[i]['ort']#Присвоить его ориентацию первой переменной
                    else:
                        ort2 = self.ALLOBJECT[i]['ort']#Иначе второй
                        if ort1 != ort2:#Если переменные не равны - Вылететь, коллекцию больше не изменять
                            bFlag = True
                            break
                    line3 = self.get_snap_line(i)[2]#Взять размерную линию размера
                    coord = self.c.coords(line3)#Взять координаты размерной линии
                    line3_list.append(coord[0:2])#Добавить в список координат только 2 первые координаты
                if bFlag == False:#Если Вылетания не произошло
                    for ind, i in enumerate(line3_list):#Перебрать список координат
                        if ort1 == 'vertical':#Если оринтация вертикальная
                            if i == line3_list[-1]:#Если элемент последний в списке
                                ii = -1#Второй элемент - взять предыдущий
                            else:
                                ii = 1#Иначе - последующий
                            if i[1] != line3_list[ind + ii][1]:#Если координата y второго не равна y первого - Вылететь, коллекцию больше не изменять
                                bFlag = True
                                break
                        else:
                            if i == line3_list[-1]:
                                ii = -1
                            else:
                                ii = 1
                            if i[0] != line3_list[ind + ii][0]:#Если координата x второго не равна x первого - Вылететь, коллекцию больше не изменять
                                bFlag = True
                                break
                    if bFlag == False:#Если вылетания и теперь не произошло
                        self.collection = dim_list#Коллекция = списку размеров
                        for i in self.collection:#Поменять цвет размеров
                            self.c.delete('C'+i)
                        select_clone.Select_clone(self.collection, graf)
                                        
    def colorer(self, event):#действие при наезжании курсора на приметив
        Num = self.get_obj(event.x, event.y, 'all')
        print 111
        if Num not in self.collection and Num in self.ALLOBJECT and Num != 'trace':#Если объект отсутствует в коллекции - сменить цвет, включить флаг
            select_clone.Select_clone((Num,), graf)
            print Num
        if self.resFlag == False:#Если ничего не рисуется - выключить действия lapping
            self.c.unbind('<Button-1>')
            self.c.unbind('<Shift-Button-1>')

    def colorerL(self, event=None):#действие при уходн курсора с приметива
        Num = self.get_obj(event.x, event.y, 'all')
        if Num not in self.collection and Num in self.ALLOBJECT:#Если объект не в коллекции, вернуть цвет
            if Num in self.ALLOBJECT:
                self.c.delete(self.all_clone['C'+Num])
                del self.all_clone['C'+Num]
        if self.resFlag == False:
            self.c.bind('<Button-1>', self.lapping_sel)
            self.c.bind('<Shift-Button-1>', self.lapping_desel)

    def m_coordinator(self, arg, zoomOLDres): #Переводит расстояния момента при zoomOLDres в расстояния сейчас
        if self.zoomOLD != zoomOLDres:
            r = -self.zoomOLD+zoomOLDres
            if self.zoomOLD>zoomOLDres:
                arg *= (zoomm**r)
            else:
                arg *= zoomp**(-r)
        return arg

    def n_coordinator(self, arg): #Переводит расстояния момента при zoomOLDres в насстоящие расстояния
        if self.zoomOLD>0:
            arg = arg*zoomm**self.zoomOLD
        else:
            zoomOLDx = self.zoomOLD*(-1)
            arg = arg*zoomp**zoomOLDx
        return arg

    def coordinator(self,x,y,zoomOLDres = None, xynachres = None):#Пересчитывает координаты если был изменен зум или перемещен экран
        xynach=self.c.coords(self.nachCoordy)
        if zoomOLDres == None:
            zoomOLDres = self.zoomOLDres
            xynachres = self.xynachres

        if self.zoomOLD == zoomOLDres:
            dx=xynach[0]-xynachres[0]
            dy=xynach[1]-xynachres[1]
        else:
            r=-self.zoomOLD+zoomOLDres
            if self.zoomOLD>zoomOLDres:
                x *= zoomm**r
                y *= zoomm**r
                dx = xynach[0] - xynachres[0] * zoomm**r
                dy = xynach[1] - xynachres[1] * zoomm**r
            else:
                x *= zoomp**(-r)
                y *= zoomp**(-r)
                dx = xynach[0] - xynachres[0] * zoomp**(-r)
                dy = xynach[1] - xynachres[1] * zoomp**(-r)

        x = dx + x
        y = dy + y

        return x,y

    def coordinator2(self,arg):#Переводит действительные расстояния в расстояния сейчас
        if self.zoomOLD>0:
            arg *= zoomp**self.zoomOLD
        else:
            zoomOLDx = self.zoomOLD*(-1)
            arg /= zoomp**zoomOLDx
        return arg

    def standart_unbind(self):
        self.resFlag = True
        self.c.bind_class(self.master1,"<Return>", self.kill)
        self.c.unbind('<Button-3>')
        self.c.unbind_class(self.master1, "<Control-Button-3>")
        self.c.unbind('<Button-1>')
        self.c.unbind('<Shift-Button-1>')
        self.c.unbind_class(self.master1, "<Delete>")

    def kill(self, event=None):#Возвращает все в исходное состояние
        if self.rect:
            self.c.delete(self.rect)
            self.rect = None
        if self.col:
            #fill = self.ALLOBJECT[self.col]['fill']
            #self.back_color(fill, self.col)
            self.c.delete('C'+self.col)
            self.col = None
        if self.curent_class:
            del self.curent_class
            self.curent_class = None
        t=self.c.find_withtag('c1')
        if t:
            self.c.delete('c1')
        if 'trace' in self.ALLOBJECT:
            self.c.delete('trace')
            del self.ALLOBJECT['trace']
        self.c.delete('clone')
        self.c.delete('temp')
        self.unpriv = False
        self.edit_clone = False
        self.move_clone = False
        self.mirror_clone = False
        self.rotate_clone = False
        self.edit_dim_clone = False
        self.copy_clone = False
        self.line_clone = False
        self.circle_clone = False
        self.arc_clone = False
        self.dim_clone = False
        self.dimR_clone = False
        self.trim_dim_clone = False
        self.edit_dim_text_clone = False
        self.c.bind_class(self.c,"<Motion>", self.gpriv)
        self.c.bind_class(self.master1, "<Control-Button-3>", self.BackCol)
        self.c.bind('<Button-1>', self.lapping_sel)
        self.c.bind('<Shift-Button-1>', self.lapping_desel)
        self.c.bind('<Button-3>', self.edit_butt_3)
        self.c.bind_class(self.master1, "<Return>", self.old_function)
        self.c.bind_class(self.master1, "<Delete>", self.delete)

        self.c.unbind_class(self.c,"<Shift-1>")
        self.c.unbind_class(self.master1, "<Motion>")
        self.c.unbind_class(self.c, "<End>")
        self.dialog.config(text = u'Command:')
        self.info.config(text = '')
        self.resFlag = False
        self.lappingFlag = False
        self.anchorFlag = False
        self.trace_on = False
        self.command.delete(0,END)
        self.com = None
        self.sbros()
        self.func_collection = []
        self.temp_collection = []
        self.c.config(cursor = 'crosshair')
        draft_gui.gui.update_prop()

    def comY_N(self, default):#Проверяет, как ответил пользователь на yes/No, если не ответил - вернет то, что по умолчанию
        com=self.command.get()
        if com:
            com = str.upper(com)
            if com in ['N', 'Y']:
                default = com
            else:
                default = 'unknow'
            self.command.delete(0,END)
        else:
            default = default
        return default

    def comOrKill(self, event=None):#Берет значени из коммандной строки если пользователь вписал число, отчищает ком.строку
        com=self.command.get()
        try:
            com = float(com)
        except ValueError:
            self.info.config(text = u'Unknow command')
            self.com = None
        else:
            self.com = com

    def commer(self,x1,y1,x2,y2): #Просчитывает координаты если self.com == True
        self.comOrKill()
        if self.com:
            self.com = self.coordinator2(self.com)
            dx=x1-x2
            dy=y1-y2
            if self.ortoFlag == False and x1 != x2 and y1 != y2:
                dx0=math.sqrt((self.com*self.com * dx*dx)/(dy*dy + dx*dx))
                dy0=dx0*dy/dx
                i=1
                if x1<x2:
                    i=-1
                x2=x1-i*dx0
                y2=y1-i*dy0
            else:
                x2,y2=self.orto(x1,y1,x2,y2)
                x2,y2=self.ortoRes(x1,y1,x2,y2)
        return x2,y2

    def gpriv(self,event=None, x=None, y = None, f = None):
        t=self.c.find_withtag('c1')#Найти значек привязки
        if t:#Если таковой имеется
            self.c.delete('c1')#Удалить значек
            if  self.resFlag == False:#Если режим рисования не включен
                self.c.bind('<Button-1>', self.lapping_sel)
                self.c.bind('<Shift-Button-1>', self.lapping_desel)
                self.find_privs = ['t'] #Отчистить список привязок


        #if event:#Если метод вызван событием
        self.find_privs = ['t']#Список приметивов привязки (с разделителем)
        #self.c.unbind_class(self.master1, "<End>")#Выключить реакцию на End - перебор привязок
        x=event.x#Получить координаты положения курсора
        y=event.y
        if not self.unpriv: 
            self.x_priv, self.y_priv, self.tip_p = self.priv(x,y)#Проверить, попадает ли положение курсора под возможность привязки к приметиву
            p = self.tip_p #Тип привязки
            self.priv_coord = (self.x_priv, self.y_priv)#Назначить кориеж координат привязки
            if x!=self.x_priv or y!=self.y_priv or p != self.tip_p: #Если координаты курсора не равны координатам привязки или тип привязки сменился
                self.tip_p = p #Переназначить тип привязки на новый
                x1 = self.x_priv
                y1 = self.y_priv
                r=self.size_simbol_p
                if p == 'r':#Если тип привязки - к конечной точке
                    self.c.create_oval(x1-r,y1-r,x1+r,y1+r, outline = self.priv_color,width = 3, fill = None, tags = 'c1')#Нарисовать знак привязки - круг
                elif p == 'c':#Если привязка к середине нарисовать знак привязки - треугольник
                    self.c.create_line(x1-r,y1-r,x1+r,y1-r,fill=self.priv_color,width=3,tags='c1')
                    self.c.create_line(x1-r,y1-r,x1,y1+r,fill=self.priv_color,width=3,tags='c1')
                    self.c.create_line(x1,y1+r,x1+r,y1-r,fill=self.priv_color,width=3,tags='c1')
                elif p == 'X': #Если привязка к пересечению - нарисовать знак Х
                    self.c.create_line(x1-r,y1-r,x1+r,y1+r,fill=self.priv_color,width=3,tags='c1')
                    self.c.create_line(x1+r,y1-r,x1-r,y1+r,fill=self.priv_color,width=3,tags='c1')
                elif p == 'N': #Если привязка к ближайшей - нарисовать знак N
                    self.c.create_line(x1-r,y1-r,x1+r,y1+r,fill=self.priv_color,width=3,tags='c1')
                    self.c.create_line(x1+r,y1-r,x1-r,y1+r,fill=self.priv_color,width=3,tags='c1')
                    self.c.create_line(x1-r,y1-r,x1-r,y1+r,fill=self.priv_color,width=3,tags='c1')
                    self.c.create_line(x1+r,y1-r,x1+r,y1+r,fill=self.priv_color,width=3,tags='c1')

                if  self.resFlag == False:#Если режим рисования не включен
                    #self.c.tag_unbind('sel', "<Button-1>")#Выключить возможность выделения
                    self.c.bind('<Button-1>', self.editEvent)#Включить возможность редактирования узла
            else:
                if not self.rect:
                    el = get_object.get_obj(x, y, graf, 'all')
                    if el and el != 'trace':
                        if el == self.Old_sel:
                            pass
                        elif el != self.Old_sel:
                            if self.Old_sel:
                                self.c.delete('C'+self.Old_sel)
                                self.Old_sel = None
                            if el not in self.collection and el in self.ALLOBJECT:#Если объект отсутствует в коллекции - сменить цвет, включить флаг
                                select_clone.Select_clone((el,), graf)
                                self.Old_sel = el
                            if self.resFlag == False:#Если ничего не рисуется - выключить действия lapping
                                self.c.bind('<Button-1>', self.collektor_sel)
                                self.c.bind('<Shift-Button-1>', self.collektor_desel)
                    else:
                        if self.Old_sel:
                            self.c.delete('C'+self.Old_sel)
                            self.Old_sel = None
                            
                        if self.resFlag == False:
                            self.c.bind('<Button-1>', self.lapping_sel)
                            self.c.bind('<Shift-Button-1>', self.lapping_desel)

            if any((self.edit_clone, self.move_clone, self.copy_clone, self.mirror_clone, self.rotate_clone, self.edit_dim_clone, self.line_clone, self.circle_clone, self.arc_clone, self.dim_clone, self.edit_dim_text_clone, self.dimR_clone, self.trim_dim_clone)):
                if len(self.collection) < 100:
                    self.c.delete('temp')
                    if self.edit_clone:
                        self.curent_class.editEvent2()
                    elif self.move_clone:
                        self.curent_class.moveEvent3()
                    elif self.copy_clone:
                        self.curent_class.copyEvent3()
                    elif self.mirror_clone:
                        self.curent_class.mirrorEvent4()
                    elif self.rotate_clone:
                        self.curent_class.rotateEvent5()
                    elif self.line_clone:
                        self.curent_class.line2()
                    elif self.circle_clone:
                        self.curent_class.circle2()
                    elif self.arc_clone:
                        self.curent_class.arc3()
                    elif self.dim_clone:
                        self.curent_class.risDim4()
                    elif self.edit_dim_text_clone:
                        self.editDimTextPlace2()
                    elif self.dimR_clone:
                        self.curent_class.risDimR3()
                    elif self.trim_dim_clone:
                        self.curent_class.dim_conf()

            if self.trace_on:
                trace.tracer(graf, self.trace_x1, self.trace_y1, self.trace_x2, self.trace_y2, self.snap_s, self.angle_s)
        else:
            self.x_priv, self.y_priv = x, y
            self.priv_coord = (self.x_priv, self.y_priv)
            
    def priv(self, x, y, f = None):#Принимает координаты точки и может принять список приметивов, возвращает координаты точки привязки если привязка допустима, в противном случае не изменяет пришедших координат
        if f == None:#Если список приметивов не назначен
            find = list(self.c.find_overlapping(x-self.snap_s,y-self.snap_s,x+self.snap_s,y+self.snap_s))#Найти все приметивы, попадающие в квадрат вокруг точки
            if self.rect:
                try:
                    find.remove(self.rect)
                except ValueError:
                    pass      
        else:
            find = [f]#Иначе приобразовать пришедший список в список
        
        tip_p = None
        stopFlag = False
        xi=x#Приравнять возвращаемые координаты к тем, которые пришли
        yi=y
        priv_coord_list = [] #Список координат приметивов с тегом привязки
        ### Привязка к одному приметиву ###
        for i in find:#Перебрать список приметивов
            obj_tags = self.c.gettags(i)
            t = obj_tags[1]
            if t[0] == 'C' or 'temp' in obj_tags or 'text' in obj_tags:
                continue
            
            tags = self.ALLOBJECT[t]['id'][i]
            
                
            if 'priv' in tags and 'line' in tags:#Если у приметива есть тег привязки
                xy = self.c.coords(i)#Взять координаты приметива
                priv_coord_list.append((xy,'line'))#Добавить координаты приметива в список
                ay1 = abs(y-xy[1])#Получить разность координат приметива и пришедших в метод координат (коорд. курсора)
                ay2 = abs(y-xy[3])
                ax1 = abs(x-xy[0])
                ax2 = abs(x-xy[2])
                if ax1<=ax2 and ax1<=self.snap_s and ay1<=self.snap_s: #or ay2<=self.snap_s):#Если разность координат х по первой точке меньше, чем по второй и эта разность меньше self.snap_s
                    if ay1<=ay2 and ay1<self.snap_s:#Если разность по у первой точки меньше, чем по второй и эта разность меньше self.snap_s
                        yt=xy[1]#Текущимь координатами взять координаты первой точки приметива
                        xt=xy[0]
                        tip_p = 'r'#Тип привязки - к конточке
                        self.find_privs.append(i)#Добавить приметив в список привязок
                        if stopFlag == False:#Если точка привязки не была найдена ранее
                            xi = xt#Назначить возвращаемые координаты равными координатам точки
                            yi = yt
                            stopFlag = True#Остановить назначение возвращаемых координат

                elif ax1>=ax2 and ax2<=self.snap_s and ay2<=self.snap_s:#(ay1<=self.snap_s or ay2<=self.snap_s):#Если разность координат х по второй точке меньше, чем по первой и эта разность меньше self.snap_s
                    if ay1>=ay2 and ay2<=self.snap_s:
                        yt=xy[3]
                        xt=xy[2]
                        tip_p = 'r'
                        self.find_privs.append(i)
                        if stopFlag == False:
                            xi = xt
                            yi = yt
                            stopFlag = True

                else:#Если не подошел не один из вариантов - привязка к середине
                    y0=xy[1]-((xy[1]-xy[3])/2.0)
                    x0=xy[0]-((xy[0]-xy[2])/2.0)

                    if abs(x-x0)<=self.snap_s and abs(y-y0)<=self.snap_s:
                        yt=y0
                        xt=x0
                        tip_p = 'c'
                        self.find_privs.append(i)
                        if stopFlag == False:
                            xi = xt
                            yi = yt
                            stopFlag = True
               
                if 'temp' in tags or 'cir_centr' in tags or 'a_centr' in tags:
                    tip_p = None
                    stopFlag = False
                    xi=x
                    yi=y

            elif 'priv' in tags and 'cir' in tags:
                xy = self.c.coords(i)
                priv_coord_list.append((xy,'cir'))
                xc,yc,R = self.coord_circle(xy[0],xy[1],xy[2],xy[3])
                if abs(x - xc)<=self.snap_s:
                    if abs(yc-R - y) <= self.snap_s:
                        xi = xc
                        yi = yc-R
                        tip_p = 'r'
                        stopFlag = True
                        self.find_privs.append(i)
                    elif abs(yc+R - y) <= self.snap_s:
                        xi = xc
                        yi = yc+R
                        tip_p = 'r'
                        stopFlag = True
                        self.find_privs.append(i)

                elif abs(y - yc)<=self.snap_s:
                    if abs(xc-R - x) <= self.snap_s:
                        xi = xc-R
                        yi = yc
                        tip_p = 'r'
                        stopFlag = True
                        self.find_privs.append(i)
                    elif abs(xc+R - x) <= self.snap_s:
                        xi = xc+R
                        yi = yc
                        tip_p = 'r'
                        stopFlag = True
                        self.find_privs.append(i)


            elif 'priv' in tags and 'a' in tags:
                xy = self.c.coords(i)
                start = float(self.c.itemcget(i, 'start'))
                extent = float(self.c.itemcget(i, 'extent'))
                priv_coord_list.append((xy,'a'))
                xc, yc, dx1, dy1, dx2, dy2 = get_conf.get_arc_coord(xy[0],xy[1],xy[2],xy[3], start, extent)
                R = (xy[2]-xy[0])/2.0
                if abs(x - dx1)<=self.snap_s:
                    if abs(y - dy1)<=self.snap_s:
                        xi = dx1
                        yi = dy1
                        tip_p = 'r'
                        stopFlag = True
                        self.find_privs.append(i)
                elif abs(x - dx2)<=self.snap_s:
                    if abs(y - dy2)<=self.snap_s:
                        xi = dx2
                        yi = dy2
                        tip_p = 'r'
                        stopFlag = True
                        self.find_privs.append(i)
        if stopFlag == False and self.snap_near == True and self.resFlag == True and priv_coord_list:#Привязка к ближайшей точке на линии - Если неподошел не один предыдущий вариант
            for i in priv_coord_list:
                xy = priv_coord_list[priv_coord_list.index(i)][0]
                if i[1] == 'line':

                    xt, yt = calc.min_distanse(xy[0],xy[1],xy[2],xy[3], x,y)
                    if xt:
                        xi = xt
                        yi = yt
                        tip_p = 'N'
                        break
                else:
                    xc,yc,R = self.coord_circle(xy[0],xy[1],xy[2],xy[3])
                    if i[1] == 'a':
                        xt,yt, d = calc.min_distanse_cir(xc, yc, R, x, y)
                        if d<=self.snap_s:
                            xi = xt#Назначить координаты выхода полученным координатам
                            yi = yt
                            tip_p = 'N'
                            break

                    elif i[1] == 'cir':
                        xt,yt, d = calc.min_distanse_cir(xc, yc, R, x, y)
                        if d<=self.snap_s:
                            xi = xt#Назначить координаты выхода полученным координатам
                            yi = yt
                            tip_p = 'N'
                            break


        ### Привязка к двум приметивам ###
        if len(priv_coord_list) > 1 and stopFlag == False:#Привязка к пересечению
            for i in priv_coord_list:#Перебрать список координат
                ind = priv_coord_list.index(i)#Взять индекс текущего элемента
                if ind == 0:#Если элемент первый - приверять пересечение с последующим
                    ii = 1
                else:#Иначе с предыдущим
                    ii = -1
                r = priv_coord_list[ind+ii]
                if i[1] == 'line' and r[1] == 'line':
                    xt,yt = calc.intersection_l_l(i[0][0],i[0][1],i[0][2],i[0][3],r[0][0],r[0][1],r[0][2],r[0][3])#Проверить есть ли точка пересечения, если да - вычислить
                    if xt != None:#Если точка есть
                        if (abs(y-yt)<=self.snap_s) and (abs(x-xt)<=self.snap_s):#Если разность координат не превышает self.snap_s
                            if (xt != i[0][0] or yt != i[0][1]) and (xt != i[0][2] or yt != i[0][3]):#Если эта точка не равна одной из точек
                                if (xt != r[0][0] or yt != r[0][1]) and (xt != r[0][2] or yt != r[0][3]):
                                    xi = xt#Назначить координаты выхода полученным координатам
                                    yi = yt
                                    tip_p = 'X'#Тип привязки - пересечение
                                    break
                elif (i[1] == 'line' and r[1] in ['cir', 'a']) or (i[1] in ['cir', 'a'] and r[1] == 'line'):
                    if i[1] == 'line':
                        line = i
                        circle = r
                    else:
                        line = r
                        circle = i
                    xc,yc,R = self.coord_circle(circle[0][0],circle[0][1],circle[0][2],circle[0][3])
                    xt,yt = calc.intersection_l_c(xc, yc, R, line[0][0], line[0][1], line[0][2], line[0][3], x, y)
                    if xt != None:#Если точка есть
                        if (abs(y-yt)<=self.snap_s) and (abs(x-xt)<=self.snap_s):#Если разность координат не превышает self.snap_s
                            xi = xt#Назначить координаты выхода полученным координатам
                            yi = yt
                            tip_p = 'X'#Тип привязки - пересечение
                            break
                elif i[1] in ['cir', 'a'] and r[1] in ['cir', 'a']:
                    xc1,yc1,R1 = self.coord_circle(i[0][0],i[0][1],i[0][2],i[0][3])
                    xc2,yc2,R2 = self.coord_circle(r[0][0],r[0][1],r[0][2],r[0][3])
                    xt, yt = calc.intersection_c_c(xc1, yc1, R1, xc2, yc2, R2, x, y)
                    if xt != None:#Если точка есть
                        if (abs(y-yt)<=self.snap_s) and (abs(x-xt)<=self.snap_s):#Если разность координат не превышает self.snap_s
                            xi = xt#Назначить координаты выхода полученным координатам
                            yi = yt
                            tip_p = 'X'#Тип привязки - пересечение
                            break

        if f == None: #Если список приметивов не был назначен - включить функцию перебора привязки
            self.perebor_priv()
        return xi,yi,tip_p #Вернуть координаты привязки, и ее тип

    def coord_circle(self, x1,y1,x2,y2):
        xc = (x1+x2)/2.0
        yc = (y1+y2)/2.0
        R = (x2-x1)/2.0
        return xc, yc, R

    def perebor_priv(self):
        if len(self.find_privs)>2:
            self.c.bind_class(self.master1, "<End>", self.end_priv)

    def end_priv(self, event):#Переберает тип привязки, если есть варианты
        t_index = self.find_privs.index('t')
        if len(self.find_privs) == t_index+1:
            self.gpriv(x = self.x_priv, y = self.y_priv, f = self.find_privs[0])

            self.find_privs.remove('t')
            self.find_privs.insert(1, 't')
        else:
            self.gpriv(x = self.x_priv, y = self.y_priv, f = self.find_privs[t_index+1])

            self.find_privs.remove('t')
            self.find_privs.insert(t_index+1, 't')

    def ort(self, event=None, color_only = None):
        if not color_only:
            if self.ortoFlag == True:
                self.ortoFlag = False
                self.button_orto.config(bg='white',fg='black', activebackground = 'white', activeforeground = 'black')
            else:
                self.ortoFlag=True
                self.button_orto.config(bg='blue',fg='red', activebackground = 'blue', activeforeground = 'red')
        else:
            if self.ortoFlag == False:
                self.button_orto.config(bg='white',fg='black', activebackground = 'white', activeforeground = 'black')
            else:
                self.button_orto.config(bg='blue',fg='red', activebackground = 'blue', activeforeground = 'red')


    def trac(self, event=None, color_only = None):
        if 'trace' in self.ALLOBJECT:
            self.c.delete('trace')
            del self.ALLOBJECT['trace']
        if not color_only:
            if self.tracingFlag == True:
                self.tracingFlag = False
                self.trace_on = False
                self.button_trace.config(bg='white',fg='black', activebackground = 'white', activeforeground = 'black')
            else:
                self.tracingFlag=True
                self.button_trace.config(bg='blue',fg='red', activebackground = 'blue', activeforeground = 'red')
        else:
            if self.tracingFlag == False:
                self.button_trace.config(bg='white',fg='black', activebackground = 'white', activeforeground = 'black')
            else:
                self.button_trace.config(bg='blue',fg='red', activebackground = 'blue', activeforeground = 'red')

    def snap_n(self, event = None, color_only = None):
        if not color_only:
            if self.snap_near == True:
                self.snap_near = False
                self.button_snap_N.config(bg='white',fg='black', activebackground = 'white', activeforeground = 'black')
            else:
                self.snap_near=True
                self.button_snap_N.config(bg='blue',fg='red', activebackground = 'blue', activeforeground = 'red')
        else:
            if self.snap_near == False:
                self.button_snap_N.config(bg='white',fg='black', activebackground = 'white', activeforeground = 'black')
            else:
                self.button_snap_N.config(bg='blue',fg='red', activebackground = 'blue', activeforeground = 'red')
            
    def orto(self,x1,y1,x2,y2):
        if abs(x2-x1)>abs(y2-y1):
            y2=y1
        else:
            x2=x1
        return x2,y2

    def ortoRes(self,x1,y1,x2,y2):
        i=1
        if x2==x1:
            if y1>y2:
                i=-1
            y2=y1+i*self.com
        else:
            if x1>x2:
                i=-1
            x2=x1+i*self.com
        return x2,y2

#выход из редактора
    def exitMethod(self):
        self.save_change()
        e = self.donate()
        if e != 3:
            self.master1.destroy()

    #please, donate!

    def d(self):
        eroot = Toplevel()
        eroot.title('Donate adress')
        self.don = PhotoImage(file = os.path.join(self.appPath, 'res', 'don.gif'))
        val = '5213 2437 3660 6532'
        val2 = '1Kgect6s92fhRftHeuLVqgPJ1FYt7Lhee9'
        val3 = 'simonovsen@gmail.com'
        l_donate = Text(eroot, relief = 'flat', height = 1, width = len(val), bg = 'light gray')
        l_donate11 = Label(eroot, text = 'Bank card:')
        l_donate12 = Label(eroot, text = 'Bitcoin adress:')
        l_donate13 = Label(eroot, text = 'PayPal account:')
        l_donate2 = Text(eroot, relief = 'flat', height = 1, width = len(val2), bg = 'light gray')
        l_donate3 = Text(eroot, relief = 'flat', height = 1, width = len(val3), bg = 'light gray')
        l_donate.insert(END, val)
        l_donate2.insert(END, val2)
        l_donate3.insert(END, val3)
        l_donate.configure(state = DISABLED)
        l_donate2.configure(state = DISABLED)
        l_donate3.configure(state = DISABLED)

        l_donate11.grid(row=0, column = 0, sticky = 'w', padx = 3, pady = 3)
        l_donate.grid(row=0, column = 1, sticky = 'w', padx = 3, pady = 3)

        l_donate12.grid(row=1, column = 0, sticky = 'w', padx = 2, pady = 3)
        l_donate2.grid(row=1, column = 1, sticky = 'w', padx = 3, pady = 3)

        l_donate13.grid(row=2, column = 0, sticky = 'w', padx = 2, pady = 3)
        l_donate3.grid(row=2, column = 1, sticky = 'w', padx = 3, pady = 3)

        but = Button(eroot, text = 'OK', command = eroot.destroy)
        but.grid(row=3, column = 1, sticky = 'e', padx = 10, pady = 10)

    def donate(self):
        e = randint(2, 5)
        if e == 3:
              eroot = Toplevel()
              eroot.title('Please, donate!')
              self.don = PhotoImage(file = os.path.join(self.appPath, 'res', 'don.gif'))
              eroot.tk.call('wm', 'iconphoto', eroot._w, self.don)
              eroot.resizable(width=FALSE, height=FALSE)
              from locale import getdefaultlocale
              lang = getdefaultlocale()
              if lang[0][0:2] != 'ru':
                  donate_text = u'''
            SAMoCAD - open sours program,
            so developers want to eat.

            You can help the project.
            '''
                  feed = 'Feed :-)'
                  away = 'Get away from me!'
              else:
                  donate_text = u'''
            SAMoCAD - бесплатная програма,
            поэтому разработчики хотят кушать.

            Вы можете помочь проекту.
            '''
                  feed = u'Накормить'
                  away = u'Отстаньте от меня!'

              l_donate = Label(eroot, justify = LEFT, text = donate_text)

              self.imag = PhotoImage(file = os.path.join(self.appPath, 'res', 'icon3.gif'))

              but = Button(eroot, text = feed, command = self.d)
              but2 = Button(eroot, text = away, command = self.master1.destroy)
              ca = Canvas(eroot, width = 100, height = 100)
              ca.create_image(0,0,anchor=NW,image = self.imag)
              ca.grid(row=0, column = 0, rowspan = 2, padx = 5, pady = 5)
              l_donate.grid(row=0, column = 1,columnspan = 2, padx = 10, pady = 10)
              but.grid(row=1, column = 1, padx = 10, pady = 10)
              but2.grid(row=1, column = 2, padx = 10, pady = 10)
        return e


#РИСОВАНИЕ ОБЪЕКТОВ - СОБЫТИЯ
    #ПОСТРОЕНИЕ ВРЕМЕННЫХ ЛИНИЙ
    def temp_lines(self, event):
        self.oldinfo = self.info.cget('text')
        self.info.config(text = (self.oldinfo + ' Create temp lines - line 2'))
        Num = self.c.gettags(self.c.find_withtag('current'))[1]
        self.temp_collection.append(Num)
        #self.c.tag_bind('Line', '<Button-3>', self.temp_lines2)

    def temp_lines2(self, event):
        self.info.config(text = self.oldinfo)
        Num = self.c.gettags(self.c.find_withtag('current'))[1]
        self.temp_collection.append(Num)
        stopFlag = False
        if len(self.temp_collection) > 1:
            for i in self.temp_collection:
                if i not in self.ALLOBJECT:
                    stopFlag = True
            if stopFlag == False:
                c = map(lambda i: self.c.coords(self.c.find_withtag(i)[0]), self.temp_collection)
                x, y = calc.intersection_stright(c[0][0],c[0][1],c[0][2],c[0][3],c[1][0],c[1][1],c[1][2],c[1][3])
                if x != None:
                    self.c_line(x-5,y-5,x+5,y+5,fill='gray',width=1,sloy = 'temp', tip = 'temp')
                    self.temp_lines_list.append(self.Nline)
                    self.c_line(x+5,y-5,x-5,y+5,fill='gray',width=1,sloy = 'temp', tip = 'temp')
                    self.temp_lines_list.append(self.Nline)
                    self.c.bind_class(self.master1, "<Control-KeyPress-j>", self.del_temp_lines)
            self.temp_collection = []

    def del_temp_lines(self, event=None):
        find = self.c.find_withtag('temp')
        del_list = []
        for i in find:
            Num = self.c.gettags(i)[1]
            del_list.append(Num)
        if del_list:
            self.delete(elements = del_list)
            self.c.unbind_class(self.master1, "<Control-KeyPress-j>")


    #ЛИНИЯ
    def risLine(self):
        self.curent_class = line.Line(graf)

    #РАЗМЕР
    def risDim(self):
        self.curent_class = dimension.Dimension(graf)

    def risDimR(self):
        self.curent_class = dimension.Dimension_R(graf)

    #ТЕКСТ
    def risText(self, event = None):
        self.curent_class = text_line.Text(graf)

#МЕТОДЫ ЧЕРЧЕНИЯ ОБЪЕКТОВ
    #КРУГ
    def risCircle(self):
        self.curent_class = circle.Circle(graf)

    #ДУГА
    def risArc(self):
        self.curent_class = arc.Arc(graf)

#ЛИНИЯ
    def c_line(self, x1, y1, x2, y2, width = None, sloy = None, fill = None, stipple = None, tip = 'norm'):
        self.curent_class = line.c_line(graf, x1, y1, x2, y2, width, sloy, fill, stipple, tip)

    def copy_line(self, content):
        self.Nlined += 1
        self.Nline = 'L' + str(self.Nlined)
        self.ALLOBJECT[self.Nline] = self.ALLOBJECT[content].copy()
        return self.Nline
   
#РАЗМЕР ЛИНЕЙНЫЙ
    def dim(self,x1,y1,x2,y2,x3,y3,text=None, sloy = None,
                                                fill = None,
                                                size = None,
                                                ort = None,
                                                text_change = 'unchange',
                                                text_place = None,
                                                s=None,
                                                vv_s=None,
                                                vr_s = None,
                                                arrow_s = None,
                                                type_arrow = None,
                                                s_s = None,
                                                w_text = None,
                                                font = None):
        
        self.curent_class = dimension.c_dim(self,x1,y1,x2,y2,x3,y3,text, sloy,
                                                fill,
                                                size,
                                                ort,
                                                text_change,
                                                text_place,
                                                s,
                                                vv_s,
                                                vr_s,
                                                arrow_s,
                                                type_arrow,
                                                s_s,
                                                w_text,
                                                font)
    
    def get_snap_line(self, cont):#Находит в сложном объекте линии привязки
        lines = []
        if cont[0] in ('d', 'r'):
            for i in self.ALLOBJECT[cont]['id']:
                tag = self.ALLOBJECT[cont]['id'][i]
                if 'priv' in tag:
                    if 'dim_text' not in tag and 'dimr_text' not in tag:
                        lines.append(i)
        else:
            for i in self.ALLOBJECT[cont]['id']:
                tag = self.ALLOBJECT[cont]['id'][i]
                if 'priv' in tag:
                    lines.append(i)
        return lines
   
#РАЗМЕР РАДИУСНЫЙ
    def dimR(self,x1,y1,x2,y2, text=None, sloy = None,
                                                fill = None,
                                                size = None,
                                                s=None,
                                                vr_s = None,
                                                arrow_s = None,
                                                type_arrow = None,
                                                s_s = None,
                                                w_text = None,
                                                font = None,
                                                Rn = None):
        
        self.curent_class = dimension.c_dimR(self,x1,y1,x2,y2, text, sloy,
                                                fill,
                                                size,
                                                s,
                                                vr_s,
                                                arrow_s,
                                                type_arrow,
                                                s_s,
                                                w_text,
                                                font,
                                                Rn)
   
#КРУГ
    def c_circle(self,x0,y0,xr = None, yr = None, width = None, sloy = None, fill = None, R = None):
        self.curent_class = circle.c_circle(graf, x0, y0, xr, yr, width, sloy, fill, R)
 
#ДУГА
    def c_arc(self,x0,y0,xr1=None, yr1=None, xr2=None, yr2=None, width = None, sloy = None, fill = None, R = None, start = None, extent = None):
        self.curent_class = arc.c_arc(graf, x0,y0,xr1, yr1, xr2, yr2, width, sloy, fill, R, start, extent)
    
#ТЕКСТ
    def c_text(self, x, y, text, anchor = 'sw', sloy = None, fill = None, angle = 0, size = None, s_s = None, w_text = None, font = None): #Текст - отрисовка
        self.curent_class = text_line.c_text(graf, x, y, text, anchor, sloy, fill, angle, size, s_s, w_text, font)

#Печать картинки в постскрипт
    def print_postScript(self, event = None):
        self.curent_class = print_ps.Print_PS(graf)

    def enumerator_p(self):
        self.enumerator +=1
        if self.enumerator == 20:
            self.enumerator = 0
            self.fileCurSave()

    def exportDXF(self):
        self.s_dxf = True
        self.fileSave()
        self.s_dxf = False

    def fileSave(self):
        opt = options = {}
        if self.s_dxf == False:
            options['defaultextension'] = '.txt'
            options['filetypes'] = [('text files', '.txt'),
                                ('all files', '.*')]
        else:
            options['defaultextension'] = '.dxf'
            options['filetypes'] = [('text files', '.dxf'),
                                ('all files', '.*')]
        options['initialdir'] = self.appPath
        options['initialfile'] = 'draft_1'
        options['parent'] = self.master1
        options['title'] = 'Save file'
        f = tkFileDialog.asksaveasfile(mode='w', **opt)
        if f:
            if self.zoomOLD != 0:
                if self.zoomOLD>0:
                    self.c.scale('obj',0,0,zoomm**self.zoomOLD,zoomm**self.zoomOLD)
                else:
                    zoomOLDx=self.zoomOLD*(-1)
                    self.c.scale('obj',0,0,zoomp**zoomOLDx,zoomp**zoomOLDx)
            xynach=self.c.coords(self.nachCoordy)
            dx=-xynach[0]
            dy=-xynach[1]
            self.c.move('obj',dx+10,dy+10)
            if self.s_dxf == False:
                save = save_file.saver(graf)
                for i in save.write_list:
                    if i[:8] == 'self.c_t' or i[:8] == 'self.dim':
                        f.write(codecs.BOM_UTF8)
                    f.writelines("%s\n" % i.encode("utf8"))
                f.close()
                self.saveFlag = True
                self.changeFlag = False
                self.current_file = f.name
                self.master1.title(self.prog_version + ' - ' + self.current_file)
            else:
                save = to_dxf.Dxfer(graf)
                for i in save.write_list:
                    f.writelines("%s\n" % i)

            if self.zoomOLD != 0:
                self.c.move('obj',-dx-10,-dy-10)

                if self.zoomOLD>0:
                    self.c.scale('obj',0,0,zoomp**self.zoomOLD,zoomp**self.zoomOLD)

                else:
                    zoomOLDx=self.zoomOLD*(-1)
                    self.c.scale('obj',0,0,zoomm**zoomOLDx,zoomm**zoomOLDx)

    def fileCurSave(self):
        if self.saveFlag == False:
            self.fileSave()
        else:
            back_file = self.current_file[0:-4]+'.bak'
            try:
                copyfile(self.current_file, back_file)
            except IOError:
                print 'Error Back file'
            f = open(self.current_file, 'w')
            if self.zoomOLD != 0:
                if self.zoomOLD>0:
                    self.c.scale('obj',0,0,zoomm**self.zoomOLD,zoomm**self.zoomOLD)
                else:
                    zoomOLDx=self.zoomOLD*(-1)
                    self.c.scale('obj',0,0,zoomp**zoomOLDx,zoomp**zoomOLDx)
            xynach=self.c.coords(self.nachCoordy)
            dx=-xynach[0]
            dy=-xynach[1]
            self.c.move('obj',dx+10,dy+10)

            save = save_file.saver(graf)
            for i in save.write_list:
                if i[:8] == 'self.c_t' or i[:8] == 'self.dim':
                    f.write(codecs.BOM_UTF8)

                f.writelines("%s\n" % i.encode("utf8"))
            f.close()
            self.changeFlag = False

            if self.zoomOLD != 0:
                self.c.move('obj',-dx-10,-dy-10)

                if self.zoomOLD>0:
                    self.c.scale('obj',0,0,zoomp**self.zoomOLD,zoomp**self.zoomOLD)

                else:
                    zoomOLDx=self.zoomOLD*(-1)
                    self.c.scale('obj',0,0,zoomm**zoomOLDx,zoomm**zoomOLDx)

    def new(self, event = None):
        self.save_change()
        self.saveFlag = False
        self.changeFlag = False
        self.current_file = 'New draft'
        self.master1.title(self.prog_version + ' - ' + self.current_file)
        self.delete(elements = self.ALLOBJECT.keys())
        self.sbros_all()

    def sbros_all(self):
        self.collection = []
        self.collectionBack = []
        self.history_undo = []

    def save_change(self):
        if self.ALLOBJECT and self.changeFlag == True:
            save_yes_no = tkMessageBox.askyesno('Save draft?', u'Save drawing?')
            if save_yes_no == True:
                self.fileCurSave()

    def importDXF(self):
        self.s_dxf = True
        self.fileOpen()
        self.s_dxf = False

    def fileOpen(self, event = None):
        self.save_change()
        opt = options = {}
        if self.s_dxf == False:
            options['defaultextension'] = '.txt'
            options['filetypes'] = [('text files', '.txt'),
                                    ('all files', '.*')]
            options['title'] = 'Open file'
        else:
            options['defaultextension'] = '.dxf'
            options['filetypes'] = [('DXF files', '.dxf'),
                                    ('all files', '.*')]
            options['title'] = 'Import from DXF'
        options['initialdir'] = self.appPath
        options['parent'] = self.master1

        f = tkFileDialog.askopenfile(**opt)
        if f:
            if self.ALLOBJECT:
                self.delete(elements = self.ALLOBJECT.keys())
            if self.zoomOLD != 0:
                if self.zoomOLD>0:
                    self.c.scale('obj',0,0,zoomm**self.zoomOLD,zoomm**self.zoomOLD)
                else:
                    zoomOLDx=self.zoomOLD*(-1)
                    self.c.scale('obj',0,0,zoomp**zoomOLDx,zoomp**zoomOLDx)
            zoomOLD = self.zoomOLD
            self.zoomOLD = 0
            xynach=self.c.coords(self.nachCoordy)
            dx=-xynach[0]
            dy=-xynach[1]
            self.c.move('obj',dx+10,dy+10)
            if self.s_dxf == False:
                list_command = f.readlines()
            else:
                text = f.read()
                DXF = from_dxf.DXFopener(text)
                list_command = DXF.command_list
            if list_command:
                for i in list_command:
                    #try:
                    exec(i)
                    #except:
                        #print 'Error in opened file!'
                        #print repr(i)
                        #continue
            f.close()
            if self.s_dxf == False:
                self.saveFlag = True
                self.changeFlag = False
                self.current_file = f.name
                self.master1.title(self.prog_version + ' - ' + self.current_file)
            else:
                self.saveFlag = False
                self.changeFlag = True
                self.current_file = 'New draft'
                self.master1.title(self.prog_version + ' - ' + self.current_file)
            self.sbros_all()


            self.c.move('obj',-dx-10,-dy-10)
            self.zoomOLD = zoomOLD
            if zoomOLD != 0:
                if zoomOLD>0:
                    self.c.scale('obj',0,0,zoomp**zoomOLD,zoomp**zoomOLD)
                else:
                    zoomOLDx=zoomOLD*(-1)
                    self.c.scale('obj',0,0,zoomm**zoomOLDx,zoomm**zoomOLDx)


    def zoomP(self,x,y):
        self.c.scale('obj',x,y,zoomp,zoomp)

    def zoomM(self,x,y):
        self.c.scale('obj',x,y,zoomm,zoomm)

    def zoommerP(self):
        x=self.frame1.winfo_width()/2.0
        y=self.frame1.winfo_height()/2.0
        self.zoomOLD += 1
        if self.zoomOLD == -19:
            self.c.itemconfig('t_LOD', state = 'normal')
            self.c.itemconfig('snap_text', stipple = ('@'+os.path.join(self.appPath, 'res', '00.xbm')))
        self.c.scale('obj',x,y,zoomp,zoomp)
        

    def zoommerM(self):
        x=self.frame1.winfo_width()/2.0
        y=self.frame1.winfo_height()/2.0
        self.zoomOLD -= 1
        if self.zoomOLD ==-20:
            self.c.itemconfig('t_LOD', state = 'hidden')
            self.c.itemconfig('snap_text', stipple = '')
        self.c.scale('obj',x,y,zoomm,zoomm)

    def Mzoommer(self,event):
        x = self.priv_coord[0]#event.x
        y = self.priv_coord[1]#event.y
        #if x<0:
            #x = -x
        #if y<0:
           # y = -y
        if event.delta > 0 or event.num == 4:
            self.zoomOLD += 1
            if self.zoomOLD == -19:
                self.c.itemconfig('t_LOD', state = 'normal')
                self.c.itemconfig('snap_text', stipple = ('@'+os.path.join(self.appPath, 'res', '00.xbm')))
            self.c.scale('obj',x,y,zoomp,zoomp)
            #self.zoomP(x,y)

        else:
            self.zoomOLD -= 1
            if self.zoomOLD ==-20:
                self.c.itemconfig('t_LOD', state = 'hidden')
                self.c.itemconfig('snap_text', stipple = '')
            self.c.scale('obj',x,y,zoomm,zoomm)
            #self.zoomM(x,y)

    def mouseMove(self,event):
        global x1,y1
        self.c.move('obj', event.x - x1, event.y - y1)
        x1 = event.x
        y1 = event.y

    def OnMouseMove(self,event):
        global x1,y1
        x1 = event.x
        y1 = event.y


root = Tk()

graf=Graphics()
graf.initial(root)
root.mainloop()
