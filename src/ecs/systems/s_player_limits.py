import pygame
import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_player_limits(world:esper.World, screen:pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CVelocity, CSurface, CTagPlayer)
    
    c_t:CTransform
    c_v:CVelocity
    c_s:CSurface
    
    for entity, (c_t, c_v, c_s, c_e) in components:
        player_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if not screen_rect.contains(player_rect):
            player_rect.clamp_ip(screen_rect)
            c_t.pos.xy = player_rect.topleft
