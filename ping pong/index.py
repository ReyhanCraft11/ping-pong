from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
win = font1.render('YOU WON!', True, (255, 255, 255))
lose = font2.render('GAME OVER!', True, (180, 0, 0))

img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_asteroid = "asteroid.png"

score = 0
miss = 0
max_miss = 3
goal = 100
HP = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class Player(GameSprite):
    def update(self):
        keys =  key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global miss
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            miss = miss + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

game = True
finish = False
clock = time.Clock()
FPS = 60

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 5):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_asteroid, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

finish = False
run = True

rel_time = False
num_fire = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 45 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 45 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0,0))
        
        text = font1.render("Score: " + str(score), 1, (255,255,255))
        window.blit(text, (10, 0))

        text_miss = font1.render("Missed: " + str (miss), 1, (255, 255, 255))
        window.blit(text_miss, (10, 50))
        
        HP_color = (255, 80, 80)
        text_HP = font1.render("HP: " + str(HP), 1, (HP_color))
        window.blit(text_HP, (550, 10))

        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Reloading', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True) or sprite.groupcollide(asteroids, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            HP = HP - 1

        # if sprite.spritecollide(ship, monsters, False) or miss >= max_miss:
        #     finish = True
        #     window.blit(lose, (200, 200))

        # if sprite.spritecollide(ship, asteroids):
        #     finish = True
        #     window.blit(lose, (200, 200))

        if HP == 0 or miss >= max_miss:
            finish = True
            window.blit(lose, (200, 200))
        
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        # if HP == 3:
        #     HP_color = (0, 150, 0)
        # if HP == 2:
        #     HP_color = (150, 150, 0)
        # if HP == 1:
        #     HP_color = (150, 0, 0)

        display.update()

    else:
        finish = False
        score = 0
        miss = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

    time.delay(50)
    
    

