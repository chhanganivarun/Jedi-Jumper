import colorama
from character import Character
import numpy as np
from board import Board
from din import Din
import time
from kbhit import KBHit
import sys
from bullet import Bullet
from coin import Coin
from magnet import Magnet
from beam import Beam
from dragon import Dragon


def check_collisions(board,din,coins,bullets,beams,dragon):
    """
        din coin done
        din bullet done
        din beam done
        beam bullet done
    """
    # pos = lambda y, x: '\x1b[%d;%dH' % (y, x)

    dpos = din.get_pos()
    # dpos = (dpos[0],board.get_window_size()[1] - dpos[1])
    dh,dw = din.get_dim()
    posi = board.get_current_pos()
    for coin in coins:
        if coin.is_taken():
            continue
        x,y = coin.get_pos()
        h,w = coin.get_dim()
        horiz = False
        vert = False
        if x<=dpos[0]+posi and dpos[0]+posi-x<=w:
            horiz = True
        elif x> dpos[0]+posi and x-dpos[0]-posi < dw:
            horiz = True
        if y<=dpos[1] and dpos[1]-y<=dh:
            vert = True
        elif y> dpos[1] and y-dpos[1] < h:
            vert = True
        if horiz == True and vert == True:
            din.inc_score()
            coin.take()
            coins.pop(coins.index(coin))
            # print(pos(0,150),end = '')
            # print(din.get_pos(),dpos,x,y,x+w,y+h,state)
            # time.sleep(5)
    
    for beam in beams:
        # direc = beam.get_direction()
        if beam.is_taken():
            continue
        x,y = beam.get_pos()
        h,w = beam.get_dim()
        horiz = False
        vert = False
        if y <= dpos[1] and dpos[1] - y <= dh:
            vert = True
        elif y> dpos[1] and y-dpos[1] < h:
            vert = True
        if x <= dpos[0]+posi and dpos[0]+posi -x <= w:
            horiz = True
        elif x >= dpos[0]+posi and x-dpos[0]-posi <= dw:
            horiz = True

        if horiz == True and vert == True:
            din.dec_life()
            beam.take()
            beams.pop(beams.index(beam))

    for bullet in bullets:
        if bullet.is_taken():
            continue
        x,y = bullet.get_pos()
        h,w = bullet.get_dim()
        horiz = False
        vert = False
        if x<=dpos[0] and dpos[0]-x<=w:
            horiz = True
        elif x> dpos[0] and x-dpos[0] < dw:
            horiz = True
        if y<=dpos[1] and dpos[1]-y<=dh:
            vert = True
        elif y> dpos[1] and y-dpos[1] < h:
            vert = True
        if horiz == True and vert == True:
            din.dec_life()
            bullet.take()
            bullets.pop(bullets.index(bullet))
            
        for beam in beams:
            # direc = beam.get_direction()
            if beam.is_taken():
                continue
            ex,ey = beam.get_pos()
            eh,ew = beam.get_dim()
            horiz = False
            vert = False
            if ey <= y and y - ey <= h:
                vert = True
            elif ey> y and ey-y < eh:
                vert = True
            if ex <= x+posi and x+posi -ex <= ew:
                horiz = True
            elif ex >= x+posi and ex-x-posi <= w:
                horiz = True

            if horiz == True and vert == True:
                beam.take()
                bullet.take()
                bullets.pop(bullets.index(bullet))
                beams.pop(beams.index(beam))

    

    if not dragon.is_hibernating():
        """
            dragon bullet
        """
        dpos = dragon.get_pos()
        dh,dw = dragon.get_dim()
        for bullet in bullets:
            if bullet.is_taken():
                continue
            x,y = bullet.get_pos()
            h,w = bullet.get_dim()
            horiz = False
            vert = False
            if x<=dpos[0] and dpos[0]-x<=w:
                horiz = True
            elif x> dpos[0] and x-dpos[0] < dw:
                horiz = True
            if y<=dpos[1] and dpos[1]-y<=dh:
                vert = True
            elif y> dpos[1] and y-dpos[1] < h:
                vert = True
            if horiz == True and vert == True:
                dragon.dec_life()
                bullet.take()
                bullets.pop(bullets.index(bullet))


if __name__ == '__main__':
    colorama.init()
    pos = lambda y, x: '\x1b[%d;%dH' % (y, x)
    din = Din(5)
    # din.greet()
    board = Board(din)
    board.draw()
    # din.print_sprite(0,2,0)
    kb = KBHit()

    bullets = []

    num_coins = 50
    coins = []
    coin_places_list = [np.array(range(board.get_bg_size()[0]+6,board.get_bg_size()[1]-board.get_window_size()[1],6)),np.array(range(din.get_ceil_ground()[1]+6,din.get_ceil_ground()[0],6))]
    for i in range(num_coins):
        x = (int(np.random.choice(coin_places_list[0])),int(np.random.choice(coin_places_list[1])))
        if x not in coins:
            coins.append(Coin(x[0],x[1]))
    coins = sorted(coins,key = lambda x: x.get_pos()[0])

    num_beams = 10
    beams = []
    beam_places_list = [np.array(range(board.get_bg_size()[0]+6,board.get_bg_size()[1]-board.get_window_size()[1],6)),np.array(range(din.get_ceil_ground()[1]+20,din.get_ceil_ground()[0]-10,6))]
    for i in range(num_beams):
        x = (int(np.random.choice(beam_places_list[0])),int(np.random.choice(beam_places_list[1])))
        if x not in coins and x[0]:
            beams.append(Beam(x[0],x[1],np.random.choice([7,8,12]),np.random.choice([0,1,2])))
    coins = sorted(coins,key = lambda x: x.get_pos()[0])


    magnet = Magnet(np.random.randint(board.get_window_size()[0]+10,board.get_bg_size()[1]-board.get_window_size()[1]))
    dragon = Dragon(din,board)
    # board.set_current_pos(board.get_bg_size()[1] - board.get_window_size()[1])
    kb.getch()
    while dragon.get_ended() == 0 and din.get_lives() > 0:
        board.update()
        if kb.kbhit():
            c = kb.getch()
            if c == 'q':
                break
            if c == 'k':
                board.speed_up()
            if c == 'j':
                board.speed_down()
            din_ret = din.update(c)
            if c == 's':
                bullets.append(din_ret)
        else:
            din.update()

        for bullet in bullets:
            bullet.update()
            xpos,ypos = bullet.get_pos()
            if xpos >= board.get_window_size()[1] or xpos<= 5:
                bullet.clear()
                x = bullets.pop(bullets.index(bullet))
                del bullet
                del x

        for beam in beams:
            x,y = beam.get_pos()
            xlen,ylen = beam.get_len()
            d = beam.get_direction()
            if x+xlen>=board.get_current_pos() and x< board.get_current_pos()+board.get_window_size()[1]-5:
                beam.display(board.get_current_pos())
            # elif x+xlen<board.get_current_pos():
            #     beam.pop(beams.index(beam))
            # elif x>= board.get_current_pos()+board.get_window_size()[1]-5:
            #     break


        for coin in coins:
            x,y = coin.get_pos()
            if x>=board.get_current_pos() and x< board.get_current_pos()+board.get_window_size()[1]-5:
                coin.display(board.get_current_pos())
            elif x<board.get_current_pos():
                coins.pop(coins.index(coin))
            elif x>= board.get_current_pos()+board.get_window_size()[1]-5:
                break

        if board.get_current_pos() >= board.get_bg_size()[1] - board.get_window_size()[1]-5:
            din.end()
            ret = dragon.update(board.get_current_pos())
            if ret is not None:
                bullets.append(ret)

        check_collisions(board,din,coins,bullets,beams,dragon)


        if magnet.get_pos()-magnet.get_affect() < din.get_pos()[0]+board.get_current_pos() and magnet.get_pos()>din.get_pos()[0]+board.get_current_pos():
            din.set_xacc(8)
            print(pos(0,120)+"Magnet Front")
        elif magnet.get_pos()+magnet.get_affect() > din.get_pos()[0]+board.get_current_pos() and magnet.get_pos()<din.get_pos()[0]+board.get_current_pos():
            din.set_xacc(-8)
            print(pos(0,120)+"Magnet Back ")
        else:
            din.set_xacc(0)
            print(pos(0,120)+'            ')
        

        time.sleep(0.05)

        print(pos(0,70)+"                     ") # Shield bar
        print(pos(0,20)+"Lives:{}".format(din.get_lives()))
        print(pos(0,40)+"Score:{}".format(din.get_score()))
        if din.get_ended():
            print(pos(0,170)+"Dragon Lives:{}".format(dragon.get_lives()))
        

        sys.stdout.flush()
    while kb.kbhit():
        kb.getch()
    kb.set_normal_term()
    print(chr(27)+'[2j')
    print('\033c')
    print('\x1bc')
    print('Score:{}'.format(din.get_score()))
    print('You Win' if din.get_lives() and din.get_ended() else 'You Lose')

