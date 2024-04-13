import pygame
import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet


def system_bullet_limits(world:esper.World, screen:pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CVelocity, CSurface, CTagBullet)
        
    for entity, (c_t, c_v, c_s, c_e) in components:
        bullet_rect = c_s.surf.get_rect(topleft=c_t.pos)
        if not screen_rect.contains(bullet_rect):
            world.delete_entity(entity)

