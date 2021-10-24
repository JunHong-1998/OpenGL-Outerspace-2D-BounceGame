from random import*
from pygame.locals import *
from OpenGL.GLU import *
from BounceBall import *
from BounceMAP import *
from BounceProps import *

Props = BounceProps()
Map = BounceMAP(-222,20,0, 2)
Ball = BounceBall()

class BounceMain:
    def __init__(self):
        self.Eye = [0,0,0,0]
        self.UI = 0
        self.LOAD_END = False
        self.LOAD = False
        self.MENU = False
        self.GAME = False
        self.MUTE = False
        self.Level = 1
        self.Lvl_update = 1
        self.score = [0,0,0]
        self.time_PAUSE_record = False
        self.time = 0
        self.time_run = 0
        self.time_last = 0
        self.time_pause = 0
        self.time_level = [0,0,0]
        self.Key_score = [True, True]
        self.Heart_score = True
        self.Game_RESTART = False
        self.Star = []
        self.Star_list()
        self.Bonus = 100
        self.Game_LEVEL_Complete = False
        self.Game_LEVEL_Warn = False
        self.Game_LEVEL_Fail = False
        self.Game_PAUSE = False
        self.Setting_event = 0
        self.Setting_Func = 0
        self.SetFunc_Key = 0
        self.Enter = False
        self.Game_PAUSE_setting = False
        self.Game_LEVEL_Warn_play = True

    def Camera_view(self):
        if self.GAME:
            self.Eye[0] = Ball.x
            self.Eye[2] = Ball.z+23
            self.Eye[3] = Ball.x
            if 6<Ball.y<20:
                self.Eye[1] = 13
            elif -32 < Ball.y < -16:
                self.Eye[1] = -24
            else:
                self.Eye[1] = Ball.y
        glLoadIdentity()  # Reset the matrix system
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(self.Eye[0], self.Eye[1], self.Eye[2], self.Eye[3], self.Eye[1], Ball.z, 0, 1, 0)

    def Interface(self):
        self.Background()
        self.Camera_view()
        if self.Setting_event>0:
            self.Setting_Event_Func()

    def Loading(self):
        if not self.LOAD:
            pygame.mixer.music.load('ext/background_msc.wav')
            pygame.mixer.music.play(-1)
            self.Level = 1
            Ball.x, Ball.y = 52, 13
            self.LOAD = True
        self.Load_Effect()

    def Control(self):
        Ball.x, Ball.y = -154,-19
        self.Eye = [Ball.x, Ball.y, Ball.z + 10, Ball.x]
        self.Control_Key(-154,-19,0)
        self.DisplayText("Pause/Exit", (38, 455), (1,1,1), 0)
        self.DisplayText("esc", (38, 425), (0,0,0), 0)
        self.DisplayText("A", (105, 278), (0,0,0), 0)
        self.DisplayText("W", (155, 330), (0, 0, 0), 0)
        self.DisplayText("Movement", (200, 380), (1,1,1), 0)
        self.DisplayText("D", (210, 278), (0, 0, 0), 0)
        self.DisplayText("Space", (220, 190), (0, 0, 0), 0)
        self.DisplayText("Selection", (320, 130), (1,1,1), 0)
        self.DisplayText("<", (628, 175), (0, 0, 0), 0)
        self.DisplayText(">", (733, 175), (0, 0, 0), 0)
        self.DisplayText("Option", (650, 130), (1, 1, 1), 0)

    def Menu(self):
        self.DisplayText("OUTERSPACE", (500, 350, 100), (1, 1, 1), 0.1)
        if not self.MENU:
            self.Level = Props.Lvl = Map.Lvl = 1
            Ball.x, Ball.y, Ball.z = 90,-5, 0
            self.LOAD, self.MENU, self.GAME = False, True, False
            self.Eye = [90, -5, 180, 90]
        self.Setting(90-2, -5, self.Eye[2] - 10, 1)
        self.Setting(90+2, -5, self.Eye[2] - 10, 5)
        self.Setting_event = 1
        self.Menu_Effect()

    def Menu_Effect(self):
        Props.Load_show, Map.Load_show, Ball.Load_show = True, False, True
        if self.Level==1:
            Ball.x-=2
            if Ball.x<=-55:
                self.Level = Props.Lvl = Map.Lvl = 2
        elif self.Level==2:
            Ball.x += 2
            if Ball.x>=150:
                self.Level = Props.Lvl = Map.Lvl = 3
                Ball.y = -8
        elif self.Level==3:
            if Ball.x>250:
                Ball.y = -5
            elif Ball.x<50:
                self.Level = Props.Lvl = Map.Lvl = 1
            if Ball.y==-5:
                Ball.x -= 2
            else:
                Ball.x += 2

    def Load_Effect(self):
        Props.Load_show, Map.Load_show, Ball.Load_show = True, True, True
        if self.Level==1:
            Ball.x -= 0.8
            self.Eye = [Ball.x+20, Ball.y, Ball.z+15, Ball.x]
            if Ball.x<-248:
                self.Level = Props.Lvl = Map.Lvl = 2
                Ball.y = -24
        elif self.Level==2:
            Ball.x += 1
            self.Eye = [Ball.x - 20, Ball.y, Ball.z, Ball.x]
            if Ball.x>144:
                self.Level = Props.Lvl = Map.Lvl = 3
        elif self.Level==3:
            if Ball.x<290 and Ball.y<=-24:
                self.Eye = [Ball.x + 30, Ball.y-7, Ball.z, Ball.x]
                Ball.x += 1
                if Ball.x > 256:
                    Ball.y = 13
            elif Ball.y>=13 and Ball.x>78-20:
                self.Eye = [Ball.x+20, Ball.y-5, Ball.z+5, Ball.x]
                Ball.x -= 1
            else:
                self.DisplayText("Made By : Low Jun Hong", (265, 200), (1, 1, 1), 0)
                Ball.x, Ball.y = 54, 13
                self.Eye = [Ball.x, Ball.y, Ball.z + 5, Ball.x]
                if Ball.z<4:
                    Ball.z +=0.008
                else:
                    self.DisplayText("Press Spacebar to Continue", (260, 15), (1, 1, 1), 0)
                    self.LOAD_END = True

    def Update(self):
        if Ball.hp==0 and not self.Game_LEVEL_Fail or self.Level==4 and not self.Game_LEVEL_Complete and not self.Game_LEVEL_Fail:
            self.Game_LEVEL_Fail, self.Game_PAUSE = True, True
            if not self.MUTE:
                Props.effect.stop()
                effect = pygame.mixer.Sound('ext/Lose.wav')
                effect.play()
        if self.Game_RESTART:
            self.Level = Props.Lvl = Map.Lvl = Ball.Lvl = self.Lvl_update = 1
            self.score, self.time_level = [0, 0, 0], [0, 0, 0]
            self.time_last = self.time_run
            self.Game_RESTART, self.Game_LEVEL_Fail, self.Game_PAUSE = False, False, False
        if not self.Game_PAUSE and not self.Game_LEVEL_Warn and not self.Game_LEVEL_Complete and self.time_PAUSE_record:
            self.time_last += (self.time_run - self.time_pause)
            self.time_pause, self.time_PAUSE_record = 0, False
        if self.Game_PAUSE:
            self.Pause_Setting()
        self.Display_GameLEVEL()
        self.Level_update()
        self.Score_update()
        self.Display_GameINFO()

    def Pause_Setting(self):
        if self.Game_PAUSE_setting:
            self.Setting_event=2
            self.Setting(Ball.x - 4, self.Eye[1], Ball.z + 10, 2)
            self.Setting(Ball.x, self.Eye[1], Ball.z + 10, 4)
            self.Setting(Ball.x + 4, self.Eye[1], Ball.z + 10, 3)

    def Setting_Event_Func(self):
        if self.Setting_event==1:   #Menu
            if self.SetFunc_Key==1 or self.SetFunc_Key==2:
                if self.Setting_Func==1:
                    self.Setting_Func = 5
                else:
                    self.Setting_Func = 1
        if self.Setting_event==2:   #PauseSetting
            if self.SetFunc_Key==1:
                if self.Setting_Func==4:
                    self.Setting_Func = 2
                elif self.Setting_Func==2:
                    self.Setting_Func = 3
                else:
                    self.Setting_Func = 4
            elif self.SetFunc_Key==2:
                if self.Setting_Func==4:
                    self.Setting_Func = 3
                elif self.Setting_Func==3:
                    self.Setting_Func = 2
                else:
                    self.Setting_Func = 4
        elif self.Setting_event==3:   #GameOver
            if self.SetFunc_Key==1 or self.SetFunc_Key==2:
                if self.Setting_Func==1:
                    self.Setting_Func = 3
                else:
                    self.Setting_Func = 1
        if self.Enter and self.Setting_event>0:
            if self.Setting_Func==1:
                if self.MENU:
                    self.MENU = False
                    Props.Load_show = Ball.Load_show = False
                    self.UI = 3
                    self.GAME = True
                    pygame.mixer.music.fadeout(1000)
                    if not self.MUTE:
                        pygame.mixer.music.load('ext/game_msc.wav')
                        pygame.mixer.music.play(-1)
                self.Game_RESTART = True
            elif self.Setting_Func==2:
                if self.MUTE:
                    Props.MUTE = self.MUTE = False
                    pygame.mixer.music.load('ext/game_msc.wav')
                    pygame.mixer.music.play(-1)
                else:
                    Props.MUTE = self.MUTE= True
                    pygame.mixer.music.stop()
            elif self.Setting_Func == 3:
                self.UI = 1
                if not self.MUTE:
                    pygame.mixer.music.load('ext/background_msc.wav')
                    pygame.mixer.music.play(-1)
            elif self.Setting_Func == 4:
                self.Game_PAUSE = False
            else:
                self.UI = 2
                self.MENU = False
            if self.Game_PAUSE_setting and not self.Setting_Func==2:
                self.Game_PAUSE_setting = False
            self.Enter = False
            if not self.Setting_Func==2:
                self.Setting_event = 0
        self.SetFunc_Key = 0

    def Display_GameLEVEL(self):
        if self.Game_LEVEL_Fail:
            self.Setting(Ball.x - 2, self.Eye[1], Ball.z+10,1)
            self.Setting(Ball.x + 2, self.Eye[1], Ball.z + 10, 3)
            self.Setting_event = 3
        elif self.Game_LEVEL_Complete:
            if self.Level==2:
                self.Level_INFO(Ball.x, 0,Ball.z+8.1)
                self.DisplayText("LEVEL ", (850, 350, 9), (1, 1, 1), 0.015)
                self.DisplayText(str(self.Level - 1), (1250, 350, 9), (1, 1, 1), 0.015)
                self.DisplayText("COMPLETE", (1280, 250, 9), (1, 1, 1), 0.01)
                self.DisplayText("TIME", (1500, -150, 9), (1, 1, 1), 0.009)
                self.DisplayText(str(self.time_level[self.Level-2]), (1900, -150, 9), (1, 1, 1), 0.009)
                self.DisplayText("SCORE", (1400, -500, 9), (1, 1, 1), 0.009)
                self.DisplayText(str(self.score[self.Level-2]), (1900, -500, 9), (1, 1, 1), 0.009)
                self.DisplayText("CONTINUE", (1700, -1280, 9), (1, 1, 1), 0.008)
            elif self.Level==3:
                self.Level_INFO(Ball.x, -23,Ball.z+8.1)
                self.DisplayText("LEVEL ", (9600, -2700, 9), (1, 1, 1), 0.015)
                self.DisplayText(str(self.Level - 1), (10050, -2700, 9), (1, 1, 1), 0.015)
                self.DisplayText("COMPLETE", (14480, -4350, 9), (1, 1, 1), 0.01)
                self.DisplayText("TIME", (16200, -5300, 9), (1, 1, 1), 0.009)
                self.DisplayText(str(self.time_level[self.Level - 2]), (16600, -5300, 9), (1, 1, 1), 0.009)
                self.DisplayText("SCORE", (16100, -5700, 9), (1, 1, 1), 0.009)
                self.DisplayText(str(self.score[self.Level-2]), (16600, -5700, 9), (1, 1, 1), 0.009)
                self.DisplayText("CONTINUE", (18200, -7020, 9), (1, 1, 1), 0.008)
            elif self.Level==4:
                self.Level_INFO(Ball.x, 13, Ball.z + 8.1)
                self.DisplayText("LEVEL ", (17760, 2150, 9), (1, 1, 1), 0.015)
                self.DisplayText(str(self.Level - 1), (18220, 2150, 9), (1, 1, 1), 0.015)
                self.DisplayText("COMPLETE", (26720, 3000, 9), (1, 1, 1), 0.01)
                self.DisplayText("TIME", (29480, 3000, 9), (1, 1, 1), 0.009)
                self.DisplayText(str(self.time_level[self.Level - 2]), (30220, 3000, 9), (1, 1, 1), 0.009)
                self.DisplayText("SCORE", (29480, 2750, 9), (1, 1, 1), 0.009)
                self.DisplayText(str(self.score[self.Level - 2]), (30220, 2750, 9), (1, 1, 1), 0.009)
                self.DisplayText("TOTALTIME", (33150, 2800, 9), (1, 0, 0), 0.008)
                self.DisplayText(str(sum(self.time_level)), (34000, 2800, 9), (1, 0, 0), 0.008)
                self.DisplayText("TOTALSCORE", (33150, 2500, 9), (1, 0, 0), 0.008)
                self.DisplayText(str(sum(self.score)+Ball.hp*800), (34000, 2500, 9), (1, 0, 0), 0.008)
                self.DisplayText("CONTINUE", (33500, 2000, 9), (1, 1, 1), 0.008)
        elif self.Game_LEVEL_Warn:
            Props.Level_show = True
            if not self.MUTE and self.Game_LEVEL_Warn_play:
                effect = pygame.mixer.Sound('ext/Level_Warn.wav')
                effect.play()
                self.Game_LEVEL_Warn_play = False
            if self.Level==1:
                self.Level_INFO(Ball.x, 13,Ball.z+8.1)
                self.DisplayText("LEVEL ", (-14550, 2150, 9), (1, 1, 1), 0.015)
                self.DisplayText(str(self.Level), (-14150, 2150, 9), (1, 1, 1), 0.015)
                self.DisplayText("WARNING ", (-14600, 1950, 9), (1, 0, 0), 0.015)
                self.DisplayText("WARNING ", (-14605, 1955, 9), (1, 0, 0), 0.015)
                self.DisplayText("ALIEN EGG", (-24220, 2400, 9), (1, 0, 0), 0.009)
                self.DisplayText("Don't", (-27420, 2450, 9), (1, 0, 1), 0.008)
                self.DisplayText("Touch", (-27080, 2450, 9), (1, 0, 1), 0.008)
                self.DisplayText("Them", (-26670, 2450, 9), (1, 0, 1), 0.008)
                self.DisplayText("CONTINUE", (-27180, 2000, 9), (1, 1, 1), 0.008)
            elif self.Level==2:
                self.Level_INFO(Ball.x, 0, Ball.z + 8.1)
                self.DisplayText("LEVEL ", (820, 350, 9), (1, 1, 1), 0.015)
                self.DisplayText(str(self.Level), (1230, 350, 9), (1, 1, 1), 0.015)
                self.DisplayText("WARNING ", (795, 150, 9), (1, 0, 0), 0.015)
                self.DisplayText("WARNING ", (800, 155, 9), (1, 0, 0), 0.015)
                self.DisplayText("BLACK HOLE", (1370, -450, 9), (1, 0, 0), 0.009)
                self.DisplayText("Mind", (1530, -830, 9), (1, 0, 1), 0.008)
                self.DisplayText("Your", (1890, -830, 9), (1, 0, 1), 0.008)
                self.DisplayText("Step", (2240, -830, 9), (1, 0, 1), 0.008)
                self.DisplayText("CONTINUE", (1700, -1280, 9), (1, 1, 1), 0.008)
            elif self.Level==3:
                self.Level_INFO(Ball.x, -23,Ball.z+8.1)
                self.DisplayText("LEVEL ", (9600, -2700, 9), (1, 1, 1), 0.015)
                self.DisplayText(str(self.Level), (10050, -2700, 9), (1, 1, 1), 0.015)
                self.DisplayText("WARNING ", (9600, -2900, 9), (1, 0, 0), 0.015)
                self.DisplayText("WARNING ", (9605, -2895, 9), (1, 0, 0), 0.015)
                self.DisplayText("SHURIKEN", (16150, -5700, 9), (1, 0, 0), 0.009)
                self.DisplayText("Never", (18000, -6600, 9), (1, 0, 1), 0.008)
                self.DisplayText("Turn", (18400, -6600, 9), (1, 0, 1), 0.008)
                self.DisplayText("Back", (18750, -6600, 9), (1, 0, 1), 0.008)
                self.DisplayText("CONTINUE", (18200, -7020, 9), (1, 1, 1), 0.008)
        else:
            Props.Level_show = False

    def Display_GameINFO(self):
        if self.Game_PAUSE:
            self.time = self.time_pause-self.time_last
        else:
            self.time = self.time_run - self.time_last
        if self.Level==4:
            score,level,time = "-","-","-"
        else:
            score = str(self.score[self.Level-1])
            level = str(self.Level)
            time = str(self.time)
        self.DisplayText("LEVEL : " + level, (350, 570), (1, 1, 1), 0)
        self.DisplayText("LIFE : " + str(Ball.hp), (15, 5), (1, 1, 1), 0)
        self.DisplayText("TIME : " + time, (350, 5), (1, 1, 1), 0)
        self.DisplayText("SCORE : " + score, (600,5), (1,1,1), 0)

    def Score_update(self):
        score_collect = 0
        if 1<=self.Level<=3:
            if not Props.Heart_show and self.Heart_score:
                score_collect += 350
                self.Heart_score = False
            if self.Level>1:
                if not Props.Key_show[0] and self.Key_score[0]:
                    score_collect += 320
                    self.Key_score[0] = False
                elif not Props.Key_show[1] and self.Key_score[1]:
                    score_collect += 320
                    self.Key_score[1] = False
            if Props.collided:
                self.score[self.Level-1] -= 255
                self.Bonus = 0
                Props.collided = False
                if Ball.hp>1:
                    self.time_last+=1
            if score_collect!=0:
                self.score[self.Level-1] += score_collect

    def DisplayText(self, text, pos, color, Sc):
        glColor3fv(color)
        if Sc==0:
            glWindowPos2fv(pos)
            for ch in text:
                glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ctypes.c_int(ord(ch)))
        else:
            glPushMatrix()
            glScalef(Sc, Sc/2, 1)
            glTranslatef(pos[0], pos[1], pos[2])
            for ch in text:
                glutStrokeCharacter(GLUT_STROKE_ROMAN, ctypes.c_int(ord(ch)))
            glPopMatrix()

    def Level_update(self):
        if self.Level==1 and Ball.y<6 and self.Lvl_update==2:
            self.Level = 2
        elif self.Level==2 and Ball.x > 147 and Ball.y >-20 and self.Lvl_update==3:
            self.Level = 3
        elif self.Level==3 and Ball.x >270 and Ball.y<8 and self.Lvl_update==4:
            self.Level = 4
        if self.Lvl_update==1 and self.Level == 1:
            self.Reset_ALL()
        elif self.Lvl_update==2 and self.Level == 2:
            self.Reset_ALL()
        elif self.Lvl_update==3 and self.Level == 3:
            self.Reset_ALL()
        elif self.Lvl_update==4 and self.Level == 4:
            self.Reset_ALL()

    def Reset_ALL(self):
        self.Lvl_update += 1
        if self.Level==1:
            self.Game_LEVEL_Warn, self.Game_PAUSE = True, True
        else:
            self.score[self.Level - 2] += self.Bonus
            self.Game_LEVEL_Complete, self.Game_PAUSE = True, True
            if self.Level<=3:
                self.Game_LEVEL_Warn = True
        if not self.Level == 4:
            Ball.Lvl = Props.Lvl = Map.Lvl = self.Level
            Ball.RESET(Map.update())
            Props.RESET()
            self.Key_score = [True, True]
            self.Heart_score = True
            self.Bonus = 100
        self.time_level[self.Level - 2] = self.time
        if self.time > 0:
            self.score[self.Level - 2] += int(100000*(self.Level-1) / self.time_level[self.Level - 2])
        self.time_last = self.time_run
        self.Game_LEVEL_Warn_play = True
        if not self.MUTE and self.Level==4:
            effect = pygame.mixer.Sound('ext/Win.wav')
            effect.play()

    def Background(self):
        if not self.MENU:
            glPointSize(2.7)
            glBegin(GL_POINTS)
            glColor3ub(28, 255, 226)
            for i in range(len(self.Star)):
                point = self.Star[i]
                if Ball.x-25<point[0]<Ball.x+25 and Ball.y-26<point[1]<Ball.y+26:
                    glVertex3f(point[0], point[1], point[2])
                if not self.Game_PAUSE:
                    point[0] -= point[3]
                if point[0]<-239:
                    point[0] = 297
            glEnd()

    def Star_list(self):
        for i in range(250):
            x = randint(-239, 297)
            y = randint(-42, 31)
            z = randint(-14, -9)
            vel = 2/randint(1, 5)
            self.Star.append([x,y,z, vel])

    def main(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.mixer.init()
        glutInit()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption('OUTERSPACE by Low Jun Hong BS18110173')
        glViewport(0, 0, display[0], display[1])
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, (display[0] / display[1]), 0.1, 180)
        glMatrixMode(GL_MODELVIEW)
        clock = pygame.time.Clock()
        Left, Right, Up = False, False, False
        while True:
            clock.tick(80)
            self.time_run = int(pygame.time.get_ticks()/1000)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_a:
                        Left, Right = True, False
                    elif event.key == K_d:
                        Right, Left = True, False
                    elif event.key == K_w:
                        Up = True
                    elif event.key == K_ESCAPE:
                        if self.UI==2:
                            self.UI = 1
                        elif not self.Game_LEVEL_Warn and not self.Game_LEVEL_Complete and self.GAME:
                            if self.Game_PAUSE:
                                self.Game_PAUSE, self.Game_PAUSE_setting = False, False
                            else:
                                self.Game_PAUSE, self.Game_PAUSE_setting = True, True
                    elif event.key == K_SPACE:
                        if self.LOAD and self.LOAD_END:
                            self.UI = 1
                        elif self.Game_LEVEL_Complete:
                            self.Game_LEVEL_Complete = False
                        elif self.Game_LEVEL_Warn:
                            self.Game_LEVEL_Warn, self.Game_PAUSE = False, False
                        elif self.Setting_event>0 and self.Setting_Func>0:
                            self.Enter = True
                            if not self.MUTE:
                                effect = pygame.mixer.Sound('ext/Selection.wav')
                                effect.play()
                    elif self.Setting_event > 0:
                        if event.key == K_LEFT:
                            self.SetFunc_Key = 1
                            if not self.MUTE:
                                effect = pygame.mixer.Sound('ext/Selection.wav')
                                effect.play()
                        elif event.key == K_RIGHT:
                            self.SetFunc_Key = 2
                            if not self.MUTE:
                                effect = pygame.mixer.Sound('ext/Selection.wav')
                                effect.play()
                elif event.type == pygame.KEYUP:
                    if event.key == K_a:
                        Left = False
                    elif event.key == K_d:
                        Right = False
                    elif event.key == K_w:
                        Up = False
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glClearDepthf(1)
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LEQUAL)
            self.Interface()
            if self.UI==0:      #Loading
                self.Loading()
            elif self.UI==1:      #Menu
                self.Menu()
            elif self.UI==2:      #Control
                self.Control()
            elif self.UI==3:    #Game
                self.Update()
                if self.Game_PAUSE:
                    if not self.time_PAUSE_record:
                        self.time_pause = self.time_run
                        self.time_PAUSE_record = True
                else:
                    Ball.hp = Props.update(Ball.x, Ball.y, Ball.r, Ball.hp)
                    Ball.MAPupdate(Props.Door_info)
                    Ball.update(Left, Right, Up, Props.collided)
            Ball.draw()
            glPushMatrix()
            if self.MENU:
                glScalef(1,1.3,1)
            Props.draw(Ball.x, Ball.y, Map.color)
            Map.draw(Ball.x, Ball.y, Ball.r, Ball.hp)
            glPopMatrix()
            pygame.display.flip()

    def Control_Key(self, Xo, Yo, Zo):
        d = 0.5
        Vtx = [(Xo - d * 14, Yo + d * 5.5, Zo), (Xo - d * 12.5, Yo + d * 5.5, Zo), (Xo - d * 12.5, Yo + d * 4.5, Zo), (Xo - d * 14, Yo + d * 4.5, Zo),
               (Xo - d * 12, Yo + d * .5, Zo), (Xo - d * 10, Yo + d * .5, Zo), (Xo - d * 10, Yo - d * 1.5, Zo), (Xo - d * 12, Yo - d * 1.5, Zo),
               (Xo - d * 10, Yo + d * 2.5, Zo), (Xo - d * 8, Yo + d * 2.5, Zo), (Xo - d * 8, Yo + d * .5, Zo), (Xo - d * 10, Yo + d * .5, Zo),
               (Xo - d * 8, Yo + d * .5, Zo), (Xo - d * 6, Yo + d * .5, Zo), (Xo - d * 6, Yo - d * 1.5, Zo), (Xo - d * 8, Yo - d * 1.5, Zo),
               (Xo - d * 7, Yo - d * 3.5, Zo), (Xo + d * 4, Yo - d * 3.5, Zo), (Xo + d * 4, Yo - d * 5.5, Zo), (Xo - d * 7, Yo - d * 5.5, Zo),
               (Xo + d * 8, Yo - d * 3.5, Zo), (Xo + d * 10, Yo - d * 3.5, Zo), (Xo + d * 10, Yo - d * 5.5, Zo), (Xo + d * 8, Yo - d * 5.5, Zo),
               (Xo + d * 12, Yo - d * 3.5, Zo), (Xo + d * 14, Yo - d * 3.5, Zo), (Xo + d * 14, Yo - d * 5.5, Zo), (Xo + d * 12, Yo - d * 5.5, Zo)]
        Surf = [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15), (16, 17, 18, 19), (20, 21, 22, 23), (24, 25, 26, 27)]
        color = [(1, 0, 1), (1, 1, 0), (0, 1, 1), (0, 1, 1)]
        glBegin(GL_QUADS)
        for surface in Surf:
            x = 0
            for vertex in surface:
                glColor3fv(color[x])
                glVertex3fv(Vtx[vertex])
                x += 1
        glEnd()

    def Setting(self, Xo, Yo, Zo, func):
        Vtx, Surf, a, d = [], [], 0, 0.85
        if self.Setting_Func==func:
            glBegin(GL_TRIANGLE_FAN)
            glColor3ub(244,190,43)
            glVertex3f(Xo,Yo, Zo - 0.1)
            for i in range(361):
                x = d * math.cos(math.radians(i)) + Xo
                y = d * math.sin(math.radians(i)) + Yo
                glVertex3f(x,y,Zo-0.1)
            glEnd()
        if func == 1:  # play
            glBegin(GL_TRIANGLES)
            glColor3f(1,0,174/255)
            glVertex3f(Xo + d * 0.5, Yo, Zo)
            glVertex3f(Xo - d * 0.25, Yo + d * .5, Zo)
            glVertex3f(Xo - d * 0.25, Yo - d * .5, Zo)
            glEnd()
        elif func == 2:  # Mute
            MuteVtx = [(Xo - d * 0.5, Yo + d * .2, Zo), (Xo - d * 0.3, Yo + d * .2, Zo), (Xo + d * 0.45, Yo + d * .6, Zo), (Xo + d * 0.45, Yo - d * .6, Zo), (Xo - d * 0.3, Yo - d * .2, Zo), (Xo - d * 0.5, Yo - d * .2, Zo)]
            MuteSurf = [(0, 1, 4, 5), (1, 2, 3, 4)]
            glBegin(GL_QUADS)
            for surface in MuteSurf:
                for vertex in surface:
                    glColor3f(1,0,174/255)
                    glVertex3fv(MuteVtx[vertex])
            glEnd()
            if self.MUTE:
                glLineWidth(8)
                glBegin(GL_LINES)
                glVertex3f(Xo-d*0.7, Yo-d*.8,Zo)
                glVertex3f(Xo + d * 0.7, Yo + d*.8, Zo)
                glEnd()
        elif func == 3:  # Home
            glBegin(GL_TRIANGLES)
            glColor3f(1,0,174/255)
            glVertex3f(Xo, Yo + d * .7, Zo)
            glVertex3f(Xo + d * 0.7, Yo + d * .1, Zo)
            glVertex3f(Xo - d * 0.7, Yo + d * .1, Zo)
            glEnd()
            HomeVtx = [(Xo - d * 0.5, Yo + d * .1, Zo), (Xo - d * 0.2, Yo + d * .1, Zo), (Xo + d * 0.2, Yo + d * .1, Zo), (Xo + d * 0.5, Yo + d * .1, Zo), (Xo + d * 0.5, Yo - d * .6, Zo), (Xo + d * 0.2, Yo - d * .6, Zo), (Xo + d * 0.2, Yo - d * .2, Zo),
                       (Xo - d * 0.2, Yo - d * .2, Zo), (Xo - d * 0.2, Yo - d * .6, Zo), (Xo - d * 0.5, Yo - d * .6, Zo)]
            HomeSurf = [(0, 1, 8, 9), (1, 2, 6, 7), (2, 3, 4, 5)]
            glBegin(GL_QUADS)
            for surface in HomeSurf:
                for vertex in surface:
                    glColor3f(1,0,174/255)
                    glVertex3fv(HomeVtx[vertex])
            glEnd()
        elif func == 4:  # Pause
            PauseVtx = [(Xo - d * .4, Yo + d * .5, Zo), (Xo - d * .1, Yo + d * .5, Zo), (Xo - d * .1, Yo - d * .5, Zo), (Xo - d * .4, Yo - d * .5, Zo),
                        (Xo + d * .1, Yo + d * .5, Zo), (Xo + d * .4, Yo + d * .5, Zo), (Xo + d * .4, Yo - d * .5, Zo), (Xo + d * .1, Yo - d * .5, Zo)]
            PauseSurf = [(0, 1, 2, 3), (4, 5, 6, 7)]
            glBegin(GL_QUADS)
            for surface in PauseSurf:
                for vertex in surface:
                    glColor3f(1,0,174/255)
                    glVertex3fv(PauseVtx[vertex])
            glEnd()
        elif func == 5:  # Control
            ControlVtx = [(Xo - d * .85, Yo + d * .2, Zo), (Xo - d * .45, Yo + d * .2, Zo), (Xo - d * .15, Yo, Zo), (Xo - d * .45, Yo - d * .2, Zo), (Xo - d * .85, Yo - d * .2, Zo),
                          (Xo + d * .85, Yo + d * .2, Zo), (Xo + d * .45, Yo + d * .2, Zo), (Xo + d * .15, Yo, Zo), (Xo + d * .45, Yo - d * .2, Zo), (Xo + d * .85, Yo - d * .2, Zo),
                          (Xo + d * .2, Yo + d * .85, Zo), (Xo + d * .2, Yo + d * .45, Zo), (Xo, Yo + d * .15, Zo), (Xo - d * .2, Yo + d * .45, Zo), (Xo - d * .2, Yo + d * .85, Zo),
                          (Xo + d * .2, Yo - d * .85, Zo), (Xo + d * .2, Yo - d * .45, Zo), (Xo, Yo - d * .15, Zo), (Xo - d * .2, Yo - d * .45, Zo), (Xo - d * .2, Yo - d * .85, Zo)]
            ControlSurf = [(0, 1, 3, 4), (1, 2, 3, 1), (5, 6, 8, 9), (6, 7, 8, 6), (10, 11, 13, 14), (11, 12, 13, 11), (15, 16, 18, 19), (16, 17, 18, 16)]
            glBegin(GL_QUADS)
            for surface in ControlSurf:
                for vertex in surface:
                    glColor3f(1,0,174/255)
                    glVertex3fv(ControlVtx[vertex])
            glEnd()
        for j in range(4):
            for i in range(72):
                if j == 0 or j == 2:
                    r = 1
                    if i == 71:
                        Surf.append((a, a - 71, a + 2, a + 72))
                    else:
                        Surf.append((a, a + 1, a + 73, a + 72))
                else:
                    r = 0.85
                if j < 2:
                    d = 0.2
                    if i == 71:
                        Surf.append((a + 144, a + 73, a - 71, a))
                    else:
                        Surf.append((a + 144, a + 145, a + 1, a))
                else:
                    d = -0.2
                x = r * math.cos(math.radians(i * 5)) + Xo
                y = r * math.sin(math.radians(i * 5)) + Yo
                Vtx.append([x, y, Zo + d])
                a += 1
        color = [(127/255,0,87/255), (127/255,0,87/255), (1,0,174/255), (1,0,174/255)]
        glBegin(GL_QUADS)
        for surface in Surf:
            x = 0
            for vertex in surface:
                glColor3fv(color[x])
                glVertex3fv(Vtx[vertex])
                x += 1
        glEnd()

    def Level_INFO(self, Tx, Ty, Tz):
        w, h, Vtx, X, Eqn, k = 6, 1.1, [], 0, 0, 0
        for k in range(2):
            if k == 1:
                w -= 0.3
            for j in range(4):
                for i in range(5):
                    if j == 0:
                        X = - w + 0.25 * i
                        Eqn = -0.8 * (X + (w - 1)) ** 2 + (w - 1)
                    elif j == 1:
                        X = (w - 1) + 0.25 * i
                        Eqn = -0.8 * (X - (w - 1)) ** 2 + (w - 1)
                    elif j == 2:
                        X = w - 0.25 * i
                        Eqn = 0.8 * (X - (w - 1)) ** 2 - (w - 1)
                    else:
                        X = - (w - 1) - 0.25 * i
                        Eqn = 0.8 * (X + (w - 1)) ** 2 - (w - 1)
                    Vtx.append((X, Eqn))
        SquareVtx = [(-w * 4 / 7, h - w * 0.9), (w * 4 / 7, h - w * 0.9), (w * 4 / 7, -h - w * 0.9), (-w * 4 / 7, -h - w * 0.9),
                     (-w * 3.6 / 7, h * 0.8 - w * 0.9), (w * 3.6 / 7, h * 0.8 - w * 0.9), (w * 3.6 / 7, -h * 0.8 - w * 0.9), (-w * 3.6 / 7, -h * 0.8 - w * 0.9)]
        glPushMatrix()
        glTranslatef(Tx, Ty, Tz)
        glBegin(GL_POLYGON)
        for v in Vtx:
            if k < 26:
                glColor3ub(1,59,10)
            else:
                glColor3ub(39,39,120)
                # k = 0
            glVertex2fv(v)
            k += 1
        glEnd()
        glLineWidth(3)
        glBegin(GL_LINE_LOOP)
        glColor3f(1, 1, 1)
        for v in range(int(len(Vtx) / 2)):
            glVertex2fv(Vtx[v])
        glEnd()
        glBegin(GL_LINE_LOOP)
        # glColor3f(1, 1, 1)
        for v in range(int(len(Vtx) / 2), len(Vtx)):
            glVertex2fv(Vtx[v])
        glEnd()
        glBegin(GL_POLYGON)
        glColor3ub(27, 107, 57)
        for v in SquareVtx:
            glVertex2fv(v)
        glEnd()
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        glColor3f(1, 1, 1)
        for v in range(int(len(SquareVtx) / 2)):
            glVertex2fv(SquareVtx[v])
        glEnd()
        glBegin(GL_LINE_LOOP)
        # glColor3f(1, 1, 1)
        for v in range(int(len(SquareVtx) / 2), len(SquareVtx)):
            glVertex2fv(SquareVtx[v])
        glEnd()
        glPopMatrix()

if __name__ == "__main__":
    Game = BounceMain()
    Game.main()
    del Ball
    del Map
    del Props