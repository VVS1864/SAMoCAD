#!/usr/bin/python
# -*- coding: utf-8 -*-
#from __future__ import division
import src.clip as clip
import src.line as line
import src.gui  as gui
import src.undo as undo

import src.sectors_alg as sectors_alg
import src.opengl_wrapper as opengl_wrapper

import src.select_clone as select_clone
import src.motion_event as motion_event
import src.right_mouse_event as right_mouse_event
import src.left_mouse_event as left_mouse_event

import src.dxf_library.color_acad_rgb as color_acad_rgb

from OpenGL.GL import *
from OpenGL.GLU import *


import time as t
import wx
from random import random, randint, uniform
import copy
import os
import sys
import array

class Graphics:
    def __init__(self):
        self.init = False

        if 'linux' in sys.platform:
            self.os = 'linux'
        else:
            self.os = 'windows'
        print 'OS', sys.platform, ', ', 'defined as', self.os
            
            
        self.scale_size = 1.5
        
        self.vbo = None
        self.color_vbo = None

        self.vbo_col = None
        self.color_vbo_col = None

        self.dynamic_vbo = None

        # Ширина и высота рабочей области
        self.drawing_w = 1000000.0
        self.drawing_h = 1000000.0
        self.q_scale = 10000

        self.ex = 0.0
        self.ey = 0.0
        self.ex2 = 0.0
        self.ey2 = 0.0
        self.ex3 = 0.0
        self.ey3 = 0.0

        self.mouse_x = 0
        self.mouse_y = 0

        self.min_e = 0.00001 #Минимальная величина чертежа

        #переменные для отображениия
        self.zoomOLD = 0
        
        self.layer = '1' #Текущий слой
        self.color = [255, 255, 255] #Текущий цвет
        self.width = 2 #Текущая толщина
        self.stipple = None
        self.factor_stipple = 200 #размер типа линий
        self.layers = {
            self.layer:{
                'color':self.color,
                'width':self.width,
                'stipple':self.stipple,
                'factor_stipple':self.factor_stipple,
                },
            }
        self.default_layer = copy.copy(self.layers['1'])
        print 'layers', self.layers
        
        self.select_color = [0, 255, 0] #Цвет выделяемых объектов
        self.priv_color = [0, 255, 255] #Цвет привязки
        self.back_color = 'black'
        self.right_color = [0, 255, 255]#'light blue'
        self.left_color = [255, 0, 0]#'red'
        self.text_size = 500 #Текущий размер шрифта текста (5 мм)
        self.dim_text_size = 350 #Текущий размер шрифта размеров (3.5 мм)
        self.size_simbol_p = 20 #Размер значка привязки
        self.anchor = 'sw' #Текущая привязка текста
        self.text_font = 'TXT'#'Architectural'
        self.text_s_s = 1.0 #Межбуквенное расстояние
        self.text_w = 1.4 #Ширина буквы
        self.s = 50 #Расстоение от низа текста до размерной линии (в размере)
        self.arrow_s = 100 #Размер стрелки
        self.vr_s = 200 #Вылет за размерную линию
        self.vv_s = 100 #Вылет размерной линии
        self.type_arrow = 'Arch'
        self.dim_text_s_s = 1.0
        self.dim_text_w = 1.5
        self.dim_text_font = 'TXT'#'Architectural'
        self.snap_s = 10 #Определяет дальнобойность привязки (расстояние в точках на экране)
        self.angle_s = 15.0 #Угол трассировки
        self.auto_save_step = 30 #Количество действий между автосохранениями

        self.total_N = 0 #тотальное количество нарисованных объектов (для ID)

        #Типы линий
        self.stipples_list = (
            '_____________',
            '_ _ _ _ _ _ _',
            '____ _ ____ _',
            '____ _ _ ____',
            )
        self.stipples_values = (
            None,
            (1,1),
            (4,1,1,1),
            (4,1,1,1,1,1),
            )
        
        self.stipples = dict((i, self.stipples_values[ind]) for ind, i in enumerate(self.stipples_list))       
        self.DXF_RGB_colores = color_acad_rgb.DXF_RGB_colores
        self.RGB_DXF_colores = {v: k for k, v in self.DXF_RGB_colores.items()}
            
        #Толщины линий
        self.widthes = [
            "1",
            "2",
            "3",
            "4",
            ]

        self.properties = {
            'color':('Color', 'color'),
            'layer':('Layer', self.layers.keys()),
            'width':('Width', self.widthes),
            'stipple':('Line type', self.stipples_list),
            'factor_stipple':('Line size', 'Num'),
            'text_size':('Text size', 'Num'),
            's':('Offset from dim line', 'Num'),
            'vr_s':('Extend ticks', 'Num'),
            'vv_s':('Extend dim lines', 'Num'),
            'arrow_s':('Arrowhead size', 'Num'),
            'type_arrow':('Arrowheads', None),
            'text_s_s':('Letters distance factor', 'Num'),
            'text_w':('Width of letters factor', 'Num'),
            'text_font':('Text font', None),
            'dim_text_size':('Dim text size', 'Num'),
            'dim_text_s_s':('Letters distance factor', 'Num'),
            'dim_text_w':('Width of letters factor', 'Num'),
            'dim_text_font':('Dim font', None),
            }

        self.objects_base_parametrs = {}
        
        self.old_func = (self.action, line.Line)
        self.prog_version = 'Samocad - v0.0.9.0'
        self.old_text = self.prog_version
        self.old_offset = 0
        self.old_fillet_R = 0
        self.old_scale = 1
        self.old_print_scale = 100.0
        
        self.motion_flag = False #True - Если нажата ср. кн. мыши
        self.current_flag = True #True - если можно подсвечивать текущий объект под курсором
        self.current_select_flag = True #True - если можно захватить/выкинуть текущий объект под курсором
        self.trace_flag = False #Трасировка off-on
        self.trace_obj_flag = False #объектное отслеживание off-on
        self.snap_flag = True #Привязка off-on

        self.ortoFlag=False #Если True - значит орто вкл
        self.trace_on = False
        self.trace_obj_on = False
        #self.tracingFlag = True
        #self.tracing_obj_Flag = True
        self.snap_near = True #Привязка к ближайшей
        #self.lappingFlag = False #Если True - значит активен квадрат выделения
        self.resFlag = False #Если True - значит рисуем объекты
        #self.anchorFlag = False #Если True - режим выбора привязки текста
        self.saveFlag = False
        self.changeFlag = False
        
        self.current_print_file = os.path.join(os.getcwd(), 'print_1')
        self.current_file = 'New_draft.dxf'
        self.current_save_path = os.path.join(os.getcwd(), self.current_file)
        
        self.s_dxf = False
        self.curent_class = None
        
        self.rect = False #True если рисуется рамка выделения
        self.print_flag = False #True если выбор области печати
        self.print_rect = [] #Область печати
        
        self.snap = None #None если нет захвата привязки
        self.current_select = False #True если объект под курсором и его можно выбрать
        self.current_change = False #True если объект под курсором можно редактировать
        self.current = None #Текущий объект под курсором
        self.temp = False #True, если работает "резиновость" - временное рисавание объекта

        self.func_collection = [] #Объекты из коллекции, над которыми уже было проведено действие
        self.collection = [] #Выделенные объекты
        self.find_privs = [] #Набор объектов-привязок
        self.collectionBack = [] #Сброшенный набор объектов
        self.temp_collection = []
        self.temp_lines_list = []
        self.ALLOBJECT = {} #ВСЕ объекты (Объект : {параметр : значение}}
        self.all_clone = {}

        #Список событий:
        #Структура history_undo:
        #[action,]
        #action =  [mode, {object_id:parametrs,}]
        #parametrs =  {parametr:value,} для del
        #parametrs = None для create
        self.history_undo = []
        self.set_replace = set()

        self.drawing_rect_data = [
            0.0, 0.0, self.drawing_w, 0.0,
            0.0, 0.0, 0.0, self.drawing_h,
            self.drawing_w, self.drawing_h, self.drawing_w, 0.0,
            self.drawing_w, self.drawing_h, 0.0, self.drawing_h
                                  ]
        self.drawing_rect_color = [255, 255, 255]*(len(self.drawing_rect_data)//2)

        self.clear_pointdata()

        #self.pointdata = array.array('f', [])
        #self.colordata = array.array('B', [])
        

        self.collection_data = []
        self.collection_color = []
        self.standart_state()
        
        self.activIDs = set() #Массив активных ID (которые в активных секторах)
        self.activSectors = [] #Активные сектора
        
        
        
        self.trace_x1 = 0
        self.trace_y1 = 0
        self.trace_x2 = 0
        self.trace_y2 = 0

        #Технические переменные
        self.first = True
        

        self.interface = gui.Window(None, self.current_file + ' - '+ self.prog_version, self)
        self.gl_wrap = opengl_wrapper.GL_wrapper(self)
        self.c = self.interface.canvas
        self.info = self.interface.info
        self.info2 = self.interface.info2
        self.cmd = self.interface.cmd
        self.cmd.SetFocus()
        if self.os != 'linux':
            self.interface.Show(True)
            self.gl_wrap.OnDraw(None)
        wx.EVT_ERASE_BACKGROUND(self.c, self.gl_wrap.OnEraseBackground)
        wx.EVT_PAINT(self.c, self.gl_wrap.OnDraw)
        wx.EVT_SIZE(self.c, self.gl_wrap.OnSize)

         
        
        
    def initial(self):
        #События мыши
        self.c.Bind(wx.EVT_MIDDLE_DOWN, self.move_on)
        
        self.c.Bind(wx.EVT_MIDDLE_UP, self.move_off)
        self.interface.Bind(wx.EVT_CLOSE, self.gl_wrap.destroy)
        
        if self.os == 'linux':
            self.c.Bind(wx.EVT_MOUSEWHEEL, self.zoom_event)
        else:
            self.interface.cmd.Bind(wx.EVT_MOUSEWHEEL, self.zoom_event)
            
        self.create_sectors()
       
        t1 = t.time()
        for i in xrange(1): #Количество вершин
            x1,y1 = uniform(0.0, 1000.0), uniform(0.0, 1000.0)
            x2,y2 = uniform(0.0, 1000.0), uniform(0.0, 1000.0)
            line.c_line(
                graf, x1, y1, x2, y2,
                width = self.width,
                layer = self.layer,
                color = self.color,
                stipple = None,
                factor_stipple = 1,
                in_mass = True,
                        )
        
        line.c_line(
            graf, 50, 50, 50, 300,
            width = self.width,
            layer = self.layer,
            color = self.color,
            stipple = None,
            factor_stipple = 1,
            in_mass = True,
                    )
        line.c_line(
            graf, 50, 50, 500, 50,
            width = self.width,
            layer = self.layer,
            color = self.color,
            stipple = None,
            factor_stipple = 1,
            in_mass = True,
                    )
        
        
            
        self.ALLOBJECT, self.sectors = sectors_alg.quadric_mass(self.ALLOBJECT, self.ALLOBJECT.keys(), self.sectors, self.q_scale)
        
        print 'Create lines', t.time() - t1
        
        
        
        self.standart_binds()
        self.interface.Show(True)
        for i in xrange(10):
            self.zoom((0,500), -1)

    

    def create_sectors(self):
        t1 = t.time()
        #del self.sectors
        self.sectors = {}
        #Разбивка поля на сектора
        for i in xrange(int(self.drawing_w/self.q_scale)):
            for j in xrange(int(self.drawing_h/self.q_scale)):
                c = str(i) +' '+ str(j)
                self.sectors[c] = []
        print int(self.drawing_w/self.q_scale)
        print int(self.drawing_h/self.q_scale)
        print 'set drawing width', int(self.drawing_w)
        print 'set drawing hight', int(self.drawing_h)
        print 'Create sectors', t.time() - t1, 'sec'

    def mem(self):
        print len(self.point_color_data_vbo_dict[1][0])+len(self.point_color_data_vbo_dict[2][0])+len(self.point_color_data_vbo_dict[3][0])+len(self.point_color_data_vbo_dict[4][0])
        
    def focus_cmd(self, e = None):
        self.cmd.SetFocus()
        

    def standart_binds(self):
        self.c.Unbind(wx.EVT_LEFT_DOWN)
        self.c.Unbind(wx.EVT_RIGHT_DOWN)
        self.c.Unbind(wx.EVT_MOTION)
        self.interface.cmd.Unbind(wx.EVT_KEY_DOWN)
        
        self.c.Bind(wx.EVT_RIGHT_DOWN, lambda x: right_mouse_event.right_mouse_event(self))
        self.c.Bind(wx.EVT_LEFT_DOWN, self.left_mouse_event)
        self.c.Bind(wx.EVT_MOTION, self.motion)
        self.interface.cmd.Bind(wx.EVT_KEY_DOWN, self.key)


    def standart_state(self):
        self.red_line_data = []
        self.red_line_color = []
        self.snap_data = []
        self.snap_color = []
        self.current_data = []
        self.current_color = []
        self.tempdata = []
        self.tempcolor = []
        self.trace_data = []
        self.trace_color = []
        self.rect_data = []
        self.rect_color = []
        self.dynamic_data = []
        self.dynamic_color = []
        self.dynamic_vbo_data = []

    def clear_pointdata(self):
        '''
        self.vbo_1 = glGenBuffers(1)
        self.color_vbo_1 = glGenBuffers(1)
        
        self.vbo_2 = glGenBuffers(1)
        self.color_vbo_2 = glGenBuffers(1)
        
        self.vbo_3 = glGenBuffers(1)
        self.color_vbo_3 = glGenBuffers(1)
        
        self.vbo_4 = glGenBuffers(1)
        self.color_vbo_4 = glGenBuffers(1)
        '''
        
        '''
        try:
            pd = self.point_color_data_vbo_dict
        except AttributeError:
            pd = None
        else:
            glDeleteBuffers(1, [pd[1][2], pd[1][3], pd[2][2], pd[2][3], pd[3][2], pd[3][3], pd[4][2], pd[4][3]])

        try:
            del pd
            del self.point_color_data_vbo_dict
        except AttributeError:
            pass
        '''
        self.point_color_data_vbo_dict = {
        #Width: [pointdata,            colordata,            color_vbo,        vbo]
            1 : [array.array('f', []), array.array('B', []), None,             None],
            2 : [array.array('f', []), array.array('B', []), None,             None],
            3 : [array.array('f', []), array.array('B', []), None,             None],
            4 : [array.array('f', []), array.array('B', []), None,             None],
            }
        
    def update_prop(self):
        self.interface.OnPropDialog()
        
    def amount_of_select(self):
        amount = len(self.collection)
        if amount:            
            self.info2.SetValue(('Selected %s objects. Enter - stop')%(amount))
        else:
            self.info2.SetValue((''))

    def change_pointdata(self):
        self.gl_wrap.change_pointdata()    

    def action(self, object_class):
        self.curent_class = object_class(self)
        #self.resFlag = True

    def from_cmd(self, type_data):
        data = self.cmd.GetValue()
        try:
            data = type_data(data)
        except:
            data = None
        return data

    
    def get_world_coords(self, x, y):
        size = glGetIntegerv(GL_VIEWPORT)  
        xy = gluUnProject(x, size[3]-y, 0)

        return xy[0], xy[1]
        
    def zoom_event(self, e):
        xy = wx.GetMousePosition()
        w = e.GetWheelRotation()
        canvas_xy = self.c.GetScreenPosition() 
        xy = (xy[0] - canvas_xy[0], xy[1] - canvas_xy[1])

        self.zoom(xy, w)        
        
    def zoom(self, xy, w):
        x, y = self.get_world_coords(xy[0], xy[1])
        xy1 = gluUnProject(1, 0, 0)
        xy2 = gluUnProject(0, 0, 0)
        
        glTranslate(x, y, 0)
        
        if w < 0:
            glScalef(1.0/self.scale_size, 1.0/self.scale_size, 1.0/self.scale_size)
        else:
            if xy1[0]-xy2[0] >= self.min_e:
                glScalef(self.scale_size, self.scale_size, self.scale_size)
            else:
                print 'Max size!'
        glTranslate(-x, -y, 0)
        
        self.c.Refresh()              #Обновить картинку
        #self.c.Update()
        

    def motion_plane(self, e):
        x = e.GetX()
        y = e.GetY()
        xy1 = gluUnProject(x, y, 0)
        xy2 = gluUnProject(self.mouse_x, self.mouse_y, 0)
        
        glTranslate((xy1[0] - xy2[0]), (xy2[1] - xy1[1]), 0)
        
        
        self.mouse_x = x
        self.mouse_y = y

    def back_collection(self):
        #Возвращает в коллекцию предыдущий набор, если начего не рисуется и коллекция не пуста
        if self.resFlag == False and not self.collection:
            self.mass_collector(self.collectionBack, 'select')
        self.c.Refresh()
            #select_clone.Select_clone(self.collection, graf)
            #self.colObj()#Посчитать колличество выделенных объектов
            #draft_gui.gui.update_prop()

    def delete_objects(self, objects, add_history = False):
        #Уделение объектов
        if add_history:
            undo.add_undo(self, objects, mode = 'del')
        #else:
        for i, o in enumerate(objects):
            for s in self.ALLOBJECT[o]['sectors']:
                self.sectors[s].remove(o)
            del self.ALLOBJECT[o]
            
        if 'trace' in self.ALLOBJECT:
            for s in self.ALLOBJECT['trace']['sectors']:
                self.sectors[s].remove('trace')
            del self.ALLOBJECT['trace']
             
        #self.pointdata = array.array('f', [])
        #self.colordata = array.array('B', [])
        self.clear_pointdata()
        
        #if 'trace' in self.ALLOBJECT:
            #del self.ALLOBJECT['trase']
        for obj in self.ALLOBJECT.values():
            pointdata = obj['pointdata']
            len_pointdata = len(pointdata)/2

            self.point_color_data_vbo_dict[obj['width']][0].extend(pointdata)
            self.point_color_data_vbo_dict[obj['width']][1].extend(len_pointdata*obj['color'])
            #self.pointdata.fromlist(pointdata)
            #self.colordata.fromlist(len_pointdata*obj['color'])

                

        
    def mass_collector(self, objects, select):
        a = set(self.collection)
        b = set(objects)
        if select == 'select':
            a.update(b)
        else:
            a.difference_update(b)

        self.collection = list(a)
        self.collection_data, self.collection_color = select_clone.select_clone(
                                                            self,
                                                            self.collection,
                                                            self.select_color,
                                                            )
        self.gl_wrap.c_collection_VBO()

    def edit_collector(self, objects, x, y):
        #Проверяет, какие объекты находятся в коллекции:
        #если только размеры по линии - оставляет коллекцию неизменной,
        #если есть другие объекты - оставляет в кол. только те, к которым есть привязка в данный момент

        dim_list = []#Список размеров из коллекции
        line_dim_edit = True #True - пока не попался НЕразмер
        
        bFlag = False#Если False - то все размерные линии имеют одну общую координату (x или y) и лежат по одной линии

        for i in objects:#Перебрать пришедшую коллекцию
            if self.ALLOBJECT[i]['object'] == 'dim':
                dim_list.append(i)#Добавить в список размеров
            else:
                line_dim_edit = False#Иначе неразмер попался

#!!! - определяет, по одной линии все размеры или нет.
#Если да - можно радактировать всю размерную цепочку
        if line_dim_edit == True:#Если ни одного НЕразмера не попалось
            if len(dim_list) > 1:#Если количество размеров > 1
                
                line3_list = []#Список первых координат размерных линий размеров                
                ort1 = self.ALLOBJECT[dim_list[0]]['ort']
                if ort1 == 'vertical':
                    line_3_xy = (self.ALLOBJECT[dim_list[0]]['line3'][0], 0, x)
                else:
                    line_3_xy = (self.ALLOBJECT[dim_list[0]]['line3'][1], 1, y)
                    
                for i in dim_list[1:]:# Перебрать список размеров
                    ort2 = self.ALLOBJECT[i]['ort']
                    if ort1 != ort2:#Если переменные не равны - Вылететь, коллекцию больше не изменять
                        bFlag = True
                        break
                    line3 = self.ALLOBJECT[i]['line3']#Взять размерную линию размера                    
                    if line3[line_3_xy[1]] != line_3_xy[0] and abs(line3[line_3_xy[1]] - line_3_xy[1]) > self.min_e:
                        bFlag = True
                        break
            if bFlag == False:#Если вылетания и теперь не произошло
                objects = dim_list#Коллекция = списку размеров
            
            
        return objects

    def get_current_objects(self, rect, enclose = False):
        #Принимает прямоугольную область в мировых координатах, возвращает все примитивы, попадающие в нее
        self.activIDs = set()
        self.activSectors = []
        for i, j in enumerate(rect):
            if j < 0:
                rect[i] = 0
        if rect[0] > self.drawing_w:
            rect[0] = self.drawing_w
        if rect[2] > self.drawing_w:
            rect[2] = self.drawing_w
        if rect[1] > self.drawing_h:
            rect[1] = self.drawing_h
        if rect[3] > self.drawing_h:
            rect[3] = self.drawing_h
             
        
                
        
        r1 = (int(rect[0]//self.q_scale),
              int(rect[1]//self.q_scale),
              int(rect[2]//self.q_scale),
              int(rect[3]//self.q_scale))

        x_sect_list = [x_pos for x_pos in xrange(r1[0], r1[2]+1)]
        y_sect_list = [y_pos for y_pos in xrange(r1[1], r1[3]+1)]
        for x_sector in x_sect_list:
            for y_sector in y_sect_list:
                sector = (str(x_sector) + ' ' + str(y_sector))
                try:
                    self.activIDs.update(self.sectors[sector])
                except KeyError:
                    break
                else:
                    self.activSectors.append(sector)
        
        if enclose:
            clip_func = clip.enclosing
        else:
            clip_func = clip.simple
        objects = clip_func(
                        rect[0],
                        rect[1],
                        rect[2],
                        rect[3],
                        self.activIDs,
                        self.ALLOBJECT,
                        )               
        return objects
    
    def draw_rect(self, x, y):
        #Цвет зависит от координаты x
        if self.rectx < x:
            color = self.right_color
        else:
            color = self.left_color
        self.rect_data = [self.rectx, self.recty, self.rectx, y,
                          self.rectx, self.recty, x, self.recty,
                          x, self.recty, x, y,
                          self.rectx, y, x, y]
        self.rect_color = color*(len(self.rect_data)//2)
        
    def motion(self, e):
        motion_event.motion(self, e)
    
    def left_mouse_event(self, e):
        left_mouse_event.left_mouse_event(self)

    def move_on(self, e):        
        self.motion_flag = True
        self.mouse_x = e.GetX()
        self.mouse_y = e.GetY()
        e.Skip()

    def move_off(self, e):
        self.motion_flag = False
        e.Skip()
        
    def key(self, e):
        key =  e.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.kill()
        elif not self.resFlag:
            try:
                chr_key = chr(key)
            except:
                return
            if key == wx.WXK_DELETE and self.collection:
                t1 = t.time()
                self.delete_objects(self.collection, add_history = True)
                self.change_pointdata()
                t2 = t.time()
                print 'delete ', len(self.collection), ' objects', t2-t1, 'sec'
                self.collection = []
                self.kill()
            
            elif e.ControlDown() and chr_key in self.interface.hot_keys_dict:
                self.action(self.interface.hot_keys_dict[chr_key])
                self.focus_cmd()
                
        if key == wx.WXK_RETURN:
            if self.resFlag:
                self.kill()
            else:
                self.old_func[0](self.old_func[1])
            
        #e.Skip()

    def kill(self, event=None):#Возвращает все в исходное состояние
        print 'kill'
        self.rect = False
        self.trace_on = False
        if 'trace' in self.ALLOBJECT:
            self.delete_objects(['trace',], False)
            self.change_pointdata()
        self.curent_class = None
        self.resFlag = False
        self.print_flag = False
        self.current_flag = True
        self.current_select_flag = True
        self.snap_flag = True

        self.first = True 

        self.standart_binds()
        self.standart_state()
        self.collection_data = []
        self.collection_color = []
        self.gl_wrap.c_collection_VBO()
        self.collectionBack = self.collection
        self.collection = []

        #self.cmd.Clear()
        self.cmd.ChangeValue('')
        self.info2.SetValue('')
        self.info.SetValue('Command:')
        self.update_prop()

        self.c.Refresh()
    
    
    
           
app = wx.App()
graf = Graphics()

graf.initial()
app.MainLoop()

