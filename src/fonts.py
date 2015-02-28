# -*- coding: utf-8 -*-
class Font_Arch:
    def __init__(self):
        self.w_text = None
        self.nachTextX = None
        self.sx = None
        self.liter = None
        self.nachTextY = None
        self.liter_dict = {
                    u'А':self.a,
                    'A':self.a,
                    'a':self.a,
                    u'а':self.a,
                    
                    u'б':self.r6,
                    u'Б':self.r6,
                    '6':self.r6,

                    u'В':self.b,
                    u'в':self.b,
                    'B':self.b,
                    'b':self.b,
                    '8':self.b,

                    u'С':self.c,
                    'C':self.c,
                    'c':self.c,
                    u'с':self.c,

                    u'Г':self.rg,
                    u'г':self.rg,

                    u'Д':self.rd,
                    u'д':self.rd,

                    u'Е':self.e,
                    u'е':self.e,
                    u'Ё':self.e,
                    u'ё':self.e,
                    'e':self.e,
                    'E':self.e,

                    u'Ж':self.rj,
                    u'ж':self.rj,

                    u'З':self.r3,
                    u'з':self.r3,
                    '3':self.r3,

                    u'И':self.ri,
                    u'и':self.ri,

                    u'Й':self.rikr,
                    u'й':self.rikr,

                    u'К':self.k,
                    u'к':self.k,
                    'K':self.k,
                    'k':self.k,

                    u'Л':self.rl,
                    u'л':self.rl,

                    u'М':self.m,
                    u'м':self.m,
                    'M':self.m,
                    'm':self.m,

                    u'Н':self.h,
                    u'н':self.h,
                    'H':self.h,
                    'h':self.h,

                    u'О':self.o,
                    u'о':self.o,
                    'O':self.o,
                    'o':self.o,
                    '0':self.o,

                    u'П':self.rp,
                    u'п':self.rp,

                    u'Р':self.p,
                    u'р':self.p,
                    'P':self.p,
                    'p':self.p,

                    u'Т':self.t,
                    u'т':self.t,
                    'T':self.t,
                    't':self.t,

                    u'У':self.y,
                    u'у':self.y,
                    'Y':self.y,
                    'y':self.y,

                    u'Ф':self.rf,
                    u'ф':self.rf,

                    u'Х':self.x,
                    u'х':self.x,
                    'X':self.x,
                    'x':self.x,

                    u'Ч':self.rch,
                    u'ч':self.rch,

                    u'Ц':self.rc,
                    u'ц':self.rc,

                    u'Ш':self.rsh,
                    u'ш':self.rsh,

                    u'Щ':self.rcsh,
                    u'щ':self.rcsh,

                    u'Ь':self.rmz,
                    u'ь':self.rmz,

                    u'Ъ':self.rtz,
                    u'ъ':self.rtz,

                    u'Ы':self.rii,
                    u'ы':self.rii,

                    u'Э':self.rae,
                    u'э':self.rae,

                    u'Ю':self.ru,
                    u'ю':self.ru,

                    u'Я':self.rya,
                    u'я':self.rya,

                    'D':self.d,
                    'd':self.d,

                    'I':self.i,
                    'i':self.i,

                    'J':self.j,
                    'j':self.j,

                    'F':self.f,
                    'f':self.f,

                    'G':self.g,
                    'g':self.g,

                    'L':self.L,
                    'l':self.L,

                    'N':self.n,
                    'n':self.n,

                    'Q':self.q,
                    'q':self.q,

                    'R':self.r,
                    'r':self.r,

                    'S':self.r5,
                    's':self.r5,

                    'U':self.u,
                    'u':self.u,

                    'V':self.v,
                    'v':self.v,

                    'W':self.w,
                    'w':self.w,

                    'Z':self.z,
                    'z':self.z,

                    '1':self.r1,
                    '2':self.r2,
                    '4':self.r4,
                    '5':self.r5,
                    '7':self.r7,
                    '9':self.r9,
                    
                    ',':self.comma,
                    '.':self.point,
                    ';':self.c_point,
                    ':':self.p_point,
                    '!':self.emark,
                    '?':self.qmark,
                    '(':self.lbkt,
                    ')':self.rbkt,
                    '*':self.star,
                    "/":self.dr,
                    '+':self.plus,
                    '-':self.minus,
                    '=':self.equal,
                    '>':self.bigest,
                    '<':self.smollest,
                    u'№':self.num,
                    ' ':self.space,
                    }

    def ns(self, w = 1): #Определяет начало рисования символа
        w *= self.w_text #Относительная ширина
        x=self.nachTextX+self.sx*self.liter*2 #Начало рисования
        y=self.nachTextY
        y2 = self.sy #Высота символа
        x2 = self.sx * w #Ширина символа
        return x,y,x2,y2
#Символы узкого архитектурного шрифта 
    def a(self):#Символ А
        x,y,x2,y2 = self.ns()#Определяет нижнюю левую точку символа и его ширину (x2) и высоту (y2)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0.5,-1.0) , #линия / в А (Y координата п рограмме перевернута)
        (1.0,0,0.5,-1.0) , #линия \
        (0.25,-0.5,0.75,-0.5) , #линия -
        ]]

    def r6(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-0.75),
        (0,0,1.0,0),
        (0,-0.75,1.0,-0.75),
        (0,-1.0,1.0,-1.0),
        ]]

    def b(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,0,1.0,0),
        (0,-0.75,1.0,-0.75),
        (0,-1.0,1.0,-1.0),
        ]]

    def c(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,0,1.0,0),
        (0,-1.0,1.0,-1.0),
        ]]
    
    def rd(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0.5,-1.0),
        (1.0,0,0.5,-1.0),
        (-1.0/10.0,0,11.0/10.0,0),
        (-1.0/10.0,0,-1.0/10.0,1.0/8.0),
        (11.0/10.0,0,11.0/10.0,1.0/8.0),
        ]]
    
    def rg(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,-1.0,1.0,-1.0),
        ]]

    def e(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,0,1.0,0),
        (0,-0.75,1.0,-0.75),
        (0,-1.0,1.0,-1.0),
        ]]

    def r3(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,0,1.0,-1.0),
        (0,0,1.0,0),
        (0,-0.75,1.0,-0.75),
        (0,-1.0,1.0,-1.0),
        ]]

    def ri(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,-0.75,1.0,-1.0),
        ]]

    def rikr(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,-0.75,1.0,-1.0),
        (0.5,-16.0/15.0,1.0,-7.0/6.0),
        ]]

    def k(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,-0.25,1.0,-1.0),
        (0,-0.25,1.0,-0.25),
        (0,-0.25,1.0,0),
        ]]

    def rl(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,1.0/2,-1.0),
        (1.0,0,1.0/2,-1.0),
        ]]

    def m(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,-1.0,0.5,-0.75),
        (0.5,-0.75,1.0,-1.0),
        ]]

    def h(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,-0.75,1.0,-0.75),
        ]]

    def o(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,0,1.0,0),
        (0,-1.0,1.0,-1.0),
        ]]

    def rp(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,-1.0,1.0,-1.0),
        ]]

    def p(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,-0.25,1.0,-1.0),
        (0,-0.25,1.0,-0.25),
        (0,-1.0,1.0,-1.0),
        ]]
    
    def t(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.5,0,0.5,-1.0),
        (0,-1.0,1.0,-1.0),
        ]]

    def y(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,0,1.0,-1.0),
        (0,-0.25,0,-1.0),
        (0,-0.25,1.0,-0.25),
        (0,0,1.0,0),
        ]]

    def rf(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.25,0,-0.75),
        (1.0,-0.25,1.0,-0.75),
        (0,-0.25,1.0,-0.25),
        (0,-0.75,1.0,-0.75),
        (0.5,0,0.5,-1.0),
        ]]

    def x(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,1.0,-1.0),
        (0,-1.0,1.0,0),
        ]]

    def rch(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,0,1.0,-1.0),
        (0,-0.25,0,-1.0),
        (0,-0.25,1.0,-0.25),
        ]]

    def rc(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,0,11.0/10.0,0),
        (11.0/10.0,0,11.0/10.0,1/8.0),
        ]]

    def rsh(self):
        x,y,x2,y2 = self.ns(w = 1.5)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,0,1.0,0),
        (0.5,0,0.5,-1.0),
        ]]

    def rcsh(self):
        x,y,x2,y2 = self.ns(w = 1.5)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,0,11.0/10.0,0),
        (11.0/10.0,0,11.0/10.0,1/8.0),
        (0.5,0,0.5,-1.0),
        ]]

    def rmz(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-0.75),
        (0,0,1.0,0),
        (0,-0.75,1.0,-0.75),
        ]]

    def rtz(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-0.75),
        (0,0,1.0,0),
        (0,-0.75,1.0,-0.75),
        (0,-1.0,-1.0/6.0,-1.0),
        ]]

    def rii(self):
        x,y,x2,y2 = self.ns(1.5)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,0,0.66,0),
        (0,-0.75,0.66,-0.75),
        (0.66,0,0.66,-0.75),
        ]]

    def rae(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,0,1.0,-1.0),
        (0,0,1.0,0),
        (0,-0.5,1.0,-0.5),
        (0,-1.0,1.0,-1.0),
        ]]

    def ru(self):
        x,y,x2,y2 = self.ns(1.5)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0.33,0,0.33,-1.0),
        (0.33,0,1.0,0),
        (0.33,-1.0,1.0,-1.0),
        (0,-0.5,0.33,-0.5),
        ]]

    def rya(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,0,1.0,-1.0),
        (0,-0.25,0,-1.0),
        (0,-0.25,1.0,-0.25),
        (0,0,1.0,-0.25),
        (0,-1.0,1.0,-1.0),
        ]]
    
    def rj(self):
        x,y,x2,y2 = self.ns(w = 1.5)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.25,0,-1.0),
        (1.0,-0.25,1.0,-1.0),
        (0,-0.25,1.0,-0.25),
        (0.5,0,0.5,-1.0),
        (0.5,-0.25,0,0),
        (0.5,-0.25,1.0,0),
        ]]
#Английские буквы (не объявленные ранее)
    def d(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,0,0.66,0),
        (0,-1.0,0.66,-1.0),
        (0.66,0,1.0,-0.25),
        (0.66,-1.0,1.0,-0.75),
        (1.0,-0.75,1.0,-0.25),
        ]]

    def i(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.5,0,0.5,-1.0),
        (0,-1.0,1.0,-1.0),
        (0,0,1.0,0),
        ]]

    def j(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.5,0,0.5,-1.0),
        (0,-1.0,1.0,-1.0),
        (0,0,0.5,0),
        (0,0,0,-1.0/5.0),
        ]]
    
    def f(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,-0.75,1.0,-0.75),
        (0,-1.0,1.0,-1.0),
        ]]
    
    def g(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,0,1.0,0),
        (0,-1.0,1.0,-1.0),
        (1.0,0,1.0,-1.0/6.0),
        (7.0/6.0,-1.0/6.0,5.0/6.0,-1.0/6.0),
        ]]

    def L(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,0,1.0,0),
        ]]

    def n(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,-1.0,1.0,0),
        ]]

    def q(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,0,1.0,0),
        (0,-1.0,1.0,-1.0),
        (4.0/5.0,-1.0/10.0,6.0/5.0,1/10.0),
        ]]

    def r(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,-0.25,1.0,-1.0),
        (0,-0.25,1.0,-0.25),
        (0,-1.0,1.0,-1.0),
        (1.0,0,0,-0.25),
        ]]
    
    def u(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,0,1.0,0),
        ]]

    def v(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-1.0,0.5,0),
        (1.0,-1.0,0.5,0),
        ]]

    def w(self):
        x,y,x2,y2 = self.ns(1.5)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-1.0,0.25,0),
        (0.5,-1.0,0.25,0),
        (0.5,-1.0,0.75,0),
        (0.75,0,1.0,-1.0),
        ]]

    def z(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,-1.0,0,0),
        (0,-1.0,1.0,-1.0),
        (0,0,1.0,0),
        ]]
    
#Цифры (не заданные ранее)
    def r1(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,0,1.0,-1.0),
        (0,-0.75,1.0,-1.0),
        ]]
    
    def r2(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,-7.0/8.0,0,0),
        (1.0,-1.0,1.0,-7.0/8.0),
        (0,-7.0/8.0,0,-1.0),
        (0,-1.0,1.0,-1.0),
        (0,0,1.0,0),
        ]]

    def r4(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,0,1.0,-1.0),
        (1.0,-1.0,0,-0.25),
        (0,-0.25,1.0,-0.25),
        ]]

    def r5(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.75,0,-1.0),
        (1.0,0,1.0,-0.75),
        (0,0,1.0,0),
        (0,-0.75,1.0,-0.75),
        (0,-1.0,1.0,-1.0),
        ]]

    def r7(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,-1.0,0,0),
        (0,-7.0/8.0,0,-1.0),
        (0,-1.0,1.0,-1.0),
        ]]

    def r9(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,0,1.0,-1.0),
        (0,-0.25,0,-1.0),
        (0,-0.25,1.0,-0.25),
        (0,0,1.0,0),
        (0,-1.0,1.0,-1.0),
        ]]

#Знаки
    def comma(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,-0.33,1/5.0),
        ]]

    def point(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,-1.0/16.0,0),
        ]]

    def c_point(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,-0.33,1/5.0),
        (0,-1.0,-1.0/16.0,-1.0),
        ]]

    def p_point(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,-1.0/16.0,0),
        (0,-1.0,-1.0/16.0,-1.0),
        ]]

    def emark(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,-1.0/16.0,0),
        (-1.0/32.0,-1.0/10.0,-1.0/32.0,-1.0),
        ]]

    def qmark(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,-1.0/16.0,0),
        (1.0,-7.0/8.0,0,-0.25),
        (0,-0.25,0,-1.0/8.0),
        (1.0,-1.0,1.0,-7.0/8.0),
        (0,-7.0/8.0,0,-1.0),
        (0,-1.0,1.0,-1.0),
        
        ]]

    def lbkt(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,0,0,-1.0/4),
        (1.0,-1.0,0,-0.75),
        (0,-0.75,0,-0.25),
        ]]

    def rbkt(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,1.0,-0.25),
        (0,-1.0,1.0,-0.75),
        (1.0,-0.75,1.0,-0.25),
        ]]

    def star(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-1.0,1.0,-0.75),
        (1.0,-1.0,0,-0.75),
        (0.5,-1.0,0.5,-0.75),
        ]]

    def dr(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,-1.0,0,0),
        ]]

    def plus(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.5,-0.66,0.5,-0.33),
        (0,-0.5,1.0,-0.5),
        ]]

    def minus(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.5,1.0,-0.5),
        ]]

    def equal(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.33,1.0,-0.33),
        (0,-0.5,1.0,-0.5),
        ]]

    def bigest(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-1.0/3.5,1.0,-0.33),
        (0,-1.0/3.5,1.0,-0.25),
        ]]

    def smollest(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.33,1.0,-1.0/3.5),
        (0,-0.25,1.0,-1.0/3.5),
        ]]

    def num(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,-1.0,1.0,0),
        (7.0/6.0,-1.0,8.0/6.0,-1.0),
        (1.33,-1.0,1.33,-0.75),
        (1.33,-0.75,7.0/6.0,-0.75),
        (7.0/6.0,-0.75,7.0/6.0,-1.0),
        (1.33,-0.5,7.0/6.0,-0.5),
        ]]

    def space(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        ]]


class Font_TXT:
    def __init__(self):
        self.w_text = None
        self.nachTextX = None
        self.sx = None
        self.sy = None
        self.liter = None
        self.nachTextY = None
        self.liter_dict = {
                    u'А':self.a,
                    'A':self.a,
                    'a':self.am,
                    u'а':self.am,

                    u'б':self.rbm,
                    u'Б':self.rb,
                    
                    u'В':self.b,
                    u'в':self.rvm,
                    'B':self.b,
                    'b':self.bm,

                    u'С':self.c,
                    'C':self.c,
                    'c':self.cm,
                    u'с':self.cm,

                    u'Г':self.rg,
                    u'г':self.rgm,

                    u'Д':self.rd,
                    u'д':self.rdm,

                    u'Е':self.e,
                    u'е':self.em,
                    u'Ё':self.e,
                    u'ё':self.em,
                    'e':self.em,
                    'E':self.e,

                    u'Ж':self.rj,
                    u'ж':self.rjm,

                    u'З':self.rz,
                    u'з':self.rzm,

                    u'И':self.ri,
                    u'и':self.rim,

                    u'Й':self.rikr,
                    u'й':self.rikrm,

                    u'К':self.k,
                    u'к':self.rkm,
                    'K':self.k,
                    'k':self.km,

                    u'Л':self.rl,
                    u'л':self.rlm,

                    u'М':self.m,
                    u'м':self.rmm,
                    'M':self.m,
                    'm':self.mm,

                    u'Н':self.h,
                    u'н':self.rnm,
                    'H':self.h,
                    'h':self.hm,

                    u'О':self.ro,
                    u'о':self.om,
                    'O':self.o,
                    'o':self.om,

                    u'П':self.rp,
                    u'п':self.rpm,

                    u'Р':self.p,
                    u'р':self.pm,
                    'P':self.p,
                    'p':self.pm,

                    u'Т':self.t,
                    u'т':self.rtm,
                    'T':self.t,
                    't':self.tm,

                    u'У':self.ru,
                    u'у':self.rum,

                    u'Ф':self.rf,
                    u'ф':self.rfm,

                    u'Х':self.x,
                    u'х':self.xm,
                    'X':self.x,
                    'x':self.xm,

                    u'Ч':self.rtch,
                    u'ч':self.rtchm,

                    u'Ц':self.rtc,
                    u'ц':self.rtcm,

                    u'Ш':self.rsh,
                    u'ш':self.rshm,

                    u'Щ':self.rtsh,
                    u'щ':self.rtshm,

                    u'Ь':self.rmznak,
                    u'ь':self.rmznakm,

                    u'Ъ':self.rtznak,
                    u'ъ':self.rtznakm,

                    u'Ы':self.rii,
                    u'ы':self.riim,

                    u'Э':self.rae,
                    u'э':self.raem,

                    u'Ю':self.ryu,
                    u'ю':self.ryum,

                    u'Я':self.rya,
                    u'я':self.ryam,

                    'D':self.d,
                    'd':self.dm,

                    'I':self.i,
                    'i':self.im,

                    'J':self.j,
                    'j':self.jm,

                    'K':self.k,
                    'k':self.km,

                    'F':self.f,
                    'f':self.fm,

                    'G':self.g,
                    'g':self.gm,

                    'L':self.l,
                    'l':self.lm,

                    'N':self.n,
                    'n':self.nm,

                    'Q':self.q,
                    'q':self.qm,

                    'R':self.r,
                    'r':self.rm,

                    'S':self.s,
                    's':self.sm,

                    'U':self.u,
                    'u':self.um,

                    'V':self.v,
                    'v':self.vm,

                    'W':self.w,
                    'w':self.wm,

                    'Y':self.y,
                    'y':self.ym,

                    'Z':self.z,
                    'z':self.zm,

                    '1':self.n1,
                    '2':self.n2,
                    '3':self.rz,
                    '4':self.n4,
                    '5':self.n5,
                    '6':self.n6,
                    '7':self.n7,
                    '8':self.n8,
                    '9':self.n9,
                    '0':self.n0,
                    
                    ',':self.comma,
                    '.':self.point,
                    ';':self.c_point,
                    ':':self.p_point,
                    '!':self.emark,
                    '?':self.qmark,
                    '(':self.lbkt,
                    ')':self.rbkt,
                    '*':self.star,
                    "/":self.dr,
                    '+':self.plus,
                    '-':self.minus,
                    '=':self.equal,
                    '>':self.bigest,
                    '<':self.smollest,
                    u'№':self.num,
                    ' ':self.space,
                    }

    def ns(self, w = 1): #Определяет начало рисования символа
        w *= self.w_text
        x=self.nachTextX+self.sx*self.liter*2 #Начало рисования
        y=self.nachTextY
        y2 = self.sy
        x2 = self.sx * w
        return x,y,x2,y2
    
    def a(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-0.33),
        (1.0,0,1.0,-0.33),
        (0,-0.33,1.0,-0.33),
        (0,-0.33,0.5,-1.0),
        (1.0,-0.33,0.5,-1.0),
        ]]

    def am(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.33,0,-0.66),
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.66),
        (1.0,0,1.0,-1.0),
        (0.33,0,0.66,0),
        (0.33,0,0,-0.33),
        (0.66,0,1.0,-0.33),
        ]]

    def b(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,-1.0,0.66,-1.0),
        (0,0,0.66,0),
        (0,-0.5,0.66,-0.5),
        (0.66,-0.5,1.0,-0.33),
        (1.0,-0.33,1,-1.0/6.0),
        (1.0,-1.0/6.0,0.66,0),
        (0.66,-1.0,1.0,-5.0/6.0),
        (1.0,-5.0/6.0,1.0,-4.0/6.0),
        (1.0,-4.0/6.0,0.66,-0.5),
        ]]

    def bm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,-0.33,1.0,-0.66),
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.66),
        (0,0,0,-1.33),
        (0.33,0,0.66,0),
        (0.33,0,0,-0.33),
        (0.66,0,1.0,-0.33),
        ]]

    def c(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.33,0,-0.66),
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.66),
        (0.33,0,0.66,0),
        (0.33,0,0,-0.33),
        ((1/3.0)*2.0,0,1.0,-0.33),
        ]]

    def cm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.33,0,-0.66),
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,1.0,-1.0),
        (0.33,0,1.0,0),
        (0.33,0,0,-0.33),
        ]]

    def d(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,-0.33,1.0,-0.66),
        (-0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.66),
        (0,0,0,-1.0),
        (-0.33,0,0.66,0),
        (0.66,0,1.0,-0.33),
        ]]

    def dm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.33,0,-0.66),
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.66),
        (1.0,0,1.0,-1.33),
        (0.33,0,0.66,0),
        (0.33,0,0,-0.33),
        (0.66,0,1.0,-0.33),
        ]]

    def e(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,-1.0,1.0,-1.0),
        (0,0,1.0,0),
        (0,-0.5,0.5,-0.5),
        ]]

    def em(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.5,0.66,-0.5),
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.75),
        (0,-0.33,0,-0.66),
        (0.33,0,0.66,0),
        (0.33,0,0,-0.33),
        (0.66,-0.5,1.0,-0.75),
        ]]

    def f(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,-1.0,1.0,-1.0),
        (0,-0.5,0.5,-0.5),
        ]]

    def fm(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (-0.33,-0.5,0.66,-0.5),
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.75),
        (0,0,0,-0.66),
        ]]

    def g(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.33,0,-0.66),
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,1.0,-1.0),
        (0.33,0,1.0,0),
        (0.33,0,0,-0.33),
        (1.0,0,1.0,-0.5),
        (1.0,-0.5,0.75,-0.5),
        ]]

    def gm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.33,0,-0.66),
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.66),
        (1.0,0.33,1.0,-0.66),
        (0.33,0,1.0,0),
        (0.33,0,0,-0.33),
        (0.66,0.66,1.0,0.33),
        (0.33,0.66,0.66,0.66),
        (0.33,0.66,0,0.33),
        ]]

    def h(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,-0.75,1.0,-0.75),
        ]]

    def hm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.66),
        (0,0,0,-1.33),
        (1.0,0,1.0,-0.66),
        ]]

    def i(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.33,0,0.66,0),
        (0.33,-1.0,0.66,-1.0),
        (0.5,0,0.5,-1.0),
        ]]

    def im(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.5,0,0.5,-1.0),
        (0.5,-1.33,0.5,-3.5/3.0),
        ]]

    def j(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,-0.33,1.0,-1.0),
        (0.33,0,0.66,0),
        (0.33,0,0,-0.33),
        (0.66,0,1.0,-0.33),
        ]]

    def jm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,-0.33,1.0,-1.0),
        (0.33,0,0.66,0),
        (0.33,0,0,-0.33),
        (0.66,0,1.0,-0.33),
        (1.0,-1.33,1.0,-3.5/3.0),
        ]]
    
    def k(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,-0.5,0.33,-0.5),
        (0.33,-0.5,1.0,-1.0),
        (0.33,-0.5,1.0,0),
        ]]

    def km(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.33),
        (0,-0.5,0.33,-0.5),
        (0.33,-0.5,1.0,-1.0),
        (0.33,-0.5,1.0,0),
        ]]

    def l(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,0,1.0,0),
        ]]

    def lm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.5,-0.25,0.5,-1.0),
        (0.5,-0.25,0.75,0),
        ]]

    def m(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,-1.0,0.5,-0.5),
        (0.5,-0.5,1.0,-1.0),
        ]]

    def mm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.75,0.25,-1.0),
        (0.25,-1.0,0.5,-0.75),
        (0.5,-0.75,0.75,-1.0),
        (0.75,-1.0,1.0,-0.75),
        (0,0,0,-1.0),
        (1.0,0,1.0,-0.75),
        (0.5,-0.75,0.5,-0.5),
        ]]

    def n(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,-1.0,1.0,0),
        ]]

    def nm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.66),
        (0,0,0,-1.0),
        (1.0,0,1.0,-0.66),
        ]]

    def o(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,0,1.0,0),
        (0,-1.0,1.0,-1.0),
        ]]

    def om(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.33,0,-0.66),
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.66),
        (1.0,-0.66,1.0,-0.33),
        (0.33,0,0.66,0),
        (0.33,0,0,-0.33),
        (0.66,0,1.0,-0.33),
        ]]

    def p(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,-1.0,0.66,-1.0),
        (0,-0.5,0.66,-0.5),
        (0.66,-1.0,1.0,-5.0/6.0),
        (1.0,-5.0/6.0,1.0,-4.0/6.0),
        (1.0,-4.0/6.0,0.66,-0.5),
        ]]

    def pm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,-0.33,1.0,-0.66),
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.66),
        (0,0.5,0,-1.0),
        (0,0,0.66,0),
        (0.66,0,1.0,-0.33),
        ]]
    
    def q(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.33,0,-0.66),
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.66),
        (1.0,-0.66,1.0,-0.33),
        (0.33,0,0.66,0),
        (0.33,0,0,-0.33),
        (0.66,0,1.0,-0.33),
        (0.66,-0.33,1.0,0),
        ]]
    
    def qm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.33,0,-0.66),
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.66),
        (1.0,0.66,1.0,-1.0),
        (0.33,0,1.0,0),
        (0.33,0,0,-0.33),
        ]]

    def r(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,-1.0,0.66,-1.0),
        (0,-0.5,0.66,-0.5),
        (0.66,-1.0,1.0,-5.0/6.0),
        (1.0,-5.0/6.0,1.0,-4.0/6.0),
        (1.0,-4.0/6.0,0.66,-0.5),
        (0.33,-0.5,1.0,0),
        ]]
    
    def rm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.66),
        (0,0,0,-1.0),
        ]]

    def s(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-5.0/6.0,1.0/6.0,-1.0),
        (1.0/6.0,-1.0,5.0/6.0,-1.0),
        (5.0/6.0,-1.0,1.0,-5.0/6.0),
        (0,-5.0/6.0,1.0,-1.0/6.0),
        (1.0/6.0,0,5.0/6.0,0),
        (1.0/6.0,0,0,-1.0/6.0),
        (5.0/6.0,0,1.0,-1.0/6.0),
        ]]

    def sm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.75,0.33,-1.0),
        (0.33,-1.0,1.0,-1.0),
        (0,-0.75,0.33,-0.5),
        (0.33,-0.5,0.66,-0.5),
        (0.66,-0.5,1.0,-0.25),
        (1.0,-0.25,0.66,0),
        (0.66,0,0,0),
        ]]

    def t(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0/2,0,1.0/2,-1.0),
        (0,-1.0,1.0,-1.0),
        ]]

    def tm(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.5,-0.25,0.5,-1.0),
        (0,-0.66,1.0,-0.66),
        (0.5,-0.25,0.75,0),
        (0.75,0,1.0,-0.25),
        ]]

    def u(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.33,0,-1.0),
        (1.0,-0.33,1.0,-1.0),
        (0.33,0,0.66,0),
        (0.33,0,0,-0.33),
        (0.66,0,1.0,-0.33),
        ]]

    def um(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.33,0,-1.0),
        (0,-0.33,0.33,0),
        (0.33,0,0.66,0),
        (1.0,-0.33,0.66,0),
        (1.0,0,1.0,-1.0),
        ]]

    def v(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-1.0,0.5,0),
        (0.5,0,1.0, -1),
        ]]

    def vm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-1.0,0.5,0),
        (0.5,0,1.0, -1.0),
        ]]

    def w(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-1.0,0.25,0),
        (0.25,0,0.5, -1/2.0),
        (0.5, -1/2.0,0.75, 0),
        (0.75, 0,1.0, -1),
        ]]

    def wm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-1.0,0.25,0),
        (0.25,0,0.5, -1.0),
        (0.5, -1.0,0.75, 0),
        (0.75, 0,1.0, -1.0),
        ]]

    def x(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-1.0,1.0,0),
        (0,0,1.0,-1.0),
        ]]

    def xm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-1.0,1.0,0),
        (0,0,1.0,-1.0),
        ]]

    def y(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-1.0,0.5,-0.5),
        (1.0, -1,0.5,-0.5),
        (0.5,-0.5,0.5,0),
        ]]

    def ym(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-1.0,0.5,-0.5),
        (0,0,1.0,-1.0),
        ]]

    def z(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,-1.0,0,0),
        (0,-1.0,1.0,-1.0),
        (0,0,1.0,0),
        ]]

    def zm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,-1.0,0,0),
        (0,-1.0,1.0,-1.0),
        (0,0,1.0,0),
        ]]

#Русские буквы (которые не встречались ранее)

    def rb(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,-1.0,0.66,-1.0),
        (0,0,0.66,0),
        (0,-0.5,0.66,-0.5),
        (0.66,-0.5,1.0,-0.33),
        (1.0,-0.33,1.0,-1.0/6.0),
        (1.0,-1.0/6.0,0.66,0),
        (0.66,-1.0,0.66,-5.0/6.0),
        ]]

    def rbm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,-1.0,0.66,-1.0),
        (0,0,0.66,0),
        (0,-0.5,0.66,-0.5),
        (0.66,-0.5,1.0,-0.33),
        (1.0,-0.33,1.0,-1.0/6.0),
        (1.0,-1.0/6.0,0.66,0),
        ]]

    def rvm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,-1.0,0.66,-1.0),
        (0,0,0.66,0),
        (0,-0.5,0.66,-0.5),
        (0.66,-0.5,1.0,-0.33),
        (1.0,-0.33,1.0,-1.0/6.0),
        (1.0,-1.0/6.0,0.66,0),
        (0.66,-1.0,1.0,-5.0/6.0),
        (1.0,-5.0/6.0,1.0,-4.0/6.0),
        (1.0,-4.0/6.0,0.66,-0.5),
        ]]
    
    def rg(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,-1.0,1.0,-1.0),
        (1.0,-1.0,1.0,-5.0/6.0),
        ]]

    def rgm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,-1.0,1.0,-1.0),
        ]]

    def rd(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (-1.0/6.0,0,7.0/6.0,0),
        (-1.0/6.0,0,-1.0/6.0,1/6.0),
        (7.0/6.0,1/6.0,7.0/6.0,0),
        (0,0,0,-0.5),
        (0,-0.5,0.33,-1.0),
        (0.33,-1.0,1.0,-1.0),
        (1.0,-1.0,1.0,0),
        ]]

    def rdm(self):
        x,y,x2,y2 = self.ns(0.8)
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (-1.0/6.0,0,7.0/6.0,0),
        (-1.0/6.0,0,-1.0/6.0,1.0/6.0),
        (7.0/6.0,1.0/6.0,7.0/6.0,0),
        (0,0,0,-0.5),
        (0,-0.5,0.33,-1.0),
        (0.33,-1.0,1.0,-1.0),
        (1.0,-1.0,1.0,0),
        ]]

    def rj(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,1.0,-1.0),
        (0,-1.0,1.0,0),
        (0.5,0,0.5,-1.0),
        ]]

    def rjm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,1.0,-1.0),
        (0,-1.0,1.0,0),
        (0.5,0,0.5,-1.0),
        ]]

    def rz(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.5,-0.5,0.66,-0.5),
        (0.33,-1.0,0.66,-1.0),
        (0.33,0,0.66,0),
        (0.66,-0.5,1.0,-0.33),
        (1.0,-0.33,1.0,-1.0/6.0),
        (1.0,-1.0/6.0,0.66,0),
        (0.66,-1.0,1.0,-5.0/6.0),
        (1.0,-5.0/6.0,1.0,-4.0/6.0),
        (1.0,-4.0/6.0,0.66,-0.5),
        (0.33,-1.0,0,-5.0/6.0),
        (0.33,0,0,-1.0/6.0),
        ]]

    def rzm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.5,-0.5,0.66,-0.5),
        (0.33,-1.0,0.66,-1.0),
        (0.33,0,0.66,0),
        (0.66,-0.5,1.0,-0.33),
        (1.0,-0.33,1.0,-1.0/6.0),
        (1.0,-1.0/6.0,0.66,0),
        (0.66,-1.0,1.0,-5.0/6.0),
        (1.0,-5.0/6.0,1.0,-4.0/6.0),
        (1.0,-4.0/6.0,0.66,-0.5),
        (0.33,-1.0,0,-5.0/6.0),
        (0.33,0,0,-1.0/6.0),
        ]]

    def ri(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,0,1.0,-0.66),
        ]]

    def rim(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,0,1.0,-0.66),
        ]]

    def rikr(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,0,1.0,-0.66),
        (0.33,-1.0,0.66,-1.0),
        ]]

    def rikrm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,0,1.0,-0.66),
        (0.33,-1.0,0.66,-1.0),
        ]]

    def rkm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,-0.5,0.33,-0.5),
        (0.33,-0.5,1.0,-1.0),
        (0.33,-0.5,1.0,0),
        ]]

    def rl(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.25,0,0.75,-1.0),
        (0.75,-1.0,1.0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,0,0.25,0),
        ]]

    def rlm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0.5,-1.0),
        (0.5,-1.0,1.0,-1.0),
        (1.0,0,1.0,-1.0),
        ]]

    def rmm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,-1.0,0.5,-0.5),
        (0.5,-0.5,1.0,-1.0),
        ]]

    def rnm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,-1.+0.25,1.0,-1.+0.25),
        ]]
    
    def ro(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.33,0,-0.66),
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.66),
        (1.0,-0.66,1.0,-0.33),
        (0.33,0,0.66,0),
        (0.33,0,0,-0.33),
        (0.66,0,1.0,-0.33),
        ]]

    def rp(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,-1.0,1.0,-1.0),
        ]]

    def rpm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,-1.0,1.0,-1.0),
        ]]

    def rtm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0/2,0,1.0/2,-1.0),
        (0,-1.0,1.0,-1.0),
        ]]

    def ru(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-1.0,0,-0.66),
        (0,-0.66,0.25,-0.5),
        (1.0,-1.0,1.0,-0.25),
        (1.0,-0.25,0.75,0),
        (0.75,0,0.25,0),
        (0.25,0,0,-0.25),
        (0.25,-0.5,1.0,-0.5),
        ]]

    def rum(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-1.0,0.5,-0.5),
        (1.0,-1.0,1.0,-0.25),
        (1.0,-0.25,0.75,0),
        (0.75,0,0.25,0),
        (0.25,0,0,-0.25),
        (0.5,-0.5,1.0,-0.5),
        ]]

    def rf(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.5,-1.0,0.5,0),
        (0.25,-1.0,0.75,-1.0),
        (0.75,-1.0,1.0,-0.75),
        (1.0,-0.75,1.0,-0.5),
        (1.0,-0.5,0.75,-0.25),
        (0.75,-0.25,0.25,-0.25),
        (0.25,-0.25,0,-0.5),
        (0,-0.5,0,-0.75),
        (0,-0.75,0.25,-1.0),
        ]]

    def rfm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.5,-1.0,0.5,0),
        (0.25,-1.0,0.75,-1.0),
        (0.75,-1.0,1.0,-0.75),
        (1.0,-0.75,1.0,-0.5),
        (1.0,-0.5,0.75,-0.25),
        (0.75,-0.25,0.25,-0.25),
        (0.25,-0.25,0,-0.5),
        (0,-0.5,0,-0.75),
        (0,-0.75,0.25,-1.0),
        ]]

    def rtc(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,0,7.0/6.0,0),
        (7.0/6.0,0,7.0/6.0,1.0/6.0),
        ]]

    def rtcm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,0,7.0/6.0,0),
        (7.0/6.0,0,7.0/6.0,1.0/6.0),
        ]]

    def rtch(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-1.0,0,-0.66),
        (0,-0.66,0.25,-0.5),
        (1.0,0,1.0,-1.0),
        (0.25,-0.5,1.0,-0.5),
        ]]

    def rtchm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-1.0,0,-0.5),
        (1.0,0,1.0,-1.0),
        (0,-0.5,1.0,-0.5),
        ]]

    def rsh(self):
        x,y,x2,y2 = self.ns(1.2)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0.5,-0.5,0.5,0),
        (0,0,1.0,0),
        ]]

    def rshm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0.5,-0.5,0.5,0),
        (0,0,1.0,0),
        ]]

    def rtsh(self):
        x,y,x2,y2 = self.ns(1.2)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0.5,-0.5,0.5,0),
        (0,0,7.0/6.0,0),
        (7.0/6.0,0,7.0/6.0,1.0/6.0),
        ]]

    def rtshm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0.5,-0.5,0.5,0),
        (0,0,7.0/6.0,0),
        (7.0/6.0,0,7.0/6.0,1.0/6.0),
        ]]

    def rtznak(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,-1.0,-1.0/6.0,-1.0),
        (0,0,0.66,0),
        (0,-0.5,0.66,-0.5),
        (0.66,-0.5,1.0,-0.33),
        (1.0,-0.33,1.0,-1.0/6.0),
        (1.0,-1.0/6.0,0.66,0),
        (-1.0/6.0,-1.0,-1.0/6.0,-5.0/6.0),
        ]]

    
    def rtznakm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,-1.0,-1.0/6.0,-1.0),
        (0,0,0.66,0),
        (0,-0.5,0.66,-0.5),
        (0.66,-0.5,1.0,-0.33),
        (1.0,-0.33,1.0,-1.0/6.0),
        (1.0,-1.0/6.0,0.66,0),
        (-1.0/6.0,-1.0,-1.0/6.0,-5.0/6.0),
        ]]

    def rii(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (7.0/6.0,-1.0,7.0/6.0,0),
        (0,0,0.66,0),
        (0,-0.5,0.66,-0.5),
        (0.66,-0.5,1.0,-0.33),
        (1.0,-0.33,1.0,-1.0/6.0),
        (1.0,-1.0/6.0,0.66,0),
        ]]

    def riim(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (7.0/6.0,-1.0,7.0/6.0,0),
        (0,0,0.66,0),
        (0,-0.5,0.66,-0.5),
        (0.66,-0.5,1.0,-0.33),
        (1.0,-0.33,1.0,-1.0/6.0),
        (1.0,-1.0/6.0,0.66,0),
        ]]

    def rmznak(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,0,0.66,0),
        (0,-0.5,0.66,-0.5),
        (0.66,-0.5,1.0,-0.33),
        (1.0,-0.33,1.0,-1.0/6.0),
        (1.0,-1.0/6.0,0.66,0),
        ]]

    def rmznakm(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (0,0,0.66,0),
        (0,-0.5,0.66,-0.5),
        (0.66,-0.5,1.0,-0.33),
        (1.0,-0.33,1.0,-1.0/6.0),
        (1.0,-1.0/6.0,0.66,0),
        ]]

    def rae(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.33,-0.5,1.0,-0.5),
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.66),
        (1.0,-0.66,1.0,-0.33),
        (0.33,0,0.66,0),
        (0.33,0,0,-0.33),
        (0.66,0,1.0,-0.33),
        ]]

    def raem(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.33,-0.5,1.0,-0.5),
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.66),
        (1.0,-0.66,1.0,-0.33),
        (0.33,0,0.66,0),
        (0.33,0,0,-0.33),
        (0.66,0,1.0,-0.33),
        ]]

    def ryu(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.33,0,-0.66),
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.66),
        (1.0,-0.66,1.0,-0.33),
        (0.33,0,0.66,0),
        (0.33,0,0,-0.33),
        (0.66,0,1.0,-0.33),
        (-1.0/6.0,-0.5,0,-0.5),
        (-1.0/6.0,0,-1.0/6.0,-1.0),
        ]]

    def ryum(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.33,0,-0.66),
        (0,-0.66,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-0.66),
        (1.0,-0.66,1.0,-0.33),
        (0.33,0,0.66,0),
        (0.33,0,0,-0.33),
        (0.66,0,1.0,-0.33),
        (-1.0/6.0,-0.5,0,-0.5),
        (-1.0/6.0,0,-1.0/6.0,-1.0),
        ]]

    def rya(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,0,1.0,-1.0),
        (1.0,-1.0,0.33,-1.0),
        (0.33,-1.0,0,-0.75),
        (0,-0.75,0,-0.5),
        (0,-0.5,0.25, -1/4.0),
        (0.25, -1/4.0,1.0, -1/4.0),
        (0.5, -1/4.0,0, 0),
        ]]

    def ryam(self):
        x,y,x2,y2 = self.ns()
        y2 *= 0.75
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,0,1.0,-1.0),
        (1.0,-1.0,0.33,-1.0),
        (0.33,-1.0,0,-0.75),
        (0,-0.75,0,-0.5),
        (0,-0.5,0.25, -0.25),
        (0.25, -0.25,1.0, -0.25),
        (0.5, -0.25,0, 0),
        ]]

    #Цифры
    def n1(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.33,0,0.66,0),
        (0.5,-1.0,0.33,-5.0/6.0),
        (0.5,0,0.5,-1.0),
        ]]

    def n2(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-5.0/6.0,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-5.0/6.0),
        (1.0,-5.0/6.0,1.0,-0.66),
        (1.0,-0.66,0.66,-0.5),
        (0.66,-0.5,0.33,-0.5),
        (0.33,-0.5,0,-0.33),
        (0,-0.33,0,0),
        (0,0,1.0,0),
        ]]

    def n4(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,-1.0,1.0,0),
        (1.0,-1.0,0,-0.5),
        (0,-0.5,7.0/6.0,-0.5),
        ]]

    def n5(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,-1.0,0,-1.0),
        (0,-1.0,0,-0.75),
        (0,-0.75,0.66,-0.75),
        (0.66,-0.75,1.0,-0.5),
        (1.0,-0.5,1.0,-0.25),
        (1.0,-0.25,0.66,0),
        (0.66,0,0.33,0),
        (0.33,0,0,-0.25),
        ]]

    def n6(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.66,-1.0,0.33,-1.0),
        (0.33,-1.0,0,-0.75),
        (0,-0.75,0,-0.25),
        (0.66,-0.5,1.0,-0.33),
        (1.0,-0.33,1.0,-0.25),
        (1.0,-0.25,0.66,0),
        (0.66,0,0.33,0),
        (0.33,0,0,-0.25),
        (0,-0.5,0.66,-0.5),
        ]]

    def n7(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-1.0,1.0,-1.0),
        (1.0,-1.0,0,0),
        ]]

    def n8(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-5.0/6.0,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-5.0/6.0),
        (1.0,-5.0/6.0,1.0,-0.66),
        (1.0,-0.66,0.66,-0.5),
        (0.66,-0.5,0.33,-0.5),
        (0.33,-0.5,0,-0.33),
        (0,-0.33,0,-1.0/6.0),
        (0,-1.0/6.0,0.33,0),
        (0.33,0,0.66,0),
        (0.66,0,1.0,-1.0/6.0),
        (1.0,-1.0/6.0,1.0,-0.33),
        (1.0,-0.33,0.66,-0.5),
        (0,-5.0/6.0,0,-0.66),
        (0,-0.66,0.33,-0.5),
        ]]

    def n9(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-5.0/6.0,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-5.0/6.0),
        (1.0,-5.0/6.0,1.0,-1.0/6.0),
        (1.0,-0.5,0.33,-0.5),
        (0.33,0,0.66,0),
        (0.66,0,1.0,-1.0/6.0),
        (0,-5.0/6.0,0,-0.66),
        (0,-0.66,0.33,-0.5),
        ]]

    def n0(self):
        x,y,x2,y2 = self.ns(0.8)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-1.0/6.0,0,-5.0/6.0),
        (0,-5.0/6.0,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-5.0/6.0),
        (1.0,-5.0/6.0,1.0,-1.0/6.0),
        (0.33,0,0.66,0),
        (0.33,0,0,-1.0/6.0),
        (0.66,0,1.0,-1.0/6.0),
        ]]

    #Знаки препинания
    def point(self):
        x,y,x2,y2 = self.ns(0.8)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.5,0,0.5,-1.0/6.0),
        ]]

    def comma(self):
        x,y,x2,y2 = self.ns(0.8)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.5,0,0.5,-1.0/6.0),
        (0.5,0,0,0.33),
        ]]

    def c_point(self):
        x,y,x2,y2 = self.ns(0.8)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.5,0,0.5,-1.0/6.0),
        (0.5,0,0,0.33),
        (0.5,-0.33,0.5,-0.5),
        ]]

    def p_point(self):
        x,y,x2,y2 = self.ns(0.8)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.5,0,0.5,-1.0/6.0),
        (0.5,-0.33,0.5,-0.5),
        ]]

    def emark(self):
        x,y,x2,y2 = self.ns(0.8)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.5,0,0.5,-1.0/6.0),
        (0.5,-0.33,0.5,-1.0),
        ]]
    
    def space(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        ]]

    def qmark(self):
        x,y,x2,y2 = self.ns(0.8)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-5.0/6.0,0.33,-1.0),
        (0.33,-1.0,0.66,-1.0),
        (0.66,-1.0,1.0,-5.0/6.0),
        (1.0,-5.0/6.0,0.5,-0.5),
        (0.5,0,0.5,-1.0/6.0),
        (0.5,-0.33,0.5,-0.5),
        ]]

    def lbkt(self):
        x,y,x2,y2 = self.ns(0.5)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,0,0,-0.33),
        (0,-0.33,0,-0.66),
        (0,-0.66,1.0,-1.0),
        ]]

    def rbkt(self):
        x,y,x2,y2 = self.ns(0.5)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,1.0,-0.33),
        (1.0,-0.33,1.0,-0.66),
        (1.0,-0.66,0,-1.0),
        ]]

    def star(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.33,1.0,-0.66),
        (1.0,-0.33,0,-0.66),
        (0,-0.5,1.0,-0.5),
        ]]

    def dr(self):
        x,y,x2,y2 = self.ns(0.8)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,1.0,-1.0),
        ]]

    def plus(self):
        x,y,x2,y2 = self.ns(0.8)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0.5,-0.33,0.5,-0.66),
        (0,-0.5,1.0,-0.5),
        ]]
    
    def minus(self):
        x,y,x2,y2 = self.ns(0.8)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.5,1.0,-0.5),
        ]]

    def equal(self):
        x,y,x2,y2 = self.ns(0.8)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.33,1.0,-0.33),
        (0,-0.66,1.0,-0.66),
        ]]

    def smollest(self):
        x,y,x2,y2 = self.ns(0.8)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,-0.5,1.0,-0.33),
        (0,-0.5,1.0,-0.66),
        ]]

    def bigest(self):
        x,y,x2,y2 = self.ns(0.8)
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (1.0,-0.5,0,-0.33),
        (1.0,-0.5,0,-0.66),
        ]]

    def num(self):
        x,y,x2,y2 = self.ns()
        return [ [x+x2*ax, y+y2*ay, x+x2*bx, y+y2*by] for (ax,ay,bx,by) in [
        (0,0,0,-1.0),
        (1.0,0,1.0,-1.0),
        (0,-1.0,1.0,0),
        (7.0/6.0,-1.0,1.33,-1.0),
        (1.33,-1.0,1.33,-0.75),
        (1.33,-0.75,7.0/6.0,-0.75),
        (7.0/6.0,-0.75,7.0/6.0,-1.0),
        (1.33,-0.5,7.0/6.0,-0.5),
        ]]
