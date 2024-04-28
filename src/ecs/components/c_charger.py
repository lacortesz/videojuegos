import pygame
from enum import Enum

class CCharger:
    def __init__(self, on_full_info:dict, on_charge_info:dict) -> None:    
        self.state = CChargerState.NotInitialized
        self.initialized = False
        self.on_charge = False
        self.counter = 0
        self.framerate = 1.0 / on_charge_info["framerate"]
        self.current_time = self.framerate
        self.full_info = on_full_info
        self.on_charge_info = on_charge_info
        self.current_entity = 0
        
        
class CChargerState(Enum):
    NotInitialized = 0
    Initialized = 1
    OnCharge = 2
    Charged = 3  

    