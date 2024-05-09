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


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

#### 检测 Rectangle 碰撞 ####


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
        self.hitbox = (self.x, self.y, self.width, self.height)    # 碰撞衫
        self.hitboxBorder = 5
    def move_OK(self):
       '''
        先不管拉!爱去哪去哪里！！
       '''
    def update(self):
        '''
        更新对象画面
        '''
        self.hitbox = (self.x, self.y, self.width, self.height) # 同步碰撞杉
        pygame.draw.rect(screen, pygame.Color("Red"), (self.x, self.y, self.width, self.height))    # 绘制碰撞杉
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
    def __init__(self, x: int, y: int, width: int, height: int, color: (int, int, int)):
        self.max_hp = 100
        self.hp = 100
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp_bar_width = self.width
        self.hp_bar_height = self.height // 5
        self.x_vel = randint(Speed.slow, Speed.fast)
        self.y_vel = Speed.slow
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.hitboxBorder = 10
        self.bar_gap = 10
        self.bar_backcolor = Color("Red")
        self.hp_bar_border = 2
        self.hp_back_bar = (self.x, self.y - self.hp_bar_height, self.hp_bar_width, self.hp_bar_height)
        self.hp_front_bar = ((self.x, self.y - self.hp_bar_height, self.hp_bar_width * (self.hp / self.max_hp), self.hp_bar_height))
        self.hp_front_color = Color("Green")

    def rand_move(self):
        if self.x > WIDTH or self.x < 0:
            self.x_vel *= -1
        if self.y < 0 or self.y > HEIGHT:
            self.y_vel *= -1

        self.y += self.y_vel
        self.x += self.x_vel
    def update(self):
        self.rand_move()
        #### ----------------------------------------------------------------------------------------- #### 更新盒子位置
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.hp_back_bar = (self.x, self.y - self.hp_bar_height, self.hp_bar_width, self.hp_bar_height)
        self.hp_front_bar = (
        (self.x, self.y - self.hp_bar_height, self.hp_bar_width * (self.hp / self.max_hp), self.hp_bar_height))
        #### ----------------------------------------------------------------------------------------- ####
        pygame.draw.rect(screen, self.color, self.hitbox) # 碰撞箱
        pygame.draw.rect(screen, self.bar_backcolor, self.hp_back_bar)   # 绘制雪条背景
        pygame.draw.rect(screen, self.hp_front_color, self.hp_front_bar)    # 绘制雪条
        #### ----------------------------------------------------------------------------------------- #### 更新画布绘制

class EnemyList(object):
    def __init__(self):
        self.list = []
        for i in range(5):
            rand_color = (randint(1, 255), randint(1, 255), randint(1, 255))
            self.list.append(Enemy(WIDTH // 2, 0, player.width, player.height, rand_color))
    def __iter__(self):
        for enemy in self.list:
            yield enemy
        return
    def add_randColor(self):
        self.list.append(Enemy(WIDTH // 2, 0, player.width, player.height, (randint(1, 255), randint(1, 255), randint(1, 255))))
    def kill_enemy(self, enemy):
        self.list.pop(self.list.index((enemy)))
    def update(self):
        for enemy in self.list:
            enemy.update()

#### 抛射物 ####
class Bullet(object):
    '''
    x, y, r, color
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 50
        self.color = Color("green")
        self.color = Color("green")
        self.vel = randint(Speed.fast * 2, Speed.fast * 4)
        self.hitbox = (self.x, self.y, self.width, self.height)
    def update(self):
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, Color("White"), self.hitbox, 6)

class BulletList(object):
    '''
    从前有个类，美名其月“弹夹(BulletList)”
    '''
    SIZE = 5
    def __init__(self):
        self.list = []
        self.damage = 10
    def __iter__(self):
        for bullet in self.list:
            yield bullet
        return
    def kill_bullet(self, bullet):
        self.list.pop(self.list.index(bullet))
    def appand(self, player):
        if len(self.list) <= BulletList.SIZE:
            self.list.append(Bullet(player.x, player.y))  # 添加弹丸

    def move_all(self):
        for bullet in self.list:
            if bullet.x >= 0 and bullet.x <= WIDTH and bullet.y >= 0 and bullet.y <= HEIGHT:
                bullet.y -= bullet.vel
            else:
                self.list.pop(self.list.index(bullet))  # 子弹出界清除机制

    def update(self, enemylist):
        #### 检查子弹和敌人的碰撞 ####
        for bullet in self:
            for enemy in enemylist:
                if CollisionController.RectCollide(enemy.hitbox, bullet.hitbox):
                    enemy.hp -= self.damage
                    self.kill_bullet(bullet)
                    if enemy.hp <= 0:
                        enemylist.kill_enemy(enemy) # 删除敌人
                    break
        #### ----------------- ####

        #### ----------------- #### 更新画面中所有子弹s
        for bullet in bulletlist:
            bullet.update()
        #### ----------------- ####


class CollisionController():
    def RectCollide(hitbox1, hitbox2):
        '''
        检测四个点是否在另一个矩形体内即可
        box1 = (x, y, width, height)
                0  1   2     3
        :param hitbox1:
        :param hitbox2:
        :return:
        '''
        p1 = Point(hitbox1[0], hitbox1[1])
        p2 = Point(hitbox1[0] + hitbox1[2], hitbox1[1])
        p3 = Point(hitbox1[0], hitbox1[1] + hitbox1[3])
        p4 = Point(hitbox1[0] + hitbox1[2], hitbox1[1] + hitbox1[3])
        points = [p1, p2, p3, p4]
        for p in points:
            if p.x >= hitbox2[0] and p.x <= hitbox2[0] + hitbox2[2] and p.y >= hitbox2[1] and p.y <= hitbox2[1] + hitbox2[3]:
                return True
        return False

#### 创建游戏对象 ####
player = Player()       # 玩家
bulletlist = BulletList()   # 弹夹
enemylist = EnemyList() # 小怪列表
collision_controller = CollisionController()    # 碰撞控制器
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
            bulletlist.appand(player) # 装弹
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
        bulletlist.update(enemylist)
        player.update()
        enemylist.update()
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