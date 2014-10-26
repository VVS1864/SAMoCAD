# -*- coding: utf-8; -*-
import sys

from Tkinter import*
import ttk
import os
from entry import*
from math import fmod, pi
from tooltip import ToolTip
import select_clone

appPath = os.getcwd()
class Gui:
    def __init__(self, master1, parent1):
        self.d_opt1 = None #окно параметров рисования
        self.d_opt2 = None #окно параметров размеров
        self.d_opt3 = None #окно параметров линий
        self.d_opt4 = None #окно параметров текста
        self.o_prop = None #окно свойств
        self.d_opt1_off_on = False
        self.d_opt2_off_on = False
        self.d_opt3_off_on = False
        self.d_opt4_off_on = False
        self.o_prop_off_on = False
        self.colores = ["white",
                        "light blue",
                        "blue",
                        "green",
                        "gray",
                        "black",
                        "yellow",
                        "orange",
                        "red"]

        self.stipples = {'_____________':None,
                         '_ _ _ _ _ _ _':[1.0,1.0],
                         '____ _ ____ _':[4.0,1.0,1.0,1.0],
                         '____ _ _ ____':[4.0,1.0,1.0,1.0,1.0,1.0]}

        self.parent = parent1
        #self.button_zoom_color = 'grey'#'red'
        #self.button_res_color = 'grey'#'light blue'
        #self.button_func_color = 'grey'#'orange'

        self.master1 = master1
        self.ico = PhotoImage(file = os.path.join(appPath, 'res', 'icon2.gif'))
        self.master1.tk.call('wm', 'iconphoto', self.master1._w, self.ico) #Иконка
        self.master1.title(self.parent.prog_version + ' - ' + 'New draft')
        self.master1.geometry('1024x720+0+0')


#Менюбар
        self.menubar = Menu(self.master1)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.parent.new, accelerator = 'ctrl + n')
        self.filemenu.add_command(label="Save as", command=self.parent.fileSave)
        self.filemenu.add_command(label="Save", command=self.parent.fileCurSave)
        self.filemenu.add_command(label="Open", command=self.parent.fileOpen, accelerator = 'ctrl + o')
        self.filemenu.add_command(label="Print to postScript", command=self.parent.print_postScript, accelerator = 'ctrl + p')
        self.filemenu.add_command(label="Export to DXF", command=self.parent.exportDXF)
        self.filemenu.add_command(label="Import from DXF", command=self.parent.importDXF)
        self.filemenu.add_command(label="Exit", command=self.parent.exitMethod)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.viewmenu = Menu(self.menubar, tearoff=0)
        self.viewmenu.add_command(label="Zoom +", command=self.parent.zoommerP)
        self.viewmenu.add_command(label="Zoom -", command=self.parent.zoommerM)
        self.menubar.add_cascade(label="View", menu=self.viewmenu)

        self.drawmenu = Menu(self.menubar, tearoff=0)
        self.drawmenu.add_command(label="Line", command=self.parent.risLine)
        self.drawmenu.add_command(label="Dimension", command=self.parent.risDim)
        self.drawmenu.add_command(label="Text", command=self.parent.risText)
        self.drawmenu.add_command(label="Circle", command=self.parent.risCircle)
        self.drawmenu.add_command(label="Arc", command=self.parent.risArc)
        self.menubar.add_cascade(label="Draw", menu=self.drawmenu)

        self.funcmenu = Menu(self.menubar, tearoff=0)
        self.funcmenu.add_command(label="Copy", command=self.parent.copyEvent, accelerator = 'ctrl + z')
        self.funcmenu.add_command(label="Move", command=self.parent.moveEvent, accelerator = 'ctrl + a')
        self.funcmenu.add_command(label="Mirror", command=self.parent.mirrorEvent, accelerator = 'ctrl + x')
        self.funcmenu.add_command(label="Rotate", command=self.parent.rotateEvent, accelerator = 'ctrl + s')
        self.funcmenu.add_command(label="Offset", command=self.parent.offsetEvent)
        self.funcmenu.add_command(label="Copy properties", command=self.parent.copy_prop, accelerator = 'ctrl + d')
        self.funcmenu.add_command(label="Fillet", command=self.parent.filletEvent)
        self.funcmenu.add_command(label="Trim", command=self.parent.trimEvent, accelerator = 'ctrl + q')
        self.funcmenu.add_command(label="Extend", command=self.parent.extendEvent, accelerator = 'ctrl + w')
        self.funcmenu.add_command(label="Scale", command=self.parent.scaleEvent, accelerator = 'ctrl + r')
        self.funcmenu.add_command(label="Chain dimension", command=self.parent.trim_dim, accelerator = 'ctrl + m')
        self.menubar.add_cascade(label="Functions", menu=self.funcmenu)

        self.toolsmenu = Menu(self.menubar, tearoff=0)
        self.toolsmenu.add_command(label="Object properties", command=self.obj_prop)
        self.menubar.add_cascade(label="Tools", menu=self.toolsmenu)



        self.funcmenu = Menu(self.menubar, tearoff=0)
        self.funcmenu.add_command(label="Draw options", command=self.draw_opt)
        self.funcmenu.add_command(label="Dimension options", command=self.dim_opt)
        self.funcmenu.add_command(label="Lines options", command=self.line_opt)
        self.funcmenu.add_command(label="Text options", command=self.text_opt)
        self.menubar.add_cascade(label="Options", menu=self.funcmenu)



        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About programm", command=self.about)
        self.helpmenu.add_separator({})
        self.helpmenu.add_command(label="License", command=self.license_)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)


        self.master1.config(menu=self.menubar)

#Текст
        self.Habout = u"""
Programm SAMoCAD is open software
and designed to create simple drawings

Version - 0.0.8.5 alfa

Copyright 2014 - VVS1864

Apache License, Version 2.0.
"""
        self.lic  = u"""
Copyright 2014 Vlad Simonov

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

#Фреймы
        self.propertis_frame = Frame(self.master1)#Параметры
        self.propertis_frame.pack(side=TOP, fill=X)

        self.frame1=Frame(self.master1)#Канвас
        self.frame1.pack(side=TOP, fill=BOTH,expand=YES)

        self.frame2=Frame(self.frame1)#Панель кнопок лево
        self.frame2.pack(side=LEFT,fill=Y)

        self.frame2p=Frame(self.frame1)#Панель кнопок право
        

        self.frame3=Frame(self.master1)
        self.frame3.pack(side=BOTTOM, fill=X)

        self.frame5=Frame(self.master1)#Инфо
        self.frame5.pack(side=BOTTOM, fill=X)

        self.frame4=Frame(self.master1)#Коммандная строка
        self.frame4.pack(side=BOTTOM, fill=X)

#Панеть настроек черчения
        def size_t_ok(event = None):
            size = self.entry_size_t.get()
            if size < 0:
                size = -size
            if size > 0:
                size = -float(size)*100
                self.parent.size_t = size
                self.parent.param_edit({'size':size})
                self.command.focus_set()

        def size_f_ok(event = None):
            size = self.entry_size_f.get()
            if size < 0:
                size = -size
            if size > 0:
                size = -float(size)*100
                self.parent.size_f = size
                self.parent.param_edit({'size':size})
                self.command.focus_set()

        self.label_color = Label(self.propertis_frame, text = '           ', bg = self.parent.color)
        self.label_color.grid(row = 0, column = 0, padx = 3, pady = 3)
        self.combo_color = ttk.Combobox(self.propertis_frame, values = self.colores, state='readonly')
        self.combo_color.set("white")
        self.combo_color.grid(row = 0, column = 1, padx = 3, pady = 3)

        self.image_width = PhotoImage(file = os.path.join(appPath, 'res', 'width.gif'))
        self.label_width = Label(self.propertis_frame, image = self.image_width)
        self.label_width.grid(row = 0, column = 2, padx = 3, pady = 3)
        self.combo_width = ttk.Combobox(self.propertis_frame, values = ["1",
                                                               "2",
                                                               "3",
                                                               "4"], width = 5, state='readonly')
        self.combo_width.set("2")
        self.combo_width.grid(row = 0, column = 3, padx = 3, pady = 3)

        self.combo_s = ttk.Combobox(self.propertis_frame, values = self.stipples.keys(), width = 10, state='readonly')
        self.combo_s.set("_____________")
        self.combo_s.grid(row = 0, column = 4, padx = 3, pady = 3)

        self.image_h_text = PhotoImage(file = os.path.join(appPath, 'res', 'h_text.gif'))
        self.label_size_t = Label(self.propertis_frame, image = self.image_h_text)
        self.label_size_t.grid(row = 0, column = 5, padx = 3, pady = 3)

        self.entry_size_t = FloatEntry(self.propertis_frame, font = 'txt 12', width=5)
        self.entry_size_t.insert(0, "5")
        self.entry_size_t.grid(row = 0, column = 6, padx = 3, pady = 3)

        self.image_h_dim = PhotoImage(file = os.path.join(appPath, 'res', 'h_dim.gif'))
        self.label_size_f = Label(self.propertis_frame, image = self.image_h_dim)
        self.label_size_f.grid(row = 0, column = 7, padx = 3, pady = 3)

        self.entry_size_f = FloatEntry(self.propertis_frame, font = 'txt 12', width=5)
        self.entry_size_f.insert(0, "3.5")
        self.entry_size_f.grid(row = 0, column = 8, padx = 3, pady = 3)

        self.image_save = PhotoImage(file = os.path.join(appPath, 'res', 'saveas.gif'))
        self.button_seve=Button(self.propertis_frame, image = self.image_save, command = self.parent.fileCurSave)
        self.button_seve.grid(row = 0, column = 9,  sticky = 'e')

        self.image_open = PhotoImage(file = os.path.join(appPath, 'res', 'open.gif'))
        self.button_open=Button(self.propertis_frame, image = self.image_open, command = self.parent.fileOpen)
        self.button_open.grid(row = 0, column = 10, sticky = 'e')

        self.image_undo = PhotoImage(file = os.path.join(appPath, 'res', 'undo.gif'))
        self.button_undo=Button(self.propertis_frame, image = self.image_undo, command = self.parent.undo)
        self.button_undo.grid(row = 0, column = 11, sticky = 'e')

#командная строка
        self.dialog=Label(self.frame4, anchor = W, font='txt 12', width=30, text='Command:')
        self.dialog.grid(row=0,column=0)
        self.command = Entry(self.frame4, font = 'txt 12',width=100)
        self.command.grid(row=0,column=1)
        self.info=Label(self.frame5, anchor = W, font='txt 12', text='')
        self.info.grid(row=0,column=0)
        self.command.focus_set()
#Кнопки
        self.button_orto=Button(self.frame3,text="Orto",font=('txt 12'),command = self.parent.ort)
        self.button_orto.pack(side = LEFT)
        self.button_orto.config(bg='white',fg='black', activebackground = 'white', activeforeground = 'black')

        self.button_trace = Button(self.frame3,text="Trace",font=('txt 12'),command = self.parent.trac)
        self.button_trace.pack(side = LEFT)
        self.button_trace.config(bg='blue',fg='red', activebackground = 'blue', activeforeground = 'red')

        self.button_trace_obj = Button(self.frame3,text="Object trace",font=('txt 12'),command = self.parent.trac_obj)
        self.button_trace_obj.pack(side = LEFT)
        self.button_trace_obj.config(bg='blue',fg='red', activebackground = 'blue', activeforeground = 'red')

        self.button_snap_N = Button(self.frame3,text="Snap near",font=('txt 12'),command = self.parent.snap_n)
        self.button_snap_N.pack(side = LEFT)
        self.button_snap_N.config(bg='blue',fg='red', activebackground = 'blue', activeforeground = 'red')


        self.p = PhotoImage(file = os.path.join(appPath, 'res', 'p2.gif'))
        self.buttonP=Button(self.frame2,command = self.parent.zoommerP, image = self.p)#, #bg = self.button_zoom_color)
        self.buttonP.grid(row = 2, column = 0)

        self.m = PhotoImage(file = os.path.join(appPath, 'res', 'm2.gif'))
        self.buttonM=Button(self.frame2,command = self.parent.zoommerM, image = self.m)#, bg = self.button_zoom_color)
        self.buttonM.grid(row = 3, column = 0)

        self.image_line = PhotoImage(file = os.path.join(appPath, 'res', 'line2.gif'))
        self.buttonLine=Button(self.frame2,command = self.parent.risLine, image = self.image_line)#, bg = self.button_res_color)
        self.buttonLine.grid(row = 4, column = 0)

        self.image_circle = PhotoImage(file = os.path.join(appPath, 'res', 'circle2.gif'))
        self.buttonCircle=Button(self.frame2,command = self.parent.risCircle, image = self.image_circle)#, bg = self.button_res_color)
        self.buttonCircle.grid(row = 5, column = 0)

        self.image_arc = PhotoImage(file = os.path.join(appPath, 'res', 'arc2.gif'))
        self.buttonArc=Button(self.frame2,command = self.parent.risArc, image = self.image_arc)#,  bg = self.button_res_color)
        self.buttonArc.grid(row = 6, column = 0)

        self.image_dim = PhotoImage(file = os.path.join(appPath, 'res', 'dim2.gif'))
        self.buttonDim=Button(self.frame2,font=('txt 12'),command = self.parent.risDim, image = self.image_dim)#, bg = self.button_res_color)
        self.buttonDim.grid(row =7, column = 0)

        self.image_dimR = PhotoImage(file = os.path.join(appPath, 'res', 'radius.gif'))
        self.buttonDimR=Button(self.frame2,font=('txt 12'),command = self.parent.risDimR, image = self.image_dimR)#, bg = self.button_res_color)
        self.buttonDimR.grid(row =8, column = 0)

        self.image_text = PhotoImage(file = os.path.join(appPath, 'res', 'text2.gif'))
        self.buttonText=Button(self.frame2,font=('txt 12'),command = self.parent.risText, image = self.image_text)#, bg = self.button_res_color)
        self.buttonText.grid(row = 9, column = 0)

        self.image_copy = PhotoImage(file = os.path.join(appPath, 'res', 'copy2.gif'))
        self.buttonCopy=Button(self.frame2p,command = self.parent.copyEvent, image = self.image_copy)#, bg = self.button_func_color)
        self.buttonCopy.grid(row = 0, column = 0)

        self.image_move = PhotoImage(file = os.path.join(appPath, 'res', 'move2.gif'))
        self.buttonMove=Button(self.frame2p,command = self.parent.moveEvent, image = self.image_move)#, bg = self.button_func_color)
        self.buttonMove.grid(row = 1, column = 0)


        self.image_mir = PhotoImage(file = os.path.join(appPath, 'res', 'mirror2.gif'))
        self.buttonMir=Button(self.frame2p,command = self.parent.mirrorEvent, image = self.image_mir)#, bg = self.button_func_color)
        self.buttonMir.grid(row = 2, column = 0)

        self.image_rot = PhotoImage(file = os.path.join(appPath, 'res', 'rotate2.gif'))
        self.buttonRot=Button(self.frame2p,command = self.parent.rotateEvent, image = self.image_rot)#, bg = self.button_func_color)
        self.buttonRot.grid(row = 3, column = 0)

        self.image_offset = PhotoImage(file = os.path.join(appPath, 'res', 'offset2.gif'))
        self.buttonOffset=Button(self.frame2p,image = self.image_offset, command = self.parent.offsetEvent)#, bg = self.button_func_color)
        self.buttonOffset.grid(row = 4, column = 0)

        self.image_copy_p = PhotoImage(file = os.path.join(appPath, 'res', 'copy_p2.gif'))
        self.buttonCopyP=Button(self.frame2p,image = self.image_copy_p, command = self.parent.copy_prop)#, bg = self.button_func_color)
        self.buttonCopyP.grid(row = 5, column = 0)

        self.image_fillet = PhotoImage(file = os.path.join(appPath, 'res', 'fillet2.gif'))
        self.buttonFillet=Button(self.frame2p, image = self.image_fillet, command = self.parent.filletEvent)#, bg = self.button_func_color)
        self.buttonFillet.grid(row = 6, column = 0)

        self.image_trim = PhotoImage(file = os.path.join(appPath, 'res', 'trim2.gif'))
        self.buttonTrim=Button(self.frame2p, image = self.image_trim, command = self.parent.trimEvent)#, bg = self.button_func_color)
        self.buttonTrim.grid(row = 7, column = 0)

        self.image_extend = PhotoImage(file = os.path.join(appPath, 'res', 'extend2.gif'))
        self.buttonExtend=Button(self.frame2p, image = self.image_extend, command = self.parent.extendEvent)#, bg = self.button_func_color)
        self.buttonExtend.grid(row = 8, column = 0)

        self.image_scale = PhotoImage(file = os.path.join(appPath, 'res', 'scale.gif'))
        self.buttonScale=Button(self.frame2p, image = self.image_scale, command = self.parent.scaleEvent)#, bg = self.button_func_color)
        self.buttonScale.grid(row = 9, column = 0)

        self.image_trim_dim = PhotoImage(file = os.path.join(appPath, 'res', 'chain_dim.gif'))
        self.buttonTrim_dim=Button(self.frame2p, image = self.image_trim_dim, command = self.parent.trim_dim)#, bg = self.button_func_color)
        self.buttonTrim_dim.grid(row = 10, column = 0)
#ToolTips
        self.tooltip_line = ToolTip(self.buttonLine, text="Line")
        self.tooltip_circle = ToolTip(self.buttonCircle, text="Circle")
        self.tooltip_arc = ToolTip(self.buttonArc, text="Arc")
        self.tooltip_dim = ToolTip(self.buttonDim, text="Dimension")
        self.tooltip_dimR = ToolTip(self.buttonDimR, text="Radial dimension")
        self.tooltip_text = ToolTip(self.buttonText, text="Text")
        self.tooltip_copy = ToolTip(self.buttonCopy, text="Copy")
        self.tooltip_move = ToolTip(self.buttonMove, text="Move")
        self.tooltip_mir = ToolTip(self.buttonMir, text="Mirror")
        self.tooltip_rot = ToolTip(self.buttonRot, text="Rotate")
        self.tooltip_offset = ToolTip(self.buttonOffset, text="Offset")
        self.tooltip_copy_p = ToolTip(self.buttonCopyP, text="Copy properties")
        self.tooltip_fillet = ToolTip(self.buttonFillet, text="Fillet")
        self.tooltip_trim = ToolTip(self.buttonTrim, text="Trim line")
        self.tooltip_extend = ToolTip(self.buttonExtend, text="Extend line")
        self.tooltip_scale = ToolTip(self.buttonScale, text="Scale")
        self.tooltip_trim_dim = ToolTip(self.buttonTrim_dim, text="Chain dimension")
        
#Канвас
        self.canvas=Canvas(self.frame1,bg=self.parent.fon_color)
        self.canvas.config(cursor='crosshair')
        
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        self.cc = None

        self.frame2p.pack(side=LEFT,fill=Y)

#Действия событий

        def select_color(event):
            col = self.combo_color.get()
            self.parent.color =  col
            self.label_color.config(bg = col)
            self.parent.param_edit({'fill':col})
            self.command.focus_set()


        def select_width(event):
            wid = self.combo_width.get()
            self.parent.width =  wid
            self.parent.param_edit({'width':wid})
            self.command.focus_set()

        def select_stipple(event):
            s = self.combo_s.get()
            stipple = self.stipples[s]
            #if stipple:
                #stipple = map(lambda x: x*self.parent.stipple_size, stipple)
            self.parent.stipple =  stipple
            self.parent.param_edit({'stipple':stipple})
            self.command.focus_set()



#События
        self.combo_color.bind("<<ComboboxSelected>>", select_color)
        self.combo_width.bind("<<ComboboxSelected>>", select_width)
        self.combo_s.bind("<<ComboboxSelected>>", select_stipple)

        self.entry_size_t.bind("<FocusOut>", size_t_ok)
        self.entry_size_f.bind("<FocusOut>", size_f_ok)

    def about(self, event = None):
        self.imag = PhotoImage(file = os.path.join(appPath, 'res', 'icon3.gif'))
        eroot = Toplevel()
        eroot.title('About programm')
        eroot.resizable(width=FALSE, height=FALSE)
        l_donate = Label(eroot, justify = LEFT, text = self.Habout)
        but = Button(eroot, text = 'License', command = self.license_)
        but2 = Button(eroot, text = 'Donate', command = self.parent.d)
        but3 = Button(eroot, text = 'Close', command = eroot.destroy)
        ca = Canvas(eroot, width = 100, height = 100)
        ca.create_image(0,0,anchor=NW,image = self.imag)

        ca.grid(row=0, column = 0, rowspan = 2, padx = 5, pady = 5)
        l_donate.grid(row=0, column = 1,columnspan = 3, padx = 10, pady = 10)
        but.grid(row=1, column = 1, padx = 10, pady = 10)
        but2.grid(row=1, column = 2, padx = 10, pady = 10)
        but3.grid(row=1, column = 3, padx = 10, pady = 10)

    def license_(self, event = None):
        eroot = Toplevel()
        eroot.title('License')
        eroot.resizable(width=FALSE, height=FALSE)
        l_ = Label(eroot, justify = LEFT, text = self.lic)
        but = Button(eroot, text = 'Close', command = eroot.destroy)
        l_.grid(row=0, column = 1,columnspan = 3, padx = 10, pady = 10)
        but.grid(row=1, column = 2, padx = 10, pady = 10)

    def draw_opt(self):
        if self.d_opt1_off_on == False:
            self.d_opt1 = Draw_options()

    def dim_opt(self):
        if self.d_opt2_off_on == False:
            self.d_opt2 = Dim_options()

    def line_opt(self):
        if self.d_opt3_off_on == False:
            self.d_opt3 = Line_options()

    def text_opt(self):
        if self.d_opt4_off_on == False:
            self.d_opt4 = Text_options()

    def obj_prop(self, event = None):
        if self.o_prop_off_on == False:
            self.o_prop = Object_properties()

    def update_prop(self):
        if self.o_prop:
            self.o_prop.viewer()

    def normal(self, num):
        if num < 0:
            num = -num
        if num > 0:
            num = float(num)
        return num



class Options:
    def __init__(self):

        self.window = Toplevel()
        self.ico = PhotoImage(file = os.path.join(appPath, 'res', 'options.gif'))
        self.window.tk.call('wm', 'iconphoto', self.window._w, self.ico)
        self.window.transient(gui.master1)
        self.frame_buttons = Frame(self.window)
        self.window.resizable(width=FALSE, height=FALSE)

        self.button_apply = Button(self.frame_buttons, text = 'Apply', command = self.apply_p)
        self.button_close = Button(self.frame_buttons, text = 'Close', command = self.exitMethod)
        self.button_apply.grid(row = 0, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.button_close.grid(row = 0, column = 1, sticky = 'w', padx = 3, pady = 3)
        self.window.protocol('WM_DELETE_WINDOW', self.exitMethod)
        self.window.bind("<Escape>", self.exitMethod)
        self.window.bind("<Return>", self.apply_p)

    def apply_p(self):
        pass
    def exitMethod(self, event = None):
        pass



class Draw_options(Options):
    def __init__(self):
        Options.__init__(self)
        gui.d_opt1_off_on = True
        self.window.title('Draw options')


        self.frame_label1 = Frame(self.window)
        self.frame_options1 = Frame(self.window)
        self.frame_label2 = Frame(self.window)
        self.frame_options2 = Frame(self.window)

        def check_snap():
            if self.snap_Flag == False:
                self.snap_Flag = True
            else:
                self.snap_Flag = False

        def check_tracing():
            if self.tracing_Flag == False:
                self.tracing_Flag = True
            else:
                self.tracing_Flag = False

        def select_color_snap(event):
            col = self.combo_col_snap.get()
            self.label_col_snap2.config(bg = col)
        def select_color_select(event):
            col = self.combo_col_select.get()
            self.label_col_select2.config(bg = col)
        def select_color_fon(event):
            col = self.combo_col_fon.get()
            self.label_col_fon2.config(bg = col)

        self.snap_Flag = False
        self.tracing_Flag = False
        self.snap_Flagg = IntVar()
        self.tracing_Flagg = IntVar()
        self.label_n_snap = Label(self.frame_label1, text = 'Snap options')
        self.n_snap = Checkbutton(self.frame_options1,text='Snap to near point',variable = self.snap_Flagg, command = check_snap)
        self.tracing = Checkbutton(self.frame_options1,text='Tracing',variable = self.tracing_Flagg, command = check_tracing)

        self.label_tracing_step = Label(self.frame_options1, text = 'Step of tracing angle')
        self.combo_tracing_step = ttk.Combobox(self.frame_options1, values = ('5.0',
                                                                          '10.0',
                                                                          '15.0',
                                                                          '30.0',
                                                                          '45.0',
                                                                          '60.0',
                                                                          '90.0'), width = 10, state='readonly')
        self.combo_tracing_step.set(gui.parent.angle_s)

        self.label_col_snap1 = Label(self.frame_options2, text = 'Color snap icon')
        self.label_col_snap2 = Label(self.frame_options2, text = '                 ', bg = gui.parent.priv_color)
        self.combo_col_snap = ttk.Combobox(self.frame_options2, values = gui.colores, width = 10, state='readonly')
        self.combo_col_snap.set(gui.parent.priv_color)
        self.combo_col_snap.bind("<<ComboboxSelected>>", select_color_snap)

        

        self.label_size_snap_z = Label(self.frame_options1, text = 'Size snap icon')
        self.entry_size_snap_z = FloatEntry(self.frame_options1)
        self.entry_size_snap_z.insert(0, gui.parent.size_simbol_p)

        self.label_dist_snap = Label(self.frame_options1, text = 'Snap distanse')
        self.entry_size_snap = FloatEntry(self.frame_options1)
        self.entry_size_snap.insert(0, gui.parent.snap_s)

        self.label_dr_opt = Label(self.frame_label2, text = 'Show options')
        '''
        self.label_dim_s = Label(self.frame_options2, text = 'Пропорции размеров')
        self.entry_dim_s = FloatEntry(self.frame_options2)
        self.entry_dim_s.insert(0, gui.parent.s)
        '''
        self.label_col_select = Label(self.frame_options2, text = 'Color of select objects')
        self.label_col_select2 = Label(self.frame_options2, text = '                 ', bg = gui.parent.select_color)
        self.combo_col_select = ttk.Combobox(self.frame_options2, values = gui.colores, width = 10, state='readonly')
        self.combo_col_select.set(gui.parent.select_color)
        self.combo_col_select.bind("<<ComboboxSelected>>", select_color_select)

        self.label_col_fon = Label(self.frame_options2, text = 'Color background')
        self.label_col_fon2 = Label(self.frame_options2, text = '                 ', bg = gui.parent.fon_color)
        self.combo_col_fon = ttk.Combobox(self.frame_options2, values = gui.colores, width = 10, state='readonly')
        self.combo_col_fon.set(gui.parent.fon_color)
        self.combo_col_fon.bind("<<ComboboxSelected>>", select_color_fon)


#Упаковщик
        self.frame_label1.grid(row = 0, column = 0)
        self.frame_options1.grid(row = 1, column = 0, sticky = 'w')
        self.frame_label2.grid(row = 2, column = 0)
        self.frame_options2.grid(row = 3, column = 0, sticky = 'w')
        self.frame_buttons.grid(row = 4, column = 0, sticky = 'e')

        self.label_n_snap.grid(row = 0, column = 0, columnspan = 2)
        self.n_snap.grid(row = 0, column = 0, columnspan = 2, sticky = 'w', padx = 3, pady = 3)
        self.tracing.grid(row = 1, column = 0, columnspan = 2, sticky = 'w', padx = 3, pady = 3)
        
        self.label_size_snap_z.grid(row = 2, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.entry_size_snap_z.grid(row = 2, column = 1, sticky = 'w', padx = 3, pady = 3)

        self.label_dist_snap.grid(row = 3, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.entry_size_snap.grid(row = 3, column = 1, sticky = 'w', padx = 3, pady = 3)

        self.label_tracing_step.grid(row = 4, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.combo_tracing_step.grid(row = 4, column = 1, sticky = 'w', padx = 3, pady = 3)

        self.label_dr_opt.grid(row = 0, column = 0, columnspan = 2)
        #self.label_dim_s.grid(row = 0, column = 0, sticky = 'w', padx = 3, pady = 3, columnspan = 2)
        #self.entry_dim_s.grid(row = 0, column = 1, sticky = 'w', padx = 3, pady = 3, columnspan = 2)

        self.label_col_snap1.grid(row = 0, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.label_col_snap2.grid(row = 0, column = 1, sticky = 'w', padx = 3, pady = 3)
        self.combo_col_snap.grid(row = 0, column = 2, sticky = 'w', padx = 3, pady = 3)

        self.label_col_select.grid(row = 1, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.label_col_select2.grid(row = 1, column = 1, sticky = 'w', padx = 3, pady = 3)
        self.combo_col_select.grid(row = 1, column = 2, sticky = 'w', padx = 3, pady = 3)

        self.label_col_fon.grid(row = 2, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.label_col_fon2.grid(row = 2, column = 1, sticky = 'w', padx = 3, pady = 3)
        self.combo_col_fon.grid(row = 2, column = 2, sticky = 'w', padx = 3, pady = 3)

        if gui.parent.snap_near == True:
            self.n_snap.select()
            self.snap_Flag = True

        if gui.parent.tracingFlag == True:
            self.tracing.select()
            self.tracing_Flag = True

    def apply_p(self, event = None):
        n_snap = self.snap_Flag
        tracing = self.tracing_Flag
        tracing_step = self.combo_tracing_step.get()
        combo_col_snap = self.combo_col_snap.get()
        entry_size_snap_z = self.entry_size_snap_z.get()
        entry_size_snap = self.entry_size_snap.get()
        combo_col_select = self.combo_col_select.get()
        combo_col_fon = self.combo_col_fon.get()

        gui.parent.angle_s = float(tracing_step)
        gui.parent.snap_near = n_snap
        gui.parent.tracingFlag = tracing
        gui.parent.priv_color = combo_col_snap
        gui.parent.select_color = combo_col_select

        gui.parent.fon_color = combo_col_fon
        gui.parent.c.config(bg = combo_col_fon)
        if combo_col_fon == 'light blue':
            gui.parent.left_color = 'black'
        else:
            gui.parent.left_color = 'light blue'
        if combo_col_fon == 'red':
            gui.parent.right_color = 'orange'
        else:
            gui.parent.right_color = 'red'

        gui.parent.size_simbol_p = gui.normal(entry_size_snap_z)
        gui.parent.snap_s = gui.normal(entry_size_snap)

        gui.parent.snap_n(color_only = 'yes')
        gui.parent.ort(color_only = 'yes')
        gui.parent.trac(color_only = 'yes')

    def exitMethod(self, event = None):
        self.window.destroy()
        gui.d_opt1_off_on = False

class Dim_options(Options):
    def __init__(self):
        Options.__init__(self)
        gui.d_opt2_off_on = True
        self.window.title('Dimension options')
        self.frame_options1 = Frame(self.window)
        self.frame_pic = Frame(self.window, bg = 'white', bd = 5, relief = RIDGE)

        self.select = 0
        def select_type_arrow(event):
            self.select = 1

        self.imag = PhotoImage(file = os.path.join(appPath, 'res', 'dim_prop.gif'))
        ca = Canvas(self.frame_pic, width = 200, height = 156, bg = 'white')
        ca.create_image(0,0,anchor=NW,image = self.imag)
        ca.grid(row = 0, column = 0, padx = 8, pady = 20)

        self.label_s = Label(self.frame_options1, text = 'Offset from origin [A]')
        self.entry_s = FloatEntry(self.frame_options1)
        self.entry_s.insert(0, gui.parent.s)

        self.label_arrow_s = Label(self.frame_options1, text = 'Arrowhead size [B]')
        self.entry_arrow_s = FloatEntry(self.frame_options1)
        self.entry_arrow_s.insert(0, gui.parent.arrow_s)

        self.label_vr_s = Label(self.frame_options1, text = 'Extend dim lines [C]')
        self.entry_vr_s = FloatEntry(self.frame_options1)
        self.entry_vr_s.insert(0, gui.parent.vr_s)

        self.label_vv_s = Label(self.frame_options1, text = 'Extend ticks [D]')
        self.entry_vv_s = FloatEntry(self.frame_options1)
        self.entry_vv_s.insert(0, gui.parent.vv_s)

        self.label_s_s = Label(self.frame_options1, text = 'Letters distance factor')
        self.entry_s_s = FloatEntry(self.frame_options1)
        self.entry_s_s.insert(0, gui.parent.s_s_dim)

        self.label_w_text = Label(self.frame_options1, text = 'Width of letters factor')
        self.entry_w_text = FloatEntry(self.frame_options1)
        self.entry_w_text.insert(0, gui.parent.w_text_dim)

        self.label_type_arrow = Label(self.frame_options1, text = 'Arrowhead type')
        self.combo_type_arrow = ttk.Combobox(self.frame_options1, values = ['Architectural tick',
                                                                            'Arrow'], width = 20, state='readonly')

        self.label_font = Label(self.frame_options1, text = 'Font')
        self.combo_font = ttk.Combobox(self.frame_options1, values = ['Architectural',
                                                                            'Simumar TXT'], width = 20, state='readonly')
        if gui.parent.type_arrow == 'Arch':
            self.combo_type_arrow.set('Architectural tick')
        elif gui.parent.type_arrow == 'Arrow':
            self.combo_type_arrow.set('Arrow')
        self.combo_font.set(gui.parent.font_dim)
        self.combo_type_arrow.bind("<<ComboboxSelected>>", select_type_arrow)

        #Упаковщик
        self.frame_pic.grid(row = 0, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.frame_options1.grid(row = 0, column = 1, sticky = 'w')
        self.frame_buttons.grid(row = 1, column = 1, sticky = 'e')

        self.label_s.grid(row = 1, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.entry_s.grid(row = 1, column = 1, sticky = 'w', padx = 3, pady = 3)

        self.label_arrow_s.grid(row = 2, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.entry_arrow_s.grid(row = 2, column = 1, sticky = 'w', padx = 3, pady = 3)

        self.label_vr_s.grid(row = 3, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.entry_vr_s.grid(row = 3, column = 1, sticky = 'w', padx = 3, pady = 3)

        self.label_vv_s.grid(row = 4, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.entry_vv_s.grid(row = 4, column = 1, sticky = 'w', padx = 3, pady = 3)

        self.label_s_s.grid(row = 5, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.entry_s_s.grid(row = 5, column = 1, sticky = 'w', padx = 3, pady = 3)

        self.label_w_text.grid(row = 6, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.entry_w_text.grid(row = 6, column = 1, sticky = 'w', padx = 3, pady = 3)

        self.label_type_arrow.grid(row = 7, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.combo_type_arrow.grid(row = 7, column = 1, sticky = 'w', padx = 3, pady = 3)

        self.label_font.grid(row = 8, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.combo_font.grid(row = 8, column = 1, sticky = 'w', padx = 3, pady = 3)
    def apply_p(self, event = None):
        entry_s = self.entry_s.get()
        entry_arrow_s = self.entry_arrow_s.get()
        entry_vr_s = self.entry_vr_s.get()
        entry_vv_s = self.entry_vv_s.get()
        entry_s_s = self.entry_s_s.get()
        entry_w_text = self.entry_w_text.get()
        type_arrow = self.combo_type_arrow.get()
        font = self.combo_font.get()

        if self.select == 1:
            if type_arrow == 'Architectural tick':
                gui.parent.type_arrow = 'Arch'
            elif type_arrow == 'Arrow':
                gui.parent.type_arrow = 'Arrow'
                entry_vr_s = 0
                self.entry_vr_s.delete(0, END)
                self.entry_vr_s.insert(0, str(entry_vr_s))
        gui.parent.font_dim = font
        gui.parent.s = gui.normal(entry_s)
        gui.parent.arrow_s = gui.normal(entry_arrow_s)
        gui.parent.vr_s = gui.normal(entry_vr_s)
        gui.parent.vv_s = gui.normal(entry_vv_s)
        gui.parent.s_s_dim = gui.normal(entry_s_s)
        gui.parent.w_text_dim = gui.normal(entry_w_text)

        self.select = 0

    def exitMethod(self, event = None):
        self.window.destroy()
        gui.d_opt2_off_on = False

class Line_options(Options):
    def __init__(self):
        Options.__init__(self)
        gui.d_opt3_off_on = True
        self.window.title('Lines options')
        self.frame_options1 = Frame(self.window)

        self.label_size_line = Label(self.frame_options1, text = 'Size type lines')
        self.entry_size_line = FloatEntry(self.frame_options1)
        self.entry_size_line.insert(0, gui.parent.stipple_size)

        self.frame_options1.grid(row = 0, column = 0, sticky = 'w')
        self.label_size_line.grid(row = 0, column = 0, sticky = 'w')
        self.entry_size_line.grid(row = 0, column = 1, sticky = 'w')
        self.frame_buttons.grid(row = 1, column = 0, sticky = 'e')

    def apply_p(self, event = None):
        size_line = self.entry_size_line.get()
        if size_line < 0:
            size_line = -float(size_line)
        if size_line >= 0:
            gui.parent.stipple_size = float(size_line)
            s = gui.combo_s.get()
            stipple = gui.stipples[s]
            if stipple:
                stipple = map(lambda x: x*gui.parent.stipple_size, stipple)
            gui.parent.stipple = stipple


    def exitMethod(self, event = None):
        self.window.destroy()
        gui.d_opt3_off_on = False

class Text_options(Options):
    def __init__(self):
        Options.__init__(self)
        gui.d_opt4_off_on = True
        self.window.title('Text options')
        self.frame_options1 = Frame(self.window)

        self.select = 0
        def select_type_font(event):
            self.select = 1

        self.label_s_s = Label(self.frame_options1, text = 'Letters distance factor')
        self.entry_s_s = FloatEntry(self.frame_options1)
        self.entry_s_s.insert(0, gui.parent.s_s)

        self.label_w_text = Label(self.frame_options1, text = 'Width of letters factor')
        self.entry_w_text = FloatEntry(self.frame_options1)
        self.entry_w_text.insert(0, gui.parent.w_text)

        self.label_type_font = Label(self.frame_options1, text = 'Font')
        self.combo_type_font = ttk.Combobox(self.frame_options1, values = ['Architectural',
                                                                            'Simular TXT'], width = 15, state='readonly')
        if gui.parent.font == 'Architectural':
            self.combo_type_font.set('Architectural')
        elif gui.parent.font == 'Simular TXT':
            self.combo_type_font.set('Simular TXT')
        self.combo_type_font.bind("<<ComboboxSelected>>", select_type_font)

        #Упаковщик
        self.frame_options1.grid(row = 0, column = 0, sticky = 'w')
        self.label_s_s.grid(row = 0, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.entry_s_s.grid(row = 0, column = 1, sticky = 'w', padx = 3, pady = 3)

        self.label_w_text.grid(row = 1, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.entry_w_text.grid(row = 1, column = 1, sticky = 'w', padx = 3, pady = 3)

        self.label_type_font.grid(row = 2, column = 0, sticky = 'w', padx = 3, pady = 3)
        self.combo_type_font.grid(row = 2, column = 1, sticky = 'w', padx = 3, pady = 3)

        self.frame_buttons.grid(row = 1, column = 0, sticky = 'e')

    def apply_p(self, event = None):
        entry_s_s = self.entry_s_s.get()
        entry_w_text = self.entry_w_text.get()
        type_font = self.combo_type_font.get()

        if self.select == 1:
            if type_font == 'Architectural':
                gui.parent.font = 'Architectural'
                #gui.parent.type_arrow = 'Arch'
            elif type_font == 'Simular TXT':
                gui.parent.font = 'Simular TXT'
                #gui.parent.type_arrow = 'Arrow'
                #entry_vr_s = 0
                #self.entry_vr_s.delete(0, END)
                #self.entry_vr_s.insert(0, str(entry_vr_s))
        gui.parent.s_s = gui.normal(entry_s_s)
        gui.parent.w_text = gui.normal(entry_w_text)
        self.select = 0

    def exitMethod(self, event = None):
        self.window.destroy()
        gui.d_opt4_off_on = False


class Object_properties(Options):
    def __init__(self):
        Options.__init__(self)
        gui.o_prop_off_on = True
        self.window.title('Object properties')
        self.frame_options1 = Frame(self.window)

        #Упаковщик
        self.frame_options1.grid(row = 0, column = 0, sticky = 'w')
        self.frame_buttons.grid(row = 1, column = 0, sticky = 'e')
        self.viewer()

    def viewer(self):
        if len(gui.parent.collection) == 1:
            c = gui.parent.collection[0]
            AL = gui.parent.ALLOBJECT
            self.param = {}

            self.label_object = Label(self.frame_options1, text = 'Object:')
            self.entry_object = Entry(self.frame_options1, width = 20)
            t = AL[c]['object'] + ' ' + c[1:]
            self.entry_object.insert(0, t)
            self.entry_object.config(state = 'readonly')
            self.label_object.grid(row = 0, column = 0, sticky = 'w', padx = 3)
            self.entry_object.grid(row = 0, column = 1, columnspan = 3, sticky = 'w', padx = 3)

            self.label_layer = Label(self.frame_options1, text = 'Layer:')
            self.entry_layer = Entry(self.frame_options1, width = 20)
            t = AL[c]['sloy']
            self.entry_layer.insert(0, t)
            self.entry_layer.config(state = 'readonly')
            self.label_layer.grid(row = 1, column = 0, sticky = 'w', padx = 3)
            self.entry_layer.grid(row = 1, column = 1, columnspan = 3, sticky = 'w', padx = 3)

            self.label_col = Label(self.frame_options1, text = 'Color:')
            self.label_col2 = Label(self.frame_options1, text = '                 ', bg = AL[c]['fill'])
            self.combo_col = ttk.Combobox(self.frame_options1, values = gui.colores, width = 8, state='readonly')
            self.combo_col.set(AL[c]['fill'])
            self.label_col.grid(row = 2, column = 0, sticky = 'w', padx = 3)
            self.label_col2.grid(row = 2, column = 1, sticky = 'w', padx = 3)
            self.combo_col.grid(row = 2, column = 2, sticky = 'w', padx = 3)
            self.combo_col.bind("<<ComboboxSelected>>", lambda x: self.label_col2.config(bg = self.combo_col.get()))
            self.param['fill'] = self.combo_col
            if c[0] in ('L', 'a', 'c'):
                self.label_w = Label(self.frame_options1, text = 'Width:')
                self.combo_w = ttk.Combobox(self.frame_options1, values = ["1",
                                                               "2",
                                                               "3",
                                                               "4"], width = 20, state='readonly')
                self.combo_w.set(AL[c]['width'])
                self.label_w.grid(row = 3, column = 0, sticky = 'w', padx = 3)
                self.combo_w.grid(row = 3, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                self.param['width'] = self.combo_w
                if c[0] == 'L':
                    self.label_stip = Label(self.frame_options1, text = 'Type line:')
                    self.combo_stip = ttk.Combobox(self.frame_options1, values = gui.stipples.keys(), width = 20, state='readonly')
                    #if AL[c]['stipple']:
                    for i in gui.stipples:
                        #if gui.stipples[i]:
                            
                            #t = map(lambda x: x*float(AL[c]['factor_stip']), gui.stipples[i])
                        print (i, AL[c]['stipple'], gui.stipples[i])
                        if gui.stipples[i] == AL[c]['stipple']:
                            stip = i
                            break
                    #else:
                        #stip = '_____________'
                    self.combo_stip.set(stip)
                    self.label_stip.grid(row = 4, column = 0, sticky = 'w', padx = 3)
                    self.combo_stip.grid(row = 4, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                    self.param['stipple'] = self.combo_stip

                    self.label_stip_size = Label(self.frame_options1, text = 'Size line type:')
                    self.entry_stip_size = FloatEntry(self.frame_options1, width = 20)
                    t = float(AL[c]['factor_stip'])
                    self.entry_stip_size.insert(0, t)
                    self.label_stip_size.grid(row = 5, column = 0, sticky = 'w', padx = 3)
                    self.entry_stip_size.grid(row = 5, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                    self.param['factor_stip'] = self.entry_stip_size
                elif c[0] in ('a', 'c'):
                    self.label_R = Label(self.frame_options1, text = 'Radius:')
                    self.entry_R = FloatEntry(self.frame_options1, width = 20)
                    t = "%.2f" % float(AL[c]['R'])
                    self.entry_R.insert(0, t)
                    self.label_R.grid(row = 4, column = 0, sticky = 'w', padx = 3)
                    self.entry_R.grid(row = 4, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                    self.param['R'] = self.entry_R
                    if c[0] == 'a':
                        self.label_start = Label(self.frame_options1, text = 'Start angle:')
                        self.entry_start = FloatEntry(self.frame_options1, width = 20)
                        t = AL[c]['start']
                        self.entry_start.insert(0, t)
                        self.label_start.grid(row = 5, column = 0, sticky = 'w', padx = 3)
                        self.entry_start.grid(row = 5, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                        self.param['start'] = self.entry_start

                        self.label_extent = Label(self.frame_options1, text = 'Extent angle:')
                        self.entry_extent = FloatEntry(self.frame_options1, width = 20)
                        t = AL[c]['extent']
                        self.entry_extent.insert(0, t)
                        self.label_extent.grid(row = 6, column = 0, sticky = 'w', padx = 3)
                        self.entry_extent.grid(row = 6, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                        self.param['extent'] = self.entry_extent
            elif c[0] in ('t', 'd', 'r'):
                self.label_angle = Label(self.frame_options1, text = 'Angle:')
                self.entry_angle = FloatEntry(self.frame_options1, width = 20)
                t = float(AL[c]['angle'])*180.0/pi
                self.entry_angle.insert(0, t)
                self.label_angle.grid(row = 3, column = 0, sticky = 'w', padx = 3)
                self.entry_angle.grid(row = 3, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                self.param['angle'] = self.entry_angle

                self.label_text = Label(self.frame_options1, text = 'Text:')
                self.entry_text = Entry(self.frame_options1, width = 20)
                t = AL[c]['text']
                if t == None:
                    t = ''
                self.entry_text.insert(0, t)
                self.label_text.grid(row = 4, column = 0, sticky = 'w', padx = 3)
                self.entry_text.grid(row = 4, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                self.param['text'] = self.entry_text

                self.label_size = Label(self.frame_options1, text = 'Size:')
                self.entry_size = FloatEntry(self.frame_options1, width = 20)
                t = float(AL[c]['size']) / -100.0
                self.entry_size.insert(0, t)
                self.label_size.grid(row = 5, column = 0, sticky = 'w', padx = 3)
                self.entry_size.grid(row = 5, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                self.param['size'] = self.entry_size

                self.label_s_s = Label(self.frame_options1, text = 'Letter distanse:')
                self.entry_s_s = FloatEntry(self.frame_options1, width = 20)
                if c[0] in ('d', 'r'):
                    t1 = AL[c]['s_s_dim']
                    t2 = AL[c]['w_text_dim']
                    t3 = AL[c]['font_dim']
                else:
                    t1 = AL[c]['s_s']
                    t2 = AL[c]['w_text']
                    t3 = AL[c]['font']
                t1 = "%.2f" % float(t1)
                t2 = "%.2f" % float(t2)

                self.entry_s_s.insert(0, t1)
                self.label_s_s.grid(row = 6, column = 0, sticky = 'w', padx = 3)
                self.entry_s_s.grid(row = 6, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                self.param['s_s'] = self.entry_s_s

                self.label_w_text = Label(self.frame_options1, text = 'Width of letters:')
                self.entry_w_text = FloatEntry(self.frame_options1, width = 20)
                self.entry_w_text.insert(0, t2)
                self.label_w_text.grid(row = 7, column = 0, sticky = 'w', padx = 3)
                self.entry_w_text.grid(row = 7, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                self.param['w_text'] = self.entry_w_text

                self.label_font = Label(self.frame_options1, text = 'Font:')
                self.combo_font = ttk.Combobox(self.frame_options1, values = ['Architectural',
                                                                            'Simular TXT'], width = 20, state='readonly')
                self.combo_font.set(t3)
                self.label_font.grid(row = 8, column = 0, sticky = 'w', padx = 3)
                self.combo_font.grid(row = 8, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                self.param['font'] = self.combo_font

                if c[0] == 't':
                    self.label_anchor = Label(self.frame_options1, text = 'Anchor:')
                    self.entry_anchor = Entry(self.frame_options1, width = 20)
                    t = AL[c]['anchor']
                    self.entry_anchor.insert(0, t)
                    self.label_anchor.grid(row = 9, column = 0, sticky = 'w', padx = 3)
                    self.entry_anchor.grid(row = 9, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                    self.param['anchor'] = self.entry_anchor

                elif c[0] in ('d', 'r'):
                    self.label_s = Label(self.frame_options1, text = 'Ofset from origin:')
                    self.entry_s = FloatEntry(self.frame_options1, width = 20)
                    t = "%.2f" % float(AL[c]['s'])
                    self.entry_s.insert(0, t)
                    self.label_s.grid(row = 9, column = 0, sticky = 'w', padx = 3)
                    self.entry_s.grid(row = 9, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                    self.param['s'] = self.entry_s

                    self.label_vr_s = Label(self.frame_options1, text = 'Extend ticks:')
                    self.entry_vr_s = FloatEntry(self.frame_options1, width = 20)
                    t = "%.2f" % float(AL[c]['vr_s'])
                    self.entry_vr_s.insert(0, t)
                    self.label_vr_s.grid(row = 10, column = 0, sticky = 'w', padx = 3)
                    self.entry_vr_s.grid(row = 10, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                    self.param['vr_s'] = self.entry_vr_s

                    self.label_arrow_s = Label(self.frame_options1, text = 'Arrowhead:')
                    self.entry_arrow_s = FloatEntry(self.frame_options1, width = 20)
                    t = "%.2f" % float(AL[c]['arrow_s'])
                    self.entry_arrow_s.insert(0, t)
                    self.label_arrow_s.grid(row = 11, column = 0, sticky = 'w', padx = 3)
                    self.entry_arrow_s.grid(row = 11, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                    self.param['arrow_s'] = self.entry_arrow_s

                    self.label_arrow = Label(self.frame_options1, text = 'Arrow type:')
                    self.combo_arrow = ttk.Combobox(self.frame_options1, values = ['Architectural ticks',
                                                                                'Arrow'], width = 20, state='readonly')
                    t = AL[c]['type_arrow']
                    if t == 'Arch':
                        t = 'Architectural ticks'
                    self.combo_arrow.set(t)
                    self.label_arrow.grid(row = 12, column = 0, sticky = 'w', padx = 3)
                    self.combo_arrow.grid(row = 12, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                    self.param['type_arrow'] = self.combo_arrow

                    if c[0] == 'd':
                        self.label_vv_s = Label(self.frame_options1, text = 'Extend dim lines:')
                        self.entry_vv_s = FloatEntry(self.frame_options1, width = 20)
                        t = "%.2f" % float(AL[c]['vv_s'])
                        self.entry_vv_s.insert(0, t)
                        self.label_vv_s.grid(row = 13, column = 0, sticky = 'w', padx = 3)
                        self.entry_vv_s.grid(row = 13, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                        self.param['vv_s'] = self.entry_vv_s
                    else:
                        self.label_R = Label(self.frame_options1, text = 'Radius:')
                        self.entry_R = FloatEntry(self.frame_options1, width = 20)
                        t = "%.2f" % float(AL[c]['R'])
                        self.entry_R.insert(0, t)
                        self.label_R.grid(row = 13, column = 0, sticky = 'w', padx = 3)
                        self.entry_R.grid(row = 13, column = 1, columnspan = 3, sticky = 'w', padx = 3)
                        self.param['Rn'] = self.entry_R

        else:
            self.frame_options1.destroy()
            self.frame_options1 = Frame(self.window)
            self.frame_options1.grid(row = 0, column = 0, sticky = 'w')

    def apply_p(self, event = None):
        if len(gui.parent.collection) == 1:
            AL = gui.parent.ALLOBJECT
            c = gui.parent.collection[0]
            params = {}

            for i in self.param:
                e = self.param[i].get()
                if c[0] in ('d', 'r'):
                    if i == 's_s':
                        params['s_s_dim'] = e
                    elif i == 'w_text':
                        params['w_text_dim'] = e
                    elif i == 'font':
                        params['font_dim'] = e
                elif c[0] == 'L':
                    if i == 'factor_stip':
                        params['factor_stip'] = float(e)
                    elif i == 'stipple':
                        stip = gui.stipples[e]
                        params[i] = stip
                    continue
                        #if stip:
                            #params[i] = map(lambda x: x*float(self.param['factor_stip'].get()), stip)
                if e == '':
                    params[i] = AL[c][i]
                    continue
                if i == 'size':
                    size = float(e) * -100.0
                    params[i] = size
                elif i == 'angle':
                    angle = float(e)*pi/180.0
                    params[i] = angle
                elif i == 'type_arrow':
                    if e == 'Architectural ticks':
                        params[i] = 'Arch'
                    else:
                        params[i] = 'Arrow'
                elif i == 'R':
                    params[i] = gui.parent.coordinator2(float(e))
                elif i == 'Rn':
                    params['R'] = float(e)
                else:
                    params[i] = e

            gui.parent.c.delete('C' + gui.parent.collection[0])
            gui.parent.param_edit(params)
            select_clone.Select_clone([gui.parent.collection[0],], gui.parent)




    def exitMethod(self, event = None):
        self.window.destroy()
        gui.o_prop_off_on = False
        gui.o_prop = None
        gui.command.focus_set()

