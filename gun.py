import math
from random import choice, randint

import pygame
from pygame.draw import *


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
pygame.font.init()
font_style = pygame.font.Font(None, 50)


WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 20
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 1
        self.time = 0

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
        self.vy -= 5
        if self.x >= (800 - self.r) or self.x <= self.r:
            self.vx *= -1
            self.x += 2 * self.vx
        if self.y >= (600 - self.r) or self.y <= self.r:
            self.vy *= -0.8

        self.time += 1

    def draw(self):
        pygame.draw.circle(self.screen, choice(GAME_COLORS), (self.x, self.y), self.r)

    def hittest(self, obj):
        "условия столкновения снаряда и мишени"
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            return True
        return False

    def hittest1(self, obj):
        "описывает столкновение снаряда со второй пушкой"
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + 20)**2:
            return True
        return False

class Ellipsball:
    def __init__(self, screen: pygame.Surface, x= 40, y = 50,  w = 80, l = 30):
        """ Конструктор класса ellipsball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        w - ширина объекта
        l - длина объекта
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.l = l
        self.r = 20
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 1
        self.time = 0

    def move(self):
        """Переместить снаряд по прошествии единицы времени.

        Метод описывает перемещение за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
        self.w += 10
        self.l += 5
        self.vy -= 5
        if self.x >= (800 - 30) or self.x <= 30:
            self.vx *= -1
            self.x += 2 * self.vx
        if self.y >= (600 - 10) or self.y <= 10:
            self.vy *= -0.8
        if self.w >= 140:
            self.w -= 15
        elif self.w <= 85:
            self.w += 10
        if self.l >= 85:
            self.l -= 10
        elif self.l <= 5:
            self.l += 5

        self.time += 1

    def draw(self):
        "рисует сняряд второго типа"
        pygame.draw.ellipse(self.screen, choice(GAME_COLORS), (self.x, self.y, self.w, self.l))

    def hittest(self, obj):
        "описывает столкновение снаряда и мишени"
        if  self.x - self.w/2 <= obj.x <= self.x + self.w/2 and self.y - self.l/2 <= obj.y <= self.y + self.l/2:
            return True
        return False

    def hittest1(self, obj):
        "описывает столкновение снаряда и пушки"
        if (self.x - 20)**2 + (self.y - 520)**2 <= (30)**2:
            return True
        return False

class Gun:
    "описание объекта класса Gun"
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 30
        self.f2_on = 0
        self.an = 1
        self.color = MAGENTA
        self.life = 90
        self.x = 20
        self.y = 520

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 20


    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-40))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY


    def draw(self):
        x0, y0 = 20, 520
        d = self.f2_power
        x1, y1 = x0 + d*math.cos(self.an), y0+d*math.sin(self.an)
        pygame.draw.line(self.screen, self.color, [x0, y0], [x1, y1], 20)


    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

class Gun2:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 30
        self.f2_on = 0
        self.an = -1
        self.color = MAGENTA
        self.life = 90
        self.x = 30
        self.y = 45

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global ellipsballs, bullet
        bullet += 1
        new_elball = Ellipsball(self.screen)
        new_elball.r += 5
        self.an = math.atan2((event.pos[1] - new_elball.y), (event.pos[0] - new_elball.x))
        new_elball.vx = - self.f2_power * math.cos(self.an)
        new_elball.vy = - self.f2_power * math.sin(self.an)
        ellipsballs.append(new_elball)
        self.f2_on = 0
        self.f2_power = 20


    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event and event.pos[0] != 40:
            self.an = math.atan((event.pos[1] - 50) / (event.pos[0] - 40))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY


    def draw(self):
        x0, y0 = 30, 45
        d = self.f2_power
        x1, y1 = x0 + d*math.cos(self.an), y0+d*math.sin(self.an)
        pygame.draw.line(self.screen, self.color, [x0, y0], [x1, y1], 20)


    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

class Target:
    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.live = 1
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = randint(600, 780)
        y = self.y = randint(300, 550)
        r = self.r = randint(10, 50)
        self.color = choice(GAME_COLORS)
        if r < 20:
            self.vx = randint(-1, 1)
            while self.vx == 0:
                self.vx = randint(-1, 1)
            self.vy = 0
        elif 20 <= r < 35:
            self.vx = randint(-8, 8)
            while self.vx == 0:
                self.vx = randint(-8, 8)
            self.vy = 0
        else:
            self.vx = randint(-10, 10)
            while self.vx == 0:
                self.vx = randint(-10, 10)
            self.vy = randint(-3, 3)
            while self.vy == 0:
                self.vy = randint(-3, 3)


    def hit(self, points = 1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        if self.r < 20:
            pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
            pygame.draw.rect(self.screen, (0, 0, 0), [self.x - 7, self.y + 4, 10, 3], 0)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x - 7, self.y - 2), 2)
            pygame.draw.rect(self.screen, (0, 0, 0), [self.x + 1, self.y - 2, 5, 2], 0)
        elif 20 <= self.r < 35:
            pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
            pygame.draw.rect(self.screen, (0, 0, 0), [self.x - 10, self.y + 5, 20, 5], 0)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x - 10, self.y - 2.5), 2.5)
            pygame.draw.rect(self.screen, (0, 0, 0), [self.x + 1.5, self.y - 2.5, 7.5, 2], 0)
        else:
            pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
            pygame.draw.rect(self.screen, (0, 0, 0), [self.x - 20, self.y + 10, 40, 10], 0)
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x - 20, self.y - 5), 5)
            pygame.draw.rect(self.screen, (0, 0, 0), [self.x + 3, self.y - 5, 15, 4], 0)

    def move(self):
        'Движение целей по экрану'
        x, y, vx, vy = self.x, self.y, self.vx, self.vy
        r = self.r
        x += vx
        y += vy
        if x + r + vx > 801:
            vx *= -1
        if x - r + vx < 0:
            vx *= -1
        if y + r + vy > 601:
            vy *= -1
        if y - r + vy < 0:
            vy *= -1
        self.x, self.y, self.vx, self.vy = x, y, vx, vy

def score_message(msg, color):
    '''Current player rate on the screen'''
    mesg = font_style.render("Score: " + str(msg), True, color)
    screen.blit(mesg, [500, 50])


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
ellipsballs = []

clock = pygame.time.Clock()
gun = Gun(screen)
gun2 = Gun2(screen)
target1 = Target(screen)
target2 = Target(screen)
target3 = Target(screen)
finished = False
count = 0

while not finished:
    screen.fill(WHITE)
    if gun.life > 0:
        gun.draw()
    if gun2.life > 0:
        gun2.draw()
    target1.draw()
    target2.draw()
    target3.draw()
    for ball in balls:
        if ball.live >= 1:
            ball.draw()
    for elball in ellipsballs:
        if elball.live >= 1:
            elball.draw()
    score_message(str(count), MAGENTA)
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] >= 300 and gun.life > 0:
                gun.fire2_start(event)
            if event.pos[1] < 300 and gun2.life > 0:
                gun2.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.pos[1] >= 300 and gun.life > 0:
                gun.fire2_end(event)
            if event.pos[1] < 300 and gun2.life > 0:
                gun2.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            if event.pos[1] >= 300:
                gun.targetting(event)
            else:
                gun2.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target1) and target1.live:
            target1.live = 1
            target1.hit()
            if b in balls:
                balls.remove(b)
            target1.new_target()
            if target1.r < 20:
                count += 5
            elif 20 <= target1.r < 35:
                count += 10
            else:
                count += 15
        if b.hittest(target2) and target2.live:
            target2.live = 1
            target2.hit()
            if b in balls:
                balls.remove(b)
            target2.new_target()
            if target2.r < 20:
                count += 5
            elif 20 <= target2.r < 35:
                count += 10
            else:
                count += 15
        if b.hittest(target3) and target3.live:
            target3.live = 1
            target3.hit()
            if b in balls:
                balls.remove(b)
            target3.new_target()
            if target3.r < 20:
                count += 5
            elif 20 <= target3.r < 35:
                count += 10
            else:
                count += 15
        if b.hittest1(gun2):
            gun2.life -= 5
            if b in balls:
                balls.remove(b)
    for eb in ellipsballs:
        eb.move()
        if eb.hittest(target1) and target1.live:
            target1.live = 1
            target1.hit()
            if eb in ellipsballs:
                ellipsballs.remove(eb)
            target1.new_target()
            if target1.r < 20:
                count += 5
            elif 20 <= target1.r < 35:
                count += 10
            else:
                count += 15
        if eb.hittest(target2) and target2.live:
            target2.live = 1
            target2.hit()
            if eb in ellipsballs:
                ellipsballs.remove(eb)
            target2.new_target()
            if target2.r < 20:
                count += 5
            elif 20 <= target2.r < 35:
                count += 10
            else:
                count += 15
        if eb.hittest(target3) and target3.live:
            target3.live = 1
            target3.hit()
            if eb in ellipsballs:
                ellipsballs.remove(eb)
            target3.new_target()
            if target3.r < 20:
                count += 5
            elif 20 <= target3.r < 35:
                count += 10
            else:
                count += 15
        if eb.hittest1(gun):
            gun.life -= 5
            if eb in ellipsballs:
                ellipsballs.remove(eb)
    target1.move()
    target2.move()
    target3.move()
    gun.power_up()
    gun2.power_up()

pygame.quit()
