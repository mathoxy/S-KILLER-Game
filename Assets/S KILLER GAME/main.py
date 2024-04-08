import random 
import math 
import pygame
from player import Player
from object import Block
from enemy import Enemy
pygame.init()

# Setting the caption and changing the icon
pygame.display.set_caption("S KILLER")
pygame.display.set_icon(pygame.image.load("icon/ninja.png"))

# Setting the background music
pygame.mixer.music.load('Menu/kuno_boss.mp3')
pygame.mixer.music.play(-1)
    
# Define constants and variables
WIDTH, HEIGHT = 1000, 700
FPS, PLAYER_VELX, PLAYER_VELY =  60, 5, 3.5 # Frame Per Second and Player's velosity 
BLOCK_SIZE = 96
STABILIZE = 17
START_POS = 100
offset_x = 0
scroll_width = 200


# Create a screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Background
def draw_background(path, player, offset_x, objects=None, window=None):
    image = pygame.image.load(path)
    _, _, width, height = image.get_rect()
    tiles = []

    # Multiply the image many times in order to fill the whole screen
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            tiles.append((i * width, j * height))

    
        
    # Draw the background
    for tile in tiles:
        screen.blit(image, tile)

    # Draw blocks
    if objects != None:
        for object in objects:
            object.draw(screen, offset_x)

    # Draw life
    heart = pygame.image.load("items/heart.png")
    heart_rect = heart.get_rect()
    heart_rect.x = 50
    heart_rect.y = 25
    if window != None:
        window.blit(heart, heart_rect)

        font = pygame.font.Font('Font/OpenSans-Bold.ttf', 30)
        life = font.render(str(math.ceil(player.health)), True, (0, 0, 0))
        life_rect =life.get_rect()
        life_rect.x = 130
        life_rect.y = 45
        window.blit(life, life_rect)
        score = font.render(f"Score: {player.score}", True, (0, 0, 0))
        score_rect = score.get_rect()
        score_rect.x = 180
        score_rect.y = 45
        window.blit(score, score_rect)


# Draw menu
def draw_menu(window):
    width, height = pygame.display.get_window_size()
    # Load images
    start = pygame.image.load("Menu/Start.png")
    pygame.transform.scale(start ,(width / 2, height / 2))
    start_rect = start.get_rect()
    start_rect.centerx = width / 2

    play_button = pygame.image.load("Menu/Play.png")
    play_button_rect = play_button.get_rect()
    play_button_rect.centerx = width / 2
    play_button_rect.centery = height/ 2


    # Draw images on the screen
    window.blit(start, start_rect)
    window.blit(play_button, play_button_rect)

    return play_button_rect


def load_bocks():
    floor = [Block(i * BLOCK_SIZE, HEIGHT - BLOCK_SIZE, BLOCK_SIZE) for i in range(-WIDTH // BLOCK_SIZE, (WIDTH * 2)// BLOCK_SIZE)]
    objects = [
        *floor, 
        Block(0, HEIGHT - BLOCK_SIZE * 2, BLOCK_SIZE),
        *[Block(BLOCK_SIZE * i, HEIGHT - BLOCK_SIZE * i, BLOCK_SIZE) for i in range(3, 7)],
        *[Block(BLOCK_SIZE * (13 - i), HEIGHT - BLOCK_SIZE * i, BLOCK_SIZE) for i in range(6, 2, -1)],
        Block(BLOCK_SIZE*13, HEIGHT - BLOCK_SIZE * 2, BLOCK_SIZE)
    ]
    return objects


# Handle vertical collision
def vertical_collision(player, objects, dy):
    collided_objects = []
    for object in objects:
        if pygame.sprite.collide_mask(player, object):
            if dy < 0:
                player.rect.top = object.rect.bottom
                player.hit_head()
            elif dy > 0:
                player.rect.bottom = object.rect.top + STABILIZE# stabilize the player  
                player.landed()
    
    collided_objects.append(object)

    return collided_objects


# Handle horizontal collision
def collide(player, objects, dx):
    player.move(dx, 0)
    player.rect.top -= STABILIZE
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
        
    player.move(-dx, 0)
    player.rect.top += STABILIZE
    player.update()
    return collided_object


# Handle player move
def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    # Initialisation
    player.x_vel = 0

    collide_left = collide(player, objects, -PLAYER_VELX * 2)
    collide_right = collide(player, objects, PLAYER_VELX * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VELX)
    
    elif keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VELX)

    elif keys[pygame.K_a]:
        player.attack = True

    vertical_collision(player, objects, player.y_vel)


def game_statut(player):
    global offset_x

    # If the player falls down
    if math.ceil(player.health) <=  0:
            player.health = player.MAX_HEALTH
            player.score = 0
            return False
    if player.rect.y > HEIGHT:
        player.rect.x, player.rect.y = START_POS, START_POS
        offset_x = 0
        return True
    
    return True


def enemy_move(player, enemy, objects):
    enemy.x_vel = 0
    # Assingn a velosity to the enemies
    if enemy.index == 0: enemy_velx = 1
    if enemy.index == 1: enemy_velx = 1.5
    if enemy.index == 2: enemy_velx = 2
    collide_left = collide(enemy, objects, -enemy_velx * 2)
    collide_right = collide(enemy, objects, enemy_velx * 2)

    # If there is a collision with an object 
    if collide_right or collide_left: 
        if enemy.previous_direction == "left": 
            enemy.move_right(enemy_velx)
            enemy.previous_direction = "right"
        elif enemy.previous_direction == "right":
            enemy.move_left(enemy_velx)
            enemy.previous_direction = "left"

    else: 
        if enemy.previous_direction == "right": 
            enemy.move_right(enemy_velx)
            enemy.previous_direction = "right"
        else:
            enemy.move_left(enemy_velx)
            enemy.previous_direction = "left"
    vertical_collision(enemy, objects, enemy.y_vel)

    # If player arround 
    if 4 < abs(enemy.rect.centerx - player.rect.centerx) < 90 and abs(enemy.rect.centery - player.rect.centery) < 90:
        
        if enemy.previous_direction == "left" and player.rect.centerx > enemy.rect.centerx: 
            enemy.move_right(enemy_velx)
            enemy.previous_direction =   "right"
        elif enemy.previous_direction == "right" and player.rect.centerx < enemy.rect.centerx:
            enemy.move_left(enemy_velx)
            enemy.previous_direction = "left"
            
    # If the enemy collides the player
    if pygame.sprite.collide_mask(enemy, player): 
        enemy.attack = True
        player.touched = True
        if player.attack:
            enemy.touched = True

    # If the enemy falls down
    if enemy.rect.y >= WIDTH:
        enemy.rect.x, enemy.rect.y = random.randint(0, WIDTH), START_POS 

    # Enemy statut
    enemy.statut(player)


def main(window):
    global offset_x
    game_active = False
    clock = pygame.time.Clock()
    
    # Create instances
    player = Player(START_POS, START_POS, 70, 70)
    enemy_group = pygame.sprite.Group(Enemy(random.randint(0, WIDTH), START_POS, 80, 80, 0),
                     Enemy(random.randint(0, WIDTH), START_POS, 80, 80, 1),
                     Enemy(random.randint(0, WIDTH), START_POS, 80, 80, 2))
    
    objects = load_bocks()
    
        
    run = True
    

    
    # Game loop
    while run:
        clock.tick(FPS) # Impose the number of frames per second
        
        

        if game_active:
            game_active = game_statut(player)
            draw_background("Background/Purple.png", player, offset_x, objects, window)
            player.loop(FPS, HEIGHT)
            player.draw(window, offset_x)
            handle_move(player, objects)
            for enemy in enemy_group:
                enemy.loop(FPS, HEIGHT)
                enemy.draw(window, offset_x)
                enemy_move(player, enemy, objects)                

            if (player.rect.right - offset_x >= WIDTH - scroll_width and player.x_vel > 0) or (
                player.rect.left - offset_x <= scroll_width and player.x_vel < 0):
                offset_x += player.x_vel

            # Pause the background sound
            pygame.mixer.music.pause()
            
        else:
            draw_background("Background/Purple.png", player, offset_x)
            play_button_rect = draw_menu(window)
            pygame.mixer.music.unpause()
             

        # Getting events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
       
            elif event.type == pygame.KEYDOWN and game_active:
                if event.key == pygame.K_UP and player.jump_count < 2:
                    player.jump()
        
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_active:
                if play_button_rect.collidepoint(event.pos):
                    game_active = True
            elif event.type == pygame.KEYDOWN and not game_active:
                if event.key == pygame.K_SPACE:
                    game_active = True

        pygame.display.update()

    pygame.quit()
        

if __name__ == "__main__":
    main(screen)

