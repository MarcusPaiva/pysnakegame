import pygame


class SoundEffect:
    def __init__(self, file:str):
        self.__sound = pygame.mixer.Sound(file)

    def set_volume(self, value:float):
        self.__sound.set_volume(value)
        return self

    def play(self):
        self.__sound.play(0)
        return self

class Music:

    def __init__(self, file:str):
        self.__sound = pygame.mixer.music
        self.__sound.load(file)

    def set_volume(self, value:float):
        self.__sound.set_volume(value)
        return self

    def play_loop(self):
        self.__sound.play(-1,0.0)
        return self

    def stop_loop(self):
        self.__sound.stop()
        return self

    def pause_loop(self):
        self.__sound.pause()
        return self

    def resume_loop(self):
        self.__sound.unpause()
        return self