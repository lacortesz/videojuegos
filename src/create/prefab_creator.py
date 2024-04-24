import math
import random
import esper
import pygame
from src.ecs.components.c_input_command import CInputCommand

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.tags.c_tag_asteroid import CTagEnemyAsteroid
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_hunter import CTagEnemyHunter
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator

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

def create_sprite(world:esper.World, pos:pygame.Vector2, vel:pygame.Vector2, surface:pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, CTransform(pos))
    world.add_component(sprite_entity, CVelocity(vel))
    world.add_component(sprite_entity, CSurface.from_surface(surface))
    return sprite_entity


def create_enemy_square(ecs_world:esper.World, position:pygame.Vector2, enemy_info:dict):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])     
    vel_min = enemy_info["velocity_min"]
    vel_max = enemy_info["velocity_max"]

    if vel_min == vel_max:
        vel_range = vel_min
    else:
        vel_range = random.randrange(vel_min, vel_max)
    
    velocity = pygame.Vector2(random.choice([-vel_range, vel_range]), 
                            random.choice([-vel_range, vel_range]))

    enemy_entity = create_sprite(ecs_world, position, velocity, enemy_surface)    
    ecs_world.add_component(enemy_entity, CTagEnemy())
    ecs_world.add_component(enemy_entity, CTagEnemyAsteroid())
    ServiceLocator.sounds_service.play(enemy_info["sound"])  

    
def create_player_square(world:esper.World, player_info:dict, player_lvl_info:dict) -> int:
    player_surface = ServiceLocator.images_service.get(player_info["image"])  
    size = player_surface.get_size()
    
    player_size = player_surface.get_size()
    
    player_size = (player_size[0] / player_info["animations"]["number_frames"], player_size[1])
    pos = pygame.Vector2(player_lvl_info["position"]["x"] - (player_size[0]/2), player_lvl_info["position"]["y"] - (player_size[1]/2))

    vel = pygame.Vector2(0,0)
    player_entity = create_sprite(world, pos, vel, player_surface)
    world.add_component(player_entity, CTagPlayer())
    world.add_component(player_entity, CAnimation(player_info["animations"]))
    world.add_component(player_entity, CPlayerState())
    
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
    bullet_surface = ServiceLocator.images_service.get(bullet_info["image"])  
    bullet_size = bullet_surface.get_rect().size
    pos = pygame.Vector2(player_position.x + (player_size[0]/2) - (bullet_size[0] / 2), 
                         player_position.y + (player_size[1]/2) - (bullet_size[0] / 2))
    
    player_position_center =  pygame.Vector2(player_position.x + (player_size[0]/2),
                                             player_position.y + (player_size[1]/2))
    vel = (mouse_position - player_position_center)
    vel = vel.normalize() * bullet_info["velocity"]
    
    bullet_entity = create_sprite(world, pos, vel, bullet_surface)
    world.add_component(bullet_entity, CTagBullet())
    ServiceLocator.sounds_service.play(bullet_info["sound"])  


def create_enemy_hunter(ecs_world:esper.World, position:pygame.Vector2, enemy_info:dict):
    hunter_surface = ServiceLocator.images_service.get(enemy_info["image"])  
    velocity = pygame.Vector2(0,0)      
    
    hunter_entity = create_sprite(ecs_world, position, velocity, hunter_surface)    
    ecs_world.add_component(hunter_entity, CHunterState(position))
    ecs_world.add_component(hunter_entity, CAnimation(enemy_info["animations"]))
    ecs_world.add_component(hunter_entity, CTagEnemy())
    ecs_world.add_component(hunter_entity, CTagEnemyHunter())
    
def create_explosion(world:esper.World, pos:pygame.Vector2, explosion_info:dict):
    explosion_surface = ServiceLocator.images_service.get(explosion_info["image"])  
    vel = pygame.Vector2(0,0)
    explosion_entity = create_sprite(world, pos, vel, explosion_surface)
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity, CAnimation(explosion_info["animations"]))
    ServiceLocator.sounds_service.play(explosion_info["sound"])
    
    return explosion_entity