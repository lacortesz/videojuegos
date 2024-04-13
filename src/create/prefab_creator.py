import math
import random
import esper
import pygame
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.tags.c_tag_bullet import CTagBullet
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

def create_enemy_square(ecs_world:esper.World, position:pygame.Vector2, enemy_info:dict):
    
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
    ecs_world.add_component(enemy_entity, CTagEnemy())
    
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
    world.add_component(player_entity, CTagPlayer())
        
    return player_entity

def create_input_player(world:esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()
    input_fire = world.create_entity()
    
    world.add_component(input_left, CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right, CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    world.add_component(input_up, CInputCommand("PLAYER_UP", pygame.K_UP)), 
    world.add_component(input_down, CInputCommand("PLAYER_DOWN", pygame.K_DOWN))
    world.add_component(input_fire, CInputCommand("PLAYER_FIRE", pygame.BUTTON_LEFT))

def create_bullet(world:esper.World, bullet_info:dict, player_position:pygame.Vector2, player_size:pygame.Vector2, mouse_position:pygame.Vector2):
    size = pygame.Vector2(bullet_info["size"]["x"] ,
                          bullet_info["size"]["y"] )
    color = pygame.Color(bullet_info["color"]["r"],
                           bullet_info["color"]["b"],
                           bullet_info["color"]["g"])
    pos = pygame.Vector2(player_position.x + (player_size[0]/2), player_position.y + player_size[1]/2)
    vel = (mouse_position - player_position)
    vel = vel.normalize() * bullet_info["velocity"]
    
    bullet_entity = create_square(world, size, pos, vel, color)
    world.add_component(bullet_entity, CTagBullet())
