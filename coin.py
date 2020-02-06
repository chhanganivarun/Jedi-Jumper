import colorama
class Coin:
    def __init__(self,x,y):
        self.__xpos = x
        self.__ypos = y
        self.__taken = 0
        self.__sprite = ' '+colorama.Fore.WHITE+colorama.Back.YELLOW+'==\n|++|\n'+colorama.Style.RESET_ALL+' '+colorama.Fore.WHITE+colorama.Back.YELLOW+'==\n'+colorama.Style.RESET_ALL
        self.__clean_sprite = '   \n    \n   \n'
        self.__sprite_width = max([ len(x) for x in self.__clean_sprite.split('\n')])
        self.__sprite_height = len(self.__clean_sprite.split('\n'))

    def get_pos(self):
        return (self.__xpos,self.__ypos)

    def print_sprite(self,x,y,sp):
        y = 78-y
        pos = lambda y, x: '\x1b[%d;%dH' % (y, x)
        s = sp.split('\n')
        for i in range(len(s)):
            print(pos(y+i+1,x+1),end='')
            print(s[i],end='')
    
    def display(self,offset):
        if int(self.__xpos)-offset >= 0:
            self.print_sprite(int(self.__xpos)-offset,int(self.__ypos),self.__sprite if self.__taken == 0 else self.__clean_sprite)

    def clear(self):
        self.print_sprite(int(self.__xpos),int(self.__ypos),self.__clean_sprite)
    
    def get_dim(self):
        return (self.__sprite_height,self.__sprite_width)
    def take(self):
        self.__taken = 1
    def is_taken(self):
        return self.__taken

r"""
 ==
|++|
 ==
"""