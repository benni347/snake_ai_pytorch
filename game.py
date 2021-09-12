"""
The classic game of snake. Made with python
and pygame with reinforcement learning from pytorch


Date Modified:  Sep 12, 2021
Author: https://www.github.com/benni347
"""

# Imports
import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

# init pygame
pygame.init()

# use the arial font
font = pygame.font.Font("arial.ttf", 25)

# reset

# reward

# play(action) -> direction

# game_iteration

# is_collision


class Direction(Enum):
    """
    Direction class representing the direction.
    """
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


point = namedtuple("point", "x, y")

# RGB Color Vars
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

# Game vars
BLOCK_SIZE = 20
SPEED = 20


class SnakeGameAI:
    """
    SnakeGame class representing the game.
    """

    def __init__(self, width=640, height=480):
        """
        Initialize the object
        :param width: starting x pos (int)
        :param height: starting y pos (int)
        :return: None
        """
        self.width = width
        self.height = height
        # init display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        """
        When the AI dies it resets the game.
        :return: None
        """
        # init game state
        self.direction = Direction.RIGHT

        self.head = point(self.width/2, self.height/2)
        self.snake = [self.head,
                      point(self.head.x-BLOCK_SIZE, self.head.y),
                      point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        """
        Place the food somewhere on the screen.
        :return: None
        """
        x = random.randint(0, (self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE  # random x pos for spawning food (int)
        y = random.randint(0, (self.height-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE  # random y pos for spawning food (int)
        self.food = point(x, y)
        if self.food in self.snake:  # this will check if food would spawn in the snake if yes it tries again
            self._place_food()

    def play_step(self, action):
        """
        Main things for the game.
        :param action: move (tuple)
        :return: [int, bool, int]
        """
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Close the window when the x is pressed
                pygame.quit()
                quit()

        # 2. move
        self._move(action)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. return game over and score
        return reward, game_over, self.score


    def is_collision(self, pt=None):
        """
        Check for collision.
        :param self: list
        :param pt: bool
        :return: bool
        """
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.width - BLOCK_SIZE or pt.x < 0 or pt.y > self.height - BLOCK_SIZE or pt.y < 0:
            return True
        # hits self
        if pt in self.snake[1:]:
            return True

        return False


    def _update_ui(self):
        """
        Update the user interface.
        :return: None
        """
        self.display.fill(BLACK)

        # draw the snake
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        # draw the food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # draw the score in the upper left
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def _move(self, action):
        """
        Move the snake head
        :param action: move (tuple)
        :return: None
        """
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = point(x, y)
