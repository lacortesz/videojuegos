import random
import esper
import pygame
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_enemy_spawner import CEnemySpawner

def crear_cuadrado(ecs_world:esper.World, size:pygame.Vector2,
                   pos:pygame.Vector2, vel:pygame.Vector2, col:pygame.Color):
    
    cuad_entity = ecs_world.create_entity()
    ecs_world.add_component(cuad_entity, CSurface(size, col))
    ecs_world.add_component(cuad_entity, CTransform(pos))
    ecs_world.add_component(cuad_entity, CVelocity(vel))
    
def crear_level(ecs_world:esper.World, level):
    level_entity = ecs_world.create_entity()
    ecs_world.add_component(level_entity, CEnemySpawner(level))

def crear_cuadrado_enemigo(ecs_world:esper.World, position:pygame.Vector2, enemy:dict):
    
    vel_min = enemy["velocity_min"]
    vel_max = enemy["velocity_max"]
    
    if vel_min == vel_max:
        vel_range = vel_min
    else:
        vel_range = random.randrange(enemy["velocity_min"], enemy["velocity_max"])
    
    velocity = pygame.Vector2(random.choice([-vel_range, vel_range]), 
                            random.choice([-vel_range, vel_range]))

    crear_cuadrado(ecs_world, 
                   (enemy["size"]["x"], enemy["size"]["y"]),
                   position,
                   velocity,
                   (enemy["color"]["r"], enemy["color"]["g"], enemy["color"]["b"]))
    
    