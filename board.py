import numpy as np
import colorama
import sys
from din import Din
pos = lambda y, x: '\x1b[%d;%dH' % (y, x)
class Board:
    def __init__(self,din):
        self.__window_size = (77,337)
        self.__bg_size = (77,10000)
        self.__current_pos = 0
        self.__current_pos_float = 0
        self.__vel = 220
        self.__update_time = 0.1
        self.__ceil, self.__ground = din.get_ceil_ground()
        self.din = din
        self.mat = np.full((self.__bg_size[0],self.__bg_size[1]),colorama.Fore.RED+' '+colorama.Style.RESET_ALL)
        self.add_bg()
        for i in range(self.__bg_size[0]-self.__ceil):
            self.mat[i] = np.full((1,self.__bg_size[1]),colorama.Fore.RED+'#'+colorama.Style.RESET_ALL)
        self.mat[self.__bg_size[0]-10] = np.full((1,self.__bg_size[1]),colorama.Fore.BLUE+'_'+colorama.Style.RESET_ALL)
        for i in range(self.__bg_size[1]):
            self.mat[self.__bg_size[0]-self.__ground][i] = colorama.Fore.BLUE+str(i%10)+colorama.Style.RESET_ALL
        for i in range(self.__bg_size[0]-self.__ground+1,self.__bg_size[0]):
            self.mat[i] = np.full((1,self.__bg_size[1]),colorama.Fore.GREEN+'+'+colorama.Style.RESET_ALL)
        
        print(chr(27)+'[2j')
        print('\033c')
        print('\x1bc')
    def draw(self):
        
        print(pos(1,1))
        for i in range(self.__window_size[0]):
            for j in range(self.__window_size[1]):
                # if ' ' not in self.mat[i][j+self.__current_pos]:
                print(self.mat[i][j+self.__current_pos],end = '')
            print('')
            sys.stdout.flush()

    def print_bg(self,x,y,height,width):
        y = self.__bg_size[0]+1-y
        pos = lambda y, x: '\x1b[%d;%dH' % (y, x)

        s = self.mat[y-1:y+height-1,self.__current_pos+x-1:self.__current_pos+x+width-1]
        for i in range(len(s)):
            print(pos(y+i+1,x+1),end='')
            for x in range(len(s[i])):
                print(s[i][x],end='')
            # print(s[i],end='')
        # sys.stdout.flush()

    def clear_sprite(self,obj):
        x = obj.clear()
        if x==0:
            return
        xpos,ypos = obj.get_pos()
        height,width = obj.get_dim()
        self.print_bg(xpos,ypos,height,width)

    def update(self):
        # self.clear_sprite(self.din)
        self.__current_pos_float = min(self.__current_pos_float+self.__vel*self.__update_time,self.__bg_size[1]-self.__window_size[1])
        self.__current_pos = int(self.__current_pos_float)
        self.draw()

    def get_window_size(self):
        return self.__window_size
    def get_bg_size(self):
        return self.__bg_size

    def get_current_pos(self):
        return self.__current_pos
    def speed_up(self):
        self.__vel = min(self.__vel+20,1000)
    
    def speed_down(self):
        self.__vel = max(self.__vel-20,120)
    def set_current_pos(self,posi):
        if type(posi) is int and posi<=self.__bg_size[1]-self.__window_size[1]:
            self.__current_pos_float = posi

    def add_bg(self):
        a = r"""______/\\\\\\\\\\\__/\\\\\\\\\\\\\\\__/\\\\\\\\\\\\_____/\\\\\\\\\\\__________________________/\\\\\\\\\\\__/\\\________/\\\__/\\\\____________/\\\\__/\\\\\\\\\\\\\___        
 _____\/////\\\///__\/\\\///////////__\/\\\////////\\\__\/////\\\///__________________________\/////\\\///__\/\\\_______\/\\\_\/\\\\\\________/\\\\\\_\/\\\/////////\\\_       
  _________\/\\\_____\/\\\_____________\/\\\______\//\\\_____\/\\\_________________________________\/\\\_____\/\\\_______\/\\\_\/\\\//\\\____/\\\//\\\_\/\\\_______\/\\\_      
   _________\/\\\_____\/\\\\\\\\\\\_____\/\\\_______\/\\\_____\/\\\_________________________________\/\\\_____\/\\\_______\/\\\_\/\\\\///\\\/\\\/_\/\\\_\/\\\\\\\\\\\\\/__     
    _________\/\\\_____\/\\\///////______\/\\\_______\/\\\_____\/\\\_________________________________\/\\\_____\/\\\_______\/\\\_\/\\\__\///\\\/___\/\\\_\/\\\/////////____    
     _________\/\\\_____\/\\\_____________\/\\\_______\/\\\_____\/\\\_________________________________\/\\\_____\/\\\_______\/\\\_\/\\\____\///_____\/\\\_\/\\\_____________   
      __/\\\___\/\\\_____\/\\\_____________\/\\\_______/\\\______\/\\\__________________________/\\\___\/\\\_____\//\\\______/\\\__\/\\\_____________\/\\\_\/\\\_____________  
       _\//\\\\\\\\\______\/\\\\\\\\\\\\\\\_\/\\\\\\\\\\\\/____/\\\\\\\\\\\_____________________\//\\\\\\\\\_______\///\\\\\\\\\/___\/\\\_____________\/\\\_\/\\\_____________ 
        __\/////////_______\///////////////__\////////////_____\///////////_______________________\/////////__________\/////////_____\///______________\///__\///______________"""
        
        self.__insert_art_at_loc(20,(self.__window_size[0]-self.__ceil)+10,a)
        h,w = self.__get_h_w_str(a)


        a = r""" _______  ______    _______  _______  _______        _______        ___   _  _______  __   __        _______  _______        _______  _______  _______  ______    _______ 
|       ||    _ |  |       ||       ||       |      |   _   |      |   | | ||       ||  | |  |      |       ||       |      |       ||       ||   _   ||    _ |  |       |
|    _  ||   | ||  |    ___||  _____||  _____|      |  |_|  |      |   |_| ||    ___||  |_|  |      |_     _||   _   |      |  _____||_     _||  |_|  ||   | ||  |_     _|
|   |_| ||   |_||_ |   |___ | |_____ | |_____       |       |      |      _||   |___ |       |        |   |  |  | |  |      | |_____   |   |  |       ||   |_||_   |   |  
|    ___||    __  ||    ___||_____  ||_____  |      |       |      |     |_ |    ___||_     _|        |   |  |  |_|  |      |_____  |  |   |  |       ||    __  |  |   |  
|   |    |   |  | ||   |___  _____| | _____| |      |   _   |      |    _  ||   |___   |   |          |   |  |       |       _____| |  |   |  |   _   ||   |  | |  |   |  
|___|    |___|  |_||_______||_______||_______|      |__| |__|      |___| |_||_______|  |___|          |___|  |_______|      |_______|  |___|  |__| |__||___|  |_|  |___|  """
        self.__insert_art_at_loc(20,(self.__window_size[0]-self.__ceil)+20+h,a)

        a=r"""                                                         .       
                                              .         ;        
                 .              .              ;%     ;;         
                   ,           ,                :;%  %;          
                    :         ;                   :;%;'     .,   
           ,.        %;     %;            ;        %;'    ,;     
             ;       ;%;  %%;        ,     %;    ;%;    ,%'      
              %;       %;%;      ,  ;       %;  ;%;   ,%;'       
               ;%;      %;        ;%;        % ;%;  ,%;'         
                `%;.     ;%;     %;'         `;%%;.%;'           
                 `:;%.    ;%%. %@;        %; ;@%;%'              
                    `:%;.  :;bd%;          %;@%;'                
                      `@%:.  :;%.         ;@@%;'                 
                        `@%.  `;@%.      ;@@%;                   
                          `@%%. `@%%    ;@@%;                    
                            ;@%. :@%%  %@@%;                     
                              %@bd%%%bd%%:;                      
                                #@%%%%%:;;                       
                                %@@%%%::;                        
                                %@@@%(o);  . '                   
                                %@@@o%;:(.,'                     
                            `.. %@@@o%::;                        
                               `)@@@o%::;                        
                                %@@(o)::;                        
                               .%@@@@%::;                        
                               ;%@@@@%::;.                       
                              ;%@@@@%%:;;;.                      
                          ...;%@@@@@%%:;;;;,..                   """
        h,w = self.__get_h_w_str(a)
        for i in range(20):
            self.__insert_art_at_loc(self.__window_size[1]+i*w,self.__window_size[0]-self.__ceil+5,a)
        t = self.__window_size[1]+21*w
        a = r"""   ___________________________________________________________ 
  |                                                           |
  |     _____                                                 |
  |    |  |  |`-._______________________________________      |
  |    | ( ) |  | _  _  _  _  _  _  _  _  _  _ |   _____\     |
  |  [=|  |  |.-|| || || || || || || || || || ||-. \xxxxx\    |
  |  `-|  |  ||_||_||_||_||_||_||_||_||_||_||_||_|||~\XXXX\   |
  |  [=|  |  |  |______________________________|__`'-------)  |
  |  [=| ()=-| ]|__________|    |---/  \---|  /___________/   |
  |     \ |  |  |   |   /| `--._|__/____\__|_|     ()=-  /    |
  |      \()=- ]|  _|__/_|____.'             |________.+'     |
  |       \__|__|_/__________________________|_____.-'-'      |
  |                                    \_X                    |
  |                                       \                   |
  |                                                        LS |
  |___________________________________________________________|
                                                               
        Telgorn Corporation's Gamma-class Assault Shuttle      """        
        self.__insert_art_at_loc(t,self.__window_size[0]-self.__ceil+5,a)
        h,w = self.__get_h_w_str(a)
        t += 2*w

        a = r"""   _______________                            
 / \     / \     / \                          
|------------------|======|                   
| --    --    --    |==============llll----i++
|__________________|======|                   
   |             |                            
   |             |                            
   |             |                            
   |             |                            
   |             |                            
   |             |                            
   /`~\   /~~\   \  /~~\                      
  /   ~~`~    \ /~~~~   \                     
 /             \         \                    """
        self.__insert_art_at_loc(t,self.__window_size[0]-self.__ceil+5,a)
        h,w = self.__get_h_w_str(a)
        t += 2*w

        self.__insert_art_at_loc(t,self.__window_size[0]-self.__ceil+5,a)
        h,w = self.__get_h_w_str(a)
        t += 2*w

        self.__insert_art_at_loc(t,self.__window_size[0]-self.__ceil+5,a)
        h,w = self.__get_h_w_str(a)
        t += 2*w

        self.__insert_art_at_loc(t,self.__window_size[0]-self.__ceil+5,a)
        h,w = self.__get_h_w_str(a)
        t += 2*w

        self.__insert_art_at_loc(t,self.__window_size[0]-self.__ceil+5,a)
        h,w = self.__get_h_w_str(a)
        t += 2*w


        a = r"""88                                           
88                                           
88                                           
88,dPPYba,   ,adPPYba,  ,adPPYba, ,adPPYba,  
88P'    "8a a8"     "8a I8[    "" I8[    ""  
88       d8 8b       d8  `"Y8ba,   `"Y8ba,   
88b,   ,a8" "8a,   ,a8" aa    ]8I aa    ]8I  
8Y"Ybbd8"'   `"YbbdP"'  `"YbbdP"' `"YbbdP"'  """
        self.__insert_art_at_loc(self.__bg_size[1]-1-w-20,(self.__window_size[0]-self.__ceil)+10,a)
        
    def __get_h_w_str(self,strg):
        h = len(strg.split('\n'))
        w = max([len(x) for x in strg.split('\n')])
        return (h,w)
    def __insert_art_at_loc(self,x,y,strg):
        h,w = self.__get_h_w_str(strg)
        self.mat[y:y+h,x:x+w] = np.array([np.array([ a for a in x]) for x in strg.split('\n')])