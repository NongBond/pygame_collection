import pygame, sys
from setting import *
from os import walk

pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()
start_bg = pygame.image.load("./asset_kenney_pixel-platformer/AdditionArtwork/start_bg.png").convert_alpha()
font = pygame.font.SysFont("arial", 40, bold=True)
buttonImg = pygame.image.load("./asset_kenney_pixel-platformer/Tiles/tile_0086.png").convert_alpha()
tutorial_button_image = pygame.image.load("./asset_kenney_pixel-platformer/AdditionArtwork/tutorial_button.png").convert_alpha()
tutorial_image = pygame.image.load("./asset_kenney_pixel-platformer/AdditionArtwork/tutorial.png").convert_alpha()
trap_image = pygame.image.load("./asset_kenney_pixel-platformer/Tiles/tile_0068.png").convert_alpha()
green_character = pygame.image.load("./asset_kenney_pixel-platformer/Characters/character_0000.png").convert_alpha()
blue_character = pygame.image.load("./asset_kenney_pixel-platformer/Characters/character_0002.png").convert_alpha()
pink_character = pygame.image.load("./asset_kenney_pixel-platformer/Characters/character_0004.png").convert_alpha()
yellow_character = pygame.image.load("./asset_kenney_pixel-platformer/Characters/character_0006.png").convert_alpha()
character_color = ""
pygame.mixer.init()
collect_itme_sound = pygame.mixer.Sound("./Sound/collectItem.mp3")
collect_itme_sound.set_volume(0.2)
jump_sound = pygame.mixer.Sound("./Sound/jump.mp3") 
jump_sound.set_volume(0.2)
hurt_sound = pygame.mixer.Sound("./Sound/hurt.mp3")
hurt_sound.set_volume(0.2)
heal_sound = pygame.mixer.Sound("./Sound/heal.mp3")
heal_sound.set_volume(0.2)
bg_sound = pygame.mixer.Sound("./Sound/background.mp3")
bg_sound.set_volume(0.2)
bg_sound.play(loops=-1)
keyImg = pygame.image.load("./asset_kenney_pixel-platformer/Tiles/tile_0027.png").convert_alpha()
chest_img = pygame.image.load("./asset_kenney_pixel-platformer/Tiles/tile_0028.png").convert_alpha()
gameover_bg = pygame.image.load("./asset_kenney_pixel-platformer/AdditionArtwork/gameover_bg.png").convert_alpha()
gameover_button = pygame.image.load("./asset_kenney_pixel-platformer/AdditionArtwork/button.png").convert_alpha()
start_time = 0
health_decrease_rate = 1
last_decrease = 0




class Player(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.1
        self.character_asset_catagory()
        self.image = self.characters["Green"][0]
        self.image = pygame.transform.rotozoom(self.image, 0, 2)
        self.rect = self.image.get_rect(topleft = (pos))
        self.speed = 5
        self.direction = pygame.math.Vector2()
        self.gravity = 0.98
        self.jump_force = -19
        self.player_state = "idle"
        self.facing_left = True
        self.on_ground = False
        self.score = 0
        self.max_health = 20
        self.health = self.max_health
        self.health_bar = Healthbar(self, self.max_health, 100, 20)
        self.invincible = False 
        self.invincible_start_time = 0
        self.invincible_duration = 5

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_left = False
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_left = True
        else:
            self.direction.x = 0
        
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def death(self):
        game_over()

    def animation(self):
        character = self.characters[character_color]

        if self.character_state == "idle":
            self.frame_index = 0
     
        if self.character_state == "run":
            self.frame_index += self.animation_speed
            if self.frame_index >= len(character):
                self.frame_index = 0
        if self.character_state == "jump":
            self.image = character[0]
            self.image = pygame.transform.rotozoom(self.image, 0, 2)

        if self.facing_left:
            self.image = character[int(self.frame_index)]
            self.image = pygame.transform.rotozoom(self.image, 0, 2)
        else:
            self.flipImage = pygame.transform.flip(character[int(self.frame_index)], True, False)
            self.image = pygame.transform.rotozoom(self.flipImage, 0, 2)

    def character_asset_catagory(self):
        character_path = "./asset_kenney_pixel-platformer/MainCharacter"
        self.characters = {"Green":[], "Blue":[], "Yellow":[], "Pink":[]}
        for character in self.characters.keys():
            full_path = character_path + "/" + character
            self.characters[character] = import_folder(full_path)

    def get_character_state(self):
        if self.direction.y < 0:
            self.character_state = "jump"
        elif self.direction.y > 0:
            self.character_state = "fall"
        else:
            if self.direction.x != 0:
                self.character_state = "run"
            else:
                self.character_state = "idle"

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_force
        jump_sound.play()

    def get_hit(self):
        if not self.invincible:
            hurt_sound.play()
            self.health -= 5
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()

    def update(self) -> None:
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_start_time >= self.invincible_duration * 1000:
                self.invincible = False
        self.get_input()
        self.get_character_state()
        self.animation()
        self.health_bar.update()
        if self.health <= 0 or self.rect.top > SCREEN_HEIGHT:
            self.death()

class Level():
    def __init__(self, level_data, surface) -> None:
        self.display_surf = surface
        self.level_setup(level_data)
        self.move_map = 0
        self.score_text = None
        self.health_text = None
        self.font = pygame.font.SysFont("arial", 40)
        self.last_decrease_time = 0

    def level_setup(self, layout):
        self.tiles = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.chest = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for column_index, column in enumerate(row):
                #print(f"row:{row_index}, column:{column_index} = {column}")
                x = column_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if column == "X":
                    tile = Tile((x, y), TILE_SIZE, "dirt")
                    self.tiles.add(tile)
                if column == "G":
                    tile = Tile((x, y), TILE_SIZE, "grass")
                    self.tiles.add(tile)
                if column == "L":
                    tile = Tile((x, y), TILE_SIZE, "left_grass")
                    self.tiles.add(tile)
                if column == "R":
                    tile = Tile((x, y), TILE_SIZE, "right_grass")
                    self.tiles.add(tile)
                if column == "K":
                    item = Item((x, y), TILE_SIZE, "key")
                    self.keys.add(item)
                if column == "H":
                    item = Item((x, y), TILE_SIZE, "heart")
                    self.hearts.add(item)
                if column == "C":
                    item = Item((x, y), TILE_SIZE, "chest")
                    self.chest.add(item)
                if column == "T":
                    item = Item((x, y), TILE_SIZE, "trap")
                    self.traps.add(item)
                if column == "P":
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        player_direction = player.direction.x
        
        if player_x < SCREEN_WIDTH/3 and player_direction < 0: # move left
            self.move_map = 5 # move map to the left
            player.speed = 0
        elif player_x > SCREEN_WIDTH - (SCREEN_WIDTH/3) and player_direction > 0: # move right
            self.move_map = -5 # move map to the right
            player.speed = 0
        else:
            self.move_map = 0
            player.speed = 5

    def horizontal_collision(self):
        player = self.player.sprite
        chest = self.chest.sprite
        player.rect.x += player.direction.x * player.speed
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
        for sprite in self.keys.sprites():
            if sprite.rect.colliderect(player.rect):
                sprite.kill()
                player.score += 1
                collect_itme_sound.play()
        for sprite in self.hearts.sprites():
            if sprite.rect.colliderect(player.rect):
                sprite.kill()
                player.health += 5
                heal_sound.play()
                if player.health >= player.max_health:
                    player.health = player.max_health
        for sprite in self.traps.sprites():
            if sprite.rect.colliderect(player.rect):
                player.get_hit()
        if chest.rect.colliderect(player.rect) and player.score == 10:
            win()

    def vertical_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0: # player is in the fall state
                    player.rect.bottom = sprite.rect.top # prevent falling down
                    player.direction.y = 0 # prevent excessive gravity force
                    player.on_ground = True
                elif player.direction.y < 0: # player is in the jump state
                    player.rect.top = sprite.rect.bottom # prevent from jumping through the tiles
                    player.direction.y = 0 # cancel player jump force
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        
    def display_text(self):
        scaled_key_img = pygame.transform.scale(keyImg, (32, 32))
        self.display_surf.blit(scaled_key_img, (SCREEN_WIDTH/2, 60))
        #self.score_text = self.font.render(str(self.player.sprite.score), True, "bisque4")
        self.score_text = self.font.render(str(len(self.keys)), True, "bisque4")
        self.display_surf.blit(self.score_text, (SCREEN_WIDTH/2 + 40, 54))

        #self.health_text = self.font.render(str(self.player.sprite.health), True, "darkred")
        #self.display_surf.blit(self.health_text, (self.player.sprite.health_bar.rect.width+10, 0))

        self.player.sprite.health_bar.update()
        self.display_surf.blit(self.player.sprite.health_bar.image, (10, 10))

    def timer(self):
        current_time = pygame.time.get_ticks() 
        if current_time - self.last_decrease_time >= 1000:  
            self.last_decrease_time = current_time  
            if self.player.sprite.health > 0:
                self.player.sprite.health -= health_decrease_rate
            else:
                self.player.sprite.health = 0
        
    def run(self):
        self.tiles.update(self.move_map)
        self.tiles.draw(self.display_surf)

        self.keys.update(self.move_map)
        self.keys.draw(self.display_surf)

        self.hearts.update(self.move_map)
        self.hearts.draw(self.display_surf)

        self.traps.update(self.move_map)
        self.traps.draw(self.display_surf)

        self.chest.update(self.move_map)
        self.chest.draw(self.display_surf)

        self.player.update()
        self.player.draw(self.display_surf)
        self.scroll_x()
        self.horizontal_collision()
        self.vertical_collision()
        self.display_text()
        self.timer()

class Healthbar(pygame.sprite.Sprite):
    def __init__(self, player,max_health, width, height):
        super().__init__()

        self.max_health = max_health
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.player = player

        self.fill_color = (255, 0, 0) 
        self.empty_color = (0, 0, 0)  


    def update(self):
        if self.player.health < 0:
            self.player.health = 0
        health_ratio = self.player.health / self.max_health
        self.image.fill(self.empty_color)
        pygame.draw.rect(self.image, self.fill_color, (0, 0, int(self.width * health_ratio), self.height))


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, type):
        super().__init__()
        # self.image = pygame.Surface((size, size))
        # self.image.fill("black")
        self.tile_type(type)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft = (pos))
    
    def update(self, x_move):
        self.rect.x += x_move

    def tile_type(self, type):
        if type == "dirt":
            self.image = pygame.image.load("./asset_kenney_pixel-platformer/Tiles/tile_0004.png").convert_alpha()
        if type == "grass":
            self.image = pygame.image.load("./asset_kenney_pixel-platformer/Tiles/tile_0002.png").convert_alpha()
        if type == "left_grass":
            self.image = pygame.image.load("./asset_kenney_pixel-platformer/Tiles/tile_0001.png").convert_alpha()
        if type == "right_grass":
            self.image = pygame.image.load("./asset_kenney_pixel-platformer/Tiles/tile_0003.png").convert_alpha()
        if type == "key":
            self.image = pygame.image.load("./asset_kenney_pixel-platformer/Tiles/tile_0027.png").convert_alpha()

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, size, type):
        super().__init__()
        # self.image = pygame.Surface((size, size))
        # self.image.fill("black")
        self.item_type(type)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft = (pos))
    
    def update(self, x_move):
        self.rect.x += x_move

    def item_type(self, type):
        if type == "key":
            self.image = keyImg
        if type == "heart":
            self.image = pygame.image.load("./asset_kenney_pixel-platformer/Tiles/tile_0044.png").convert_alpha()
        if type == "trap":
            self.image = pygame.image.load("./asset_kenney_pixel-platformer/Tiles/tile_0068.png").convert_alpha()
        if type == "chest":
            self.image = chest_img


class Button: 
    def __init__(self, image, size, pos, word):
        self.image = image
        self.image = pygame.transform.scale(self.image, (size, size))
        self.xpos = pos[0]
        self.ypos = pos[1]
        self.word = word
        self.text = font.render(self.word, True, (150, 150, 150))
        self.rect = self.image.get_rect(center=(self.xpos, self.ypos-20))
        self.text_rect = self.text.get_rect(center=(self.xpos, self.ypos-20))

    def update(self, screen): 
        screen.blit(self.image, self.rect)
        screen.blit(font.render(self.word, True, "bisque2"), self.text_rect)

    def check_input(self, pos): 
        if self.rect.collidepoint(pos):
            return True
        return False
    
def pause_menu():
    while True:
        mouse_pos = pygame.mouse.get_pos()
        pause_text = font.render("Paused", True, "bisque2")
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH / 2, 100))
        resume_button = Button(buttonImg, 216, pos=(SCREEN_WIDTH/2, 350), word="RESUME") 
        back_button = Button(buttonImg, 216, pos=(SCREEN_WIDTH/2, 650), word="BACK")

        SCREEN.blit(pause_text, pause_rect)
        for button in [resume_button, back_button]:
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if resume_button.check_input(mouse_pos):
                    return
                if back_button.check_input(mouse_pos):
                    main_menu()
        pygame.display.flip()

def main_menu(): 
    while True:
        SCREEN.blit(start_bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        menu_text = font.render("Main Menu", True, "bisque2")
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH / 2, 100))
        start_button = Button(buttonImg, 162, pos=(SCREEN_WIDTH/2, 350), word="START") 
        quit_button = Button(buttonImg, 162, pos=(SCREEN_WIDTH/2, 600), word="QUIT")
        tutorial_button = Button(tutorial_button_image, 64, pos=(1220, 720), word="")

        SCREEN.blit(menu_text, menu_rect)
        for button in [start_button, quit_button, tutorial_button]:
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if start_button.check_input(mouse_pos):
                    select_character()
                if quit_button.check_input(mouse_pos):
                    pygame.quit()
                    sys.exit()
                if tutorial_button.check_input(mouse_pos):
                    tutorial()
        pygame.display.flip()

def select_character(): 
    global character_color
    while True:
        SCREEN.blit(start_bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        character_text = font.render("SELECT YOUR CHARACTER", True, "bisque2")
        character_rect = character_text.get_rect(center=(SCREEN_WIDTH / 2, 200))
        green_button = Button(green_character,126, pos=(250, SCREEN_HEIGHT/2), word="") 
        blue_button = Button(blue_character, 126, pos=(500, SCREEN_HEIGHT/2), word="")
        pink_button = Button(pink_character, 126, pos=(750, SCREEN_HEIGHT/2), word="")
        yellow_button = Button(yellow_character, 126, pos=(1000, SCREEN_HEIGHT/2), word="")


        SCREEN.blit(character_text, character_rect)
        for button in [green_button, blue_button, pink_button, yellow_button]:
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if green_button.check_input(mouse_pos):
                    character_color = "Green"
                    return game()
                if blue_button.check_input(mouse_pos):
                    character_color = "Blue"
                    return game()
                if pink_button.check_input(mouse_pos):
                    character_color = "Pink"
                    return game()
                if yellow_button.check_input(mouse_pos):
                    character_color = "Yellow"
                    return game()
        pygame.display.flip()

def game():
    level = Level(level_data, SCREEN)
    pause = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not pause:
                        pause = True
                        pause_menu()
                    else:
                        pause = False
        SCREEN.fill("aquamarine2")
        clock.tick(FPS)
        level.run()
        
            
        pygame.display.update()

def game_over():
    while True:
        SCREEN.blit(gameover_bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        death_text = font.render("YOU ARE DEATH", True, "bisque2")
        death_rect = death_text.get_rect(center=(SCREEN_WIDTH / 2, 100))
        restart_button = Button(buttonImg, 216, pos=(SCREEN_WIDTH/2, 350), word="RESTART") 
        back_button = Button(buttonImg, 216, pos=(SCREEN_WIDTH/2, 650), word="BACK")

        SCREEN.blit(death_text, death_rect)
        for button in [restart_button, back_button]:
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if restart_button.check_input(mouse_pos):
                    game()
                if back_button.check_input(mouse_pos):
                    main_menu()
        clock.tick(FPS)
        pygame.display.flip()

def win():
    while True:
        mouse_pos = pygame.mouse.get_pos()
        winning_text = font.render("YOU WIN!!", True, "brown")
        winning_rect = winning_text.get_rect(center=(SCREEN_WIDTH/2, 100))
        back_button = Button(buttonImg, 216, pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), word="Back")

        SCREEN.blit(winning_text, winning_rect)
        back_button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_input(mouse_pos):
                    main_menu()
        pygame.display.flip()

def tutorial():
     while True:
        SCREEN.blit(tutorial_image, (110, 60))
        mouse_pos = pygame.mouse.get_pos()
        back_button = Button(buttonImg, 126, pos=(1080, 180), word="Back")

        back_button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_input(mouse_pos):
                    main_menu()
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()