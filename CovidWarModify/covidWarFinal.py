import random
import pygame
import os
import sys

#setup
WIDTH = 600
HEIGHT = 800
FPS = 60
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Covid19War")
font = pygame.font.SysFont("robotto", 40, bold=True)
bg = pygame.image.load("bg.png")
bg_offset = bg.get_height()-HEIGHT
pygame.mixer.init()
boom_sound = pygame.mixer.Sound("boom.wav")
shooting_sound = pygame.mixer.Sound("shooting_sound.mp3") 
shooting_sound.set_volume(0.2)
hurt_sound = pygame.mixer.Sound("hurt.mp3")
hurt_sound.set_volume(0.2)
heal_sound = pygame.mixer.Sound("heal.mp3")
heal_sound.set_volume(0.2)
collect_itme_sound = pygame.mixer.Sound("collectItem.mp3")
collect_itme_sound.set_volume(0.2)
tutorial_panel = pygame.image.load("tutorial_panel.png").convert_alpha()
clock = pygame.time.Clock()
running = 1
game_active = True 
game_end = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.playerImages = [pygame.image.load("JiJiSR1.png").convert_alpha(),
                         pygame.image.load("JiJiSR1L.png").convert_alpha(),
                         pygame.image.load("JiJiSR1R.png").convert_alpha()]
        self.image = self.playerImages[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = WIDTH/2, HEIGHT-50
        self.radius = 40
        self.speedx = 0
        self.speedy = 0
        self.lastSpeedx = self.speedx
        self.lastSpeedy = self.speedy
        self.life = 100
        self.score = 0

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.speedx < 0 ) and (self.lastSpeedx != self.speedx):
            #print("left",self.lastSpeedx,self.speedx)
            self.image = self.playerImages[1]
        elif (self.speedx > 0 ) and (self.lastSpeedx != self.speedx):
            #print("right",self.lastSpeedx,self.speedx)
            self.image = self.playerImages[2]
        elif (self.speedx == 0)  and (self.lastSpeedx != self.speedx):
            #print("center",self.lastSpeedx,self.speedx)
            self.image = self.playerImages[0]
        self.lastSpeedx = self.speedx
        self.lastSpeedy = self.speedy
    def shoot(self):
        cure = Cure(self.rect.centerx, self.rect.top)
        allsprites.add(cure)
        cures.add(cure)
        shooting_sound.play() 

class Covid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("covid19.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*.7/2)
        self.reSpawn()
    def reSpawn(self):
        self.rect.x = random.randrange(WIDTH-self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedx = random.randrange(-2,2)
        self.speedy = random.randrange(1,10)
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.x >= WIDTH or self.rect.x < 0:
            self.speedx = -self.speedx
        if self.rect.top > HEIGHT+10:
            self.reSpawn()


class Heal(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("heart.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.reSpawn()
    def reSpawn(self):
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedx = random.randrange(-2,2)
        self.speedy = random.randrange(1,10)
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT+10:
            self.reSpawn()
 

class Trap(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bomb.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.reSpawn()
    def reSpawn(self):
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedx = random.randrange(-2,2)
        self.speedy = random.randrange(1,10)
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT+10:
            self.reSpawn()

class Coin(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("coin.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.reSpawn()
    def reSpawn(self):
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedx = random.randrange(-2,2)
        self.speedy = random.randrange(1,10)
    def update(self): 
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT+10:
            self.reSpawn()
       

class Cure(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("cure.png").convert_alpha()
        self.image_orig = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
    def update(self):
        self.rect.y += self.speedy
        self.rotate()
        if self.rect.bottom < 0:
            self.kill()



    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            #print("rotate")
class Button: 
    def __init__(self, image, pos, word):
        self.image = image
        self.xpos = pos[0]
        self.ypos = pos[1]
        self.word = word
        self.text = font.render(self.word, True, (150, 150, 150))
        self.rect = self.image.get_rect(center=(self.xpos, self.ypos))
        self.text_rect = self.text.get_rect(center=(self.xpos, self.ypos))

    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(font.render(self.word, True, (150, 150, 150)), self.text_rect)

    def check_input(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False


def play():
    running = 1
    game_active = True
    pause = False
    time_cnt = 600
    spawnTrap = False
    spawnTraps = False
    if player.score > 100:
        t = Trap()
        allsprites.add(t)
        traps.add(t)

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a : 
                    player.speedx = -6
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d : 
                    player.speedx = 6
                if event.key == pygame.K_UP or event.key == pygame.K_w : 
                    player.speedy = -6
                if event.key == pygame.K_DOWN or event.key == pygame.K_s : 
                    player.speedy = 6
                if (event.key == pygame.K_SPACE) and (player.life > 0):
                    player.shoot()
                if event.key == pygame.K_ESCAPE and player.life > 0:
                    pause_game()
                    
                if event.key == pygame.K_r and player.life > 0: 
                    game_active = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a or player.rect.bottomright[0] >= 0: 
                    player.speedx = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d or player.rect.bottomright[0] <= WIDTH: 
                    player.speedx = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w or player.rect.bottomright[0] >= 0: 
                    player.speedy = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s or player.rect.bottomright[0] <= WIDTH: 
                    player.speedy = 0
                if (event.key == pygame.K_RETURN) and (player.life <= 0):
                    reset_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and player.life > 0:
                    if player.life > 0:
                        player.shoot()
                  

    #process
        allsprites.update()
        player_hit = pygame.sprite.spritecollide(player,covids,True,pygame.sprite.collide_circle)
        if player_hit and game_active:
            player.life -= 1
            hurt_sound.play()
            
        cures_hits = pygame.sprite.groupcollide(covids, cures,True,True)
        for hit in cures_hits:
            c = Covid()
            allsprites.add(c)
            covids.add(c)
            #player.score += 10

        player_heal = pygame.sprite.spritecollide(player, heals, True, pygame.sprite.collide_rect)
        if player_heal:
            for _ in range(len(player_heal)):  
                h = Heal()
                allsprites.add(h)
                heals.add(h)
            player.life += 1 
            heal_sound.play()
        
        player_collect = pygame.sprite.spritecollide(player, coins, True, pygame.sprite.collide_rect) 
        if player_collect:
            for _ in range(len(player_collect)):  
                coin = Coin()
                allsprites.add(coin)
                coins.add(coin)
            player.score += 10 
            collect_itme_sound.play() 

        if player.score == 90:
            spawnTrap = True

        if spawnTrap and player.score == 100:
            spawn_trap()
            spawnTrap = False
        elif player.score == 200:
            spawn_traps()
            # spawnTraps = False
        player_trapped = pygame.sprite.groupcollide(traps, cures, True, True)
        if player_trapped and game_active: 
            boom_sound.play() 
            player.life = 0
        player_hit_trap = pygame.sprite.spritecollide(player, traps, True, pygame.sprite.collide_rect) 
        if player_hit_trap and game_active:
            boom_sound.play()
            for _ in range(len(player_hit_trap)):  
                t = Trap()
                allsprites.add(t)
                traps.add(t)
            player.life = 0

        if player.rect.x > WIDTH:
            player.speedx = 0
      

        if time_cnt > 0:
            time_cnt -= 1
        elif bg_offset > 0:
            time_cnt = 120
            bg_offset -= 1
    
        #output
        if game_active: 
            bg_offset = bg.get_height()-HEIGHT
            screen.blit(bg,(-0,-bg_offset))
            allsprites.draw(screen)
            for hit in cures_hits:
                pygame.draw.circle(screen,(255,255,255),hit.rect.center,40)
            pygame.draw.rect(screen,(0,255,255),(10,10,player.life,10))
            if os.path.exists("score.txt"): 
                with open("score.txt", "r") as f:
                    high_score = int(f.read()) 
            else:
                high_score = 0 
            if high_score < player.score:
                high_score = player.score
                with open("score.txt", "w") as f:
                    f.write(str(high_score)) 
            textScore = font.render("score " + str(player.score), True, (0,255,255))
            screen.blit(textScore,((WIDTH-textScore.get_width())/2, 10))
            high_score_text = font.render(f"high score {high_score}", True, (0, 255, 255)) 
            screen.blit(high_score_text,((WIDTH-high_score_text.get_width()), 10))
            if player.life <= 0:
                game_active = False 
          
            
                
        else: 
            textOver = font.render("Game Over ", True, (0,255,255))
            screen.blit(textOver,((WIDTH-textOver.get_width())/2, HEIGHT/2-50))
            textOver = font.render("Press Enter to try again", True, (0,255,255))
            screen.blit(textOver,((WIDTH-textOver.get_width())/2, HEIGHT/2))
            screen.blit(high_score_text,((WIDTH-high_score_text.get_width())/2, HEIGHT/2 + 50)) 
                
        pygame.display.flip()

def main_menu(): 
    while True:
        screen.blit(pygame.image.load("menuBG.png"), (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        menu_text = font.render("Main Menu", True, (150, 150, 150))
        menu_rect = menu_text.get_rect(center=(WIDTH / 2, 100))

        start_button = Button(pygame.image.load("button.png"), pos=(300, 250), word="START") 
        quit_button = Button(pygame.image.load("button.png"), pos=(300, 450), word="QUIT")
        tutorial_button = Button(pygame.image.load("tutorial_button.png"), pos=(540, 700), word="")

        screen.blit(menu_text, menu_rect)
        for button in [start_button, quit_button, tutorial_button]:
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if start_button.check_input(mouse_pos):
                    play()
                if quit_button.check_input(mouse_pos):
                    pygame.quit()
                    sys.exit()
                if tutorial_button.check_input(mouse_pos):
                    drawn_tutorial()
        pygame.display.flip()

def pause_game():
    while True:
        mouse_pos = pygame.mouse.get_pos()
        pause_text = font.render("Game is pause", True, (255, 0 , 0))
        pause_rect = pause_text.get_rect(center=(WIDTH / 2, 100))

        resume_button = Button(pygame.image.load("pause_button.png"), pos=(300, 250), word="RESUME") 
        back_button = Button(pygame.image.load("pause_button.png"), pos=(300, 450), word="BACK")
        screen.blit(pause_text, pause_rect)
        for button in [resume_button, back_button]:
            button.update(screen)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.check_input(mouse_pos):
                    play()
                if back_button.check_input(mouse_pos):
                    main_menu()
        pygame.display.flip()

def spawn_trap():
   t = Trap() 
   allsprites.add(t)
   traps.add(t)

def spawn_traps():
    global trigger
    if not trigger:  
        for _ in range(3):  
            t = Trap()
            allsprites.add(t)
            traps.add(t)
        trigger = True 

trigger = False 
        
def drawn_tutorial():
    while True:
            screen.blit(tutorial_panel,(0,0))
            mouse_pos = pygame.mouse.get_pos()

            back_button = Button(pygame.image.load("pause_button.png"), pos=(300, 730), word="BACK")
            back_button.update(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.check_input(mouse_pos):
                        main_menu()
            pygame.display.flip()

def reset_game():
    global game_active
    game_active = True
    player.life = 100
    player.score = 0
    allsprites.empty()
    trigger = True
    covids.empty()
    cures.empty()
    heals.empty()
    traps.empty()
    player.rect.midbottom = WIDTH / 2, HEIGHT - 50
    allsprites.add(player)
    for _ in range(10):
        c = Covid()
        allsprites.add(c)
        covids.add(c)
    h = Heal()
    allsprites.add(h)
    heals.add(h)
    coin = Coin()
    allsprites.add(coin)
    coins.add(coin)
    time_cnt = 600

    play()



if __name__ == "__main__":

    allsprites = pygame.sprite.Group()
    covids = pygame.sprite.Group()
    cures = pygame.sprite.Group()
    heals = pygame.sprite.Group()
    traps  = pygame.sprite.Group()
    coins = pygame.sprite.Group()

    player = Player()
    allsprites.add(player)
    for i in range(10):
        c = Covid()
        allsprites.add(c)
        covids.add(c)
    h = Heal()
    allsprites.add(h)
    heals.add(h)
    coin = Coin()
    allsprites.add(coin)
    coins.add(coin)
    time_cnt = 600
    main_menu()





