import pygame
from enum import Enum

class CCharger:
    def __init__(self, info:dict) -> None:    
        self.state = CChargerState.NotInitialized
        self.initialized = False
        self.on_charge = False
        self.counter = 0
        self.framerate = 1.0 / info["framerate"]
        self.current_time = self.framerate
        self.info = info
        self.current_entity = 0
        
        
class CChargerState(Enum):
    NotInitialized = 0
    Initialized = 1
    OnCharge = 2
    Charged = 3  

    