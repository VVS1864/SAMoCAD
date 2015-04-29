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
        '''
        # Стандартная инициализация матриц
        print 'starn init GL...'
        glClearColor(0, 0, 0, 0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        size = glGetIntegerv(GL_VIEWPORT)
        glViewport(0, 0, size[2], size[3])
        
        #Заново задать проекционную матрицу
        glOrtho(0,size[2],0,size[3],-100,100)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, 100.0)
        '''
        ver = glGetString(GL_VERSION)
        ver = float(ver[:3])
        print 'OpenGL version', ver
        #ver = 1
        if ver > 2:
            self.par.GL_version = '3'
        else:
            self.par.GL_version = '1'
            use_ARB()
        
        self.par.draw = self.draw_VBO
            
        if self.par.GL_version in ('3', '1'):
            vsh = """
            //uniform mat4 projection;
            //uniform mat4 mvp;
            varying vec4 vertex_color;
            //varying vec4 gl_Vertex;
                        void main(){
                            
                            //gl_Position = projection * mvp * gl_Vertex;
                            //gl_Position = mvp * gl_Vertex;
                            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                            vertex_color = gl_Color;
                            gl_PointSize    = 8.0;
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
            '''
            self.par.projMatrix = numpy.matrix(
                [[1.0, 0.0, 0.0, 0.0], 
                [0.0, 1.0, 0.0, 0.0], 
                [0.0, 0.0, 1.0, 0.0], 
                [0.0, 0.0, 0.0, 1.0]], numpy.float32)
            
            self.par.mvMatrix = numpy.matrix(
                [[1.0, 0.0, 0.0, 0.0], 
                [0.0, 1.0, 0.0, 0.0], 
                [0.0, 0.0, 1.0, 0.0], 
                [0.0, 0.0, 0.0, 1.0]], numpy.float32)
            self.par.projMatrix.dot(self.par.mvMatrix)
            glUseProgram(self.program)
            glUniformMatrix4fv(self.par.Matrix_proj_ID, 1, GL_FALSE, self.par.projMatrix.flatten())
            glUniformMatrix4fv(self.par.Matrix_mvp_ID, 1, GL_FALSE, self.par.mvMatrix.flatten())
            '''
            size = glGetIntegerv(GL_VIEWPORT)
            #self.ortho(0.0, float(size[2]), 0.0, float(size[3]),-100.0,100.0)
            glViewport(0, 0, size[2], size[3])
            
            #Заново задать проекционную матрицу
            glOrtho(0,size[2],0,size[3],-100,100)
            
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glTranslatef(0.0, 0.0, 100.0)
            '''
            self.par.mvMatrix = numpy.array([1.0, 0.0, 0.0, 0.0, 
                                    0.0, 1.0, 0.0, 0.0, 
                                    0.0, 0.0, 1.0, 0.0, 
                                    0.0, 0.0, 0.0, 1.0], numpy.float32)
            '''

            #self.translate(0.0, 0.0, 100.0)
            
            
            '''
            translateMatrix = numpy.array([1.0, 0.0, 0.0, 0.0, 
                                    0.0, 1.0, 0.0, 0.0, 
                                    0.0, 0.0, 1.0, 100.0, 
                                    0.0, 0.0, 0.0, 1.0], numpy.float32)
                                    
            self.par.mvMatrix = self.par.mvMatrix * translateMatrix
            glUniformMatrix4fv(self.par.MatrixID, 1, GL_FALSE, self.par.mvMatrix)
        '''  
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

        self.par.draw()
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
        glBindBuffer( GL_ARRAY_BUFFER, self.par.color_vbo)
        # Указываем, где взять массив цветов:
        # Параметры аналогичны, но указывается массив цветов
        glColorPointer(3, GL_UNSIGNED_BYTE, 0, None)
        
        glBindBuffer( GL_ARRAY_BUFFER, self.par.vbo )       # Активирует VBO
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
        glDrawArrays(GL_LINES, 0, len(self.par.pointdata)//2)
        
        if self.par.collection_data:
            
            glBindBuffer( GL_ARRAY_BUFFER, self.par.color_vbo_col)
            glColorPointer(3, GL_UNSIGNED_BYTE, 0, None)
        
            glBindBuffer( GL_ARRAY_BUFFER, self.par.vbo_col )       
            glVertexPointer(2, GL_FLOAT, 0, None) 
        
            glDrawArrays(GL_LINES, 0, len(self.par.collection_data)//2)
        glBindBuffer( GL_ARRAY_BUFFER, 0)
        '''
        else:
            glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.par.color_vbo)
            # Указываем, где взять массив цветов:
            # Параметры аналогичны, но указывается массив цветов
            glColorPointer(3, GL_UNSIGNED_BYTE, 0, None)
            
            glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.par.vbo )       # Активирует VBO
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
            glDrawArrays(GL_LINES, 0, len(self.par.pointdata)//2)
            
            if self.par.collection_data:
                glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.par.color_vbo_col)
                glColorPointer(3, GL_UNSIGNED_BYTE, 0, None)
            
                glBindBufferARB( GL_ARRAY_BUFFER_ARB, self.par.vbo_col )       
                glVertexPointer(2, GL_FLOAT, 0, None) 
            
                glDrawArrays(GL_LINES, 0, len(self.par.collection_data)//2)
            glBindBufferARB( GL_ARRAY_BUFFER_ARB, 0)
        '''
    '''
    def draw_array(self):
        #glBindBuffer( GL_ARRAY_BUFFER, self.par.color_vbo)
        # Указываем, где взять массив цветов:
        # Параметры аналогичны, но указывается массив цветов
        glColorPointer(3, GL_UNSIGNED_BYTE, 0, self.par.colordata)
        
        #glBindBuffer( GL_ARRAY_BUFFER, self.par.vbo )       # Активирует VBO
        # Указываем, где взять массив верши:
        # Первый параметр - сколько используется координат на одну вершину
        # Второй параметр - определяем тип данных для каждой координаты вершины
        # Третий парметр - определяет смещение между вершинами в массиве
        # Если вершины идут одна за другой, то смещение 0
        # Четвертый параметр - указатель на первую координату первой вершины в массиве
        glVertexPointer(2, GL_FLOAT, 0, self.par.pointdata) # None - потому что VBO активирован
        
        # Рисуем данные массивов за один проход:
        # Первый параметр - какой тип примитивов использовать (треугольники, точки, линии и др.)
        # Второй параметр - начальный индекс в указанных массивах
        # Третий параметр - количество рисуемых объектов (в нашем случае это 2 вершины - 4 координаты)
        glDrawArrays(GL_LINES, 0, len(self.par.pointdata)//2)
        
        
        if self.par.collection_data:
            #glBindBuffer( GL_ARRAY_BUFFER, 0)
            #glBindBuffer( GL_ARRAY_BUFFER, self.par.color_vbo_col)
            glColorPointer(3, GL_UNSIGNED_BYTE, 0, self.par.collection_color)
        
            #glBindBuffer( GL_ARRAY_BUFFER, self.par.vbo_col )       
            glVertexPointer(2, GL_FLOAT, 0, self.par.collection_data) 
        
            glDrawArrays(GL_LINES, 0, len(self.par.collection_data)//2)
    '''

              
    
    def c_collection_VBO(self):
        c_pointdata = numpy.array(self.par.collection_data, dtype = numpy.float32)
        c_colordata = numpy.array(self.par.collection_color, dtype = numpy.ubyte)
        
        if not self.par.vbo_col:
            self.par.vbo_col = glGenBuffers(1)
            self.par.color_vbo_col = glGenBuffers(1)
        '''
        if self.par.vbo_col: # Если уже есть - удалить
            glDeleteBuffers(1, [self.par.vbo_col])
            glDeleteBuffers(1, [self.par.color_vbo_col])
        '''

        ### Стандартная процедура создания VBO ###
        glBindBuffer (GL_ARRAY_BUFFER, self.par.vbo_col)
        # 2 Параметр - указатель на массив pointdata
        glBufferData (GL_ARRAY_BUFFER, c_pointdata, GL_STATIC_DRAW)
        glBindBuffer (GL_ARRAY_BUFFER, 0)
        
        glBindBuffer (GL_ARRAY_BUFFER, self.par.color_vbo_col)
        # 2 Параметр - указатель на массив colordata
        glBufferData (GL_ARRAY_BUFFER, c_colordata, GL_STATIC_DRAW)
        glBindBuffer (GL_ARRAY_BUFFER, 0)
        '''
        else:
            #if self.par.vbo_col: # Если уже есть - удалить
                #glDeleteBuffers(1, [self.par.vbo_col])
                #glDeleteBuffers(1, [self.par.color_vbo_col])

            if not self.par.vbo_col:
                self.par.vbo_col = glGenBuffersARB(1)
                self.par.color_vbo_col = glGenBuffersARB(1)

            ### Стандартная процедура создания VBO ###
            #self.par.vbo_col = glGenBuffersARB(1)
            glBindBufferARB (GL_ARRAY_BUFFER_ARB, self.par.vbo_col)
            # 2 Параметр - указатель на массив pointdata
            glBufferDataARB (GL_ARRAY_BUFFER_ARB, c_pointdata, GL_STATIC_DRAW_ARB)
            glBindBufferARB (GL_ARRAY_BUFFER_ARB, 0)
            
            self.par.color_vbo_col = glGenBuffersARB(1)
            glBindBufferARB (GL_ARRAY_BUFFER_ARB, self.par.color_vbo_col)
            # 2 Параметр - указатель на массив colordata
            glBufferDataARB (GL_ARRAY_BUFFER_ARB, c_colordata, GL_STATIC_DRAW_ARB)
            glBindBufferARB (GL_ARRAY_BUFFER_ARB, 0)
        '''

    def change_pointdata(self):        
        self.par.inds_vals = dict((y,x) for x,y in enumerate(self.par.IDs))
        if not self.par.vbo:
            '''
            a = range(6000000)
            b = a*6
            self.vbo_size = len((GLfloat*len(a))(*a))#len(c_pointdata)#numpy.array(a, dtype = numpy.float32)
            self.color_vbo_size = len((GLfloat*len(b))(*b))#len(c_colordata)#numpy.array(b, dtype = numpy.ubyte)
            '''
            self.par.vbo = glGenBuffers(1)
            self.par.color_vbo = glGenBuffers(1)
            '''
            else:
                self.par.vbo = glGenBuffersARB(1)
                self.par.color_vbo = glGenBuffersARB(1)
            '''
        else:
            if self.par.vbo: # Если VBO есть - удалить
                glDeleteBuffers(1, [self.par.vbo, self.par.color_vbo])
                #glDeleteBuffers(1, [self.par.color_vbo])
    
        self.par.vbo, self.par.color_vbo = self.c_VBO(self.par.vbo, self.par.color_vbo, self.par.pointdata, self.par.colordata)

        #else:
            #self.update_VBO()
    '''
    def update_VBO(self):
        glBindBuffer (GL_ARRAY_BUFFER, self.par.vbo)
        
        vbo_pointer = ctypes.cast(
            glMapBuffer(
                GL_ARRAY_BUFFER, GL_WRITE_ONLY),
                ctypes.POINTER(ctypes.c_float)
            )
        vbo_array = numpy.ctypeslib.as_array(vbo_pointer,
                    (self.vbo_size,))
        
        data = numpy.array(self.par.pointdata, dtype = numpy.float32)
        #c_data = data.view(dtype=numpy.float32)
        #numpy.ctypeslib.as_ctypes(numpy.array(self.par.pointdata, dtype = numpy.float32))
        #numpy.array(pointdata, dtype = numpy.float32)
        #print len(data)
        #for ind, i in enumerate(vbo_array[0:len(data)]):
            #vbo_array[ind] = data[ind]
        vbo_array[0:len(data)] = data

        glUnmapBuffer(GL_ARRAY_BUFFER)
        glBindBuffer (GL_ARRAY_BUFFER, 0)
        glBindBuffer (GL_ARRAY_BUFFER, self.par.color_vbo)

        vbo_pointer = ctypes.cast(
            glMapBuffer(
                GL_ARRAY_BUFFER, GL_WRITE_ONLY),
                ctypes.POINTER(ctypes.c_ubyte)
            )
        vbo_array = numpy.ctypeslib.as_array(vbo_pointer,
                    (self.color_vbo_size,))
        
        data = numpy.array(self.par.colordata, dtype = numpy.ubyte)
        #numpy.ctypeslib.as_ctypes(numpy.array(self.par.colordata, dtype = numpy.ubyte))
        #numpy.array(pointdata, dtype = numpy.float32)
        #c_data = data.view(dtype=numpy.float32)
        #for ind, i in enumerate(vbo_array[0:len(data)]):
            #vbo_array[ind] = data[ind]
        vbo_array[0:len(data)] = data

        glUnmapBuffer(GL_ARRAY_BUFFER)
    '''
        
    def c_VBO(self, vbo, color_vbo, pointdata, colordata):
        '''
        #c_pointdata = (GLfloat*len(pointdata))(*pointdata)#
        #c_pointdata = numpy.array(pointdata, dtype = numpy.float32)
        c_pointdata = pointdata.tostring()
        c_colordata = colordata.tostring()
        #c_colordata = (GLubyte*len(colordata))(*colordata)#
        #c_colordata = numpy.array(colordata, dtype = numpy.ubyte)
        #size_point = c_pointdata.nbytes
        #size_color = c_colordata.nbytes
        #print size_point, size_color, size_point+size_color
            
        ### Стандартная процедура создания VBO ###            
        glBindBuffer (GL_ARRAY_BUFFER, vbo)
        
        # 2 Параметр - указатель на массив pointdata
        glBufferData (GL_ARRAY_BUFFER, c_pointdata, GL_STATIC_DRAW)
        #glBufferSubData(GL_ARRAY_BUFFER, 0, size_point, c_pointdata)
        glBindBuffer (GL_ARRAY_BUFFER, 0)
        
        glBindBuffer (GL_ARRAY_BUFFER, color_vbo)

        # 2 Параметр - указатель на массив colordata
        glBufferData (GL_ARRAY_BUFFER, c_colordata, GL_STATIC_DRAW)
        #glBufferSubData(GL_ARRAY_BUFFER, 0, size_color, c_colordata)
        glBindBuffer (GL_ARRAY_BUFFER, 0)
        '''
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
        #self.par.dynamic_matrix = matrix
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
    #, GL_FRAGMENT_SHADER, glCreateProgram, glAttachShader, glLinkProgram, glUseProgram, glCreateShader, glShaderSource, glCompileShader

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
