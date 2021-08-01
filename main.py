# pygame
# sprite - 飛船
# sprite - 石頭
# sprite - 子彈
# 碰撞處理 (group,sprite)

import pygame
import random

FSP = 60   
WHITE = (255,255,255) 
GREEN =(0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)

WIDTE = 500
HIGHT = 600

PYGAME_NAME = "太空遊戲！"


# 遊戲初始化 ＆ 創建視窗
pygame.init()
screen = pygame.display.set_mode((WIDTE,HIGHT))
pygame.display.set_caption(PYGAME_NAME)
clock = pygame.time.Clock() # 創建設定一秒幾次的物件

# 創建遊戲角色類別
class Player (pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTE/2
        self.rect.bottom = HIGHT-10
        self.spacex = 8

    def update (self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT] :
            self.rect.x += self.spacex
        if key_pressed[pygame.K_LEFT] :
            self.rect.x -= self.spacex
            
        if self.rect.right > WIDTE :
            self.rect.right = WIDTE
        if self.rect.left < 0 :
            self.rect.left = 0 

    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Rock (pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange (0,WIDTE-self.rect.width)
        self.rect.y = random.randrange (-100,-40)
        self.spacey = random.randrange (2,10)
        self.spacex = random.randrange (-3,3)

    def update (self):
        self.rect.y += self.spacey
        self.rect.x += self.spacex
        if self.rect.top > HIGHT or self.rect.left > WIDTE or self.rect.right < 0 : 
            self.rect.x = random.randrange (0,WIDTE-self.rect.width)
            self.rect.y = random.randrange (-100,-40)
            self.spacey = random.randrange (2,10)
            self.spacex = random.randrange (-3,3)
 
class Bullet (pygame.sprite.Sprite) :
    def __init__(self,x,y) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.spacey = -10
 
    def update (self):
        self.rect.y += self.spacey
        if self.rect.bottom < 0 :
            self.kill()
        
# 設定角色群組 
all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player) # 把player 加入群組中

# 創建石頭
for i in range(8):
    r =Rock()
    all_sprites.add(r)
    rocks.add(r)

running = True
# 遊戲迴圈 (視窗有效中) 
while running :

    # 使用pygame 物件 設定一秒只能跑幾次
    clock.tick(FSP) 

    # 取得輸入
    for event in pygame.event.get():
        if event.type ==  pygame.QUIT :
            running = False
        elif event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE :
                player.shoot()
        

    # 更新遊戲資料
    all_sprites.update()

    hits = pygame.sprite.groupcollide(rocks,bullets,True,True) # 是否有碰撞
    for hit in hits :
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)

    hits = pygame.sprite.spritecollide(player,rocks,False) 
    if hits :
        running = False 

  
    

    # 畫面顯示
    screen.fill(BLACK) #R,G,B調色盤
    all_sprites.draw(screen)
    pygame.display.update()

# 遊戲結束 (視窗關閉)
pygame.quit()