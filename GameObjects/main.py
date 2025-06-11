import pygame

from game_stage import Stage

pygame.init()
screen = pygame.display.set_mode((1280, 720))

stage = Stage(screen)
stage.setup()
stage.loop()

pygame.quit()