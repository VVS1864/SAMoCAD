# -*- coding: utf-8; -*-
def lapping2(par, select): #Выделение/снятие выделения рамкой
    if par.lappingFlag == True:#Если кончание выделения
        par.c.delete(par.rect)#Удалить прямоугольник выделения
        par.rect = None
        par.ex = par.rectx
        par.ey = par.recty
        par.ex2 = par.rectx2
        par.ey2 = par.recty2
        if par.ex<par.ex2:#Пересчет координат для функций канваса
            x1=par.ex
            x2=par.ex2
            if par.ey<par.ey2:
                y1=par.ey
                y2=par.ey2
            else:
                y1=par.ey2
                y2=par.ey
            c = par.c.find_overlapping(x1,y1,x2,y2)
            par.mass_collektor(c, select)

        else:
            x1=par.ex2
            x2=par.ex
            if par.ey<par.ey2:
                y1=par.ey
                y2=par.ey2
            else:
                y1=par.ey2
                y2=par.ey
            c = par.c.find_enclosed(x1,y1,x2,y2)#Получить все объекты, попавшие полностью в рамку
            par.mass_collektor(c, select)#Добавить полученное в коллекцию


        par.colObj()#Пересчитать количество объектов
        par.lappingFlag = False
        par.c.unbind_class(par.c, "<Motion>")#Вернуть события в исходное состояние
        #par.c.tag_bind('sel', "<Button-1>", par.collektor_sel)
        #par.c.tag_bind('sel', "<Shift-Button-1>", par.collektor_desel)
        par.c.bind_class(par.c,"<Motion>", par.gpriv)
        par.c.bind_class(par.master1,"<Return>", par.old_function)
        par.dialog.config(text = u'Command:')
    else:#Если начало выделения
        par.dialog.config(text = u'Select - ending point:')
        par.info.config(text = u'Escape - stop')
        par.lappingFlag=True
        par.rectx=par.priv_coord[0]
        par.recty=par.priv_coord[1]
        par.set_coord()
        #par.c.tag_unbind('sel', "<Button-1>")
        #par.c.tag_unbind('sel', "<Shift-Button-1>")
        par.c.unbind_class(par.c,"<Motion>")
        par.c.bind_class(par.c, "<Motion>", par.resRect)
        par.c.unbind_class(par.master1,"<Return>")

