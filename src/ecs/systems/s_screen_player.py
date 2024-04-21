import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_screen_player(world:esper.World, screen:pygame.Surface):
    screen_player_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CVelocity, CTagPlayer)
    for _, (transform, surface, velocity, _) in components:
        player_rect = CSurface.get_area_relative(surface.area, transform.pos)
        if not screen_player_rect.contains(player_rect):
            player_rect.clamp_ip(screen_player_rect)
            transform.pos.xy = player_rect.topleft