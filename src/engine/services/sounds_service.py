import pygame

class SoundsServices:
    def __init__(self) -> None:
        self._sounds = {}
    
    def play(self, path:str):
        if path not in self._sounds:
            self._sounds[path] = pygame.mixer.Sound(path)
        self._sounds[path].play()
    
    def play_loop(self, path:str):
        if path not in self._sounds:
            self._sounds[path] = pygame.mixer.Sound(path)
        self._sounds[path].play(-1)
    
    def stop(self, path:str):
        if path in self._sounds:
            self._sounds[path].stop()
    