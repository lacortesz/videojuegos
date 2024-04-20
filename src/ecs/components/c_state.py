from enum import Enum

class CPlayerState:
    def __init__(self) -> None:
        self.state = PlayerState.IDLE
        
class PlayerState(Enum):
    IDLE = 0
    MOVE = 1
    
class CHunterState:
    def __init__(self) -> None:
        self.state = HunterState.IDLE

class HunterState(Enum):
    IDLE = 0
    MOVE = 1
        