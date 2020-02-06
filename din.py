from character import Character
import colorama
import time
import sys
import numpy as np
from bullet import Bullet

pos = lambda y, x: '\x1b[%d;%dH' % (y, x)

class Din(Character):
    def __init__(self,lives=None):
        Character.__init__(self,'Din',lives)
        self.__shield_active = 1
        self.__shield_tl = 2 # Shield time left after shield started
        self.__shield_ta = 0 # Time since spawn/last time shield used if shield_ta>
        # Sprite details
        self.__sprite = ["","","","",""]
        self.__sprite[0] = '           T"-.,_             \n           l:    ~{--._       \n          I:    .`     "c     \n .--.     l    /.-~"-.  |     \nY /~("-, I___ )Y .--r_Y |     \n\\_ "./~_~]__=~"j \\__L__[|     \n \\~" \\T T.__~<--r.__./  |___  \n  {--}]_L_,.) )( ( /\\___lc--\' \n Y /~("___\\ /^--^-`   \'--`    \n \\` " / \\7~"                  \n  [--]\\\\ \\\\                   \n  L :| Xo >\\                  \n /o |`  \\  \\\\                 \n [  I    \\ .\\\\                \n | :l     \\]/ \\               \n I_|`       \\\\.Y              \n]: L         Z_I              \nl]n[        7-."\\             \n\\\\ I         \\ \\ Y            \n \\"]\\         \\ ]|            \n  \\.\\\\         \\:L            \n   \\ \\\\  _      7_[           \n    \\_K^"_"=-,  _             \n    ].-"~ "~-.[] [            '
        self.__sprite[1] = '           T"-.,_             \n           l:    ~{--._       \n          I:    .`     "c     \n .--.     l    /.-~"-.  |     \nY /~("-, I___ )Y .--r_Y |     \n\\_ "./~_~]__=~"j \\__L__[|     \n \\~" \\T T.__~<--r.__./  |___  \n  {--}]_L_,.) )( ( /\\___lc--\' \n Y /~("___\\ /^--^-`   \'--`    \n \\` " / \\7~"                  \n  [--]\\\\ \\\\                   \n  L :|:|                      \n /o |` |`                     \n [  I   I                     \n | :l  :l                     \n  I_|` |`                     \n]: L  : L                     \nl]n[   n[                     \n\\\\ I \\\\ I                     \n \\"]\\ "]\\                     \n  \\.\\\\ \\\\                     \n   \\ \\\\ \\_                    \n    \\_K^"_"=-,  _  _          \n    ].-"~ "~-.[] [] [         '
        self.__sprite[2] = '           T"-.,_             \n           l:    ~{--._       \n          I:    .`     "c     \n .--.     l    \\.-~"-.  |     \nY \\~("-, I___ )Y .--r_Y |     \n/_ ".\\~_~]__=~"j /__L__[|     \n /~" /T T.__~<--r.__.\\  |___  \n  {--}]_L_,.) )( ( \\/___lc--\' \n Y \\~("___/ \\^--^-`   \'--`    \n /` " \\ /7~"                  \n  // //[--]                   \n   Xo >/ :|                   \n   /  //o |`                  \n    / .// I                   \n     /]\\ /l                   \n      //.Y                    \n        Z_I                   \n        |l7-."/               \n        |/ / / Y              \n        /  / ]|    _          \n        |/.//:L/_K^"_"=-,  _  \n        |_   ].-"~ "~-.[] [   \n        /_K^"_"=-,  _         \n        ].-"~ "~-.[] [        '
        self.__sprite[3] = '           T"-.,_             \n           l:    ~{--._       \n          I:    .`     "c     \n .--.     l    /.-~"-.  |     \nY /~("-, I___ )Y .--r_Y |     \n\\_ "./~_~]__=~"j \\__L__[|     \n \\~" \\T T.__~<--r.__./  |___  \n  {--}]_L_,.) )( ( /\\___lc--\' \n Y /~("___\\ /^--^-`   \'--`    \n \\` " / \\7~"                  \n  [--]\\\\ \\\\                   \n  L :|:|                      \n /o |` |`                     \n [  I   I                     \n | :l  :l                     \n  I_|` |`                     \n]: L  : L                     \nl]n[   n[                     \n\\\\ I \\\\ I                     \n \\"]\\ "]\\                     \n  \\.\\\\ \\\\                     \n   \\ \\\\ \\_                    \n    \\_K^"_"=-,  _  _          \n    ].-"~ "~-.[] [] [         '
        self.__sprite_width = max([ len(x) for x in self.__sprite[0].split('\n')])
        self.__sprite_height = len(self.__sprite[0].split('\n'))
        self.__sprite[4] = [ [  ' ' for j in range(self.__sprite_width) ] for i in range(self.__sprite_height)]
        temp = [ '' for i in range(self.__sprite_height)]
        for i in range(len(self.__sprite[4])):
            temp[i] = ''.join(self.__sprite[4][i])
        self.__sprite[4] = '\n'.join(temp)
        
        self.__acc = -9.8
        self.__xacc = 0
        self.__xvel = 0
        self.__ground = 10
        self.__ceil = 70
        self.__ypos = self.__ground+self.__sprite_height
        self.__xpos = self._xpos # Inheritance
        self.__update_time = 0.1
        self.__current_sprite = 0
        self.__vel = 0
        self.__end = 0
        self.__score = 0

        self.__prev = (self.__xpos,self.__ypos)

    def print_sprite(self,x,y,sp_no=0):
        y = 78-y
        pos = lambda y, x: '\x1b[%d;%dH' % (y, x)
        temp_sprite = np.array(self.__sprite[sp_no].split('\n'))
        s = temp_sprite
        for i in range(len(s)):
            print(pos(int(y+i+1),int(x+1)),end='')
            print(s[i],end='')
            if self.__shield_active:
                print(colorama.Fore.WHITE+colorama.Back.BLUE+'x'+colorama.Style.RESET_ALL,end = '')
    
    def accelarate(self):
        # self.__acc += 20
        self.__vel += 40
        # self.__acc = -9.8
        self.update_vel()
        

    def update_vel(self):
        
        if self.__vel>0 and self.__ypos<self.__ceil:
            self.__vel = self.__vel +self.__acc*self.__update_time
        elif self.__vel>0 and self.__ypos>=self.__ceil:
            self.__vel = 0
            # self.__acc = -9.8
        
        elif self.__acc<0 and self.__ypos-self.__sprite_height>self.__ground:
            self.__vel = self.__vel +self.__acc*self.__update_time    
        elif self.__acc<0 and self.__ypos-self.__sprite_height<=self.__ground:
            self.__vel = 0
            # self.__acc = 0
            # self.__acc = 0
        if self.__xacc !=0:
            if self.__xacc < 0 and self.__xpos <= 1:
                self.__xvel = 0
            elif self.__xacc <0:
                self.__xvel += self.__xacc * self.__update_time
            elif self.__xacc > 0 and self.__xpos >= 320-self.__sprite_width:
                self.__xvel = 0
            elif self.__xacc > 0:
                self.__xvel += self.__xacc * self.__update_time


        self.__vel = self.__vel +self.__acc*self.__update_time
        
        
    
    def update(self,inChar = None):
        if self.__shield_active:
            print(pos(0,70)+colorama.Back.GREEN+''.join(['x' for i in range(10 - 2*int(self.__update_time *self.__shield_tl))])+colorama.Style.RESET_ALL)
        elif self.__shield_ta*self.__update_time < 60/2:
            print(pos(0,70)+colorama.Back.BLUE+''.join(['+' for i in range(int((self.__shield_ta*self.__update_time)//3))])+colorama.Style.RESET_ALL)
        else:
            print(pos(0,70)+colorama.Back.RED+''.join(['O' for i in range(10)])+colorama.Style.RESET_ALL)
        self.__prev = (self.__xpos,self.__ypos)
        self.__shield_ta += 1
        if self.__shield_active:
            self.__shield_tl += 1
        if self.__shield_tl * self.__update_time>= 10/2:
            self.__shield_active = 0
        if (self.__xvel * self.__xacc) <0 :
            self.__xvel = 0 
        # self.display(4)
        if inChar != None:
            if inChar == 'w':
                self.accelarate()
            if inChar == 'a':
                if self.__xpos<=20:
                    self.__xpos = 1
                else:
                    self.__xpos -= 20
                if self.__xvel>0:
                    self.__xvel = 0
            if inChar == 'd':
                if self.__xpos>=300-self.__sprite_width:
                    self.__xpos = 320-self.__sprite_width
                else:
                    self.__xpos += 20
                if self.__xvel<0:
                    self.__xvel = 0
            if inChar == 's':
                return self.shoot()
            if inChar == ' ':
                return self.start_shield()
        self.update_vel()
        
        self.__ypos += self.__vel * self.__update_time if self.__ypos + self.__vel * self.__update_time - self.__sprite_height >self.__ground else self.__sprite_height + self.__ground - self.__ypos
        self.__ypos = self.__ypos if self.__ypos <= self.__ceil else self.__ceil

        self.__xpos += self.__xvel * self.__update_time if self.__xpos + self.__xvel * self.__update_time >= 1 else 1 - self.__xpos
        self.__xpos = self.__xpos if self.__xpos <= 320-self.__sprite_width else 320-self.__sprite_width
        

        self.__current_sprite = 10 if self.__ypos-self.__sprite_height>self.__ground else (self.__current_sprite+4)%40
        self.display(self.__current_sprite//10)

    def display(self,sp_no=0):
        self.print_sprite(int(self.__xpos),int(self.__ypos),sp_no if self.__end==0 else 1)

    def clear(self):
        self.display(4)

    def set_xacc(self,acc=8):
        self.__xacc = acc
    def get_pos(self):
        return (int(self.__xpos),int(self.__ypos))
    def dec_life(self):
        if self.__shield_active == 1:
            pass
        else:
            self._lives_left -= 1
    def shoot(self):
        bullet = Bullet(self.__xpos+self.__sprite_width,int(self.__ypos-self.__sprite_height/2))
        return bullet
    def get_ceil_ground(self):
        return (self.__ceil,self.__ground)
    def get_dim(self):
        return (self.__sprite_height,self.__sprite_width)
    def start_shield(self):
        if self.__shield_ta*self.__update_time >= 60/2:
            self.__shield_active = 1
            self.__shield_ta = 0
            self.__shield_tl = 5
    def end(self):
        self.__end = 1
    def get_ended(self):
        return self.__end
    def inc_score(self,sc = 50):
        self.__score += sc
    def get_score(self):
        return self.__score


# initial images:
r"""
            _,.-"T
      _.--{~    :l
    c"     `.    :I
    |  .-"~-.\    l     .--.
    | Y_r--. Y) ___I ,-"(~\ Y
    |[__L__/ j"~=__]~_~\." _/
 ___|  \.__.r--<~__.T T/ "~/
'--cl___/\ ( () ).,_L_]}--{
   `--'   `-^--^\ /___"(~\ Y
                 "~7/ \ " `/
                  // //]--[
                 /> oX |: L
                //  /  `| o\
               //. /    I  [
              / \]/     l: |
             Y.//       `|_I
             I_Z         L :]
            /".-7        [n]l
           Y / /         I //
           |] /         /]"/
           L:/         //./
          [_7      _  // /
            _  ,-="_"^K_/
           [ ][.-~" ~"-.]   
"""
r"""
            _,.-"T
      _.--{~    :l
    c"     `.    :I
    |  .-"~-.\    l     .--.
    | Y_r--. Y) ___I ,-"(~\ Y
    |[__L__/ j"~=__]~_~\." _/
 ___|  \.__.r--<~__.T T/ "~/
'--cl___/\ ( () ).,_L_]}--{
   `--'   `-^--^\ /___"(~\ Y
                 "~7/ \ " `/
                  // //]--[
                     |:|: L
                    `| `| o\
                    I   I  [
                    l:  l: |
                    `| `|_I
                    L :  L :]
                    [n   [n]l
                    I // I //
                    /]" /]"/
                    // //./
                   _/ // /
         _  _  ,-="_"^K_/
        [ ][ ][.-~" ~"-.]
"""
r"""
           T"-.,_
           l:    ~{--._
          I:    .`     "c
 .--.     l    /.-~"-.  |
Y /~("-, I___ )Y .--r_Y |
\_ "./~_~]__=~"j \__L__[|
 \~" \T T.__~<--r.__./  |___
  {--}]_L_,.) )( ( /\___lc--'
 Y /~("___\ /^--^-`   '--`
 \` " / \7~"
  \\ \\[--]
   Xo >\ :| 
   \  \\o |`
    \ .\\ I    
     \]/ \l
      \\.Y
        Z_I
        |l7-."\
        |\ \ \ Y
        \  \ ]|    _
        |\.\\:L\_K^"_"=-,  _
        |_   ].-"~ "~-.[] [
        \_K^"_"=-,  _
        ].-"~ "~-.[] [
"""