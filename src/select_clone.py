
class Select_clone:
    def __init__(self, Nums, par, color =  None):
        if not color:
            color = par.select_color            
        for Num in Nums:
            Nclone = 'C'+Num
            ids = par.ALLOBJECT[Num]['id']
            if par.zoomOLD < -20:
                ids2 = {}
                for i in ids:
                    if 'priv' in ids[i]:
                        ids2[i] = ids[i]
                ids = ids2

            
            if Num[0] in ('L', 't', 'd', 'r'):
                for i in ids:
                    
                    par.c.create_line(par.c.coords(i), fill = color, width = 3, tags = ('obj', Nclone, 'clone'))
            elif Num[0] == 'a':
                for i in ids:
                    if 'line' in ids[i]:
                        par.c.create_line(par.c.coords(i), fill = color, width = 3, tags = ('obj', Nclone, 'clone'))
                    else:
                        par.c.create_arc(par.c.coords(i), start = par.c.itemcget(i, 'start'), extent = par.c.itemcget(i, 'extent'), outline = color, fill = None, width = 3, style = 'arc', tags = ('obj', Nclone, 'clone'))

            elif Num[0] == 'c':
                for i in ids:
                    if 'line' in ids[i]:
                        par.c.create_line(par.c.coords(i), fill = color, width = 3, tags = ('obj', Nclone, 'clone'))
                    else:
                        par.c.create_oval(par.c.coords(i), outline = color, width = 3, tags = ('obj', Nclone, 'clone'))
