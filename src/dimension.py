# -*- coding: utf-8; -*-
from math import pi, sqrt, degrees, radians
from os import path
from calc import calc_angle, rotate_lines, rotate_points
import symbols
from move_object import move_lines
from text_line import c_text
from collections import OrderedDict

zoomm = 0.8
zoomp = 1.0/0.8
#РАЗМЕР
class Dimension:
    def __init__(self, par):
        self.par = par
        self.risDim()
        
    def risDim(self):
        self.par.kill()
        self.par.standart_unbind()
        self.par.old_func = 'self.risDim()'
        self.par.c.bind('<Button-1>', self.risDim2)
        self.par.dialog.config(text = u'Dimension - point 1:')
        self.par.info.config(text = u'Enter - stop')

    def risDim2(self, event):
        self.par.ex = self.par.priv_coord[0]
        self.par.ey = self.par.priv_coord[1]
        self.par.set_coord()
        self.par.c.bind_class(self.par.c,"<1>", self.risDim3)
        self.par.dialog.config(text = u'Dimension - point 2:')
        self.par.command.focus_set()

    def risDim3(self, event):
        self.par.ex2 = self.par.priv_coord[0]
        self.par.ey2 = self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        self.par.set_coord()
        self.par.c.bind_class(self.par.c,"<1>", self.risDim4)
        self.par.dialog.config(text = u'Dimension - dim line:')
        self.par.command.focus_set()
        self.par.dim_clone = True

    def risDim4(self, event = None):
        self.par.ex3 = self.par.priv_coord[0]
        self.par.ey3 = self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        self.par.ex2,self.par.ey2 = self.par.coordinator(self.par.ex2,self.par.ey2)
        self.par.comOrKill()
        if self.par.com:
            self.par.com = self.par.coordinator2(self.par.com)
            if self.par.ex3>self.par.ex2 and self.par.ex3>self.par.ex:
                self.par.ex3=self.par.ex2+self.par.com
            else:
                self.par.ex3=self.par.ex2-self.par.com
            if self.par.ey3>self.par.ey2 and self.par.ey3>self.par.ey:
                self.par.ey3=self.par.ey2+self.par.com
            else:
                self.par.ey3=self.par.ey2-self.par.com
        if event:
            c_dim(self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2,self.par.ex3,self.par.ey3)
            self.par.history_undo.append(('c_', self.par.Ndim))
            self.par.com = None
            self.par.changeFlag = True
            self.par.enumerator_p()
            self.par.risDim()
        else:
            self.par.set_coord()
            c_dim(self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2,self.par.ex3,self.par.ey3, temp = 'Yes')
            

def c_dim(par,x1,y1,x2,y2,x3,y3,text=None, sloy = None,
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
                                            font = None,
                                            temp = None,
                                            ID = None):
    if sloy == None:
        sloy = par.sloy
        fill = par.color
        size = par.size_f
        s = s_old = par.s
        vr_s = vr_s_old = par.vr_s
        vv_s = vv_s_old = par.vv_s
        arrow_s = arrow_s_old = par.arrow_s
        type_arrow = par.type_arrow
        s_s =  par.s_s_dim
        w_text = par.w_text_dim
        font = par.font_dim
    else:
        s_old = s
        vr_s_old = vr_s
        vv_s_old = vv_s
        arrow_s_old = arrow_s
    if not temp:
        if text == 'None':
            text = None#АХТУНГ
        if not ID:
            par.Ndimd+=1
            ID = par.Ndim = 'd' + str(par.Ndimd)
        dx=abs(x1-x2)
        dy=abs(y1-y2)
         
        id_dict = OrderedDict()
        list_arrow = []
        list_lines = []
        list_text_lines = []

        if par.zoomOLD==0:
            ddx=dx
            ddy=dy
        else:
            if par.zoomOLD>0:
                s*=(zoomp**par.zoomOLD)
                arrow_s*=(zoomp**par.zoomOLD)
                vr_s*=(zoomp**par.zoomOLD)
                vv_s*=(zoomp**par.zoomOLD)
                ddx=dx*zoomm**par.zoomOLD
                ddy=dy*zoomm**par.zoomOLD
            else:
                zoomOLDx=par.zoomOLD*(-1)
                s/=(zoomp**zoomOLDx)
                arrow_s/=(zoomp**zoomOLDx)
                vr_s/=(zoomp**zoomOLDx)
                vv_s/=(zoomp**zoomOLDx)
                ddx=dx*zoomp**zoomOLDx
                ddy=dy*zoomp**zoomOLDx
        ddx=format(ddx, '.0f')
        ddy=format(ddy, '.0f')
        x = max(x1, x2)
        xm = min(x1, x2)
        y = max(y1, y2)
        ym = min(y1, y2)
        if ort == None:
            xe_max = max(x3, x)
            xe_min = min(x3, x)
            ye_max = max(y3, y)
            ye_min = min(y3, y)
            if xe_max-xe_min > ye_max-ye_min:
                ort="horizontal"
            else:
                ort="vertical"
            if ym<=y3<=y:
                ort="horizontal"
            if xm<=x3<=x:
                ort="vertical"
        elif ort == 'rotated':
            pass
        if text:
            textt = text
        else:
            textt = ddx
        if ort == "horizontal":
            if text_place == None:
                text_place = [0, 0]
            if text:
                textt = text
            else:
                textt = ddy

            [[x2,y2], [x3,y3], [text_place[0], text_place[1]]]  = rotate_points(x1, y1, [[x2,y2], [x3,y3], [text_place[0], text_place[1]]], -radians(90))
            x = max(x1, x2)
            xm = min(x1, x2)
            y = max(y1, y2)
            ym = min(y1, y2)

        else:
            if text:
                textt = text
            else:
                textt = ddx

        dx=abs(x1-x2)
        dy=abs(y1-y2)
        angle = 0
        #Выносные линии
        zvv_s = 1
        if y3 < y:
            zvv_s = -1
       
        list_lines.extend([[x1, y1, x1, y3+vv_s*zvv_s], [x2, y2, x2, y3+vv_s*zvv_s]])
        #Размерная линия + текст(если задан, если нет - вкличина размера)
        if text_change == 'unchange':
            text_place = [xm+dx/2.0,y3-s] 
        elif text_change == 'online3'  or text_change == 'online3_m_l':
            text_place[1] = y3-s
        list_text_lines = symbols.font(text_place[0], text_place[1], textt, size, par.zoomOLD, s_s, w_text, 'sc', font, 0)
        if text_change == 'online3':
            e2 = list_text_lines.nabor[0][0]
            e3 = list_text_lines.nabor[0][2]
            if x<e3:
                line3 = [xm-vr_s, y3, e3, y3]
            else:
                line3 = [e2, y3, x+vr_s, y3]
        else:
            line3 = [xm-vr_s,y3,x+vr_s,y3]
        i = 1
        if text_change == 'unchange':
            e = list_text_lines.Ltext
            #Если текст не вмещается между выносными линиями - нарисовать сбоку
            if e>dx-arrow_s: 
                list_text_lines.nabor = move_lines(text_place[0], text_place[1], xm-arrow_s-list_text_lines.Ltext/2.0, y3-s, list_text_lines.nabor)
                e = list_text_lines.nabor[0][0]
                line3 = [x+arrow_s, y3, e, y3]
                i = -1
                text_change = 'online3'
        list_lines.append(line3)       
        #Засечки
        if type_arrow == 'Arch':
            L1 = [x2-arrow_s,y3+arrow_s,x2+arrow_s,y3-arrow_s]
            L2 = [x1-arrow_s,y3+arrow_s,x1+arrow_s,y3-arrow_s]
            list_arrow.extend([L1, L2])
        elif type_arrow == 'Arrow':
            L1 = [xm, y3, xm+arrow_s*i, y3-arrow_s/10.0]
            L2 = [xm, y3, xm+arrow_s*i, y3+arrow_s/10.0]
            L3 = [x, y3, x-arrow_s*i, y3-arrow_s/10.0]
            L4 = [x, y3, x-arrow_s*i, y3+arrow_s/10.0]
            list_arrow.extend([L1, L2, L3, L4])

        if ort == 'horizontal':
            angle = radians(90)
            list_text_lines.nabor = rotate_lines(x1, y1, list_text_lines.nabor, angle)
            list_arrow = rotate_lines(x1, y1, list_arrow, angle)
            list_lines = rotate_lines(x1, y1, list_lines, angle)

        for i in list_lines:
            id = par.c.create_line(i, fill=fill, tags = ('obj', ID, 'sel'))
            id_dict[id] = ('line', 'priv')
        #Перебрать координаты линий текста, нарисовать линии
        for i in list_text_lines.nabor[1:]: 
            try:
                id = par.c.create_line(i[0],i[1],i[2],i[3],fill=fill, tags = ('obj', ID, 't_LOD', 'sel'))
                id_dict[id] = ('line', 'dim_text')
            except:
                pass
        snap_text = list_text_lines.nabor[0]
        id = par.c.create_line(snap_text[0],snap_text[1],snap_text[2],snap_text[3], width=8, fill = fill, stipple = ('@'+path.join(par.appPath, 'res', '00.xbm')), tags = ('obj', ID, 'snap_text', 'sel'))#'ltext', par.Ntext, 'line', 'obj', 'priv', par.Ntext+'xy'#, sloy])
        id_dict[id] = ('line', 'priv', 'dim_text', 'dim_text_priv')

        for i in list_arrow:
            id = par.c.create_line(i, fill=fill, tags = ('obj', ID, 't_LOD', 'sel'))
            id_dict[id] = ('line',)

        #Записать в ALLOBJECT параметры размера
        par.ALLOBJECT[ID]={
                                'text':text,
                                'angle':angle,
                                'object':'dim',
                                'ort':ort,
                                'fill':fill,
                                'size':size,
                                'sloy':sloy,
                                'text_change':text_change,
                                's' : s_old,
                                'vr_s': vr_s_old,
                                'vv_s':vv_s_old,
                                'arrow_s':arrow_s_old,
                                'type_arrow':type_arrow,
                                's_s_dim':s_s,
                                'w_text_dim':w_text,
                                'font_dim':font,
                                'id':id_dict,
                                }

    else:
        if text == 'None':
            text = None#АХТУНГ
        #par.Ndimd+=1
        #par.Ndim = 'd' + str(par.Ndimd)
        dx=abs(x1-x2)
        dy=abs(y1-y2)
         
        id_dict = OrderedDict()
        list_arrow = []
        list_lines = []
        list_text_lines = []

        if par.zoomOLD==0:
            ddx=dx
            ddy=dy
        else:
            if par.zoomOLD>0:
                s*=(zoomp**par.zoomOLD)
                arrow_s*=(zoomp**par.zoomOLD)
                vr_s*=(zoomp**par.zoomOLD)
                vv_s*=(zoomp**par.zoomOLD)
                ddx=dx*zoomm**par.zoomOLD
                ddy=dy*zoomm**par.zoomOLD
            else:
                zoomOLDx=par.zoomOLD*(-1)
                s/=(zoomp**zoomOLDx)
                arrow_s/=(zoomp**zoomOLDx)
                vr_s/=(zoomp**zoomOLDx)
                vv_s/=(zoomp**zoomOLDx)
                ddx=dx*zoomp**zoomOLDx
                ddy=dy*zoomp**zoomOLDx
        ddx=format(ddx, '.0f')
        ddy=format(ddy, '.0f')
        x = max(x1, x2)
        xm = min(x1, x2)
        y = max(y1, y2)
        ym = min(y1, y2)
        if ort == None:
            xe_max = max(x3, x)
            xe_min = min(x3, x)
            ye_max = max(y3, y)
            ye_min = min(y3, y)
            if xe_max-xe_min > ye_max-ye_min:
                ort="horizontal"
            else:
                ort="vertical"
            if ym<=y3<=y:
                ort="horizontal"
            if xm<=x3<=x:
                ort="vertical"
        elif ort == 'rotated':
            pass
        if text:
            textt = text
        else:
            textt = ddx
        if ort == "horizontal":
            if text_place == None:
                text_place = [0, 0]
            if text:
                textt = text
            else:
                textt = ddy

            [[x2,y2], [x3,y3], [text_place[0], text_place[1]]]  = rotate_points(x1, y1, [[x2,y2], [x3,y3], [text_place[0], text_place[1]]], -radians(90))
            x = max(x1, x2)
            xm = min(x1, x2)
            y = max(y1, y2)
            ym = min(y1, y2)

        else:
            if text:
                textt = text
            else:
                textt = ddx

        dx=abs(x1-x2)
        dy=abs(y1-y2)
        angle = 0
        #Выносные линии
        zvv_s = 1
        if y3 < y:
            zvv_s = -1
       
        list_lines.extend([[x1, y1, x1, y3+vv_s*zvv_s], [x2, y2, x2, y3+vv_s*zvv_s]])
        #Размерная линия + текст(если задан, если нет - вкличина размера)
        if text_change == 'unchange':
            text_place = [xm+dx/2.0,y3-s] 
        elif text_change == 'online3'  or text_change == 'online3_m_l':
            text_place[1] = y3-s
        list_text_lines = symbols.font(text_place[0], text_place[1], textt, size, par.zoomOLD, s_s, w_text, 'sc', font, 0)
        if text_change == 'online3':
            e2 = list_text_lines.nabor[0][0]
            e3 = list_text_lines.nabor[0][2]
            if x<e3:
                line3 = [xm-vr_s, y3, e3, y3]
            else:
                line3 = [e2, y3, x+vr_s, y3]
        else:
            line3 = [xm-vr_s,y3,x+vr_s,y3]
        i = 1
        if text_change == 'unchange':
            e = list_text_lines.Ltext
            #Если текст не вмещается между выносными линиями - нарисовать сбоку
            if e>dx-arrow_s: 
                list_text_lines.nabor = move_lines(text_place[0], text_place[1], xm-arrow_s-list_text_lines.Ltext/2.0, y3-s, list_text_lines.nabor)
                e = list_text_lines.nabor[0][0]
                line3 = [x+arrow_s, y3, e, y3]
                i = -1
                text_change = 'online3'
        list_lines.append(line3)       
        #Засечки
        if type_arrow == 'Arch':
            L1 = [x2-arrow_s,y3+arrow_s,x2+arrow_s,y3-arrow_s]
            L2 = [x1-arrow_s,y3+arrow_s,x1+arrow_s,y3-arrow_s]
            list_arrow.extend([L1, L2])
        elif type_arrow == 'Arrow':
            L1 = [xm, y3, xm+arrow_s*i, y3-arrow_s/10.0]
            L2 = [xm, y3, xm+arrow_s*i, y3+arrow_s/10.0]
            L3 = [x, y3, x-arrow_s*i, y3-arrow_s/10.0]
            L4 = [x, y3, x-arrow_s*i, y3+arrow_s/10.0]
            list_arrow.extend([L1, L2, L3, L4])

        if ort == 'horizontal':
            angle = radians(90)
            list_text_lines.nabor = rotate_lines(x1, y1, list_text_lines.nabor, angle)
            list_arrow = rotate_lines(x1, y1, list_arrow, angle)
            list_lines = rotate_lines(x1, y1, list_lines, angle)

        for i in list_lines:
            par.c.create_line(i, fill=fill, tags = ('obj', 'temp'))
        #Перебрать координаты линий текста, нарисовать линии
        for i in list_text_lines.nabor[1:]: 
            try:
                par.c.create_line(i[0],i[1],i[2],i[3],fill=fill, tags = ('obj', 'temp'))
            except:
                pass
        snap_text = list_text_lines.nabor[0]
        par.c.create_line(snap_text[0],snap_text[1],snap_text[2],snap_text[3], width=8, fill = fill, stipple = ('@'+path.join(par.appPath, 'res', '00.xbm')), tags = ('obj', 'temp'))#'ltext', par.Ntext, 'line', 'obj', 'priv', par.Ntext+'xy'#, sloy])
        

        for i in list_arrow:
            par.c.create_line(i, fill=fill, tags = ('obj', 'temp'))
    

#РАЗМЕР РАДИУСНЫЙ
class Dimension_R:
    def __init__(self, par):
        self.par = par
        self.risDimR()

    def risDimR(self, event = None):
        self.par.kill()
        self.par.standart_unbind()
        self.par.old_func = 'self.risDimR()'
        self.par.c.bind('<Button-1>', self.risDimR2)
        self.par.dialog.config(text = u'Radius dimension - point 1:')
        self.par.info.config(text = u'Enter - stop')

    def risDimR2(self, event):
        self.par.ex = self.par.priv_coord[0]
        self.par.ey = self.par.priv_coord[1]
        self.par.set_coord()
        self.par.c.bind_class(self.par.c,"<1>", self.risDimR3)
        self.par.dialog.config(text = u'Radius dimension - point 2:')
        self.par.command.focus_set()
        self.par.dimR_clone = True    

    def risDimR3(self, event=None):
        self.par.ex2 = self.par.priv_coord[0]
        self.par.ey2 = self.par.priv_coord[1]
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        self.par.set_coord()
        self.par.trace_on = True
        self.par.trace_x1, self.par.trace_y1 = self.par.ex,self.par.ey
        self.par.trace_x2, self.par.trace_y2 = self.par.ex2,self.par.ey2
        if (self.par.ex2, self.par.ey2) != (self.par.ex, self.par.ey):
            if event:
                c_dimR(self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2)
                self.par.history_undo.append(('c_', self.par.Ndimr))
                self.par.changeFlag = True
                self.par.enumerator_p()
                self.par.risDimR()
            else:
                self.par.set_coord()
                c_dimR(self.par, self.par.ex,self.par.ey,self.par.ex2,self.par.ey2, temp = 'Yes')

def c_dimR(par,x1,y1,x2,y2, text=None, sloy = None,
                                            fill = None,
                                            size = None,
                                            s=None,
                                            vr_s = None,
                                            arrow_s = None,
                                            type_arrow = None,
                                            s_s = None,
                                            w_text = None,
                                            font = None,
                                            Rn = None,
                                            temp = None):
    if sloy == None:
        sloy = par.sloy
        fill = par.color
        size = par.size_f
        s = old_s = par.s
        vr_s = old_vr_s = par.vr_s
        arrow_s = old_arrow_s = par.arrow_s
        type_arrow = par.type_arrow
        s_s = par.s_s_dim
        w_text = par.w_text_dim
        font = par.font_dim
    else:
        old_s = s
        old_vr_s = vr_s
        old_arrow_s = arrow_s
    if text == 'None':
        text = None
    if not temp:
        par.Ndimrd+=1
        par.Ndimr = 'r' + str(par.Ndimrd)
        dx=x2-x1
        dy=y2-y1
        R = sqrt(dx*dx + dy*dy)
        
        id_dict = {}
        list_arrow = []
        list_lines = []
        list_text_lines = []
        
        if par.zoomOLD==0:
            Rr = R
        else:
            if par.zoomOLD>0:
                s*=(zoomp**par.zoomOLD)
                arrow_s*=(zoomp**par.zoomOLD)
                vr_s*=(zoomp**par.zoomOLD)
                Rr=R*zoomm**par.zoomOLD
            else:
                zoomOLDx=par.zoomOLD*(-1)
                s/=(zoomp**zoomOLDx)
                arrow_s/=(zoomp**zoomOLDx)
                vr_s/=(zoomp**zoomOLDx)
                Rr=R*zoomp**zoomOLDx
        if Rn != None:
            Rr = Rn
            R = par.coordinator2(Rn)
        Rrr=format(Rr, '.0f')

        angle = abs(calc_angle(x1, y1, x2, y2, x1+R, y1))
        i = 1
        anchor = 'sw'
        if y2>y1:
            angle = -angle
        if x2<x1:
            i = -1
            angle = angle-pi
            anchor = 'se'
        if text:
            textt = text
        else:
            textt = 'R ' + Rrr
        x1t = x1 + i*(R + arrow_s*2.0)
        y1t = y1 - s
        list_text_lines = symbols.font(x1t, y1t, textt, size, par.zoomOLD, s_s, w_text, anchor, font, 0)
        e = list_text_lines.nabor[0]
        if i > 0:
            list_lines.extend([[x1, y1, e[2], y1]])
        else:
            list_lines.extend([[x1, y1, e[0], y1]])
            
        if type_arrow == 'Arch':
            L1 = [x1+i*(R-arrow_s), y1+arrow_s, x1+i*(R+arrow_s), y1-arrow_s]
            list_arrow.extend([L1,])
                                  
        elif type_arrow == 'Arrow':
            L1 = [x1+i*R,y1,x1+i*(R-arrow_s),y1-arrow_s/10.0]
            L2 = [x1+i*R,y1,x1+i*(R-arrow_s),y1+arrow_s/10.0]
            list_arrow.extend([L1, L2])
        print x1, y1, list_text_lines.nabor
        list_text_lines.nabor = rotate_lines(x1, y1, list_text_lines.nabor, angle)
        list_arrow = rotate_lines(x1, y1, list_arrow, angle)
        list_lines = rotate_lines(x1, y1, list_lines, angle)
            
        for i in list_arrow:
            id = par.c.create_line(i, fill=fill, tags = ('obj', par.Ndimr, 'sel'))
            id_dict[id] = ('line',)
        for i in list_lines:
            id = par.c.create_line(i, fill=fill, tags = ('obj', par.Ndimr, 'sel'))
            id_dict[id] = ('line', 'priv')
            
        for i in list_text_lines.nabor[1:]: 
            try:
                id = par.c.create_line(i[0],i[1],i[2],i[3],fill=fill, tags = ('obj', par.Ndimr, 't_LOD', 'sel'))
                id_dict[id] = ('line', 'dim_text')
            except:
                pass
        snap_text = list_text_lines.nabor[0]
        id = par.c.create_line(snap_text[0],snap_text[1],snap_text[2],snap_text[3], width=8, fill = fill, stipple = ('@'+path.join(par.appPath, 'res', '00.xbm')), tags = ('obj', par.Ndimr, 'snap_text', 'sel'))        
        id_dict[id] = ('line', 'priv', 'dim_text', 'dim_text_priv')
        par.ALLOBJECT[par.Ndimr]={'text':text,#Записать в ALLOBJECT параметры размера
                                    'angle':angle,
                                    'object':'dimr',
                                    'fill':fill,
                                    'size':size,
                                    'sloy':sloy,
                                    's' : old_s,
                                    'R' : Rr,
                                    'vr_s': old_vr_s,
                                    'arrow_s': old_arrow_s,
                                    'type_arrow':type_arrow,
                                    's_s_dim':s_s,
                                    'w_text_dim':w_text,
                                    'font_dim':font,
                                    'id':id_dict}
    else:
        dx=x2-x1
        dy=y2-y1
        R = sqrt(dx*dx + dy*dy)
        list_arrow = []
        list_lines = []
        list_text_lines = []   
        if par.zoomOLD==0:
            Rr = R
        else:
            if par.zoomOLD>0:
                s*=(zoomp**par.zoomOLD)
                arrow_s*=(zoomp**par.zoomOLD)
                vr_s*=(zoomp**par.zoomOLD)
                Rr=R*zoomm**par.zoomOLD
            else:
                zoomOLDx=par.zoomOLD*(-1)
                s/=(zoomp**zoomOLDx)
                arrow_s/=(zoomp**zoomOLDx)
                vr_s/=(zoomp**zoomOLDx)
                Rr=R*zoomp**zoomOLDx
        if Rn != None:
            Rr = Rn
            R = par.coordinator2(Rn)
        Rrr=format(Rr, '.0f')

        angle = abs(calc_angle(x1, y1, x2, y2, x1+R, y1))
        i = 1
        anchor = 'sw'
        if y2>y1:
            angle = -angle
        if x2<x1:
            i = -1
            angle = angle-pi
            anchor = 'se'
        if text:
            textt = text
        else:
            textt = 'R ' + Rrr
        x1t = x1 + i*(R + arrow_s*2.0)
        y1t = y1 - s
        list_text_lines = symbols.font(x1t, y1t, textt, size, par.zoomOLD, s_s, w_text, anchor, font, 0)
        e = list_text_lines.nabor[0]
        if i > 0:
            list_lines.extend([[x1, y1, e[2], y1]])
        else:
            list_lines.extend([[x1, y1, e[0], y1]])
            
        if type_arrow == 'Arch':
            L1 = [x1+i*(R-arrow_s), y1+arrow_s, x1+i*(R+arrow_s), y1-arrow_s]
            list_arrow.extend([L1,])
                                  
        elif type_arrow == 'Arrow':
            L1 = [x1+i*R,y1,x1+i*(R-arrow_s),y1-arrow_s/10.0]
            L2 = [x1+i*R,y1,x1+i*(R-arrow_s),y1+arrow_s/10.0]
            list_arrow.extend([L1, L2])

        list_text_lines.nabor = rotate_lines(x1, y1, list_text_lines.nabor, angle)
        list_arrow = rotate_lines(x1, y1, list_arrow, angle)
        list_lines = rotate_lines(x1, y1, list_lines, angle)
            
        for i in list_arrow:
            par.c.create_line(i, fill=fill, tags = ('obj', 'temp'))
        for i in list_lines:
            par.c.create_line(i, fill=fill, tags = ('obj', 'temp'))
        for i in list_text_lines.nabor[1:]: 
            try:
                par.c.create_line(i[0],i[1],i[2],i[3],fill=fill, tags = ('obj', 'temp'))
            except:
                pass
        snap_text = list_text_lines.nabor[0]
        par.c.create_line(snap_text[0],snap_text[1],snap_text[2],snap_text[3], width=8, fill = fill, stipple = ('@'+path.join(par.appPath, 'res', '00.xbm')), tags = ('obj', 'temp'))
        
      
