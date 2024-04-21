import esper
import pygame
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy



def system_collission_player_enemy(world:esper.World, player_entity:int, level:dict, explosion_info:dict, player_info:dict):
    components = world.get_components(CSurface, CTransform, CTagEnemy)
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    pl_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)
    
    for enemy_entity, (c_s, c_t, _) in components:       
        ene_rect = c_s.area.copy()
        ene_rect.topleft = c_t.pos
        if ene_rect.colliderect(pl_rect):
            world.delete_entity(enemy_entity)
            
            player_size =  pl_s.surf.get_size()    
               
            player_size = (player_size[0] / player_info["animations"]["number_frames"], player_size[1])
    
            pos = pygame.Vector2(level["player_spawn"]["position"]["x"] - (player_size[0]/2), level["player_spawn"]["position"]["y"] - (player_size[1]/2)) 
                                   
            pl_t.pos.x = level["player_spawn"]["position"]["x"] - (player_size[0] /2)
            pl_t.pos.y = level["player_spawn"]["position"]["y"] - (player_size[1] /2)

            create_explosion(world, ene_rect, explosion_info)
            
            