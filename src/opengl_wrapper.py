# -*- coding: utf-8 -*-
import numpy
import ctypes
import time as t
import array

from OpenGL.GL import *


class GL_wrapper:
    def __init__(self, par):
        self.par = par

    def InitGL(self):
        ver = glGetString(GL_VERSION)
        ver = float(ver[:3])
        print 'OpenGL version', ver
        if ver > 2:
            self.par.GL_version = '3'
        else:
            self.par.GL_version = '1'
            use_ARB()
            
        if self.par.GL_version in ('3', '1'):
            vsh = """
            varying vec4 vertex_color;
                        void main(){
                            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                            vertex_color = gl_Color;
                        }"""
            
            vertex = create_shader(GL_VERTEX_SHADER, vsh)
            # Создаем фрагментный шейдер:
            fsh = """
            varying vec4 vertex_color;
                        void main() {
                            gl_FragColor = vertex_color;
            }"""
            
            fragment = create_shader(GL_FRAGMENT_SHADER, fsh)

            
            # Создаем пустой объект шейдерной программы
            self.program = glCreateProgram()
            
            # Приcоединяем вершинный шейдер к программе
            glAttachShader(self.program, vertex)
            # Присоединяем фрагментный шейдер к программе
            glAttachShader(self.program, fragment)
            # "Собираем" шейдерную программу
            glLinkProgram(self.program)
            # Сообщаем OpenGL о необходимости использовать данную шейдерну программу при отрисовке объектов
            glUseProgram(self.program)
            
            #self.par.Matrix_proj_ID = glGetUniformLocation(self.program, "projection")
            #self.par.Matrix_mvp_ID = glGetUniformLocation(self.program, "mvp")
            # Стандартная инициализация матриц
            print 'starn init GL...'
            glClearColor(0, 0, 0, 0)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            
            size = glGetIntegerv(GL_VIEWPORT)
            #self.ortho(0.0, float(size[2]), 0.0, float(size[3]),-100.0,100.0)
            glViewport(0, 0, size[2], size[3])
            
            #Заново задать проекционную матрицу
            glOrtho(0,size[2],0,size[3],-100,100)
            
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glTranslatef(0.0, 0.0, 100.0)
             
        print 'end init GL'
        
        print 'start init VBO...'
        self.par.change_pointdata()
        print 'end init VBO'

    def OnDraw(self, event):
        self.par.c.SetCurrent(self.par.c.context)
        if not self.par.c.init:
            self.InitGL()
            self.par.c.init = True
        
        
        glClear(GL_COLOR_BUFFER_BIT)                    # Очищаем экран и заливаем серым цветом
        
        glEnableClientState(GL_VERTEX_ARRAY)            # Включаем использование массива вершин
        glEnableClientState(GL_COLOR_ARRAY)             # Включаем использование массива цветов

        self.draw_VBO()
        if not self.par.first:
            self.draw_dinamic_vbo()
        
        
        tempdata = (
            self.par.current_data +
            self.par.snap_data +
            self.par.drawing_rect_data +
            self.par.red_line_data
            )
        tempcolor = (
            self.par.current_color +
            self.par.snap_color +
            self.par.drawing_rect_color +
            self.par.red_line_color
            )          
             
        w_tempdata = (
            self.par.trace_data +
            self.par.rect_data +
            self.par.dynamic_data
            )
        w_tempcolor = (
            self.par.trace_color +
            self.par.rect_color +
            self.par.dynamic_color
            )
       
        if tempdata or w_tempdata:
            c_tempdata = numpy.array(tempdata, dtype = numpy.float32)
            c_tempcolor = numpy.array(tempcolor, dtype = numpy.ubyte)
            c_w_tempdata = numpy.array(w_tempdata, dtype = numpy.float32)
            c_w_tempcolor = numpy.array(w_tempcolor, dtype = numpy.ubyte)

            glLineWidth(3)
            glColorPointer(3, GL_UNSIGNED_BYTE, 0, c_tempcolor)
            glVertexPointer(2, GL_FLOAT, 0, c_tempdata)
            glDrawArrays(GL_LINES, 0, len(tempdata)//2)
            glLineWidth(1)
            glColorPointer(3, GL_UNSIGNED_BYTE, 0, c_w_tempcolor)
            glVertexPointer(2, GL_FLOAT, 0, c_w_tempdata)
            glDrawArrays(GL_LINES, 0, len(w_tempdata)//2)
            
        glDisableClientState(GL_VERTEX_ARRAY)           # Отключаем использование массива вершин
        glDisableClientState(GL_COLOR_ARRAY)            # Отключаем использование массива цветов
        # Выводим все нарисованное в памяти на экран
        self.par.c.SwapBuffers()

    def ortho(self, l, r, b, t, n_v, f_v):
        tx = -(r+l)/(r-l)
        ty = -(t+b)/(t-b)
        tz = -(f_v+n_v)/(f_v-n_v)
        orthoMatrix = numpy.matrix(
            [[2/(r-l), 0.0,     0.0,          tx], 
             [0.0,     2/(t-b), 0.0,          ty], 
             [0.0,     0.0,     -2/(f_v-n_v), tz], 
             [0.0,     0.0,     0.0,          1.0]], numpy.float32)
        
        self.par.projMatrix = self.par.projMatrix.dot(orthoMatrix)
        #self.par.MVP = self.par.projMatrix.dot(self.par.mvMatrix)
        
        glUseProgram(self.program)
        glUniformMatrix4fv(self.par.Matrix_proj_ID, 1, GL_TRUE, self.par.projMatrix)
        glUniformMatrix4fv(self.par.Matrix_mvp_ID, 1, GL_TRUE, self.par.mvMatrix)
        #glUniformMatrix4fv(self.par.Matrix_mvp_ID, 1, GL_FALSE, self.par.MVP.flatten())

    def translate(self, x, y, z):
        translateMatrix = numpy.matrix(
            [[1.0, 0.0, 0.0, float(x)], 
             [0.0, 1.0, 0.0, float(y)], 
             [0.0, 0.0, 1.0, float(y)], 
             [0.0, 0.0, 0.0, 1.0]], numpy.float32)
        
        self.par.mvMatrix = self.par.mvMatrix.dot(translateMatrix)
        #self.par.MVP = self.par.projMatrix.dot(self.par.mvMatrix)
        
        glUseProgram(self.program)
        glUniformMatrix4fv(self.par.Matrix_proj_ID, 1, GL_TRUE, self.par.projMatrix)
        glUniformMatrix4fv(self.par.Matrix_mvp_ID, 1, GL_TRUE, self.par.mvMatrix)
        #glUniformMatrix4fv(self.par.Matrix_mvp_ID, 1, GL_FALSE, self.par.MVP.flatten())

    def OnEraseBackground(self, event):
        pass

    def draw_dinamic_vbo(self):
        glPushMatrix()
        glMultMatrixf(self.par.dynamic_matrix)
        
        glColor(255.0, 255.0, 0.0)
        glBindBuffer( GL_ARRAY_BUFFER, self.par.dynamic_vbo)
        glVertexPointer(2, GL_FLOAT, 0, None)
        glDrawArrays(GL_LINES, 0, len(self.par.dynamic_vbo_data)//2)
        glBindBuffer( GL_ARRAY_BUFFER, 0)
        
        glPopMatrix()
        
    def draw_VBO(self):
        
        for data_list in self.par.point_color_data_vbo_dict.keys():
        #print data_list
        #self.par.point_color_data_vbo_dict
            if data_list > 1:
                glLineWidth(data_list*2)
            glBindBuffer( GL_ARRAY_BUFFER, self.par.point_color_data_vbo_dict[data_list][2])
            # Указываем, где взять массив цветов:
            # Параметры аналогичны, но указывается массив цветов
            glColorPointer(3, GL_UNSIGNED_BYTE, 0, None)
            
            glBindBuffer( GL_ARRAY_BUFFER, self.par.point_color_data_vbo_dict[data_list][3])
            
            # Активирует VBO
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
            glDrawArrays(GL_LINES, 0, len(self.par.point_color_data_vbo_dict[data_list][0])//2)
            
            glBindBuffer( GL_ARRAY_BUFFER, 0)

        
        if self.par.collection_data:
            glLineWidth(5)
            glBindBuffer( GL_ARRAY_BUFFER, self.par.color_vbo_col)
            glColorPointer(3, GL_UNSIGNED_BYTE, 0, None)
        
            glBindBuffer( GL_ARRAY_BUFFER, self.par.vbo_col )       
            glVertexPointer(2, GL_FLOAT, 0, None) 
        
            glDrawArrays(GL_LINES, 0, len(self.par.collection_data)//2)
        glBindBuffer( GL_ARRAY_BUFFER, 0)
    def c_collection_VBO(self):
        c_pointdata = numpy.array(self.par.collection_data, dtype = numpy.float32)
        c_colordata = numpy.array(self.par.collection_color, dtype = numpy.ubyte)
        
        if not self.par.vbo_col:
            self.par.vbo_col = glGenBuffers(1)
            self.par.color_vbo_col = glGenBuffers(1)

        ### Стандартная процедура создания VBO ###
        glBindBuffer (GL_ARRAY_BUFFER, self.par.vbo_col)
        # 2 Параметр - указатель на массив pointdata
        glBufferData (GL_ARRAY_BUFFER, c_pointdata, GL_STATIC_DRAW)
        glBindBuffer (GL_ARRAY_BUFFER, 0)
        
        glBindBuffer (GL_ARRAY_BUFFER, self.par.color_vbo_col)
        # 2 Параметр - указатель на массив colordata
        glBufferData (GL_ARRAY_BUFFER, c_colordata, GL_STATIC_DRAW)
        glBindBuffer (GL_ARRAY_BUFFER, 0)
        

    def change_pointdata(self):        
        if not self.par.point_color_data_vbo_dict[1][2]:
            for data_list in self.par.point_color_data_vbo_dict.keys():
                vbo = glGenBuffers(1)
                color_vbo = glGenBuffers(1)
                self.par.point_color_data_vbo_dict[data_list][3] = vbo
                self.par.point_color_data_vbo_dict[data_list][2] = color_vbo
                
            '''
            self.vbo_2 = glGenBuffers(1)
            self.color_vbo_2 = glGenBuffers(1)
            
            self.vbo_3 = glGenBuffers(1)
            self.color_vbo_3 = glGenBuffers(1)
            
            self.vbo_4 = glGenBuffers(1)
            self.color_vbo_4 = glGenBuffers(1)
            '''
        
            #self.par.vbo = glGenBuffers(1)
            #self.par.color_vbo = glGenBuffers(1)
            
        else:
            pd = self.par.point_color_data_vbo_dict
            
            glDeleteBuffers(1, [pd[1][2], pd[1][3], pd[2][2], pd[2][3], pd[3][2], pd[3][3], pd[4][2], pd[4][3]])
            #if self.par.vbo: # Если VBO есть - удалить
                #glDeleteBuffers(1, [self.par.vbo, self.par.color_vbo])
        
        
        for data_list in self.par.point_color_data_vbo_dict.keys():
            
            self.c_VBO(self.par.point_color_data_vbo_dict[data_list][3], self.par.point_color_data_vbo_dict[data_list][2], self.par.point_color_data_vbo_dict[data_list][0], self.par.point_color_data_vbo_dict[data_list][1])

    def update_pointdata(self, pointdata, colordata, width = 1):
        #self.par.pointdata.extend(pointdata)
        #self.par.colordata.extend(colordata)
        self.par.point_color_data_vbo_dict[width][0].extend(pointdata)
        self.par.point_color_data_vbo_dict[width][1].extend(colordata)
        
    def c_VBO(self, vbo, color_vbo, pointdata, colordata):
        #print vbo, color_vbo, pointdata, colordata
        vbo = self.simple_c_VBO(vbo, pointdata)
        color_vbo = self.simple_c_VBO(color_vbo, colordata)

        return vbo, color_vbo

    def simple_c_VBO(self, vbo, pointdata):
        if not vbo:
            vbo = glGenBuffers(1)
        c_pointdata = pointdata.tostring()           
        glBindBuffer (GL_ARRAY_BUFFER, vbo)
        glBufferData (GL_ARRAY_BUFFER, c_pointdata, GL_STATIC_DRAW)
        glBindBuffer (GL_ARRAY_BUFFER, 0)
        return vbo

    def dinamic_vbo_on(self):
        self.par.dynamic_vbo_data = array.array('f', [])
        self.par.dynamic_vbo_data.fromlist(self.par.dynamic_data)
        self.par.dynamic_data = []
        self.par.dynamic_color = []
        self.par.dynamic_vbo = self.simple_c_VBO(
            self.par.dynamic_vbo,
            self.par.dynamic_vbo_data,
            )            
        
    def OnSize(self, event): # Перисовывает окно при ресайзе
        #Получить новый размер окна
        try:
            width, height = event.GetSize()
        except:
            width = event.GetSize().width
            height = event.GetSize().height
        #Запомнить модельную матрицу (все перемещения и зуммы)
        try:
            glPushMatrix()
        except:
            print 'Error in OnSize - GL Context not be created'
            return
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
        self.par.c.Refresh()
        #self.par.c.Update()
        event.Skip()
        
    def destroy(self, event):
        print 'destroy'
        if self.par.vbo: # Если VBO есть - удалить
            glDeleteBuffers(1, [self.par.vbo])
            glDeleteBuffers(1, [self.par.color_vbo])
        self.par.interface.Destroy()

def use_ARB():
    import OpenGL.GL.ARB.vertex_buffer_object as ARB
    
    import OpenGL.GL.ARB.shader_objects as shARB
    import OpenGL.GL.ARB.shader_objects as shARB
    import OpenGL.GL.ARB.vertex_shader as vshARB
    import OpenGL.GL.ARB.fragment_shader as fshARB
    
    global glBindBuffer, glGenBuffers, glBufferData, GL_STATIC_DRAW, GL_DYNAMIC_DRAW, GL_ARRAY_BUFFER, glDeleteBuffers
    global GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glCreateProgram, glAttachShader, glLinkProgram, glUseProgram, glCreateShader, glShaderSource, glCompileShader

    glBindBuffer = ARB.glBindBufferARB
    glGenBuffers = ARB.glGenBuffersARB
    glBufferData = ARB.glBufferDataARB
    GL_STATIC_DRAW = ARB.GL_STATIC_DRAW_ARB
    GL_DYNAMIC_DRAW = ARB.GL_DYNAMIC_DRAW_ARB
    GL_ARRAY_BUFFER = ARB.GL_ARRAY_BUFFER_ARB
    glDeleteBuffers = ARB.glDeleteBuffersARB

    GL_VERTEX_SHADER = vshARB.GL_VERTEX_SHADER_ARB
    GL_FRAGMENT_SHADER = fshARB.GL_FRAGMENT_SHADER_ARB
    glCreateProgram = shARB.glCreateProgramObjectARB
    glAttachShader = shARB.glAttachObjectARB
    glLinkProgram = shARB.glLinkProgramARB
    glUseProgram = shARB.glUseProgramObjectARB
    glCreateShader = shARB.glCreateShaderObjectARB
    glShaderSource = shARB.glShaderSourceARB
    glCompileShader = shARB.glCompileShaderARB

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
