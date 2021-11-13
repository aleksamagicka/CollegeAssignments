import heapq
from _heapq import heappush
from collections import deque
from math import sqrt

import pygame
import os
import config


class BaseSprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, row, col, file_name, transparent_color=None):
        pygame.sprite.Sprite.__init__(self)
        if file_name in BaseSprite.images:
            self.image = BaseSprite.images[file_name]
        else:
            self.image = pygame.image.load(os.path.join(config.IMG_FOLDER, file_name)).convert()
            self.image = pygame.transform.scale(self.image, (config.TILE_SIZE, config.TILE_SIZE))
            BaseSprite.images[file_name] = self.image
        # making the image transparent (if needed)
        if transparent_color:
            self.image.set_colorkey(transparent_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * config.TILE_SIZE, row * config.TILE_SIZE)
        self.row = row
        self.col = col


class Agent(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Agent, self).__init__(row, col, file_name, config.DARK_GREEN)

    def move_towards(self, row, col):
        row = row - self.row
        col = col - self.col
        self.rect.x += col
        self.rect.y += row

    def place_to(self, row, col):
        self.row = row
        self.col = col
        self.rect.x = col * config.TILE_SIZE
        self.rect.y = row * config.TILE_SIZE

    # game_map - list of lists of elements of type Tile
    # goal - (row, col)
    # return value - list of elements of type Tile
    def get_agent_path(self, game_map, goal):
        pass


class ExampleAgent(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        row = self.row
        col = self.col
        while True:
            if row != goal[0]:
                row = row + 1 if row < goal[0] else row - 1
            elif col != goal[1]:
                col = col + 1 if col < goal[1] else col - 1
            else:
                break
            path.append(game_map[row][col])
        return path

def get_around(row, col, game_map):
    around = list()

    max_row = len(game_map)
    max_col = len(game_map[0])

    # Sever
    if row - 1 >= 0:
        # Can go up
        around.append(game_map[row - 1][col])
    # Istok
    if col + 1 < max_col:
        # Can go right
        around.append(game_map[row][col + 1])
    # Jug
    if row + 1 < max_row:
        # Can go down
        around.append(game_map[row + 1][col])
    # Zapad
    if col - 1 >= 0:
        # Can go left
        around.append(game_map[row][col - 1])

    return around

class Aki(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        # Putanja do sada i sledeci cvor
        stack = deque([([], game_map[self.row][self.col])])
        poseceni = set()
        while stack:
            path, current = stack.pop()

            if current.row == goal[0] and current.col == goal[1]:
                return path + [current]
            if current in poseceni:
                continue
            poseceni.add(current)

            polja_okolo = get_around(current.row, current.col, game_map)

            polja_okolo.sort(key=lambda y: y.cost())

            polja_okolo.reverse()

            for polje in polja_okolo:
                stack.append((path + [current], polje))

        return path

class Jocke(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        # Putanja do sada i sledeci cvor
        queue = deque([([], game_map[self.row][self.col])])
        poseceni = set()
        while queue:
            path, current = queue.popleft()

            if current.row == goal[0] and current.col == goal[1]:
                return path + [current]
            if current in poseceni:
                continue
            poseceni.add(current)

            polja_okolo = get_around(current.row, current.col, game_map)
            polja_okolo.reverse()

            heap = list()

            for p in polja_okolo:
                # Njihova tri polja
                tri_polja = get_around(p.row, p.col, game_map)
                heap.append(((sum(polje.cost() for polje in tri_polja) - current.cost()) / (len(tri_polja) - 1), p))

            heapq.heapify(heap)

            while heap:
                queue.append((path + [current], heapq.heappop(heap)[1]))

        return path

class Draza(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        paths = [(0, path)]

        while paths:
            cost, path = heapq.heappop(paths)
            last = path[-1]

            # Provera na ekspandovani cvor
            if last.row == goal[0] and last.col == goal[1]:
                return path

            polja_okolo = get_around(last.row, last.col, game_map)

            for p in polja_okolo:
                if p not in path:
                    heapq.heappush(paths, (cost + p.cost(), path + [p]))

        return path


class Bole(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        paths = [(0, path, 0)]

        while paths:
            cost, path, old_heuristic = heapq.heappop(paths)
            last = path[-1]

            # Provera na ekspandovani cvor
            if last.row == goal[0] and last.col == goal[1]:
                return path

            polja_okolo = get_around(last.row, last.col, game_map)
            heapq.heapify(polja_okolo)

            for p in polja_okolo:
                if p not in path:
                    manhattan_distance = abs(p.row - goal[0]) + abs(p.col-goal[1])
                    euc_distance = sqrt((p.row-goal[0])**2 + (p.col-goal[1])**2)
                    heuristic = manhattan_distance

                    heapq.heappush(paths, (cost + p.cost() + heuristic - old_heuristic, path + [p], heuristic))

        return path

class Tile(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Tile, self).__init__(row, col, file_name)

    def position(self):
        return self.row, self.col

    def cost(self):
        pass

    def kind(self):
        pass

    def __lt__(self, other):
        return self.cost() < other.cost()


class Stone(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'stone.png')

    def cost(self):
        return 1000

    def kind(self):
        return 's'


class Water(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'water.png')

    def cost(self):
        return 500

    def kind(self):
        return 'w'


class Road(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'road.png')

    def cost(self):
        return 2

    def kind(self):
        return 'r'


class Grass(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'grass.png')

    def cost(self):
        return 3

    def kind(self):
        return 'g'


class Mud(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'mud.png')

    def cost(self):
        return 5

    def kind(self):
        return 'm'


class Dune(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'dune.png')

    def cost(self):
        return 7

    def kind(self):
        return 's'


class Goal(BaseSprite):
    def __init__(self, row, col):
        super().__init__(row, col, 'x.png', config.DARK_GREEN)


class Trail(BaseSprite):
    def __init__(self, row, col, num):
        super().__init__(row, col, 'trail.png', config.DARK_GREEN)
        self.num = num

    def draw(self, screen):
        text = config.GAME_FONT.render(f'{self.num}', True, config.WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
