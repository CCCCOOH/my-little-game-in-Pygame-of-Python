import sys
import pygame
from random import randint

pygame.init()
#### Global Values ####
running = True
FPS = 60
WIDTH, HEIGHT = 1000, 1600
#### ------------- ####
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("怀念高中第一次学习Pygame的那个暑假。")
clock = pygame.time.Clock()

class Color(pygame.Color):
    lbl = (102, 178, 255)
    red = pygame.Color("Red")
class Speed:
    normal = 10
    fast = 15
    slow = 5

#### 玩家对象 ####
class Player(object):
    def __init__(self):
        '''
        对象属性
        '''
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.width = 40
        self.height = 60
        self.vel = Speed.normal     # How fast our gameobject move.
        self.hitbox = (self.x )
    def move_OK(self):
       '''
        先不管拉!爱去哪去哪里！！
       '''
    def update(self):
        '''
        更新对象画面
        '''
        pygame.draw.rect(screen, pygame.Color("Red"), (self.x, self.y, self.width, self.height))
    def left(self):
        self.x -= self.vel
    def right(self):
        self.x += self.vel
    def up(self):
        self.y -= self.vel
    def down(self):
        self.y += self.vel

class Enemy(object):
    '''
    x, y, width, height, end
    '''
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = randint(Speed.slow, Speed.fast)
    def rand_move(self):
        if self.x > WIDTH or self.x < 0:
            self.vel *= -1
        self.x += self.vel
    def update(self):
        self.rand_move()
        pygame.draw.rect(screen, Color("Green"), (self.x, self.y, self.width, self.height))
# NVIDIA

#### 抛射物 ####
class Bullet(object):
    '''
    x, y, r, color
    '''
    def __init__(self, x: int, y: int, radius: int, color: (int, int, int)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = randint(Speed.normal, Speed.fast)
    def update(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class BulletList(object):
    '''
    从前有个类，美名其月“弹夹(BulletList)”
    '''
    SIZE = 5
    def __init__(self):
        self.bullets = []
    def reload(self, player):
        if len(self.bullets) <= BulletList.SIZE:
            self.bullets.append(Bullet(player.x + randint(0, player.width), player.y, 15, pygame.Color("YELLOW")))  # 添加弹丸
    def move_all(self):
        for bullet in self.bullets:
            if bullet.x >= 0 and bullet.x <= WIDTH and bullet.y >= 0 and bullet.y <= HEIGHT:
                bullet.y -= bullet.vel
            else:
                self.bullets.pop(self.bullets.index(bullet))  # 删除该子弹
    def update(self):
        for bullet in bulletlist.bullets:
            bullet.update()

#### 创建游戏对象 ####
player = Player()       # 玩家
bulletlist = BulletList()   # 弹夹
enemy = Enemy(WIDTH // 2, 0, player.width, player.height)
#### ---------- ####

if __name__ == "__main__":
    while running:
        # --------------------- # 检测按键输入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # --------------------- #

        # --------------------- # 用户操作按键
        keys = pygame.key.get_pressed()  # get keys
        if keys[pygame.K_LEFT]:
            player.left()
        if keys[pygame.K_RIGHT]:
            player.right()
        if keys[pygame.K_UP]:
            player.up()
        if keys[pygame.K_DOWN]:
            player.down()
            # 子弹发射!
        if keys[pygame.K_SPACE]:
            bulletlist.reload(player) # 装弹
        # --------------------- #

        #--------------------- # 刷新背景
        screen.fill(Color.lbl)
        clock.tick(FPS)
        # --------------------- #

        # ****************************** # 更新游戏对象
        #### 移动子弹 ####
        bulletlist.move_all()
        #### ------ ####

        # --------------------- # 更新对象绘制
        bulletlist.update()
        player.update()
        enemy.update()
        # --------------------- # 更新游戏画面
        pygame.display.flip()
        pygame.display.update()
        # --------------------- #
        # ****************************** #

    #-----------------------# 结束游戏
    pygame.quit()
    sys.exit()
    #-----------------------#

# -----------------------# 写在最后
# @项目借鉴 -- YouTube大佬的教程:[https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/projectiles]
''' # 跳跃模块(本游戏不考虑加入...)
if not(isJusmp):
    if keys[pygame.K_UP]:
        y -= vel
else:
    if jumpCount >= -10:
        neg = 1
        y -= jumpCount ** 2 * 0.5 * neg
        jumpCount -= 1
    else:
        isJump = False
        jumpCount = 10
'''
# Version -- 0.0.0.1
# -----------------------#