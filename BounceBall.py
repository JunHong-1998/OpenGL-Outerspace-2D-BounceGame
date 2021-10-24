from OpenGL.GL import *
import math

class BounceBall:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.r = 1
        self.hp = 3
        self.Lvl = 1
        self.coords_reset = 0,0
        self.LEFT = False
        self.RIGHT = False
        self.UP = False
        self.jumpCOUNT = 0
        self.vel = 0
        self.Load_show = False
        self.map = None

    def RESET(self, map):
        x = y = 0
        if self.Lvl==1:
            self.hp = 3
            x, y = -215, 18
        elif self.Lvl==2:
            x,y = 16, -1
        elif self.Lvl==3:
            x, y = 148, -19
        self.x, self.y = x, y
        self.coords_reset = x, y
        self.map = map

    def draw(self):
        if not self.Load_show:
            self.Sphere(self.x, self.y, self.z, self.r)

    def update(self, left, right, up, reset):
        if reset:
            self.hp -= 1
            if self.hp>0:
                self.x, self.y = self.coords_reset
        if left and self.LEFT:
            self.x -=0.5
        elif right and self.RIGHT:
            self.x += 0.5
        if up:
            self.UP = True

    def MAPupdate(self, Door):
        err, bottom, top, g, dt, topRANK, bottomRANK, door, door2 = 0.5,0,0, 10, 0.08, 0,0, Door, Door
        self.LEFT, self.RIGHT = True, True
        if self.Lvl>1:
            door, door2 = Door[0], Door[1]
        for i in range(len(self.map)):
            brd = self.map[i]
            if brd[0]-self.r<self.x<brd[0]+brd[2]+self.r:
                if brd[4] == 5 and self.y<brd[1]-brd[3]:
                    if self.Lvl == 3:
                        if self.y < -5 and brd[1] < -5:
                            top, topRANK = brd[1] - brd[3], 6
                        elif self.y >= -5 and brd[1] >= -5:
                            top, topRANK = brd[1] - brd[3], 6
                    else:
                        top, topRANK = brd[1] - brd[3], 6
                elif brd[4] == 7 and self.y < brd[1] - brd[3] and topRANK<6:
                    if self.Lvl == 3:
                        if self.y < -5 and brd[1] < -5:
                            top, topRANK = brd[1] - brd[3], 5
                        elif self.y >= -5 and brd[1] >= -5:
                            top, topRANK = brd[1] - brd[3], 5
                    else:
                        top, topRANK = brd[1] - brd[3], 5
                elif brd[4] == 6 and self.y < brd[1] - brd[3] and topRANK<5:
                    if self.Lvl == 3:
                        if self.y < -5 and brd[1] < -5:
                            top, topRANK = brd[1] - brd[3], 4
                        elif self.y >= -5 and brd[1] >= -5:
                            top, topRANK = brd[1] - brd[3], 4
                    else:
                        top, topRANK = brd[1] - brd[3], 4
                elif brd[4] == 0 and self.y < brd[1] - brd[3] and topRANK<4:
                    if self.Lvl == 3:
                        if self.y < -5 and brd[1] < -5:
                            top, topRANK = brd[1] - brd[3], 3
                        elif self.y >= -5 and brd[1] >= -5:
                            top, topRANK = brd[1] - brd[3], 3
                    else:
                        top, topRANK = brd[1] - brd[3], 3
                elif brd[4] == 1 and topRANK<3:
                    if self.Lvl == 3:
                        if self.y < -5 and brd[1] < -5:
                            top, topRANK = brd[1] - brd[3], 2
                        elif self.y >= -5 and brd[1] >= -5:
                            top, topRANK = brd[1] - brd[3], 2
                    else:
                        top, topRANK = brd[1] - brd[3], 2
                elif brd[4] == 2 and topRANK<2:
                    if self.Lvl ==3:
                        if self.y<-5 and brd[1]<-5:
                            top, topRANK = brd[1] - brd[3], 1
                        elif self.y>=-5 and brd[1]>=-5:
                            top, topRANK = brd[1] - brd[3], 1
                    else:
                        top, topRANK = brd[1] - brd[3], 1

                if brd[4] == 5 and self.y > brd[1] - self.r:
                    if self.Lvl == 3:
                        if self.y < -5 and brd[1] < -5:
                            bottom, bottomRANK = brd[1], 8
                        elif self.y >= -5 and brd[1] >= -5:
                            bottom, bottomRANK = brd[1], 8
                    else:
                        bottom, bottomRANK = brd[1], 8
                elif brd[4] == 7 and self.y > brd[1] - self.r and bottomRANK<8 and brd[0] + self.r / 2 < self.x < brd[0] + brd[2] + self.r:
                    if self.Lvl == 3:
                        if self.y < -5 and brd[1] < -5:
                            bottom, bottomRANK = brd[1], 7
                        elif self.y >= -5 and brd[1] >= -5:
                            bottom, bottomRANK = brd[1], 7
                    else:
                        bottom, bottomRANK = brd[1], 7
                elif brd[4] == 6 and self.y > brd[1] - self.r and bottomRANK<7 and brd[0] - self.r < self.x < brd[0] + brd[2] - self.r / 2:
                    if self.Lvl == 3:
                        if self.y < -5 and brd[1] < -5:
                            bottom, bottomRANK = brd[1], 6
                        elif self.y >= -5 and brd[1] >= -5:
                            bottom, bottomRANK = brd[1], 6
                    else:
                        bottom, bottomRANK = brd[1], 6
                elif brd[4] == 0 and self.y > brd[1] - self.r and bottomRANK<6:
                    if self.Lvl == 3:
                        if self.y < -5 and brd[1] < -5:
                            bottom, bottomRANK = brd[1], 5
                        elif self.y >= -5 and brd[1] >= -5:
                            bottom, bottomRANK = brd[1], 5
                    else:
                        bottom, bottomRANK = brd[1], 5
                elif brd[4] == -1 and bottomRANK<5:
                    if self.Lvl == 3:
                        if self.y < -5 and brd[1] < -5:
                            bottom, bottomRANK = brd[1], 4
                        elif self.y >= -5 and brd[1] >= -5:
                            bottom, bottomRANK = brd[1], 4
                    else:
                        bottom, bottomRANK = brd[1], 4
                elif brd[4] == -4 and brd[0] - self.r < self.x < brd[0] + brd[2] - self.r / 2 and bottomRANK < 4:
                    if self.Lvl == 3:
                        if self.y < -5 and brd[1] < -5:
                            bottom, bottomRANK = brd[1], 3
                        elif self.y >= -5 and brd[1] >= -5:
                            bottom, bottomRANK = brd[1], 3
                    else:
                        bottom, bottomRANK = brd[1], 3
                elif brd[4] == -3 and brd[0] + self.r / 2 < self.x < brd[0] + brd[2] + self.r and bottomRANK < 3:
                    if self.Lvl == 3:
                        if self.y < -5 and brd[1] < -5:
                            bottom, bottomRANK = brd[1], 2
                        elif self.y >= -5 and brd[1] >= -5:
                            bottom, bottomRANK = brd[1], 2
                    else:
                        bottom, bottomRANK = brd[1], 2
                elif brd[4]==-2 and bottomRANK<2 and brd[0]-self.r/4<self.x<brd[0]+brd[2]+self.r/4:
                    if self.Lvl ==3:
                        if self.y<-5 and brd[1]<-5:
                            bottom, bottomRANK = brd[1], 1
                        elif self.y>=-5 and brd[1]>=-5:
                            bottom, bottomRANK = brd[1], 1
                    else:
                        bottom, bottomRANK = brd[1], 1
            if brd[0]-self.r-err<self.x<=brd[0]+self.r and brd[1]-brd[3]-self.r<self.y<brd[1]+self.r or door[0]-self.r-err<self.x<=door[0]+self.r and not door[1] and not self.Lvl==3\
                    or door2[0]-self.r-err<self.x<=door2[0]+self.r and not door2[1] and not self.Lvl==3:
                self.RIGHT = False
            elif brd[0]+brd[2]-self.r-err<self.x<=brd[0]+brd[2]+self.r and brd[1]-brd[3]-self.r<self.y<brd[1]+self.r or door[0]+door[2]-self.r-err<self.x<=door[0]+door[2]+self.r and not door[1] and not self.Lvl==3\
                    or door2[0]+door2[2]-self.r-err<self.x<=door2[0]+door2[2]+self.r and not door2[1] and not self.Lvl==3:
                self.LEFT = False
            if self.Lvl==3:
                if self.y>=7:
                    if door[0]-self.r-err<self.x<=door[0]+self.r and not door[1] or door2[0]-self.r-err<self.x<=door2[0]+self.r and not door2[1]:
                        self.RIGHT = False
                    elif door[0]+door[2]-self.r-err<self.x<=door[0]+door[2]+self.r and not door[1] or door2[0]+door2[2]-self.r-err<self.x<=door2[0]+door2[2]+self.r and not door2[1]:
                        self.LEFT = False
        if bottom==0:   #No bottom set
            bottom = -38
        if self.UP and self.y<top-self.r:
            btm = bottom
            if bottom==-38:
                btm = -32
            if self.jumpCOUNT == 0:
                self.y += 3.5
                self.jumpCOUNT = 1
                self.vel = self.y - btm
                if self.vel >4.5:
                    self.vel = 4.5
            elif self.jumpCOUNT==1 and self.vel<=0:
                self.y += 2.5
                self.vel = self.y - btm
                self.jumpCOUNT = 2
                if self.vel >7.7:
                    self.vel = 7.7
            self.UP = False
        if self.y>top-self.r:
            self.y = top-self.r
            self.vel = 0
        if self.y>bottom+self.r:
            self.vel = self.vel - g * dt
            self.y = self.y + self.vel * dt - 0.5*g*dt*dt
            if self.y<bottom+self.r:
                self.y = bottom+self.r
            if self.y==bottom+self.r:       #new
                self.vel = 0
        if bottom-err<self.y<bottom+self.r+err:     # new cond vel==0
            self.jumpCOUNT = 0

    def Sphere(self,Xo, Yo, Zo, r):
        glLineWidth(3)
        glBegin(GL_LINE_LOOP)
        glColor3f(1,1,1)
        for i in range(72):
            x = r * math.cos(math.radians(i * 5)) + Xo
            y = r * math.sin(math.radians(i * 5)) + Yo
            z = Zo
            glVertex3f(x,y,z)
        glEnd()