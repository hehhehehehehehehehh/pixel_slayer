import pygame
import random

pygame.init()

#화면 크기 설정
screen_width = 700
screen_height = 700

screen = pygame.display.set_mode((screen_width,screen_height))

clock = pygame.time.Clock()
FPS = 60

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

class Player:
    def __init__(self):
        self.rect = pygame.Rect(screen_width/2-30,screen_height/2-30,30,30)
        self.speed = 10
        self.lives = 3
        self.attack_range = pygame.Rect(self.rect.x - 30, self.rect.y-30,100,100)
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = 0
        self.attack_cooldown_base = 3 * FPS
        self.attack_cooldown_max = self.attack_cooldown_base
        self.haste_time = 0
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
        self.attack_range.topleft = (self.rect.x -30, self.rect.y - 30)
        
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
             
    def draw(self):
        pygame.draw.rect(screen,(0,255,255),self.rect)
        if self.attacking:
            pygame.draw.rect(screen,(255,100,100),self.attack_range,2)
        else:
            pygame.draw.rect(screen,(255,255,255),self.attack_range,1)
        for n in range(self.lives):
            pygame.draw.rect(screen,(255,0,0),(30+30*n,30,20,20))
        
        
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
        pygame.draw.rect(screen,(255,0,0),self.rect)
        
class Heal:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,20,20)
        self.duration = 10 * FPS
        
    def update(self):
        self.duration -= 1

    def is_expired(self):
        return self.duration <= 0 

    def draw(self):
        pygame.draw.rect(screen,(50, 255, 0),self.rect)

class Haste:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,20,20)
        self.duration = 5 * FPS

    def update(self):
        self.duration -= 1

    def is_expired(self):
        return self.duration <= 0
    
    def draw(self):
        pygame.draw.rect(screen,(255, 255, 255),self.rect)
        
def main():
    running = True
    player = Player()
    enemies = [Enemy() for i in range(6)]
    heals = []
    hastes = []
    
    enemy_spawn_timer = 0
    enemy_spawn_interval = 100
    
    while running:
        clock.tick(FPS)
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False       
        keys = pygame.key.get_pressed()
        player.move(keys)
        if keys[pygame.K_SPACE]:
            killed = player.attack(enemies)
            for e in killed:
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
                player.lives -=1
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
        
        player.update()
        player.draw()
        
        for e in enemies:
            e.draw()
        for h in heals:
            h.draw()
        for hs in hastes:
            hs.draw()

        
        if player.lives <= 0:
            print("Game Over")
            pygame.time.delay(2000)
            running = False
            
        pygame.display.update()
        
    pygame.quit()
    
if __name__ == "__main__":
    main()