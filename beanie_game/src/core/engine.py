import pygame
from beanie_game.config.config import WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, FPS, GREEN, TILE_SIZE
from beanie_game.src.core.area import Area
from beanie_game.src.entities.player import Player
from beanie_game.src.entities.sprites import Spritesheet, Ground, Block, Enemy

engine = None
default_width = WINDOW_WIDTH
default_height = WINDOW_HEIGHT

class Engine:
    def __init__(self, game_title):
        from beanie_game.src.core.camera import create_screen
        global engine
        engine = self

        # self.active_objs = [] # Anything with an update() method which can be called

        # Layers of what order things are drawn. UI Drawables draw over Background for example
        self.background_drawables = []
        self.collisions_drawables = []
        # self.collision_objects_layer = []
        # self.drawables = [] # Anything to be drawn in the world
        # self.ui_drawables = [] # Anything to be drawn over the world
        # self.usables = []
        # self.effects = []

        self.clear_color = (30, 150, 240) # Default color if nothing else is drawn somewhere
        self.screen = create_screen(default_width, default_height, game_title) # The rectangle in the window itself
        # self.stages = {}
        # self.current_stage = None
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_spritesheet = Spritesheet('../assets/generic/character.png')
        self.char_test_spritesheet = Spritesheet('../assets/generic/char_test.png')
        self.terrain_spritesheet = Spritesheet('../assets/generic/terrain.png')
        self.main_character_spritesheet = Spritesheet('../assets/characters/main_character_male/Character_Walk.png')

        self.collision_objects_to_draw = []


    def new(self):
        # new game starts
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        # Create the Starting area, may be moved into 'stages' later
        self.area = Area(self, "area_map_terrain_layer.csv", None, stage="start")
        # self.build_collision_objects_to_draw()
        self.enemy_test = Enemy(self, 20,15)
        self.enemy_test2 = Enemy(self, 2,15)
        self.enemy_test3 = Enemy(self, 7,10)
        self.enemy_test4 = Enemy(self, 20,20)
        self.build_terrain()
        self.build_collisions()
        self.player = Player(self, 10, 10)


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        # all_sprites consists of player, ground and blocks
        self.all_sprites.update()

    def build_terrain(self):
        for layer in self.area.map.tiled_map:
            if layer.name =="Background" or layer.name =="Background2":
                for x, y, image in layer.tiles():
                    Ground(self, x , y, image=image)

    def build_collisions(self):
        from beanie_game.src.core.camera import camera
        for layer in self.area.map.tiled_map:
            if layer.name =="Collision":
                for x, y, image in layer.tiles():
                    # screen.blit(image, (x * self.tile_size, y * self.tile_size))
                    # screen.blit(image, (x * self.tile_size - camera.x, y * self.tile_size - camera.y))
                    # screen.blit(image, (x * self.tile_size, y * self.tile_size))
                    # screen.blit(image, (x, y))

                    # background moves with camera
                    # Block(self, x, y, image=image)
                    # all in top corner square
                    # Block(self, x * TILE_SIZE - camera.x, y * TILE_SIZE - camera.y, image=image)
                    # all in top corner square
                    # Block(self, x * TILE_SIZE , y * TILE_SIZE, image=image)
                    # displays as expected, background moves with camera
                    Block(self, x , y, image=image)

    def draw(self):
        # todo, can we fill the screen with a repeating image instead of block colour
        self.screen.fill(GREEN)
        # todo add the background/terrain to a group and set the layer
        # Draw background items like the tiles
        # for b in self.background_drawables:
        #     b.draw(self.screen)

        self.all_sprites.draw(self.screen)
        self.blocks.draw(self.screen)
        self.enemies.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass