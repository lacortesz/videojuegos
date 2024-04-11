import pygame

class CEnemySpawner:
    def __init__(self, level:dict) -> None:
        self.ahora:float = 0
        self.events:list[Event] = []       
        for event in level["enemy_spawn_events"]:
            self.events.append(Event(event))       
            
class Event:
    def __init__(self, event:dict) -> None:
        self.time:float = event["time"]
        self.enemy_type:str = event["enemy_type"]
        self.position:pygame.Vector2 = pygame.Vector2(event["position"]["x"], event["position"]["y"])
        self.actived = False