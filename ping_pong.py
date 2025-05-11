from pygame import *
from random import randint
from time import time as timer

font.init()
font1 = font.Font(None, 35)
lose1 = font1.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = font1.render('PLAYER 2 LOSE!', True, (180, 0, 0))
speed_x = 3
speed_y = 3

font2 = font.SysFont('Arial', 36)

img_back = "sky.jpeg"
img_hero1 = "racket.png"
img_hero2 = "racket.png"
ball_img = "tenis_ball.png"

class GameSprite(sprite.Sprite):
 #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
 
 
        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
 
        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#класс главного игрока
class Player(GameSprite):
    #метод для управления спрайтом стрелками клавиатуры
    def update1(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_width - 80:
            self.rect.y += self.speed
    def update2(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_width - 80:
            self.rect.y += self.speed
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)


#класс спрайта-врага  
class Enemy(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезает, если дойдёт до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

#создаём окошко
win_width = 700
win_height = 500
display.set_caption("ping-pong")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

#создаём спрайты
racket1 = Player(img_hero1, 5, 250, 20, 150, 10)
racket2 = Player(img_hero2, 680, 250, 20, 150, 10)
ball = Enemy(ball_img, 250, 350, 80, 80, 100)
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
clock = time.Clock()
start = timer()


while run:
    #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        #событие нажатия на пробел - спрайт стреляет

            
 #сама игра: действия спрайтов, проверка правил игры, перерисовка
    if not finish:
        #обновляем фон
        window.blit(background,(0,0))
        
        #производим движения спрайтов
        racket2.update1()
        racket1.update2()
        ball.rect.x += speed_x
        ball.rect.y += speed_y
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
            #обновляем их в новом местоположении при каждой итерации цикла
        racket1.reset()    
        racket2.reset()
        ball.reset()
         

 
 
            
            
        #возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
  
        if ball.rect.x < 0:
            finish = True
            window.blit(lose1, (200, 200))
        if ball.rect.x > 700:
            finish = True
            window.blit(lose2, (200, 200))
        #проверка выигрыша: сколько очков набрали?
 
 
        clock.tick(40)
        display.update()
