import pygame
import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet


def system_bullet_limits(world:esper.World, screen:pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CVelocity, CSurface, CTagBullet)
    
    c_t:CTransform
    c_v:CVelocity
    c_s:CSurface
    
    for entity, (c_t, c_v, c_s, c_e) in components:
        cuad_rect = c_s.surf.get_rect(topleft=c_t.pos)
        if cuad_rect.left < 0 or \
            cuad_rect.right > screen_rect.width or \
            cuad_rect.top < 0 or \
            cuad_rect.bottom > screen_rect.height: 
            world.delete_entity(entity)

