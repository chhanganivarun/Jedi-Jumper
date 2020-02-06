import colorama
from bullet import Bullet
from character import Character
class Dragon(Character):
    def __init__(self,din,board,shots = 10,lives = None):
        Character.__init__(self,'Dragon',lives)
        self.__din = din
        self.init_sprite()
        self.__sprite_width = max([ len(x) for x in self.__sprite.split('\n')])
        self.__sprite_height = len(self.__sprite)
        self.__sprite = colorama.Fore.RED+ self.__sprite + colorama.Style.RESET_ALL
        self.__clean_sprite = '\n'.join([ ''.join([' ' for j in range(self.__sprite_width)]) for i in range(self.__sprite_height)])

        self.__shots_left = shots
        self.__time = 0
        self.__time_thresh = 1
        self.__update_time = 0.1
        self.__ypos = self.__din.get_pos()[1]
        self.__xpos = board.get_window_size()[1] - self.__sprite_width -1
        self.__end = 0
        self.__hibernating = 1

    def update(self,offset):
        self.__hibernating = 0
        self.__time += self.__update_time
        self.display(offset)
        if self.__shots_left <=0:
            self.__end = 1
        if self.__time>= self.__time_thresh:
            x = self.shoot()
            self.__ypos = self.__din.get_pos()[1] - self.__din.get_dim()[0]/2
            self.__shots_left -=1
            self.__time = 0
            return x
        else:
            return None
    
    def print_sprite(self,x,y,sp):
        y = 78-y
        pos = lambda y, x: '\x1b[%d;%dH' % (y, x)
        s = sp.split('\n')
        for i in range(len(s)):
            print(pos(y+i+1,x+1),end='')
            print(s[i],end='')

    def display(self,offset):
        # if int(self.__xpos)-offset >= 0:
        self.print_sprite(int(self.__xpos),int(self.__ypos),self.__sprite)

    def get_pos(self):
        return (int(self.__xpos),int(self.__ypos))
    
    def clear(self):
        self.print_sprite(int(self.__xpos),int(self.__ypos),self.__clean_sprite)

    def get_dim(self):
        return (self.__sprite_height,self.__sprite_width)

        
    def shoot(self):
        bullet = Bullet(self.__xpos-6,int(self.__ypos),1)
        return bullet

    def dec_life(self):
        self._lives_left -= 1

    def is_hibernating(self):
        return self.__hibernating

    def get_ended(self):
        return self.__end

    def init_sprite(self):
        self.__sprite = r"""                      ,-,-      
                     / / |      
   ,-'             _/ / /       
  (-_          _,-' `Z_/        
   "#:      ,-'_,-.    \  _     
    #'    _(_-'_()\     \" |    
  ,--_,--'                 |    
 / ""                      L-'\ 
 \,--^---v--v-._        /   \ | 
   \_________________,-'      | 
                    \           
                     \          """
        
