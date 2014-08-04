# -*- coding: utf-8; -*-
import copy

def undo(fact, parent):
    ev = copy.copy(fact[0])
    
    if ev == 'c_':
        del parent.history_undo[-1]
        parent.delete(elements = [fact[1],], add_history = 'add')
    elif ev == 'delete':
        el = fact[1]
        del parent.history_undo[-1]
        for i in el[0]:
            if i[0] == 'line':
                fill = i[1]
                width = i[2]
                sloy = i[3]
                stipple = i[4]
                c = i[5]
                x1, y1 = parent.coordinator(c[0], c[1], zoomOLDres = el[2], xynachres = el[1])
                x2, y2 = parent.coordinator(c[2], c[3], zoomOLDres = el[2], xynachres = el[1])
                parent.c_line(x1, y1, x2, y2, fill = fill, width = width, stipple = stipple, sloy = sloy)

            elif i[0] == 'circle':
                xc, yc = parent.coordinator(i[1], i[2], zoomOLDres = el[2], xynachres = el[1])
                R = parent.m_coordinator(i[3], zoomOLDres = el[2])
                fill = i[4]
                width = i[5]
                sloy = i[6]
                parent.c_circle(xc, yc, fill = fill, width = width, sloy = sloy, R = R)

            elif i[0] == 'arc':
                xc, yc = parent.coordinator(i[1], i[2], zoomOLDres = el[2], xynachres = el[1])
                dx1, dy1 = parent.coordinator(i[3], i[4], zoomOLDres = el[2], xynachres = el[1])
                dx2, dy2 = parent.coordinator(i[5], i[6], zoomOLDres = el[2], xynachres = el[1])
                fill = i[7]
                width = i[8]
                sloy = i[9]
                parent.c_arc(xc, yc, dx1, dy1, dx2, dy2, fill = fill, width = width, sloy = sloy)

            elif i[0] == 'dim':
                x1, y1 = parent.coordinator(i[1], i[2], zoomOLDres = el[2], xynachres = el[1])
                x2, y2 = parent.coordinator(i[3], i[4], zoomOLDres = el[2], xynachres = el[1])
                x3, y3 = parent.coordinator(i[5], i[6], zoomOLDres = el[2], xynachres = el[1])
                ort = i[7]
                size = i[8]
                fill = i[9]
                text = i[10]
                sloy = i[11]
                text_change = i[12]
                text_place = i[13]
                s = i[14]
                vr_s = i[15]
                vv_s = i[16]
                arrow_s = i[17]
                type_arrow = i[18]
                s_s_dim = i[19]
                w_text_dim = i[20]
                font_dim = i[21]

                parent.dim(x1,y1,x2,y2,x3,y3,text=text, sloy = sloy,
                                                fill = fill,
                                                size = size,
                                                ort = ort,
                                                text_change = text_change,
                                                text_place = text_place,
                                                s=s,
                                                vv_s=vv_s,
                                                vr_s = vr_s,
                                                arrow_s = arrow_s,
                                                type_arrow = type_arrow,
                                                s_s = s_s_dim,
                                                w_text = w_text_dim,
                                                font = font_dim)
                
            elif i[0] == 'text':
                fill = i[1]
                text = i[2]
                sloy = i[3]
                angle = i[4]
                anchor = i[5]
                size = i[6]
                c = i[8]
                s_s = i[9]
                w_text = i[10]
                font = i[11]
                x1, y1 = parent.coordinator(c[0], c[1], zoomOLDres = el[2], xynachres = el[1])
                parent.c_text(x1, y1, text=text, anchor = anchor, sloy = sloy, fill = fill, angle = angle, size = size, s_s = s_s, w_text = w_text, font = font)
'''
def redo(fact, parent):
    ev = copy.copy(fact[0])
    
    if ev == 'c_':
        del parent.history_undo[-1]
        parent.delete(elements = [fact[1],], add_history = 'add')
    elif ev == 'delete':
        el = fact[1]
        del parent.history_undo[-1]
        for i in el[0]:
            if i[0] == 'line':
                fill = i[1]
                width = i[2]
                sloy = i[3]
                c = i[4]
                x1, y1 = parent.coordinator(c[0], c[1], zoomOLDres = el[2], xynachres = el[1])
                x2, y2 = parent.coordinator(c[2], c[3], zoomOLDres = el[2], xynachres = el[1])
                parent.c_line(x1, y1, x2, y2, fill = fill, width = width, sloy = sloy)
'''
