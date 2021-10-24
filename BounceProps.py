from OpenGL.GL import *
from OpenGL.GLUT import *
from math import sqrt
import numpy as np
import pygame
import math

class BounceProps:
    def __init__(self):
        self.Lvl = 1
        self.collided = False
        self.Heart_show = True
        self.Key_show = []
        self.Key_count = 0
        self.DoorCount = 0
        self.Rot_Count = 0
        self.open = False #To open door
        self.open2 = False
        self.Surf_face = [(3,4,5,2), (11,10,9,12), (17,18,19,16), (25,24,23,26),(2,5,19,16), (12,9,23,26),  (2,5,6,1), (12,9,8,13), (16,19,20,15), (26,23,22,27),
                          (1,6,20,15), (13,8,22,27),(1,6,7,0), (13,8,7,0), (15,20,21,14), (27,22,21,14), ]# From outer
        self.Surf_face2 = []
        self.Door_info = [0, False, 0]
        self.Pass = False
        self.Pass2 = False
        self.Shuriken_Coord = []
        self.Shuriken_Move = []
        self.Shuriken_Bound = []
        self.Level_show = False
        self.Load_show = False
        self.MUTE = False
        self.effect = None
        self.Egg = None
        self.Hole = None

    def RESET(self):
        if self.Lvl>1:
            self.Door_info = [(0, False, 0), (0, False, 0)]
            self.Key_show = [True, True]
            self.Key_count = 2
            self.Surf_face2 = [(3, 4, 5, 2), (11, 10, 9, 12), (17, 18, 19, 16), (25, 24, 23, 26), (2, 5, 19, 16), (12, 9, 23, 26), (2, 5, 6, 1), (12, 9, 8, 13), (16, 19, 20, 15), (26, 23, 22, 27),
                               (1, 6, 20, 15), (13, 8, 22, 27), (1, 6, 7, 0), (13, 8, 7, 0), (15, 20, 21, 14), (27, 22, 21, 14), ]  # From outer
            if self.Lvl==3:
                self.Shuriken_list()
        else:
            self.Key_show = []
            self.Key_count = 0
            self.Door_info = [0, False, 0]
            self.Surf_face2.clear()
            self.Shuriken_Coord.clear()
            self.Shuriken_Move.clear()
            self.Shuriken_Bound.clear()
        self.Surf_face = [(3, 4, 5, 2), (11, 10, 9, 12), (17, 18, 19, 16), (25, 24, 23, 26), (2, 5, 19, 16), (12, 9, 23, 26), (2, 5, 6, 1), (12, 9, 8, 13), (16, 19, 20, 15), (26, 23, 22, 27),
                          (1, 6, 20, 15), (13, 8, 22, 27), (1, 6, 7, 0), (13, 8, 7, 0), (15, 20, 21, 14), (27, 22, 21, 14), ]  # From outer
        self.Heart_show = True
        self.DoorCount = 0
        self.Rot_Count = 0
        self.open = False  # To open door
        self.open2 = False
        self.Pass = False
        self.Pass2 = False
        self.Level_show = False
        self.Egg_coord()
        self.BlackHole()

    def draw(self, Bx, By, color):
        self.SpaceCorridor(Bx, By, color)
        if not self.Load_show:
            self.Mobilenemy(Bx, By)
            self.Staticenemy(Bx, By)
            self.SpaceDoor(Bx, By)
            self.Rot_Count += 20
        else:
            self.Key(54,13,5)
            self.Rot_Count += 5
        if self.Level_show:
            if self.Lvl==1:
                glPushMatrix()
                glScalef(1, 1.2, 1)
                self.AlienEgg(-215, 10.8, 9)
                glPopMatrix()
            elif self.Lvl==2:
                glPushMatrix()
                glTranslatef(0,0,10)
                self.BlackHOLE(14,4,-0.5)
                glPopMatrix()   
            elif self.Lvl==3:
                glPushMatrix()
                glTranslatef(148,-23.5,10)
                self.Shuriken()
                glPopMatrix()


    def update(self, Bx, By, Br, B_Hp):
        if self.Lvl==3:
            self.Shuriken_Movement()
            self.Shuriken_collision(Bx, By, Br)
        if self.Heart_show:
            self.PowerUp(Bx, By, Br)
            if not self.Heart_show:
                B_Hp += 1
                if not self.MUTE:
                    self.effect = pygame.mixer.Sound('ext/RestoreHealth.wav')
                    self.effect.play()
        if self.Key_count>0:
            self.CheckPoint(Bx, By, Br)
        if not self.collided and By<-32-Br:   #BlackHole detect
            if not self.MUTE:
                self.effect = pygame.mixer.Sound('ext/BlackHole.wav')
                self.effect.play()
            self.collided = True
        if not self.collided:
            for i in range(len(self.Egg)):
                distX, distY, rad,err = 0,0,1.7,0.65
                brd = self.Egg[i]
                if brd[0]-rad-err< Bx <brd[0]+rad+err:
                    if brd[0] < Bx:
                        distX = Bx - brd[0]
                    elif brd[0] > Bx:
                        distX = brd[0] - Bx
                    if By > brd[1]+err:
                        distY = By - brd[1]-err
                    elif By < brd[1]+err:
                        distY = Br+rad+err*10  #not for lower boundary
                    distance = sqrt((distX ** 2) + (distY ** 2))
                    if distance < rad + Br:
                        self.collided = True
                        if not self.MUTE:
                            self.effect = pygame.mixer.Sound('ext/Alien.wav')
                            self.effect.play()
                        break
                    elif brd[0]-rad+err< Bx <brd[0]+rad-err and brd[1]+rad*2<By<brd[1]+rad*2+err/2:
                        self.collided = True
                        if not self.MUTE:
                            self.effect = pygame.mixer.Sound('ext/Alien.wav')
                            self.effect.play()
                        break
        if self.collided and B_Hp>1:
            pygame.time.delay(1000)
        return B_Hp

    def Egg_coord(self):
        if self.Lvl==1:
            self.Egg = [(-199, 5.5), (-189, 5.5), (-177, 11.5), (-163, 11.5), (-155, 5.5), (-150, 5.5), (-133, 5.5), (-125, 5.5), (-115, 5.5),
             (-99, 5.5), (-92, 7.5), (-71, 5.5), (-61, 7.5), (-41, 5.5),(-30, 5.5), (-19, 5.5), (-8, 7.5), (-4, 7.5)]
        elif self.Lvl==2:
            self.Egg = [(-89,-32.5), (-83,-32.5), (-69,-32.5), (-61, -24.5), (-45,-32.5), (-39,-22.5), (-35,-32.5), (-23,-32.5), (-7,-32.5),
                   (13,-32.5), (19,-32.5), (33,-32.5), (44, -24.5), (57, -32.5), (70, -32.5), (79, -26.5), (87, -24.5), (99,-28.5), (110, -32.5),
                   (123, -32.5), (131, -32.5), (141, -30.5)]
        elif self.Lvl == 3:
            self.Egg = [(138, -32.5), (177, -24.5), (195, -26.5), (210, -32.5),
                   (84, 5.5), (97, 5.5), (113, 5.5), (127,11.5), (138,7.5), (147,5.5), (185,5.5), (197,5.5), (217,5.5), (243,9.5)]

    def BlackHole(self):
        if self.Lvl==2:
            self.Hole = [(-58,8),(-44,6), (-32,6), (-18,8), (36,10), (50, 6), (64,4,), (72,4), (84, 10), (124, 6)]
        elif self.Lvl==3:
            self.Hole = [(156,8), (166,8),(182, 8), (198, 10)]


    def SpaceCorridor(self, Bx, By, color):
        # if x within range, build corridorddd
        x,y,h = 0,0,0
        if self.Lvl==1:
            x = [-222, -197, -172, -147, -122, -97, -72, -47, -22, 3]
            y,h = 6, 14
        elif self.Lvl==2:
            x = [-97, -72, -47, -22, 3, 28, 53, 78, 103, 128]
            y,h = -32, 16
        elif self.Lvl==3:
            x = [78, 103, 128, 153, 178, 203, 228, 253]
        for i in range(len(x)):
            if Bx-25*2<x[i]<Bx+25:
                if self.Lvl==2 and x[i]==3:
                    h = 34
                elif self.Lvl==3:
                    if x[i]==228 and By<-6:
                        break
                    if x[i]==128 or x[i]==178:
                        if By<=-6:
                            y, h = 6, 14
                        elif By>-6:
                            y, h = -32, 16
                        self.CorridorBase(x[i], y, 0, h, color)
                    if x[i]==153:
                        y, h = -32, 52
                    elif By>-6:
                        y, h = 6, 14
                    elif By<=-6:
                        y, h = -32, 16
                self.CorridorBase(x[i], y, 0, h, color)
                if self.Lvl==2 and x[i]==3:
                    h = 16

    def SpaceDoor(self, Bx, By):
        x1, x2, H,y,w = 0,0,0,0,2
        if self.Lvl==1:
            x1, y, H = 8, 6, 14
            self.Door_info = [x1, self.Pass, w]
        elif self.Lvl==2:
            x1, x2, y, H = 26, 142, -32, 16
            self.Door_info = [(x1, self.Pass, w), (x2, self.Pass2, w)]   #x, False, w
        elif self.Lvl==3:
            x1, x2, y, H = 154, 176, 6, 14
            self.Door_info = [(x1, self.Pass, w), (x2, self.Pass2, w)]   #x, False, w
        for i in range(len(self.Door_info)):
            if i==0:
                surf = self.Surf_face
            else:
                surf = self.Surf_face2
            if self.Lvl==1:
                x = self.Door_info[0]
            else:
                DOOR = self.Door_info[i]
                x = DOOR[0]
            if Bx-23<x<Bx+23:
                self.DoorBase(x,y,0,w,1,1,H, surf)
                if self.Lvl==1 and not self.Pass and not self.open:
                    if Bx - 8 < x < Bx + 8 and y < By < y + 12:
                        self.open = True
                        if not self.MUTE:
                            self.effect = pygame.mixer.Sound('ext/DoorOpen.wav')
                            self.effect.play()
                elif self.Lvl>1 and self.Key_count==1 and not self.Pass and not self.open and i==0:
                    if Bx - 8 < x < Bx + 8 and y < By < y + 12:
                        self.open = True
                        if not self.MUTE:
                            self.effect.stop()
                            self.effect = pygame.mixer.Sound('ext/DoorOpen2.wav')
                            self.effect.play()
                elif self.Lvl>1 and self.Key_count==0 and not self.Pass2 and not self.open2 and i==1:
                    if Bx - 8 < x < Bx + 8 and y < By < y + 12:
                        self.open2 = True
                        if not self.MUTE:
                            self.effect.stop()
                            self.effect = pygame.mixer.Sound('ext/DoorOpen2.wav')
                            self.effect.play()
        if self.open or self.open2:
            if self.open:
                Surface = self.Surf_face
            else:
                Surface = self.Surf_face2
            if self.DoorCount <= 60:
                self.DoorCount += 1
                if self.DoorCount == 20:
                    for i in range(4):
                        Surface.pop()
                elif self.DoorCount == 40:
                    for i in range(6):
                        Surface.pop()
                elif self.DoorCount == 60:
                    for i in range(6):
                        Surface.pop()
                    self.DoorCount = 0
                    if self.open:
                        self.open = False
                        self.Pass = True
                    else:
                        self.open2 = False
                        self.Pass2 = True

    def Shuriken_collision(self, Bx, By, Br):
        for i in range(len(self.Shuriken_Coord)):
            Coord = self.Shuriken_Coord[i]
            if Bx - Br - 4 < Coord[0] < Bx + Br + 4:
                distX, distY = 0, 0
                if Coord[0] < Bx:
                    distX = Bx - Coord[0]
                elif Coord[0] > Bx:
                    distX = Coord[0] - Bx
                if By > Coord[1]:
                    distY = By - Coord[1]
                elif By < Coord[1]:
                    distY = Coord[1] - By
                distance = sqrt((distX ** 2) + (distY ** 2))
                if distance < 1.8 + Br:
                    self.collided = True
                    if not self.MUTE:
                        self.effect.stop()
                        self.effect = pygame.mixer.Sound('ext/Shuriken_collided.wav')
                        self.effect.play()
                    break

    def Mobilenemy(self, Bx, By):
        for i in range(len(self.Shuriken_Coord)):
            Coord, Bound = self.Shuriken_Coord[i], self.Shuriken_Bound[i]
            if Bx-18<Coord[0]<Bx+18 and By-14<Coord[1]<By+14:
                if not self.MUTE:
                    if Bx-3<=Coord[0]<=Bx+3 and By-7<Coord[1]<By+7 or By-2<=Coord[1]<=By+2 and Bx-7<Coord[0]<Bx+7:
                        self.effect = pygame.mixer.Sound('ext/Shuriken.wav')
                        self.effect.play()
                glPushMatrix()
                glTranslate(Coord[0], Coord[1], 0)
                self.Shuriken()
                glPopMatrix()

    def Shuriken_list(self):
        self.Shuriken_Coord = [[92,18], [158,-30], [174,18], [218,-18], [186,8], [232,18], [256,8]]
        self.Shuriken_Move = [[False, False, False, True], [True, False, False, False], [False, True, False, False], [False, True, False, False],
                              [True, False, False, False], [False, False, False, True], [False, False, True, False]]
        self.Shuriken_Bound = [[18,8,92,118], [18,-30,158,174], [18,-30,158,174], [-18, -30, 206, 218], [18, 8, 186, 262], [18, 8, 186, 262], [18, 8, 186, 262]]

    def Shuriken_Movement(self):
        for i in range(len(self.Shuriken_Coord)):
            Coord, Move, Bound = self.Shuriken_Coord[i], self.Shuriken_Move[i], self.Shuriken_Bound[i]
            if Move[0]:
                if Coord[1]==Bound[0]:
                    Move[0] = False
                    Move[3] = True
                else:
                    Coord[1] += 1
            elif Move[1]:
                if Coord[1]==Bound[1]:
                    Move[1] = False
                    Move[2] = True
                else:
                    Coord[1] -= 1
            elif Move[2]:
                if Coord[0]==Bound[2]:
                    Move[2] = False
                    Move[0] = True
                else:
                    Coord[0] -= 1
            elif Move[3]:
                if Coord[0]==Bound[3]:
                    Move[3] = False
                    Move[1] = True
                else:
                    Coord[0] += 1
            self.Shuriken_Coord[i], self.Shuriken_Move[i] = Coord, Move

    def PowerUp(self, Bx, By, Br):
        Hx, Hy, Hr = 0,0,0.8
        if self.Lvl==1:
            Hx, Hy = -115, 19
        elif self.Lvl==2:
            Hx, Hy = 16,-25
        elif self.Lvl==3:
            Hx, Hy = 151, 7
        if Bx-18<Hx<Bx+18:
            self.Heart(Hx, Hy, 0)
            distX, distY = 0, 0        
            if Hx < Bx:
                distX = Bx - Hx
            elif Hx > Bx:
                distX = Hx - Bx
            if By > Hy:
                distY = By - Hy
            elif By < Hy:
                distY = Hy - By
            distance = sqrt((distX ** 2) + (distY ** 2))
            if distance < Hr + Br:
                self.Heart_show = False

    def CheckPoint(self, Bx, By, Br):
        Kr, Key_coord = 0.8, 0
        if self.Lvl == 2:
            Key_coord = [(-77, -27, 0), (119,-17, 0)]
        elif self.Lvl == 3:
            Key_coord = [(223, -17, 0), (83, 11, 0)]
        for i in range(len(Key_coord)):
            Key = Key_coord[i]
            if Bx - 18 < Key[0] < Bx + 18 and self.Key_show[i]:
                self.Key(Key[0], Key[1], Key[2])
                distX, distY = 0, 0
                if Key[0] < Bx:
                    distX = Bx - Key[0]
                elif Key[0] > Bx:
                    distX = Key[0] - Bx
                if By > Key[1]:
                    distY = By - Key[1]
                elif By < Key[1]:
                    distY = Key[1] - By
                distance = sqrt((distX ** 2) + (distY ** 2))
                if distance < Kr + Br:
                    if not self.MUTE:
                        self.effect.stop()
                        self.effect = pygame.mixer.Sound('ext/GetKey.wav')
                        self.effect.play()
                    self.Key_show[i] = False
                    self.Key_count -= 1

    def Staticenemy(self, Bx, By):
        glPushMatrix()
        glScalef(1, 1.2, 1)
        for i in range(len(self.Egg)):
            coord = self.Egg[i]
            if Bx-18<coord[0]<Bx+18:
                if self.Lvl==3:
                    if By < -5 and coord[1] < -5 or By >= -5 and coord[1] >= -5:
                        self.AlienEgg(coord[0], coord[1], 0)
                else:
                    self.AlienEgg(coord[0], coord[1], 0)
        glPopMatrix()
        if self.Lvl>1:
            for i in range(len(self.Hole)):
                coord = self.Hole[i]
                if Bx - 20 < coord[0] < Bx + 20:
                    self.BlackHOLE(coord[0], coord[1], -32)

    def loadTexture(self, image):
        textureSurface = pygame.image.load(image)
        textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    def Key(self, X, Y, Z):
        gap, d, r, Vtx = 0.025, 0.15, 0.8, []
        Y += 0.15
        h = math.sqrt(2 * r ** 2 - r ** 2) / 2
        Obj = np.array([(- gap, h, d, 1), (- gap * 2.5, h * 0.4, d, 1), (- r, - h + gap * 0.2, d, 1), (- r * 0.4, - h * 0.4, d, 1),
               (- r * 0.9, - h, d, 1), (- r * 0.4, - h * 0.7 - gap * 0.2, d, 1), (r * 0.9, - h, d, 1), (r * 0.4, - h * 0.7 - gap * 0.2, d, 1),
               (r, - h + gap * 0.2, d, 1), (r * 0.4, - h * 0.4, d, 1), (gap, h, d, 1), (gap * 2.5, h * 0.4, d, 1),
               (- gap, h, - d, 1), (- gap * 2.5, h * 0.4, - d, 1), (- r, - h + gap * 0.2, - d, 1), (- r * 0.4, - h * 0.4, - d, 1),
               (- r * 0.9, - h, - d, 1), (- r * 0.4, - h * 0.7 - gap * 0.2, - d, 1), (r * 0.9, - h, - d, 1), (r * 0.4, - h * 0.7 - gap * 0.2, - d, 1),
               (r, - h + gap * 0.2, - d, 1), (r * 0.4, - h * 0.4, - d, 1), (gap, h, - d, 1), (gap * 2.5, h * 0.4, - d, 1) ])
        for i in range(len(Obj)):
            RotY = np.array((math.cos(math.radians(self.Rot_Count)), 0, math.sin(math.radians(self.Rot_Count)), X, 0, 1, 0, Y, -math.sin(math.radians(self.Rot_Count)), 0, math.cos(math.radians(self.Rot_Count)), Z, 0, 0, 0, 1)).reshape(4, 4)
            Coords = np.array(np.dot(RotY, Obj[i])).tolist()
            Vtx.append((Coords[0], Coords[1], Coords[2]))
        Surf = [(0, 1, 3, 2), (4, 5, 7, 6), (8, 9, 11, 10),
                (12, 13, 15, 14), (16, 17, 19, 18), (20, 21, 23, 22),
                (0, 1, 13, 12), (2, 3, 15, 14), (5, 4, 16, 17), (7, 6, 18, 19), (8, 9, 21, 20), (10, 11, 23, 22),
                (0, 12, 14, 2), (1, 13, 15, 3), (4, 16, 18, 6), (5, 17, 19, 7), (8, 20, 22, 10), (9, 21, 23, 11)]
        color = ((164 / 255, 183 / 255, 0), (77 / 255, 83 / 255, 28 / 255), (77 / 255, 83 / 255, 28 / 255), (164 / 255, 183 / 255, 0))
        glBegin(GL_QUADS)
        for surface in Surf:
            x = 0
            for vertex in surface:
                glColor3fv(color[x])
                glVertex3fv(Vtx[vertex])
                x += 1
        glEnd()

    def Heart(self, X, Y, Z):  # Heart(0,0,0,.08,.08,0.25)
        Vtx, Surf, S_x, S_y, d, a = [], [], 0.06,0.06,0.5, 0
        for k in range(3):
            if k == 0 or k == 2:
                Sx, Sy = S_x * .7, S_y * .7
                Z -= d
                if k == 2:
                    Z += d * 2
            else:
                Sx, Sy = S_x, S_y
                Z += d
            for i in range(36):
                x = 16 * math.pow(math.sin(math.radians(i * 10)), 3)
                y = 13 * math.cos(math.radians(i * 10)) - 5 * math.cos(2 * math.radians(i * 10)) - 2 * math.cos(3 * math.radians(i * 10)) - math.cos(4 * math.radians(i * 10))
                Obj = np.array((x, y, 0, 1))
                Scal = np.array((Sx, 0, 0, 0, 0, Sy, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)).reshape(4, 4)
                RotY = np.array((math.cos(math.radians(self.Rot_Count)), 0, math.sin(math.radians(self.Rot_Count)), X, 0, 1, 0, Y, -math.sin(math.radians(self.Rot_Count)), 0, math.cos(math.radians(self.Rot_Count)), Z, 0,0,0,1)).reshape(4,4)
                Coords = np.array(np.dot(RotY, np.dot(Scal, Obj))).tolist()
                Vtx.append((Coords[0], Coords[1], Coords[2]))
                if k == 0:
                    if i == 35:
                        Surf.append((a + 36, a + 1, a - 35, a))
                    else:
                        Surf.append((a + 36, a + 37, a + 1, a))
                elif k == 1:
                    if i == 35:
                        Surf.append((a, a - 35, a + 1, a + 36))
                    else:
                        Surf.append((a + 1, a, a + 36, a + 37))
                else:
                    if i == 35:
                        Surf.append((a, a -35, a - 107, a -72))
                    else:
                        Surf.append((a, a+1, a -71, a -72))
                a += 1
        color = ((217 / 255, 116 / 255, 226 / 255), (217 / 255, 116 / 255, 226 / 255), (246 / 255, 72 / 255, 150 / 255), (246 / 255, 72 / 255, 150 / 255))
        glBegin(GL_QUADS)
        for surface in Surf:
            x = 0
            for vertex in surface:
                glColor3fv(color[x])
                glVertex3fv(Vtx[vertex])
                x += 1
        glEnd()

    def Shuriken(self):
        w, h, d,a = 0.1, 0.1, 0.15,0
        Surf1, Surf2, Surf3, Vtx = [], [], [], []
        Vtx_sample = [(-w * 3, h, d * .65), (-w * 3, -h, d * .65), (-w * 6, h * 0, d * .65), (-w * 6, -h * 2, d * .65), (-w * 9, -h / 2, d * .75), (-w * 9, -h * 2, d * .75)]
        for i in range(4):
            step = 0.2 * i
            if i == 3:
                step = 0.7
            y1 = 0.9 * ((-w * 11 - step) + abs(-w * 11)) ** 2 - h / 2
            y2 = 1.2 * ((-w * 11 - step) + abs(-w * 11)) ** 2 - h * 2
            Vtx_sample.append((-w * 11 - step, y1, d * (.75 - i * 0.05)))
            Vtx_sample.append((-w * 11 - step, y2, d * (.75 - i * 0.05)))
        vtx_left = [(-w * 5, h / 2, d), (-w * 5, -h * 2, d), (-w * 7, h / 2, d), (-w * 7, -h * 2, d), (-w * 11, -h, d), (-w * 11, -h * 2, d)]
        for vtx in vtx_left:
            Vtx_sample.append(vtx)
        for k in range(len(Vtx_sample)):
            p = Vtx_sample[k]
            lst = list(p)
            lst[2] *= -1
            p = tuple(lst)
            Vtx_sample.append(p)
        for deg in range(6):
            for v in range(len(Vtx_sample)):
                newVtx = Vtx_sample[v]
                Obj = np.array(newVtx)
                RotZ = np.array([math.cos(math.radians(deg * 60 - self.Rot_Count)), -math.sin(math.radians(deg * 60 - self.Rot_Count)), 0, math.sin(math.radians(deg * 60 - self.Rot_Count)), math.cos(math.radians(deg * 60 - self.Rot_Count)), 0, 0, 0, 1]).reshape(3, 3)
                Coords = np.array(np.dot(RotZ, Obj)).tolist()
                Vtx.append((Coords[0], Coords[1], Coords[2]))
        for k in range(12):
            for j in range(7):
                if j == 1 or j == 5:
                    a += 2
                if j == 0:
                    Surf1.append((a, a + 1, a + 3, a + 2))
                    if k % 2 == 0:
                        Surf1.append((a + 1, a + 21, a + 20, a))  # front
                        Surf1.append((a + 20, a, a + 2, a + 22))
                        Surf1.append((a + 21, a + 1, a + 3, a + 23))
                elif 1 <= j <= 4:
                    Surf2.append((a, a + 1, a + 3, a + 2))
                    if k % 2 == 0:
                        Surf2.append((a, a + 20, a + 22, a + 2))  # top
                        Surf2.append((a + 1, a + 21, a + 23, a + 3))  # bottom
                        if j == 4:
                            Surf2.append((a + 2, a + 3, a + 23, a + 22))
                else:
                    Surf3.append((a, a + 1, a + 3, a + 2))
                    if k % 2 == 0:
                        Surf3.append((a, a + 20, a + 22, a + 2))  # top
                        Surf3.append((a + 1, a + 21, a + 23, a + 3))  # bottom
                        if j == 5:
                            Surf3.append((a, a + 1, a + 21, a + 20))
                a += 2
            a += 2
        color = [(185 / 255, 245 / 255, 236 / 255), (185 / 255, 245 / 255, 236 / 255), (5 / 255, 148 / 255, 106 / 255), (5 / 255, 148 / 255, 106 / 255),
                 (157 / 255, 249 / 255, 248 / 255), (7 / 255, 100 / 255, 99 / 255), (7 / 255, 100 / 255, 99 / 255), (157 / 255, 249 / 255, 248 / 255),
                 (1, 1, 1), (7 / 255, 100 / 255, 99 / 255), (7 / 255, 100 / 255, 99 / 255), (1, 1, 1)]
        glBegin(GL_QUADS)
        for surface in Surf1:
            x = 0
            for vertex in surface:
                glColor3fv(color[x])
                glVertex3fv(Vtx[vertex])
                x += 1
        for surface in Surf2:
            x = 4
            for vertex in surface:
                glColor3fv(color[x])
                glVertex3fv(Vtx[vertex])
                x += 1
        for surface in Surf3:
            x = 8
            for vertex in surface:
                glColor3fv(color[x])
                glVertex3fv(Vtx[vertex])
                x += 1
        glEnd()

    def BlackHOLE(self, x, w, y):
        Coords = [(x,y,-1), (x,y,1), (x+w,y,1), (x+w,y,-1)]
        glColor3f(0,0,0)
        glBegin(GL_QUADS)
        for vtx in Coords:
            glVertex3fv(vtx)
        glEnd()

    def AlienEgg(self, newX, newY, newZ):
        Vtx, Surf, Txt, a, ss = [], [], [], 0, 0
        MDL_sphere_Lyt = self.SphereModel()
        coord = MDL_sphere_Lyt[0]
        if newY<-30:
            newY+=6.5
        elif newY<-28:
            newY+=6
        elif newY<=-26.5:
            newY += 5.5
        elif newY<-20:
            newY+=5
        elif newY==11.5 or newY==9.5:
            newY -=1

        for j in range(19):
            point = coord[j]
            for k in range(12):
                x = point[0] * math.cos(math.radians(k * 30)) + newX
                y = point[1] + newY
                z = point[0] * math.sin(math.radians(k * 30)) + newZ
                Vtx.append((x, y, z))
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        self.loadTexture("ext/alien_egg.png")
        glBegin(GL_QUADS)
        x = 0
        for surface in MDL_sphere_Lyt[1]:
            for vertex in surface:
                glTexCoord2fv(MDL_sphere_Lyt[2][x])
                glVertex3fv(Vtx[vertex])
                x += 1
        glEnd()
        glDeleteTextures(1)
        # glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    def SphereModel(self):
        VtxLyt, Surf, Txt, a, ss, r = [], [], [], 0, 0, 1.2
        for i in range(19):
            x = r * math.cos(math.radians(i * 10 - 90))
            y = r * math.sin(math.radians(i * 10 - 90))
            VtxLyt.append((x, y))
        for k in range(17):
            sss = 0
            h = k / 17
            for i in range(12):
                tt, uu, vv = ss + 1, ss + 13, ss + 12
                if i == 11:
                    tt -= 12
                Surf.append((ss, tt, uu, vv))
                ss += 1
                Txt.append((sss, h))
                Txt.append((sss + 1 / 12, h))
                Txt.append((sss, h + 1 / 17))
                Txt.append((sss + 1 / 12, h + 1 / 17))
                sss += 1 / 12
        return VtxLyt, Surf, Txt

    def CorridorBase(self, Xo, Yo, Zo, H, Special_color):
        w,d,h,R = 25,1,1,12
        Vtx = [(Xo, Yo + h, Zo - d * 6), (Xo + w, Yo + h, Zo - d * 6), (Xo, Yo + h, Zo - d * 4),
               (Xo + w, Yo + h, Zo - d * 4), (Xo, Yo, Zo - d * 3), (Xo + w, Yo, Zo - d * 3),
               (Xo, Yo, Zo + d * 3), (Xo + w, Yo, Zo + d * 3), (Xo, Yo + h, Zo + d * 4), (Xo + w, Yo + h, Zo + d * 4),
               (Xo, Yo + h, Zo + d * 6), (Xo + w, Yo + h, Zo + d * 6),
               (Xo, Yo, Zo - d * 7), (Xo + w, Yo, Zo - d * 7), (Xo, Yo, Zo - d * 5), (Xo + w, Yo, Zo - d * 5),
               (Xo, Yo - h, Zo - d * 4), (Xo + w, Yo - h, Zo - d * 4),
               (Xo, Yo - h, Zo + d * 4), (Xo + w, Yo - h, Zo + d * 4), (Xo, Yo, Zo + d * 5), (Xo + w, Yo, Zo + d * 5),
               (Xo, Yo, Zo + d * 7), (Xo + w, Yo, Zo + d * 7),
               (Xo, Yo - h + H, Zo - d * 7), (Xo + w, Yo - h + H, Zo - d * 7), (Xo, Yo - h + H, Zo - d * 5),
               (Xo + w, Yo - h + H, Zo - d * 5), (Xo, Yo + H, Zo - d * 4), (Xo + w, Yo + H, Zo - d * 4),
               (Xo, Yo + H, Zo + d * 4), (Xo + w, Yo + H, Zo + d * 4), (Xo, Yo - h + H, Zo + d * 5),
               (Xo + w, Yo - h + H, Zo + d * 5), (Xo, Yo - h + H, Zo + d * 7), (Xo + w, Yo - h + H, Zo + d * 7),
               (Xo, Yo + H, Zo - d * 8), (Xo + w, Yo + H, Zo - d * 8), (Xo, Yo + H, Zo - d * 6),
               (Xo + w, Yo + H, Zo - d * 6), (Xo, Yo + h + H, Zo - d * 5), (Xo + w, Yo + h + H, Zo - d * 5),
               (Xo, Yo + h + H, Zo + d * 5), (Xo + w, Yo + h + H, Zo + d * 5), (Xo, Yo + H, Zo + d * 6),
               (Xo + w, Yo + H, Zo + d * 6), (Xo, Yo + H, Zo + d * 8), (Xo + w, Yo + H, Zo + d * 8),
               (Xo + w / R, Yo + h, Zo - d * 6), (Xo + w * (R-1) / R, Yo + h, Zo - d * 6), (Xo + w / R, Yo, Zo - d * 7),(Xo + w * (R-1) / R, Yo, Zo - d * 7),
               (Xo + w / R, Yo + h, Zo + d * 6), (Xo + w * (R-1) / R, Yo + h, Zo + d * 6), (Xo + w / R, Yo, Zo + d * 7),(Xo + w * (R-1) / R, Yo, Zo + d * 7),
               (Xo + w / (R+4), Yo - h + H, Zo - d * 7), (Xo + w * (R+3) / (R+4), Yo - h + H, Zo - d * 7),(Xo + w / (R+4), Yo + H, Zo - d * 8), (Xo + w * (R+3) / (R+4), Yo + H, Zo - d * 8),
               (Xo + w / (R+4), Yo - h + H, Zo + d * 7), (Xo + w * (R+3) / (R+4), Yo - h + H, Zo + d * 7),(Xo + w / (R+4), Yo + H, Zo + d * 8), (Xo + w * (R+3) / (R+4), Yo + H, Zo + d * 8),
               (Xo, Yo, Zo - d), (Xo + w, Yo, Zo - d), (Xo + w, Yo, Zo + d), (Xo, Yo, Zo + d),
               (Xo, Yo + H, Zo - d), (Xo + w, Yo + H, Zo - d), (Xo + w, Yo + H, Zo + d), (Xo, Yo + H, Zo + d)]
        Surf_inner = [(0, 1, 3, 2),  (10, 11, 9, 8), (24, 25, 27, 26),(34, 35, 33, 32),
                      (0, 48, 56, 24), (49, 1, 25, 57), (10, 52, 60, 34), (53, 11, 35, 61),
                      (48, 50, 58, 56), (54, 52, 60, 62), (51, 49, 57, 59), (53, 55, 63, 61)]
        Surf_outer = [(14, 12, 0, 2), (16, 14, 2, 4), (18, 16, 4, 6), (20, 18, 6, 8), (22, 20, 8, 10),
                      (13, 15, 3, 1), (15, 17, 5, 3), (17, 19, 7, 5), (19, 21, 9, 7), (21, 23, 11, 9),
                      (12, 13, 15, 14), (14, 15, 17, 16), (16, 17, 19, 18), (18, 19, 21, 20), (20, 21, 23, 22),
                      (26, 24, 36, 38), (28, 26, 38, 40), (30, 28, 40, 42), (32, 30, 42, 44), (34, 32, 44, 46),
                      (25, 27, 39, 37), (27, 29, 41, 39), (29, 31, 43, 41), (31, 33, 45, 43), (33, 35, 47, 45),
                      (36, 37, 39, 38), (38, 39, 41, 40), (40, 41, 43, 42), (42, 43, 45, 44), (44, 45, 47, 46),
                      (12, 13, 1, 0), (22, 23, 11, 10), (36, 37, 25, 24), (46, 47, 35, 34),
                      (0, 12, 36, 24), (13, 1, 25, 37), (10, 22, 46, 34), (23, 11, 35, 47),
                      (12, 50, 58, 36), (51, 13, 37, 59), (22, 54, 62, 46), (55, 23, 47, 63)]
        Surf_effect = [(4, 5, 3, 2), (6, 7, 9, 8), (28, 29, 27, 26), (30, 31, 33, 32), (64,65,66,67), (68,69,70,71)]
        Surf_floor = [(4, 5, 7, 6), (28, 29, 31, 30)]
        color1 = [(22 / 255, 57 / 255, 67 / 255), (22 / 255, 57 / 255, 67 / 255), (22 / 255, 57 / 255, 67 / 255),(22 / 255, 57 / 255, 67 / 255)]
        color2 = [(47 / 255, 62 / 255, 7 / 255), (47 / 255, 62 / 255, 7 / 255), (103 / 255, 133 / 255, 20 / 255),(125 / 255, 162 / 255, 23 / 255), ]
        color3 = [(0, 10 / 255, 44 / 255), (0, 10 / 255, 44 / 255), (11 / 255, 22 / 255, 60 / 255),(13 / 255, 30 / 255, 88 / 255), ]
        glBegin(GL_QUADS)
        for surface in Surf_floor:
            x = 0
            for vertex in surface:
                glColor3fv(color1[x])
                glVertex3fv(Vtx[vertex])
                x += 1
        for surface in Surf_effect:
            x = 0
            for vertex in surface:
                glColor3fv(Special_color[x])
                glVertex3fv(Vtx[vertex])
                x += 1
        for surface in Surf_outer:
            x = 0
            for vertex in surface:
                glColor3fv(color2[x])
                glVertex3fv(Vtx[vertex])
                x += 1
        for surface in Surf_inner:
            x = 0
            for vertex in surface:
                glColor3fv(color3[x])
                glVertex3fv(Vtx[vertex])
                x += 1
        glEnd()

    def DoorBase(self, Xo, Yo, Zo, w, d, h, H, surf):
        counter = 0
        Vtx = [(Xo, Yo, Zo), (Xo, Yo, Zo - d * 3), (Xo, Yo + h, Zo - d * 4), (Xo, Yo + h, Zo - d * 6),(Xo, Yo - h + H, Zo - d * 7), (Xo, Yo - h + H, Zo - d * 5), (Xo, Yo + H, Zo - d * 4),
               (Xo, Yo + H, Zo), (Xo, Yo + H, Zo + d * 4), (Xo, Yo - h + H, Zo + d * 5), (Xo, Yo - h + H, Zo + d * 7),(Xo, Yo + h, Zo + d * 6), (Xo, Yo + h, Zo + d * 4), (Xo, Yo, Zo + d * 3),
               (Xo + w, Yo, Zo), (Xo + w, Yo, Zo - d * 3), (Xo + w, Yo + h, Zo - d * 4), (Xo + w, Yo + h, Zo - d * 6),(Xo + w, Yo - h + H, Zo - d * 7), (Xo + w, Yo - h + H, Zo - d * 5), (Xo + w, Yo + H, Zo - d * 4),
               (Xo + w, Yo + H, Zo), (Xo + w, Yo + H, Zo + d * 4), (Xo + w, Yo - h + H, Zo + d * 5),(Xo + w, Yo - h + H, Zo + d * 7),(Xo + w, Yo + h, Zo + d * 6), (Xo + w, Yo + h, Zo + d * 4), (Xo + w, Yo, Zo + d * 3),]
        Surf_side = [(15, 1, 2, 16), (17, 3, 2, 16), (17, 3, 4, 18), (19, 5, 4, 18), (19, 5, 6, 20), (27, 13, 1, 15),
                     (27, 13, 12, 26), (25, 11, 12, 26), (25, 11, 10, 24), (23, 9, 10, 24), (23, 9, 8, 22),(22, 8, 6, 20)  ]# Side
        color = ((18 / 255, 0, 44 / 255), (18 / 255, 0, 44 / 255), (85 / 255, 35 / 255, 160 / 255),(49 / 255, 16 / 255, 99 / 255),)
        colors = ((33 / 255, 0, 80 / 255), (61 / 255, 8 / 255, 135 / 255), (80 / 255, 30 / 255, 139 / 255),(33 / 255, 0, 80 / 255),
                  (33 / 255, 0, 80 / 255), (80 / 255, 30 / 255, 139 / 255), (102 / 255, 44 / 255, 184 / 255),(33 / 255, 0, 80 / 255),
                  (33 / 255, 0, 80 / 255), (102 / 255, 44 / 255, 184 / 255), (128 / 255, 60 / 255, 223 / 255),(156 / 255, 85 / 255, 1),)
        glBegin(GL_QUADS)
        for surface in Surf_side:
            x = 0
            for vertex in surface:
                glColor3fv(color[x])
                glVertex3fv(Vtx[vertex])
                x += 1
        if len(surf)>1:
            for surface in surf:
                if counter >= 12:
                    x = 8
                elif counter >= 6:
                    x = 4
                else:
                    x = 0
                for vertex in surface:
                    glColor3fv(colors[x])
                    glVertex3fv(Vtx[vertex])
                    x += 1
                counter += 1
        glEnd()
