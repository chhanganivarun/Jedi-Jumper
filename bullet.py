import colorama
class Bullet:
    def __init__(self,xpos,ypos,sp = 0):
        self.__xpos = xpos
        self.__ypos = ypos
        self.__sprite = colorama.Fore.BLUE+colorama.Back.RED+'___\n===/\n===\\\n¯¯¯\n'+colorama.Style.RESET_ALL if sp == 0 else  colorama.Fore.RED+colorama.Back.BLUE+' ___\n\\===\n/===\n ¯¯¯\n'+colorama.Style.RESET_ALL
        self.__sprite_width = max([ len(x) for x in '___\n===/\n===\\\n¯¯¯\n'.split('\n')])
        self.__sprite_height = len(self.__sprite.split('\n'))
        self.__clean_sprite = '\n'.join([ ''.join([' ' for j in i]) for i in self.__sprite.split('\n')])
        self.__update_time = 0.1
        self.__vel = 200 if sp == 0 else -200
        self.__taken = 0

    def print_sprite(self,x,y,sp):
        y = 78-y
        pos = lambda y, x: '\x1b[%d;%dH' % (y, x)
        s = sp.split('\n')
        for i in range(len(s)):
            print(pos(y+i+1,x+1),end='')
            print(s[i],end='')
    
    def display(self):
        self.print_sprite(int(self.__xpos),int(self.__ypos),self.__sprite if self.__taken == 0 else self.__clean_sprite)

    def update(self): # Please make a loop to delete all bullets that have been out of frame
        self.__xpos = self.__xpos + self.__vel * self.__update_time
        self.display()
    def get_pos(self):
        return (int(self.__xpos),int(self.__ypos))
    
    def clear(self):
        self.print_sprite(int(self.__xpos),int(self.__ypos),self.__clean_sprite)
    def get_dim(self):
        return (self.__sprite_height,self.__sprite_width)
    def take(self):
        self.__taken = 1
    def is_taken(self):
        return self.__taken




r"""
___
===\
===/
¯¯¯

 ___
/===
\===
 ¯¯¯
"""