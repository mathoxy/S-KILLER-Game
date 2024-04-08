from os import listdir
from os.path import join, isfile
import pygame

WIDTH_IMG, HEIGHT_IMG = 70, 70


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprites(path, direction=False):
    all_sprites = {}
    for dir in listdir(path):
        images_path = join(path, dir)
        images = [i for i in listdir(images_path) if isfile(join(images_path, i))]
        sprites = []
        for image in images:
            try:
                sprite = pygame.image.load(join(images_path, image))
                sprites.append(pygame.transform.scale(sprite, (WIDTH_IMG, HEIGHT_IMG)))
            except pygame.error as e:
                print("Assets/Error loading image:", e)

        if direction:
            all_sprites[dir + "_left"] = sprites
            all_sprites[dir + "_right"] = flip(sprites)
        else:
            all_sprites[dir + "_left"] = flip(sprites)
            all_sprites[dir + "_right"] = sprites
             
    return all_sprites


# Player class
class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    ANIMATION_DELAY = 3
    MAX_HEALTH = 5
    LIVE_POINT = 5
    SPRITES = load_sprites("Assets/mini-ninja/", True)
    def __init__(self, x, y, WIDTH_IMG, HEIGHT_IMG):
        super().__init__()
        self.rect = pygame.Rect(x, y, WIDTH_IMG, HEIGHT_IMG)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.health = self.MAX_HEALTH
        self.attack = False
        self.attack_point = 0.5
        self.touched = False
        self.score = 0
        self.shuriken_group = pygame.sprite.Group()

        
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
    
    
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    
    
    def loop(self, fps, height):
        # Set gravity
        self.y_vel += min(2, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.update_sprite()
        self.update_heath(height)
        self.fall_count += 1
    
    def draw(self, window, offset_x):
        window.blit(self.sprite, (self.rect.x -offset_x, self.rect.y))

    
    def update_sprite(self):
        sprite_sheet = "Idle"
        if self.y_vel != 0:
            if self.jump_count in [1, 2]:
                sprite_sheet = "Jump"
        elif self.y_vel > self.GRAVITY * 3:
            sprite_sheet = "Fall"

        if self.x_vel != 0:
            sprite_sheet = "Run"  

        if self.attack:
            sprite_sheet = "Attack1"
            self.attack = False
        if self.health <= 0:
            sprite_sheet = "Dead"
            
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()


    def update(self):
        # Adjust the rectangle 
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)


    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0


    def hit_head(self):
        self.fall_count = 0
        self.y_vel *= -1


    def jump(self):
        self.animation_count = 0
        self.jump_count += 1
        self.y_vel = - self.GRAVITY * 8
        if self.jump_count == 1:
            self.fall_count = 0


    def update_heath(self, height):
        # If player falls down
        if self.rect.y > height:
            self.health -= self.LIVE_POINT/5
        if self.touched:
            self.health -= self.LIVE_POINT/1000
            self.touched = False







