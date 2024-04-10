import random
import esper
import pygame
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer

def create_square(ecs_world:esper.World, size:pygame.Vector2,
                   pos:pygame.Vector2, vel:pygame.Vector2, col:pygame.Color) -> int:
    
    cuad_entity = ecs_world.create_entity()
    ecs_world.add_component(cuad_entity, CSurface(size, col))
    ecs_world.add_component(cuad_entity, CTransform(pos))
    ecs_world.add_component(cuad_entity, CVelocity(vel))
    return cuad_entity
    
def create_level(ecs_world:esper.World, level):
    level_entity = ecs_world.create_entity()
    ecs_world.add_component(level_entity, CEnemySpawner(level))

def create_enemy_spawner(ecs_world:esper.World, position:pygame.Vector2, enemy_info:dict):
    
    size = pygame.Vector2(enemy_info["size"]["x"],
                          enemy_info["size"]["y"])
    color = pygame.Color(enemy_info["color"]["r"], 
                          enemy_info["color"]["g"],
                          enemy_info["color"]["b"])
     
    vel_min = enemy_info["velocity_min"]
    vel_max = enemy_info["velocity_max"]

    if vel_min == vel_max:
        vel_range = vel_min
    else:
        vel_range = random.randrange(vel_min, vel_max)
    
    velocity = pygame.Vector2(random.choice([-vel_range, vel_range]), 
                            random.choice([-vel_range, vel_range]))

    enemy_entity = create_square(ecs_world, size, position, velocity, color)
    ecs_world.add_component(enemy_entity, CTagEnemy)
    
def create_player_square(world:esper.World, player_info:dict, player_lvl_info:dict) -> int:
    size = pygame.Vector2(player_info["size"]["x"] ,
                          player_info["size"]["y"] )
    color = pygame.Color(player_info["color"]["r"],
                           player_info["color"]["b"],
                           player_info["color"]["g"])
    pos = pygame.Vector2(player_lvl_info["position"]["x"] - (size.x/2),
                         player_lvl_info["position"]["y"]- (size.y/2))
    vel = pygame.Vector2(0,0)
    player_entity = create_square(world, size, pos, vel, color)
    world.add_component(player_entity, CTagPlayer)
    return player_entity