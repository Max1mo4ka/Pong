from pygame import *
import random
import os

'''Необходимые классы'''
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, wight, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (wight, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class AIPaddle(GameSprite):
    def update(self):
        if self.rect.centery < ball.rect.centery and self.rect.y < win_height - 150:
            self.rect.y += self.speed
        if self.rect.centery > ball.rect.centery and self.rect.y > 5:
            self.rect.y -= self.speed

# Инициализация
init()
back = (200, 255, 255)  # Возвращаем цветной фон
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))

# Музыка
music_files = [
    'candyland.ogg',
    'theonlythingtheyfearisyou.ogg',
    'stereomadness.ogg',
    'unholyinsurgency.ogg',
    'finale.ogg'
]

mixer.init()
mixer.music.set_endevent(USEREVENT + 1)
current_music = random.choice(music_files)
mixer.music.load(current_music)
mixer.music.play()

# Объекты
racket1 = Player('racket.png', 30, 200, 4, 50, 150)
racket2 = AIPaddle('racket.png', 520, 200, 3, 50, 150)
ball = GameSprite('tenis_ball.png', 200, 200, 4, 50, 50)

# Текст
font.init()
font = font.Font(None, 35)
lose1 = font.render('ИГРОК ПРОИГРАЛ!', True, (180, 0, 0))
lose2 = font.render('ИИ ПРОИГРАЛ!', True, (180, 0, 0))

speed_x = 3
speed_y = 3
game = True
finish = False
clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and finish:
            if e.key == K_r:
                finish = False
                ball.rect.x = 200
                ball.rect.y = 200
                speed_x = 3
                speed_y = 3
        if e.type == USEREVENT + 1:
            current_music = random.choice(music_files)
            mixer.music.load(current_music)
            mixer.music.play()

    if not finish:
        window.fill(back)  # Заливка цветом вместо фонового изображения
        
        racket1.update_r()
        racket2.update()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1.1
            speed_y *= random.uniform(0.9, 1.1)

        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1

        if ball.rect.x < 0:
            finish = True
            window.blit(lose1, (200, 200))

        if ball.rect.x > win_width:
            finish = True
            window.blit(lose2, (200, 200))

        racket1.reset()
        racket2.reset()
        ball.reset()

    display.update()
    clock.tick(FPS)
