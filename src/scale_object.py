# -*- coding: utf-8; -*-
class Scale_object:
    def __init__(self, par):
        self.par = par
        self.scaleEvent()

    def scaleEvent(self):
        if self.par.collection: #Если есть выбранные объекты
            self.par.standart_unbind()
            self.par.old_func = 'self.scaleEvent()'
            self.par.resFlag = True
            self.par.info.config(text = (u'Selected %s objects. Escape - stop') %(len(self.par.collection)))
            self.par.dialog.config(text = u'Scale - base point:')
            #self.par.c.tag_unbind('sel', '<Button-1>')
            #self.par.c.tag_unbind('sel', "<Leave>")
            #self.par.c.tag_unbind('sel', "<Enter>")
            self.par.c.bind('<Button-1>', self.scaleEvent2)
            self.par.c.unbind('<Shift-Button-1>')
            self.par.c.unbind_class(self.par.master1,"<Return>")
        else:
            self.par.info.config(text = u'Objects do not selected')

    def scaleEvent2(self, event):
        self.par.dialog.config(text = (u'Scale - factor [%s]:') %(self.par.old_scale))
        self.par.ex=self.par.priv_coord[0]
        self.par.ey=self.par.priv_coord[1]
        self.par.set_coord()
        self.par.c.unbind('<Button-1>')
        self.par.c.bind_class(self.par.master1,"<Return>", self.scaleEvent3)

    def scaleEvent3(self, event):
        self.par.ex,self.par.ey = self.par.coordinator(self.par.ex,self.par.ey)
        self.par.comOrKill()
        if self.par.com:
            pd = float(self.par.com)
            self.par.old_scale = pd
        else:
            pd = self.par.old_scale
       
        for i in self.par.collection:
            if i[0] not in ('t', 'd'):
                self.par.c.addtag_withtag('scale', i)
                if i[0] == 'l':
                    stip = self.par.ALLOBJECT[i]['stipple']
                    self.par.ALLOBJECT[i]['stipple'] = map(lambda x: x*pd, stip)
                    self.par.ALLOBJECT[i]['factor_stip'] *= pd
                elif i[0] in ('c', 'a'):
                    self.par.ALLOBJECT[i]['R'] *= pd
        self.par.c.scale('scale', self.par.ex, self.par.ey, pd, pd)
        self.par.c.dtag('scale')
        self.par.kill()
