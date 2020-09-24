import pygame
from pygame.locals import *
import time,random
import wx

class myPlane:
    '''自機'''
    def __init__(self,screen):
        self.x=200
        self.y=600
        self.screen = screen
        self.image=pygame.image.load('./images/me.png')
        self.bullet_list=[]
    def display(self):
        '''自機を描く'''
        self.screen.blit(self.image,(self.x,self.y))
        '''弾を描く'''
        for b in self.bullet_list:
            b.display()
            T=b.move()
            if T:
                self.bullet_list.remove(b)
    def move_up(self):
        self.y-=5
        if self.y<=0:
            self.y=0
    def move_down(self):
        self.y+=5
        if self.y>=690:
            self.y=690
    def move_left(self):
        '''左移动飞机'''
        self.x-=5
        if self.x<=0:
            self.x=0
    def move_right(self):
        self.x+=5
        if self.x>=406:
            self.x=406
    def fire(self):
        self.bullet_list.append(Bullet(self.screen,self))
class Bullet:
    def __init__(self,screen,myplane):
        self.screen=screen
        self.x1,self.y1=myplane.x+25,myplane.y
        self.x2,self.y2=myplane.x+75,myplane.y
        self.image=pygame.image.load('./images/pd.png')
    def display(self):
        self.screen.blit(self.image,(self.x1,self.y1))
        self.screen.blit(self.image,(self.x2,self.y2))
    def move(self):
        self.y1-=10
        self.y2-=10
        if self.y1<=0 or self.y2<=0:
            return True
class Enemyplane:
    def __init__(self,screen):
        self.screen=screen
        self.x,self.y=random.randrange(408),-79
        self.image=pygame.image.load('./images/e'+str(random.randrange(3))+'.png')
    def display(self):
        self.screen.blit(self.image,(self.x,self.y))
    def move(self,myplane,enemybullet_list):
        self.y+=3
        if self.y%64==0:
           enemybullet_list.append(Enemybullet(self.screen,self))
        if self.y>=800:
            return True,-1
        #自機が発射した全ての弾に対して当たり判定を行う
        for b in myplane.bullet_list:
            if (self.x<=b.x1 and self.x+100>=b.x1 and self.y+30<=b.y1 and self.y+80>=b.y1) or \
                (self.x <= b.x2 and self.x + 100 >= b.x2 and self.y + 30 <= b.y2 and self.y + 80 >= b.y2):
                myplane.bullet_list.remove(b)
                return True,self.x,self.y
        if (myplane.x>=self.x and myplane.x+100<=self.x+110) and myplane.y<=self.y+35  :
            return True,-2
        return (False,)

class Enemybullet:
    def __init__(self,screen,enemy):
            self.screen=screen
            self.x,self.y=enemy.x+50,enemy.y+80
            self.image=pygame.image.load('./images/pd.png')
    def display(self):
            self.screen.blit(self.image,(self.x,self.y))
    def move(self,myplane):
        self.y+=4
        if self.y>=800:
            return True,-1
        if self.x>=myplane.x+30 and self.x<=myplane.x+100 and self.y>=myplane.y+20 and self.y<=myplane.y+80:
            return True,self.x,self.y
        return (False,)
def key_control(myplane):
    ''''''
    #終了
    for event in pygame.event.get():
        if event.type == QUIT:
            print("exit()")
            exit()
    #キーボード情報取得
    pressed_keys=pygame.key.get_pressed()
    if pressed_keys[K_LEFT] or pressed_keys[K_a]:
        #print('Left')
        if myplane==None:
            return 0
        myplane.move_left()
    elif pressed_keys[K_RIGHT] or pressed_keys[K_d]:
        #print('Right')
        if myplane==None:
            return 0
        myplane.move_right()
    if pressed_keys[K_UP] or pressed_keys[K_w]:
        #print('Up')
        if myplane==None:
            return 0
        myplane.move_up()
    elif pressed_keys[K_DOWN] or pressed_keys[K_s]:
        #print('Down')
        if myplane==None:
            return 0
        myplane.move_down()
    if pressed_keys[K_SPACE]:
        #print('Space')
        if myplane==None:
            return -1
        myplane.fire()
        print(len(myplane.bullet_list))
def bomb(screen,bomb1,bomb2,bomb3,T):
    for i in range(30):
        screen.blit(bomb1, (T[1]-20, T[2]))
    for i in range(30):
        screen.blit(bomb2, (T[1]-20, T[2]))
    for i in range(30):
        screen.blit(bomb3, (T[1]-20, T[2]))
    #做判断 并执行对象的操作
def main():
    #game window
    screen=pygame.display.set_mode((512,766),0,0)
    print(screen)
    #game background
    background = pygame.image.load('./images/bg2.jpg')
    #bomb
    bomb1=pygame.image.load('./images/b3.jpg')
    bomb2 = pygame.image.load('./images/b4.jpg')
    bomb3 = pygame.image.load('./images/b2.jpg')
    gameover=pygame.image.load('./images/game_over.png')
    restart2=pygame.image.load('./images/restart2.png')
    end = False
    m=-770
    while True:
        screen.blit(background, (0, m))
        m += 2
        if m >= 0: m = -770
        #自機
        myplane=myPlane(screen)
        #敵機リスト
        enemy_list=[]
        #敵機の弾リスト
        enemybullet_list=[]
        if end==False:
            while True:
                #背景画面
                screen.blit(background,(0,m))
                m+=2
                if m>=0: m=-770
                #自機を描く
                myplane.display()
                #敵機を描き、弾を発射
                if random.randrange(200)==7:
                    E=Enemyplane(screen)
                    enemy_list.append(E)
                    enemybullet_list.append(Enemybullet(screen, E))
                for e in enemy_list:
                    e.display()
                    T=e.move(myplane,enemybullet_list)
                    if T[0] and T[1]>0:
                        enemy_list.remove(e)
                        bomb(screen,bomb1,bomb2,bomb3,T)            #敵機が撃たれたら　　
                    elif T[0] and T[1]==-1: enemy_list.remove(e)    #敵機が通り過ぎたら
                    elif T[0] and T[1]==-2: end=True                #自機と敵機撃がぶつかったら
                for b in enemybullet_list:
                    b.display()
                    T=b.move(myplane)
                    if T[0] and T[1]==-1: enemybullet_list.remove(b)#敵機の弾が通り過ぎたら
                    elif T[0] and T[1]!=-1:                         #自機が撃たれたら
                        enemybullet_list.remove(b)
                        del myplane
                        bomb(screen, bomb1, bomb2, bomb3, T)
                        end=True
                        break
                if end==True:
                    break
                #方向キーの情報を取得
                key_control(myplane)
                #画面更新
                pygame.display.update()
                #定時更新
                time.sleep(0.01)
                # 敵機に撃たれたらゲームオーバー

        screen.blit(gameover, (0, 70))
        screen.blit(restart2, (180, 350))
        T = key_control(None)
        if T == -1:
            end=False
        else:pass
        pygame.display.update()
        # 定時更新
        time.sleep(0.05)
if __name__ == '__main__':
    main()
