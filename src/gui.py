# -*- coding: utf-8 -*-
import src.line as line
import src.text_line as text_line
import src.dimension as dimension
import src.circle as circle
import src.arc as arc

import src.copy_object as copy_object
import src.move_object as move_object
import src.mirror_object as mirror_object
import src.rotate_object as rotate_object
import src.trim_extend as trim_extend
import src.copy_prop as copy_prop
import src.edit_prop as edit_prop
import src.trim_dim_line as trim_dim_line
import src.scale_object as scale_object
import src.fillet as fillet


import src.print_to_file as print_to_file
import src.save_file as save_file
import src.open_file as open_file
import src.dxf_library.dxf_write as dxf_write
import src.dxf_library.dxf_read as dxf_read
import src.dxf_library.color_acad_rgb as color_acad_rgb

import wx
from wx.lib.masked import NumCtrl
from wx.glcanvas import GLCanvas
import os
import math
appPath = os.getcwd()

class Window(wx.Frame):
    def __init__(self, parent, title, par):
        self.par = par

#Dialogs
        self.print_dialog = None
        self.print_dialog_on = False

        self.dimstyle_dialog = None
        self.dimstyle_dialog_on = False

        self.line_dialog = None
        self.line_dialog_on = False

        self.text_style_dialog = None
        self.text_style_dialog_on = False

        self.hot_keys_dict = {
            'Z' : copy_object.Object,
            'X' : mirror_object.Object,
            'A' : move_object.Object,
            'S' : rotate_object.Object,
            'Q' : trim_extend.Trim,
            'W' : trim_extend.Extend,
            'D' : copy_prop.Copy_prop,
            }
        
        wx.Frame.__init__(self, parent, -1, title = title)
        self.SetBackgroundColour((214, 210, 208))
        #self.sizer_panel = wx.BoxSizer()
        #self.sizer_panel.Add(self.panel)
        self.icon = wx.Icon(os.path.join(appPath, 'res', 'icon2.gif'), wx.BITMAP_TYPE_GIF)
        self.SetIcon(self.icon)
        
        self.SetSize((800, 640))

        self.menubar = wx.MenuBar()
        
        menu_file = wx.Menu()
        self.open_p = menu_file.Append(wx.ID_OPEN, "&Open")
        self.save_p = menu_file.Append(wx.ID_SAVEAS, "&Save as")
        self.print_p = menu_file.Append(wx.ID_PRINT, "&Print\tCtrl+P")
        self.exit_p = menu_file.Append(wx.ID_ANY,"&Exit")

        menu_format = wx.Menu()
        self.dim_style_p = menu_format.Append(-1, "Dimension style")
        self.line_p = menu_format.Append(-1, "Line options")
        self.text_style_p = menu_format.Append(-1, "Text style")
        
        bar = wx.MenuBar()
        bar.Append(menu_file,"File")
        bar.Append(menu_format,"Format")
        self.SetMenuBar(bar)
        
        self.Bind(wx.EVT_MENU, self.OnOpen, self.open_p)
        self.Bind(wx.EVT_MENU, self.OnSave, self.save_p)
        self.Bind(wx.EVT_MENU, self.OnPrint, self.print_p)
        self.Bind(wx.EVT_MENU, self.OnExit, self.exit_p)
        
        self.Bind(wx.EVT_MENU, self.OnDimStyle, self.dim_style_p)
        self.Bind(wx.EVT_MENU, self.OnLineOpt, self.line_p)
        self.Bind(wx.EVT_MENU, self.OnTextStyle, self.text_style_p)
        
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
        self.button_circle.Bind(wx.EVT_BUTTON, self.circle)

        self.image_arc = wx.Image(os.path.join(appPath, 'res', 'arc2.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_arc = wx.BitmapButton(self, wx.NewId(), self.image_arc)
        self.sizer_buttons_left.Add(self.button_arc)
        self.button_arc.Bind(wx.EVT_BUTTON, self.arc)

        self.image_dim = wx.Image(os.path.join(appPath, 'res', 'dim2.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_dim = wx.BitmapButton(self, wx.NewId(), self.image_dim)
        self.sizer_buttons_left.Add(self.button_dim)
        self.button_dim.Bind(wx.EVT_BUTTON, self.dim)

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
        self.button_copy_p.Bind(wx.EVT_BUTTON, self.copy_prop)

        self.image_fillet = wx.Image(os.path.join(appPath, 'res', 'fillet2.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_fillet = wx.BitmapButton(self, wx.NewId(), self.image_fillet)
        self.sizer_buttons_right.Add(self.button_fillet)
        self.button_fillet.Bind(wx.EVT_BUTTON, self.fillet)

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
        self.button_scale.Bind(wx.EVT_BUTTON, self.scale)

        self.image_trim_dim = wx.Image(os.path.join(appPath, 'res', 'chain_dim.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.button_trim_dim = wx.BitmapButton(self, wx.NewId(), self.image_trim_dim)
        self.button_trim_dim.Bind(wx.EVT_BUTTON, self.trim_dim)
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
        
        norm_RGB = []
        min_dist = (2500,None)
        for dxf_color in self.par.RGB_DXF_colores:
            r1 = dxf_color[0]
            g1 = dxf_color[1]
            b1 = dxf_color[2]
            r2 = RGB[0]
            g2 = RGB[1]
            b2 = RGB[2]
            color_distanse = math.sqrt((r1-r2)**2+(g1-g2)**2+(b1-b2)**2)
            if color_distanse < min_dist[0]:
                min_dist = (color_distanse, dxf_color)

        norm_RGB = list(min_dist[1])
                        
        RGB = norm_RGB
        if RGB == [0, 0, 0]:
            RGB = [255, 255, 255]
        self.color_pick.SetColour(tuple(RGB))
        self.par.color = list(RGB)
        self.edit_prop({'color':self.par.color})
        #edit_prop.Edit_prop(self.par, {'color':self.par.color}, self.par.collection)
        self.par.focus_cmd()
        e.Skip()

    def width(self, e):
        line_width = e.GetString()
        self.par.width = int(line_width)
        self.edit_prop({'width':self.par.width})
        #edit_prop.Edit_prop(self.par, {'width':self.par.width}, self.par.collection)
        self.par.focus_cmd()
        e.Skip()

    def stipple(self, e):
        self.par.stipple = self.par.stipples[e.GetString()]
        self.edit_prop({'stipple':self.par.stipple})
        #edit_prop.Edit_prop(self.par, {'stipple':self.par.stipple}, self.par.collection)
        self.par.focus_cmd()
        e.Skip()

    def size_text(self, e):
        self.par.text_size = self.text_size_ctrl.GetValue()*100.0
        self.edit_prop({'text_size':self.par.text_size})
        #edit_prop.Edit_prop(self.par, {'text_size':self.par.text_size}, self.par.collection)
        self.par.focus_cmd()
        e.Skip()

    def size_text_enter(self, e):
        key =  e.GetKeyCode()
        if key == wx.WXK_RETURN:
            self.size_text(e)
            self.par.focus_cmd()
        e.Skip()

    def dim_size_text(self, e):
        self.par.dim_text_size = self.dim_text_size_ctrl.GetValue()*100.0
        self.edit_prop({'dim_text_size':self.par.dim_text_size})
        #edit_prop.Edit_prop(self.par, {'dim_text_size':self.par.dim_text_size}, self.par.collection)
        self.par.focus_cmd()
        e.Skip()

    def dim_size_text_enter(self, e):
        key =  e.GetKeyCode()
        if key == wx.WXK_RETURN:
            self.dim_size_text(e)
            self.par.focus_cmd()
        e.Skip()
            

# ОБРАБОТЧИКИ КНОПОК СЛЕВА
    def line(self, e):
        self.par.action(line.Line)
        self.par.focus_cmd()

    def text(self, e):
        self.par.action(text_line.Object)
        self.par.focus_cmd()

    def dim(self, e):
        self.par.action(dimension.Dimension)
        self.par.focus_cmd()

    def circle(self, e):
        self.par.action(circle.Circle)
        self.par.focus_cmd()

    def arc(self, e):
        self.par.action(arc.Arc)
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
        self.par.action(trim_extend.Extend)
        self.par.focus_cmd()
        
    def trim(self, e):
        self.par.action(trim_extend.Trim)
        self.par.focus_cmd()

    def copy_prop(self, e):
        self.par.action(copy_prop.Copy_prop)
        self.par.focus_cmd()

    def trim_dim(self, e):
        self.par.action(trim_dim_line.Object)
        self.par.focus_cmd()

    def scale(self, e):
        self.par.action(scale_object.Object)
        self.par.focus_cmd()

    def fillet(self, e):
        self.par.action(fillet.Fillet)
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
        self.print_dialog, self.print_dialog_on = self.open_show_hide(self.print_dialog, Print_dialog, self.print_dialog_on)
        

    def OnSave(self, e):
        head, tail = os.path.split(self.par.current_save_path)
        self.file_dialog =  wx.FileDialog(self, "Save drawing", head, tail,
                                    "DXF files (*.dxf)|*.dxf|SVG files (*.svg)|*.svg",
                                    style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if self.file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        direct = self.file_dialog.GetDirectory()
        file_name = self.file_dialog.GetFilename()
        self.par.current_save_path = get_path(self.par.os, direct, file_name)

        self.par.current_file = self.par.current_save_path
        name, f_format = os.path.splitext(self.par.current_save_path)
        if f_format == '.dxf':
            dxf_write.Save_to_DXF(
                            self.par,
                            self.par.current_file,
                            f_format,
                            self.par.ALLOBJECT,
                            self.par.layers,
                            self.par.stipples,
                            self.par.drawing_w,
                            self.par.drawing_h,
                            )
        else:
            save_file.Save_to_SVG(
                            self.par,
                            self.par.current_file,
                            f_format,
                            self.par.ALLOBJECT,
                            self.par.layers,
                            self.par.drawing_w,
                            self.par.drawing_h,
                            )
        print 'Save file', self.par.current_file

    def OnOpen(self, e):
        head, tail = os.path.split(self.par.current_save_path)
        self.file_dialog =  wx.FileDialog(self, "Open drawing", head, tail,
                                    "DXF files (*.dxf)|*.dxf|DXF files (*.DXF)|*.DXF|SVG files (*.svg)|*.svg",
                                    style = wx.FD_OPEN)
        if self.file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        direct = self.file_dialog.GetDirectory()
        file_name = self.file_dialog.GetFilename()
        self.par.current_save_path = get_path(self.par.os, direct, file_name)
        self.par.current_file = self.par.current_save_path
        name, f_format = os.path.splitext(self.par.current_save_path)
        f_format = f_format.lower()
        if f_format == '.dxf':
            dxf_read.Load_from_DXF(self.par, self.par.current_file)
        else:
            open_file.Open_from_SVG(self.par, self.par.current_file)    
       
    def OnExit(self, e):
        pass

    def OnDimStyle(self, e):
        self.dimstyle_dialog, self.dimstyle_dialog_on = self.open_show_hide(self.dimstyle_dialog, Dimstyle_dialog, self.dimstyle_dialog_on)

    def OnLineOpt(self, e):
        self.line_dialog, self.line_dialog_on = self.open_show_hide(self.line_dialog, Line_dialog, self.line_dialog_on)

    def OnTextStyle(self, e):
        self.text_style_dialog, self.text_style_dialog_on = self.open_show_hide(self.text_style_dialog, Text_style_dialog, self.text_style_dialog_on)

# Изменяет цвет кнопок снизу
    def blue_reder(self, button, flag):
        if flag:
            button.SetBackgroundColour("Blue")
            button.SetForegroundColour("Red")
        else:
            button.SetBackgroundColour("White")
            button.SetForegroundColour("Black")

# Смена свойств выделенных объектов при изменении глобальных параметров

    def edit_prop(self, dict_prop, get_objects = []):
        if not get_objects:
            objects = self.par.collection
        else:
            objects = get_objects
            
        new_objects = edit_prop.Edit_prop(self.par, dict_prop, objects)
        if new_objects and not get_objects:
            self.par.collection = new_objects
            self.par.kill()
            self.par.mass_collector(new_objects, 'select')
            #self.par.collectionBack = []

    def open_show_hide(self, dialog, function, key_on):
        if not dialog:
            dialog = function(self.par)
        if not key_on:
            dialog.Show()
            key_on = True
        else:
            dialog.Hide()
            key_on = False
            
        return dialog, key_on

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
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title = self.title,
                          style = wx.FRAME_FLOAT_ON_PARENT|wx.DEFAULT_FRAME_STYLE)
        self.SetBackgroundColour((214, 210, 208))
        self.Bind(wx.EVT_CLOSE, par.interface.OnPrint)
        
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
        
        direct = self.file_dialog.GetDirectory()
        file_name = self.file_dialog.GetFilename()
        self.par.current_print_file = get_path(self.par.os, direct, file_name)
        self.par.current_print_file = os.path.splitext(self.par.current_print_file)[0]#Взять без разрешения
        #print_file_base = os.path.splitext(file_name)[0] #Взять без разрешения
        #self.par.current_print_file = os.path.join(direct, print_file_base)
        self.dir.SetValue(self.par.current_print_file)
        

    def Print(self, e):
        if self.par.print_rect:
            scale = self.dict_scale[self.combo_scale.GetValue()]
            file_format = self.combo_format.GetValue()
            file_name = self.dir.GetValue()
            print_file_base = os.path.splitext(file_name)
            if not print_file_base[1]:
                file_name = file_name + '.%s' %file_format.lower()
            print_to_file.print_to(self.par, self.par.print_rect, self.par.ALLOBJECT, scale, file_format, file_name) 

class My_dialog(wx.Frame):
    def __init__(self, par, OnFunc, title, size):
        self.par = par
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title = title,
                          style = wx.FRAME_FLOAT_ON_PARENT|(wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER))
        self.SetBackgroundColour((214, 210, 208))
        self.Bind(wx.EVT_CLOSE, OnFunc)

        self.SetSize(size)

    def add_apply(self, sizer):
        self.button_apply = wx.Button(self, wx.NewId(), 'Apply')
        sizer.Add(self.button_apply)
        self.button_apply.Bind(wx.EVT_BUTTON, self.apply_style)
        

class Dimstyle_dialog(My_dialog):
    
    def __init__(self, par):
        title = "Dimension style"
        size = (550, 220)
        My_dialog.__init__(self, par, par.interface.OnDimStyle, title, size)
        
        self.staticbox = wx.StaticBox (self, wx.NewId(), label="Dimension parametrs")
        self.sizer_right = wx.StaticBoxSizer(self.staticbox, wx.HORIZONTAL)
        self.sizer_right_1 = wx.GridSizer(cols = 2)
        self.sizer_right_2 = wx.BoxSizer(wx.VERTICAL)
        
        self.sizer_left = wx.BoxSizer(wx.VERTICAL)
        
        
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        png = wx.Bitmap(os.path.join(appPath, 'res', 'dim_prop.gif'))#, wx.BITMAP_TYPE_GIF)#.ConvertToBitmap()
        r = wx.StaticBitmap(self, -1, png, (png.GetWidth(), png.GetHeight()))

        self.sizer_left.Add(r)

        
        self.text_s, self.s = stroker(self, 'Offset from dim line [A]', self.par.s, self.sizer_right_1, self.sizer_right_2)
        self.text_arrow_s, self.arrow_s = stroker(self, 'Arrowhead size [B]', self.par.arrow_s, self.sizer_right_1, self.sizer_right_2)
        self.text_vr_s, self.vr_s = stroker(self, 'Extend dim lines [C]', self.par.vr_s, self.sizer_right_1, self.sizer_right_2)
        self.text_vv_s, self.vv_s = stroker(self, 'Extend ticks [D]', self.par.vv_s, self.sizer_right_1, self.sizer_right_2)

        self.text_type_arrow, self.type_arrow = stroker(self, 'Arrowheads', self.par.type_arrow, self.sizer_right_1, self.sizer_right_2, 'combobox', ['Arch', 'Arrow'])

        
        
        
        self.add_apply(self.sizer_right_1)

        self.sizer_right.Add(self.sizer_right_1)
        #self.sizer_right.Add(self.sizer_right_2, flag = wx.EXPAND)

        
        self.sizer.Add(self.sizer_left, flag = wx.ALL, border = 8)
        self.sizer.Add(self.sizer_right, flag = wx.ALL, border = 8)
        self.SetSizer(self.sizer)

    def apply_style(self, e):
        s = float(self.s.GetValue())
        self.par.s = s
        s = float(self.arrow_s.GetValue())
        self.par.arrow_s = s
        s = float(self.vv_s.GetValue())
        self.par.vv_s = s
        s = float(self.vr_s.GetValue())
        self.par.vr_s = s
        s = self.type_arrow.GetValue()
        self.par.type_arrow = s
        
        
        print (self.par.s,
               self.par.arrow_s,
               self.par.vv_s,
               self.par.vr_s,
               self.par.type_arrow)

class Line_dialog(My_dialog):

    def __init__(self, par):
        title = "Line options"
        size = (250, 80)
        My_dialog.__init__(self, par, par.interface.OnLineOpt, title, size)       
        
        self.sizer_right_1 = wx.GridSizer(cols = 2)                

        
        self.text_factor_stipple, self.factor_stipple = stroker(self, 'Size of lile', self.par.factor_stipple, self.sizer_right_1, None)     

        self.add_apply(self.sizer_right_1)

        self.SetSizer(self.sizer_right_1)

    def apply_style(self, e):
        s = float(self.factor_stipple.GetValue())
        self.par.factor_stipple = s        
        
        print (self.par.factor_stipple)

class Text_style_dialog(My_dialog):

    def __init__(self, par):
        title = "Text style"
        size = (250, 100)
        My_dialog.__init__(self, par, par.interface.OnTextStyle, title, size)       
        
        self.sizer_right_1 = wx.GridSizer(cols = 2)                

        
        self.text_text_s_s, self.text_s_s = stroker(self, 'Letters distance factor', self.par.text_s_s, self.sizer_right_1, None)
        self.text_text_w, self.text_w = stroker(self, 'Width of letters factor', self.par.text_w, self.sizer_right_1, None)

        self.add_apply(self.sizer_right_1)

        self.SetSizer(self.sizer_right_1)

    def apply_style(self, e):
        s = float(self.text_s_s.GetValue())
        self.par.text_s_s = s
        s = float(self.text_w.GetValue())
        self.par.text_w = s
        
        print (self.par.text_w,
               self.par.text_s_s)


def stroker(frame, text, var, sizer_1, sizer_2, widget_type = 'entry', choices = None):        
    text_ctrl = wx.TextCtrl(frame, -1, text, size = (150, -1), style = wx.TE_READONLY | wx.BORDER_NONE)
    text_ctrl.SetBackgroundColour((214, 210, 208))
    if widget_type == 'entry':
        widget = wx.lib.masked.NumCtrl(
            frame,
            style = wx.TE_PROCESS_ENTER,
            fractionWidth = 2,
            size = (100, -1),
            autoSize = False,
            )
        widget.SetValue(var)
    elif widget_type == 'combobox':
        widget = wx.ComboBox(
            frame,
            choices = choices, 
            style = wx.CB_READONLY,
            size = (100, -1)
            )
        #widget.SetSelection(var)
        widget.SetValue(var)
        
    sizer_1.Add(text_ctrl)
    sizer_1.Add(widget, flag = wx.ALIGN_RIGHT)
    #sizer_2.Add(widget, flag = wx.ALIGN_RIGHT | wx.ALL, border = 4)
    return text_ctrl, widget

def get_path(system, direct, file_name):
    if system == 'windows' and direct[-1] == ':':
        direct += '\\'
    
    path = os.path.join(direct, file_name)
    return path
    
            
        
        
        
    
