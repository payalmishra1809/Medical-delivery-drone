import pygame
import random
import math
import os
import numpy as np

# Game Variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)
display_width = 1400
display_height = 800
FPS = 60
pipe_gap = 200
between_pipe = 200
pipe_width = 100
pipe_speed = 6
velocity = 10
pipe_count = display_width // (pipe_width + between_pipe) + 2

# Genetic Variables
population = 350
hidden_nodes = 8
inp = 4  # inputs + bias
bias1 = np.random.uniform()
bias2 = np.random.uniform()

# Neural Network and Genetic Algorithm Functions
def sigmoid(value):
    value = float(math.exp(-value))
    value = float(value + 1)
    value = float(1/value)
    return value

def nn(arr, paras, bias2):
    hidden_activations = np.dot(arr, paras[0])
    hidden_activations = [bias2] + list(map(sigmoid, hidden_activations))
    return sigmoid(np.dot(hidden_activations, paras[1]))

def mutate(master):
    mutation = np.random.normal(scale=1)
    return (master + mutation)

def make_parameters(master, population):
    para_list = [master]
    for _ in range(population - 1):
        para_list.append(mutate(np.asarray(master)))
    return para_list

# Pygame Sprite Classes
class Bird(pygame.sprite.Sprite):
    def __init__(self, x_loc, y_loc, velocity):
        super().__init__()
        self.velocity = velocity
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.image = pygame.image.load(os.path.join('assets', 'index.png')).convert()
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (x_loc, y_loc)
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.rect.y += self.velocity
        self.velocity = self.velocity + 1
    def jump(self):
        self.velocity = -10
    def boundary_collision(self):
        return self.rect.bottom + 100 >= display_height or self.rect.top <= 0

class UpperPipe(pygame.sprite.Sprite):
    def __init__(self, pipe_x, pipe_height, pipe_speed):
        super().__init__()
        self.pipe_speed = pipe_speed
        self.pipe_height = pipe_height
        self.image = pygame.Surface((pipe_width, pipe_height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = pipe_x
        self.rect.y = 0

class LowerPipe(pygame.sprite.Sprite):
    def __init__(self, pipe_x, pipe_height, pipe_speed):
        super().__init__()
        self.pipe_speed = pipe_speed
        self.image = pygame.Surface((pipe_width, display_height - (pipe_gap + pipe_height)))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = pipe_x
        self.rect.y = pipe_height + pipe_gap

# Main Game Initialization
pygame.init()
gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
bird_list = []
pipe_group = pygame.sprite.Group()

# Main Game Loop (simplified)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    gameDisplay.fill(WHITE)
    # Update and draw sprites here
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
