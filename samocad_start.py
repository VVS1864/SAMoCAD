# -*- coding: utf-8 -*-
from __future__ import division

import src.clip as clip
import src.line as line
import src.gui  as gui

import src.sectors_alg as sectors_alg

import src.grab_object as grab_object
import src.select_clone as select_clone
import src.motion_event as motion_event

import time as t
import wx
from random import random, randint, uniform
import copy
import os

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.ARB.vertex_buffer_object import *      
    
class Graphics:
    def __init__(self):
       
        self.init = False
        self.scale_size = 1.5
        self.vbo = None
        self.color_vbo = None

        self.vbo_col = None
        self.color_vbo_col = None

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
        self.select_color = [0, 255, 0] #Цвет выделяемых объектов
        self.priv_color = [0, 255, 255] #Цвет привязки
        self.back_color = 'black'
        self.left_color = [0, 255, 255]#'light blue'
        self.right_color = [255, 0, 0]#'red'
        self.text_size = 500 #Текущий размер шрифта текста (5 мм)
        self.dim_text_size = 350 #Текущий размер шрифта размеров (3.5 мм)
        self.size_simbol_p = 20 #Размер значка привязки
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
        self.auto_save_step = 30 #Количество действий между автосохранениями
        self.max_clone = 5000

        self.total_N = 0 #тотальное количество нарисованных объектов (для ID)

        #Типы линий
        self.stipples_list = [
            '_____________',
            '_ _ _ _ _ _ _',
            '____ _ ____ _',
            '____ _ _ ____',
            ]
        self.stipples_values = [
            None,
            (1,1),
            (4,1,1,1),
            (4,1,1,1,1,1),
            ]
        
        self.stipples = dict((i, self.stipples_values[ind]) for ind, i in enumerate(self.stipples_list))       
            
            
        #Толщины линий
        self.widthes = [
            "1",
            "2",
            "3",
            "4",
            ]
        
        self.old_func = (self.action, line.Line)
        self.prog_version = 'Samocad - v0.0.9.0'
        self.old_text = self.prog_version
        self.old_offset = 0
        self.old_fillet_R = 0
        self.old_scale = 1
        self.old_print_scale = 100.0
        
        self.motion_flag = False #True - Если нажата ср. кн. мыши
        self.current_flag = True #True - если можно подсвечивать текущий объект под курсором
        self.trace_flag = True
        self.trace_obj_flag = False
        self.snap_flag = True

        self.ortoFlag=False #Если True - значит орто вкл
        self.trace_on = False
        self.trace_obj_on = False
        #self.tracingFlag = True
        #self.tracing_obj_Flag = True
        self.snap_near = True
        #self.lappingFlag = False #Если True - значит активен квадрат выделения
        self.resFlag = False #Если True - значит рисуем объекты
        #self.anchorFlag = False #Если True - режим выбора привязки текста
        self.saveFlag = False
        self.changeFlag = False
        
        self.current_print_file = os.path.join(os.getcwd(), 'print_1')
        self.current_file = 'New draft'
        
        self.s_dxf = False
        self.curent_class = None
        #self.unpriv = False
        
        self.rect = False #True если рисуется рамка выделения
        self.print_flag = False #True если выбор области печати
        self.print_rect = [] #Область печати
        
        self.snap = None #None если нет захвата привязки
        self.current_select = False #True если объект под курсором можно выбрать
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
        self.history_undo = [] #Список событий

        self.drawing_rect_data = [
            0.0, 0.0, 10000.0, 0.0,
            0.0, 0.0, 0.0, 10000.0,
            10000.0, 10000.0, 10000.0, 0.0,
            10000.0, 10000.0, 0.0, 10000.0
                                  ]
        self.drawing_rect_color = [255, 255, 255]*(len(self.drawing_rect_data)//2)
        self.pointdata = []
        self.colordata = []
        

        self.collection_data = []
        self.collection_color = []
        self.standart_state()
        
        self.activIDs = set() #Массив активных ID (которые в активных секторах)
        self.activSectors = [] #Активные сектора
        self.IDs = []
        self.q_scale = 200
        self.sectors = {}
        
        self.trace_x1 = 0
        self.trace_y1 = 0
        self.trace_x2 = 0
        self.trace_y2 = 0
        

        self.interface = gui.Window(None, self.current_file + ' - '+ self.prog_version, self)
        self.c = self.interface.canvas
        self.info = self.interface.info
        self.info2 = self.interface.info2
        self.cmd = self.interface.cmd
        self.cmd.SetFocus()
        
        
    def initial(self):
        wx.EVT_PAINT(self.c, self.OnDraw) 
        wx.EVT_SIZE(self.c, self.OnSize)
        #self.interface.Bind(wx.EVT_CLOSE, self.destroy)
        self.interface.cmd.Bind(wx.EVT_KEY_DOWN, self.key, self.interface.cmd)
        self.interface.cmd.Bind(wx.EVT_KILL_FOCUS, self.focus_cmd, self.interface.cmd)
        #wx.EVT_KEY_DOWN(self.c, self.key)
        #События мыши
        self.standart_binds()
        self.c.Bind(wx.EVT_MIDDLE_DOWN, self.move_on)
        #self.c.Bind(wx.EVT_LEFT_DOWN, self.left_mouse_event)
        self.c.Bind(wx.EVT_RIGHT_DOWN, self.right_mouse_event)
        #self.c.Bind(wx.EVT_MOTION, self.motion)
        self.c.Bind(wx.EVT_MIDDLE_UP, self.move_off)
        self.c.Bind(wx.EVT_MOUSEWHEEL, self.zoom)
        
        t1 = t.time()
        #Разбивка поля на сектора
        for i in xrange(10000//self.q_scale):
            for j in xrange(10000//self.q_scale):
                c = str(i) +' '+ str(j)
                self.sectors[c] = []
        print 'Create sectors', t.time() - t1
        t1 = t.time()
        
        for i in xrange(800): #Количество вершин
            x1,y1 = uniform(0.0, 1000.0), uniform(0.0, 1000.0)
            x2,y2 = uniform(0.0, 1000.0), uniform(0.0, 1000.0)
            line.c_line(
                graf, x1, y1, x2, y2,
                width = self.width,
                layer = self.layer,
                color = self.color,
                stipple = None,
                factor_stipple = None,
                #stipple = (1,1),
                #factor_stipple = 10,
                in_mass = True,
                        )
        
        line.c_line(
            graf, 50, 50, 50, 300,
            width = self.width,
            layer = self.layer,
            color = self.color,
            stipple = None,
            factor_stipple = None,
            in_mass = True,
                    )
        line.c_line(
            graf, 50, 50, 500, 50,
            width = self.width,
            layer = self.layer,
            color = self.color,
            stipple = None,
            factor_stipple = None,
            in_mass = True,
                    )
        
        
            
        self.ALLOBJECT, self.sectors = sectors_alg.quadric_mass(self.ALLOBJECT, self.ALLOBJECT.keys(), self.sectors, self.q_scale)
    
        #Список индексов ID
        self.inds_vals = dict((y,x) for x,y in enumerate(self.IDs))
        
        print 'Create lines', t.time() - t1
        self.interface.Show(True)

    def focus_cmd(self, e):
        self.cmd.SetFocus()

    def standart_binds(self):
        self.c.Unbind(wx.EVT_LEFT_DOWN)
        self.c.Unbind(wx.EVT_MOTION)
        self.c.Bind(wx.EVT_LEFT_DOWN, self.left_mouse_event)
        self.c.Bind(wx.EVT_MOTION, self.motion)


    def standart_state(self):
        self.clone_data = []
        self.clone_color = []
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

    def amount_of_select(self):
        amount = len(self.collection)
        if amount:            
            self.info2.SetValue(('Selected %s objects. Enter - stop')%(amount))
        else:
            self.info2.SetValue((''))

    def change_pointdata(self):
        self.inds_vals = dict((y,x) for x,y in enumerate(self.IDs))
        self.vbo, self.color_vbo = self.c_VBO(self.pointdata, self.colordata)

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

    
        

    def get_world_coords(self, e):
        x = e.GetX()
        y = e.GetY()
        size = glGetIntegerv(GL_VIEWPORT)  
        xy = gluUnProject(x, size[3]-y, 0)

        return xy[0], xy[1]
        

    def zoom(self, e):
        w = e.GetWheelRotation()
        x, y = self.get_world_coords(e)
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
        '''
            def BC(i):
                if i in self.ALLOBJECT:#Если объект есть в обхем списке (не был удален)
                    self.collection.append(i)#Добавить в коллекцию
                    
            map(BC, self.collectionBack)#Перебрать старую коллекцию
        '''
            #select_clone.Select_clone(self.collection, graf)
            #self.colObj()#Посчитать колличество выделенных объектов
            #draft_gui.gui.update_prop()

    def delete_objects(self, objects, add_history = False):
        #Уделение объектов
        if add_history:
            pass
        else:
            begin_list, end_list = self.get_indexes(objects)
            all_indexes = set()
            for i, o in enumerate(objects):
                all_indexes.update(xrange(begin_list[i], end_list[i]))
                for s in self.ALLOBJECT[o]['sectors']:
                    self.sectors[s].remove(o)
                del self.ALLOBJECT[o]
            
            self.colordata = [x for i, x in enumerate(self.colordata) if i*2//3 not in all_indexes]
            self.pointdata = [x for i, x in enumerate(self.pointdata) if i not in all_indexes]
            self.IDs = [x for i, x in enumerate(self.IDs) if i*4 not in all_indexes]
        
        '''
        def dele(i, h = None):#Удаляет пришедший объект с канваса и из ALLOBJECT
            if h:
                e = self.ALLOBJECT[i]['class'].get_conf()#self.get_conf(i)
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
        print ('delete', t2-t1)
        '''
    def mass_collector(self, objects, select):
        a = set(self.collection)
        b = set(objects)
        if select == 'select':
            a.update(b)
        else:
            a.difference_update(b)

        self.collection = list(a)
        self.collection_data, self.collection_color = select_clone.select_clone(
                                                            graf,
                                                            self.collection,
                                                            self.select_color,
                                                            )
        self.c_collection_VBO()

    def get_indexes(self, objects):
        begin_list = []
        end_list = []
        
        for e in objects:
            i = self.inds_vals[e]
            begin_index = i*4
            
            lines = self.ALLOBJECT[e]['lines']
            end_index = begin_index + len(lines)*4
            
            begin_list.append(begin_index)
            end_list.append(end_index)
            
        return begin_list, end_list

    def get_current_objects(self, rect, enclose = False):
        #Принимает прямоугольную область в мировых координатах, возвращает все примитивы, попадающие в нее
        self.activIDs = set()
        self.activSectors = []
        
        
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

    def right_mouse_event(self, e):
        state = wx.GetMouseState()
        if state.ControlDown():
            self.back_collection()

    def left_mouse_event(self, e):
        x, y = self.get_world_coords(e)
        state = wx.GetMouseState()
        #print self.resFlag
        if self.resFlag:
            pass
        else:
            #добавить - убрать из коллекции
            if state.ShiftDown():
                select = 'deselect'
            else:
                select = 'select'
            if self.rect:
                self.rectx2 = x
                self.recty2 = y
                objects = grab_object.select(self, [self.rectx, self.recty, self.rectx2, self.recty2])
                self.mass_collector(objects, select)
                self.amount_of_select()
                self.rect = False
                self.rect_data = []
                self.rect_color = []
                self.c.Refresh()
                
            elif self.current_select:
                self.mass_collector([self.current,], select = select)
                self.c.Refresh()
                
            elif not self.current_change:
                #Если объект под курсором нельзя изменить
                self.rect = True
                self.rectx = x
                self.recty = y
        self.standart_state()
        e.Skip()

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
        elif key == wx.WXK_DELETE and self.collection and not self.resFlag:
            t1 = t.time()
            self.delete_objects(self.collection)
            self.change_pointdata()
            t2 = t.time()
            print 'delete ', len(self.collection), ' objects', t2-t1, 'sec'
            self.collection = []
            self.kill()
        elif key == wx.WXK_RETURN:
            if self.resFlag:
                self.kill()
            else:
                self.old_func[0](self.old_func[1])
            
        e.Skip()

    def kill(self, event=None):#Возвращает все в исходное состояние
        
        print 'kill'
        self.rect = False
        self.trace_on = False
        if 'trace' in self.ALLOBJECT:
            self.ALLOBJECT, self.sectors = sectors_alg.delete(self.ALLOBJECT, self.sectors, ['trace',])
            
        self.curent_class = None
        self.resFlag = False
        self.print_flag = False
        self.current_flag = True

        self.standart_binds()
        self.standart_state()
        self.collection_data = []
        self.collection_color = []
        self.c_collection_VBO()
        self.collectionBack = self.collection
        self.collection = []

        self.info2.SetValue('')
        self.info.SetValue('Command:')
        self.c.Refresh()
        '''
        if self.rect:
            self.c.delete(self.rect)
            self.rect = None
        if self.col:
            self.c.delete('C'+self.col)
            self.col = None
        if self.curent_class:
            del self.curent_class
            self.curent_class = None
        ##t=self.c.find_withtag('c1')
        if t:
            self.c.delete('c1')
        if 'trace' in self.ALLOBJECT:
            self.c.delete('trace')
            del self.ALLOBJECT['trace']
        if 'trace_o' in self.ALLOBJECT:
            self.c.delete('trace_o')
            del self.ALLOBJECT['trace_o']
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
        self.dialog.config(text = 'Command:')
        self.info.config(text = '')
        self.resFlag = False
        self.lappingFlag = False
        self.anchorFlag = False
        self.trace_on = False
        self.trace_obj_on = False
        self.command.delete(0,END)
        self.com = None
        self.sbros()
        self.func_collection = []
        self.temp_collection = []
        ##self.c.config(cursor = 'crosshair')
        draft_gui.gui.update_prop()
        '''

    def draw_VBO(self):
        if self.GL_version == '3':
            glBindBuffer( GL_ARRAY_BUFFER, self.color_vbo)
            # Указываем, где взять массив цветов:
            # Параметры аналогичны, но указывается массив цветов
            glColorPointer(3, GL_UNSIGNED_BYTE, 0, None)
            
            glBindBuffer( GL_ARRAY_BUFFER, self.vbo )       # Активирует VBO
            # Указываем, где взять массив верши:
            # Первый параметр - сколько используется координат на одну вершину
            # Второй параметр - определяем тип данных для каждой координаты вершины
            # Третий парметр - определяет смещение между вершинами в массиве
            # Если вершины идут одна за другой, то смещение 0
            # Четвертый параметр - указатель на первую координату первой вершины в массиве
            glVertexPointer(2, GL_FLOAT, 0, None) # None - потому что VBO активирован
            
            # Рисуем данные массивов за один проход:
            # Первый параметр - какой тип примитивов использовать (треугольники, точки, линии и др.)
            # Второй параметр - начальный индекс в указанных массивах
            # Третий параметр - количество рисуемых объектов (в нашем случае это 2 вершины - 4 координаты)
            glDrawArrays(GL_LINES, 0, len(self.pointdata)//2)
            
            
            if self.collection_data:
                #glBindBuffer( GL_ARRAY_BUFFER, 0)
                glBindBuffer( GL_ARRAY_BUFFER, self.color_vbo_col)
                glColorPointer(3, GL_UNSIGNED_BYTE, 0, None)
            
                glBindBuffer( GL_ARRAY_BUFFER, self.vbo_col )       
                glVertexPointer(2, GL_FLOAT, 0, None) 
            
                glDrawArrays(GL_LINES, 0, len(self.collection_data)//2)
            glBindBuffer( GL_ARRAY_BUFFER, 0)

        else:
            glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.color_vbo)
            # Указываем, где взять массив цветов:
            # Параметры аналогичны, но указывается массив цветов
            glColorPointer(3, GL_UNSIGNED_BYTE, 0, None)
            
            glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.vbo )       # Активирует VBO
            # Указываем, где взять массив верши:
            # Первый параметр - сколько используется координат на одну вершину
            # Второй параметр - определяем тип данных для каждой координаты вершины
            # Третий парметр - определяет смещение между вершинами в массиве
            # Если вершины идут одна за другой, то смещение 0
            # Четвертый параметр - указатель на первую координату первой вершины в массиве
            glVertexPointer(2, GL_FLOAT, 0, None) # None - потому что VBO активирован
            
            # Рисуем данные массивов за один проход:
            # Первый параметр - какой тип примитивов использовать (треугольники, точки, линии и др.)
            # Второй параметр - начальный индекс в указанных массивах
            # Третий параметр - количество рисуемых объектов (в нашем случае это 2 вершины - 4 координаты)
            glDrawArrays(GL_LINES, 0, len(self.pointdata)//2)
            
            
            if self.collection_data:
                #glBindBuffer( GL_ARRAY_BUFFER, 0)
                glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.color_vbo_col)
                glColorPointer(3, GL_UNSIGNED_BYTE, 0, None)
            
                glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.vbo_col )       
                glVertexPointer(2, GL_FLOAT, 0, None) 
            
                glDrawArrays(GL_LINES, 0, len(self.collection_data)//2)
            glBindBufferARB( GL_ARRAY_BUFFER_ARB, 0)

    def draw_array(self):
        #glBindBuffer( GL_ARRAY_BUFFER, self.color_vbo)
        # Указываем, где взять массив цветов:
        # Параметры аналогичны, но указывается массив цветов
        glColorPointer(3, GL_UNSIGNED_BYTE, 0, self.colordata)
        
        #glBindBuffer( GL_ARRAY_BUFFER, self.vbo )       # Активирует VBO
        # Указываем, где взять массив верши:
        # Первый параметр - сколько используется координат на одну вершину
        # Второй параметр - определяем тип данных для каждой координаты вершины
        # Третий парметр - определяет смещение между вершинами в массиве
        # Если вершины идут одна за другой, то смещение 0
        # Четвертый параметр - указатель на первую координату первой вершины в массиве
        glVertexPointer(2, GL_FLOAT, 0, self.pointdata) # None - потому что VBO активирован
        
        # Рисуем данные массивов за один проход:
        # Первый параметр - какой тип примитивов использовать (треугольники, точки, линии и др.)
        # Второй параметр - начальный индекс в указанных массивах
        # Третий параметр - количество рисуемых объектов (в нашем случае это 2 вершины - 4 координаты)
        glDrawArrays(GL_LINES, 0, len(self.pointdata)//2)
        
        
        if self.collection_data:
            #glBindBuffer( GL_ARRAY_BUFFER, 0)
            #glBindBuffer( GL_ARRAY_BUFFER, self.color_vbo_col)
            glColorPointer(3, GL_UNSIGNED_BYTE, 0, self.collection_color)
        
            #glBindBuffer( GL_ARRAY_BUFFER, self.vbo_col )       
            glVertexPointer(2, GL_FLOAT, 0, self.collection_data) 
        
            glDrawArrays(GL_LINES, 0, len(self.collection_data)//2)

    def OnDraw(self,event):
        
        self.c.SetCurrent()
        if not self.init:
            self.InitGL()
            self.init = True
        
        
        glClear(GL_COLOR_BUFFER_BIT)                    # Очищаем экран и заливаем серым цветом
        
        glEnableClientState(GL_VERTEX_ARRAY)            # Включаем использование массива вершин
        glEnableClientState(GL_COLOR_ARRAY)             # Включаем использование массива цветов

        self.draw()
        
        tempdata = (
            self.current_data +
            self.snap_data +
            self.drawing_rect_data
            )
        tempcolor = (
            self.current_color +
            self.snap_color +
            self.drawing_rect_color
            )
        w_tempdata = (
            self.trace_data +
            self.rect_data +
            self.dynamic_data
            )
        w_tempcolor = (
            self.trace_color +
            self.rect_color +
            self.dynamic_color
            )
       
        if tempdata or w_tempdata:
            
            glLineWidth(3)
            glColorPointer(3, GL_UNSIGNED_BYTE, 0, tempcolor)
            glVertexPointer(2, GL_FLOAT, 0, tempdata)
            glDrawArrays(GL_LINES, 0, len(tempdata)//2)
            glLineWidth(1)
            #glBindBuffer( GL_ARRAY_BUFFER, 0)
            glColorPointer(3, GL_UNSIGNED_BYTE, 0, w_tempcolor)
            glVertexPointer(2, GL_FLOAT, 0, w_tempdata)
            glDrawArrays(GL_LINES, 0, len(w_tempdata)//2)
            
        glDisableClientState(GL_VERTEX_ARRAY)           # Отключаем использование массива вершин
        glDisableClientState(GL_COLOR_ARRAY)            # Отключаем использование массива цветов
        #glutSwapBuffers() Не работает                  # Выводим все нарисованное в памяти на экран

        glFinish()
            
    def InitGL(self): # Стандартная инициализация матриц
        glClearColor(0, 0, 0, 0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #glOrtho(0,1000,0,1000,-100,100)
        size = glGetIntegerv(GL_VIEWPORT)
        glViewport(0, 0, size[2], size[3])
        #Заново задать проекционную матрицу
        glOrtho(0,size[2],0,size[3],-100,100)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, 100.0)
        ver = glGetString(GL_VERSION)
        ver = float(ver[:3])
        print 'OpenGL version', ver
        if ver > 2:
            self.GL_version = '3'
        else:
            self.GL_version = '1'

        self.draw = self.draw_VBO
            
        if self.GL_version == '3':
            vertex = create_shader(GL_VERTEX_SHADER, """
            varying vec4 vertex_color;
                        void main(){
                            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                            vertex_color = gl_Color;
                        }""")
            # Создаем фрагментный шейдер:
            # Определяет цвет каждого фрагмента как "смешанный" цвет его вершин
            fragment = create_shader(GL_FRAGMENT_SHADER, """
            varying vec4 vertex_color;
                        void main() {
                            gl_FragColor = vertex_color;
            }""")
            # Создаем пустой объект шейдерной программы
            program = glCreateProgram()
            # Приcоединяем вершинный шейдер к программе
            glAttachShader(program, vertex)
            # Присоединяем фрагментный шейдер к программе
            glAttachShader(program, fragment)
            # "Собираем" шейдерную программу
            glLinkProgram(program)
            # Сообщаем OpenGL о необходимости использовать данную шейдерну программу при отрисовке объектов
            glUseProgram(program)
            
            #self.c_VBO()
        #else:
        self.vbo, self.color_vbo = self.c_VBO(self.pointdata, self.colordata)
            #from OpenGL.GL.ARB.vertex_buffer_object import *

    def destroy(self, event):
        if self.vbo: # Если уже есть - удалить
            glDeleteBuffers(1, [self.vbo])
            glDeleteBuffers(1, [self.color_vbo])
        self.interface.Destroy()

    def c_collection_VBO(self):
        if self.GL_version == '3':
            #if self.vbo_col: # Если уже есть - удалить
                #glDeleteBuffers(1, [self.vbo_col])
                #glDeleteBuffers(1, [self.color_vbo_col])

            ### Стандартная процедура создания VBO ###
            self.vbo_col = glGenBuffers(1)
            glBindBuffer (GL_ARRAY_BUFFER, self.vbo_col)
            # 2 Параметр - указатель на массив pointdata
            glBufferData (GL_ARRAY_BUFFER, (GLfloat*len(self.collection_data))(*self.collection_data), GL_STATIC_DRAW)
            glBindBuffer (GL_ARRAY_BUFFER, 0)
            
            self.color_vbo_col = glGenBuffers(1)
            glBindBuffer (GL_ARRAY_BUFFER, self.color_vbo_col)
            # 2 Параметр - указатель на массив colordata
            glBufferData (GL_ARRAY_BUFFER, (GLubyte*len(self.collection_color))(*self.collection_color), GL_STATIC_DRAW)
            glBindBuffer (GL_ARRAY_BUFFER, 0)

        else:
            #if self.vbo_col: # Если уже есть - удалить
                #glDeleteBuffers(1, [self.vbo_col])
                #glDeleteBuffers(1, [self.color_vbo_col])

            ### Стандартная процедура создания VBO ###
            self.vbo_col = glGenBuffersARB(1)
            glBindBufferARB (GL_ARRAY_BUFFER_ARB, self.vbo_col)
            # 2 Параметр - указатель на массив pointdata
            glBufferDataARB (GL_ARRAY_BUFFER_ARB, (GLfloat*len(self.collection_data))(*self.collection_data), GL_STATIC_DRAW_ARB)
            glBindBufferARB (GL_ARRAY_BUFFER_ARB, 0)
            
            self.color_vbo_col = glGenBuffersARB(1)
            glBindBufferARB (GL_ARRAY_BUFFER_ARB, self.color_vbo_col)
            # 2 Параметр - указатель на массив colordata
            glBufferDataARB (GL_ARRAY_BUFFER_ARB, (GLubyte*len(self.collection_color))(*self.collection_color), GL_STATIC_DRAW_ARB)
            glBindBufferARB (GL_ARRAY_BUFFER_ARB, 0)
        
    def c_VBO(self, pointdata, colordata):
        if self.GL_version == '3':
            #self.vbo_data = self.pointdata + self.collection_data
            #self.vbo_color = self.colordata + self.collection_color
            #if self.vbo: # Если уже есть - удалить
                #glDeleteBuffers(1, [self.vbo])
                #glDeleteBuffers(1, [self.color_vbo])
            
            ### Стандартная процедура создания VBO ###
            vbo = glGenBuffersARB(1)
            glBindBuffer (GL_ARRAY_BUFFER, vbo)
            # 2 Параметр - указатель на массив pointdata
            
            glBufferData (GL_ARRAY_BUFFER, (GLfloat*len(pointdata))(*pointdata), GL_STATIC_DRAW)
            glBindBuffer (GL_ARRAY_BUFFER, 0)
            
            color_vbo = glGenBuffersARB(1)
            glBindBuffer (GL_ARRAY_BUFFER, color_vbo)
            # 2 Параметр - указатель на массив colordata
            glBufferData (GL_ARRAY_BUFFER, (GLubyte*len(colordata))(*colordata), GL_STATIC_DRAW)
            glBindBuffer (GL_ARRAY_BUFFER, 0)

        else:
            #self.vbo_data = self.pointdata + self.collection_data
            #self.vbo_color = self.colordata + self.collection_color
            #if self.vbo: # Если уже есть - удалить
                #glDeleteBuffers(1, [self.vbo])
                #glDeleteBuffers(1, [self.color_vbo])
            
            ### Стандартная процедура создания VBO ###
            vbo = glGenBuffersARB(1)
            glBindBufferARB (GL_ARRAY_BUFFER_ARB, vbo)
            # 2 Параметр - указатель на массив pointdata
            
            glBufferDataARB (GL_ARRAY_BUFFER_ARB, (GLfloat*len(pointdata))(*pointdata), GL_STATIC_DRAW_ARB)
            glBindBufferARB (GL_ARRAY_BUFFER_ARB, 0)
            
            color_vbo = glGenBuffersARB(1)
            glBindBufferARB (GL_ARRAY_BUFFER_ARB, color_vbo)
            # 2 Параметр - указатель на массив colordata
            glBufferDataARB (GL_ARRAY_BUFFER_ARB, (GLubyte*len(colordata))(*colordata), GL_STATIC_DRAW_ARB)
            glBindBufferARB (GL_ARRAY_BUFFER_ARB, 0)

        return vbo, color_vbo
        
    def OnSize(self, event): # Перисовывает окно при ресайзе
        #Получить новый размер окна
        try:
            width, height = event.GetSize()
        except:
            width = event.GetSize().width
            height = event.GetSize().height
        #Запомнить модельную матрицу (все перемещения и зуммы)
        glPushMatrix()
        #Установить текущей проекционную матрицу
        glMatrixMode(GL_PROJECTION)
        #Отчистить ее
        glLoadIdentity()
        #Задать новую область просмотра
        glViewport(0, 0, width, height)
        #Заново задать проекционную матрицу
        glOrtho(0,width,0,height,-100,100)
        #Сделать текущей модельную матрицу
        glMatrixMode(GL_MODELVIEW)
        #Вернуть все перемещения и зуммы
        glPopMatrix()
        #Перерисовать
        self.c.Refresh()
        #self.c.Update()


# Процедура подготовки шейдера (тип шейдера, текст шейдера)
def create_shader(shader_type, source):
    # Создаем пустой объект шейдера
    shader = glCreateShader(shader_type)
    # Привязываем текст шейдера к пустому объекту шейдера
    glShaderSource(shader, source)
    # Компилируем шейдер
    glCompileShader(shader)
    # Возвращаем созданный шейдер
    return shader
            


app = wx.App()
graf = Graphics()

graf.initial()
app.MainLoop()

