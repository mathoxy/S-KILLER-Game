from random import randint
from player import Player, load_sprites
WIDTH = 1000


class Enemy(Player):
    MAX_HEALTH = 3
    LIVE_POINT = 50
    SPRITES = load_sprites("EnemyGuy2/", False)
    def __init__(self, x, y, WIDTH_IMG, HEIGHT_IMG, index):
        super().__init__(x, y, WIDTH_IMG, HEIGHT_IMG)
        self.index = index
        self.previous_direction = "right"


    def update_heath(self, height):
        if self.touched:
            self.health -= self.LIVE_POINT/1000
            self.touched = False

    def statut(self, player):
        if self.health <= 0:
            player.score += 10
            self.health = self.MAX_HEALTH
            random_number = randint(-2*WIDTH, -1*WIDTH) if randint(0, 1) == 0 else randint(WIDTH, 2*WIDTH)
            self.rect.x , self.rect.y = random_number, 0

    

        


