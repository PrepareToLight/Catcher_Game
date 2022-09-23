import pygame as pg
from random import randint
from numpy import ones

FPS = 60
width, height = 900, 600
MARGIN = 100

def vel_vec(n:int, m:int=2) -> list:
    #n - how much Squres do you want to be moving?
    VEL_vector = ones((n,m))
    VEL_arr = list(VEL_vector)
    for i,np_arr in enumerate(VEL_arr):
        VEL_arr[i] = list(np_arr)

    return VEL_arr

vel_vector = vel_vec(10)

def distance(vec_x1:tuple, vec_x2:tuple) -> int:
    return abs(vec_x1[0]-vec_x2[0]) + abs(vec_x1[1]-vec_x2[1])

class Hero:
    def __init__(self, screen) -> None:
        self.body = pg.Rect(width/2, height/2, 10, 50)
        self.screen = screen

    def move(self, position:tuple) -> None:
        self.body.centerx, self.body.centery = position

    def show(self) -> None:
        pg.draw.rect(self.screen, (255,255,255), self.body, 1)

        
class Net(Hero):
    def __init__(self, screen) -> None:
        super().__init__(screen)
        self.stick = pg.Rect(width/2, height/2,50,1)
        self.net = pg.Rect(width/2, height/2,30,30)
        self.directory = "d_right"
        self.catched_num = 0
        self.stick.x, self.stick.y = self.body.centerx, self.body.centery
        self.net.centerx, self.net.centery = self.stick.midright

        self.position_square = pg.Rect(width/2, height/2,100,100)
        self.position_square.centerx, self.position_square.centery = self.body.centerx, self.body.centery        
    def catch_directory(self, keys_pressed):
        if keys_pressed[pg.K_w]:
            self.directory = "w_up"
            x, y = self.position_square.midtop
            self.stick = pg.Rect(x, y, 1, 50)
            self.net.centerx, self.net.centery = self.stick.x, self.stick.y
        if keys_pressed[pg.K_a]:
            self.directory = "a_left"
            x, y = self.position_square.midleft
            self.stick = pg.Rect(x, y, 50, 1)
            self.net.centerx, self.net.centery = self.stick.x, self.stick.y
        if keys_pressed[pg.K_d]:
            self.directory = "d_right"
            self.stick = pg.Rect(self.position_square.centerx, self.position_square.centery, 50, 1)
            self.net.centerx, self.net.centery = self.stick.midright
        if keys_pressed[pg.K_s]:
            self.directory = "s_down"
            self.stick = pg.Rect(self.position_square.centerx, self.position_square.centery, 1, 50)
            self.net.centerx, self.net.centery = self.stick.bottomright
            

    def move(self, position:tuple) -> None:
        self.position_square.centerx, self.position_square.centery = position

        if self.directory == "w_up":
            self.stick.x, self.stick.y = self.position_square.midtop
            self.net.centerx, self.net.centery = self.stick.x, self.stick.y
        if self.directory == "a_left":
            self.stick.x, self.stick.y = self.position_square.midleft
            self.net.centerx, self.net.centery = self.stick.x, self.stick.y
        if self.directory == "d_right":
            self.stick.x, self.stick.y = position
            self.net.centerx, self.net.centery = self.stick.midright
        if self.directory == "s_down":
            self.stick.x, self.stick.y = self.position_square.centerx,self.position_square.centery
            self.net.centerx, self.net.centery = self.stick.bottomright

    def net_catch(self, id:int, square, list_squares:list) -> None:
        dist = distance((self.net.centerx, self.net.centery), (square.body.centerx, square.body.centery))
        if dist < 20 and dist >=0:
            self.catched_num += 1
            print("catched", id)
            square = Squares(self.screen)
            list_squares[id] = square



    def show(self) -> None:
        #pg.draw.rect(self.screen, (0,0,255), self.position_square, 1) #draw object to see the orientation of net
        pg.draw.rect(self.screen, (255,255,255), self.stick, 1)
        pg.draw.rect(self.screen, (255,255,0), self.net, 1)

class Squares:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        x, y = self.generate()
        print(x,y)
        self.body = pg.Rect(x, y, 20, 20)


    def generate(self) -> tuple:
        x = randint(0, self.screen_width)
        y = randint(0, self.screen_height)
        choice = randint(0, 3)
        if choice == 0:
            return x, -MARGIN
        if choice == 1:
            return -MARGIN, y
        if choice == 2:
            return x, self.screen_height+MARGIN
        if choice == 3:
            return self.screen_width+MARGIN, y

        return 0, 0

    def move(self, id:int):
        self.body.x += vel_vector[id][0]
        self.body.y += vel_vector[id][1]
        if self.body.x < - MARGIN:
            vel_vector[id][0] *= -1
            #print(self.body.x, self.body.y)
        if self.body.x > self.screen_width + MARGIN:
            vel_vector[id][0] *= -1
            #print(self.body.x, self.body.y)
        if self.body.y < -MARGIN:
            vel_vector[id][1] *= -1
            #print(self.body.x, self.body.y)
        if self.body.y > self.screen_height + MARGIN:
            vel_vector[id][1] *= -1
            #print(self.body.x, self.body.y)  

    def colide_squares(self, id1, id2, square2):
        if distance((self.body.x, self.body.y), (square2.x, square2.y)) < 100:
            vel_vector[id1][0] = vel_vector[id2][0]
            vel_vector[id1][1] = vel_vector[id2][1]

    def __del__(self):
        pass

    def __str__(self) -> str:
        return "Square class"

    def show(self) -> None:
        pg.draw.rect(self.screen, (255,0,0), self.body)
        

