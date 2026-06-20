import pygame
import random

pygame.init()

# 화면 크기 설정
screen_width = 720
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()
FPS = 60

class Player:
    def __init__(self):
        # self.rect.width = self.speed 같게
        self.rect = pygame.Rect(360,360,30,30)
        self.speed = self.rect.width
        self.lives = 3
        self.attack_range = pygame.Rect(self.rect.x - 30, self.rect.y - 30, 100, 100)
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = 0

    def move(self, keys):
        if keys[pygame.K_RIGHT]:
            if self.rect.x <= 720 - self.speed - self.rect.width:
                self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            if self.rect.x >= self.speed:
                self.rect.x -= self.speed
        if keys[pygame.K_UP]: 
            if self.rect.y >= self.speed:
                self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            if self.rect.y <= 720 - self.speed - self.rect.height:
                self.rect.y += self.speed
        self.attack_range.topleft = (self.rect.x - 30, self.rect.y - 30)
    def attack(self, enemies):
        if not self.attacking and self.attack_cooldown <= 0:
            self.attacking = True
            self.attack_timer = 15
            self.attack_cooldown = 300
            new_enemies = []
            for e in enemies:
                if not self.attack_range.colliderect(e.rect):
                    new_enemies.append(e)
            enemies[:] = new_enemies

    def update(self):
        if self.attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1        

    def draw(self):
        pygame.draw.rect(screen,(255,255,255), self.rect)
        if self.attacking:
            pygame.draw.rect(screen, (0,255,0), self.attack_range, 2)
        else:
            pygame.draw.rect(screen, (0,0,0), self.attack_range, 1)
        for i in range(self.lives):
            pygame.draw.rect(screen, (0, 255, 0), (10 + i * 12, 710, 10, 10))

class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, screen_width-30), random.randint(0, screen_height - 30), 30, 30)
        self.speed = 1.5
    def move_towards(self, target):
        if self.rect.x < target.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > target.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < target.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > target.rect.y:
            self.rect.y -= self.speed
    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
def main():
    running = True
    player = Player()
    enemies = [Enemy() for i in range(3)]

    enemy_spawn_timer = 0
    enemy_spawn_interval = 60

    while running:
        clock.tick(FPS)
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        player.move(keys)

        if keys[pygame.K_SPACE]:
            player.attack(enemies)
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_interval:
            enemies.append(Enemy())
            enemy_spawn_timer = 0
        for e in enemies:
            e.move_towards(player)
        for e in enemies[:]:    
            if player.rect.colliderect(e.rect):
                player.lives -= 1
                enemies.remove(e)
        
        player.update()    
        player.draw()

        for e in enemies:
            e.draw()
        if player.lives <= 0:
            print("Game Over")
            pygame.time.delay(2000)
            running = False
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()