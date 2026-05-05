import random
import time
import math
import pygame
from core.maze import Maze
from entities.player import Player
from entities.enemy import Enemy
from entities.support_enemy import Support_enemy

class Level2:
    def __init__(self, game):
        self.game = game

        self.type = random.randint(1, 3)
        self.map = random.randint(1, 3)

        self.maze = Maze.load_from_txt(f"maps/level1/map{self.map}.txt")

        self.player_spawn = (0, 0)
        self.goal_x = self.maze.cols - 1
        self.goal_y = self.maze.rows - 1

        self.enemy_spawn = self.get_enemy_spawn()

        self.player = Player(*self.player_spawn)
        self.enemy = Enemy(*self.enemy_spawn)

        self.randomize()

        self.support_enemy_spawn = self.get_support_enemy_spawn()
        self.support_enemy = Support_enemy(*self.support_enemy_spawn)

        self.carry = False
        self.points = 0
        self.satisfy = False
        self.change = False

        self.alpha = 255
        self.alpha_dir = -5
        self.sun_angle = 0
        self.last_move = 0

        self.tutorial_data = {
            "lines": [
                "Collect Dorayaki and give them to Doraemon",
                "Get enough to unlock the Magic Door and escape!",
                "Avoid Jaian!"
            ],
            "note": "Note: You can carry only one Dorayaki at a time."
        }

    def get_support_enemy_spawn(self):
        walkable = []

        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                if (self.maze.is_walkable(j, i) and (i, j) != self.player_spawn and (j, i) != (self.goal_x, self.goal_y)) and (i, j) != self.enemy_spawn:
                    walkable.append((j, i))

        def far(cell):
            return min(
                abs(cell[0] - self.player_spawn[0]) + abs(cell[1] - self.player_spawn[1]),
                abs(cell[0] - self.doraemon[0]) + abs(cell[1] - self.doraemon[1]),
                abs(cell[0] - self.enemy_spawn[0]) + abs(cell[1] - self.enemy_spawn[1]),
            )

        walkable.sort(key=far, reverse=True)

        return walkable[0]
    
    def get_enemy_spawn(self):
        walkable = []

        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                if (self.maze.is_walkable(i, j) and (i, j) != self.player_spawn and (j, i) != (self.goal_x, self.goal_y)):
                    walkable.append((j, i))

        def far(cell):
            return abs(cell[0] - self.player_spawn[0]) + abs(cell[1] - self.player_spawn[1])

        walkable.sort(key=far, reverse=True)

        enemy = walkable[:len(walkable) // 4]

        return enemy[0]

    def randomize(self):
        walkable = []

        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                if (self.maze.is_walkable(i, j) and (i, j) != self.player_spawn and (j, i) != (self.goal_x, self.goal_y) and (i, j) != self.enemy_spawn): 
                    walkable.append((j, i))

        def far_doraemon(cell):
            return abs(cell[0] - self.player_spawn[0]) + abs(cell[1] - self.player_spawn[1]) + abs(cell[0] - self.enemy_spawn[0]) + abs(cell[1] - self.enemy_spawn[1])

        far_cells = sorted(walkable, key=far_doraemon, reverse=True)
        positions = random.sample(far_cells[:len(far_cells) // 2], 1)
        self.doraemon = positions[0]

        def far_dorayaki(cell):
            return abs(cell[0] - self.player_spawn[0]) + abs(cell[1] - self.player_spawn[1]) + abs(cell[0] - self.enemy_spawn[0]) + abs(cell[1] - self.enemy_spawn[1]) + abs(cell[0] - self.doraemon[0]) + abs(cell[1] - self.doraemon[1])


        far_cells = sorted(walkable, key=far_dorayaki, reverse=True)
        positions = random.sample(far_cells[:len(far_cells)], 3)
        self.dorayaki = positions[:3]
        

    def update(self):
        keys = pygame.key.get_pressed()

        self.player.handle_input(keys, self.maze)
        self.player.update()

        if self.carry or self.points:
            if time.time() - self.last_move > 0.4 - (self.carry + self.points) * 0.05:
                self.enemy.update(self.player, self.maze)
                self.last_move = time.time()
        if self.points:
            self.support_enemy.update(self.player, self.maze, self.game)

        if (self.enemy.grid_x == self.player.grid_x and self.enemy.grid_y == self.player.grid_y):
            self.game.game_over = True

        if (self.satisfy and self.player.grid_x == self.goal_x and self.player.grid_y == self.goal_y):
            self.game.game_victory = True

        px = self.player.grid_x
        py = self.player.grid_y

        for item in self.dorayaki[:]:
            if self.carry:
                break

            if item == (py, px):
                self.dorayaki.remove(item)
                self.carry = True

        if (self.carry and self.player.grid_x == self.doraemon[1] and self.player.grid_y == self.doraemon[0]):
            self.points += 1
            self.carry = False

        if self.points == 3:
            self.satisfy = True

    def draw(self, renderer, screen):
        if self.satisfy and self.change == False:
            gx = self.goal_x
            gy = self.goal_y

            renderer.maze_surface.blit(renderer.exit_open_image, (gx * 30, gy * 30))

            self.change = True

        if self.points:
            gx, gy = self.doraemon

            if self.type == 1:
                renderer.draw_path_block1(renderer.maze_surface, gy * 30, gx * 30)

            elif self.type == 2:
                renderer.draw_path_block2(renderer.maze_surface, gy * 30, gx * 30)

            else:
                renderer.draw_path_block3(renderer.maze_surface, gy * 30, gx * 30)

            renderer.maze_surface.blit(renderer.doraemon_eating_image, (gy * 30, gx * 30))

        screen.blit(renderer.maze_surface, (0, 0))

        renderer.draw_player(screen, self.player)

        renderer.draw_enemy(screen, self.enemy)

        renderer.draw_support_enemy(screen, self.support_enemy)

        self.alpha += self.alpha_dir

        if self.alpha <= 120 or self.alpha >= 255:
            self.alpha_dir *= -1

        self.sun_angle += 2

        img = renderer.dorayaki_image.copy()
        img.set_alpha(self.alpha)

        for x, y in self.dorayaki:
            cx = y * 30 + 15
            cy = x * 30 + 15

            for i in range(12):
                angle = math.radians(i * 30 + self.sun_angle)

                length1 = 11
                length2 = 21

                x1 = cx + math.cos(angle) * length1
                y1 = cy + math.sin(angle) * length1

                x2 = cx + math.cos(angle) * length2
                y2 = cy + math.sin(angle) * length2

                pygame.draw.line(screen, (255, 200, 0), (x1, y1), (x2, y2), 3)

            screen.blit(img, (y * 30, x * 30))