# -*- coding: utf-8; -*-
import text_line, dimension, circle, arc
import line as _line

class Param_edit:
    def __init__(self, par, params):
        self.par = par
        self.param_edit(params)
            
    def param_edit(self, params):
        if self.par.collection:
            remove_list = []
            st = lambda x: x
            str_float_text = {'text':(2, st),
                             'anchor':(3, st),
                             'fill':(5, st),
                             'angle':(6, float),
                             'size':(7, float),
                             's_s':(8, float),
                             'w_text':(9, float),
                             'font':(10, st)}
            
            str_float_dimr = {'size':(4, float),
                             'fill':(5, st),
                             'text':(6, st),
                             's':(8, float),
                             'vr_s':(9, float),
                             'arrow_s':(10, float),
                             'type_arrow':(11, st),
                             's_s_dim':(12, float),
                             'w_text_dim':(13, float),
                             'font_dim':(14, st),
                             'R':(15, float)}

            str_float_dim = {'size':(9, float),
                             'fill':(8, st),
                             'text':(6, st),
                             's':(13, float),
                             'vr_s':(14, float),
                             'vv_s':(15, float),
                             'arrow_s':(16, float),
                             'type_arrow':(17, st),
                             's_s_dim':(18, float),
                             'w_text_dim':(19, float),
                             'font_dim':(20, st)}
            

            for i in self.par.collection:
                #args = None
                #obj = None
                r_list = self.par.ALLOBJECT[i]['class'].edit_prop(params)
                if r_list:
                    remove_list.append(r_list)
                '''
                for param in params:
                    if param in self.par.ALLOBJECT[i]:
                        arg = params[param]
                        self.par.ALLOBJECT[i][param] = arg
                        self.par.changeFlag = True
                        if i[0] == 't':
                            if args:
                                if param in str_float_text:
                                    j,f = str_float_text[param]
                                    args[j] = f(arg)
                            else:
                                fill, text, sloy, angle, anchor, size, line, coord, s_s, w_text, font = self.par.get_text_conf(i)
                                if param == 'size':
                                    size = float(arg)
                                elif param == 'fill':
                                    fill = arg
                                elif param == 'angle':
                                    angle = arg
                                elif param == 's_s':
                                    s_s = float(arg)
                                elif param == 'w_text':
                                    w_text = float(arg)
                                elif param == 'font':
                                    font = arg
                                elif param == 'text':
                                    text = arg
                                args = [coord[0], coord[1], text, anchor, sloy, fill, angle, size, s_s, w_text, font]
                                obj = 'ltext'

                        elif i[0] == 'd':
                            if args:
                                if param in str_float_dim:
                                    j,f = str_float_dim[param]
                                    args[j] = f(arg)
                            else:
                                x1, y1, x2, y2, x3, y3, ort, size, fill, text, sloy, text_change, text_place, s, vr_s, vv_s, arrow_s, type_arrow, s_s_dim, w_text_dim, font_dim  = self.par.get_dim_conf(i)

                                if param == 'size':
                                    size = float(arg)
                                elif param == 'fill':
                                    fill = arg
                                elif param == 'text':
                                    text = arg
                                elif param == 's':
                                    s = float(arg)
                                elif param == 'vr_s':
                                    vr_s = float(arg)
                                elif param == 'vv_s':
                                    vv_s = float(arg)
                                elif param == 'arrow_s':
                                    arrow_s = float(arg)
                                elif param == 'type_arrow':
                                    type_arrow = arg
                                elif param == 's_s_dim':
                                    s_s_dim = float(arg)
                                elif param == 'w_text_dim':
                                    w_text_dim = arg
                                elif param == 'font_dim':
                                    font_dim = arg
                                args = [x1, y1, x2, y2, x3, y3, text, sloy, fill, size, ort, text_change, text_place, s, vr_s, vv_s, arrow_s, type_arrow, s_s_dim, w_text_dim, font_dim]
                                obj = 'dim'

                        elif i[0] == 'r':
                            if args:
                                if param in str_float_dimr:
                                    j,f = str_float_dimr[param]
                                    args[j] = f(arg)
                            else:
                                xc, yc, x1, y1, size, fill, text, sloy, s, vr_s, arrow_s, type_arrow, s_s_dim, w_text_dim, font_dim, R  = self.par.get_dimR_conf(i)

                                if param == 'size':
                                    size = float(arg)
                                elif param == 'fill':
                                    fill = arg
                                elif param == 'text':
                                    text = arg
                                elif param == 's':
                                    s = float(arg)
                                elif param == 'vr_s':
                                    vr_s = float(arg)
                                elif param == 'arrow_s':
                                    arrow_s = float(arg)
                                elif param == 'type_arrow':
                                    type_arrow = arg
                                elif param == 's_s_dim':
                                    s_s_dim = float(arg)
                                elif param == 'w_text_dim':
                                    w_text_dim = arg
                                elif param == 'font_dim':
                                    font_dim = arg
                                elif param == 'R':
                                    R = arg
                                args = [xc, yc, x1, y1, size, fill, text, sloy, s, vr_s, arrow_s, type_arrow, s_s_dim, w_text_dim, font_dim, R]
                                obj = 'dimr'

                        elif i[0] == 'L':
                            self.par.ALLOBJECT[i]['class'].edit_prop(self.par, i, param, )
                            
                            if args:
                                if param == 'width':
                                    args[4] = int(arg)
                                elif param == 'stipple':
                                    if arg:
                                        args[7] = map(lambda x: float(x), arg)
                                    else:
                                        args[7] = arg
                                elif param == 'fill':
                                    args[6] = arg
                                    
                                elif param == 'factor_stip':                                    
                                    args[8] = arg
                            else:
                                fill, width, sloy, stipple, coord, factor_stip = self.par.get_line_conf(i)
                                if param == 'width':
                                    width = int(arg)
                                elif param == 'stipple':
                                    if arg:
                                        stipple = map(lambda x: float(x), arg)
                                elif param == 'fill':
                                    fill = arg
                                elif param == 'factor_stip':
                                    factor_stip = arg
                                args = [coord[0], coord[1], coord[2], coord[3],  width, sloy, fill, stipple, factor_stip]
                                obj = 'line'
                            
                        elif i[0] == 'c':
                            if args:
                                if param == 'R':
                                    args[2] = float(arg)
                                elif param == 'width':
                                    args[4] = int(arg)
                                elif param == 'fill':
                                    args[3] = arg
                            else:
                                x0, y0, R, fill, width, sloy = self.par.get_circle_conf(i)
                                if param == 'width':
                                    width = int(arg)
                                elif param == 'fill':
                                    fill = arg
                                elif param == 'R':
                                    R = arg
                                args = [x0, y0, R, fill, width, sloy]
                                obj = 'circle'

                        elif i[0] == 'a':
                            if args:
                                if param == 'width':
                                    args[7] = int(arg)
                                elif param == 'fill':
                                    args[6] = arg
                            else:
                                xc, yc, dx1, dy1, dx2, dy2, fill, width, sloy = self.par.get_arc_conf(i)
                                if param == 'width':
                                    width = int(arg)
                                elif param == 'fill':
                                    fill = arg
                                args = [xc, yc, dx1, dy1, dx2, dy2, fill, width, sloy]
                                obj = 'arc'

                if args:
                    if obj == 'ltext':
                        text_line.c_text(self.par, args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7],args[8],args[9],args[10])
                        remove_list.append((i,self.par.Ntext))
                    elif obj == 'dim':
                        dimension.c_dim(self.par, args[0],args[1],args[2],args[3],args[4],args[5],
                                 text = args[6],
                                 sloy = args[7],
                                 fill = args[8],
                                 size = args[9],
                                 ort = args[10],
                                 text_change = args[11],
                                 text_place = args[12],
                                 s = args[13],
                                 vr_s = args[14],
                                 vv_s = args[15],
                                 arrow_s = args[16],
                                 type_arrow = args[17],
                                 s_s = args[18],
                                 w_text = args[19],
                                 font = args[20])
                        remove_list.append((i,self.par.Ndim))

                    elif obj == 'dimr':

                        dimension.c_dimR(self.par, args[0],args[1],args[2],args[3],
                                 text = args[6],
                                 sloy = args[7],
                                 fill = args[5],
                                 size = args[4],
                                 s = args[8],
                                 vr_s = args[9],
                                 arrow_s = args[10],
                                 type_arrow = args[11],
                                 s_s = args[12],
                                 w_text = args[13],
                                 font = args[14],
                                 Rn = args[15])
                        remove_list.append((i,self.par.Ndimr))

                    elif obj == 'line':
                        _line.c_line(self.par, args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7],args[8])
                        remove_list.append((i,self.par.Nline))

                    elif obj == 'circle':
                        circle.c_circle(self.par, args[0],args[1],R = args[2], fill = args[3],width = args[4],sloy = args[5])
                        remove_list.append((i,self.par.Ncircle))

                    elif obj == 'arc':
                        arc.c_arc(self.par, args[0],args[1],args[2], args[3],args[4],args[5],fill =  args[6],width = args[7],sloy = args[8])
                        remove_list.append((i,self.par.Narc))
            '''
        if remove_list:
            del_list = [x[0] for x in remove_list]
            self.par.delete(elements = del_list)
            for r in remove_list:
                self.par.collection.remove(r[0])
                self.par.collection.append(r[1])
            
