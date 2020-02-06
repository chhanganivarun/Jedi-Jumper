import colorama
import numpy as np
class Beam:
    def __init__(self,x,y,length,direction=0):
        """
        direction:
                    0: horizontal
                    1: Vertical
                    2: 45 degree
        """
        self.__xpos = x
        self.__ypos = y
        self.__length = length
        self.__direction = direction
        self.__taken = 0 #beam hit by bullet or din
        if self.__direction == 0:
            # self.__sprite = np.full((1,self.__length),colorama.Back.YELLOW+'—'+colorama.Style.RESET_ALL)
            self.__sprite = colorama.Fore.YELLOW+'\n'.join([''.join([ '—' for j in range(self.__length)]) for i in range(1)])+colorama.Style.RESET_ALL
            self.__sprite = self.__sprite.replace('—',colorama.Back.YELLOW+'—'+colorama.Style.RESET_ALL)
            # self.__clean_sprite = np.full((1,self.__length),' ')
            self.__clean_sprite = '\n'.join([''.join([ ' ' for j in range(self.__length)]) for i in range(1)])
            self.__sprite_width = self.__length
            self.__sprite_height = 1
        elif self.__direction == 1:
            # self.__sprite = np.full((self.__length,1),colorama.Back.YELLOW+'|'+colorama.Style.RESET_ALL)
            self.__sprite = colorama.Fore.YELLOW+'\n'.join([''.join([ '|' for j in range(1)]) for i in range(self.__length)])+colorama.Style.RESET_ALL
            self.__sprite = self.__sprite.replace('|',colorama.Back.YELLOW+'|'+colorama.Style.RESET_ALL)
            self.__clean_sprite = '\n'.join([''.join([ ' ' for j in range(1)]) for i in range(self.__length)])
            self.__clean_sprite = np.full((self.__length,1),' ')
            self.__sprite_width = 1
            self.__sprite_height = self.__length
        elif self.__direction == 2:
            # self.__sprite = np.fill_diagonal(np.zeros((self.__length,self.__length)),colorama.Back.YELLOW+'\\'+colorama.Style.RESET_ALL)
            self.__sprite = colorama.Fore.YELLOW+'\n'.join([''.join([ '\\' if i == j else ' ' for j in range(self.__length)]) for i in range(self.__length)])+colorama.Style.RESET_ALL
            self.__sprite = self.__sprite.replace('\\',colorama.Back.YELLOW+'\\'+colorama.Style.RESET_ALL)
            
            self.__clean_sprite = '\n'.join([''.join([ ' ' for j in range(self.__length)]) for i in range(self.__length)])
            self.__sprite_width = self.__length
            self.__sprite_height = self.__length
    
    def print_sprite(self,x,y,sp):
        y = 78-y
        pos = lambda y, x: '\x1b[%d;%dH' % (y, x)
        s = sp.split('\n')
        for i in range(len(s)):
            print(pos(y+i+1,x+1),end='')
            # for j in range(len(s[i])):
            print(s[i],end='')
    
    def display(self,offset):
        if int(self.__xpos)-offset >= 0:
            self.print_sprite(int(self.__xpos)-offset,int(self.__ypos),self.__sprite if self.__taken == 0 else self.__clean_sprite)

    def clear(self):
        self.print_sprite(int(self.__xpos),int(self.__ypos),self.__clean_sprite)
    
    def get_pos(self):
        return (int(self.__xpos),int(self.__ypos))
    def get_len(self):
        return self.__sprite_width,self.__sprite_height
    def get_direction(self):
        return self.__direction
    def get_dim(self):
        return (self.__sprite_height,self.__sprite_width)
    def take(self):
        self.__taken = 1
    def is_taken(self):
        return self.__taken