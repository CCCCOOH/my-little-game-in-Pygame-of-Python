import sys

import pygame
pygame.init()   # 初始化pygame模块
WIDTH, HEIGHT = 800, 1200   # 窗口宽度，高度
FPS = 60    # 帧率
running = True  # 游戏运行状态
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # 设置窗口,screen为窗口对象
pygame.display.set_caption("怀念高中第一次接触Pygame的那个暑假！") # 设置窗口标题
clock = pygame.time.Clock() # 统一游戏帧率

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Player(object):
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.width = 100
        self.height = 200
        self.hit_box = (self.x, self.y, self.width, self.height)
        self.color = pygame.Color("Blue")   # 颜色
        self.velocity = 10
    def left(self):
        self.x -= self.velocity
    def right(self):
        self.x += self.velocity
    def up(self):
        self.y -= self.velocity
    def down(self):
        self.y += self.velocity
    def update(self):
        self.hit_box = (self.x, self.y, self.width, self.height)    # 更新碰撞箱位置
        pygame.draw.rect(screen, self.color, self.hit_box)  # 更新绘制
class Enemy(Player):
    pass

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
            if (p.x >= hitbox2[0]
                    and p.x <= hitbox2[0] + hitbox2[2]
                    and p.y >= hitbox2[1]
                    and p.y <= hitbox2[1] + hitbox2[3]):
                return True
        return False
    # def obj_collided(self, object1, object2):
    #     if self.RectCollide(object1.hit_box, object2.hit_box):
    #         return True
    #     else:
    #         return False

################### 创建一个方块对象
player = Player()
enemy = Enemy()
###################



if __name__ == "__main__":
    while running:
        screen.fill(pygame.Color("White"))  # 填充一个背景色
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 检测是否点击右上角窗口小x
                running = False
        ############ 获取输入 ##################
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            player.down()
        if keys[pygame.K_UP]:
            player.up()
        if keys[pygame.K_LEFT]:
            player.left()
        if keys[pygame.K_RIGHT]:
            player.right()
        ######################################

        # $$$$$$$$$$$$$$$ 碰撞检测 $$$$$$$$$$$$$$$$$$$
        if CollisionController.RectCollide(player.hit_box, enemy.hit_box):
            print("哎呀，创了一下咧！")
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        # ****************** 更新对象 *******************
        enemy.update()
        player.update()
        # ****************** ------ *******************
        pygame.display.update() # 更新画面

    pygame.quit()
    sys.exit()
    # 退出游戏辣！
