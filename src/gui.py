# -*- coding: utf-8 -*-
import src.line as line
import src.text_line as text_line

import src.copy_object as copy_object
import src.move_object as move_object
import src.mirror_object as mirror_object
import src.rotate_object as rotate_object
import src.trim_extend as trim_extend

import src.print_to_file as print_to_file
import src.save_file as save_file
import src.open_file as open_file

import wx
from wx.lib.masked import NumCtrl
from wx.glcanvas import GLCanvas
import OpenGL.GL
import os
appPath = os.getcwd()

class Window(wx.Frame):
    def __init__(self, parent, title, par):
        self.par = par
        self.print_dialog = None
        self.print_dialog_on = False

        self.hot_keys_dict = {
            'Z' : copy_object,
            'X' : mirror_object,
            'A' : move_object,
            'S' : rotate_object,
            }
        
        wx.Frame.__init__(self, parent, -1, title = title)
        #self.sizer_panel = wx.BoxSizer()
        #self.sizer_panel.Add(self.panel)
        self.icon = wx.Icon(os.path.join(appPath, 'res', 'icon2.gif'), wx.BITMAP_TYPE_GIF)
        self.SetIcon(self.icon)
        
        self.SetSize((800, 640))

        self.menubar = wx.MenuBar()
        menu = wx.Menu()
        self.open_p = menu.Append(wx.ID_OPEN, "&Open")
        self.save_p = menu.Append(wx.ID_SAVEAS, "&Save as")
        self.print_p = menu.Append(wx.ID_PRINT, "&Print\tCtrl+P")
        #aboutItem = menu.Append(wx.ID_ABOUT,"About")
        self.exit_p = menu.Append(wx.ID_ANY,"&Exit")
        bar = wx.MenuBar()
        bar.Append(menu,"File")
        self.SetMenuBar(bar)
        self.Bind(wx.EVT_MENU, self.OnOpen, self.open_p)
        self.Bind(wx.EVT_MENU, self.OnSave, self.save_p)
        self.Bind(wx.EVT_MENU, self.OnPrint, self.print_p)
        #self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.OnExit, self.exit_p)
        
        self.sizer_parent = wx.BoxSizer(wx.VERTICAL)

        self.sizer_toolbar = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_top = wx.BoxSizer(wx.HORIZONTAL)
        #self.sizer_bot = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_cmd = wx.BoxSizer(wx.VERTICAL)#(wx.HORIZONTAL)
        self.sizer_flags = wx.BoxSizer(wx.HORIZONTAL)

        #Тулбар
        self.image_save = wx.Image(os.path.join(appPath, 'res', 'saveas.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_save = wx.BitmapButton(self, wx.NewId(), self.image_save)
        self.sizer_toolbar.Add(self.button_save)
        self.button_save.Bind(wx.EVT_BUTTON, self.OnSave)

        self.image_open = wx.Image(os.path.join(appPath, 'res', 'open.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_open = wx.BitmapButton(self, wx.NewId(), self.image_open)
        self.sizer_toolbar.Add(self.button_open)
        self.button_open.Bind(wx.EVT_BUTTON, self.OnOpen)
        
        self.color_pick = wx.ColourPickerCtrl(self)
        self.color_pick.SetColour((255, 255, 255))
        self.sizer_toolbar.Add(self.color_pick, flag = wx.ALL, border = 4)
        self.color_pick.Bind(wx.EVT_COLOURPICKER_CHANGED, self.color)

        self.image_width = wx.Image(os.path.join(appPath, 'res', 'width.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.static_i_width = wx.StaticBitmap(self, -1, self.image_width)
        self.combo_width = wx.ComboBox(
                                    self,
                                    choices = self.par.widthes,
                                    style = wx.CB_READONLY,
                                    size = (60, -1)
                                    )
        self.combo_width.SetSelection(self.par.widthes.index(str(self.par.width)))
        self.sizer_toolbar.Add(self.static_i_width, flag = wx.ALL, border = 4)
        self.sizer_toolbar.Add(self.combo_width, flag = wx.ALL, border = 4)
        self.combo_width.Bind(wx.EVT_COMBOBOX, self.width)

        self.combo_stipple = wx.ComboBox(
                                    self,
                                    choices = self.par.stipples_list,
                                    style = wx.CB_READONLY,
                                    size = (130, -1)
                                    )
        self.combo_stipple.SetSelection(0)
        self.sizer_toolbar.Add(self.combo_stipple, flag = wx.ALL, border = 4)
        self.combo_stipple.Bind(wx.EVT_COMBOBOX, self.stipple)

        self.image_text_size = wx.Image(os.path.join(appPath, 'res', 'h_text.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.static_text_size = wx.StaticBitmap(self, -1, self.image_text_size)
        self.text_size_ctrl = wx.lib.masked.NumCtrl(
                                    self,
                                    style = wx.TE_PROCESS_ENTER,
                                    fractionWidth = 2,
                                    size = (80, -1),
                                    autoSize = False,
                                    )
        self.text_size_ctrl.SetValue(self.par.text_size/100.0)
        self.sizer_toolbar.Add(self.static_text_size, flag = wx.ALL, border = 4)
        self.sizer_toolbar.Add(self.text_size_ctrl, flag = wx.ALL, border = 4)
        self.text_size_ctrl.Bind(wx.EVT_KILL_FOCUS, self.size_text)
        self.text_size_ctrl.Bind(wx.EVT_KEY_DOWN, self.size_text_enter)

        self.image_dim_text_size = wx.Image(os.path.join(appPath, 'res', 'h_dim.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.static_dim_text_size = wx.StaticBitmap(self, -1, self.image_dim_text_size)
        self.dim_text_size_ctrl = wx.lib.masked.NumCtrl(
                                    self,
                                    style = wx.TE_PROCESS_ENTER,
                                    fractionWidth = 2,
                                    size = (80, -1),
                                    autoSize = False,
                                    )
        self.dim_text_size_ctrl.SetValue(self.par.dim_text_size/100.0)
        self.sizer_toolbar.Add(self.static_dim_text_size, flag = wx.ALL, border = 4)
        self.sizer_toolbar.Add(self.dim_text_size_ctrl, flag = wx.ALL, border = 4)
        self.dim_text_size_ctrl.Bind(wx.EVT_KILL_FOCUS, self.dim_size_text)
        self.dim_text_size_ctrl.Bind(wx.EVT_KEY_DOWN, self.dim_size_text_enter)

        #Создаем GLCanvas и запихиваем его в сайзер
        self.canvas = myGLCanvas(self)
        self.canvas.SetMinSize((200, 200))
        self.sizer_canvas = wx.BoxSizer()       
        self.sizer_canvas.Add (self.canvas, 1, flag = wx.EXPAND)

        #Левая колонка кнопок
        self.sizer_buttons_left = wx.BoxSizer(wx.VERTICAL)
        
        self.image_line = wx.Image(os.path.join(appPath, 'res', 'line2.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_line = wx.BitmapButton(self, wx.NewId(), self.image_line)
        self.sizer_buttons_left.Add(self.button_line)
        self.button_line.Bind(wx.EVT_BUTTON, self.line)

        self.image_circle = wx.Image(os.path.join(appPath, 'res', 'circle2.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_circle = wx.BitmapButton(self, wx.NewId(), self.image_circle)
        self.sizer_buttons_left.Add(self.button_circle)

        self.image_arc = wx.Image(os.path.join(appPath, 'res', 'arc2.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_arc = wx.BitmapButton(self, wx.NewId(), self.image_arc)
        self.sizer_buttons_left.Add(self.button_arc)

        self.image_dim = wx.Image(os.path.join(appPath, 'res', 'dim2.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_dim = wx.BitmapButton(self, wx.NewId(), self.image_dim)
        self.sizer_buttons_left.Add(self.button_dim)

        self.image_dimR = wx.Image(os.path.join(appPath, 'res', 'radius.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_dimR = wx.BitmapButton(self, wx.NewId(), self.image_dimR)
        self.sizer_buttons_left.Add(self.button_dimR)

        self.image_text = wx.Image(os.path.join(appPath, 'res', 'text2.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_text = wx.BitmapButton(self, wx.NewId(), self.image_text)
        self.sizer_buttons_left.Add(self.button_text)
        self.button_text.Bind(wx.EVT_BUTTON, self.text)

        #Правая колонка кнопок
        self.sizer_buttons_right = wx.BoxSizer(wx.VERTICAL)

        self.image_copy = wx.Image(os.path.join(appPath, 'res', 'copy2.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_copy = wx.BitmapButton(self, wx.NewId(), self.image_copy)
        self.sizer_buttons_right.Add(self.button_copy)
        self.button_copy.Bind(wx.EVT_BUTTON, self.copy)

        self.image_move = wx.Image(os.path.join(appPath, 'res', 'move2.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_move = wx.BitmapButton(self, wx.NewId(), self.image_move)
        self.sizer_buttons_right.Add(self.button_move)
        self.button_move.Bind(wx.EVT_BUTTON, self.move)

        self.image_mir = wx.Image(os.path.join(appPath, 'res', 'mirror2.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_mir = wx.BitmapButton(self, wx.NewId(), self.image_mir)
        self.sizer_buttons_right.Add(self.button_mir)
        self.button_mir.Bind(wx.EVT_BUTTON, self.mirror)

        self.image_rot = wx.Image(os.path.join(appPath, 'res', 'rotate2.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_rot = wx.BitmapButton(self, wx.NewId(), self.image_rot)
        self.sizer_buttons_right.Add(self.button_rot)
        self.button_rot.Bind(wx.EVT_BUTTON, self.rotate)

        self.image_offset = wx.Image(os.path.join(appPath, 'res', 'offset2.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_offset = wx.BitmapButton(self, wx.NewId(), self.image_offset)
        self.sizer_buttons_right.Add(self.button_offset)

        self.image_copy_p = wx.Image(os.path.join(appPath, 'res', 'copy_p2.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_copy_p = wx.BitmapButton(self, wx.NewId(), self.image_copy_p)
        self.sizer_buttons_right.Add(self.button_copy_p)

        self.image_fillet = wx.Image(os.path.join(appPath, 'res', 'fillet2.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_fillet = wx.BitmapButton(self, wx.NewId(), self.image_fillet)
        self.sizer_buttons_right.Add(self.button_fillet)

        self.image_trim = wx.Image(os.path.join(appPath, 'res', 'trim2.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_trim = wx.BitmapButton(self, wx.NewId(), self.image_trim)
        self.sizer_buttons_right.Add(self.button_trim)
        self.button_trim.Bind(wx.EVT_BUTTON, self.trim)

        self.image_extend = wx.Image(os.path.join(appPath, 'res', 'extend2.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_extend = wx.BitmapButton(self, wx.NewId(), self.image_extend)
        self.sizer_buttons_right.Add(self.button_extend)
        self.button_extend.Bind(wx.EVT_BUTTON, self.extend)

        self.image_scale = wx.Image(os.path.join(appPath, 'res', 'scale.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_scale = wx.BitmapButton(self, wx.NewId(), self.image_scale)
        self.sizer_buttons_right.Add(self.button_scale)

        self.image_trim_dim = wx.Image(os.path.join(appPath, 'res', 'chain_dim.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_trim_dim = wx.BitmapButton(self, wx.NewId(), self.image_trim_dim)
        self.sizer_buttons_right.Add(self.button_trim_dim)
        
        # Собираем сайзеры в top
        self.sizer_top.Add(self.sizer_buttons_left,  flag = wx.ALIGN_LEFT)
        self.sizer_top.Add(self.sizer_canvas, 1, flag = wx.EXPAND)
        self.sizer_top.Add(self.sizer_buttons_right,  flag = wx.ALIGN_RIGHT)

        # Командная строка и кнопки снизу
        self.sizer_info_cmd = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_info = wx.BoxSizer(wx.VERTICAL)
        self.info = wx.TextCtrl(self, -1, 'Command:', size = (150, -1), style = wx.TE_READONLY | wx.BORDER_NONE)
        self.info.SetBackgroundColour((214, 210, 208))
        self.sizer_info_cmd.Add(self.info)
     
        self.cmd = wx.TextCtrl(self, -1, '', size = (900, -1))
        self.sizer_info_cmd.Add(self.cmd)

        self.info2 = wx.TextCtrl(self, -1, '', size = (400, -1), style = wx.TE_READONLY | wx.BORDER_NONE)
        self.info2.SetBackgroundColour((214, 210, 208))
        self.sizer_info.Add(self.info2)
        
        self.sizer_cmd.Add(self.sizer_info_cmd)
        self.sizer_cmd.Add(self.sizer_info)

        self.button_ortho = wx.Button(self, wx.NewId(), 'Ortho')
        self.blue_reder(self.button_ortho, self.par.ortoFlag)
        #self.button_ortho.SetBackgroundColour("White")
        #self.button_ortho.SetForegroundColour("Black")
        #self.button_ortho.SetBackgroundColour("Blue")
        #self.button_ortho.SetForegroundColour("Red")
        self.sizer_flags.Add(self.button_ortho)

        self.button_trace = wx.Button(self, wx.NewId(), 'Trace')
        self.blue_reder(self.button_trace, self.par.trace_flag)
        #self.button_trace.SetBackgroundColour("White")
        #self.button_trace.SetForegroundColour("Black")
        self.sizer_flags.Add(self.button_trace)
        self.button_trace.Bind(wx.EVT_BUTTON, self.trace_off_on)

        self.button_trace_obj = wx.Button(self, wx.NewId(), 'Object trace')
        self.blue_reder(self.button_trace_obj, self.par.trace_obj_flag)
        #self.button_trace_obj.SetBackgroundColour("White")
        #self.button_trace_obj.SetForegroundColour("Black")
        self.sizer_flags.Add(self.button_trace_obj)

        self.button_snap_N = wx.Button(self, wx.NewId(), 'Snap near')
        self.blue_reder(self.button_snap_N, self.par.snap_near)
        #self.button_snap_N.SetBackgroundColour("White")
        #self.button_snap_N.SetForegroundColour("Black")
        self.sizer_flags.Add(self.button_snap_N)
        self.button_snap_N.Bind(wx.EVT_BUTTON, self.snap_N_off_on)

        # Собираем сайзеры в parent
        self.sizer_parent.Add(self.sizer_toolbar, flag = wx.ALIGN_TOP)
        self.sizer_parent.Add(self.sizer_top, 1, flag = wx.ALIGN_TOP | wx.EXPAND)
        self.sizer_parent.Add(self.sizer_cmd, flag = wx.ALIGN_BOTTOM) #| wx.ALL, border = 4)
        self.sizer_parent.Add(self.sizer_flags, flag = wx.ALIGN_BOTTOM)
        
        self.SetAutoLayout(True)
        self.SetSizer(self.sizer_parent)

        
# ОБРАБОТЧИКИ ТУЛБАРА
        
    def color(self, e):
        RGB = e.GetColour().Get()
        if RGB == (0, 0, 0):
            RGB = (255, 255, 255)
            self.color_pick.SetColour(RGB)
        self.par.color = list(RGB)
        e.Skip()

    def width(self, e):
        line_width = e.GetString()
        self.par.width = int(line_width)
        e.Skip()

    def stipple(self, e):
        self.par.stipple = self.par.stipples[e.GetString()]
        e.Skip()

    def size_text(self, e):
        self.par.text_size = self.text_size_ctrl.GetValue()*100.0
        e.Skip()

    def size_text_enter(self, e):
        key =  e.GetKeyCode()
        if key == wx.WXK_RETURN:
            self.size_text(e)
        e.Skip()

    def dim_size_text(self, e):
        self.par.dim_text_size = self.dim_text_size_ctrl.GetValue()*100.0
        e.Skip()

    def dim_size_text_enter(self, e):
        key =  e.GetKeyCode()
        if key == wx.WXK_RETURN:
            self.dim_size_text(e)
        e.Skip()
            

# ОБРАБОТЧИКИ КНОПОК СЛЕВА
    def line(self, e):
        self.par.action(line.Line)
        self.par.focus_cmd()

    def text(self, e):
        self.par.action(text_line.Object)
        self.par.focus_cmd()

# ОБРАБОТЧИКИ КНОПОК СЛЕВА
    def copy(self, e):
        self.par.action(copy_object.Object)
        self.par.focus_cmd()

    def move(self, e):
        self.par.action(move_object.Object)
        self.par.focus_cmd()

    def mirror(self, e):
        self.par.action(mirror_object.Object)
        self.par.focus_cmd()

    def rotate(self, e):
        self.par.action(rotate_object.Object)
        self.par.focus_cmd()

    def extend(self, e):
        self.par.trim_extend = 'Extend'
        self.par.action(trim_extend.Object)
        self.par.focus_cmd()
        
    def trim(self, e):
        self.par.trim_extend = 'Trim'
        self.par.action(trim_extend.Object)
        self.par.focus_cmd()

# ОБРАБОТЧИКИ КНОПОК СНИЗУ
    def trace_off_on(self, e):
        self.par.focus_cmd()
        if self.par.trace_flag:
            self.par.trace_flag = False
            self.par.trace_on = False
            self.par.trace_data = []
            self.par.trace_color = []
        else:
            self.par.trace_flag = True

        self.blue_reder(self.button_trace, self.par.trace_flag)

    def snap_N_off_on(self, e):
        self.par.focus_cmd()
        if self.par.snap_near:
            self.par.snap_near = False    
        else:
            self.par.snap_near = True

        self.blue_reder(self.button_snap_N, self.par.snap_near)
    
# ОБРАБОТЧИКИ МЕНЮ
    def OnPrint(self, e):
        if not self.print_dialog:
            self.print_dialog = Print_dialog(self.par)
        if not self.print_dialog_on:
            self.print_dialog.Show()
            self.print_dialog_on = True
        else:
            self.print_dialog.Hide()
            self.print_dialog_on = False
        #print_to_file.print_to(self.par)

    def OnSave(self, e):
        head, tail = os.path.split(self.par.current_save_path)
        self.file_dialog =  wx.FileDialog(self, "Save drawing", head, tail,
                                    "SVG files (*.svg)|*.svg",
                                    style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if self.file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        self.par.current_save_path = os.path.join(self.file_dialog.GetDirectory(), self.file_dialog.GetFilename())
        self.par.current_file = self.par.current_save_path
        save_file.Save_to_SVG(
                            self.par.current_file,
                            'svg',
                            self.par.ALLOBJECT,
                            self.par.layers,
                            self.par.drawing_w,
                            self.par.drawing_h,
                            )

    def OnOpen(self, e):
        print 111
        head, tail = os.path.split(self.par.current_save_path)
        self.file_dialog =  wx.FileDialog(self, "Open drawing", head, tail,
                                    "SVG files (*.svg)|*.svg",
                                    style = wx.FD_OPEN)
        if self.file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        self.par.current_save_path = os.path.join(self.file_dialog.GetDirectory(), self.file_dialog.GetFilename())
        self.par.current_file = self.par.current_save_path
        open_file.Open_from_SVG(self.par, self.par.current_file,'svg')
        
    def OnAbout(self, e):
        pass
    
       
    def OnExit(self, e):
        pass

# Изменяет цвет кнопок снизу
    def blue_reder(self, button, flag):
        if flag:
            button.SetBackgroundColour("Blue")
            button.SetForegroundColour("Red")
        else:
            button.SetBackgroundColour("White")
            button.SetForegroundColour("Black")
    

class myGLCanvas(GLCanvas):
    def __init__(self, parent):
        GLCanvas.__init__(self, parent,-1)
        self.init = False
        self.context = wx.glcanvas.GLContext(self)
        #курсор
        #self.cursor = wx.StockCursor(wx.CURSOR_CROSS)
        #self.cursor = wx.Cursor(os.path.join(appPath, 'res', 'cursor.png'), wx.BITMAP_TYPE_PNG, 64, 64)#wx.StockCursor(wx.CURSOR_POINT_LEFT)
        #self.SetCursor(self.cursor)

class Print_dialog(wx.Frame):

    title = "Print options"

    def __init__(self, par):
        self.par = par
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title = self.title, style = wx.FRAME_FLOAT_ON_PARENT)

        self.scale = [
            500,
            200,
            100,
            50,
            25,
            15,
            10,
            5,
            1,
            ]
        self.text_scale = ['1:%s' %x for x in self.scale]
        self.dict_scale = dict(('1:%s' %x, x) for x in self.scale)

        self.format = [
            'PDF',
            'PNG',
            'GIF',
            'JPEG',
            'BMP',
            ]
        #print self.text_scales
        self.SetSize((530, 100))
        self.sizer_top = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_bot = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.text1 = wx.StaticText(self, -1, 'Scale:')
        self.sizer_top.Add(self.text1, flag = wx.ALIGN_CENTER | wx.ALL, border = 4)

        self.combo_scale = wx.ComboBox(
                                    self,
                                    choices = self.text_scale,
                                    style = wx.CB_READONLY,
                                    size = (130, -1)
                                    )
        self.combo_scale.SetValue('1:1')
        self.sizer_top.Add(self.combo_scale, flag = wx.ALIGN_CENTER | wx.ALL, border = 4)

        self.text2 = wx.StaticText(self, -1, 'Format:')
        self.sizer_top.Add(self.text2, flag = wx.ALIGN_CENTER | wx.ALL, border = 4)

        self.combo_format = wx.ComboBox(
                                    self,
                                    choices = self.format,
                                    style = wx.CB_READONLY,
                                    size = (130, -1)
                                    )
        self.combo_format.SetValue('PDF')
        self.sizer_top.Add(self.combo_format, flag = wx.ALIGN_CENTER | wx.ALL, border = 4)

        self.button_area = wx.Button(self, wx.NewId(), 'Select print area')
        self.sizer_top.Add(self.button_area, flag = wx.ALIGN_CENTER | wx.ALL, border = 4)
        self.button_area.Bind(wx.EVT_BUTTON, self.OnArea)

        self.dir = wx.TextCtrl(self, -1, self.par.current_print_file, size = (200, -1))
        self.sizer_bot.Add(self.dir, flag = wx.ALIGN_CENTER)

        self.button_dir = wx.Button(self, wx.NewId(), 'Choose')
        self.sizer_bot.Add(self.button_dir, flag = wx.ALIGN_CENTER | wx.ALL, border = 4)
        self.button_dir.Bind(wx.EVT_BUTTON, self.choose_dir)

        self.button_print = wx.Button(self, wx.NewId(), 'Print')
        self.sizer_bot.Add(self.button_print, flag = wx.ALIGN_CENTER | wx.ALL, border = 4)
        self.button_print.Bind(wx.EVT_BUTTON, self.Print)

        self.sizer.Add(self.sizer_top)
        self.sizer.Add(self.sizer_bot, flag = wx.ALIGN_CENTER)
        self.SetSizer(self.sizer)

    def OnArea(self, e):
        self.par.action(print_to_file.Select_area)

    def choose_dir(self, e):
        head, tail = os.path.split(self.par.current_print_file)
        file_format = self.combo_format.GetValue()
        self.file_dialog =  wx.FileDialog(self, "Print file", head, tail,
                                    "%s files (*.%s)|*.%s"%(file_format, file_format.lower(), file_format.lower()),
                                    style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if self.file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        self.par.current_print_file = os.path.join(self.file_dialog.GetDirectory(), self.file_dialog.GetFilename())
        self.dir.SetValue(self.par.current_print_file)
        

    def Print(self, e):
        if self.par.print_rect:
            scale = self.dict_scale[self.combo_scale.GetValue()]
            file_format = self.combo_format.GetValue()
            file_name = self.dir.GetValue()
            print_to_file.print_to(self.par, self.par.print_rect, self.par.ALLOBJECT, scale, file_format, file_name) 
                               

    
        
        
    
