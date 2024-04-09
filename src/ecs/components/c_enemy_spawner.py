import pygame

class CEnemySpawner:
    def __init__(self, level:dict) -> None:
        self.ahora:float = 0
        self.events:list[Event] = []       
        for event in level["enemy_spawn_events"]:
            self.events.append(Event(event))       
        
        '''    temp = {}
            temp["time"] = event["time"]
            temp["enemy_type"] = event["enemy_type"] 
            position = {}
            position["x"] = event["position"]["x"]
            position["y"] = event["position"]["y"]
            temp["position"] = position
            temp["actived"] = False
            self.events.append(temp)'''
            
class Event:
    def __init__(self, event:dict) -> None:
        self.time:float = event["time"]
        self.enemy_type:str = event["enemy_type"]
        self.position:pygame.Vector2 = pygame.Vector2(event["position"]["x"], event["position"]["y"])
        self.actived = False