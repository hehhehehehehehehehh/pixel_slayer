import pygame
import random

pygame.init()

#화면 크기 설정
screen_width = 700
screen_height = 700

screen = pygame.display.set_mode((screen_width,screen_height))

clock = pygame.time.Clock()
pygame.mixer.music.load("assets/usagi_rap.mp3")
pygame.mixer.music.play(-1)
paused = False

player = pygame.image.load("assets/player.png").convert_alpha()
heal_image = pygame.image.load("assets/heal.png").convert_alpha()
haste_image = pygame.image.load("assets/haste.png").convert_alpha()
shield_image = pygame.image.load("assets/shield.png").convert_alpha()
usagi_image = pygame.image.load("assets/red_usagi.png").convert_alpha()

player = pygame.transform.scale(player, (50, 50))
heal_image = pygame.transform.scale(heal_image, (50, 50))
haste_image = pygame.transform.scale(haste_image, (50, 50))
shield_image = pygame.transform.scale(shield_image, (50, 50))
usagi_image = pygame.transform.scale(usagi_image, (50, 50))

FPS = 60

BAR_X = 30
BAR_Y = 60
BAR_WIDTH = 200
BAR_HEIGHT = 15
BAFF_BAR_WIDTH = 120
BUFF_BAR_HEIGHT = 10
BAR_GAP = 8
HEAL_DROP_RATE = 0.3
HEAL_DURATION = 10 * FPS
HEAL_SIZE = 20
HEAL_COLOR = (50, 255, 50)
MAX_HEALS = 3
MAX_LIVES = 5
HASTE_DROP_RATE = 0.2
HASTE_DURATION = 5 * FPS
HASTE_SIZE = 20
HASTE_COLOR = (255, 255, 255)
MAX_HASTE = 3
SHIELD_DROP_RATE = 0.1 
SHIELD_DURATION = 10 * FPS 
SHIELD_SIZE = 15 
SHIELD_COLOR = (255,255,0)

SCORE_PER_KILL = 10
score_font = pygame.font.SysFont(None, 30)
def draw_bar(x, y, width, height, ratio, color):
    if ratio < 0:
        ratio = 0
    elif ratio > 1:
        ratio = 1
    pygame.draw.rect(screen, (60, 60, 60), (x, y, width, height))
    pygame.draw.rect(screen, color,(x,y,width*ratio, height))
    pygame.draw.rect(screen, (255,255,255), (x,y,width, height), 2)
class Player:
    def __init__(self):
        # self.rect = pygame.rect(screen_width/2-30,screen_height/2-30,30,30)
        self.rect = player.get_rect(center = (screen_width / 2, screen_height / 2))
        self.speed = 10
        self.lives = 3
        self.attack_range = pygame.Rect(self.rect.x - 100, self.rect.y- 100, 150,150)
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = 0
        self.attack_cooldown_base = 3 * FPS
        self.attack_cooldown_max = self.attack_cooldown_base
        self.haste_time = 0
        self.shield_duration = 0
        self.using_shield = False

    def move(self,keys):
        if keys[pygame.K_LEFT]:
            if self.rect.x > self.speed:
                self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            if self.rect.x < screen_width - self.speed - self.rect.width:
                self.rect.x += self.speed
        if keys[pygame.K_UP]:
            if self.rect.y > self.speed:
                self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            if self.rect.y < screen_height - self.speed - self.rect.height:
                self.rect.y += self.speed
        self.attack_range.topleft = (self.rect.x -25, self.rect.y - 25)
        
    def attack(self,enemies):
        killed = []
        if not self.attacking and self.attack_cooldown <= 0:
            self.attacking = True
            self.attack_timer = 15
            self.attack_cooldown = self.attack_cooldown_max
            new_enemies = []
            for e in enemies:
                if self.attack_range.colliderect(e.rect):
                    killed.append(e)
                else:
                    new_enemies.append(e)
            enemies[:] = new_enemies
        return killed

    def heal(self):
        self.lives = min(self.lives + 1, MAX_LIVES)

    def shield(self):
        self.shield_duration = 300
        self.using_shield = True

    def haste(self):
        self.haste_time = 10 * FPS
        self.attack_cooldown_max = self.attack_cooldown_base * 1/3

    def update(self):
        if self.attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.haste_time > 0:
            self.haste_time -= 1
            if self.haste_time == 0:
                self.attack_cooldown_max = self.attack_cooldown_base
        if self.using_shield:
            self.shield_duration -= 1
            if self.shield_duration <= 0:
                    self.using_shield = False 
                
             
    def draw(self):
        # if self.using_shield:
        #     pygame.draw.rect(screen,SHIELD_COLOR,self.rect)
        # else:
        #     pygame.draw.rect(screen,(0,255,255),self.rect)    
        screen.blit(player, self.rect)
        if self.attacking:
            pygame.draw.rect(screen,(255,100,100),self.attack_range,2)
        else:
            pygame.draw.rect(screen,(255,255,255),self.attack_range,1)
        for n in range(self.lives):
            pygame.draw.rect(screen,(255,0,0),(30+30*n,30,20,20))

    def draw_hud(self):
        for n in range(self.lives):
            pygame.draw.rect(screen, (255,0,0), (30+30*n,30,20,20))
        if self.attack_cooldown <= 0:
            color = (0,255,0)
        elif self.haste_time > 0:
            color = (255,255,0)
        else:
            color = (255, 150, 0)
        ratio = 1 - self.attack_cooldown / self.attack_cooldown_max
        draw_bar(BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT, ratio,color)

        # y = BAR_Y + BAR_HEIGHT + 
        
        
class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0,screen_width-30),random.randint(0,screen_height-30),30,30)
        self.speed = 1
    def move_towards(self,target):
        if self.rect.x < target.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > target.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < target.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > target.rect.y:
            self.rect.y -= self.speed
    def draw(self):
        screen.blit(usagi_image, self.rect)
        
class Heal:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,20,20)
        self.duration = 10 * FPS
        
    def update(self):
        self.duration -= 1

    def is_expired(self):
        return self.duration <= 0 

    def draw(self):
        screen.blit(heal_image, self.rect)

class Haste:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,20,20)
        self.duration = 5 * FPS

    def update(self):
        self.duration -= 1

    def is_expired(self):
        return self.duration <= 0
    
    def draw(self):
        screen.blit(haste_image, self.rect)

class Shield:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,15,15)
        self.duration = 10 * FPS
    
    def update(self):
        self.duration -= 1
        
    def is_expired(self):
        return self.duration <= 0
    
    def draw(self):
        screen.blit(shield_image, self.rect)
def draw_score(score):
    text = score_font.render("SCORE : " + str(int(score)), True, (255,255,255))
    screen.blit(text, (screen_width - text.get_width() - 30, 30))

def main():
    running = True
    player = Player()
    enemies = [Enemy() for i in range(6)]
    heals = []
    hastes = []
    shields = []
    score = 0
    
    enemy_spawn_timer = 0
    enemy_spawn_interval = 70
    
    while running:
        score += 1/60
        clock.tick(FPS)
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False       
        keys = pygame.key.get_pressed()
        player.move(keys)
        if keys[pygame.K_SPACE]:
            killed = player.attack(enemies)
            score += len(killed) * SCORE_PER_KILL
            for e in killed:
                if random.random() < SHIELD_DROP_RATE:
                    shields.append(Shield(e.rect.centerx - SHIELD_SIZE//2,
                                          e.rect.centery - SHIELD_SIZE//2))
                if random.random() < HASTE_DROP_RATE:
                    hastes.append(Haste(e.rect.centerx - HASTE_SIZE // 2,
                                       e.rect.centery - HEAL_SIZE // 2))
                elif random.random() < HEAL_DROP_RATE:
                    heals.append(Heal(e.rect.centerx - HEAL_SIZE // 2, 
                                        e.rect.centery - HEAL_SIZE // 2))

        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_interval:
            enemies.append(Enemy())
            enemy_spawn_timer = 0
            
        for i in enemies:
            i.move_towards(player)
        for enemy in enemies[:]:
            if player.rect.colliderect(enemy.rect):
                if player.shield_duration <= 0:
                    player.lives -= 1
                    enemies.remove(enemy)

        for h in heals[:]:
            h.update()
            if h.is_expired():
                heals.remove(h)
            elif player.rect.colliderect(h.rect):
                player.heal()
                heals.remove(h)
        for hs in hastes[:]:
            hs.update()
            if hs.is_expired():
                hastes.remove(hs)
            elif player.rect.colliderect(hs.rect):
                player.haste()
                hastes.remove(hs)

        for s in shields[:]:
            s.update()
            if s.is_expired():
                shields.remove(s)
            elif player.rect.colliderect(s.rect):
                player.shield()
                shields.remove(s)
        
        player.update()
        player.draw()
        player.draw_hud()
        
        for e in enemies:
            e.draw()
        for h in heals:
            h.draw()
        for hs in hastes:
            hs.draw()
        for shield in shields:
            shield.draw()
        draw_score(score)

        
        if player.lives <= 0:
            print("Game Over")
            pygame.time.delay(2000)
            running = False
            
        pygame.display.update()
        
    pygame.quit()
    
if __name__ == "__main__":
    main()