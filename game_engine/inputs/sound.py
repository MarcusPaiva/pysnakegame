import pygame


class SoundEffect:
    def __init__(self, file:str):
        self.__sound = pygame.mixer.Sound(file)

    def set_volume(self, value:float):
        self.__sound.set_volume(value)
        return self

    def play(self):
        self.__sound.play(0)

class Music:

    def __init__(self, file:str):
        self.__sound = pygame.mixer.music
        self.__sound.load(file)

    def set_volume(self, value:float):
        self.__sound.set_volume(value)

    def play_loop(self):
        self.__sound.play(-1,self.__sound.get_pos())

    def stop_loop(self):
        self.__sound.stop()

    def pause_loop(self):
        self.__sound.pause()

    def resume_loop(self):
        self.__sound.unpause()